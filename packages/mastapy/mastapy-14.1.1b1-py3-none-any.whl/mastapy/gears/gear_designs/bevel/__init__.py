"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.bevel._1227 import (
        AGMAGleasonConicalGearGeometryMethods,
    )
    from mastapy._private.gears.gear_designs.bevel._1228 import BevelGearDesign
    from mastapy._private.gears.gear_designs.bevel._1229 import BevelGearMeshDesign
    from mastapy._private.gears.gear_designs.bevel._1230 import BevelGearSetDesign
    from mastapy._private.gears.gear_designs.bevel._1231 import BevelMeshedGearDesign
    from mastapy._private.gears.gear_designs.bevel._1232 import (
        DrivenMachineCharacteristicGleason,
    )
    from mastapy._private.gears.gear_designs.bevel._1233 import EdgeRadiusType
    from mastapy._private.gears.gear_designs.bevel._1234 import FinishingMethods
    from mastapy._private.gears.gear_designs.bevel._1235 import (
        MachineCharacteristicAGMAKlingelnberg,
    )
    from mastapy._private.gears.gear_designs.bevel._1236 import (
        PrimeMoverCharacteristicGleason,
    )
    from mastapy._private.gears.gear_designs.bevel._1237 import (
        ToothProportionsInputMethod,
    )
    from mastapy._private.gears.gear_designs.bevel._1238 import (
        ToothThicknessSpecificationMethod,
    )
    from mastapy._private.gears.gear_designs.bevel._1239 import (
        WheelFinishCutterPointWidthRestrictionMethod,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.bevel._1227": [
            "AGMAGleasonConicalGearGeometryMethods"
        ],
        "_private.gears.gear_designs.bevel._1228": ["BevelGearDesign"],
        "_private.gears.gear_designs.bevel._1229": ["BevelGearMeshDesign"],
        "_private.gears.gear_designs.bevel._1230": ["BevelGearSetDesign"],
        "_private.gears.gear_designs.bevel._1231": ["BevelMeshedGearDesign"],
        "_private.gears.gear_designs.bevel._1232": [
            "DrivenMachineCharacteristicGleason"
        ],
        "_private.gears.gear_designs.bevel._1233": ["EdgeRadiusType"],
        "_private.gears.gear_designs.bevel._1234": ["FinishingMethods"],
        "_private.gears.gear_designs.bevel._1235": [
            "MachineCharacteristicAGMAKlingelnberg"
        ],
        "_private.gears.gear_designs.bevel._1236": ["PrimeMoverCharacteristicGleason"],
        "_private.gears.gear_designs.bevel._1237": ["ToothProportionsInputMethod"],
        "_private.gears.gear_designs.bevel._1238": [
            "ToothThicknessSpecificationMethod"
        ],
        "_private.gears.gear_designs.bevel._1239": [
            "WheelFinishCutterPointWidthRestrictionMethod"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMAGleasonConicalGearGeometryMethods",
    "BevelGearDesign",
    "BevelGearMeshDesign",
    "BevelGearSetDesign",
    "BevelMeshedGearDesign",
    "DrivenMachineCharacteristicGleason",
    "EdgeRadiusType",
    "FinishingMethods",
    "MachineCharacteristicAGMAKlingelnberg",
    "PrimeMoverCharacteristicGleason",
    "ToothProportionsInputMethod",
    "ToothThicknessSpecificationMethod",
    "WheelFinishCutterPointWidthRestrictionMethod",
)
