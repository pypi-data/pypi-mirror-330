"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.concept._1224 import ConceptGearDesign
    from mastapy._private.gears.gear_designs.concept._1225 import ConceptGearMeshDesign
    from mastapy._private.gears.gear_designs.concept._1226 import ConceptGearSetDesign
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.concept._1224": ["ConceptGearDesign"],
        "_private.gears.gear_designs.concept._1225": ["ConceptGearMeshDesign"],
        "_private.gears.gear_designs.concept._1226": ["ConceptGearSetDesign"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConceptGearDesign",
    "ConceptGearMeshDesign",
    "ConceptGearSetDesign",
)
