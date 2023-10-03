// DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/cpp/mod.rs
// Based on "crates/re_types/definitions/rerun/archetypes/text_document.fbs".

#pragma once

#include "../arrow.hpp"
#include "../component_batch.hpp"
#include "../components/media_type.hpp"
#include "../components/text.hpp"
#include "../data_cell.hpp"
#include "../result.hpp"

#include <cstdint>
#include <optional>
#include <utility>
#include <vector>

namespace rerun {
    namespace archetypes {
        /// **Archetype**: A text element intended to be displayed in its own text-box.
        struct TextDocument {
            /// Contents of the text document.
            rerun::components::Text text;

            /// The Media Type of the text.
            ///
            /// For instance:
            /// * `text/plain`
            /// * `text/markdown`
            ///
            /// If omitted, `text/plain` is assumed.
            std::optional<rerun::components::MediaType> media_type;

            /// Name of the indicator component, used to identify the archetype when converting to a
            /// list of components.
            static const char INDICATOR_COMPONENT_NAME[];

          public:
            TextDocument() = default;

            TextDocument(rerun::components::Text _text) : text(std::move(_text)) {}

            /// The Media Type of the text.
            ///
            /// For instance:
            /// * `text/plain`
            /// * `text/markdown`
            ///
            /// If omitted, `text/plain` is assumed.
            TextDocument& with_media_type(rerun::components::MediaType _media_type) {
                media_type = std::move(_media_type);
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
