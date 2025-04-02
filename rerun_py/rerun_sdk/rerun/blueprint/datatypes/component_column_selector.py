# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/blueprint/datatypes/component_column_selector.fbs".

# You can extend this class by creating a "ComponentColumnSelectorExt" class in "component_column_selector_ext.py".

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Union

import pyarrow as pa
from attrs import define, field

from ... import datatypes
from ..._baseclasses import (
    BaseBatch,
)
from .component_column_selector_ext import ComponentColumnSelectorExt

__all__ = [
    "ComponentColumnSelector",
    "ComponentColumnSelectorArrayLike",
    "ComponentColumnSelectorBatch",
    "ComponentColumnSelectorLike",
]


def _component_column_selector__entity_path__special_field_converter_override(
    x: datatypes.EntityPathLike,
) -> datatypes.EntityPath:
    if isinstance(x, datatypes.EntityPath):
        return x
    else:
        return datatypes.EntityPath(x)


def _component_column_selector__component__special_field_converter_override(x: datatypes.Utf8Like) -> datatypes.Utf8:
    if isinstance(x, datatypes.Utf8):
        return x
    else:
        return datatypes.Utf8(x)


@define(init=False)
class ComponentColumnSelector(ComponentColumnSelectorExt):
    """
    **Datatype**: Describe a component column to be selected in the dataframe view.

    ⚠️ **This type is _unstable_ and may change significantly in a way that the data won't be backwards compatible.**
    """

    # __init__ can be found in component_column_selector_ext.py

    entity_path: datatypes.EntityPath = field(
        converter=_component_column_selector__entity_path__special_field_converter_override
    )
    # The entity path for this component.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    component: datatypes.Utf8 = field(converter=_component_column_selector__component__special_field_converter_override)
    # The name of the component.
    #
    # (Docstring intentionally commented out to hide this field from the docs)


if TYPE_CHECKING:
    ComponentColumnSelectorLike = Union[ComponentColumnSelector, str]
else:
    ComponentColumnSelectorLike = Any

ComponentColumnSelectorArrayLike = Union[
    ComponentColumnSelector,
    Sequence[ComponentColumnSelectorLike],
]


class ComponentColumnSelectorBatch(BaseBatch[ComponentColumnSelectorArrayLike]):
    _ARROW_DATATYPE = pa.struct([
        pa.field("entity_path", pa.utf8(), nullable=False, metadata={}),
        pa.field("component", pa.utf8(), nullable=False, metadata={}),
    ])

    @staticmethod
    def _native_to_pa_array(data: ComponentColumnSelectorArrayLike, data_type: pa.DataType) -> pa.Array:
        return ComponentColumnSelectorExt.native_to_pa_array_override(data, data_type)
