"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.conical._1198 import ActiveConicalFlank
    from mastapy._private.gears.gear_designs.conical._1199 import (
        BacklashDistributionRule,
    )
    from mastapy._private.gears.gear_designs.conical._1200 import ConicalFlanks
    from mastapy._private.gears.gear_designs.conical._1201 import ConicalGearCutter
    from mastapy._private.gears.gear_designs.conical._1202 import ConicalGearDesign
    from mastapy._private.gears.gear_designs.conical._1203 import ConicalGearMeshDesign
    from mastapy._private.gears.gear_designs.conical._1204 import ConicalGearSetDesign
    from mastapy._private.gears.gear_designs.conical._1205 import (
        ConicalMachineSettingCalculationMethods,
    )
    from mastapy._private.gears.gear_designs.conical._1206 import (
        ConicalManufactureMethods,
    )
    from mastapy._private.gears.gear_designs.conical._1207 import (
        ConicalMeshedGearDesign,
    )
    from mastapy._private.gears.gear_designs.conical._1208 import (
        ConicalMeshMisalignments,
    )
    from mastapy._private.gears.gear_designs.conical._1209 import CutterBladeType
    from mastapy._private.gears.gear_designs.conical._1210 import CutterGaugeLengths
    from mastapy._private.gears.gear_designs.conical._1211 import DummyConicalGearCutter
    from mastapy._private.gears.gear_designs.conical._1212 import FrontEndTypes
    from mastapy._private.gears.gear_designs.conical._1213 import (
        GleasonSafetyRequirements,
    )
    from mastapy._private.gears.gear_designs.conical._1214 import (
        KIMoSBevelHypoidSingleLoadCaseResultsData,
    )
    from mastapy._private.gears.gear_designs.conical._1215 import (
        KIMoSBevelHypoidSingleRotationAngleResult,
    )
    from mastapy._private.gears.gear_designs.conical._1216 import (
        KlingelnbergFinishingMethods,
    )
    from mastapy._private.gears.gear_designs.conical._1217 import (
        LoadDistributionFactorMethods,
    )
    from mastapy._private.gears.gear_designs.conical._1218 import TopremEntryType
    from mastapy._private.gears.gear_designs.conical._1219 import TopremLetter
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.conical._1198": ["ActiveConicalFlank"],
        "_private.gears.gear_designs.conical._1199": ["BacklashDistributionRule"],
        "_private.gears.gear_designs.conical._1200": ["ConicalFlanks"],
        "_private.gears.gear_designs.conical._1201": ["ConicalGearCutter"],
        "_private.gears.gear_designs.conical._1202": ["ConicalGearDesign"],
        "_private.gears.gear_designs.conical._1203": ["ConicalGearMeshDesign"],
        "_private.gears.gear_designs.conical._1204": ["ConicalGearSetDesign"],
        "_private.gears.gear_designs.conical._1205": [
            "ConicalMachineSettingCalculationMethods"
        ],
        "_private.gears.gear_designs.conical._1206": ["ConicalManufactureMethods"],
        "_private.gears.gear_designs.conical._1207": ["ConicalMeshedGearDesign"],
        "_private.gears.gear_designs.conical._1208": ["ConicalMeshMisalignments"],
        "_private.gears.gear_designs.conical._1209": ["CutterBladeType"],
        "_private.gears.gear_designs.conical._1210": ["CutterGaugeLengths"],
        "_private.gears.gear_designs.conical._1211": ["DummyConicalGearCutter"],
        "_private.gears.gear_designs.conical._1212": ["FrontEndTypes"],
        "_private.gears.gear_designs.conical._1213": ["GleasonSafetyRequirements"],
        "_private.gears.gear_designs.conical._1214": [
            "KIMoSBevelHypoidSingleLoadCaseResultsData"
        ],
        "_private.gears.gear_designs.conical._1215": [
            "KIMoSBevelHypoidSingleRotationAngleResult"
        ],
        "_private.gears.gear_designs.conical._1216": ["KlingelnbergFinishingMethods"],
        "_private.gears.gear_designs.conical._1217": ["LoadDistributionFactorMethods"],
        "_private.gears.gear_designs.conical._1218": ["TopremEntryType"],
        "_private.gears.gear_designs.conical._1219": ["TopremLetter"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ActiveConicalFlank",
    "BacklashDistributionRule",
    "ConicalFlanks",
    "ConicalGearCutter",
    "ConicalGearDesign",
    "ConicalGearMeshDesign",
    "ConicalGearSetDesign",
    "ConicalMachineSettingCalculationMethods",
    "ConicalManufactureMethods",
    "ConicalMeshedGearDesign",
    "ConicalMeshMisalignments",
    "CutterBladeType",
    "CutterGaugeLengths",
    "DummyConicalGearCutter",
    "FrontEndTypes",
    "GleasonSafetyRequirements",
    "KIMoSBevelHypoidSingleLoadCaseResultsData",
    "KIMoSBevelHypoidSingleRotationAngleResult",
    "KlingelnbergFinishingMethods",
    "LoadDistributionFactorMethods",
    "TopremEntryType",
    "TopremLetter",
)
