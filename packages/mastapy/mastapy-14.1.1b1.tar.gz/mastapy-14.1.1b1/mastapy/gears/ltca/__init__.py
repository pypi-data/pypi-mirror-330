"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.ltca._856 import ConicalGearFilletStressResults
    from mastapy._private.gears.ltca._857 import ConicalGearRootFilletStressResults
    from mastapy._private.gears.ltca._858 import ContactResultType
    from mastapy._private.gears.ltca._859 import CylindricalGearFilletNodeStressResults
    from mastapy._private.gears.ltca._860 import (
        CylindricalGearFilletNodeStressResultsColumn,
    )
    from mastapy._private.gears.ltca._861 import (
        CylindricalGearFilletNodeStressResultsRow,
    )
    from mastapy._private.gears.ltca._862 import CylindricalGearRootFilletStressResults
    from mastapy._private.gears.ltca._863 import (
        CylindricalMeshedGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca._864 import GearBendingStiffness
    from mastapy._private.gears.ltca._865 import GearBendingStiffnessNode
    from mastapy._private.gears.ltca._866 import GearContactStiffness
    from mastapy._private.gears.ltca._867 import GearContactStiffnessNode
    from mastapy._private.gears.ltca._868 import GearFilletNodeStressResults
    from mastapy._private.gears.ltca._869 import GearFilletNodeStressResultsColumn
    from mastapy._private.gears.ltca._870 import GearFilletNodeStressResultsRow
    from mastapy._private.gears.ltca._871 import GearLoadDistributionAnalysis
    from mastapy._private.gears.ltca._872 import GearMeshLoadDistributionAnalysis
    from mastapy._private.gears.ltca._873 import GearMeshLoadDistributionAtRotation
    from mastapy._private.gears.ltca._874 import GearMeshLoadedContactLine
    from mastapy._private.gears.ltca._875 import GearMeshLoadedContactPoint
    from mastapy._private.gears.ltca._876 import GearRootFilletStressResults
    from mastapy._private.gears.ltca._877 import GearSetLoadDistributionAnalysis
    from mastapy._private.gears.ltca._878 import GearStiffness
    from mastapy._private.gears.ltca._879 import GearStiffnessNode
    from mastapy._private.gears.ltca._880 import (
        MeshedGearLoadDistributionAnalysisAtRotation,
    )
    from mastapy._private.gears.ltca._881 import UseAdvancedLTCAOptions
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.ltca._856": ["ConicalGearFilletStressResults"],
        "_private.gears.ltca._857": ["ConicalGearRootFilletStressResults"],
        "_private.gears.ltca._858": ["ContactResultType"],
        "_private.gears.ltca._859": ["CylindricalGearFilletNodeStressResults"],
        "_private.gears.ltca._860": ["CylindricalGearFilletNodeStressResultsColumn"],
        "_private.gears.ltca._861": ["CylindricalGearFilletNodeStressResultsRow"],
        "_private.gears.ltca._862": ["CylindricalGearRootFilletStressResults"],
        "_private.gears.ltca._863": ["CylindricalMeshedGearLoadDistributionAnalysis"],
        "_private.gears.ltca._864": ["GearBendingStiffness"],
        "_private.gears.ltca._865": ["GearBendingStiffnessNode"],
        "_private.gears.ltca._866": ["GearContactStiffness"],
        "_private.gears.ltca._867": ["GearContactStiffnessNode"],
        "_private.gears.ltca._868": ["GearFilletNodeStressResults"],
        "_private.gears.ltca._869": ["GearFilletNodeStressResultsColumn"],
        "_private.gears.ltca._870": ["GearFilletNodeStressResultsRow"],
        "_private.gears.ltca._871": ["GearLoadDistributionAnalysis"],
        "_private.gears.ltca._872": ["GearMeshLoadDistributionAnalysis"],
        "_private.gears.ltca._873": ["GearMeshLoadDistributionAtRotation"],
        "_private.gears.ltca._874": ["GearMeshLoadedContactLine"],
        "_private.gears.ltca._875": ["GearMeshLoadedContactPoint"],
        "_private.gears.ltca._876": ["GearRootFilletStressResults"],
        "_private.gears.ltca._877": ["GearSetLoadDistributionAnalysis"],
        "_private.gears.ltca._878": ["GearStiffness"],
        "_private.gears.ltca._879": ["GearStiffnessNode"],
        "_private.gears.ltca._880": ["MeshedGearLoadDistributionAnalysisAtRotation"],
        "_private.gears.ltca._881": ["UseAdvancedLTCAOptions"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearFilletStressResults",
    "ConicalGearRootFilletStressResults",
    "ContactResultType",
    "CylindricalGearFilletNodeStressResults",
    "CylindricalGearFilletNodeStressResultsColumn",
    "CylindricalGearFilletNodeStressResultsRow",
    "CylindricalGearRootFilletStressResults",
    "CylindricalMeshedGearLoadDistributionAnalysis",
    "GearBendingStiffness",
    "GearBendingStiffnessNode",
    "GearContactStiffness",
    "GearContactStiffnessNode",
    "GearFilletNodeStressResults",
    "GearFilletNodeStressResultsColumn",
    "GearFilletNodeStressResultsRow",
    "GearLoadDistributionAnalysis",
    "GearMeshLoadDistributionAnalysis",
    "GearMeshLoadDistributionAtRotation",
    "GearMeshLoadedContactLine",
    "GearMeshLoadedContactPoint",
    "GearRootFilletStressResults",
    "GearSetLoadDistributionAnalysis",
    "GearStiffness",
    "GearStiffnessNode",
    "MeshedGearLoadDistributionAnalysisAtRotation",
    "UseAdvancedLTCAOptions",
)
