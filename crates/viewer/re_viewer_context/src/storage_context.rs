use crate::{StoreHub, TableStores};

/// Provides read-only references over the different kinds of storage used throughout the viewer.
pub struct StorageContext<'a> {
    pub hub: &'a StoreHub,
    pub bundle: &'a re_entity_db::StoreBundle,
    pub tables: &'a TableStores,
}
