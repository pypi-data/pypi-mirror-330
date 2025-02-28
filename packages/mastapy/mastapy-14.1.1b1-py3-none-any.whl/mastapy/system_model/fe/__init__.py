"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe._2418 import AlignConnectedComponentOptions
    from mastapy._private.system_model.fe._2419 import AlignmentMethod
    from mastapy._private.system_model.fe._2420 import AlignmentMethodForRaceBearing
    from mastapy._private.system_model.fe._2421 import AlignmentUsingAxialNodePositions
    from mastapy._private.system_model.fe._2422 import AngleSource
    from mastapy._private.system_model.fe._2423 import BaseFEWithSelection
    from mastapy._private.system_model.fe._2424 import BatchOperations
    from mastapy._private.system_model.fe._2425 import BearingNodeAlignmentOption
    from mastapy._private.system_model.fe._2426 import BearingNodeOption
    from mastapy._private.system_model.fe._2427 import BearingRaceNodeLink
    from mastapy._private.system_model.fe._2428 import BearingRacePosition
    from mastapy._private.system_model.fe._2429 import ComponentOrientationOption
    from mastapy._private.system_model.fe._2430 import ContactPairWithSelection
    from mastapy._private.system_model.fe._2431 import CoordinateSystemWithSelection
    from mastapy._private.system_model.fe._2432 import CreateConnectedComponentOptions
    from mastapy._private.system_model.fe._2433 import (
        CreateMicrophoneNormalToSurfaceOptions,
    )
    from mastapy._private.system_model.fe._2434 import DegreeOfFreedomBoundaryCondition
    from mastapy._private.system_model.fe._2435 import (
        DegreeOfFreedomBoundaryConditionAngular,
    )
    from mastapy._private.system_model.fe._2436 import (
        DegreeOfFreedomBoundaryConditionLinear,
    )
    from mastapy._private.system_model.fe._2437 import ElectricMachineDataSet
    from mastapy._private.system_model.fe._2438 import ElectricMachineDynamicLoadData
    from mastapy._private.system_model.fe._2439 import ElementFaceGroupWithSelection
    from mastapy._private.system_model.fe._2440 import ElementPropertiesWithSelection
    from mastapy._private.system_model.fe._2441 import FEEntityGroupWithSelection
    from mastapy._private.system_model.fe._2442 import FEExportSettings
    from mastapy._private.system_model.fe._2443 import FEPartDRIVASurfaceSelection
    from mastapy._private.system_model.fe._2444 import FEPartWithBatchOptions
    from mastapy._private.system_model.fe._2445 import FEStiffnessGeometry
    from mastapy._private.system_model.fe._2446 import FEStiffnessTester
    from mastapy._private.system_model.fe._2447 import FESubstructure
    from mastapy._private.system_model.fe._2448 import FESubstructureExportOptions
    from mastapy._private.system_model.fe._2449 import FESubstructureNode
    from mastapy._private.system_model.fe._2450 import FESubstructureNodeModeShape
    from mastapy._private.system_model.fe._2451 import FESubstructureNodeModeShapes
    from mastapy._private.system_model.fe._2452 import FESubstructureType
    from mastapy._private.system_model.fe._2453 import FESubstructureWithBatchOptions
    from mastapy._private.system_model.fe._2454 import FESubstructureWithSelection
    from mastapy._private.system_model.fe._2455 import (
        FESubstructureWithSelectionComponents,
    )
    from mastapy._private.system_model.fe._2456 import (
        FESubstructureWithSelectionForHarmonicAnalysis,
    )
    from mastapy._private.system_model.fe._2457 import (
        FESubstructureWithSelectionForModalAnalysis,
    )
    from mastapy._private.system_model.fe._2458 import (
        FESubstructureWithSelectionForStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2459 import GearMeshingOptions
    from mastapy._private.system_model.fe._2460 import (
        IndependentMASTACreatedCondensationNode,
    )
    from mastapy._private.system_model.fe._2461 import (
        LinkComponentAxialPositionErrorReporter,
    )
    from mastapy._private.system_model.fe._2462 import LinkNodeSource
    from mastapy._private.system_model.fe._2463 import MaterialPropertiesWithSelection
    from mastapy._private.system_model.fe._2464 import (
        NodeBoundaryConditionStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2465 import NodeGroupWithSelection
    from mastapy._private.system_model.fe._2466 import NodeSelectionDepthOption
    from mastapy._private.system_model.fe._2467 import (
        OptionsWhenExternalFEFileAlreadyExists,
    )
    from mastapy._private.system_model.fe._2468 import PerLinkExportOptions
    from mastapy._private.system_model.fe._2469 import PerNodeExportOptions
    from mastapy._private.system_model.fe._2470 import RaceBearingFE
    from mastapy._private.system_model.fe._2471 import RaceBearingFESystemDeflection
    from mastapy._private.system_model.fe._2472 import RaceBearingFEWithSelection
    from mastapy._private.system_model.fe._2473 import ReplacedShaftSelectionHelper
    from mastapy._private.system_model.fe._2474 import SystemDeflectionFEExportOptions
    from mastapy._private.system_model.fe._2475 import ThermalExpansionOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe._2418": ["AlignConnectedComponentOptions"],
        "_private.system_model.fe._2419": ["AlignmentMethod"],
        "_private.system_model.fe._2420": ["AlignmentMethodForRaceBearing"],
        "_private.system_model.fe._2421": ["AlignmentUsingAxialNodePositions"],
        "_private.system_model.fe._2422": ["AngleSource"],
        "_private.system_model.fe._2423": ["BaseFEWithSelection"],
        "_private.system_model.fe._2424": ["BatchOperations"],
        "_private.system_model.fe._2425": ["BearingNodeAlignmentOption"],
        "_private.system_model.fe._2426": ["BearingNodeOption"],
        "_private.system_model.fe._2427": ["BearingRaceNodeLink"],
        "_private.system_model.fe._2428": ["BearingRacePosition"],
        "_private.system_model.fe._2429": ["ComponentOrientationOption"],
        "_private.system_model.fe._2430": ["ContactPairWithSelection"],
        "_private.system_model.fe._2431": ["CoordinateSystemWithSelection"],
        "_private.system_model.fe._2432": ["CreateConnectedComponentOptions"],
        "_private.system_model.fe._2433": ["CreateMicrophoneNormalToSurfaceOptions"],
        "_private.system_model.fe._2434": ["DegreeOfFreedomBoundaryCondition"],
        "_private.system_model.fe._2435": ["DegreeOfFreedomBoundaryConditionAngular"],
        "_private.system_model.fe._2436": ["DegreeOfFreedomBoundaryConditionLinear"],
        "_private.system_model.fe._2437": ["ElectricMachineDataSet"],
        "_private.system_model.fe._2438": ["ElectricMachineDynamicLoadData"],
        "_private.system_model.fe._2439": ["ElementFaceGroupWithSelection"],
        "_private.system_model.fe._2440": ["ElementPropertiesWithSelection"],
        "_private.system_model.fe._2441": ["FEEntityGroupWithSelection"],
        "_private.system_model.fe._2442": ["FEExportSettings"],
        "_private.system_model.fe._2443": ["FEPartDRIVASurfaceSelection"],
        "_private.system_model.fe._2444": ["FEPartWithBatchOptions"],
        "_private.system_model.fe._2445": ["FEStiffnessGeometry"],
        "_private.system_model.fe._2446": ["FEStiffnessTester"],
        "_private.system_model.fe._2447": ["FESubstructure"],
        "_private.system_model.fe._2448": ["FESubstructureExportOptions"],
        "_private.system_model.fe._2449": ["FESubstructureNode"],
        "_private.system_model.fe._2450": ["FESubstructureNodeModeShape"],
        "_private.system_model.fe._2451": ["FESubstructureNodeModeShapes"],
        "_private.system_model.fe._2452": ["FESubstructureType"],
        "_private.system_model.fe._2453": ["FESubstructureWithBatchOptions"],
        "_private.system_model.fe._2454": ["FESubstructureWithSelection"],
        "_private.system_model.fe._2455": ["FESubstructureWithSelectionComponents"],
        "_private.system_model.fe._2456": [
            "FESubstructureWithSelectionForHarmonicAnalysis"
        ],
        "_private.system_model.fe._2457": [
            "FESubstructureWithSelectionForModalAnalysis"
        ],
        "_private.system_model.fe._2458": [
            "FESubstructureWithSelectionForStaticAnalysis"
        ],
        "_private.system_model.fe._2459": ["GearMeshingOptions"],
        "_private.system_model.fe._2460": ["IndependentMASTACreatedCondensationNode"],
        "_private.system_model.fe._2461": ["LinkComponentAxialPositionErrorReporter"],
        "_private.system_model.fe._2462": ["LinkNodeSource"],
        "_private.system_model.fe._2463": ["MaterialPropertiesWithSelection"],
        "_private.system_model.fe._2464": ["NodeBoundaryConditionStaticAnalysis"],
        "_private.system_model.fe._2465": ["NodeGroupWithSelection"],
        "_private.system_model.fe._2466": ["NodeSelectionDepthOption"],
        "_private.system_model.fe._2467": ["OptionsWhenExternalFEFileAlreadyExists"],
        "_private.system_model.fe._2468": ["PerLinkExportOptions"],
        "_private.system_model.fe._2469": ["PerNodeExportOptions"],
        "_private.system_model.fe._2470": ["RaceBearingFE"],
        "_private.system_model.fe._2471": ["RaceBearingFESystemDeflection"],
        "_private.system_model.fe._2472": ["RaceBearingFEWithSelection"],
        "_private.system_model.fe._2473": ["ReplacedShaftSelectionHelper"],
        "_private.system_model.fe._2474": ["SystemDeflectionFEExportOptions"],
        "_private.system_model.fe._2475": ["ThermalExpansionOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AlignConnectedComponentOptions",
    "AlignmentMethod",
    "AlignmentMethodForRaceBearing",
    "AlignmentUsingAxialNodePositions",
    "AngleSource",
    "BaseFEWithSelection",
    "BatchOperations",
    "BearingNodeAlignmentOption",
    "BearingNodeOption",
    "BearingRaceNodeLink",
    "BearingRacePosition",
    "ComponentOrientationOption",
    "ContactPairWithSelection",
    "CoordinateSystemWithSelection",
    "CreateConnectedComponentOptions",
    "CreateMicrophoneNormalToSurfaceOptions",
    "DegreeOfFreedomBoundaryCondition",
    "DegreeOfFreedomBoundaryConditionAngular",
    "DegreeOfFreedomBoundaryConditionLinear",
    "ElectricMachineDataSet",
    "ElectricMachineDynamicLoadData",
    "ElementFaceGroupWithSelection",
    "ElementPropertiesWithSelection",
    "FEEntityGroupWithSelection",
    "FEExportSettings",
    "FEPartDRIVASurfaceSelection",
    "FEPartWithBatchOptions",
    "FEStiffnessGeometry",
    "FEStiffnessTester",
    "FESubstructure",
    "FESubstructureExportOptions",
    "FESubstructureNode",
    "FESubstructureNodeModeShape",
    "FESubstructureNodeModeShapes",
    "FESubstructureType",
    "FESubstructureWithBatchOptions",
    "FESubstructureWithSelection",
    "FESubstructureWithSelectionComponents",
    "FESubstructureWithSelectionForHarmonicAnalysis",
    "FESubstructureWithSelectionForModalAnalysis",
    "FESubstructureWithSelectionForStaticAnalysis",
    "GearMeshingOptions",
    "IndependentMASTACreatedCondensationNode",
    "LinkComponentAxialPositionErrorReporter",
    "LinkNodeSource",
    "MaterialPropertiesWithSelection",
    "NodeBoundaryConditionStaticAnalysis",
    "NodeGroupWithSelection",
    "NodeSelectionDepthOption",
    "OptionsWhenExternalFEFileAlreadyExists",
    "PerLinkExportOptions",
    "PerNodeExportOptions",
    "RaceBearingFE",
    "RaceBearingFESystemDeflection",
    "RaceBearingFEWithSelection",
    "ReplacedShaftSelectionHelper",
    "SystemDeflectionFEExportOptions",
    "ThermalExpansionOption",
)
