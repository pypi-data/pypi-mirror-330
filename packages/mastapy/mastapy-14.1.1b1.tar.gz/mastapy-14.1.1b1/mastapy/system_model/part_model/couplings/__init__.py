"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.couplings._2646 import BeltDrive
    from mastapy._private.system_model.part_model.couplings._2647 import BeltDriveType
    from mastapy._private.system_model.part_model.couplings._2648 import Clutch
    from mastapy._private.system_model.part_model.couplings._2649 import ClutchHalf
    from mastapy._private.system_model.part_model.couplings._2650 import ClutchType
    from mastapy._private.system_model.part_model.couplings._2651 import ConceptCoupling
    from mastapy._private.system_model.part_model.couplings._2652 import (
        ConceptCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2653 import (
        ConceptCouplingHalfPositioning,
    )
    from mastapy._private.system_model.part_model.couplings._2654 import Coupling
    from mastapy._private.system_model.part_model.couplings._2655 import CouplingHalf
    from mastapy._private.system_model.part_model.couplings._2656 import (
        CrowningSpecification,
    )
    from mastapy._private.system_model.part_model.couplings._2657 import CVT
    from mastapy._private.system_model.part_model.couplings._2658 import CVTPulley
    from mastapy._private.system_model.part_model.couplings._2659 import (
        PartToPartShearCoupling,
    )
    from mastapy._private.system_model.part_model.couplings._2660 import (
        PartToPartShearCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2661 import (
        PitchErrorFlankOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2662 import Pulley
    from mastapy._private.system_model.part_model.couplings._2663 import (
        RigidConnectorSettings,
    )
    from mastapy._private.system_model.part_model.couplings._2664 import (
        RigidConnectorStiffnessType,
    )
    from mastapy._private.system_model.part_model.couplings._2665 import (
        RigidConnectorTiltStiffnessTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2666 import (
        RigidConnectorToothLocation,
    )
    from mastapy._private.system_model.part_model.couplings._2667 import (
        RigidConnectorToothSpacingType,
    )
    from mastapy._private.system_model.part_model.couplings._2668 import (
        RigidConnectorTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2669 import RollingRing
    from mastapy._private.system_model.part_model.couplings._2670 import (
        RollingRingAssembly,
    )
    from mastapy._private.system_model.part_model.couplings._2671 import (
        ShaftHubConnection,
    )
    from mastapy._private.system_model.part_model.couplings._2672 import (
        SplineFitOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2673 import (
        SplineHalfManufacturingError,
    )
    from mastapy._private.system_model.part_model.couplings._2674 import (
        SplineLeadRelief,
    )
    from mastapy._private.system_model.part_model.couplings._2675 import (
        SplinePitchErrorInputType,
    )
    from mastapy._private.system_model.part_model.couplings._2676 import (
        SplinePitchErrorOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2677 import SpringDamper
    from mastapy._private.system_model.part_model.couplings._2678 import (
        SpringDamperHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2679 import Synchroniser
    from mastapy._private.system_model.part_model.couplings._2680 import (
        SynchroniserCone,
    )
    from mastapy._private.system_model.part_model.couplings._2681 import (
        SynchroniserHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2682 import (
        SynchroniserPart,
    )
    from mastapy._private.system_model.part_model.couplings._2683 import (
        SynchroniserSleeve,
    )
    from mastapy._private.system_model.part_model.couplings._2684 import TorqueConverter
    from mastapy._private.system_model.part_model.couplings._2685 import (
        TorqueConverterPump,
    )
    from mastapy._private.system_model.part_model.couplings._2686 import (
        TorqueConverterSpeedRatio,
    )
    from mastapy._private.system_model.part_model.couplings._2687 import (
        TorqueConverterTurbine,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.couplings._2646": ["BeltDrive"],
        "_private.system_model.part_model.couplings._2647": ["BeltDriveType"],
        "_private.system_model.part_model.couplings._2648": ["Clutch"],
        "_private.system_model.part_model.couplings._2649": ["ClutchHalf"],
        "_private.system_model.part_model.couplings._2650": ["ClutchType"],
        "_private.system_model.part_model.couplings._2651": ["ConceptCoupling"],
        "_private.system_model.part_model.couplings._2652": ["ConceptCouplingHalf"],
        "_private.system_model.part_model.couplings._2653": [
            "ConceptCouplingHalfPositioning"
        ],
        "_private.system_model.part_model.couplings._2654": ["Coupling"],
        "_private.system_model.part_model.couplings._2655": ["CouplingHalf"],
        "_private.system_model.part_model.couplings._2656": ["CrowningSpecification"],
        "_private.system_model.part_model.couplings._2657": ["CVT"],
        "_private.system_model.part_model.couplings._2658": ["CVTPulley"],
        "_private.system_model.part_model.couplings._2659": ["PartToPartShearCoupling"],
        "_private.system_model.part_model.couplings._2660": [
            "PartToPartShearCouplingHalf"
        ],
        "_private.system_model.part_model.couplings._2661": ["PitchErrorFlankOptions"],
        "_private.system_model.part_model.couplings._2662": ["Pulley"],
        "_private.system_model.part_model.couplings._2663": ["RigidConnectorSettings"],
        "_private.system_model.part_model.couplings._2664": [
            "RigidConnectorStiffnessType"
        ],
        "_private.system_model.part_model.couplings._2665": [
            "RigidConnectorTiltStiffnessTypes"
        ],
        "_private.system_model.part_model.couplings._2666": [
            "RigidConnectorToothLocation"
        ],
        "_private.system_model.part_model.couplings._2667": [
            "RigidConnectorToothSpacingType"
        ],
        "_private.system_model.part_model.couplings._2668": ["RigidConnectorTypes"],
        "_private.system_model.part_model.couplings._2669": ["RollingRing"],
        "_private.system_model.part_model.couplings._2670": ["RollingRingAssembly"],
        "_private.system_model.part_model.couplings._2671": ["ShaftHubConnection"],
        "_private.system_model.part_model.couplings._2672": ["SplineFitOptions"],
        "_private.system_model.part_model.couplings._2673": [
            "SplineHalfManufacturingError"
        ],
        "_private.system_model.part_model.couplings._2674": ["SplineLeadRelief"],
        "_private.system_model.part_model.couplings._2675": [
            "SplinePitchErrorInputType"
        ],
        "_private.system_model.part_model.couplings._2676": ["SplinePitchErrorOptions"],
        "_private.system_model.part_model.couplings._2677": ["SpringDamper"],
        "_private.system_model.part_model.couplings._2678": ["SpringDamperHalf"],
        "_private.system_model.part_model.couplings._2679": ["Synchroniser"],
        "_private.system_model.part_model.couplings._2680": ["SynchroniserCone"],
        "_private.system_model.part_model.couplings._2681": ["SynchroniserHalf"],
        "_private.system_model.part_model.couplings._2682": ["SynchroniserPart"],
        "_private.system_model.part_model.couplings._2683": ["SynchroniserSleeve"],
        "_private.system_model.part_model.couplings._2684": ["TorqueConverter"],
        "_private.system_model.part_model.couplings._2685": ["TorqueConverterPump"],
        "_private.system_model.part_model.couplings._2686": [
            "TorqueConverterSpeedRatio"
        ],
        "_private.system_model.part_model.couplings._2687": ["TorqueConverterTurbine"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BeltDrive",
    "BeltDriveType",
    "Clutch",
    "ClutchHalf",
    "ClutchType",
    "ConceptCoupling",
    "ConceptCouplingHalf",
    "ConceptCouplingHalfPositioning",
    "Coupling",
    "CouplingHalf",
    "CrowningSpecification",
    "CVT",
    "CVTPulley",
    "PartToPartShearCoupling",
    "PartToPartShearCouplingHalf",
    "PitchErrorFlankOptions",
    "Pulley",
    "RigidConnectorSettings",
    "RigidConnectorStiffnessType",
    "RigidConnectorTiltStiffnessTypes",
    "RigidConnectorToothLocation",
    "RigidConnectorToothSpacingType",
    "RigidConnectorTypes",
    "RollingRing",
    "RollingRingAssembly",
    "ShaftHubConnection",
    "SplineFitOptions",
    "SplineHalfManufacturingError",
    "SplineLeadRelief",
    "SplinePitchErrorInputType",
    "SplinePitchErrorOptions",
    "SpringDamper",
    "SpringDamperHalf",
    "Synchroniser",
    "SynchroniserCone",
    "SynchroniserHalf",
    "SynchroniserPart",
    "SynchroniserSleeve",
    "TorqueConverter",
    "TorqueConverterPump",
    "TorqueConverterSpeedRatio",
    "TorqueConverterTurbine",
)
