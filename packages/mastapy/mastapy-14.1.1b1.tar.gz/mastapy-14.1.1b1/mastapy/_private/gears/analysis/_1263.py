"""AbstractGearAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ABSTRACT_GEAR_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "AbstractGearAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1266, _1267, _1268, _1269
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
    from mastapy._private.gears.rating import _372, _376, _380
    from mastapy._private.gears.rating.agma_gleason_conical import _585
    from mastapy._private.gears.rating.bevel import _574
    from mastapy._private.gears.rating.concept import _567, _570
    from mastapy._private.gears.rating.conical import _557, _559
    from mastapy._private.gears.rating.cylindrical import _474, _479
    from mastapy._private.gears.rating.face import _464, _467
    from mastapy._private.gears.rating.hypoid import _458
    from mastapy._private.gears.rating.klingelnberg_conical import _431
    from mastapy._private.gears.rating.klingelnberg_hypoid import _428
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _425
    from mastapy._private.gears.rating.spiral_bevel import _422
    from mastapy._private.gears.rating.straight_bevel import _415
    from mastapy._private.gears.rating.straight_bevel_diff import _418
    from mastapy._private.gears.rating.worm import _391, _393
    from mastapy._private.gears.rating.zerol_bevel import _389

    Self = TypeVar("Self", bound="AbstractGearAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractGearAnalysis._Cast_AbstractGearAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearAnalysis:
    """Special nested class for casting AbstractGearAnalysis to subclasses."""

    __parent__: "AbstractGearAnalysis"

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_372.AbstractGearRating":
        from mastapy._private.gears.rating import _372

        return self.__parent__._cast(_372.AbstractGearRating)

    @property
    def gear_duty_cycle_rating(self: "CastSelf") -> "_376.GearDutyCycleRating":
        from mastapy._private.gears.rating import _376

        return self.__parent__._cast(_376.GearDutyCycleRating)

    @property
    def gear_rating(self: "CastSelf") -> "_380.GearRating":
        from mastapy._private.gears.rating import _380

        return self.__parent__._cast(_380.GearRating)

    @property
    def zerol_bevel_gear_rating(self: "CastSelf") -> "_389.ZerolBevelGearRating":
        from mastapy._private.gears.rating.zerol_bevel import _389

        return self.__parent__._cast(_389.ZerolBevelGearRating)

    @property
    def worm_gear_duty_cycle_rating(self: "CastSelf") -> "_391.WormGearDutyCycleRating":
        from mastapy._private.gears.rating.worm import _391

        return self.__parent__._cast(_391.WormGearDutyCycleRating)

    @property
    def worm_gear_rating(self: "CastSelf") -> "_393.WormGearRating":
        from mastapy._private.gears.rating.worm import _393

        return self.__parent__._cast(_393.WormGearRating)

    @property
    def straight_bevel_gear_rating(self: "CastSelf") -> "_415.StraightBevelGearRating":
        from mastapy._private.gears.rating.straight_bevel import _415

        return self.__parent__._cast(_415.StraightBevelGearRating)

    @property
    def straight_bevel_diff_gear_rating(
        self: "CastSelf",
    ) -> "_418.StraightBevelDiffGearRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _418

        return self.__parent__._cast(_418.StraightBevelDiffGearRating)

    @property
    def spiral_bevel_gear_rating(self: "CastSelf") -> "_422.SpiralBevelGearRating":
        from mastapy._private.gears.rating.spiral_bevel import _422

        return self.__parent__._cast(_422.SpiralBevelGearRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_rating(
        self: "CastSelf",
    ) -> "_425.KlingelnbergCycloPalloidSpiralBevelGearRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _425

        return self.__parent__._cast(_425.KlingelnbergCycloPalloidSpiralBevelGearRating)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_rating(
        self: "CastSelf",
    ) -> "_428.KlingelnbergCycloPalloidHypoidGearRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _428

        return self.__parent__._cast(_428.KlingelnbergCycloPalloidHypoidGearRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_rating(
        self: "CastSelf",
    ) -> "_431.KlingelnbergCycloPalloidConicalGearRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _431

        return self.__parent__._cast(_431.KlingelnbergCycloPalloidConicalGearRating)

    @property
    def hypoid_gear_rating(self: "CastSelf") -> "_458.HypoidGearRating":
        from mastapy._private.gears.rating.hypoid import _458

        return self.__parent__._cast(_458.HypoidGearRating)

    @property
    def face_gear_duty_cycle_rating(self: "CastSelf") -> "_464.FaceGearDutyCycleRating":
        from mastapy._private.gears.rating.face import _464

        return self.__parent__._cast(_464.FaceGearDutyCycleRating)

    @property
    def face_gear_rating(self: "CastSelf") -> "_467.FaceGearRating":
        from mastapy._private.gears.rating.face import _467

        return self.__parent__._cast(_467.FaceGearRating)

    @property
    def cylindrical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_474.CylindricalGearDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _474

        return self.__parent__._cast(_474.CylindricalGearDutyCycleRating)

    @property
    def cylindrical_gear_rating(self: "CastSelf") -> "_479.CylindricalGearRating":
        from mastapy._private.gears.rating.cylindrical import _479

        return self.__parent__._cast(_479.CylindricalGearRating)

    @property
    def conical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_557.ConicalGearDutyCycleRating":
        from mastapy._private.gears.rating.conical import _557

        return self.__parent__._cast(_557.ConicalGearDutyCycleRating)

    @property
    def conical_gear_rating(self: "CastSelf") -> "_559.ConicalGearRating":
        from mastapy._private.gears.rating.conical import _559

        return self.__parent__._cast(_559.ConicalGearRating)

    @property
    def concept_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_567.ConceptGearDutyCycleRating":
        from mastapy._private.gears.rating.concept import _567

        return self.__parent__._cast(_567.ConceptGearDutyCycleRating)

    @property
    def concept_gear_rating(self: "CastSelf") -> "_570.ConceptGearRating":
        from mastapy._private.gears.rating.concept import _570

        return self.__parent__._cast(_570.ConceptGearRating)

    @property
    def bevel_gear_rating(self: "CastSelf") -> "_574.BevelGearRating":
        from mastapy._private.gears.rating.bevel import _574

        return self.__parent__._cast(_574.BevelGearRating)

    @property
    def agma_gleason_conical_gear_rating(
        self: "CastSelf",
    ) -> "_585.AGMAGleasonConicalGearRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _585

        return self.__parent__._cast(_585.AGMAGleasonConicalGearRating)

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
    def gear_design_analysis(self: "CastSelf") -> "_1266.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1266

        return self.__parent__._cast(_1266.GearDesignAnalysis)

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
    def abstract_gear_analysis(self: "CastSelf") -> "AbstractGearAnalysis":
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
class AbstractGearAnalysis(_0.APIBase):
    """AbstractGearAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def name_with_gear_set_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NameWithGearSetName")

        if temp is None:
            return ""

        return temp

    @property
    def planet_index(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PlanetIndex")

        if temp is None:
            return 0

        return temp

    @planet_index.setter
    @enforce_parameter_types
    def planet_index(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "PlanetIndex", int(value) if value is not None else 0
        )

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractGearAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearAnalysis
        """
        return _Cast_AbstractGearAnalysis(self)
