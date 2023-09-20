# DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/python.rs
# Based on "crates/re_types/definitions/rerun/archetypes/clear.fbs".

# You can extend this class by creating a "ClearExt" class in "clear_ext.py".

from __future__ import annotations

from attrs import define, field

from .. import components
from .._baseclasses import (
    Archetype,
)

__all__ = ["Clear"]


@define(str=False, repr=False)
class Clear(Archetype):
    """
    Empties all the components of an entity.

    Examples
    --------
    Flat:
    ```python

    import rerun as rr
    import rerun.experimental as rr2

    rr.init("rerun_example_clear_simple", spawn=True)

    vectors = [(1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    origins = [(-0.5, 0.5, 0.0), (0.5, 0.5, 0.0), (0.5, -0.5, 0.0), (-0.5, -0.5, 0.0)]
    colors = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (200, 0, 200)]

    # Log a handful of arrows.
    for i, (vector, origin, color) in enumerate(zip(vectors, origins, colors)):
        rr2.log(f"arrows/{i}", rr2.Arrows3D(vector, origins=origin, colors=color))

    # Now clear them, one by one on each tick.
    for i in range(len(vectors)):
        # TODO(#3268): `rr2.Clear.flat()`
        rr2.log(f"arrows/{i}", rr2.Clear(False))
    ```

    Recursive:
    ```python

    import rerun as rr
    import rerun.experimental as rr2

    rr.init("rerun_example_clear_simple", spawn=True)

    vectors = [(1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    origins = [(-0.5, 0.5, 0.0), (0.5, 0.5, 0.0), (0.5, -0.5, 0.0), (-0.5, -0.5, 0.0)]
    colors = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (200, 0, 200)]

    # Log a handful of arrows.
    for i, (vector, origin, color) in enumerate(zip(vectors, origins, colors)):
        rr2.log(f"arrows/{i}", rr2.Arrows3D(vector, origins=origin, colors=color))

    # Now clear all of them at once.
    # TODO(#3268): `rr2.Clear.recursive()`
    rr2.log("arrows", rr2.Clear(True))
    ```
    """

    # You can define your own __init__ function as a member of ClearExt in clear_ext.py

    settings: components.ClearSettingsArray = field(
        metadata={"component": "required"},
        converter=components.ClearSettingsArray.from_similar,  # type: ignore[misc]
    )
    __str__ = Archetype.__str__
    __repr__ = Archetype.__repr__
