use std::collections::VecDeque;
use std::sync::Arc;

use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;

use re_byte_size::SizeBytes as _;
use re_chunk::{Chunk, ChunkId};
use re_chunk_store::{ChunkStore, ChunkStoreConfig, ChunkStoreHandle, LazyStore};
use re_log_types::{StoreId, StoreKind};
use re_sorbet::ChunkColumnDescriptors;

use super::error::ChunkPipelineError;
use super::py_stream::PyLazyChunkStreamInternal;
use super::stream::LazyChunkStream;
use super::{ChunkStream, ChunkStreamFactory};
use crate::catalog::PySchemaInternal;
use crate::chunk::PyChunkInternal;

/// A chunk store, either fully materialized or lazily backed by an RRD file.
///
/// This is a newtype around [`ChunkStoreInternal`] because PyO3 cannot derive
/// `#[pyclass]` on enums whose variants hold non-PyO3 types.
///
/// Implements [`ChunkStreamFactory`] so `stream()` can hand `self.clone()`
/// straight to [`LazyChunkStream::from_factory`] -- no intermediate wrapper.
#[pyclass(
    frozen,
    name = "ChunkStoreInternal",
    module = "rerun_bindings.rerun_bindings"
)]
#[derive(Clone)]
pub struct PyChunkStoreInternal(ChunkStoreInternal);

/// Fully materialized or lazily-backed chunk store.
#[derive(Clone)]
enum ChunkStoreInternal {
    /// All chunks are in memory.
    InMemory(ChunkStoreHandle),

    /// Index loaded from a [`ChunkProvider`][re_log_encoding::ChunkProvider]'s manifest, chunks
    /// loaded on demand. The provider's `source()` is used in diagnostic messages on load failure.
    Indexed(Arc<LazyStore>),
}

impl ChunkStoreInternal {
    fn schema(&self) -> ChunkColumnDescriptors {
        match self {
            Self::InMemory(handle) => handle.read().schema().chunk_column_descriptors(),
            Self::Indexed(lazy) => lazy.schema().chunk_column_descriptors(),
        }
    }
}

impl PyChunkStoreInternal {
    pub fn in_memory(store: ChunkStore) -> Self {
        Self(ChunkStoreInternal::InMemory(ChunkStoreHandle::new(store)))
    }

    pub fn indexed(lazy: LazyStore) -> Self {
        Self(ChunkStoreInternal::Indexed(Arc::new(lazy)))
    }
}

#[pymethods]
impl PyChunkStoreInternal {
    /// Build a ChunkStore from a list of chunks.
    #[staticmethod]
    #[expect(clippy::needless_pass_by_value)] // PyO3 requires owned Vec for #[staticmethod]
    fn from_chunks(chunks: Vec<PyRef<'_, PyChunkInternal>>) -> PyResult<Self> {
        let store_id = StoreId::random(StoreKind::Recording, "chunk-store");
        let mut store = ChunkStore::new(store_id, ChunkStoreConfig::ALL_DISABLED);
        for py_chunk in &chunks {
            store
                .insert_chunk(py_chunk.inner())
                .map_err(|err| PyRuntimeError::new_err(err.to_string()))?;
        }
        Ok(Self::in_memory(store))
    }

    /// The schema describing all columns in this store.
    fn schema(&self) -> PySchemaInternal {
        PySchemaInternal {
            columns: self.0.schema().into(),
            metadata: Default::default(),
        }
    }

    /// The total number of chunks in this store (virtual and physical).
    fn num_chunks(&self) -> usize {
        match &self.0 {
            ChunkStoreInternal::InMemory(handle) => handle.read().num_physical_chunks(),
            ChunkStoreInternal::Indexed(lazy) => lazy.manifest().num_chunks(),
        }
    }

    /// Compact, deterministic summary of every chunk in the store for snapshot testing.
    ///
    /// Each line describes one chunk:
    /// `{entity_path} rows={n} bytes={…} static={bool} timelines=[…] cols=[…]`
    ///
    /// Chunks are sorted by `(entity_path, !is_static)`. The `cols` list
    /// combines timeline and component column names (sorted), excluding
    /// `rerun.controls` columns.
    ///
    /// For lazily-loaded stores, this forces loading all chunk data from disk.
    //TODO(ab): should that be implemented on `re_chunk_store::ChunkStore` directly?
    fn summary(&self) -> PyResult<String> {
        let chunks = self.collect_all_chunks()?;
        Ok(summary_from_chunks(&chunks))
    }

    /// Return a lazy stream over all chunks in this store.
    fn stream(&self) -> PyLazyChunkStreamInternal {
        // Each compile() snapshots the store's current physical chunks.
        PyLazyChunkStreamInternal::new(LazyChunkStream::from_factory(self.clone()))
    }
}

impl PyChunkStoreInternal {
    /// Collect all chunks from either variant, loading lazily if needed.
    fn collect_all_chunks(&self) -> PyResult<Vec<Arc<Chunk>>> {
        match &self.0 {
            ChunkStoreInternal::InMemory(handle) => {
                Ok(handle.read().iter_physical_chunks().cloned().collect())
            }

            ChunkStoreInternal::Indexed(lazy) => lazy
                .load_all_chunks()
                .map_err(|err| PyRuntimeError::new_err(err.to_string())),
        }
    }
}

