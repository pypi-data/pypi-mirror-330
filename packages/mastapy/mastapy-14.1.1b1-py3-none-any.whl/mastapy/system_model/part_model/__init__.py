"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model._2497 import Assembly
    from mastapy._private.system_model.part_model._2498 import AbstractAssembly
    from mastapy._private.system_model.part_model._2499 import AbstractShaft
    from mastapy._private.system_model.part_model._2500 import AbstractShaftOrHousing
    from mastapy._private.system_model.part_model._2501 import (
        AGMALoadSharingTableApplicationLevel,
    )
    from mastapy._private.system_model.part_model._2502 import (
        AxialInternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2503 import Bearing
    from mastapy._private.system_model.part_model._2504 import BearingF0InputMethod
    from mastapy._private.system_model.part_model._2505 import (
        BearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2506 import Bolt
    from mastapy._private.system_model.part_model._2507 import BoltedJoint
    from mastapy._private.system_model.part_model._2508 import Component
    from mastapy._private.system_model.part_model._2509 import ComponentsConnectedResult
    from mastapy._private.system_model.part_model._2510 import ConnectedSockets
    from mastapy._private.system_model.part_model._2511 import Connector
    from mastapy._private.system_model.part_model._2512 import Datum
    from mastapy._private.system_model.part_model._2513 import (
        ElectricMachineSearchRegionSpecificationMethod,
    )
    from mastapy._private.system_model.part_model._2514 import EnginePartLoad
    from mastapy._private.system_model.part_model._2515 import EngineSpeed
    from mastapy._private.system_model.part_model._2516 import ExternalCADModel
    from mastapy._private.system_model.part_model._2517 import FEPart
    from mastapy._private.system_model.part_model._2518 import FlexiblePinAssembly
    from mastapy._private.system_model.part_model._2519 import GuideDxfModel
    from mastapy._private.system_model.part_model._2520 import GuideImage
    from mastapy._private.system_model.part_model._2521 import GuideModelUsage
    from mastapy._private.system_model.part_model._2522 import (
        InnerBearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2523 import (
        InternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2524 import LoadSharingModes
    from mastapy._private.system_model.part_model._2525 import LoadSharingSettings
    from mastapy._private.system_model.part_model._2526 import MassDisc
    from mastapy._private.system_model.part_model._2527 import MeasurementComponent
    from mastapy._private.system_model.part_model._2528 import Microphone
    from mastapy._private.system_model.part_model._2529 import MicrophoneArray
    from mastapy._private.system_model.part_model._2530 import MountableComponent
    from mastapy._private.system_model.part_model._2531 import OilLevelSpecification
    from mastapy._private.system_model.part_model._2532 import OilSeal
    from mastapy._private.system_model.part_model._2533 import (
        OuterBearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2534 import Part
    from mastapy._private.system_model.part_model._2535 import PlanetCarrier
    from mastapy._private.system_model.part_model._2536 import PlanetCarrierSettings
    from mastapy._private.system_model.part_model._2537 import PointLoad
    from mastapy._private.system_model.part_model._2538 import PowerLoad
    from mastapy._private.system_model.part_model._2539 import (
        RadialInternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2540 import (
        RollingBearingElementLoadCase,
    )
    from mastapy._private.system_model.part_model._2541 import RootAssembly
    from mastapy._private.system_model.part_model._2542 import (
        ShaftDiameterModificationDueToRollingBearingRing,
    )
    from mastapy._private.system_model.part_model._2543 import SpecialisedAssembly
    from mastapy._private.system_model.part_model._2544 import UnbalancedMass
    from mastapy._private.system_model.part_model._2545 import (
        UnbalancedMassInclusionOption,
    )
    from mastapy._private.system_model.part_model._2546 import VirtualComponent
    from mastapy._private.system_model.part_model._2547 import (
        WindTurbineBladeModeDetails,
    )
    from mastapy._private.system_model.part_model._2548 import (
        WindTurbineSingleBladeDetails,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model._2497": ["Assembly"],
        "_private.system_model.part_model._2498": ["AbstractAssembly"],
        "_private.system_model.part_model._2499": ["AbstractShaft"],
        "_private.system_model.part_model._2500": ["AbstractShaftOrHousing"],
        "_private.system_model.part_model._2501": [
            "AGMALoadSharingTableApplicationLevel"
        ],
        "_private.system_model.part_model._2502": ["AxialInternalClearanceTolerance"],
        "_private.system_model.part_model._2503": ["Bearing"],
        "_private.system_model.part_model._2504": ["BearingF0InputMethod"],
        "_private.system_model.part_model._2505": ["BearingRaceMountingOptions"],
        "_private.system_model.part_model._2506": ["Bolt"],
        "_private.system_model.part_model._2507": ["BoltedJoint"],
        "_private.system_model.part_model._2508": ["Component"],
        "_private.system_model.part_model._2509": ["ComponentsConnectedResult"],
        "_private.system_model.part_model._2510": ["ConnectedSockets"],
        "_private.system_model.part_model._2511": ["Connector"],
        "_private.system_model.part_model._2512": ["Datum"],
        "_private.system_model.part_model._2513": [
            "ElectricMachineSearchRegionSpecificationMethod"
        ],
        "_private.system_model.part_model._2514": ["EnginePartLoad"],
        "_private.system_model.part_model._2515": ["EngineSpeed"],
        "_private.system_model.part_model._2516": ["ExternalCADModel"],
        "_private.system_model.part_model._2517": ["FEPart"],
        "_private.system_model.part_model._2518": ["FlexiblePinAssembly"],
        "_private.system_model.part_model._2519": ["GuideDxfModel"],
        "_private.system_model.part_model._2520": ["GuideImage"],
        "_private.system_model.part_model._2521": ["GuideModelUsage"],
        "_private.system_model.part_model._2522": ["InnerBearingRaceMountingOptions"],
        "_private.system_model.part_model._2523": ["InternalClearanceTolerance"],
        "_private.system_model.part_model._2524": ["LoadSharingModes"],
        "_private.system_model.part_model._2525": ["LoadSharingSettings"],
        "_private.system_model.part_model._2526": ["MassDisc"],
        "_private.system_model.part_model._2527": ["MeasurementComponent"],
        "_private.system_model.part_model._2528": ["Microphone"],
        "_private.system_model.part_model._2529": ["MicrophoneArray"],
        "_private.system_model.part_model._2530": ["MountableComponent"],
        "_private.system_model.part_model._2531": ["OilLevelSpecification"],
        "_private.system_model.part_model._2532": ["OilSeal"],
        "_private.system_model.part_model._2533": ["OuterBearingRaceMountingOptions"],
        "_private.system_model.part_model._2534": ["Part"],
        "_private.system_model.part_model._2535": ["PlanetCarrier"],
        "_private.system_model.part_model._2536": ["PlanetCarrierSettings"],
        "_private.system_model.part_model._2537": ["PointLoad"],
        "_private.system_model.part_model._2538": ["PowerLoad"],
        "_private.system_model.part_model._2539": ["RadialInternalClearanceTolerance"],
        "_private.system_model.part_model._2540": ["RollingBearingElementLoadCase"],
        "_private.system_model.part_model._2541": ["RootAssembly"],
        "_private.system_model.part_model._2542": [
            "ShaftDiameterModificationDueToRollingBearingRing"
        ],
        "_private.system_model.part_model._2543": ["SpecialisedAssembly"],
        "_private.system_model.part_model._2544": ["UnbalancedMass"],
        "_private.system_model.part_model._2545": ["UnbalancedMassInclusionOption"],
        "_private.system_model.part_model._2546": ["VirtualComponent"],
        "_private.system_model.part_model._2547": ["WindTurbineBladeModeDetails"],
        "_private.system_model.part_model._2548": ["WindTurbineSingleBladeDetails"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Assembly",
    "AbstractAssembly",
    "AbstractShaft",
    "AbstractShaftOrHousing",
    "AGMALoadSharingTableApplicationLevel",
    "AxialInternalClearanceTolerance",
    "Bearing",
    "BearingF0InputMethod",
    "BearingRaceMountingOptions",
    "Bolt",
    "BoltedJoint",
    "Component",
    "ComponentsConnectedResult",
    "ConnectedSockets",
    "Connector",
    "Datum",
    "ElectricMachineSearchRegionSpecificationMethod",
    "EnginePartLoad",
    "EngineSpeed",
    "ExternalCADModel",
    "FEPart",
    "FlexiblePinAssembly",
    "GuideDxfModel",
    "GuideImage",
    "GuideModelUsage",
    "InnerBearingRaceMountingOptions",
    "InternalClearanceTolerance",
    "LoadSharingModes",
    "LoadSharingSettings",
    "MassDisc",
    "MeasurementComponent",
    "Microphone",
    "MicrophoneArray",
    "MountableComponent",
    "OilLevelSpecification",
    "OilSeal",
    "OuterBearingRaceMountingOptions",
    "Part",
    "PlanetCarrier",
    "PlanetCarrierSettings",
    "PointLoad",
    "PowerLoad",
    "RadialInternalClearanceTolerance",
    "RollingBearingElementLoadCase",
    "RootAssembly",
    "ShaftDiameterModificationDueToRollingBearingRing",
    "SpecialisedAssembly",
    "UnbalancedMass",
    "UnbalancedMassInclusionOption",
    "VirtualComponent",
    "WindTurbineBladeModeDetails",
    "WindTurbineSingleBladeDetails",
)
