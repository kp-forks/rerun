# DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/python.rs
# Based on "crates/re_types/definitions/rerun/components/out_of_tree_transform3d.fbs".

# You can extend this class by creating a "OutOfTreeTransform3DExt" class in "out_of_tree_transform3d_ext.py".

from __future__ import annotations

from .. import datatypes
from .._baseclasses import ComponentBatchMixin

__all__ = ["OutOfTreeTransform3D", "OutOfTreeTransform3DBatch", "OutOfTreeTransform3DType"]


class OutOfTreeTransform3D(datatypes.Transform3D):
    """
    **Component**: An out-of-tree affine transform between two 3D spaces, represented in a given direction.

    "Out-of-tree" means that the transform only affects its own entity: children don't inherit from it.
    """

    # You can define your own __init__ function as a member of OutOfTreeTransform3DExt in out_of_tree_transform3d_ext.py

    # Note: there are no fields here because OutOfTreeTransform3D delegates to datatypes.Transform3D
    pass


class OutOfTreeTransform3DType(datatypes.Transform3DType):
    _TYPE_NAME: str = "rerun.components.OutOfTreeTransform3D"


class OutOfTreeTransform3DBatch(datatypes.Transform3DBatch, ComponentBatchMixin):
    _ARROW_TYPE = OutOfTreeTransform3DType()


# TODO(cmc): bring back registration to pyarrow once legacy types are gone
# pa.register_extension_type(OutOfTreeTransform3DType())
