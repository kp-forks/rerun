// DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/cpp/mod.rs
// Based on "crates/re_types/definitions/rerun/archetypes/boxes2d.fbs".

#pragma once

#include "../arrow.hpp"
#include "../component_batch.hpp"
#include "../components/class_id.hpp"
#include "../components/color.hpp"
#include "../components/draw_order.hpp"
#include "../components/half_sizes2d.hpp"
#include "../components/instance_key.hpp"
#include "../components/position2d.hpp"
#include "../components/radius.hpp"
#include "../components/text.hpp"
#include "../data_cell.hpp"
#include "../result.hpp"

#include <cstdint>
#include <optional>
#include <utility>
#include <vector>

namespace rerun {
    namespace archetypes {
        /// A batch of 2d boxes with half-extents and optional center, rotations, rotations, colors
        /// etc.
        ///
        /// ## Example
        ///
        /// Simple 2D boxes:
        /// ```cpp,ignore
        /// // Log some simple 2D boxes.
        ///
        /// #include <rerun.hpp>
        ///
        /// namespace rr = rerun;
        ///
        /// int main() {
        ///     auto rec = rr::RecordingStream("rerun_example_box2d");
        ///     rec.connect("127.0.0.1:9876").throw_on_failure();
        ///
        ///     rec.log("simple", rr::Boxes2D::from_mins_and_sizes({{-1.f, -1.f}}, {{2.f, 2.f}}));
        ///
        ///     // Log an extra rect to set the view bounds
        ///     rec.log("bounds", rr::Boxes2D::from_sizes({{4.f, 3.f}}));
        /// }
        /// ```
        struct Boxes2D {
            /// All half-extents that make up the batch of boxes.
            std::vector<rerun::components::HalfSizes2D> half_sizes;

            /// Optional center positions of the boxes.
            std::optional<std::vector<rerun::components::Position2D>> centers;

            /// Optional radii for the lines that make up the boxes.
            std::optional<std::vector<rerun::components::Radius>> radii;

            /// Optional colors for the boxes.
            std::optional<std::vector<rerun::components::Color>> colors;

            /// Optional text labels for the boxes.
            std::optional<std::vector<rerun::components::Text>> labels;

            /// An optional floating point value that specifies the 2D drawing order.
            /// Objects with higher values are drawn on top of those with lower values.
            ///
            /// The default for 2D boxes is 10.0.
            std::optional<rerun::components::DrawOrder> draw_order;

            /// Optional `ClassId`s for the boxes.
            ///
            /// The class ID provides colors and labels if not specified explicitly.
            std::optional<std::vector<rerun::components::ClassId>> class_ids;

            /// Unique identifiers for each individual boxes in the batch.
            std::optional<std::vector<rerun::components::InstanceKey>> instance_keys;

            /// Name of the indicator component, used to identify the archetype when converting to a
            /// list of components.
            static const char INDICATOR_COMPONENT_NAME[];

          public:
            // Extensions to generated type defined in 'boxes2d_ext.cpp'

            /// Creates new `Boxes2D` with `half_sizes` centered around the local origin.
            static Boxes2D from_half_sizes(std::vector<components::HalfSizes2D> _half_sizes) {
                Boxes2D boxes;
                boxes.half_sizes = std::move(_half_sizes);
                return boxes;
            }

            /// Creates new `Boxes2D` with `centers` and `half_sizes`.
            static Boxes2D from_centers_and_half_sizes(
                std::vector<components::Position2D> _centers,
                std::vector<components::HalfSizes2D> _half_sizes
            ) {
                return Boxes2D::from_half_sizes(std::move(_half_sizes))
                    .with_centers(std::move(_centers));
            }

            /// Creates new `Boxes2D` with `half_sizes` created from (full) sizes.
            ///
            /// TODO(#3285): Does *not* preserve data as-is and instead creates half-sizes from the
            /// input data.
            static Boxes2D from_sizes(const std::vector<datatypes::Vec2D>& sizes);

