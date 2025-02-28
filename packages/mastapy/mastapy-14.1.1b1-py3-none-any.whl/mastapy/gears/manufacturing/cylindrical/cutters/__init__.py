"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.cylindrical.cutters._734 import (
        CurveInLinkedList,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._735 import (
        CustomisableEdgeProfile,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._736 import (
        CylindricalFormedWheelGrinderDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._737 import (
        CylindricalGearAbstractCutterDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._738 import (
        CylindricalGearFormGrindingWheel,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._739 import (
        CylindricalGearGrindingWorm,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._740 import (
        CylindricalGearHobDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._741 import (
        CylindricalGearPlungeShaver,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._742 import (
        CylindricalGearPlungeShaverDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._743 import (
        CylindricalGearRackDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._744 import (
        CylindricalGearRealCutterDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._745 import (
        CylindricalGearShaper,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._746 import (
        CylindricalGearShaver,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._747 import (
        CylindricalGearShaverDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._748 import (
        CylindricalWormGrinderDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._749 import (
        InvoluteCutterDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._750 import (
        MutableCommon,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._751 import (
        MutableCurve,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._752 import (
        MutableFillet,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._753 import (
        RoughCutterCreationSettings,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.cylindrical.cutters._734": ["CurveInLinkedList"],
        "_private.gears.manufacturing.cylindrical.cutters._735": [
            "CustomisableEdgeProfile"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._736": [
            "CylindricalFormedWheelGrinderDatabase"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._737": [
            "CylindricalGearAbstractCutterDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._738": [
            "CylindricalGearFormGrindingWheel"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._739": [
            "CylindricalGearGrindingWorm"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._740": [
            "CylindricalGearHobDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._741": [
            "CylindricalGearPlungeShaver"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._742": [
            "CylindricalGearPlungeShaverDatabase"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._743": [
            "CylindricalGearRackDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._744": [
            "CylindricalGearRealCutterDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._745": [
            "CylindricalGearShaper"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._746": [
            "CylindricalGearShaver"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._747": [
            "CylindricalGearShaverDatabase"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._748": [
            "CylindricalWormGrinderDatabase"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._749": [
            "InvoluteCutterDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._750": ["MutableCommon"],
        "_private.gears.manufacturing.cylindrical.cutters._751": ["MutableCurve"],
        "_private.gears.manufacturing.cylindrical.cutters._752": ["MutableFillet"],
        "_private.gears.manufacturing.cylindrical.cutters._753": [
            "RoughCutterCreationSettings"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CurveInLinkedList",
    "CustomisableEdgeProfile",
    "CylindricalFormedWheelGrinderDatabase",
    "CylindricalGearAbstractCutterDesign",
    "CylindricalGearFormGrindingWheel",
    "CylindricalGearGrindingWorm",
    "CylindricalGearHobDesign",
    "CylindricalGearPlungeShaver",
    "CylindricalGearPlungeShaverDatabase",
    "CylindricalGearRackDesign",
    "CylindricalGearRealCutterDesign",
    "CylindricalGearShaper",
    "CylindricalGearShaver",
    "CylindricalGearShaverDatabase",
    "CylindricalWormGrinderDatabase",
    "InvoluteCutterDesign",
    "MutableCommon",
    "MutableCurve",
    "MutableFillet",
    "RoughCutterCreationSettings",
)
