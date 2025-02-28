"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel._1005 import (
        KlingelnbergCycloPalloidSpiralBevelGearDesign,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel._1006 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshDesign,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel._1007 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetDesign,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel._1008 import (
        KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.klingelnberg_spiral_bevel._1005": [
            "KlingelnbergCycloPalloidSpiralBevelGearDesign"
        ],
        "_private.gears.gear_designs.klingelnberg_spiral_bevel._1006": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshDesign"
        ],
        "_private.gears.gear_designs.klingelnberg_spiral_bevel._1007": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetDesign"
        ],
        "_private.gears.gear_designs.klingelnberg_spiral_bevel._1008": [
            "KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "KlingelnbergCycloPalloidSpiralBevelGearDesign",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshDesign",
    "KlingelnbergCycloPalloidSpiralBevelGearSetDesign",
    "KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign",
)
