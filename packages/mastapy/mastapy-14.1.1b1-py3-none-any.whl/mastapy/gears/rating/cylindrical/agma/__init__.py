"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.cylindrical.agma._553 import (
        AGMA2101GearSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical.agma._554 import (
        AGMA2101MeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical.agma._555 import AGMA2101RateableMesh
    from mastapy._private.gears.rating.cylindrical.agma._556 import (
        ThermalReductionFactorFactorsAndExponents,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.cylindrical.agma._553": [
            "AGMA2101GearSingleFlankRating"
        ],
        "_private.gears.rating.cylindrical.agma._554": [
            "AGMA2101MeshSingleFlankRating"
        ],
        "_private.gears.rating.cylindrical.agma._555": ["AGMA2101RateableMesh"],
        "_private.gears.rating.cylindrical.agma._556": [
            "ThermalReductionFactorFactorsAndExponents"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMA2101GearSingleFlankRating",
    "AGMA2101MeshSingleFlankRating",
    "AGMA2101RateableMesh",
    "ThermalReductionFactorFactorsAndExponents",
)
