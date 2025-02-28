"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.load_case.face._910 import FaceGearLoadCase
    from mastapy._private.gears.load_case.face._911 import FaceGearSetLoadCase
    from mastapy._private.gears.load_case.face._912 import FaceMeshLoadCase
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.load_case.face._910": ["FaceGearLoadCase"],
        "_private.gears.load_case.face._911": ["FaceGearSetLoadCase"],
        "_private.gears.load_case.face._912": ["FaceMeshLoadCase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FaceGearLoadCase",
    "FaceGearSetLoadCase",
    "FaceMeshLoadCase",
)
