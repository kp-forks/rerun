# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/blueprint/components/force_iterations.fbs".

# You can extend this class by creating a "ForceIterationsExt" class in "force_iterations_ext.py".

from __future__ import annotations

from ... import datatypes
from ..._baseclasses import (
    ComponentBatchMixin,
    ComponentDescriptor,
    ComponentMixin,
)

__all__ = ["ForceIterations", "ForceIterationsBatch"]


class ForceIterations(datatypes.UInt64, ComponentMixin):
    """
    **Component**: Specifies how often this force should be applied per iteration.

    Increasing this parameter can lead to better results at the cost of longer computation time.

    ⚠️ **This type is _unstable_ and may change significantly in a way that the data won't be backwards compatible.**
    """

    _BATCH_TYPE = None
    # You can define your own __init__ function as a member of ForceIterationsExt in force_iterations_ext.py

    # Note: there are no fields here because ForceIterations delegates to datatypes.UInt64


class ForceIterationsBatch(datatypes.UInt64Batch, ComponentBatchMixin):
    _COMPONENT_DESCRIPTOR: ComponentDescriptor = ComponentDescriptor("rerun.blueprint.components.ForceIterations")


# This is patched in late to avoid circular dependencies.
ForceIterations._BATCH_TYPE = ForceIterationsBatch  # type: ignore[assignment]
