"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.micro_geometry._588 import BiasModification
    from mastapy._private.gears.micro_geometry._589 import FlankMicroGeometry
    from mastapy._private.gears.micro_geometry._590 import FlankSide
    from mastapy._private.gears.micro_geometry._591 import LeadModification
    from mastapy._private.gears.micro_geometry._592 import (
        LocationOfEvaluationLowerLimit,
    )
    from mastapy._private.gears.micro_geometry._593 import (
        LocationOfEvaluationUpperLimit,
    )
    from mastapy._private.gears.micro_geometry._594 import (
        LocationOfRootReliefEvaluation,
    )
    from mastapy._private.gears.micro_geometry._595 import LocationOfTipReliefEvaluation
    from mastapy._private.gears.micro_geometry._596 import (
        MainProfileReliefEndsAtTheStartOfRootReliefOption,
    )
    from mastapy._private.gears.micro_geometry._597 import (
        MainProfileReliefEndsAtTheStartOfTipReliefOption,
    )
    from mastapy._private.gears.micro_geometry._598 import Modification
    from mastapy._private.gears.micro_geometry._599 import (
        ParabolicRootReliefStartsTangentToMainProfileRelief,
    )
    from mastapy._private.gears.micro_geometry._600 import (
        ParabolicTipReliefStartsTangentToMainProfileRelief,
    )
    from mastapy._private.gears.micro_geometry._601 import ProfileModification
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.micro_geometry._588": ["BiasModification"],
        "_private.gears.micro_geometry._589": ["FlankMicroGeometry"],
        "_private.gears.micro_geometry._590": ["FlankSide"],
        "_private.gears.micro_geometry._591": ["LeadModification"],
        "_private.gears.micro_geometry._592": ["LocationOfEvaluationLowerLimit"],
        "_private.gears.micro_geometry._593": ["LocationOfEvaluationUpperLimit"],
        "_private.gears.micro_geometry._594": ["LocationOfRootReliefEvaluation"],
        "_private.gears.micro_geometry._595": ["LocationOfTipReliefEvaluation"],
        "_private.gears.micro_geometry._596": [
            "MainProfileReliefEndsAtTheStartOfRootReliefOption"
        ],
        "_private.gears.micro_geometry._597": [
            "MainProfileReliefEndsAtTheStartOfTipReliefOption"
        ],
        "_private.gears.micro_geometry._598": ["Modification"],
        "_private.gears.micro_geometry._599": [
            "ParabolicRootReliefStartsTangentToMainProfileRelief"
        ],
        "_private.gears.micro_geometry._600": [
            "ParabolicTipReliefStartsTangentToMainProfileRelief"
        ],
        "_private.gears.micro_geometry._601": ["ProfileModification"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BiasModification",
    "FlankMicroGeometry",
    "FlankSide",
    "LeadModification",
    "LocationOfEvaluationLowerLimit",
    "LocationOfEvaluationUpperLimit",
    "LocationOfRootReliefEvaluation",
    "LocationOfTipReliefEvaluation",
    "MainProfileReliefEndsAtTheStartOfRootReliefOption",
    "MainProfileReliefEndsAtTheStartOfTipReliefOption",
    "Modification",
    "ParabolicRootReliefStartsTangentToMainProfileRelief",
    "ParabolicTipReliefStartsTangentToMainProfileRelief",
    "ProfileModification",
)
