"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.klingelnberg_conical._1013 import (
        KlingelnbergConicalGearDesign,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_conical._1014 import (
        KlingelnbergConicalGearMeshDesign,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_conical._1015 import (
        KlingelnbergConicalGearSetDesign,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_conical._1016 import (
        KlingelnbergConicalMeshedGearDesign,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.klingelnberg_conical._1013": [
            "KlingelnbergConicalGearDesign"
        ],
        "_private.gears.gear_designs.klingelnberg_conical._1014": [
            "KlingelnbergConicalGearMeshDesign"
        ],
        "_private.gears.gear_designs.klingelnberg_conical._1015": [
            "KlingelnbergConicalGearSetDesign"
        ],
        "_private.gears.gear_designs.klingelnberg_conical._1016": [
            "KlingelnbergConicalMeshedGearDesign"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "KlingelnbergConicalGearDesign",
    "KlingelnbergConicalGearMeshDesign",
    "KlingelnbergConicalGearSetDesign",
    "KlingelnbergConicalMeshedGearDesign",
)
