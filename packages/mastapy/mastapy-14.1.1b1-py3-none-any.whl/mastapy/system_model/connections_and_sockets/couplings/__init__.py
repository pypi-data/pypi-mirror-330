"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets.couplings._2405 import (
        ClutchConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2406 import (
        ClutchSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2407 import (
        ConceptCouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2408 import (
        ConceptCouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2409 import (
        CouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2410 import (
        CouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2411 import (
        PartToPartShearCouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2412 import (
        PartToPartShearCouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2413 import (
        SpringDamperConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2414 import (
        SpringDamperSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2415 import (
        TorqueConverterConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2416 import (
        TorqueConverterPumpSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2417 import (
        TorqueConverterTurbineSocket,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets.couplings._2405": [
            "ClutchConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2406": [
            "ClutchSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2407": [
            "ConceptCouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2408": [
            "ConceptCouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2409": [
            "CouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2410": [
            "CouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2411": [
            "PartToPartShearCouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2412": [
            "PartToPartShearCouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2413": [
            "SpringDamperConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2414": [
            "SpringDamperSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2415": [
            "TorqueConverterConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2416": [
            "TorqueConverterPumpSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2417": [
            "TorqueConverterTurbineSocket"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ClutchConnection",
    "ClutchSocket",
    "ConceptCouplingConnection",
    "ConceptCouplingSocket",
    "CouplingConnection",
    "CouplingSocket",
    "PartToPartShearCouplingConnection",
    "PartToPartShearCouplingSocket",
    "SpringDamperConnection",
    "SpringDamperSocket",
    "TorqueConverterConnection",
    "TorqueConverterPumpSocket",
    "TorqueConverterTurbineSocket",
)
