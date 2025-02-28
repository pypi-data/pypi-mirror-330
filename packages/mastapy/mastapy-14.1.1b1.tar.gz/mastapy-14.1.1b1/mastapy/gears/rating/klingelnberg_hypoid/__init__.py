"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.klingelnberg_hypoid._427 import (
        KlingelnbergCycloPalloidHypoidGearMeshRating,
    )
    from mastapy._private.gears.rating.klingelnberg_hypoid._428 import (
        KlingelnbergCycloPalloidHypoidGearRating,
    )
    from mastapy._private.gears.rating.klingelnberg_hypoid._429 import (
        KlingelnbergCycloPalloidHypoidGearSetRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.klingelnberg_hypoid._427": [
            "KlingelnbergCycloPalloidHypoidGearMeshRating"
        ],
        "_private.gears.rating.klingelnberg_hypoid._428": [
            "KlingelnbergCycloPalloidHypoidGearRating"
        ],
        "_private.gears.rating.klingelnberg_hypoid._429": [
            "KlingelnbergCycloPalloidHypoidGearSetRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "KlingelnbergCycloPalloidHypoidGearMeshRating",
    "KlingelnbergCycloPalloidHypoidGearRating",
    "KlingelnbergCycloPalloidHypoidGearSetRating",
)
