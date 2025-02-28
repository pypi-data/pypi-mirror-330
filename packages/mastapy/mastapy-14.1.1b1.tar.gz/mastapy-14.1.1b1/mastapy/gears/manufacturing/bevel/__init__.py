"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.bevel._803 import AbstractTCA
    from mastapy._private.gears.manufacturing.bevel._804 import (
        BevelMachineSettingOptimizationResult,
    )
    from mastapy._private.gears.manufacturing.bevel._805 import (
        ConicalFlankDeviationsData,
    )
    from mastapy._private.gears.manufacturing.bevel._806 import (
        ConicalGearManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._807 import (
        ConicalGearManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._808 import (
        ConicalGearMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._809 import (
        ConicalGearMicroGeometryConfigBase,
    )
    from mastapy._private.gears.manufacturing.bevel._810 import (
        ConicalMeshedGearManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._811 import (
        ConicalMeshedWheelFlankManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._812 import (
        ConicalMeshFlankManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._813 import (
        ConicalMeshFlankMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._814 import (
        ConicalMeshFlankNURBSMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._815 import (
        ConicalMeshManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._816 import (
        ConicalMeshManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._817 import (
        ConicalMeshMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._818 import (
        ConicalMeshMicroGeometryConfigBase,
    )
    from mastapy._private.gears.manufacturing.bevel._819 import (
        ConicalPinionManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._820 import (
        ConicalPinionMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._821 import (
        ConicalSetManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._822 import (
        ConicalSetManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._823 import (
        ConicalSetMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._824 import (
        ConicalSetMicroGeometryConfigBase,
    )
    from mastapy._private.gears.manufacturing.bevel._825 import (
        ConicalWheelManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._826 import EaseOffBasedTCA
    from mastapy._private.gears.manufacturing.bevel._827 import FlankMeasurementBorder
    from mastapy._private.gears.manufacturing.bevel._828 import HypoidAdvancedLibrary
    from mastapy._private.gears.manufacturing.bevel._829 import MachineTypes
    from mastapy._private.gears.manufacturing.bevel._830 import ManufacturingMachine
    from mastapy._private.gears.manufacturing.bevel._831 import (
        ManufacturingMachineDatabase,
    )
    from mastapy._private.gears.manufacturing.bevel._832 import (
        PinionBevelGeneratingModifiedRollMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._833 import (
        PinionBevelGeneratingTiltMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._834 import PinionConcave
    from mastapy._private.gears.manufacturing.bevel._835 import (
        PinionConicalMachineSettingsSpecified,
    )
    from mastapy._private.gears.manufacturing.bevel._836 import PinionConvex
    from mastapy._private.gears.manufacturing.bevel._837 import (
        PinionFinishMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._838 import (
        PinionHypoidFormateTiltMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._839 import (
        PinionHypoidGeneratingTiltMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._840 import PinionMachineSettingsSMT
    from mastapy._private.gears.manufacturing.bevel._841 import (
        PinionRoughMachineSetting,
    )
    from mastapy._private.gears.manufacturing.bevel._842 import Wheel
    from mastapy._private.gears.manufacturing.bevel._843 import WheelFormatMachineTypes
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.bevel._803": ["AbstractTCA"],
        "_private.gears.manufacturing.bevel._804": [
            "BevelMachineSettingOptimizationResult"
        ],
        "_private.gears.manufacturing.bevel._805": ["ConicalFlankDeviationsData"],
        "_private.gears.manufacturing.bevel._806": ["ConicalGearManufacturingAnalysis"],
        "_private.gears.manufacturing.bevel._807": ["ConicalGearManufacturingConfig"],
        "_private.gears.manufacturing.bevel._808": ["ConicalGearMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._809": [
            "ConicalGearMicroGeometryConfigBase"
        ],
        "_private.gears.manufacturing.bevel._810": [
            "ConicalMeshedGearManufacturingAnalysis"
        ],
        "_private.gears.manufacturing.bevel._811": [
            "ConicalMeshedWheelFlankManufacturingConfig"
        ],
        "_private.gears.manufacturing.bevel._812": [
            "ConicalMeshFlankManufacturingConfig"
        ],
        "_private.gears.manufacturing.bevel._813": [
            "ConicalMeshFlankMicroGeometryConfig"
        ],
        "_private.gears.manufacturing.bevel._814": [
            "ConicalMeshFlankNURBSMicroGeometryConfig"
        ],
        "_private.gears.manufacturing.bevel._815": ["ConicalMeshManufacturingAnalysis"],
        "_private.gears.manufacturing.bevel._816": ["ConicalMeshManufacturingConfig"],
        "_private.gears.manufacturing.bevel._817": ["ConicalMeshMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._818": [
            "ConicalMeshMicroGeometryConfigBase"
        ],
        "_private.gears.manufacturing.bevel._819": ["ConicalPinionManufacturingConfig"],
        "_private.gears.manufacturing.bevel._820": ["ConicalPinionMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._821": ["ConicalSetManufacturingAnalysis"],
        "_private.gears.manufacturing.bevel._822": ["ConicalSetManufacturingConfig"],
        "_private.gears.manufacturing.bevel._823": ["ConicalSetMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._824": [
            "ConicalSetMicroGeometryConfigBase"
        ],
        "_private.gears.manufacturing.bevel._825": ["ConicalWheelManufacturingConfig"],
        "_private.gears.manufacturing.bevel._826": ["EaseOffBasedTCA"],
        "_private.gears.manufacturing.bevel._827": ["FlankMeasurementBorder"],
        "_private.gears.manufacturing.bevel._828": ["HypoidAdvancedLibrary"],
        "_private.gears.manufacturing.bevel._829": ["MachineTypes"],
        "_private.gears.manufacturing.bevel._830": ["ManufacturingMachine"],
        "_private.gears.manufacturing.bevel._831": ["ManufacturingMachineDatabase"],
        "_private.gears.manufacturing.bevel._832": [
            "PinionBevelGeneratingModifiedRollMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._833": [
            "PinionBevelGeneratingTiltMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._834": ["PinionConcave"],
        "_private.gears.manufacturing.bevel._835": [
            "PinionConicalMachineSettingsSpecified"
        ],
        "_private.gears.manufacturing.bevel._836": ["PinionConvex"],
        "_private.gears.manufacturing.bevel._837": ["PinionFinishMachineSettings"],
        "_private.gears.manufacturing.bevel._838": [
            "PinionHypoidFormateTiltMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._839": [
            "PinionHypoidGeneratingTiltMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._840": ["PinionMachineSettingsSMT"],
        "_private.gears.manufacturing.bevel._841": ["PinionRoughMachineSetting"],
        "_private.gears.manufacturing.bevel._842": ["Wheel"],
        "_private.gears.manufacturing.bevel._843": ["WheelFormatMachineTypes"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractTCA",
    "BevelMachineSettingOptimizationResult",
    "ConicalFlankDeviationsData",
    "ConicalGearManufacturingAnalysis",
    "ConicalGearManufacturingConfig",
    "ConicalGearMicroGeometryConfig",
    "ConicalGearMicroGeometryConfigBase",
    "ConicalMeshedGearManufacturingAnalysis",
    "ConicalMeshedWheelFlankManufacturingConfig",
    "ConicalMeshFlankManufacturingConfig",
    "ConicalMeshFlankMicroGeometryConfig",
    "ConicalMeshFlankNURBSMicroGeometryConfig",
    "ConicalMeshManufacturingAnalysis",
    "ConicalMeshManufacturingConfig",
    "ConicalMeshMicroGeometryConfig",
    "ConicalMeshMicroGeometryConfigBase",
    "ConicalPinionManufacturingConfig",
    "ConicalPinionMicroGeometryConfig",
    "ConicalSetManufacturingAnalysis",
    "ConicalSetManufacturingConfig",
    "ConicalSetMicroGeometryConfig",
    "ConicalSetMicroGeometryConfigBase",
    "ConicalWheelManufacturingConfig",
    "EaseOffBasedTCA",
    "FlankMeasurementBorder",
    "HypoidAdvancedLibrary",
    "MachineTypes",
    "ManufacturingMachine",
    "ManufacturingMachineDatabase",
    "PinionBevelGeneratingModifiedRollMachineSettings",
    "PinionBevelGeneratingTiltMachineSettings",
    "PinionConcave",
    "PinionConicalMachineSettingsSpecified",
    "PinionConvex",
    "PinionFinishMachineSettings",
    "PinionHypoidFormateTiltMachineSettings",
    "PinionHypoidGeneratingTiltMachineSettings",
    "PinionMachineSettingsSMT",
    "PinionRoughMachineSetting",
    "Wheel",
    "WheelFormatMachineTypes",
)
