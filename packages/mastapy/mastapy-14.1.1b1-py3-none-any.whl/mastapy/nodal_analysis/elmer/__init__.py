"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.nodal_analysis.elmer._182 import ContactType
    from mastapy._private.nodal_analysis.elmer._183 import ElectricMachineAnalysisPeriod
    from mastapy._private.nodal_analysis.elmer._184 import ElmerResultEntityType
    from mastapy._private.nodal_analysis.elmer._185 import ElmerResults
    from mastapy._private.nodal_analysis.elmer._186 import (
        ElmerResultsFromElectromagneticAnalysis,
    )
    from mastapy._private.nodal_analysis.elmer._187 import (
        ElmerResultsFromMechanicalAnalysis,
    )
    from mastapy._private.nodal_analysis.elmer._188 import ElmerResultsViewable
    from mastapy._private.nodal_analysis.elmer._189 import ElmerResultType
    from mastapy._private.nodal_analysis.elmer._190 import (
        MechanicalContactSpecification,
    )
    from mastapy._private.nodal_analysis.elmer._191 import MechanicalSolverType
    from mastapy._private.nodal_analysis.elmer._192 import NodalAverageType
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.nodal_analysis.elmer._182": ["ContactType"],
        "_private.nodal_analysis.elmer._183": ["ElectricMachineAnalysisPeriod"],
        "_private.nodal_analysis.elmer._184": ["ElmerResultEntityType"],
        "_private.nodal_analysis.elmer._185": ["ElmerResults"],
        "_private.nodal_analysis.elmer._186": [
            "ElmerResultsFromElectromagneticAnalysis"
        ],
        "_private.nodal_analysis.elmer._187": ["ElmerResultsFromMechanicalAnalysis"],
        "_private.nodal_analysis.elmer._188": ["ElmerResultsViewable"],
        "_private.nodal_analysis.elmer._189": ["ElmerResultType"],
        "_private.nodal_analysis.elmer._190": ["MechanicalContactSpecification"],
        "_private.nodal_analysis.elmer._191": ["MechanicalSolverType"],
        "_private.nodal_analysis.elmer._192": ["NodalAverageType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ContactType",
    "ElectricMachineAnalysisPeriod",
    "ElmerResultEntityType",
    "ElmerResults",
    "ElmerResultsFromElectromagneticAnalysis",
    "ElmerResultsFromMechanicalAnalysis",
    "ElmerResultsViewable",
    "ElmerResultType",
    "MechanicalContactSpecification",
    "MechanicalSolverType",
    "NodalAverageType",
)
