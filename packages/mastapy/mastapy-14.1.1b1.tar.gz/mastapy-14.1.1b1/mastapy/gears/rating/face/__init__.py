"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.face._464 import FaceGearDutyCycleRating
    from mastapy._private.gears.rating.face._465 import FaceGearMeshDutyCycleRating
    from mastapy._private.gears.rating.face._466 import FaceGearMeshRating
    from mastapy._private.gears.rating.face._467 import FaceGearRating
    from mastapy._private.gears.rating.face._468 import FaceGearSetDutyCycleRating
    from mastapy._private.gears.rating.face._469 import FaceGearSetRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.face._464": ["FaceGearDutyCycleRating"],
        "_private.gears.rating.face._465": ["FaceGearMeshDutyCycleRating"],
        "_private.gears.rating.face._466": ["FaceGearMeshRating"],
        "_private.gears.rating.face._467": ["FaceGearRating"],
        "_private.gears.rating.face._468": ["FaceGearSetDutyCycleRating"],
        "_private.gears.rating.face._469": ["FaceGearSetRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FaceGearDutyCycleRating",
    "FaceGearMeshDutyCycleRating",
    "FaceGearMeshRating",
    "FaceGearRating",
    "FaceGearSetDutyCycleRating",
    "FaceGearSetRating",
)
