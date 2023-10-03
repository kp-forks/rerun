# DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/python.rs
# Based on "crates/re_types/definitions/rerun/archetypes/text_document.fbs".

# You can extend this class by creating a "TextDocumentExt" class in "text_document_ext.py".

from __future__ import annotations

from typing import Any

from attrs import define, field

from .. import components, datatypes
from .._baseclasses import Archetype
from ..error_utils import catch_and_log_exceptions

__all__ = ["TextDocument"]


@define(str=False, repr=False, init=False)
class TextDocument(Archetype):
    """**Archetype**: A text element intended to be displayed in its own text-box."""

    def __init__(self: Any, text: datatypes.Utf8Like, *, media_type: datatypes.Utf8Like | None = None):
        """
        Create a new instance of the TextDocument archetype.

        Parameters
        ----------
        text:
             Contents of the text document.
        media_type:
             The Media Type of the text.

             For instance:
             * `text/plain`
             * `text/markdown`

             If omitted, `text/plain` is assumed.
        """

        # You can define your own __init__ function as a member of TextDocumentExt in text_document_ext.py
        with catch_and_log_exceptions(context=self.__class__.__name__):
            self.__attrs_init__(text=text, media_type=media_type)
            return
        self.__attrs_clear__()

    def __attrs_clear__(self) -> None:
        """Convenience method for calling `__attrs_init__` with all `None`s."""
        self.__attrs_init__(
            text=None,  # type: ignore[arg-type]
            media_type=None,  # type: ignore[arg-type]
        )

    @classmethod
    def _clear(cls) -> TextDocument:
        """Produce an empty TextDocument, bypassing `__init__`."""
        inst = cls.__new__(cls)
        inst.__attrs_clear__()
        return inst

    text: components.TextBatch = field(
        metadata={"component": "required"},
        converter=components.TextBatch._required,  # type: ignore[misc]
    )
    # Contents of the text document.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    media_type: components.MediaTypeBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.MediaTypeBatch._optional,  # type: ignore[misc]
    )
    # The Media Type of the text.
    #
    # For instance:
    # * `text/plain`
    # * `text/markdown`
    #
    # If omitted, `text/plain` is assumed.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    __str__ = Archetype.__str__
    __repr__ = Archetype.__repr__
