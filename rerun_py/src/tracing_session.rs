//! Python-side bridge for the `tracing_session()` context manager.
//!
//! See `rerun_py/rerun_sdk/rerun/_tracing_session.py` for the user-facing API.
//!
//! The bridge has two pyo3 entry points:
//!
//! - [`get_tracing_session_var`] — exposes the Python `ContextVar` whose current value is
//!   read by the Rust-side [`re_perf_telemetry::current_rerun_session_id`] on every
//!   outbound gRPC request. The `TraceStateEnricher` uses it to merge
//!   `rerun_session_id=<id>` into the `tracestate` header.
//!
//! - [`is_telemetry_active`] — lets the Python context manager fail fast with an
//!   actionable error when `TELEMETRY_ENABLED` is not truthy. Without an active
//!   telemetry stack, the `TracingInjectorInterceptor` has no valid OTel context to
//!   inject from, so a session id would never reach the wire.
//!
//! [`re_perf_telemetry::current_rerun_session_id`]: https://docs.rs/re_perf_telemetry

use pyo3::{Py, PyAny, PyResult, Python, pyfunction};

/// Return `True` if the rerun telemetry stack initialized successfully.
///
/// `tracing_session()` requires this to be true; otherwise the W3C propagator
/// is not registered and the session id has no transport.
#[pyfunction]
#[pyo3(name = "_is_telemetry_active")]
pub fn is_telemetry_active() -> bool {
    #[cfg(feature = "perf_telemetry")]
    {
        crate::python_bridge::telemetry_active()
    }
    #[cfg(not(feature = "perf_telemetry"))]
    {
        false
    }
}

/// Return the `ContextVar` carrying the active rerun session id.
///
/// Set by the `tracing_session()` context manager and read on every outbound
/// gRPC call to merge `rerun_session_id=<id>` into the W3C `tracestate` header.
///
/// Returns `None` when `perf_telemetry` is disabled.
#[pyfunction]
#[pyo3(name = "_get_tracing_session_var")]
pub fn get_tracing_session_var(py: Python<'_>) -> PyResult<Py<PyAny>> {
    #[cfg(feature = "perf_telemetry")]
    {
        let context_var = re_perf_telemetry::get_rerun_session_var(py)?;
        Ok(context_var.unbind())
    }
    #[cfg(not(feature = "perf_telemetry"))]
    {
        Ok(py.None())
    }
}

/// Increment the process-wide active-tracing-session gate. Called by `tracing_session().__enter__`.
#[pyfunction]
#[pyo3(name = "_inc_active_tracing_sessions")]
pub fn inc_active_tracing_sessions() {
    #[cfg(feature = "perf_telemetry")]
    {
        re_perf_telemetry::inc_active_tracing_session_count();
    }
}

/// Decrement the process-wide active-tracing-session gate. Called by `tracing_session().__exit__`.
#[pyfunction]
#[pyo3(name = "_dec_active_tracing_sessions")]
pub fn dec_active_tracing_sessions() {
    #[cfg(feature = "perf_telemetry")]
    {
        re_perf_telemetry::dec_active_tracing_session_count();
    }
}

/// Emit `rerun tracing session started: <rerun_session_id>` through the Rust `tracing` stack at INFO level.
#[pyfunction]
#[pyo3(name = "_log_tracing_session_started")]
pub fn log_tracing_session_started(rerun_session_id: &str) {
    tracing::info!("rerun tracing session started: {rerun_session_id}");
}
