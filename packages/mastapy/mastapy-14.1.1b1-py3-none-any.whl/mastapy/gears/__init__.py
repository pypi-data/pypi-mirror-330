"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears._332 import AccuracyGrades
    from mastapy._private.gears._333 import AGMAToleranceStandard
    from mastapy._private.gears._334 import BevelHypoidGearDesignSettings
    from mastapy._private.gears._335 import BevelHypoidGearRatingSettings
    from mastapy._private.gears._336 import CentreDistanceChangeMethod
    from mastapy._private.gears._337 import CoefficientOfFrictionCalculationMethod
    from mastapy._private.gears._338 import ConicalGearToothSurface
    from mastapy._private.gears._339 import ContactRatioDataSource
    from mastapy._private.gears._340 import ContactRatioRequirements
    from mastapy._private.gears._341 import CylindricalFlanks
    from mastapy._private.gears._342 import CylindricalMisalignmentDataSource
    from mastapy._private.gears._343 import DeflectionFromBendingOption
    from mastapy._private.gears._344 import GearFlanks
    from mastapy._private.gears._345 import GearNURBSSurface
    from mastapy._private.gears._346 import GearSetDesignGroup
    from mastapy._private.gears._347 import GearSetModes
    from mastapy._private.gears._348 import GearSetOptimisationResult
    from mastapy._private.gears._349 import GearSetOptimisationResults
    from mastapy._private.gears._350 import GearSetOptimiser
    from mastapy._private.gears._351 import Hand
    from mastapy._private.gears._352 import ISOToleranceStandard
    from mastapy._private.gears._353 import LubricationMethods
    from mastapy._private.gears._354 import MicroGeometryInputTypes
    from mastapy._private.gears._355 import MicroGeometryModel
    from mastapy._private.gears._356 import (
        MicropittingCoefficientOfFrictionCalculationMethod,
    )
    from mastapy._private.gears._357 import NamedPlanetAngle
    from mastapy._private.gears._358 import PlanetaryDetail
    from mastapy._private.gears._359 import PlanetaryRatingLoadSharingOption
    from mastapy._private.gears._360 import PocketingPowerLossCoefficients
    from mastapy._private.gears._361 import PocketingPowerLossCoefficientsDatabase
    from mastapy._private.gears._362 import QualityGradeTypes
    from mastapy._private.gears._363 import SafetyRequirementsAGMA
    from mastapy._private.gears._364 import (
        SpecificationForTheEffectOfOilKinematicViscosity,
    )
    from mastapy._private.gears._365 import SpiralBevelRootLineTilt
    from mastapy._private.gears._366 import SpiralBevelToothTaper
    from mastapy._private.gears._367 import TESpecificationType
    from mastapy._private.gears._368 import WormAddendumFactor
    from mastapy._private.gears._369 import WormType
    from mastapy._private.gears._370 import ZerolBevelGleasonToothTaperOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears._332": ["AccuracyGrades"],
        "_private.gears._333": ["AGMAToleranceStandard"],
        "_private.gears._334": ["BevelHypoidGearDesignSettings"],
        "_private.gears._335": ["BevelHypoidGearRatingSettings"],
        "_private.gears._336": ["CentreDistanceChangeMethod"],
        "_private.gears._337": ["CoefficientOfFrictionCalculationMethod"],
        "_private.gears._338": ["ConicalGearToothSurface"],
        "_private.gears._339": ["ContactRatioDataSource"],
        "_private.gears._340": ["ContactRatioRequirements"],
        "_private.gears._341": ["CylindricalFlanks"],
        "_private.gears._342": ["CylindricalMisalignmentDataSource"],
        "_private.gears._343": ["DeflectionFromBendingOption"],
        "_private.gears._344": ["GearFlanks"],
        "_private.gears._345": ["GearNURBSSurface"],
        "_private.gears._346": ["GearSetDesignGroup"],
        "_private.gears._347": ["GearSetModes"],
        "_private.gears._348": ["GearSetOptimisationResult"],
        "_private.gears._349": ["GearSetOptimisationResults"],
        "_private.gears._350": ["GearSetOptimiser"],
        "_private.gears._351": ["Hand"],
        "_private.gears._352": ["ISOToleranceStandard"],
        "_private.gears._353": ["LubricationMethods"],
        "_private.gears._354": ["MicroGeometryInputTypes"],
        "_private.gears._355": ["MicroGeometryModel"],
        "_private.gears._356": ["MicropittingCoefficientOfFrictionCalculationMethod"],
        "_private.gears._357": ["NamedPlanetAngle"],
        "_private.gears._358": ["PlanetaryDetail"],
        "_private.gears._359": ["PlanetaryRatingLoadSharingOption"],
        "_private.gears._360": ["PocketingPowerLossCoefficients"],
        "_private.gears._361": ["PocketingPowerLossCoefficientsDatabase"],
        "_private.gears._362": ["QualityGradeTypes"],
        "_private.gears._363": ["SafetyRequirementsAGMA"],
        "_private.gears._364": ["SpecificationForTheEffectOfOilKinematicViscosity"],
        "_private.gears._365": ["SpiralBevelRootLineTilt"],
        "_private.gears._366": ["SpiralBevelToothTaper"],
        "_private.gears._367": ["TESpecificationType"],
        "_private.gears._368": ["WormAddendumFactor"],
        "_private.gears._369": ["WormType"],
        "_private.gears._370": ["ZerolBevelGleasonToothTaperOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AccuracyGrades",
    "AGMAToleranceStandard",
    "BevelHypoidGearDesignSettings",
    "BevelHypoidGearRatingSettings",
    "CentreDistanceChangeMethod",
    "CoefficientOfFrictionCalculationMethod",
    "ConicalGearToothSurface",
    "ContactRatioDataSource",
    "ContactRatioRequirements",
    "CylindricalFlanks",
    "CylindricalMisalignmentDataSource",
    "DeflectionFromBendingOption",
    "GearFlanks",
    "GearNURBSSurface",
    "GearSetDesignGroup",
    "GearSetModes",
    "GearSetOptimisationResult",
    "GearSetOptimisationResults",
    "GearSetOptimiser",
    "Hand",
    "ISOToleranceStandard",
    "LubricationMethods",
    "MicroGeometryInputTypes",
    "MicroGeometryModel",
    "MicropittingCoefficientOfFrictionCalculationMethod",
    "NamedPlanetAngle",
    "PlanetaryDetail",
    "PlanetaryRatingLoadSharingOption",
    "PocketingPowerLossCoefficients",
    "PocketingPowerLossCoefficientsDatabase",
    "QualityGradeTypes",
    "SafetyRequirementsAGMA",
    "SpecificationForTheEffectOfOilKinematicViscosity",
    "SpiralBevelRootLineTilt",
    "SpiralBevelToothTaper",
    "TESpecificationType",
    "WormAddendumFactor",
    "WormType",
    "ZerolBevelGleasonToothTaperOption",
)
