"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.cycloidal._1510 import ContactSpecification
    from mastapy._private.cycloidal._1511 import CrowningSpecificationMethod
    from mastapy._private.cycloidal._1512 import CycloidalAssemblyDesign
    from mastapy._private.cycloidal._1513 import CycloidalDiscDesign
    from mastapy._private.cycloidal._1514 import CycloidalDiscDesignExporter
    from mastapy._private.cycloidal._1515 import CycloidalDiscMaterial
    from mastapy._private.cycloidal._1516 import CycloidalDiscMaterialDatabase
    from mastapy._private.cycloidal._1517 import CycloidalDiscModificationsSpecification
    from mastapy._private.cycloidal._1518 import DirectionOfMeasuredModifications
    from mastapy._private.cycloidal._1519 import GeometryToExport
    from mastapy._private.cycloidal._1520 import NamedDiscPhase
    from mastapy._private.cycloidal._1521 import RingPinsDesign
    from mastapy._private.cycloidal._1522 import RingPinsMaterial
    from mastapy._private.cycloidal._1523 import RingPinsMaterialDatabase
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.cycloidal._1510": ["ContactSpecification"],
        "_private.cycloidal._1511": ["CrowningSpecificationMethod"],
        "_private.cycloidal._1512": ["CycloidalAssemblyDesign"],
        "_private.cycloidal._1513": ["CycloidalDiscDesign"],
        "_private.cycloidal._1514": ["CycloidalDiscDesignExporter"],
        "_private.cycloidal._1515": ["CycloidalDiscMaterial"],
        "_private.cycloidal._1516": ["CycloidalDiscMaterialDatabase"],
        "_private.cycloidal._1517": ["CycloidalDiscModificationsSpecification"],
        "_private.cycloidal._1518": ["DirectionOfMeasuredModifications"],
        "_private.cycloidal._1519": ["GeometryToExport"],
        "_private.cycloidal._1520": ["NamedDiscPhase"],
        "_private.cycloidal._1521": ["RingPinsDesign"],
        "_private.cycloidal._1522": ["RingPinsMaterial"],
        "_private.cycloidal._1523": ["RingPinsMaterialDatabase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ContactSpecification",
    "CrowningSpecificationMethod",
    "CycloidalAssemblyDesign",
    "CycloidalDiscDesign",
    "CycloidalDiscDesignExporter",
    "CycloidalDiscMaterial",
    "CycloidalDiscMaterialDatabase",
    "CycloidalDiscModificationsSpecification",
    "DirectionOfMeasuredModifications",
    "GeometryToExport",
    "NamedDiscPhase",
    "RingPinsDesign",
    "RingPinsMaterial",
    "RingPinsMaterialDatabase",
)
