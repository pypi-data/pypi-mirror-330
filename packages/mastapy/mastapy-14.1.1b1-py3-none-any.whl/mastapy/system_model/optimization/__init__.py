"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.optimization._2289 import (
        ConicalGearOptimisationStrategy,
    )
    from mastapy._private.system_model.optimization._2290 import (
        ConicalGearOptimizationStep,
    )
    from mastapy._private.system_model.optimization._2291 import (
        ConicalGearOptimizationStrategyDatabase,
    )
    from mastapy._private.system_model.optimization._2292 import (
        CylindricalGearOptimisationStrategy,
    )
    from mastapy._private.system_model.optimization._2293 import (
        CylindricalGearOptimizationStep,
    )
    from mastapy._private.system_model.optimization._2294 import (
        MeasuredAndFactorViewModel,
    )
    from mastapy._private.system_model.optimization._2295 import (
        MicroGeometryOptimisationTarget,
    )
    from mastapy._private.system_model.optimization._2296 import OptimizationStep
    from mastapy._private.system_model.optimization._2297 import OptimizationStrategy
    from mastapy._private.system_model.optimization._2298 import (
        OptimizationStrategyBase,
    )
    from mastapy._private.system_model.optimization._2299 import (
        OptimizationStrategyDatabase,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.optimization._2289": ["ConicalGearOptimisationStrategy"],
        "_private.system_model.optimization._2290": ["ConicalGearOptimizationStep"],
        "_private.system_model.optimization._2291": [
            "ConicalGearOptimizationStrategyDatabase"
        ],
        "_private.system_model.optimization._2292": [
            "CylindricalGearOptimisationStrategy"
        ],
        "_private.system_model.optimization._2293": ["CylindricalGearOptimizationStep"],
        "_private.system_model.optimization._2294": ["MeasuredAndFactorViewModel"],
        "_private.system_model.optimization._2295": ["MicroGeometryOptimisationTarget"],
        "_private.system_model.optimization._2296": ["OptimizationStep"],
        "_private.system_model.optimization._2297": ["OptimizationStrategy"],
        "_private.system_model.optimization._2298": ["OptimizationStrategyBase"],
        "_private.system_model.optimization._2299": ["OptimizationStrategyDatabase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearOptimisationStrategy",
    "ConicalGearOptimizationStep",
    "ConicalGearOptimizationStrategyDatabase",
    "CylindricalGearOptimisationStrategy",
    "CylindricalGearOptimizationStep",
    "MeasuredAndFactorViewModel",
    "MicroGeometryOptimisationTarget",
    "OptimizationStep",
    "OptimizationStrategy",
    "OptimizationStrategyBase",
    "OptimizationStrategyDatabase",
)
