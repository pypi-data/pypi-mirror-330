"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe.links._2482 import FELink
    from mastapy._private.system_model.fe.links._2483 import ElectricMachineStatorFELink
    from mastapy._private.system_model.fe.links._2484 import FELinkWithSelection
    from mastapy._private.system_model.fe.links._2485 import GearMeshFELink
    from mastapy._private.system_model.fe.links._2486 import (
        GearWithDuplicatedMeshesFELink,
    )
    from mastapy._private.system_model.fe.links._2487 import MultiAngleConnectionFELink
    from mastapy._private.system_model.fe.links._2488 import MultiNodeConnectorFELink
    from mastapy._private.system_model.fe.links._2489 import MultiNodeFELink
    from mastapy._private.system_model.fe.links._2490 import (
        PlanetaryConnectorMultiNodeFELink,
    )
    from mastapy._private.system_model.fe.links._2491 import PlanetBasedFELink
    from mastapy._private.system_model.fe.links._2492 import PlanetCarrierFELink
    from mastapy._private.system_model.fe.links._2493 import PointLoadFELink
    from mastapy._private.system_model.fe.links._2494 import RollingRingConnectionFELink
    from mastapy._private.system_model.fe.links._2495 import ShaftHubConnectionFELink
    from mastapy._private.system_model.fe.links._2496 import SingleNodeFELink
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe.links._2482": ["FELink"],
        "_private.system_model.fe.links._2483": ["ElectricMachineStatorFELink"],
        "_private.system_model.fe.links._2484": ["FELinkWithSelection"],
        "_private.system_model.fe.links._2485": ["GearMeshFELink"],
        "_private.system_model.fe.links._2486": ["GearWithDuplicatedMeshesFELink"],
        "_private.system_model.fe.links._2487": ["MultiAngleConnectionFELink"],
        "_private.system_model.fe.links._2488": ["MultiNodeConnectorFELink"],
        "_private.system_model.fe.links._2489": ["MultiNodeFELink"],
        "_private.system_model.fe.links._2490": ["PlanetaryConnectorMultiNodeFELink"],
        "_private.system_model.fe.links._2491": ["PlanetBasedFELink"],
        "_private.system_model.fe.links._2492": ["PlanetCarrierFELink"],
        "_private.system_model.fe.links._2493": ["PointLoadFELink"],
        "_private.system_model.fe.links._2494": ["RollingRingConnectionFELink"],
        "_private.system_model.fe.links._2495": ["ShaftHubConnectionFELink"],
        "_private.system_model.fe.links._2496": ["SingleNodeFELink"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FELink",
    "ElectricMachineStatorFELink",
    "FELinkWithSelection",
    "GearMeshFELink",
    "GearWithDuplicatedMeshesFELink",
    "MultiAngleConnectionFELink",
    "MultiNodeConnectorFELink",
    "MultiNodeFELink",
    "PlanetaryConnectorMultiNodeFELink",
    "PlanetBasedFELink",
    "PlanetCarrierFELink",
    "PointLoadFELink",
    "RollingRingConnectionFELink",
    "ShaftHubConnectionFELink",
    "SingleNodeFELink",
)
