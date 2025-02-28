"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.geometry._324 import ClippingPlane
    from mastapy._private.geometry._325 import DrawStyle
    from mastapy._private.geometry._326 import DrawStyleBase
    from mastapy._private.geometry._327 import PackagingLimits
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.geometry._324": ["ClippingPlane"],
        "_private.geometry._325": ["DrawStyle"],
        "_private.geometry._326": ["DrawStyleBase"],
        "_private.geometry._327": ["PackagingLimits"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ClippingPlane",
    "DrawStyle",
    "DrawStyleBase",
    "PackagingLimits",
)
