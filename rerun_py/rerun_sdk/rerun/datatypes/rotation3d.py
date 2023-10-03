# DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/python.rs
# Based on "crates/re_types/definitions/rerun/datatypes/rotation3d.fbs".

# You can extend this class by creating a "Rotation3DExt" class in "rotation3d_ext.py".

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence, SupportsFloat, Union

import pyarrow as pa
from attrs import define, field

from .. import datatypes
from .._baseclasses import BaseBatch, BaseExtensionType
from .rotation3d_ext import Rotation3DExt

__all__ = ["Rotation3D", "Rotation3DArrayLike", "Rotation3DBatch", "Rotation3DLike", "Rotation3DType"]


@define
class Rotation3D(Rotation3DExt):
    """**Datatype**: A 3D rotation."""

    # You can define your own __init__ function as a member of Rotation3DExt in rotation3d_ext.py

    inner: datatypes.Quaternion | datatypes.RotationAxisAngle = field(converter=Rotation3DExt.inner__field_converter_override)  # type: ignore[misc]
    """
    Quaternion (datatypes.Quaternion):
        Rotation defined by a quaternion.

    AxisAngle (datatypes.RotationAxisAngle):
        Rotation defined with an axis and an angle.
    """


if TYPE_CHECKING:
    Rotation3DLike = Union[Rotation3D, datatypes.Quaternion, datatypes.RotationAxisAngle, Sequence[SupportsFloat]]
    Rotation3DArrayLike = Union[
        Rotation3D,
        datatypes.Quaternion,
        datatypes.RotationAxisAngle,
        Sequence[Rotation3DLike],
    ]
else:
    Rotation3DLike = Any
    Rotation3DArrayLike = Any


class Rotation3DType(BaseExtensionType):
    _TYPE_NAME: str = "rerun.datatypes.Rotation3D"

    def __init__(self) -> None:
        pa.ExtensionType.__init__(
            self,
            pa.dense_union(
                [
                    pa.field("_null_markers", pa.null(), nullable=True, metadata={}),
                    pa.field(
                        "Quaternion",
                        pa.list_(pa.field("item", pa.float32(), nullable=False, metadata={}), 4),
                        nullable=False,
                        metadata={},
                    ),
                    pa.field(
                        "AxisAngle",
                        pa.struct(
                            [
                                pa.field(
                                    "axis",
                                    pa.list_(pa.field("item", pa.float32(), nullable=False, metadata={}), 3),
                                    nullable=False,
                                    metadata={},
                                ),
                                pa.field(
                                    "angle",
                                    pa.dense_union(
                                        [
                                            pa.field("_null_markers", pa.null(), nullable=True, metadata={}),
                                            pa.field("Radians", pa.float32(), nullable=False, metadata={}),
                                            pa.field("Degrees", pa.float32(), nullable=False, metadata={}),
                                        ]
                                    ),
                                    nullable=False,
                                    metadata={},
                                ),
                            ]
                        ),
                        nullable=False,
                        metadata={},
                    ),
                ]
            ),
            self._TYPE_NAME,
        )


class Rotation3DBatch(BaseBatch[Rotation3DArrayLike]):
    _ARROW_TYPE = Rotation3DType()

    @staticmethod
    def _native_to_pa_array(data: Rotation3DArrayLike, data_type: pa.DataType) -> pa.Array:
        return Rotation3DExt.native_to_pa_array_override(data, data_type)


# TODO(cmc): bring back registration to pyarrow once legacy types are gone
# pa.register_extension_type(Rotation3DType())


if hasattr(Rotation3DExt, "deferred_patch_class"):
    Rotation3DExt.deferred_patch_class(Rotation3D)
