"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.concept._567 import ConceptGearDutyCycleRating
    from mastapy._private.gears.rating.concept._568 import (
        ConceptGearMeshDutyCycleRating,
    )
    from mastapy._private.gears.rating.concept._569 import ConceptGearMeshRating
    from mastapy._private.gears.rating.concept._570 import ConceptGearRating
    from mastapy._private.gears.rating.concept._571 import ConceptGearSetDutyCycleRating
    from mastapy._private.gears.rating.concept._572 import ConceptGearSetRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.concept._567": ["ConceptGearDutyCycleRating"],
        "_private.gears.rating.concept._568": ["ConceptGearMeshDutyCycleRating"],
        "_private.gears.rating.concept._569": ["ConceptGearMeshRating"],
        "_private.gears.rating.concept._570": ["ConceptGearRating"],
        "_private.gears.rating.concept._571": ["ConceptGearSetDutyCycleRating"],
        "_private.gears.rating.concept._572": ["ConceptGearSetRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConceptGearDutyCycleRating",
    "ConceptGearMeshDutyCycleRating",
    "ConceptGearMeshRating",
    "ConceptGearRating",
    "ConceptGearSetDutyCycleRating",
    "ConceptGearSetRating",
)
