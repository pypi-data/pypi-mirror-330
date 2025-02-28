"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.worm._391 import WormGearDutyCycleRating
    from mastapy._private.gears.rating.worm._392 import WormGearMeshRating
    from mastapy._private.gears.rating.worm._393 import WormGearRating
    from mastapy._private.gears.rating.worm._394 import WormGearSetDutyCycleRating
    from mastapy._private.gears.rating.worm._395 import WormGearSetRating
    from mastapy._private.gears.rating.worm._396 import WormMeshDutyCycleRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.worm._391": ["WormGearDutyCycleRating"],
        "_private.gears.rating.worm._392": ["WormGearMeshRating"],
        "_private.gears.rating.worm._393": ["WormGearRating"],
        "_private.gears.rating.worm._394": ["WormGearSetDutyCycleRating"],
        "_private.gears.rating.worm._395": ["WormGearSetRating"],
        "_private.gears.rating.worm._396": ["WormMeshDutyCycleRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "WormGearDutyCycleRating",
    "WormGearMeshRating",
    "WormGearRating",
    "WormGearSetDutyCycleRating",
    "WormGearSetRating",
    "WormMeshDutyCycleRating",
)
