# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/blueprint/archetypes/background.fbs".

# You can extend this class by creating a "BackgroundExt" class in "background_ext.py".

from __future__ import annotations

from attrs import define, field

from ... import components, datatypes
from ..._baseclasses import (
    Archetype,
)
from ...blueprint import components as blueprint_components
from ...error_utils import catch_and_log_exceptions
from .background_ext import BackgroundExt

__all__ = ["Background"]


@define(str=False, repr=False, init=False)
class Background(BackgroundExt, Archetype):
    """
    **Archetype**: Configuration for the background of a view.

    ⚠️ **This type is _unstable_ and may change significantly in a way that the data won't be backwards compatible.**
    """

    # __init__ can be found in background_ext.py

    def __attrs_clear__(self) -> None:
        """Convenience method for calling `__attrs_init__` with all `None`s."""
        self.__attrs_init__(
            kind=None,
            color=None,
        )

    @classmethod
    def _clear(cls) -> Background:
        """Produce an empty Background, bypassing `__init__`."""
        inst = cls.__new__(cls)
        inst.__attrs_clear__()
        return inst

    @classmethod
    def from_fields(
        cls,
        *,
        clear_unset: bool = False,
        kind: blueprint_components.BackgroundKindLike | None = None,
        color: datatypes.Rgba32Like | None = None,
    ) -> Background:
        """
        Update only some specific fields of a `Background`.

        Parameters
        ----------
        clear_unset:
            If true, all unspecified fields will be explicitly cleared.
        kind:
            The type of the background.
        color:
            Color used for the solid background type.

        """

        inst = cls.__new__(cls)
        with catch_and_log_exceptions(context=cls.__name__):
            kwargs = {
                "kind": kind,
                "color": color,
            }

            if clear_unset:
                kwargs = {k: v if v is not None else [] for k, v in kwargs.items()}  # type: ignore[misc]

            inst.__attrs_init__(**kwargs)
            return inst

        inst.__attrs_clear__()
        return inst

    @classmethod
    def cleared(cls) -> Background:
        """Clear all the fields of a `Background`."""
        return cls.from_fields(clear_unset=True)

    kind: blueprint_components.BackgroundKindBatch | None = field(
        metadata={"component": True},
        default=None,
        converter=blueprint_components.BackgroundKindBatch._converter,  # type: ignore[misc]
    )
    # The type of the background.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    color: components.ColorBatch | None = field(
        metadata={"component": True},
        default=None,
        converter=components.ColorBatch._converter,  # type: ignore[misc]
    )
    # Color used for the solid background type.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    __str__ = Archetype.__str__
    __repr__ = Archetype.__repr__  # type: ignore[assignment]
