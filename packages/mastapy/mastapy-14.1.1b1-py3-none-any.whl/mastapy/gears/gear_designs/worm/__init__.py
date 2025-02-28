"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.worm._988 import WormDesign
    from mastapy._private.gears.gear_designs.worm._989 import WormGearDesign
    from mastapy._private.gears.gear_designs.worm._990 import WormGearMeshDesign
    from mastapy._private.gears.gear_designs.worm._991 import WormGearSetDesign
    from mastapy._private.gears.gear_designs.worm._992 import WormWheelDesign
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.worm._988": ["WormDesign"],
        "_private.gears.gear_designs.worm._989": ["WormGearDesign"],
        "_private.gears.gear_designs.worm._990": ["WormGearMeshDesign"],
        "_private.gears.gear_designs.worm._991": ["WormGearSetDesign"],
        "_private.gears.gear_designs.worm._992": ["WormWheelDesign"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "WormDesign",
    "WormGearDesign",
    "WormGearMeshDesign",
    "WormGearSetDesign",
    "WormWheelDesign",
)
