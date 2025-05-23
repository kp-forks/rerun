# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/blueprint/archetypes/force_many_body.fbs".

# You can extend this class by creating a "ForceManyBodyExt" class in "force_many_body_ext.py".

from __future__ import annotations

from typing import Any

from attrs import define, field

from ... import datatypes
from ..._baseclasses import (
    Archetype,
)
from ...blueprint import components as blueprint_components
from ...error_utils import catch_and_log_exceptions

__all__ = ["ForceManyBody"]


@define(str=False, repr=False, init=False)
class ForceManyBody(Archetype):
    """
    **Archetype**: A force between each pair of nodes that ressembles an electrical charge.

    If `strength` is smaller than 0, it pushes nodes apart, if it is larger than 0 it pulls them together.

    ⚠️ **This type is _unstable_ and may change significantly in a way that the data won't be backwards compatible.**
    """

    def __init__(
        self: Any, *, enabled: datatypes.BoolLike | None = None, strength: datatypes.Float64Like | None = None
    ) -> None:
        """
        Create a new instance of the ForceManyBody archetype.

        Parameters
        ----------
        enabled:
            Whether the many body force is enabled.

            The many body force is applied on each pair of nodes in a way that ressembles an electrical charge. If the
            strength is smaller than 0, it pushes nodes apart; if it is larger than 0, it pulls them together.
        strength:
            The strength of the force.

            If `strength` is smaller than 0, it pushes nodes apart, if it is larger than 0 it pulls them together.

        """

        # You can define your own __init__ function as a member of ForceManyBodyExt in force_many_body_ext.py
        with catch_and_log_exceptions(context=self.__class__.__name__):
            self.__attrs_init__(enabled=enabled, strength=strength)
            return
        self.__attrs_clear__()

    def __attrs_clear__(self) -> None:
        """Convenience method for calling `__attrs_init__` with all `None`s."""
        self.__attrs_init__(
            enabled=None,
            strength=None,
        )

    @classmethod
    def _clear(cls) -> ForceManyBody:
        """Produce an empty ForceManyBody, bypassing `__init__`."""
        inst = cls.__new__(cls)
        inst.__attrs_clear__()
        return inst

    @classmethod
    def from_fields(
        cls,
        *,
        clear_unset: bool = False,
        enabled: datatypes.BoolLike | None = None,
        strength: datatypes.Float64Like | None = None,
    ) -> ForceManyBody:
        """
        Update only some specific fields of a `ForceManyBody`.

        Parameters
        ----------
        clear_unset:
            If true, all unspecified fields will be explicitly cleared.
        enabled:
            Whether the many body force is enabled.

            The many body force is applied on each pair of nodes in a way that ressembles an electrical charge. If the
            strength is smaller than 0, it pushes nodes apart; if it is larger than 0, it pulls them together.
        strength:
            The strength of the force.

            If `strength` is smaller than 0, it pushes nodes apart, if it is larger than 0 it pulls them together.

        """

        inst = cls.__new__(cls)
        with catch_and_log_exceptions(context=cls.__name__):
            kwargs = {
                "enabled": enabled,
                "strength": strength,
            }

            if clear_unset:
                kwargs = {k: v if v is not None else [] for k, v in kwargs.items()}  # type: ignore[misc]

            inst.__attrs_init__(**kwargs)
            return inst

        inst.__attrs_clear__()
        return inst

    @classmethod
    def cleared(cls) -> ForceManyBody:
        """Clear all the fields of a `ForceManyBody`."""
        return cls.from_fields(clear_unset=True)

    enabled: blueprint_components.EnabledBatch | None = field(
        metadata={"component": True},
        default=None,
        converter=blueprint_components.EnabledBatch._converter,  # type: ignore[misc]
    )
    # Whether the many body force is enabled.
    #
    # The many body force is applied on each pair of nodes in a way that ressembles an electrical charge. If the
    # strength is smaller than 0, it pushes nodes apart; if it is larger than 0, it pulls them together.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    strength: blueprint_components.ForceStrengthBatch | None = field(
        metadata={"component": True},
        default=None,
        converter=blueprint_components.ForceStrengthBatch._converter,  # type: ignore[misc]
    )
    # The strength of the force.
    #
    # If `strength` is smaller than 0, it pushes nodes apart, if it is larger than 0 it pulls them together.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    __str__ = Archetype.__str__
    __repr__ = Archetype.__repr__  # type: ignore[assignment]
