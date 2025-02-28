"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility.optimisation._1596 import AbstractOptimisable
    from mastapy._private.math_utility.optimisation._1597 import (
        DesignSpaceSearchStrategyDatabase,
    )
    from mastapy._private.math_utility.optimisation._1598 import InputSetter
    from mastapy._private.math_utility.optimisation._1599 import Optimisable
    from mastapy._private.math_utility.optimisation._1600 import OptimisationHistory
    from mastapy._private.math_utility.optimisation._1601 import OptimizationInput
    from mastapy._private.math_utility.optimisation._1602 import OptimizationVariable
    from mastapy._private.math_utility.optimisation._1603 import (
        ParetoOptimisationFilter,
    )
    from mastapy._private.math_utility.optimisation._1604 import ParetoOptimisationInput
    from mastapy._private.math_utility.optimisation._1605 import (
        ParetoOptimisationOutput,
    )
    from mastapy._private.math_utility.optimisation._1606 import (
        ParetoOptimisationStrategy,
    )
    from mastapy._private.math_utility.optimisation._1607 import (
        ParetoOptimisationStrategyBars,
    )
    from mastapy._private.math_utility.optimisation._1608 import (
        ParetoOptimisationStrategyChartInformation,
    )
    from mastapy._private.math_utility.optimisation._1609 import (
        ParetoOptimisationStrategyDatabase,
    )
    from mastapy._private.math_utility.optimisation._1610 import (
        ParetoOptimisationVariable,
    )
    from mastapy._private.math_utility.optimisation._1611 import (
        ParetoOptimisationVariableBase,
    )
    from mastapy._private.math_utility.optimisation._1612 import (
        PropertyTargetForDominantCandidateSearch,
    )
    from mastapy._private.math_utility.optimisation._1613 import (
        ReportingOptimizationInput,
    )
    from mastapy._private.math_utility.optimisation._1614 import (
        SpecifyOptimisationInputAs,
    )
    from mastapy._private.math_utility.optimisation._1615 import TargetingPropertyTo
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility.optimisation._1596": ["AbstractOptimisable"],
        "_private.math_utility.optimisation._1597": [
            "DesignSpaceSearchStrategyDatabase"
        ],
        "_private.math_utility.optimisation._1598": ["InputSetter"],
        "_private.math_utility.optimisation._1599": ["Optimisable"],
        "_private.math_utility.optimisation._1600": ["OptimisationHistory"],
        "_private.math_utility.optimisation._1601": ["OptimizationInput"],
        "_private.math_utility.optimisation._1602": ["OptimizationVariable"],
        "_private.math_utility.optimisation._1603": ["ParetoOptimisationFilter"],
        "_private.math_utility.optimisation._1604": ["ParetoOptimisationInput"],
        "_private.math_utility.optimisation._1605": ["ParetoOptimisationOutput"],
        "_private.math_utility.optimisation._1606": ["ParetoOptimisationStrategy"],
        "_private.math_utility.optimisation._1607": ["ParetoOptimisationStrategyBars"],
        "_private.math_utility.optimisation._1608": [
            "ParetoOptimisationStrategyChartInformation"
        ],
        "_private.math_utility.optimisation._1609": [
            "ParetoOptimisationStrategyDatabase"
        ],
        "_private.math_utility.optimisation._1610": ["ParetoOptimisationVariable"],
        "_private.math_utility.optimisation._1611": ["ParetoOptimisationVariableBase"],
        "_private.math_utility.optimisation._1612": [
            "PropertyTargetForDominantCandidateSearch"
        ],
        "_private.math_utility.optimisation._1613": ["ReportingOptimizationInput"],
        "_private.math_utility.optimisation._1614": ["SpecifyOptimisationInputAs"],
        "_private.math_utility.optimisation._1615": ["TargetingPropertyTo"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractOptimisable",
    "DesignSpaceSearchStrategyDatabase",
    "InputSetter",
    "Optimisable",
    "OptimisationHistory",
    "OptimizationInput",
    "OptimizationVariable",
    "ParetoOptimisationFilter",
    "ParetoOptimisationInput",
    "ParetoOptimisationOutput",
    "ParetoOptimisationStrategy",
    "ParetoOptimisationStrategyBars",
    "ParetoOptimisationStrategyChartInformation",
    "ParetoOptimisationStrategyDatabase",
    "ParetoOptimisationVariable",
    "ParetoOptimisationVariableBase",
    "PropertyTargetForDominantCandidateSearch",
    "ReportingOptimizationInput",
    "SpecifyOptimisationInputAs",
    "TargetingPropertyTo",
)
