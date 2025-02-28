"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.ltca.conical._894 import ConicalGearBendingStiffness
    from mastapy._private.gears.ltca.conical._895 import ConicalGearBendingStiffnessNode
    from mastapy._private.gears.ltca.conical._896 import ConicalGearContactStiffness
    from mastapy._private.gears.ltca.conical._897 import ConicalGearContactStiffnessNode
    from mastapy._private.gears.ltca.conical._898 import (
        ConicalGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._899 import (
        ConicalGearSetLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._900 import (
        ConicalMeshedGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._901 import (
        ConicalMeshLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._902 import (
        ConicalMeshLoadDistributionAtRotation,
    )
    from mastapy._private.gears.ltca.conical._903 import ConicalMeshLoadedContactLine
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.ltca.conical._894": ["ConicalGearBendingStiffness"],
        "_private.gears.ltca.conical._895": ["ConicalGearBendingStiffnessNode"],
        "_private.gears.ltca.conical._896": ["ConicalGearContactStiffness"],
        "_private.gears.ltca.conical._897": ["ConicalGearContactStiffnessNode"],
        "_private.gears.ltca.conical._898": ["ConicalGearLoadDistributionAnalysis"],
        "_private.gears.ltca.conical._899": ["ConicalGearSetLoadDistributionAnalysis"],
        "_private.gears.ltca.conical._900": [
            "ConicalMeshedGearLoadDistributionAnalysis"
        ],
        "_private.gears.ltca.conical._901": ["ConicalMeshLoadDistributionAnalysis"],
        "_private.gears.ltca.conical._902": ["ConicalMeshLoadDistributionAtRotation"],
        "_private.gears.ltca.conical._903": ["ConicalMeshLoadedContactLine"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearBendingStiffness",
    "ConicalGearBendingStiffnessNode",
    "ConicalGearContactStiffness",
    "ConicalGearContactStiffnessNode",
    "ConicalGearLoadDistributionAnalysis",
    "ConicalGearSetLoadDistributionAnalysis",
    "ConicalMeshedGearLoadDistributionAnalysis",
    "ConicalMeshLoadDistributionAnalysis",
    "ConicalMeshLoadDistributionAtRotation",
    "ConicalMeshLoadedContactLine",
)
