// DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/cpp/mod.rs
// Based on "crates/re_types/definitions/rerun/archetypes/text_log.fbs".

#pragma once

#include "../arrow.hpp"
#include "../component_batch.hpp"
#include "../components/color.hpp"
#include "../components/text.hpp"
#include "../components/text_log_level.hpp"
#include "../data_cell.hpp"
#include "../result.hpp"

#include <cstdint>
#include <optional>
#include <utility>
#include <vector>

namespace rerun {
    namespace archetypes {
        /// **Archetype**: A log entry in a text log, comprised of a text body and its log level.
        struct TextLog {
            rerun::components::Text text;

            std::optional<rerun::components::TextLogLevel> level;

            std::optional<rerun::components::Color> color;

            /// Name of the indicator component, used to identify the archetype when converting to a
            /// list of components.
            static const char INDICATOR_COMPONENT_NAME[];

          public:
            TextLog() = default;

            TextLog(rerun::components::Text _text) : text(std::move(_text)) {}

            TextLog& with_level(rerun::components::TextLogLevel _level) {
                level = std::move(_level);
                return *this;
            }

            TextLog& with_color(rerun::components::Color _color) {
                color = std::move(_color);
                return *this;
            }

            /// Returns the number of primary instances of this archetype.
            size_t num_instances() const {
                return 1;
            }

            /// Creates an `AnonymousComponentBatch` out of the associated indicator component. This
            /// allows for associating arbitrary indicator components with arbitrary data. Check out
            /// the `manual_indicator` API example to see what's possible.
            static AnonymousComponentBatch indicator();

            /// Collections all component lists into a list of component collections. *Attention:*
            /// The returned vector references this instance and does not take ownership of any
            /// data. Adding any new components to this archetype will invalidate the returned
            /// component lists!
            std::vector<AnonymousComponentBatch> as_component_batches() const;
        };
    } // namespace archetypes
} // namespace rerun
