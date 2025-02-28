"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.conical._557 import ConicalGearDutyCycleRating
    from mastapy._private.gears.rating.conical._558 import ConicalGearMeshRating
    from mastapy._private.gears.rating.conical._559 import ConicalGearRating
    from mastapy._private.gears.rating.conical._560 import ConicalGearSetDutyCycleRating
    from mastapy._private.gears.rating.conical._561 import ConicalGearSetRating
    from mastapy._private.gears.rating.conical._562 import ConicalGearSingleFlankRating
    from mastapy._private.gears.rating.conical._563 import ConicalMeshDutyCycleRating
    from mastapy._private.gears.rating.conical._564 import ConicalMeshedGearRating
    from mastapy._private.gears.rating.conical._565 import ConicalMeshSingleFlankRating
    from mastapy._private.gears.rating.conical._566 import ConicalRateableMesh
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.conical._557": ["ConicalGearDutyCycleRating"],
        "_private.gears.rating.conical._558": ["ConicalGearMeshRating"],
        "_private.gears.rating.conical._559": ["ConicalGearRating"],
        "_private.gears.rating.conical._560": ["ConicalGearSetDutyCycleRating"],
        "_private.gears.rating.conical._561": ["ConicalGearSetRating"],
        "_private.gears.rating.conical._562": ["ConicalGearSingleFlankRating"],
        "_private.gears.rating.conical._563": ["ConicalMeshDutyCycleRating"],
        "_private.gears.rating.conical._564": ["ConicalMeshedGearRating"],
        "_private.gears.rating.conical._565": ["ConicalMeshSingleFlankRating"],
        "_private.gears.rating.conical._566": ["ConicalRateableMesh"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearDutyCycleRating",
    "ConicalGearMeshRating",
    "ConicalGearRating",
    "ConicalGearSetDutyCycleRating",
    "ConicalGearSetRating",
    "ConicalGearSingleFlankRating",
    "ConicalMeshDutyCycleRating",
    "ConicalMeshedGearRating",
    "ConicalMeshSingleFlankRating",
    "ConicalRateableMesh",
)
