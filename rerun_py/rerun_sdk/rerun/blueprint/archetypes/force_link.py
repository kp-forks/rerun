# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/blueprint/archetypes/force_link.fbs".

# You can extend this class by creating a "ForceLinkExt" class in "force_link_ext.py".

from __future__ import annotations

from typing import Any

from attrs import define, field

from ... import datatypes
from ..._baseclasses import (
    Archetype,
)
from ...blueprint import components as blueprint_components
from ...error_utils import catch_and_log_exceptions

__all__ = ["ForceLink"]


@define(str=False, repr=False, init=False)
class ForceLink(Archetype):
    """
    **Archetype**: Aims to achieve a target distance between two nodes that are connected by an edge.

    ⚠️ **This type is _unstable_ and may change significantly in a way that the data won't be backwards compatible.**
    """

    def __init__(
        self: Any,
        *,
        enabled: datatypes.BoolLike | None = None,
        distance: datatypes.Float64Like | None = None,
        iterations: datatypes.UInt64Like | None = None,
    ) -> None:
        """
        Create a new instance of the ForceLink archetype.

        Parameters
        ----------
        enabled:
            Whether the link force is enabled.

            The link force aims to achieve a target distance between two nodes that are connected by one ore more edges.
        distance:
            The target distance between two nodes.
        iterations:
            Specifies how often this force should be applied per iteration.

            Increasing this parameter can lead to better results at the cost of longer computation time.

        """

        # You can define your own __init__ function as a member of ForceLinkExt in force_link_ext.py
        with catch_and_log_exceptions(context=self.__class__.__name__):
            self.__attrs_init__(enabled=enabled, distance=distance, iterations=iterations)
            return
        self.__attrs_clear__()

    def __attrs_clear__(self) -> None:
        """Convenience method for calling `__attrs_init__` with all `None`s."""
        self.__attrs_init__(
            enabled=None,
            distance=None,
            iterations=None,
        )

    @classmethod
    def _clear(cls) -> ForceLink:
        """Produce an empty ForceLink, bypassing `__init__`."""
        inst = cls.__new__(cls)
        inst.__attrs_clear__()
        return inst

    @classmethod
    def from_fields(
        cls,
        *,
        clear_unset: bool = False,
        enabled: datatypes.BoolLike | None = None,
        distance: datatypes.Float64Like | None = None,
        iterations: datatypes.UInt64Like | None = None,
    ) -> ForceLink:
        """
        Update only some specific fields of a `ForceLink`.

        Parameters
        ----------
        clear_unset:
            If true, all unspecified fields will be explicitly cleared.
        enabled:
            Whether the link force is enabled.

            The link force aims to achieve a target distance between two nodes that are connected by one ore more edges.
        distance:
            The target distance between two nodes.
        iterations:
            Specifies how often this force should be applied per iteration.

            Increasing this parameter can lead to better results at the cost of longer computation time.

        """

        inst = cls.__new__(cls)
        with catch_and_log_exceptions(context=cls.__name__):
            kwargs = {
                "enabled": enabled,
                "distance": distance,
                "iterations": iterations,
            }

            if clear_unset:
                kwargs = {k: v if v is not None else [] for k, v in kwargs.items()}  # type: ignore[misc]

            inst.__attrs_init__(**kwargs)
            return inst

        inst.__attrs_clear__()
        return inst

    @classmethod
    def cleared(cls) -> ForceLink:
        """Clear all the fields of a `ForceLink`."""
        return cls.from_fields(clear_unset=True)

    enabled: blueprint_components.EnabledBatch | None = field(
        metadata={"component": True},
        default=None,
        converter=blueprint_components.EnabledBatch._converter,  # type: ignore[misc]
    )
    # Whether the link force is enabled.
    #
    # The link force aims to achieve a target distance between two nodes that are connected by one ore more edges.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    distance: blueprint_components.ForceDistanceBatch | None = field(
        metadata={"component": True},
        default=None,
        converter=blueprint_components.ForceDistanceBatch._converter,  # type: ignore[misc]
    )
    # The target distance between two nodes.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    iterations: blueprint_components.ForceIterationsBatch | None = field(
        metadata={"component": True},
        default=None,
        converter=blueprint_components.ForceIterationsBatch._converter,  # type: ignore[misc]
    )
    # Specifies how often this force should be applied per iteration.
    #
    # Increasing this parameter can lead to better results at the cost of longer computation time.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    __str__ = Archetype.__str__
    __repr__ = Archetype.__repr__  # type: ignore[assignment]