            /// Creates new `Boxes2D` with `centers` and `half_sizes` created from centers and
            /// (full) sizes.
            ///
            /// TODO(#3285): Does *not* preserve data as-is and instead creates centers and
            /// half-sizes from the input data.
            static Boxes2D from_centers_and_sizes(
                std::vector<components::Position2D> centers,
                const std::vector<datatypes::Vec2D>& sizes
            ) {
                return from_sizes(sizes).with_centers(std::move(centers));
            }

            /// Creates new `Boxes2D` with `half_sizes` and `centers` created from minimums and
            /// (full) sizes.
            ///
            /// TODO(#3285): Does *not* preserve data as-is and instead creates centers and
            /// half-sizes from the input data.
            static Boxes2D from_mins_and_sizes(
                const std::vector<datatypes::Vec2D>& mins,
                const std::vector<datatypes::Vec2D>& sizes
            );

          public:
            Boxes2D() = default;

            /// Optional center positions of the boxes.
            Boxes2D& with_centers(std::vector<rerun::components::Position2D> _centers) {
                centers = std::move(_centers);
                return *this;
            }

            /// Optional center positions of the boxes.
            Boxes2D& with_centers(rerun::components::Position2D _centers) {
                centers = std::vector(1, std::move(_centers));
                return *this;
            }

            /// Optional radii for the lines that make up the boxes.
            Boxes2D& with_radii(std::vector<rerun::components::Radius> _radii) {
                radii = std::move(_radii);
                return *this;
            }

            /// Optional radii for the lines that make up the boxes.
            Boxes2D& with_radii(rerun::components::Radius _radii) {
                radii = std::vector(1, std::move(_radii));
                return *this;
            }

            /// Optional colors for the boxes.
            Boxes2D& with_colors(std::vector<rerun::components::Color> _colors) {
                colors = std::move(_colors);
                return *this;
            }

            /// Optional colors for the boxes.
            Boxes2D& with_colors(rerun::components::Color _colors) {
                colors = std::vector(1, std::move(_colors));
                return *this;
            }

            /// Optional text labels for the boxes.
            Boxes2D& with_labels(std::vector<rerun::components::Text> _labels) {
                labels = std::move(_labels);
                return *this;
            }

            /// Optional text labels for the boxes.
            Boxes2D& with_labels(rerun::components::Text _labels) {
                labels = std::vector(1, std::move(_labels));
                return *this;
            }

            /// An optional floating point value that specifies the 2D drawing order.
            /// Objects with higher values are drawn on top of those with lower values.
            ///
            /// The default for 2D boxes is 10.0.
            Boxes2D& with_draw_order(rerun::components::DrawOrder _draw_order) {
                draw_order = std::move(_draw_order);
                return *this;
            }

            /// Optional `ClassId`s for the boxes.
            ///
            /// The class ID provides colors and labels if not specified explicitly.
            Boxes2D& with_class_ids(std::vector<rerun::components::ClassId> _class_ids) {
                class_ids = std::move(_class_ids);
                return *this;
            }

            /// Optional `ClassId`s for the boxes.
            ///
            /// The class ID provides colors and labels if not specified explicitly.
            Boxes2D& with_class_ids(rerun::components::ClassId _class_ids) {
                class_ids = std::vector(1, std::move(_class_ids));
                return *this;
            }

            /// Unique identifiers for each individual boxes in the batch.
            Boxes2D& with_instance_keys(std::vector<rerun::components::InstanceKey> _instance_keys
            ) {
                instance_keys = std::move(_instance_keys);
                return *this;
            }

            /// Unique identifiers for each individual boxes in the batch.
            Boxes2D& with_instance_keys(rerun::components::InstanceKey _instance_keys) {
                instance_keys = std::vector(1, std::move(_instance_keys));
                return *this;
            }

            /// Returns the number of primary instances of this archetype.
            size_t num_instances() const {
                return half_sizes.size();
            }

            /// Collections all component lists into a list of component collections. *Attention:*
            /// The returned vector references this instance and does not take ownership of any
            /// data. Adding any new components to this archetype will invalidate the returned
            /// component lists!
            std::vector<AnonymousComponentBatch> as_component_batches() const;
        };
    } // namespace archetypes
} // namespace rerun
