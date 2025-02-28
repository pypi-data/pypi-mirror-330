"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.modal_analysis.gears._1858 import GearMeshForTE
    from mastapy._private.utility.modal_analysis.gears._1859 import GearOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1860 import GearPositions
    from mastapy._private.utility.modal_analysis.gears._1861 import HarmonicOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1862 import LabelOnlyOrder
    from mastapy._private.utility.modal_analysis.gears._1863 import OrderForTE
    from mastapy._private.utility.modal_analysis.gears._1864 import OrderSelector
    from mastapy._private.utility.modal_analysis.gears._1865 import OrderWithRadius
    from mastapy._private.utility.modal_analysis.gears._1866 import RollingBearingOrder
    from mastapy._private.utility.modal_analysis.gears._1867 import ShaftOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1868 import (
        UserDefinedOrderForTE,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.modal_analysis.gears._1858": ["GearMeshForTE"],
        "_private.utility.modal_analysis.gears._1859": ["GearOrderForTE"],
        "_private.utility.modal_analysis.gears._1860": ["GearPositions"],
        "_private.utility.modal_analysis.gears._1861": ["HarmonicOrderForTE"],
        "_private.utility.modal_analysis.gears._1862": ["LabelOnlyOrder"],
        "_private.utility.modal_analysis.gears._1863": ["OrderForTE"],
        "_private.utility.modal_analysis.gears._1864": ["OrderSelector"],
        "_private.utility.modal_analysis.gears._1865": ["OrderWithRadius"],
        "_private.utility.modal_analysis.gears._1866": ["RollingBearingOrder"],
        "_private.utility.modal_analysis.gears._1867": ["ShaftOrderForTE"],
        "_private.utility.modal_analysis.gears._1868": ["UserDefinedOrderForTE"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "GearMeshForTE",
    "GearOrderForTE",
    "GearPositions",
    "HarmonicOrderForTE",
    "LabelOnlyOrder",
    "OrderForTE",
    "OrderSelector",
    "OrderWithRadius",
    "RollingBearingOrder",
    "ShaftOrderForTE",
    "UserDefinedOrderForTE",
)
