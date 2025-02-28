"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.analysis._1263 import AbstractGearAnalysis
    from mastapy._private.gears.analysis._1264 import AbstractGearMeshAnalysis
    from mastapy._private.gears.analysis._1265 import AbstractGearSetAnalysis
    from mastapy._private.gears.analysis._1266 import GearDesignAnalysis
    from mastapy._private.gears.analysis._1267 import GearImplementationAnalysis
    from mastapy._private.gears.analysis._1268 import (
        GearImplementationAnalysisDutyCycle,
    )
    from mastapy._private.gears.analysis._1269 import GearImplementationDetail
    from mastapy._private.gears.analysis._1270 import GearMeshDesignAnalysis
    from mastapy._private.gears.analysis._1271 import GearMeshImplementationAnalysis
    from mastapy._private.gears.analysis._1272 import (
        GearMeshImplementationAnalysisDutyCycle,
    )
    from mastapy._private.gears.analysis._1273 import GearMeshImplementationDetail
    from mastapy._private.gears.analysis._1274 import GearSetDesignAnalysis
    from mastapy._private.gears.analysis._1275 import GearSetGroupDutyCycle
    from mastapy._private.gears.analysis._1276 import GearSetImplementationAnalysis
    from mastapy._private.gears.analysis._1277 import (
        GearSetImplementationAnalysisAbstract,
    )
    from mastapy._private.gears.analysis._1278 import (
        GearSetImplementationAnalysisDutyCycle,
    )
    from mastapy._private.gears.analysis._1279 import GearSetImplementationDetail
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.analysis._1263": ["AbstractGearAnalysis"],
        "_private.gears.analysis._1264": ["AbstractGearMeshAnalysis"],
        "_private.gears.analysis._1265": ["AbstractGearSetAnalysis"],
        "_private.gears.analysis._1266": ["GearDesignAnalysis"],
        "_private.gears.analysis._1267": ["GearImplementationAnalysis"],
        "_private.gears.analysis._1268": ["GearImplementationAnalysisDutyCycle"],
        "_private.gears.analysis._1269": ["GearImplementationDetail"],
        "_private.gears.analysis._1270": ["GearMeshDesignAnalysis"],
        "_private.gears.analysis._1271": ["GearMeshImplementationAnalysis"],
        "_private.gears.analysis._1272": ["GearMeshImplementationAnalysisDutyCycle"],
        "_private.gears.analysis._1273": ["GearMeshImplementationDetail"],
        "_private.gears.analysis._1274": ["GearSetDesignAnalysis"],
        "_private.gears.analysis._1275": ["GearSetGroupDutyCycle"],
        "_private.gears.analysis._1276": ["GearSetImplementationAnalysis"],
        "_private.gears.analysis._1277": ["GearSetImplementationAnalysisAbstract"],
        "_private.gears.analysis._1278": ["GearSetImplementationAnalysisDutyCycle"],
        "_private.gears.analysis._1279": ["GearSetImplementationDetail"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractGearAnalysis",
    "AbstractGearMeshAnalysis",
    "AbstractGearSetAnalysis",
    "GearDesignAnalysis",
    "GearImplementationAnalysis",
    "GearImplementationAnalysisDutyCycle",
    "GearImplementationDetail",
    "GearMeshDesignAnalysis",
    "GearMeshImplementationAnalysis",
    "GearMeshImplementationAnalysisDutyCycle",
    "GearMeshImplementationDetail",
    "GearSetDesignAnalysis",
    "GearSetGroupDutyCycle",
    "GearSetImplementationAnalysis",
    "GearSetImplementationAnalysisAbstract",
    "GearSetImplementationAnalysisDutyCycle",
    "GearSetImplementationDetail",
)
