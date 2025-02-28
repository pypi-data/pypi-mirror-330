"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets._2328 import (
        AbstractShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2329 import (
        BearingInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2330 import (
        BearingOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2331 import (
        BeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2332 import (
        CoaxialConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2333 import (
        ComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2334 import (
        ComponentMeasurer,
    )
    from mastapy._private.system_model.connections_and_sockets._2335 import Connection
    from mastapy._private.system_model.connections_and_sockets._2336 import (
        CVTBeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2337 import (
        CVTPulleySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2338 import (
        CylindricalComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2339 import (
        CylindricalSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2340 import (
        DatumMeasurement,
    )
    from mastapy._private.system_model.connections_and_sockets._2341 import (
        ElectricMachineStatorSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2342 import (
        InnerShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2343 import (
        InnerShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2344 import (
        InterMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2345 import (
        MountableComponentInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2346 import (
        MountableComponentOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2347 import (
        MountableComponentSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2348 import (
        OuterShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2349 import (
        OuterShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2350 import (
        PlanetaryConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2351 import (
        PlanetarySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2352 import (
        PlanetarySocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2353 import PulleySocket
    from mastapy._private.system_model.connections_and_sockets._2354 import (
        RealignmentResult,
    )
    from mastapy._private.system_model.connections_and_sockets._2355 import (
        RollingRingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2356 import (
        RollingRingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2357 import ShaftSocket
    from mastapy._private.system_model.connections_and_sockets._2358 import (
        ShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2359 import Socket
    from mastapy._private.system_model.connections_and_sockets._2360 import (
        SocketConnectionOptions,
    )
    from mastapy._private.system_model.connections_and_sockets._2361 import (
        SocketConnectionSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets._2328": [
            "AbstractShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2329": ["BearingInnerSocket"],
        "_private.system_model.connections_and_sockets._2330": ["BearingOuterSocket"],
        "_private.system_model.connections_and_sockets._2331": ["BeltConnection"],
        "_private.system_model.connections_and_sockets._2332": ["CoaxialConnection"],
        "_private.system_model.connections_and_sockets._2333": ["ComponentConnection"],
        "_private.system_model.connections_and_sockets._2334": ["ComponentMeasurer"],
        "_private.system_model.connections_and_sockets._2335": ["Connection"],
        "_private.system_model.connections_and_sockets._2336": ["CVTBeltConnection"],
        "_private.system_model.connections_and_sockets._2337": ["CVTPulleySocket"],
        "_private.system_model.connections_and_sockets._2338": [
            "CylindricalComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2339": ["CylindricalSocket"],
        "_private.system_model.connections_and_sockets._2340": ["DatumMeasurement"],
        "_private.system_model.connections_and_sockets._2341": [
            "ElectricMachineStatorSocket"
        ],
        "_private.system_model.connections_and_sockets._2342": ["InnerShaftSocket"],
        "_private.system_model.connections_and_sockets._2343": ["InnerShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2344": [
            "InterMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2345": [
            "MountableComponentInnerSocket"
        ],
        "_private.system_model.connections_and_sockets._2346": [
            "MountableComponentOuterSocket"
        ],
        "_private.system_model.connections_and_sockets._2347": [
            "MountableComponentSocket"
        ],
        "_private.system_model.connections_and_sockets._2348": ["OuterShaftSocket"],
        "_private.system_model.connections_and_sockets._2349": ["OuterShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2350": ["PlanetaryConnection"],
        "_private.system_model.connections_and_sockets._2351": ["PlanetarySocket"],
        "_private.system_model.connections_and_sockets._2352": ["PlanetarySocketBase"],
        "_private.system_model.connections_and_sockets._2353": ["PulleySocket"],
        "_private.system_model.connections_and_sockets._2354": ["RealignmentResult"],
        "_private.system_model.connections_and_sockets._2355": [
            "RollingRingConnection"
        ],
        "_private.system_model.connections_and_sockets._2356": ["RollingRingSocket"],
        "_private.system_model.connections_and_sockets._2357": ["ShaftSocket"],
        "_private.system_model.connections_and_sockets._2358": [
            "ShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2359": ["Socket"],
        "_private.system_model.connections_and_sockets._2360": [
            "SocketConnectionOptions"
        ],
        "_private.system_model.connections_and_sockets._2361": [
            "SocketConnectionSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftToMountableComponentConnection",
    "BearingInnerSocket",
    "BearingOuterSocket",
    "BeltConnection",
    "CoaxialConnection",
    "ComponentConnection",
    "ComponentMeasurer",
    "Connection",
    "CVTBeltConnection",
    "CVTPulleySocket",
    "CylindricalComponentConnection",
    "CylindricalSocket",
    "DatumMeasurement",
    "ElectricMachineStatorSocket",
    "InnerShaftSocket",
    "InnerShaftSocketBase",
    "InterMountableComponentConnection",
    "MountableComponentInnerSocket",
    "MountableComponentOuterSocket",
    "MountableComponentSocket",
    "OuterShaftSocket",
    "OuterShaftSocketBase",
    "PlanetaryConnection",
    "PlanetarySocket",
    "PlanetarySocketBase",
    "PulleySocket",
    "RealignmentResult",
    "RollingRingConnection",
    "RollingRingSocket",
    "ShaftSocket",
    "ShaftToMountableComponentConnection",
    "Socket",
    "SocketConnectionOptions",
    "SocketConnectionSelection",
)
