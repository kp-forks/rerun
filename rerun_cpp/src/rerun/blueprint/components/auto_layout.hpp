// DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/cpp/mod.rs
// Based on "crates/store/re_types/definitions/rerun/blueprint/components/auto_layout.fbs".

#pragma once

#include "../../component_descriptor.hpp"
#include "../../datatypes/bool.hpp"
#include "../../result.hpp"

#include <cstdint>
#include <memory>

namespace rerun::blueprint::components {
    /// **Component**: Whether the viewport layout is determined automatically.
    ///
    /// ⚠ **This type is _unstable_ and may change significantly in a way that the data won't be backwards compatible.**
    ///
    struct AutoLayout {
        rerun::datatypes::Bool auto_layout;

      public:
        AutoLayout() = default;

        AutoLayout(rerun::datatypes::Bool auto_layout_) : auto_layout(auto_layout_) {}

        AutoLayout& operator=(rerun::datatypes::Bool auto_layout_) {
            auto_layout = auto_layout_;
            return *this;
        }

        AutoLayout(bool value_) : auto_layout(value_) {}

        AutoLayout& operator=(bool value_) {
            auto_layout = value_;
            return *this;
        }

        /// Cast to the underlying Bool datatype
        operator rerun::datatypes::Bool() const {
            return auto_layout;
        }
    };
} // namespace rerun::blueprint::components

namespace rerun {
    static_assert(sizeof(rerun::datatypes::Bool) == sizeof(blueprint::components::AutoLayout));

    /// \private
    template <>
    struct Loggable<blueprint::components::AutoLayout> {
        static constexpr ComponentDescriptor Descriptor = "rerun.blueprint.components.AutoLayout";

        /// Returns the arrow data type this type corresponds to.
        static const std::shared_ptr<arrow::DataType>& arrow_datatype() {
            return Loggable<rerun::datatypes::Bool>::arrow_datatype();
        }

        /// Serializes an array of `rerun::blueprint:: components::AutoLayout` into an arrow array.
        static Result<std::shared_ptr<arrow::Array>> to_arrow(
            const blueprint::components::AutoLayout* instances, size_t num_instances
        ) {
            if (num_instances == 0) {
                return Loggable<rerun::datatypes::Bool>::to_arrow(nullptr, 0);
            } else if (instances == nullptr) {
                return rerun::Error(
                    ErrorCode::UnexpectedNullArgument,
                    "Passed array instances is null when num_elements> 0."
                );
            } else {
                return Loggable<rerun::datatypes::Bool>::to_arrow(
                    &instances->auto_layout,
                    num_instances
                );
            }
        }
    };
} // namespace rerun
