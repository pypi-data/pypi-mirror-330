"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.zerol_bevel._388 import ZerolBevelGearMeshRating
    from mastapy._private.gears.rating.zerol_bevel._389 import ZerolBevelGearRating
    from mastapy._private.gears.rating.zerol_bevel._390 import ZerolBevelGearSetRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.zerol_bevel._388": ["ZerolBevelGearMeshRating"],
        "_private.gears.rating.zerol_bevel._389": ["ZerolBevelGearRating"],
        "_private.gears.rating.zerol_bevel._390": ["ZerolBevelGearSetRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ZerolBevelGearMeshRating",
    "ZerolBevelGearRating",
    "ZerolBevelGearSetRating",
)