impl ChunkStreamFactory for PyChunkStoreInternal {
    fn create(&self) -> Result<Box<dyn ChunkStream>, ChunkPipelineError> {
        match &self.0 {
            ChunkStoreInternal::InMemory(handle) => {
                let chunks = handle.read().iter_physical_chunks().cloned().collect();
                Ok(Box::new(VecChunkStream { chunks, pos: 0 }))
            }
            ChunkStoreInternal::Indexed(lazy) => {
                Ok(Box::new(IndexedChunkStream::new(Arc::clone(lazy))))
            }
        }
    }
}

/// Build a summary from a list of chunks.
fn summary_from_chunks(chunks: &[Arc<Chunk>]) -> String {
    let mut chunks: Vec<&Chunk> = chunks.iter().map(|c| c.as_ref()).collect();
    chunks.sort_by(|a, b| {
        a.entity_path()
            .cmp(b.entity_path())
            .then_with(|| a.is_static().cmp(&b.is_static()).reverse())
    });

    let mut lines = Vec::new();
    for chunk in &chunks {
        let mut timelines: Vec<&str> = chunk.timelines().keys().map(|t| t.as_str()).collect();
        timelines.sort();

        let mut cols: Vec<&str> = chunk
            .timelines()
            .keys()
            .map(|t| t.as_str())
            .chain(
                chunk
                    .components()
                    .component_descriptors()
                    .map(|d| d.display_name()),
            )
            .collect();
        cols.sort();

        let timelines_str = timelines
            .iter()
            .map(|t| format!("'{t}'"))
            .collect::<Vec<_>>()
            .join(", ");
        let cols_str = cols
            .iter()
            .map(|c| format!("'{c}'"))
            .collect::<Vec<_>>()
            .join(", ");
        let is_static = if chunk.is_static() { "True" } else { "False" };
        let bytes = re_format::format_bytes(chunk.total_size_bytes() as f64);

        lines.push(format!(
            "{entity_path} rows={rows} bytes={bytes} static={is_static} timelines=[{timelines_str}] cols=[{cols_str}]",
            entity_path = chunk.entity_path(),
            rows = chunk.num_rows(),
        ));
    }

    lines.join("\n")
}

// --- Streaming ---

/// Pull-based stream over a pre-collected `Vec` of chunks.
struct VecChunkStream {
    chunks: Vec<Arc<Chunk>>,
    pos: usize,
}

// Vec<Arc<Chunk>> + usize are Send.
impl ChunkStream for VecChunkStream {
    fn next(&mut self) -> Result<Option<Arc<Chunk>>, ChunkPipelineError> {
        if self.pos < self.chunks.len() {
            let chunk = self.chunks[self.pos].clone();
            self.pos += 1;
            Ok(Some(chunk))
        } else {
            Ok(None)
        }
    }
}

/// Streaming loader for an indexed (lazy) [`ChunkStore`].
///
/// Pulls chunks from the underlying [`ChunkProvider`][re_log_encoding::ChunkProvider] in
/// byte-budgeted batches so resident memory stays bounded regardless of total recording size.
//TODO(RR-4545): this is hardly an optimal strategy. We need the ChunkProvider to expose a streaming
// API so that specific optimizations can be applied (e.g. adjacency for RRD, parallelism for
// segments, etc.)
struct IndexedChunkStream {
    lazy: Arc<LazyStore>,
    chunk_ids: Vec<ChunkId>,
    next_id: usize,
    buffer: VecDeque<Arc<Chunk>>,
}

impl IndexedChunkStream {
    /// Target bytes per batch — bounds memory while still letting `read_chunks` coalesce.
    const BATCH_BYTE_BUDGET: u64 = 8 * 1024 * 1024;

    fn new(lazy: Arc<LazyStore>) -> Self {
        let chunk_ids = lazy.manifest().col_chunk_ids().to_vec();
        Self {
            lazy,
            chunk_ids,
            next_id: 0,
            buffer: VecDeque::new(),
        }
    }

    /// End index (exclusive) of the next batch starting at `self.next_id`,
    /// chosen so the cumulative byte size stays under [`Self::BATCH_BYTE_BUDGET`].
    /// Always advances by at least one chunk to guarantee progress on huge chunks.
    fn next_batch_end(&self) -> usize {
        let sizes = self.lazy.manifest().col_chunk_byte_size();
        let mut end = self.next_id;
        let mut accumulated: u64 = 0;
        while end < self.chunk_ids.len() {
            let size = self
                .lazy
                .chunk_row_index(&self.chunk_ids[end])
                .map(|row| sizes[row])
                .unwrap_or(0);
            if end > self.next_id && accumulated.saturating_add(size) > Self::BATCH_BYTE_BUDGET {
                break;
            }
            accumulated = accumulated.saturating_add(size);
            end += 1;
        }
        end
    }
}

impl ChunkStream for IndexedChunkStream {
    fn next(&mut self) -> Result<Option<Arc<Chunk>>, ChunkPipelineError> {
        loop {
            if let Some(chunk) = self.buffer.pop_front() {
                return Ok(Some(chunk));
            }
            if self.next_id >= self.chunk_ids.len() {
                return Ok(None);
            }

            let end = self.next_batch_end();
            let ids = &self.chunk_ids[self.next_id..end];
            let chunks =
                self.lazy
                    .load_chunks(ids)
                    .map_err(|err| ChunkPipelineError::IndexedLoad {
                        from: self.lazy.source(),
                        reason: err.to_string(),
                    })?;
            self.next_id = end;
            self.buffer = chunks.into();
        }
    }
}
