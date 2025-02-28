"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.cylindrical._470 import AGMAScuffingResultsRow
    from mastapy._private.gears.rating.cylindrical._471 import (
        CylindricalGearDesignAndRatingSettings,
    )
    from mastapy._private.gears.rating.cylindrical._472 import (
        CylindricalGearDesignAndRatingSettingsDatabase,
    )
    from mastapy._private.gears.rating.cylindrical._473 import (
        CylindricalGearDesignAndRatingSettingsItem,
    )
    from mastapy._private.gears.rating.cylindrical._474 import (
        CylindricalGearDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._475 import (
        CylindricalGearFlankDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._476 import (
        CylindricalGearFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical._477 import CylindricalGearMeshRating
    from mastapy._private.gears.rating.cylindrical._478 import (
        CylindricalGearMicroPittingResults,
    )
    from mastapy._private.gears.rating.cylindrical._479 import CylindricalGearRating
    from mastapy._private.gears.rating.cylindrical._480 import (
        CylindricalGearRatingGeometryDataSource,
    )
    from mastapy._private.gears.rating.cylindrical._481 import (
        CylindricalGearScuffingResults,
    )
    from mastapy._private.gears.rating.cylindrical._482 import (
        CylindricalGearSetDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._483 import CylindricalGearSetRating
    from mastapy._private.gears.rating.cylindrical._484 import (
        CylindricalGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical._485 import (
        CylindricalMeshDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._486 import (
        CylindricalMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical._487 import (
        CylindricalPlasticGearRatingSettings,
    )
    from mastapy._private.gears.rating.cylindrical._488 import (
        CylindricalPlasticGearRatingSettingsDatabase,
    )
    from mastapy._private.gears.rating.cylindrical._489 import (
        CylindricalPlasticGearRatingSettingsItem,
    )
    from mastapy._private.gears.rating.cylindrical._490 import CylindricalRateableMesh
    from mastapy._private.gears.rating.cylindrical._491 import DynamicFactorMethods
    from mastapy._private.gears.rating.cylindrical._492 import (
        GearBlankFactorCalculationOptions,
    )
    from mastapy._private.gears.rating.cylindrical._493 import ISOScuffingResultsRow
    from mastapy._private.gears.rating.cylindrical._494 import MeshRatingForReports
    from mastapy._private.gears.rating.cylindrical._495 import MicropittingRatingMethod
    from mastapy._private.gears.rating.cylindrical._496 import MicroPittingResultsRow
    from mastapy._private.gears.rating.cylindrical._497 import (
        MisalignmentContactPatternEnhancements,
    )
    from mastapy._private.gears.rating.cylindrical._498 import RatingMethod
    from mastapy._private.gears.rating.cylindrical._499 import (
        ReducedCylindricalGearSetDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._500 import (
        ScuffingFlashTemperatureRatingMethod,
    )
    from mastapy._private.gears.rating.cylindrical._501 import (
        ScuffingIntegralTemperatureRatingMethod,
    )
    from mastapy._private.gears.rating.cylindrical._502 import ScuffingMethods
    from mastapy._private.gears.rating.cylindrical._503 import ScuffingResultsRow
    from mastapy._private.gears.rating.cylindrical._504 import ScuffingResultsRowGear
    from mastapy._private.gears.rating.cylindrical._505 import TipReliefScuffingOptions
    from mastapy._private.gears.rating.cylindrical._506 import ToothThicknesses
    from mastapy._private.gears.rating.cylindrical._507 import (
        VDI2737SafetyFactorReportingObject,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.cylindrical._470": ["AGMAScuffingResultsRow"],
        "_private.gears.rating.cylindrical._471": [
            "CylindricalGearDesignAndRatingSettings"
        ],
        "_private.gears.rating.cylindrical._472": [
            "CylindricalGearDesignAndRatingSettingsDatabase"
        ],
        "_private.gears.rating.cylindrical._473": [
            "CylindricalGearDesignAndRatingSettingsItem"
        ],
        "_private.gears.rating.cylindrical._474": ["CylindricalGearDutyCycleRating"],
        "_private.gears.rating.cylindrical._475": [
            "CylindricalGearFlankDutyCycleRating"
        ],
        "_private.gears.rating.cylindrical._476": ["CylindricalGearFlankRating"],
        "_private.gears.rating.cylindrical._477": ["CylindricalGearMeshRating"],
        "_private.gears.rating.cylindrical._478": [
            "CylindricalGearMicroPittingResults"
        ],
        "_private.gears.rating.cylindrical._479": ["CylindricalGearRating"],
        "_private.gears.rating.cylindrical._480": [
            "CylindricalGearRatingGeometryDataSource"
        ],
        "_private.gears.rating.cylindrical._481": ["CylindricalGearScuffingResults"],
        "_private.gears.rating.cylindrical._482": ["CylindricalGearSetDutyCycleRating"],
        "_private.gears.rating.cylindrical._483": ["CylindricalGearSetRating"],
        "_private.gears.rating.cylindrical._484": ["CylindricalGearSingleFlankRating"],
        "_private.gears.rating.cylindrical._485": ["CylindricalMeshDutyCycleRating"],
        "_private.gears.rating.cylindrical._486": ["CylindricalMeshSingleFlankRating"],
        "_private.gears.rating.cylindrical._487": [
            "CylindricalPlasticGearRatingSettings"
        ],
        "_private.gears.rating.cylindrical._488": [
            "CylindricalPlasticGearRatingSettingsDatabase"
        ],
        "_private.gears.rating.cylindrical._489": [
            "CylindricalPlasticGearRatingSettingsItem"
        ],
        "_private.gears.rating.cylindrical._490": ["CylindricalRateableMesh"],
        "_private.gears.rating.cylindrical._491": ["DynamicFactorMethods"],
        "_private.gears.rating.cylindrical._492": ["GearBlankFactorCalculationOptions"],
        "_private.gears.rating.cylindrical._493": ["ISOScuffingResultsRow"],
        "_private.gears.rating.cylindrical._494": ["MeshRatingForReports"],
        "_private.gears.rating.cylindrical._495": ["MicropittingRatingMethod"],
        "_private.gears.rating.cylindrical._496": ["MicroPittingResultsRow"],
        "_private.gears.rating.cylindrical._497": [
            "MisalignmentContactPatternEnhancements"
        ],
        "_private.gears.rating.cylindrical._498": ["RatingMethod"],
        "_private.gears.rating.cylindrical._499": [
            "ReducedCylindricalGearSetDutyCycleRating"
        ],
        "_private.gears.rating.cylindrical._500": [
            "ScuffingFlashTemperatureRatingMethod"
        ],
        "_private.gears.rating.cylindrical._501": [
            "ScuffingIntegralTemperatureRatingMethod"
        ],
        "_private.gears.rating.cylindrical._502": ["ScuffingMethods"],
        "_private.gears.rating.cylindrical._503": ["ScuffingResultsRow"],
        "_private.gears.rating.cylindrical._504": ["ScuffingResultsRowGear"],
        "_private.gears.rating.cylindrical._505": ["TipReliefScuffingOptions"],
        "_private.gears.rating.cylindrical._506": ["ToothThicknesses"],
        "_private.gears.rating.cylindrical._507": [
            "VDI2737SafetyFactorReportingObject"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMAScuffingResultsRow",
    "CylindricalGearDesignAndRatingSettings",
    "CylindricalGearDesignAndRatingSettingsDatabase",
    "CylindricalGearDesignAndRatingSettingsItem",
    "CylindricalGearDutyCycleRating",
    "CylindricalGearFlankDutyCycleRating",
    "CylindricalGearFlankRating",
    "CylindricalGearMeshRating",
    "CylindricalGearMicroPittingResults",
    "CylindricalGearRating",
    "CylindricalGearRatingGeometryDataSource",
    "CylindricalGearScuffingResults",
    "CylindricalGearSetDutyCycleRating",
    "CylindricalGearSetRating",
    "CylindricalGearSingleFlankRating",
    "CylindricalMeshDutyCycleRating",
    "CylindricalMeshSingleFlankRating",
    "CylindricalPlasticGearRatingSettings",
    "CylindricalPlasticGearRatingSettingsDatabase",
    "CylindricalPlasticGearRatingSettingsItem",
    "CylindricalRateableMesh",
    "DynamicFactorMethods",
    "GearBlankFactorCalculationOptions",
    "ISOScuffingResultsRow",
    "MeshRatingForReports",
    "MicropittingRatingMethod",
    "MicroPittingResultsRow",
    "MisalignmentContactPatternEnhancements",
    "RatingMethod",
    "ReducedCylindricalGearSetDutyCycleRating",
    "ScuffingFlashTemperatureRatingMethod",
    "ScuffingIntegralTemperatureRatingMethod",
    "ScuffingMethods",
    "ScuffingResultsRow",
    "ScuffingResultsRowGear",
    "TipReliefScuffingOptions",
    "ToothThicknesses",
    "VDI2737SafetyFactorReportingObject",
)
