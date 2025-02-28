"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_set_pareto_optimiser._933 import BarForPareto
    from mastapy._private.gears.gear_set_pareto_optimiser._934 import (
        CandidateDisplayChoice,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._935 import ChartInfoBase
    from mastapy._private.gears.gear_set_pareto_optimiser._936 import (
        CylindricalGearSetParetoOptimiser,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._937 import (
        DesignSpaceSearchBase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._938 import (
        DesignSpaceSearchCandidateBase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._939 import (
        FaceGearSetParetoOptimiser,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._940 import GearNameMapper
    from mastapy._private.gears.gear_set_pareto_optimiser._941 import GearNamePicker
    from mastapy._private.gears.gear_set_pareto_optimiser._942 import (
        GearSetOptimiserCandidate,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._943 import (
        GearSetParetoOptimiser,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._944 import (
        HypoidGearSetParetoOptimiser,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._945 import (
        InputSliderForPareto,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._946 import LargerOrSmaller
    from mastapy._private.gears.gear_set_pareto_optimiser._947 import (
        MicroGeometryDesignSpaceSearch,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._948 import (
        MicroGeometryDesignSpaceSearchCandidate,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._949 import (
        MicroGeometryDesignSpaceSearchChartInformation,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._950 import (
        MicroGeometryDesignSpaceSearchStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._951 import (
        MicroGeometryGearSetDesignSpaceSearch,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._952 import (
        MicroGeometryGearSetDesignSpaceSearchStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._953 import (
        MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._954 import OptimisationTarget
    from mastapy._private.gears.gear_set_pareto_optimiser._955 import (
        ParetoConicalRatingOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._956 import (
        ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._957 import (
        ParetoCylindricalGearSetOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._958 import (
        ParetoCylindricalRatingOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._959 import (
        ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._960 import (
        ParetoFaceGearSetOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._961 import (
        ParetoFaceRatingOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._962 import (
        ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._963 import (
        ParetoHypoidGearSetOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._964 import (
        ParetoOptimiserChartInformation,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._965 import (
        ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._966 import (
        ParetoSpiralBevelGearSetOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._967 import (
        ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._968 import (
        ParetoStraightBevelGearSetOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._969 import (
        ReasonsForInvalidDesigns,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._970 import (
        SpiralBevelGearSetParetoOptimiser,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._971 import (
        StraightBevelGearSetParetoOptimiser,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_set_pareto_optimiser._933": ["BarForPareto"],
        "_private.gears.gear_set_pareto_optimiser._934": ["CandidateDisplayChoice"],
        "_private.gears.gear_set_pareto_optimiser._935": ["ChartInfoBase"],
        "_private.gears.gear_set_pareto_optimiser._936": [
            "CylindricalGearSetParetoOptimiser"
        ],
        "_private.gears.gear_set_pareto_optimiser._937": ["DesignSpaceSearchBase"],
        "_private.gears.gear_set_pareto_optimiser._938": [
            "DesignSpaceSearchCandidateBase"
        ],
        "_private.gears.gear_set_pareto_optimiser._939": ["FaceGearSetParetoOptimiser"],
        "_private.gears.gear_set_pareto_optimiser._940": ["GearNameMapper"],
        "_private.gears.gear_set_pareto_optimiser._941": ["GearNamePicker"],
        "_private.gears.gear_set_pareto_optimiser._942": ["GearSetOptimiserCandidate"],
        "_private.gears.gear_set_pareto_optimiser._943": ["GearSetParetoOptimiser"],
        "_private.gears.gear_set_pareto_optimiser._944": [
            "HypoidGearSetParetoOptimiser"
        ],
        "_private.gears.gear_set_pareto_optimiser._945": ["InputSliderForPareto"],
        "_private.gears.gear_set_pareto_optimiser._946": ["LargerOrSmaller"],
        "_private.gears.gear_set_pareto_optimiser._947": [
            "MicroGeometryDesignSpaceSearch"
        ],
        "_private.gears.gear_set_pareto_optimiser._948": [
            "MicroGeometryDesignSpaceSearchCandidate"
        ],
        "_private.gears.gear_set_pareto_optimiser._949": [
            "MicroGeometryDesignSpaceSearchChartInformation"
        ],
        "_private.gears.gear_set_pareto_optimiser._950": [
            "MicroGeometryDesignSpaceSearchStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._951": [
            "MicroGeometryGearSetDesignSpaceSearch"
        ],
        "_private.gears.gear_set_pareto_optimiser._952": [
            "MicroGeometryGearSetDesignSpaceSearchStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._953": [
            "MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._954": ["OptimisationTarget"],
        "_private.gears.gear_set_pareto_optimiser._955": [
            "ParetoConicalRatingOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._956": [
            "ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._957": [
            "ParetoCylindricalGearSetOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._958": [
            "ParetoCylindricalRatingOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._959": [
            "ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._960": [
            "ParetoFaceGearSetOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._961": [
            "ParetoFaceRatingOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._962": [
            "ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._963": [
            "ParetoHypoidGearSetOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._964": [
            "ParetoOptimiserChartInformation"
        ],
        "_private.gears.gear_set_pareto_optimiser._965": [
            "ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._966": [
            "ParetoSpiralBevelGearSetOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._967": [
            "ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._968": [
            "ParetoStraightBevelGearSetOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._969": ["ReasonsForInvalidDesigns"],
        "_private.gears.gear_set_pareto_optimiser._970": [
            "SpiralBevelGearSetParetoOptimiser"
        ],
        "_private.gears.gear_set_pareto_optimiser._971": [
            "StraightBevelGearSetParetoOptimiser"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BarForPareto",
    "CandidateDisplayChoice",
    "ChartInfoBase",
    "CylindricalGearSetParetoOptimiser",
    "DesignSpaceSearchBase",
    "DesignSpaceSearchCandidateBase",
    "FaceGearSetParetoOptimiser",
    "GearNameMapper",
    "GearNamePicker",
    "GearSetOptimiserCandidate",
    "GearSetParetoOptimiser",
    "HypoidGearSetParetoOptimiser",
    "InputSliderForPareto",
    "LargerOrSmaller",
    "MicroGeometryDesignSpaceSearch",
    "MicroGeometryDesignSpaceSearchCandidate",
    "MicroGeometryDesignSpaceSearchChartInformation",
    "MicroGeometryDesignSpaceSearchStrategyDatabase",
    "MicroGeometryGearSetDesignSpaceSearch",
    "MicroGeometryGearSetDesignSpaceSearchStrategyDatabase",
    "MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase",
    "OptimisationTarget",
    "ParetoConicalRatingOptimisationStrategyDatabase",
    "ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase",
    "ParetoCylindricalGearSetOptimisationStrategyDatabase",
    "ParetoCylindricalRatingOptimisationStrategyDatabase",
    "ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase",
    "ParetoFaceGearSetOptimisationStrategyDatabase",
    "ParetoFaceRatingOptimisationStrategyDatabase",
    "ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase",
    "ParetoHypoidGearSetOptimisationStrategyDatabase",
    "ParetoOptimiserChartInformation",
    "ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase",
    "ParetoSpiralBevelGearSetOptimisationStrategyDatabase",
    "ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase",
    "ParetoStraightBevelGearSetOptimisationStrategyDatabase",
    "ReasonsForInvalidDesigns",
    "SpiralBevelGearSetParetoOptimiser",
    "StraightBevelGearSetParetoOptimiser",
)
