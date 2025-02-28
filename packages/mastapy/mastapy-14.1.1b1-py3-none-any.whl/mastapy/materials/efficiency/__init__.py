"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.materials.efficiency._311 import BearingEfficiencyRatingMethod
    from mastapy._private.materials.efficiency._312 import CombinedResistiveTorque
    from mastapy._private.materials.efficiency._313 import IndependentPowerLoss
    from mastapy._private.materials.efficiency._314 import IndependentResistiveTorque
    from mastapy._private.materials.efficiency._315 import LoadAndSpeedCombinedPowerLoss
    from mastapy._private.materials.efficiency._316 import OilPumpDetail
    from mastapy._private.materials.efficiency._317 import OilPumpDriveType
    from mastapy._private.materials.efficiency._318 import OilSealLossCalculationMethod
    from mastapy._private.materials.efficiency._319 import OilSealMaterialType
    from mastapy._private.materials.efficiency._320 import PowerLoss
    from mastapy._private.materials.efficiency._321 import ResistiveTorque
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.materials.efficiency._311": ["BearingEfficiencyRatingMethod"],
        "_private.materials.efficiency._312": ["CombinedResistiveTorque"],
        "_private.materials.efficiency._313": ["IndependentPowerLoss"],
        "_private.materials.efficiency._314": ["IndependentResistiveTorque"],
        "_private.materials.efficiency._315": ["LoadAndSpeedCombinedPowerLoss"],
        "_private.materials.efficiency._316": ["OilPumpDetail"],
        "_private.materials.efficiency._317": ["OilPumpDriveType"],
        "_private.materials.efficiency._318": ["OilSealLossCalculationMethod"],
        "_private.materials.efficiency._319": ["OilSealMaterialType"],
        "_private.materials.efficiency._320": ["PowerLoss"],
        "_private.materials.efficiency._321": ["ResistiveTorque"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingEfficiencyRatingMethod",
    "CombinedResistiveTorque",
    "IndependentPowerLoss",
    "IndependentResistiveTorque",
    "LoadAndSpeedCombinedPowerLoss",
    "OilPumpDetail",
    "OilPumpDriveType",
    "OilSealLossCalculationMethod",
    "OilSealMaterialType",
    "PowerLoss",
    "ResistiveTorque",
)
