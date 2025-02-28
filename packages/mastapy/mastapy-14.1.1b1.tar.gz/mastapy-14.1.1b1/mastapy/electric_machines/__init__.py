"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines._1292 import AbstractStator
    from mastapy._private.electric_machines._1293 import AbstractToothAndSlot
    from mastapy._private.electric_machines._1294 import CADConductor
    from mastapy._private.electric_machines._1295 import CADElectricMachineDetail
    from mastapy._private.electric_machines._1296 import CADFieldWindingSpecification
    from mastapy._private.electric_machines._1297 import CADMagnetDetails
    from mastapy._private.electric_machines._1298 import CADMagnetsForLayer
    from mastapy._private.electric_machines._1299 import CADRotor
    from mastapy._private.electric_machines._1300 import CADStator
    from mastapy._private.electric_machines._1301 import CADToothAndSlot
    from mastapy._private.electric_machines._1302 import CADWoundFieldSynchronousRotor
    from mastapy._private.electric_machines._1303 import Coil
    from mastapy._private.electric_machines._1304 import CoilPositionInSlot
    from mastapy._private.electric_machines._1305 import CoolingDuctLayerSpecification
    from mastapy._private.electric_machines._1306 import CoolingDuctShape
    from mastapy._private.electric_machines._1307 import (
        CoreLossBuildFactorSpecificationMethod,
    )
    from mastapy._private.electric_machines._1308 import CoreLossCoefficients
    from mastapy._private.electric_machines._1309 import DoubleLayerWindingSlotPositions
    from mastapy._private.electric_machines._1310 import DQAxisConvention
    from mastapy._private.electric_machines._1311 import Eccentricity
    from mastapy._private.electric_machines._1312 import ElectricMachineDetail
    from mastapy._private.electric_machines._1313 import (
        ElectricMachineDetailInitialInformation,
    )
    from mastapy._private.electric_machines._1314 import ElectricMachineGroup
    from mastapy._private.electric_machines._1315 import (
        ElectricMachineMechanicalAnalysisMeshingOptions,
    )
    from mastapy._private.electric_machines._1316 import ElectricMachineMeshingOptions
    from mastapy._private.electric_machines._1317 import (
        ElectricMachineMeshingOptionsBase,
    )
    from mastapy._private.electric_machines._1318 import ElectricMachineSetup
    from mastapy._private.electric_machines._1319 import ElectricMachineType
    from mastapy._private.electric_machines._1320 import FieldWindingSpecification
    from mastapy._private.electric_machines._1321 import FieldWindingSpecificationBase
    from mastapy._private.electric_machines._1322 import FillFactorSpecificationMethod
    from mastapy._private.electric_machines._1323 import FluxBarriers
    from mastapy._private.electric_machines._1324 import FluxBarrierOrWeb
    from mastapy._private.electric_machines._1325 import FluxBarrierStyle
    from mastapy._private.electric_machines._1326 import HairpinConductor
    from mastapy._private.electric_machines._1327 import (
        HarmonicLoadDataControlExcitationOptionForElectricMachineMode,
    )
    from mastapy._private.electric_machines._1328 import (
        IndividualConductorSpecificationSource,
    )
    from mastapy._private.electric_machines._1329 import (
        InteriorPermanentMagnetAndSynchronousReluctanceRotor,
    )
    from mastapy._private.electric_machines._1330 import InteriorPermanentMagnetMachine
    from mastapy._private.electric_machines._1331 import (
        IronLossCoefficientSpecificationMethod,
    )
    from mastapy._private.electric_machines._1332 import MagnetClearance
    from mastapy._private.electric_machines._1333 import MagnetConfiguration
    from mastapy._private.electric_machines._1334 import MagnetData
    from mastapy._private.electric_machines._1335 import MagnetDesign
    from mastapy._private.electric_machines._1336 import MagnetForLayer
    from mastapy._private.electric_machines._1337 import MagnetisationDirection
    from mastapy._private.electric_machines._1338 import MagnetMaterial
    from mastapy._private.electric_machines._1339 import MagnetMaterialDatabase
    from mastapy._private.electric_machines._1340 import MotorRotorSideFaceDetail
    from mastapy._private.electric_machines._1341 import NonCADElectricMachineDetail
    from mastapy._private.electric_machines._1342 import NotchShape
    from mastapy._private.electric_machines._1343 import NotchSpecification
    from mastapy._private.electric_machines._1344 import (
        PermanentMagnetAssistedSynchronousReluctanceMachine,
    )
    from mastapy._private.electric_machines._1345 import PermanentMagnetRotor
    from mastapy._private.electric_machines._1346 import Phase
    from mastapy._private.electric_machines._1347 import RegionID
    from mastapy._private.electric_machines._1348 import Rotor
    from mastapy._private.electric_machines._1349 import RotorInternalLayerSpecification
    from mastapy._private.electric_machines._1350 import RotorSkewSlice
    from mastapy._private.electric_machines._1351 import RotorType
    from mastapy._private.electric_machines._1352 import SingleOrDoubleLayerWindings
    from mastapy._private.electric_machines._1353 import SlotSectionDetail
    from mastapy._private.electric_machines._1354 import Stator
    from mastapy._private.electric_machines._1355 import StatorCutoutSpecification
    from mastapy._private.electric_machines._1356 import StatorRotorMaterial
    from mastapy._private.electric_machines._1357 import StatorRotorMaterialDatabase
    from mastapy._private.electric_machines._1358 import SurfacePermanentMagnetMachine
    from mastapy._private.electric_machines._1359 import SurfacePermanentMagnetRotor
    from mastapy._private.electric_machines._1360 import SynchronousReluctanceMachine
    from mastapy._private.electric_machines._1361 import ToothAndSlot
    from mastapy._private.electric_machines._1362 import ToothSlotStyle
    from mastapy._private.electric_machines._1363 import ToothTaperSpecification
    from mastapy._private.electric_machines._1364 import (
        TwoDimensionalFEModelForAnalysis,
    )
    from mastapy._private.electric_machines._1365 import (
        TwoDimensionalFEModelForElectromagneticAnalysis,
    )
    from mastapy._private.electric_machines._1366 import (
        TwoDimensionalFEModelForMechanicalAnalysis,
    )
    from mastapy._private.electric_machines._1367 import UShapedLayerSpecification
    from mastapy._private.electric_machines._1368 import VShapedMagnetLayerSpecification
    from mastapy._private.electric_machines._1369 import WindingConductor
    from mastapy._private.electric_machines._1370 import WindingConnection
    from mastapy._private.electric_machines._1371 import WindingMaterial
    from mastapy._private.electric_machines._1372 import WindingMaterialDatabase
    from mastapy._private.electric_machines._1373 import Windings
    from mastapy._private.electric_machines._1374 import WindingsViewer
    from mastapy._private.electric_machines._1375 import WindingType
    from mastapy._private.electric_machines._1376 import WireSizeSpecificationMethod
    from mastapy._private.electric_machines._1377 import WoundFieldSynchronousMachine
    from mastapy._private.electric_machines._1378 import WoundFieldSynchronousRotor
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines._1292": ["AbstractStator"],
        "_private.electric_machines._1293": ["AbstractToothAndSlot"],
        "_private.electric_machines._1294": ["CADConductor"],
        "_private.electric_machines._1295": ["CADElectricMachineDetail"],
        "_private.electric_machines._1296": ["CADFieldWindingSpecification"],
        "_private.electric_machines._1297": ["CADMagnetDetails"],
        "_private.electric_machines._1298": ["CADMagnetsForLayer"],
        "_private.electric_machines._1299": ["CADRotor"],
        "_private.electric_machines._1300": ["CADStator"],
        "_private.electric_machines._1301": ["CADToothAndSlot"],
        "_private.electric_machines._1302": ["CADWoundFieldSynchronousRotor"],
        "_private.electric_machines._1303": ["Coil"],
        "_private.electric_machines._1304": ["CoilPositionInSlot"],
        "_private.electric_machines._1305": ["CoolingDuctLayerSpecification"],
        "_private.electric_machines._1306": ["CoolingDuctShape"],
        "_private.electric_machines._1307": ["CoreLossBuildFactorSpecificationMethod"],
        "_private.electric_machines._1308": ["CoreLossCoefficients"],
        "_private.electric_machines._1309": ["DoubleLayerWindingSlotPositions"],
        "_private.electric_machines._1310": ["DQAxisConvention"],
        "_private.electric_machines._1311": ["Eccentricity"],
        "_private.electric_machines._1312": ["ElectricMachineDetail"],
        "_private.electric_machines._1313": ["ElectricMachineDetailInitialInformation"],
        "_private.electric_machines._1314": ["ElectricMachineGroup"],
        "_private.electric_machines._1315": [
            "ElectricMachineMechanicalAnalysisMeshingOptions"
        ],
        "_private.electric_machines._1316": ["ElectricMachineMeshingOptions"],
        "_private.electric_machines._1317": ["ElectricMachineMeshingOptionsBase"],
        "_private.electric_machines._1318": ["ElectricMachineSetup"],
        "_private.electric_machines._1319": ["ElectricMachineType"],
        "_private.electric_machines._1320": ["FieldWindingSpecification"],
        "_private.electric_machines._1321": ["FieldWindingSpecificationBase"],
        "_private.electric_machines._1322": ["FillFactorSpecificationMethod"],
        "_private.electric_machines._1323": ["FluxBarriers"],
        "_private.electric_machines._1324": ["FluxBarrierOrWeb"],
        "_private.electric_machines._1325": ["FluxBarrierStyle"],
        "_private.electric_machines._1326": ["HairpinConductor"],
        "_private.electric_machines._1327": [
            "HarmonicLoadDataControlExcitationOptionForElectricMachineMode"
        ],
        "_private.electric_machines._1328": ["IndividualConductorSpecificationSource"],
        "_private.electric_machines._1329": [
            "InteriorPermanentMagnetAndSynchronousReluctanceRotor"
        ],
        "_private.electric_machines._1330": ["InteriorPermanentMagnetMachine"],
        "_private.electric_machines._1331": ["IronLossCoefficientSpecificationMethod"],
        "_private.electric_machines._1332": ["MagnetClearance"],
        "_private.electric_machines._1333": ["MagnetConfiguration"],
        "_private.electric_machines._1334": ["MagnetData"],
        "_private.electric_machines._1335": ["MagnetDesign"],
        "_private.electric_machines._1336": ["MagnetForLayer"],
        "_private.electric_machines._1337": ["MagnetisationDirection"],
        "_private.electric_machines._1338": ["MagnetMaterial"],
        "_private.electric_machines._1339": ["MagnetMaterialDatabase"],
        "_private.electric_machines._1340": ["MotorRotorSideFaceDetail"],
        "_private.electric_machines._1341": ["NonCADElectricMachineDetail"],
        "_private.electric_machines._1342": ["NotchShape"],
        "_private.electric_machines._1343": ["NotchSpecification"],
        "_private.electric_machines._1344": [
            "PermanentMagnetAssistedSynchronousReluctanceMachine"
        ],
        "_private.electric_machines._1345": ["PermanentMagnetRotor"],
        "_private.electric_machines._1346": ["Phase"],
        "_private.electric_machines._1347": ["RegionID"],
        "_private.electric_machines._1348": ["Rotor"],
        "_private.electric_machines._1349": ["RotorInternalLayerSpecification"],
        "_private.electric_machines._1350": ["RotorSkewSlice"],
        "_private.electric_machines._1351": ["RotorType"],
        "_private.electric_machines._1352": ["SingleOrDoubleLayerWindings"],
        "_private.electric_machines._1353": ["SlotSectionDetail"],
        "_private.electric_machines._1354": ["Stator"],
        "_private.electric_machines._1355": ["StatorCutoutSpecification"],
        "_private.electric_machines._1356": ["StatorRotorMaterial"],
        "_private.electric_machines._1357": ["StatorRotorMaterialDatabase"],
        "_private.electric_machines._1358": ["SurfacePermanentMagnetMachine"],
        "_private.electric_machines._1359": ["SurfacePermanentMagnetRotor"],
        "_private.electric_machines._1360": ["SynchronousReluctanceMachine"],
        "_private.electric_machines._1361": ["ToothAndSlot"],
        "_private.electric_machines._1362": ["ToothSlotStyle"],
        "_private.electric_machines._1363": ["ToothTaperSpecification"],
        "_private.electric_machines._1364": ["TwoDimensionalFEModelForAnalysis"],
        "_private.electric_machines._1365": [
            "TwoDimensionalFEModelForElectromagneticAnalysis"
        ],
        "_private.electric_machines._1366": [
            "TwoDimensionalFEModelForMechanicalAnalysis"
        ],
        "_private.electric_machines._1367": ["UShapedLayerSpecification"],
        "_private.electric_machines._1368": ["VShapedMagnetLayerSpecification"],
        "_private.electric_machines._1369": ["WindingConductor"],
        "_private.electric_machines._1370": ["WindingConnection"],
        "_private.electric_machines._1371": ["WindingMaterial"],
        "_private.electric_machines._1372": ["WindingMaterialDatabase"],
        "_private.electric_machines._1373": ["Windings"],
        "_private.electric_machines._1374": ["WindingsViewer"],
        "_private.electric_machines._1375": ["WindingType"],
        "_private.electric_machines._1376": ["WireSizeSpecificationMethod"],
        "_private.electric_machines._1377": ["WoundFieldSynchronousMachine"],
        "_private.electric_machines._1378": ["WoundFieldSynchronousRotor"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractStator",
    "AbstractToothAndSlot",
    "CADConductor",
    "CADElectricMachineDetail",
    "CADFieldWindingSpecification",
    "CADMagnetDetails",
    "CADMagnetsForLayer",
    "CADRotor",
    "CADStator",
    "CADToothAndSlot",
    "CADWoundFieldSynchronousRotor",
    "Coil",
    "CoilPositionInSlot",
    "CoolingDuctLayerSpecification",
    "CoolingDuctShape",
    "CoreLossBuildFactorSpecificationMethod",
    "CoreLossCoefficients",
    "DoubleLayerWindingSlotPositions",
    "DQAxisConvention",
    "Eccentricity",
    "ElectricMachineDetail",
    "ElectricMachineDetailInitialInformation",
    "ElectricMachineGroup",
    "ElectricMachineMechanicalAnalysisMeshingOptions",
    "ElectricMachineMeshingOptions",
    "ElectricMachineMeshingOptionsBase",
    "ElectricMachineSetup",
    "ElectricMachineType",
    "FieldWindingSpecification",
    "FieldWindingSpecificationBase",
    "FillFactorSpecificationMethod",
    "FluxBarriers",
    "FluxBarrierOrWeb",
    "FluxBarrierStyle",
    "HairpinConductor",
    "HarmonicLoadDataControlExcitationOptionForElectricMachineMode",
    "IndividualConductorSpecificationSource",
    "InteriorPermanentMagnetAndSynchronousReluctanceRotor",
    "InteriorPermanentMagnetMachine",
    "IronLossCoefficientSpecificationMethod",
    "MagnetClearance",
    "MagnetConfiguration",
    "MagnetData",
    "MagnetDesign",
    "MagnetForLayer",
    "MagnetisationDirection",
    "MagnetMaterial",
    "MagnetMaterialDatabase",
    "MotorRotorSideFaceDetail",
    "NonCADElectricMachineDetail",
    "NotchShape",
    "NotchSpecification",
    "PermanentMagnetAssistedSynchronousReluctanceMachine",
    "PermanentMagnetRotor",
    "Phase",
    "RegionID",
    "Rotor",
    "RotorInternalLayerSpecification",
    "RotorSkewSlice",
    "RotorType",
    "SingleOrDoubleLayerWindings",
    "SlotSectionDetail",
    "Stator",
    "StatorCutoutSpecification",
    "StatorRotorMaterial",
    "StatorRotorMaterialDatabase",
    "SurfacePermanentMagnetMachine",
    "SurfacePermanentMagnetRotor",
    "SynchronousReluctanceMachine",
    "ToothAndSlot",
    "ToothSlotStyle",
    "ToothTaperSpecification",
    "TwoDimensionalFEModelForAnalysis",
    "TwoDimensionalFEModelForElectromagneticAnalysis",
    "TwoDimensionalFEModelForMechanicalAnalysis",
    "UShapedLayerSpecification",
    "VShapedMagnetLayerSpecification",
    "WindingConductor",
    "WindingConnection",
    "WindingMaterial",
    "WindingMaterialDatabase",
    "Windings",
    "WindingsViewer",
    "WindingType",
    "WireSizeSpecificationMethod",
    "WoundFieldSynchronousMachine",
    "WoundFieldSynchronousRotor",
)
