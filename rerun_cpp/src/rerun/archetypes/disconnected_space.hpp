// DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/cpp/mod.rs
// Based on "crates/re_types/definitions/rerun/archetypes/disconnected_space.fbs".

#pragma once

#include "../arrow.hpp"
#include "../component_batch.hpp"
#include "../components/disconnected_space.hpp"
#include "../data_cell.hpp"
#include "../result.hpp"

#include <cstdint>
#include <utility>
#include <vector>

namespace rerun {
    namespace archetypes {
        /// Specifies that the entity path at which this is logged is disconnected from its parent.
        ///
        /// This is useful for specifying that a subgraph is independent of the rest of the scene.
        ///
        /// If a transform or pinhole is logged on the same path, this archetype's components
        /// will be ignored.
        ///
        /// ## Example
        ///
        /// ```cpp,ignore
        /// // Disconnect two spaces.
        ///
        /// #include <rerun.hpp>
        ///
        /// namespace rr = rerun;
        ///
        /// int main() {
        ///     auto rec = rr::RecordingStream("rerun_example_disconnected_space");
        ///     rec.connect("127.0.0.1:9876").throw_on_failure();
        ///
        ///     // These two points can be projected into the same space..
        ///     rec.log("world/room1/point", rr::Points3D(rr::datatypes::Vec3D{0.0f, 0.0f, 0.0f}));
        ///     rec.log("world/room2/point", rr::Points3D(rr::datatypes::Vec3D{1.0f, 1.0f, 1.0f}));
        ///
        ///     // ..but this one lives in a completely separate space!
        ///     rec.log("world/wormhole", rr::DisconnectedSpace(true));
        ///     rec.log("world/wormhole/point",
        ///     rr::Points3D(rr::datatypes::Vec3D{2.0f, 2.0f, 2.0f}));
        /// }
        /// ```
        struct DisconnectedSpace {
            rerun::components::DisconnectedSpace disconnected_space;

            /// Name of the indicator component, used to identify the archetype when converting to a
            /// list of components.
            static const char INDICATOR_COMPONENT_NAME[];

          public:
            DisconnectedSpace() = default;

            DisconnectedSpace(rerun::components::DisconnectedSpace _disconnected_space)
                : disconnected_space(std::move(_disconnected_space)) {}

            /// Returns the number of primary instances of this archetype.
            size_t num_instances() const {
                return 1;
            }

            /// Collections all component lists into a list of component collections. *Attention:*
            /// The returned vector references this instance and does not take ownership of any
            /// data. Adding any new components to this archetype will invalidate the returned
            /// component lists!
            std::vector<AnonymousComponentBatch> as_component_batches() const;
        };
    } // namespace archetypes
} // namespace rerun
