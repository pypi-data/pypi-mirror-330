"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.import_from_cad._2560 import (
        AbstractShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2561 import (
        ClutchFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2562 import (
        ComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2563 import (
        ComponentFromCADBase,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2564 import (
        ConceptBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2565 import (
        ConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2566 import (
        CylindricalGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2567 import (
        CylindricalGearInPlanetarySetFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2568 import (
        CylindricalPlanetGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2569 import (
        CylindricalRingGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2570 import (
        CylindricalSunGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2571 import (
        HousedOrMounted,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2572 import (
        MountableComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2573 import (
        PlanetShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2574 import (
        PulleyFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2575 import (
        RigidConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2576 import (
        RollingBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2577 import (
        ShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2578 import (
        ShaftFromCADAuto,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.import_from_cad._2560": [
            "AbstractShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2561": ["ClutchFromCAD"],
        "_private.system_model.part_model.import_from_cad._2562": ["ComponentFromCAD"],
        "_private.system_model.part_model.import_from_cad._2563": [
            "ComponentFromCADBase"
        ],
        "_private.system_model.part_model.import_from_cad._2564": [
            "ConceptBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2565": ["ConnectorFromCAD"],
        "_private.system_model.part_model.import_from_cad._2566": [
            "CylindricalGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2567": [
            "CylindricalGearInPlanetarySetFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2568": [
            "CylindricalPlanetGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2569": [
            "CylindricalRingGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2570": [
            "CylindricalSunGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2571": ["HousedOrMounted"],
        "_private.system_model.part_model.import_from_cad._2572": [
            "MountableComponentFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2573": [
            "PlanetShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2574": ["PulleyFromCAD"],
        "_private.system_model.part_model.import_from_cad._2575": [
            "RigidConnectorFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2576": [
            "RollingBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2577": ["ShaftFromCAD"],
        "_private.system_model.part_model.import_from_cad._2578": ["ShaftFromCADAuto"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftFromCAD",
    "ClutchFromCAD",
    "ComponentFromCAD",
    "ComponentFromCADBase",
    "ConceptBearingFromCAD",
    "ConnectorFromCAD",
    "CylindricalGearFromCAD",
    "CylindricalGearInPlanetarySetFromCAD",
    "CylindricalPlanetGearFromCAD",
    "CylindricalRingGearFromCAD",
    "CylindricalSunGearFromCAD",
    "HousedOrMounted",
    "MountableComponentFromCAD",
    "PlanetShaftFromCAD",
    "PulleyFromCAD",
    "RigidConnectorFromCAD",
    "RollingBearingFromCAD",
    "ShaftFromCAD",
    "ShaftFromCADAuto",
)
