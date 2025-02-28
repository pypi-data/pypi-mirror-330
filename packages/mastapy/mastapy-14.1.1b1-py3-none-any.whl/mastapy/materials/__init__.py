"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.materials._255 import (
        AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial,
    )
    from mastapy._private.materials._256 import AcousticRadiationEfficiency
    from mastapy._private.materials._257 import AcousticRadiationEfficiencyInputType
    from mastapy._private.materials._258 import AGMALubricantType
    from mastapy._private.materials._259 import AGMAMaterialApplications
    from mastapy._private.materials._260 import AGMAMaterialClasses
    from mastapy._private.materials._261 import AGMAMaterialGrade
    from mastapy._private.materials._262 import AirProperties
    from mastapy._private.materials._263 import BearingLubricationCondition
    from mastapy._private.materials._264 import BearingMaterial
    from mastapy._private.materials._265 import BearingMaterialDatabase
    from mastapy._private.materials._266 import BHCurveExtrapolationMethod
    from mastapy._private.materials._267 import BHCurveSpecification
    from mastapy._private.materials._268 import ComponentMaterialDatabase
    from mastapy._private.materials._269 import CompositeFatigueSafetyFactorItem
    from mastapy._private.materials._270 import CylindricalGearRatingMethods
    from mastapy._private.materials._271 import DensitySpecificationMethod
    from mastapy._private.materials._272 import FatigueSafetyFactorItem
    from mastapy._private.materials._273 import FatigueSafetyFactorItemBase
    from mastapy._private.materials._274 import GearingTypes
    from mastapy._private.materials._275 import GeneralTransmissionProperties
    from mastapy._private.materials._276 import GreaseContaminationOptions
    from mastapy._private.materials._277 import HardnessType
    from mastapy._private.materials._278 import ISO76StaticSafetyFactorLimits
    from mastapy._private.materials._279 import ISOLubricantType
    from mastapy._private.materials._280 import LubricantDefinition
    from mastapy._private.materials._281 import LubricantDelivery
    from mastapy._private.materials._282 import LubricantViscosityClassAGMA
    from mastapy._private.materials._283 import LubricantViscosityClassification
    from mastapy._private.materials._284 import LubricantViscosityClassISO
    from mastapy._private.materials._285 import LubricantViscosityClassSAE
    from mastapy._private.materials._286 import LubricationDetail
    from mastapy._private.materials._287 import LubricationDetailDatabase
    from mastapy._private.materials._288 import Material
    from mastapy._private.materials._289 import MaterialDatabase
    from mastapy._private.materials._290 import MaterialsSettings
    from mastapy._private.materials._291 import MaterialsSettingsDatabase
    from mastapy._private.materials._292 import MaterialsSettingsItem
    from mastapy._private.materials._293 import MaterialStandards
    from mastapy._private.materials._294 import MetalPlasticType
    from mastapy._private.materials._295 import OilFiltrationOptions
    from mastapy._private.materials._296 import PressureViscosityCoefficientMethod
    from mastapy._private.materials._297 import QualityGrade
    from mastapy._private.materials._298 import SafetyFactorGroup
    from mastapy._private.materials._299 import SafetyFactorItem
    from mastapy._private.materials._300 import SNCurve
    from mastapy._private.materials._301 import SNCurvePoint
    from mastapy._private.materials._302 import SoundPressureEnclosure
    from mastapy._private.materials._303 import SoundPressureEnclosureType
    from mastapy._private.materials._304 import (
        StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial,
    )
    from mastapy._private.materials._305 import (
        StressCyclesDataForTheContactSNCurveOfAPlasticMaterial,
    )
    from mastapy._private.materials._306 import TransmissionApplications
    from mastapy._private.materials._307 import VDI2736LubricantType
    from mastapy._private.materials._308 import VehicleDynamicsProperties
    from mastapy._private.materials._309 import WindTurbineStandards
    from mastapy._private.materials._310 import WorkingCharacteristics
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.materials._255": [
            "AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial"
        ],
        "_private.materials._256": ["AcousticRadiationEfficiency"],
        "_private.materials._257": ["AcousticRadiationEfficiencyInputType"],
        "_private.materials._258": ["AGMALubricantType"],
        "_private.materials._259": ["AGMAMaterialApplications"],
        "_private.materials._260": ["AGMAMaterialClasses"],
        "_private.materials._261": ["AGMAMaterialGrade"],
        "_private.materials._262": ["AirProperties"],
        "_private.materials._263": ["BearingLubricationCondition"],
        "_private.materials._264": ["BearingMaterial"],
        "_private.materials._265": ["BearingMaterialDatabase"],
        "_private.materials._266": ["BHCurveExtrapolationMethod"],
        "_private.materials._267": ["BHCurveSpecification"],
        "_private.materials._268": ["ComponentMaterialDatabase"],
        "_private.materials._269": ["CompositeFatigueSafetyFactorItem"],
        "_private.materials._270": ["CylindricalGearRatingMethods"],
        "_private.materials._271": ["DensitySpecificationMethod"],
        "_private.materials._272": ["FatigueSafetyFactorItem"],
        "_private.materials._273": ["FatigueSafetyFactorItemBase"],
        "_private.materials._274": ["GearingTypes"],
        "_private.materials._275": ["GeneralTransmissionProperties"],
        "_private.materials._276": ["GreaseContaminationOptions"],
        "_private.materials._277": ["HardnessType"],
        "_private.materials._278": ["ISO76StaticSafetyFactorLimits"],
        "_private.materials._279": ["ISOLubricantType"],
        "_private.materials._280": ["LubricantDefinition"],
        "_private.materials._281": ["LubricantDelivery"],
        "_private.materials._282": ["LubricantViscosityClassAGMA"],
        "_private.materials._283": ["LubricantViscosityClassification"],
        "_private.materials._284": ["LubricantViscosityClassISO"],
        "_private.materials._285": ["LubricantViscosityClassSAE"],
        "_private.materials._286": ["LubricationDetail"],
        "_private.materials._287": ["LubricationDetailDatabase"],
        "_private.materials._288": ["Material"],
        "_private.materials._289": ["MaterialDatabase"],
        "_private.materials._290": ["MaterialsSettings"],
        "_private.materials._291": ["MaterialsSettingsDatabase"],
        "_private.materials._292": ["MaterialsSettingsItem"],
        "_private.materials._293": ["MaterialStandards"],
        "_private.materials._294": ["MetalPlasticType"],
        "_private.materials._295": ["OilFiltrationOptions"],
        "_private.materials._296": ["PressureViscosityCoefficientMethod"],
        "_private.materials._297": ["QualityGrade"],
        "_private.materials._298": ["SafetyFactorGroup"],
        "_private.materials._299": ["SafetyFactorItem"],
        "_private.materials._300": ["SNCurve"],
        "_private.materials._301": ["SNCurvePoint"],
        "_private.materials._302": ["SoundPressureEnclosure"],
        "_private.materials._303": ["SoundPressureEnclosureType"],
        "_private.materials._304": [
            "StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial"
        ],
        "_private.materials._305": [
            "StressCyclesDataForTheContactSNCurveOfAPlasticMaterial"
        ],
        "_private.materials._306": ["TransmissionApplications"],
        "_private.materials._307": ["VDI2736LubricantType"],
        "_private.materials._308": ["VehicleDynamicsProperties"],
        "_private.materials._309": ["WindTurbineStandards"],
        "_private.materials._310": ["WorkingCharacteristics"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial",
    "AcousticRadiationEfficiency",
    "AcousticRadiationEfficiencyInputType",
    "AGMALubricantType",
    "AGMAMaterialApplications",
    "AGMAMaterialClasses",
    "AGMAMaterialGrade",
    "AirProperties",
    "BearingLubricationCondition",
    "BearingMaterial",
    "BearingMaterialDatabase",
    "BHCurveExtrapolationMethod",
    "BHCurveSpecification",
    "ComponentMaterialDatabase",
    "CompositeFatigueSafetyFactorItem",
    "CylindricalGearRatingMethods",
    "DensitySpecificationMethod",
    "FatigueSafetyFactorItem",
    "FatigueSafetyFactorItemBase",
    "GearingTypes",
    "GeneralTransmissionProperties",
    "GreaseContaminationOptions",
    "HardnessType",
    "ISO76StaticSafetyFactorLimits",
    "ISOLubricantType",
    "LubricantDefinition",
    "LubricantDelivery",
    "LubricantViscosityClassAGMA",
    "LubricantViscosityClassification",
    "LubricantViscosityClassISO",
    "LubricantViscosityClassSAE",
    "LubricationDetail",
    "LubricationDetailDatabase",
    "Material",
    "MaterialDatabase",
    "MaterialsSettings",
    "MaterialsSettingsDatabase",
    "MaterialsSettingsItem",
    "MaterialStandards",
    "MetalPlasticType",
    "OilFiltrationOptions",
    "PressureViscosityCoefficientMethod",
    "QualityGrade",
    "SafetyFactorGroup",
    "SafetyFactorItem",
    "SNCurve",
    "SNCurvePoint",
    "SoundPressureEnclosure",
    "SoundPressureEnclosureType",
    "StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial",
    "StressCyclesDataForTheContactSNCurveOfAPlasticMaterial",
    "TransmissionApplications",
    "VDI2736LubricantType",
    "VehicleDynamicsProperties",
    "WindTurbineStandards",
    "WorkingCharacteristics",
)
