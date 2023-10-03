# DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/python.rs
# Based on "crates/re_types/definitions/rerun/components/view_coordinates.fbs".

# You can extend this class by creating a "ViewCoordinatesExt" class in "view_coordinates_ext.py".

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence, Union

import numpy as np
import numpy.typing as npt
import pyarrow as pa
from attrs import define, field

from .._baseclasses import BaseBatch, BaseExtensionType, ComponentBatchMixin
from .view_coordinates_ext import ViewCoordinatesExt

__all__ = [
    "ViewCoordinates",
    "ViewCoordinatesArrayLike",
    "ViewCoordinatesBatch",
    "ViewCoordinatesLike",
    "ViewCoordinatesType",
]


@define(init=False)
class ViewCoordinates(ViewCoordinatesExt):
    """
    **Component**: How we interpret the coordinate system of an entity/space.

    For instance: What is "up"? What does the Z axis mean? Is this right-handed or left-handed?

    The three coordinates are always ordered as [x, y, z].

    For example [Right, Down, Forward] means that the X axis points to the right, the Y axis points
    down, and the Z axis points forward.

    The following constants are used to represent the different directions.
     Up = 1
     Down = 2
     Right = 3
     Left = 4
     Forward = 5
     Back = 6
    """

    def __init__(self: Any, coordinates: ViewCoordinatesLike):
        """
        Create a new instance of the ViewCoordinates component.

        Parameters
        ----------
        coordinates:
             The directions of the [x, y, z] axes.
        """

        # You can define your own __init__ function as a member of ViewCoordinatesExt in view_coordinates_ext.py
        self.__attrs_init__(coordinates=coordinates)

    coordinates: npt.NDArray[np.uint8] = field(
        converter=ViewCoordinatesExt.coordinates__field_converter_override,  # type: ignore[misc]
    )
    # The directions of the [x, y, z] axes.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    def __array__(self, dtype: npt.DTypeLike = None) -> npt.NDArray[Any]:
        # You can define your own __array__ function as a member of ViewCoordinatesExt in view_coordinates_ext.py
        return np.asarray(self.coordinates, dtype=dtype)


if TYPE_CHECKING:
    ViewCoordinatesLike = Union[ViewCoordinates, npt.ArrayLike]
else:
    ViewCoordinatesLike = Any

ViewCoordinatesArrayLike = Union[ViewCoordinates, Sequence[ViewCoordinatesLike], npt.ArrayLike]


class ViewCoordinatesType(BaseExtensionType):
    _TYPE_NAME: str = "rerun.components.ViewCoordinates"

    def __init__(self) -> None:
        pa.ExtensionType.__init__(
            self, pa.list_(pa.field("item", pa.uint8(), nullable=False, metadata={}), 3), self._TYPE_NAME
        )


class ViewCoordinatesBatch(BaseBatch[ViewCoordinatesArrayLike], ComponentBatchMixin):
    _ARROW_TYPE = ViewCoordinatesType()

    @staticmethod
    def _native_to_pa_array(data: ViewCoordinatesArrayLike, data_type: pa.DataType) -> pa.Array:
        return ViewCoordinatesExt.native_to_pa_array_override(data, data_type)


# TODO(cmc): bring back registration to pyarrow once legacy types are gone
# pa.register_extension_type(ViewCoordinatesType())


if hasattr(ViewCoordinatesExt, "deferred_patch_class"):
    ViewCoordinatesExt.deferred_patch_class(ViewCoordinates)
