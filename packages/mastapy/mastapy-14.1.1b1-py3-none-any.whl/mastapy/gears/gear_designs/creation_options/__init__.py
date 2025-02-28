"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.creation_options._1193 import (
        CylindricalGearPairCreationOptions,
    )
    from mastapy._private.gears.gear_designs.creation_options._1194 import (
        DifferentialAssemblyCreationOptions,
    )
    from mastapy._private.gears.gear_designs.creation_options._1195 import (
        GearSetCreationOptions,
    )
    from mastapy._private.gears.gear_designs.creation_options._1196 import (
        HypoidGearSetCreationOptions,
    )
    from mastapy._private.gears.gear_designs.creation_options._1197 import (
        SpiralBevelGearSetCreationOptions,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.creation_options._1193": [
            "CylindricalGearPairCreationOptions"
        ],
        "_private.gears.gear_designs.creation_options._1194": [
            "DifferentialAssemblyCreationOptions"
        ],
        "_private.gears.gear_designs.creation_options._1195": [
            "GearSetCreationOptions"
        ],
        "_private.gears.gear_designs.creation_options._1196": [
            "HypoidGearSetCreationOptions"
        ],
        "_private.gears.gear_designs.creation_options._1197": [
            "SpiralBevelGearSetCreationOptions"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearPairCreationOptions",
    "DifferentialAssemblyCreationOptions",
    "GearSetCreationOptions",
    "HypoidGearSetCreationOptions",
    "SpiralBevelGearSetCreationOptions",
)
