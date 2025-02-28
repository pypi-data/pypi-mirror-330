"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.bevel.standards._576 import (
        AGMASpiralBevelGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._577 import (
        AGMASpiralBevelMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._578 import (
        GleasonSpiralBevelGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._579 import (
        GleasonSpiralBevelMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._580 import (
        SpiralBevelGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._581 import (
        SpiralBevelMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.bevel.standards._582 import (
        SpiralBevelRateableGear,
    )
    from mastapy._private.gears.rating.bevel.standards._583 import (
        SpiralBevelRateableMesh,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.bevel.standards._576": [
            "AGMASpiralBevelGearSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._577": [
            "AGMASpiralBevelMeshSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._578": [
            "GleasonSpiralBevelGearSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._579": [
            "GleasonSpiralBevelMeshSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._580": [
            "SpiralBevelGearSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._581": [
            "SpiralBevelMeshSingleFlankRating"
        ],
        "_private.gears.rating.bevel.standards._582": ["SpiralBevelRateableGear"],
        "_private.gears.rating.bevel.standards._583": ["SpiralBevelRateableMesh"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMASpiralBevelGearSingleFlankRating",
    "AGMASpiralBevelMeshSingleFlankRating",
    "GleasonSpiralBevelGearSingleFlankRating",
    "GleasonSpiralBevelMeshSingleFlankRating",
    "SpiralBevelGearSingleFlankRating",
    "SpiralBevelMeshSingleFlankRating",
    "SpiralBevelRateableGear",
    "SpiralBevelRateableMesh",
)
