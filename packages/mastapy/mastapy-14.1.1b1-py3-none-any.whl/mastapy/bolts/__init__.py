"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bolts._1524 import AxialLoadType
    from mastapy._private.bolts._1525 import BoltedJointMaterial
    from mastapy._private.bolts._1526 import BoltedJointMaterialDatabase
    from mastapy._private.bolts._1527 import BoltGeometry
    from mastapy._private.bolts._1528 import BoltGeometryDatabase
    from mastapy._private.bolts._1529 import BoltMaterial
    from mastapy._private.bolts._1530 import BoltMaterialDatabase
    from mastapy._private.bolts._1531 import BoltSection
    from mastapy._private.bolts._1532 import BoltShankType
    from mastapy._private.bolts._1533 import BoltTypes
    from mastapy._private.bolts._1534 import ClampedSection
    from mastapy._private.bolts._1535 import ClampedSectionMaterialDatabase
    from mastapy._private.bolts._1536 import DetailedBoltDesign
    from mastapy._private.bolts._1537 import DetailedBoltedJointDesign
    from mastapy._private.bolts._1538 import HeadCapTypes
    from mastapy._private.bolts._1539 import JointGeometries
    from mastapy._private.bolts._1540 import JointTypes
    from mastapy._private.bolts._1541 import LoadedBolt
    from mastapy._private.bolts._1542 import RolledBeforeOrAfterHeatTreatment
    from mastapy._private.bolts._1543 import StandardSizes
    from mastapy._private.bolts._1544 import StrengthGrades
    from mastapy._private.bolts._1545 import ThreadTypes
    from mastapy._private.bolts._1546 import TighteningTechniques
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bolts._1524": ["AxialLoadType"],
        "_private.bolts._1525": ["BoltedJointMaterial"],
        "_private.bolts._1526": ["BoltedJointMaterialDatabase"],
        "_private.bolts._1527": ["BoltGeometry"],
        "_private.bolts._1528": ["BoltGeometryDatabase"],
        "_private.bolts._1529": ["BoltMaterial"],
        "_private.bolts._1530": ["BoltMaterialDatabase"],
        "_private.bolts._1531": ["BoltSection"],
        "_private.bolts._1532": ["BoltShankType"],
        "_private.bolts._1533": ["BoltTypes"],
        "_private.bolts._1534": ["ClampedSection"],
        "_private.bolts._1535": ["ClampedSectionMaterialDatabase"],
        "_private.bolts._1536": ["DetailedBoltDesign"],
        "_private.bolts._1537": ["DetailedBoltedJointDesign"],
        "_private.bolts._1538": ["HeadCapTypes"],
        "_private.bolts._1539": ["JointGeometries"],
        "_private.bolts._1540": ["JointTypes"],
        "_private.bolts._1541": ["LoadedBolt"],
        "_private.bolts._1542": ["RolledBeforeOrAfterHeatTreatment"],
        "_private.bolts._1543": ["StandardSizes"],
        "_private.bolts._1544": ["StrengthGrades"],
        "_private.bolts._1545": ["ThreadTypes"],
        "_private.bolts._1546": ["TighteningTechniques"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AxialLoadType",
    "BoltedJointMaterial",
    "BoltedJointMaterialDatabase",
    "BoltGeometry",
    "BoltGeometryDatabase",
    "BoltMaterial",
    "BoltMaterialDatabase",
    "BoltSection",
    "BoltShankType",
    "BoltTypes",
    "ClampedSection",
    "ClampedSectionMaterialDatabase",
    "DetailedBoltDesign",
    "DetailedBoltedJointDesign",
    "HeadCapTypes",
    "JointGeometries",
    "JointTypes",
    "LoadedBolt",
    "RolledBeforeOrAfterHeatTreatment",
    "StandardSizes",
    "StrengthGrades",
    "ThreadTypes",
    "TighteningTechniques",
)
