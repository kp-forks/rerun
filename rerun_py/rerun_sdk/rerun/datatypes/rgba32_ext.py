from __future__ import annotations

import warnings
from collections.abc import Sequence
from typing import TYPE_CHECKING

import numpy as np
import numpy.typing as npt
import pyarrow as pa

from ..color_conversion import u8_array_to_rgba
from ..error_utils import RerunWarning

if TYPE_CHECKING:
    from . import Rgba32ArrayLike, Rgba32Like


def _numpy_array_to_u32(data: npt.NDArray[np.uint8 | np.float32 | np.float64]) -> npt.NDArray[np.uint32]:
    if data.size == 0:
        return np.array([], dtype=np.uint32)

    if data.dtype.type in [np.float32, np.float64]:
        array = u8_array_to_rgba(np.asarray(np.round(np.asarray(data) * 255.0), np.uint8))
    else:
        array = u8_array_to_rgba(np.asarray(data, dtype=np.uint8))
    return array


class Rgba32Ext:
    """Extension for [Rgba32][rerun.datatypes.Rgba32]."""

    """
    Extension for the `Rgba32` datatype.

    Possible input for `Rgba32`:
    - Sequence[int]: interpreted as rgb or rgba values in 0-255 range
    - numpy array: interpreted as rgb or rgba values, range depending on dtype
    - anything else (int or convertible to int): interpreted as a 32-bit packed rgba value

    Possible inputs for `Rgba32Batch()`:
    - a single `Rgba32` instance
    - a sequence of `Rgba32` instances
    - Nx3 or Nx4 numpy array, range depending on dtype
    """

    @staticmethod
    def rgba__field_converter_override(data: Rgba32Like) -> int:
        from . import Rgba32

        if isinstance(data, Rgba32):
            return data.rgba
        if isinstance(data, np.ndarray):
            return int(_numpy_array_to_u32(data.reshape((1, -1)))[0])
        elif isinstance(data, Sequence):
            data = np.array(data).reshape((1, -1))
            if data.shape[1] not in (3, 4):
                raise ValueError(f"expected sequence of length of 3 or 4, received {data.shape[1]}")
            return int(_numpy_array_to_u32(data)[0])
        else:
            return int(data)

    @staticmethod
    def native_to_pa_array_override(data: Rgba32ArrayLike, data_type: pa.DataType) -> pa.Array:
        from . import Rgba32

        if isinstance(data, int) or isinstance(data, Rgba32):
            # A single packed int or Rgba32 (which implements __int__())
            int_array = np.array([data])
        elif isinstance(data, Sequence) and len(data) == 0:
            # An empty array
            int_array = np.array([])
        else:
            # Try to coerce it to a numpy array
            try:
                arr = np.asarray(data).squeeze()

                # If the array is flat
                if len(arr.shape) <= 1:
                    # And not one of the known types
                    if arr.dtype not in (np.uint8, np.float32, np.float64, np.uint32):
                        # And not a length 3 or 4 array:
                        if arr.size not in (3, 4):
                            # We assume this is packed ints
                            arr = arr.astype(np.uint32)
                        else:
                            # Otherwise, if all the values are less than 256
                            if np.max(arr) < 256:
                                # Then treat it as a single color
                                arr = arr.reshape((1, -1))
                            else:
                                # But if not, then send a warning to the user
                                warnings.warn(
                                    f"Ambiguous input for colors of length {arr.size}. If using 0xRRGGBBAA values, please wrap as np.array with dtype=np.uint32",
                                    category=RerunWarning,
                                    stacklevel=7,
                                )
                                arr = arr.astype(np.uint32)

                    elif arr.dtype != np.uint32:
                        if len(arr.shape) <= 1:
                            if arr.size > 4:
                                # multiple RGBA colors
                                arr = arr.reshape((-1, 4))
                            else:
                                # a single color
                                arr = arr.reshape((1, -1))

                if arr.dtype == np.uint32:
                    # these are already packed values
                    int_array = arr.flatten()
                else:
                    int_array = _numpy_array_to_u32(arr)  # type: ignore[assignment]

            except (ValueError, TypeError, IndexError):
                # Fallback support
                data_list = list(data)  # type: ignore[arg-type]

                # First try to coerce it to a single Rgba32 instance
                try:
                    data_list = [Rgba32(data_list)]  # type: ignore[arg-type]
                except (IndexError, ValueError):
                    pass

                # Fially, handle heterogeneous sequence of Rgba32-like object,
                # such as Rgba32 instances, ints, sub-sequence, etc.
                #
                # Note how this is simplified by the flexible implementation of
                # `Rgba32`, thanks to its converter function and the
                # auto-generated `__int__()` method.
                int_array = np.array([Rgba32(datum) for datum in data_list], np.uint32)  # type: ignore[arg-type]

        return pa.array(int_array, type=data_type)
