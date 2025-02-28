"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.materials._602 import AGMACylindricalGearMaterial
    from mastapy._private.gears.materials._603 import (
        BenedictAndKelleyCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._604 import BevelGearAbstractMaterialDatabase
    from mastapy._private.gears.materials._605 import BevelGearISOMaterial
    from mastapy._private.gears.materials._606 import BevelGearISOMaterialDatabase
    from mastapy._private.gears.materials._607 import BevelGearMaterial
    from mastapy._private.gears.materials._608 import BevelGearMaterialDatabase
    from mastapy._private.gears.materials._609 import CoefficientOfFrictionCalculator
    from mastapy._private.gears.materials._610 import (
        CylindricalGearAGMAMaterialDatabase,
    )
    from mastapy._private.gears.materials._611 import CylindricalGearISOMaterialDatabase
    from mastapy._private.gears.materials._612 import CylindricalGearMaterial
    from mastapy._private.gears.materials._613 import CylindricalGearMaterialDatabase
    from mastapy._private.gears.materials._614 import (
        CylindricalGearPlasticMaterialDatabase,
    )
    from mastapy._private.gears.materials._615 import (
        DrozdovAndGavrikovCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._616 import GearMaterial
    from mastapy._private.gears.materials._617 import GearMaterialDatabase
    from mastapy._private.gears.materials._618 import (
        GearMaterialExpertSystemFactorSettings,
    )
    from mastapy._private.gears.materials._619 import (
        InstantaneousCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._620 import (
        ISO14179Part1CoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._621 import (
        ISO14179Part2CoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._622 import (
        ISO14179Part2CoefficientOfFrictionCalculatorBase,
    )
    from mastapy._private.gears.materials._623 import (
        ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification,
    )
    from mastapy._private.gears.materials._624 import ISOCylindricalGearMaterial
    from mastapy._private.gears.materials._625 import (
        ISOTC60CoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._626 import (
        ISOTR1417912001CoefficientOfFrictionConstants,
    )
    from mastapy._private.gears.materials._627 import (
        ISOTR1417912001CoefficientOfFrictionConstantsDatabase,
    )
    from mastapy._private.gears.materials._628 import (
        KlingelnbergConicalGearMaterialDatabase,
    )
    from mastapy._private.gears.materials._629 import (
        KlingelnbergCycloPalloidConicalGearMaterial,
    )
    from mastapy._private.gears.materials._630 import ManufactureRating
    from mastapy._private.gears.materials._631 import (
        MisharinCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._632 import (
        ODonoghueAndCameronCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._633 import PlasticCylindricalGearMaterial
    from mastapy._private.gears.materials._634 import PlasticSNCurve
    from mastapy._private.gears.materials._635 import RatingMethods
    from mastapy._private.gears.materials._636 import RawMaterial
    from mastapy._private.gears.materials._637 import RawMaterialDatabase
    from mastapy._private.gears.materials._638 import (
        ScriptCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._639 import SNCurveDefinition
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.materials._602": ["AGMACylindricalGearMaterial"],
        "_private.gears.materials._603": [
            "BenedictAndKelleyCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._604": ["BevelGearAbstractMaterialDatabase"],
        "_private.gears.materials._605": ["BevelGearISOMaterial"],
        "_private.gears.materials._606": ["BevelGearISOMaterialDatabase"],
        "_private.gears.materials._607": ["BevelGearMaterial"],
        "_private.gears.materials._608": ["BevelGearMaterialDatabase"],
        "_private.gears.materials._609": ["CoefficientOfFrictionCalculator"],
        "_private.gears.materials._610": ["CylindricalGearAGMAMaterialDatabase"],
        "_private.gears.materials._611": ["CylindricalGearISOMaterialDatabase"],
        "_private.gears.materials._612": ["CylindricalGearMaterial"],
        "_private.gears.materials._613": ["CylindricalGearMaterialDatabase"],
        "_private.gears.materials._614": ["CylindricalGearPlasticMaterialDatabase"],
        "_private.gears.materials._615": [
            "DrozdovAndGavrikovCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._616": ["GearMaterial"],
        "_private.gears.materials._617": ["GearMaterialDatabase"],
        "_private.gears.materials._618": ["GearMaterialExpertSystemFactorSettings"],
        "_private.gears.materials._619": [
            "InstantaneousCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._620": [
            "ISO14179Part1CoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._621": [
            "ISO14179Part2CoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._622": [
            "ISO14179Part2CoefficientOfFrictionCalculatorBase"
        ],
        "_private.gears.materials._623": [
            "ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification"
        ],
        "_private.gears.materials._624": ["ISOCylindricalGearMaterial"],
        "_private.gears.materials._625": ["ISOTC60CoefficientOfFrictionCalculator"],
        "_private.gears.materials._626": [
            "ISOTR1417912001CoefficientOfFrictionConstants"
        ],
        "_private.gears.materials._627": [
            "ISOTR1417912001CoefficientOfFrictionConstantsDatabase"
        ],
        "_private.gears.materials._628": ["KlingelnbergConicalGearMaterialDatabase"],
        "_private.gears.materials._629": [
            "KlingelnbergCycloPalloidConicalGearMaterial"
        ],
        "_private.gears.materials._630": ["ManufactureRating"],
        "_private.gears.materials._631": ["MisharinCoefficientOfFrictionCalculator"],
        "_private.gears.materials._632": [
            "ODonoghueAndCameronCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._633": ["PlasticCylindricalGearMaterial"],
        "_private.gears.materials._634": ["PlasticSNCurve"],
        "_private.gears.materials._635": ["RatingMethods"],
        "_private.gears.materials._636": ["RawMaterial"],
        "_private.gears.materials._637": ["RawMaterialDatabase"],
        "_private.gears.materials._638": ["ScriptCoefficientOfFrictionCalculator"],
        "_private.gears.materials._639": ["SNCurveDefinition"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMACylindricalGearMaterial",
    "BenedictAndKelleyCoefficientOfFrictionCalculator",
    "BevelGearAbstractMaterialDatabase",
    "BevelGearISOMaterial",
    "BevelGearISOMaterialDatabase",
    "BevelGearMaterial",
    "BevelGearMaterialDatabase",
    "CoefficientOfFrictionCalculator",
    "CylindricalGearAGMAMaterialDatabase",
    "CylindricalGearISOMaterialDatabase",
    "CylindricalGearMaterial",
    "CylindricalGearMaterialDatabase",
    "CylindricalGearPlasticMaterialDatabase",
    "DrozdovAndGavrikovCoefficientOfFrictionCalculator",
    "GearMaterial",
    "GearMaterialDatabase",
    "GearMaterialExpertSystemFactorSettings",
    "InstantaneousCoefficientOfFrictionCalculator",
    "ISO14179Part1CoefficientOfFrictionCalculator",
    "ISO14179Part2CoefficientOfFrictionCalculator",
    "ISO14179Part2CoefficientOfFrictionCalculatorBase",
    "ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification",
    "ISOCylindricalGearMaterial",
    "ISOTC60CoefficientOfFrictionCalculator",
    "ISOTR1417912001CoefficientOfFrictionConstants",
    "ISOTR1417912001CoefficientOfFrictionConstantsDatabase",
    "KlingelnbergConicalGearMaterialDatabase",
    "KlingelnbergCycloPalloidConicalGearMaterial",
    "ManufactureRating",
    "MisharinCoefficientOfFrictionCalculator",
    "ODonoghueAndCameronCoefficientOfFrictionCalculator",
    "PlasticCylindricalGearMaterial",
    "PlasticSNCurve",
    "RatingMethods",
    "RawMaterial",
    "RawMaterialDatabase",
    "ScriptCoefficientOfFrictionCalculator",
    "SNCurveDefinition",
)
