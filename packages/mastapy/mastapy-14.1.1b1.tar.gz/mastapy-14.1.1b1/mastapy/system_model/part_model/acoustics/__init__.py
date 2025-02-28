"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.acoustics._2697 import (
        AcousticAnalysisOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2698 import (
        AcousticAnalysisSetup,
    )
    from mastapy._private.system_model.part_model.acoustics._2699 import (
        AcousticAnalysisSetupCacheReporting,
    )
    from mastapy._private.system_model.part_model.acoustics._2700 import (
        AcousticAnalysisSetupCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2701 import (
        AcousticEnvelopeType,
    )
    from mastapy._private.system_model.part_model.acoustics._2702 import (
        AcousticInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2703 import (
        CacheMemoryEstimates,
    )
    from mastapy._private.system_model.part_model.acoustics._2704 import (
        FEPartInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2705 import (
        FESurfaceSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2706 import HoleInFaceGroup
    from mastapy._private.system_model.part_model.acoustics._2707 import (
        MeshedResultPlane,
    )
    from mastapy._private.system_model.part_model.acoustics._2708 import (
        MeshedResultSphere,
    )
    from mastapy._private.system_model.part_model.acoustics._2709 import (
        MeshedResultSurface,
    )
    from mastapy._private.system_model.part_model.acoustics._2710 import (
        MeshedResultSurfaceBase,
    )
    from mastapy._private.system_model.part_model.acoustics._2711 import (
        MicrophoneArrayDesign,
    )
    from mastapy._private.system_model.part_model.acoustics._2712 import (
        PartSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2713 import (
        ResultPlaneOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2714 import (
        ResultSphereOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2715 import (
        ResultSurfaceCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2716 import (
        ResultSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2717 import (
        SphericalEnvelopeCentreDefinition,
    )
    from mastapy._private.system_model.part_model.acoustics._2718 import (
        SphericalEnvelopeType,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.acoustics._2697": ["AcousticAnalysisOptions"],
        "_private.system_model.part_model.acoustics._2698": ["AcousticAnalysisSetup"],
        "_private.system_model.part_model.acoustics._2699": [
            "AcousticAnalysisSetupCacheReporting"
        ],
        "_private.system_model.part_model.acoustics._2700": [
            "AcousticAnalysisSetupCollection"
        ],
        "_private.system_model.part_model.acoustics._2701": ["AcousticEnvelopeType"],
        "_private.system_model.part_model.acoustics._2702": [
            "AcousticInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2703": ["CacheMemoryEstimates"],
        "_private.system_model.part_model.acoustics._2704": [
            "FEPartInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2705": [
            "FESurfaceSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2706": ["HoleInFaceGroup"],
        "_private.system_model.part_model.acoustics._2707": ["MeshedResultPlane"],
        "_private.system_model.part_model.acoustics._2708": ["MeshedResultSphere"],
        "_private.system_model.part_model.acoustics._2709": ["MeshedResultSurface"],
        "_private.system_model.part_model.acoustics._2710": ["MeshedResultSurfaceBase"],
        "_private.system_model.part_model.acoustics._2711": ["MicrophoneArrayDesign"],
        "_private.system_model.part_model.acoustics._2712": [
            "PartSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2713": ["ResultPlaneOptions"],
        "_private.system_model.part_model.acoustics._2714": ["ResultSphereOptions"],
        "_private.system_model.part_model.acoustics._2715": ["ResultSurfaceCollection"],
        "_private.system_model.part_model.acoustics._2716": ["ResultSurfaceOptions"],
        "_private.system_model.part_model.acoustics._2717": [
            "SphericalEnvelopeCentreDefinition"
        ],
        "_private.system_model.part_model.acoustics._2718": ["SphericalEnvelopeType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AcousticAnalysisOptions",
    "AcousticAnalysisSetup",
    "AcousticAnalysisSetupCacheReporting",
    "AcousticAnalysisSetupCollection",
    "AcousticEnvelopeType",
    "AcousticInputSurfaceOptions",
    "CacheMemoryEstimates",
    "FEPartInputSurfaceOptions",
    "FESurfaceSelectionForAcousticEnvelope",
    "HoleInFaceGroup",
    "MeshedResultPlane",
    "MeshedResultSphere",
    "MeshedResultSurface",
    "MeshedResultSurfaceBase",
    "MicrophoneArrayDesign",
    "PartSelectionForAcousticEnvelope",
    "ResultPlaneOptions",
    "ResultSphereOptions",
    "ResultSurfaceCollection",
    "ResultSurfaceOptions",
    "SphericalEnvelopeCentreDefinition",
    "SphericalEnvelopeType",
)
