"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.bevel._573 import BevelGearMeshRating
    from mastapy._private.gears.rating.bevel._574 import BevelGearRating
    from mastapy._private.gears.rating.bevel._575 import BevelGearSetRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.bevel._573": ["BevelGearMeshRating"],
        "_private.gears.rating.bevel._574": ["BevelGearRating"],
        "_private.gears.rating.bevel._575": ["BevelGearSetRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BevelGearMeshRating",
    "BevelGearRating",
    "BevelGearSetRating",
)
