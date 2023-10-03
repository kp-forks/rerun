# DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/python.rs
# Based on "crates/re_types/definitions/rerun/archetypes/arrows3d.fbs".

# You can extend this class by creating a "Arrows3DExt" class in "arrows3d_ext.py".

from __future__ import annotations

from attrs import define, field

from .. import components
from .._baseclasses import Archetype
from .arrows3d_ext import Arrows3DExt

__all__ = ["Arrows3D"]


@define(str=False, repr=False, init=False)
class Arrows3D(Arrows3DExt, Archetype):
    """
    **Archetype**: A batch of 3D arrows with optional colors, radii, labels, etc.

    Example
    -------
    ```python
    from math import tau

    import numpy as np
    import rerun as rr

    rr.init("rerun_example_arrow3d", spawn=True)

    lengths = np.log2(np.arange(0, 100) + 1)
    angles = np.arange(start=0, stop=tau, step=tau * 0.01)
    origins = np.zeros((100, 3))
    vectors = np.column_stack([np.sin(angles) * lengths, np.zeros(100), np.cos(angles) * lengths])
    colors = [[1.0 - c, c, 0.5, 0.5] for c in angles / tau]

    rr.log("arrows", rr.Arrows3D(origins=origins, vectors=vectors, colors=colors))
    ```
    <picture>
      <source media="(max-width: 480px)" srcset="https://static.rerun.io/arrow3d_simple/c8a8b1cbca40acdf02fb5bf264658ad66e07ca40/480w.png">
      <source media="(max-width: 768px)" srcset="https://static.rerun.io/arrow3d_simple/c8a8b1cbca40acdf02fb5bf264658ad66e07ca40/768w.png">
      <source media="(max-width: 1024px)" srcset="https://static.rerun.io/arrow3d_simple/c8a8b1cbca40acdf02fb5bf264658ad66e07ca40/1024w.png">
      <source media="(max-width: 1200px)" srcset="https://static.rerun.io/arrow3d_simple/c8a8b1cbca40acdf02fb5bf264658ad66e07ca40/1200w.png">
      <img src="https://static.rerun.io/arrow3d_simple/c8a8b1cbca40acdf02fb5bf264658ad66e07ca40/full.png">
    </picture>
    """

    # __init__ can be found in arrows3d_ext.py

    def __attrs_clear__(self) -> None:
        """Convenience method for calling `__attrs_init__` with all `None`s."""
        self.__attrs_init__(
            vectors=None,  # type: ignore[arg-type]
            origins=None,  # type: ignore[arg-type]
            radii=None,  # type: ignore[arg-type]
            colors=None,  # type: ignore[arg-type]
            labels=None,  # type: ignore[arg-type]
            class_ids=None,  # type: ignore[arg-type]
            instance_keys=None,  # type: ignore[arg-type]
        )

    @classmethod
    def _clear(cls) -> Arrows3D:
        """Produce an empty Arrows3D, bypassing `__init__`."""
        inst = cls.__new__(cls)
        inst.__attrs_clear__()
        return inst

    vectors: components.Vector3DBatch = field(
        metadata={"component": "required"},
        converter=components.Vector3DBatch._required,  # type: ignore[misc]
    )
    # All the vectors for each arrow in the batch.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    origins: components.Origin3DBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.Origin3DBatch._optional,  # type: ignore[misc]
    )
    # All the origin points for each arrow in the batch.
    #
    # If no origins are set, (0, 0, 0) is used as the origin for each arrow.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    radii: components.RadiusBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.RadiusBatch._optional,  # type: ignore[misc]
    )
    # Optional radii for the arrows.
    #
    # The shaft is rendered as a line with `radius = 0.5 * radius`.
    # The tip is rendered with `height = 2.0 * radius` and `radius = 1.0 * radius`.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    colors: components.ColorBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.ColorBatch._optional,  # type: ignore[misc]
    )
    # Optional colors for the points.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    labels: components.TextBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.TextBatch._optional,  # type: ignore[misc]
    )
    # Optional text labels for the arrows.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    class_ids: components.ClassIdBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.ClassIdBatch._optional,  # type: ignore[misc]
    )
    # Optional class Ids for the points.
    #
    # The class ID provides colors and labels if not specified explicitly.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    instance_keys: components.InstanceKeyBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.InstanceKeyBatch._optional,  # type: ignore[misc]
    )
    # Unique identifiers for each individual point in the batch.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    __str__ = Archetype.__str__
    __repr__ = Archetype.__repr__


if hasattr(Arrows3DExt, "deferred_patch_class"):
    Arrows3DExt.deferred_patch_class(Arrows3D)
