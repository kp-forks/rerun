// DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/cpp/mod.rs
// Based on "crates/store/re_types/definitions/rerun/blueprint/components/force_strength.fbs".

#pragma once

#include "../../component_descriptor.hpp"
#include "../../datatypes/float64.hpp"
#include "../../result.hpp"

#include <cstdint>
#include <memory>

namespace rerun::blueprint::components {
    /// **Component**: The strength of a given force.
    ///
    /// Allows to assign different weights to the individual forces, prioritizing one over the other.
    ///
    /// ⚠ **This type is _unstable_ and may change significantly in a way that the data won't be backwards compatible.**
    ///
    struct ForceStrength {
        rerun::datatypes::Float64 distance;

      public:
        ForceStrength() = default;

        ForceStrength(rerun::datatypes::Float64 distance_) : distance(distance_) {}

        ForceStrength& operator=(rerun::datatypes::Float64 distance_) {
            distance = distance_;
            return *this;
        }

        ForceStrength(double value_) : distance(value_) {}

        ForceStrength& operator=(double value_) {
            distance = value_;
            return *this;
        }

        /// Cast to the underlying Float64 datatype
        operator rerun::datatypes::Float64() const {
            return distance;
        }
    };
} // namespace rerun::blueprint::components

namespace rerun {
    static_assert(
        sizeof(rerun::datatypes::Float64) == sizeof(blueprint::components::ForceStrength)
    );

    /// \private
    template <>
    struct Loggable<blueprint::components::ForceStrength> {
        static constexpr ComponentDescriptor Descriptor =
            "rerun.blueprint.components.ForceStrength";

        /// Returns the arrow data type this type corresponds to.
        static const std::shared_ptr<arrow::DataType>& arrow_datatype() {
            return Loggable<rerun::datatypes::Float64>::arrow_datatype();
        }

        /// Serializes an array of `rerun::blueprint:: components::ForceStrength` into an arrow array.
        static Result<std::shared_ptr<arrow::Array>> to_arrow(
            const blueprint::components::ForceStrength* instances, size_t num_instances
        ) {
            if (num_instances == 0) {
                return Loggable<rerun::datatypes::Float64>::to_arrow(nullptr, 0);
            } else if (instances == nullptr) {
                return rerun::Error(
                    ErrorCode::UnexpectedNullArgument,
                    "Passed array instances is null when num_elements> 0."
                );
            } else {
                return Loggable<rerun::datatypes::Float64>::to_arrow(
                    &instances->distance,
                    num_instances
                );
            }
        }
    };
} // namespace rerun
