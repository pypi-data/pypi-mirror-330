"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.agma_gleason_conical._584 import (
        AGMAGleasonConicalGearMeshRating,
    )
    from mastapy._private.gears.rating.agma_gleason_conical._585 import (
        AGMAGleasonConicalGearRating,
    )
    from mastapy._private.gears.rating.agma_gleason_conical._586 import (
        AGMAGleasonConicalGearSetRating,
    )
    from mastapy._private.gears.rating.agma_gleason_conical._587 import (
        AGMAGleasonConicalRateableMesh,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.agma_gleason_conical._584": [
            "AGMAGleasonConicalGearMeshRating"
        ],
        "_private.gears.rating.agma_gleason_conical._585": [
            "AGMAGleasonConicalGearRating"
        ],
        "_private.gears.rating.agma_gleason_conical._586": [
            "AGMAGleasonConicalGearSetRating"
        ],
        "_private.gears.rating.agma_gleason_conical._587": [
            "AGMAGleasonConicalRateableMesh"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMAGleasonConicalGearMeshRating",
    "AGMAGleasonConicalGearRating",
    "AGMAGleasonConicalGearSetRating",
    "AGMAGleasonConicalRateableMesh",
)
