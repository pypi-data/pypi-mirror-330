"""GearDesignAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1263

_GEAR_DESIGN_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearDesignAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1267, _1268, _1269
    from mastapy._private.gears.fe_model import _1245
    from mastapy._private.gears.fe_model.conical import _1252
    from mastapy._private.gears.fe_model.cylindrical import _1249
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1141,
        _1142,
        _1143,
        _1145,
    )
    from mastapy._private.gears.gear_designs.face import _1025
    from mastapy._private.gears.gear_two_d_fe_analysis import _929, _930
    from mastapy._private.gears.load_case import _904
    from mastapy._private.gears.load_case.bevel import _922
    from mastapy._private.gears.load_case.concept import _919
    from mastapy._private.gears.load_case.conical import _916
    from mastapy._private.gears.load_case.cylindrical import _913
    from mastapy._private.gears.load_case.face import _910
    from mastapy._private.gears.load_case.worm import _907
    from mastapy._private.gears.ltca import _871
    from mastapy._private.gears.ltca.conical import _898
    from mastapy._private.gears.ltca.cylindrical import _887
    from mastapy._private.gears.manufacturing.bevel import (
        _806,
        _807,
        _808,
        _809,
        _819,
        _820,
        _825,
    )
    from mastapy._private.gears.manufacturing.cylindrical import _643, _647, _648

    Self = TypeVar("Self", bound="GearDesignAnalysis")
    CastSelf = TypeVar("CastSelf", bound="GearDesignAnalysis._Cast_GearDesignAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("GearDesignAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearDesignAnalysis:
    """Special nested class for casting GearDesignAnalysis to subclasses."""

    __parent__: "GearDesignAnalysis"

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1263.AbstractGearAnalysis":
        return self.__parent__._cast(_1263.AbstractGearAnalysis)

    @property
    def cylindrical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_643.CylindricalGearManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _643

        return self.__parent__._cast(_643.CylindricalGearManufacturingConfig)

    @property
    def cylindrical_manufactured_gear_duty_cycle(
        self: "CastSelf",
    ) -> "_647.CylindricalManufacturedGearDutyCycle":
        from mastapy._private.gears.manufacturing.cylindrical import _647

        return self.__parent__._cast(_647.CylindricalManufacturedGearDutyCycle)

    @property
    def cylindrical_manufactured_gear_load_case(
        self: "CastSelf",
    ) -> "_648.CylindricalManufacturedGearLoadCase":
        from mastapy._private.gears.manufacturing.cylindrical import _648

        return self.__parent__._cast(_648.CylindricalManufacturedGearLoadCase)

    @property
    def conical_gear_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_806.ConicalGearManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _806

        return self.__parent__._cast(_806.ConicalGearManufacturingAnalysis)

    @property
    def conical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_807.ConicalGearManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _807

        return self.__parent__._cast(_807.ConicalGearManufacturingConfig)

    @property
    def conical_gear_micro_geometry_config(
        self: "CastSelf",
    ) -> "_808.ConicalGearMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _808

        return self.__parent__._cast(_808.ConicalGearMicroGeometryConfig)

    @property
    def conical_gear_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_809.ConicalGearMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _809

        return self.__parent__._cast(_809.ConicalGearMicroGeometryConfigBase)

    @property
    def conical_pinion_manufacturing_config(
        self: "CastSelf",
    ) -> "_819.ConicalPinionManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _819

        return self.__parent__._cast(_819.ConicalPinionManufacturingConfig)

    @property
    def conical_pinion_micro_geometry_config(
        self: "CastSelf",
    ) -> "_820.ConicalPinionMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _820

        return self.__parent__._cast(_820.ConicalPinionMicroGeometryConfig)

    @property
    def conical_wheel_manufacturing_config(
        self: "CastSelf",
    ) -> "_825.ConicalWheelManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _825

        return self.__parent__._cast(_825.ConicalWheelManufacturingConfig)

    @property
    def gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_871.GearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _871

        return self.__parent__._cast(_871.GearLoadDistributionAnalysis)

    @property
    def cylindrical_gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_887.CylindricalGearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _887

        return self.__parent__._cast(_887.CylindricalGearLoadDistributionAnalysis)

    @property
    def conical_gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_898.ConicalGearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _898

        return self.__parent__._cast(_898.ConicalGearLoadDistributionAnalysis)

    @property
    def gear_load_case_base(self: "CastSelf") -> "_904.GearLoadCaseBase":
        from mastapy._private.gears.load_case import _904

        return self.__parent__._cast(_904.GearLoadCaseBase)

    @property
    def worm_gear_load_case(self: "CastSelf") -> "_907.WormGearLoadCase":
        from mastapy._private.gears.load_case.worm import _907

        return self.__parent__._cast(_907.WormGearLoadCase)

    @property
    def face_gear_load_case(self: "CastSelf") -> "_910.FaceGearLoadCase":
        from mastapy._private.gears.load_case.face import _910

        return self.__parent__._cast(_910.FaceGearLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "_913.CylindricalGearLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _913

        return self.__parent__._cast(_913.CylindricalGearLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_916.ConicalGearLoadCase":
        from mastapy._private.gears.load_case.conical import _916

        return self.__parent__._cast(_916.ConicalGearLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_919.ConceptGearLoadCase":
        from mastapy._private.gears.load_case.concept import _919

        return self.__parent__._cast(_919.ConceptGearLoadCase)

    @property
    def bevel_load_case(self: "CastSelf") -> "_922.BevelLoadCase":
        from mastapy._private.gears.load_case.bevel import _922

        return self.__parent__._cast(_922.BevelLoadCase)

    @property
    def cylindrical_gear_tiff_analysis(
        self: "CastSelf",
    ) -> "_929.CylindricalGearTIFFAnalysis":
        from mastapy._private.gears.gear_two_d_fe_analysis import _929

        return self.__parent__._cast(_929.CylindricalGearTIFFAnalysis)

    @property
    def cylindrical_gear_tiff_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_930.CylindricalGearTIFFAnalysisDutyCycle":
        from mastapy._private.gears.gear_two_d_fe_analysis import _930

        return self.__parent__._cast(_930.CylindricalGearTIFFAnalysisDutyCycle)

    @property
    def face_gear_micro_geometry(self: "CastSelf") -> "_1025.FaceGearMicroGeometry":
        from mastapy._private.gears.gear_designs.face import _1025

        return self.__parent__._cast(_1025.FaceGearMicroGeometry)

    @property
    def cylindrical_gear_micro_geometry(
        self: "CastSelf",
    ) -> "_1141.CylindricalGearMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1141

        return self.__parent__._cast(_1141.CylindricalGearMicroGeometry)

    @property
    def cylindrical_gear_micro_geometry_base(
        self: "CastSelf",
    ) -> "_1142.CylindricalGearMicroGeometryBase":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1142

        return self.__parent__._cast(_1142.CylindricalGearMicroGeometryBase)

    @property
    def cylindrical_gear_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1143.CylindricalGearMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1143

        return self.__parent__._cast(_1143.CylindricalGearMicroGeometryDutyCycle)

    @property
    def cylindrical_gear_micro_geometry_per_tooth(
        self: "CastSelf",
    ) -> "_1145.CylindricalGearMicroGeometryPerTooth":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1145

        return self.__parent__._cast(_1145.CylindricalGearMicroGeometryPerTooth)

    @property
    def gear_fe_model(self: "CastSelf") -> "_1245.GearFEModel":
        from mastapy._private.gears.fe_model import _1245

        return self.__parent__._cast(_1245.GearFEModel)

    @property
    def cylindrical_gear_fe_model(self: "CastSelf") -> "_1249.CylindricalGearFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1249

        return self.__parent__._cast(_1249.CylindricalGearFEModel)

    @property
    def conical_gear_fe_model(self: "CastSelf") -> "_1252.ConicalGearFEModel":
        from mastapy._private.gears.fe_model.conical import _1252

        return self.__parent__._cast(_1252.ConicalGearFEModel)

    @property
    def gear_implementation_analysis(
        self: "CastSelf",
    ) -> "_1267.GearImplementationAnalysis":
        from mastapy._private.gears.analysis import _1267

        return self.__parent__._cast(_1267.GearImplementationAnalysis)

    @property
    def gear_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1268.GearImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1268

        return self.__parent__._cast(_1268.GearImplementationAnalysisDutyCycle)

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1269.GearImplementationDetail":
        from mastapy._private.gears.analysis import _1269

        return self.__parent__._cast(_1269.GearImplementationDetail)

    @property
    def gear_design_analysis(self: "CastSelf") -> "GearDesignAnalysis":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class GearDesignAnalysis(_1263.AbstractGearAnalysis):
    """GearDesignAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_DESIGN_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearDesignAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearDesignAnalysis
        """
        return _Cast_GearDesignAnalysis(self)
