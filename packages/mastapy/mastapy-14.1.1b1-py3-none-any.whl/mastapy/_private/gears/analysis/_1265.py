"""AbstractGearSetAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ABSTRACT_GEAR_SET_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "AbstractGearSetAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1274, _1276, _1277, _1278, _1279
    from mastapy._private.gears.fe_model import _1248
    from mastapy._private.gears.fe_model.conical import _1254
    from mastapy._private.gears.fe_model.cylindrical import _1251
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1148,
        _1149,
    )
    from mastapy._private.gears.gear_designs.face import _1028
    from mastapy._private.gears.gear_two_d_fe_analysis import _927, _928
    from mastapy._private.gears.load_case import _905
    from mastapy._private.gears.load_case.bevel import _924
    from mastapy._private.gears.load_case.concept import _920
    from mastapy._private.gears.load_case.conical import _917
    from mastapy._private.gears.load_case.cylindrical import _914
    from mastapy._private.gears.load_case.face import _911
    from mastapy._private.gears.load_case.worm import _908
    from mastapy._private.gears.ltca import _877
    from mastapy._private.gears.ltca.conical import _899
    from mastapy._private.gears.ltca.cylindrical import _891, _893
    from mastapy._private.gears.manufacturing.bevel import _821, _822, _823, _824
    from mastapy._private.gears.manufacturing.cylindrical import _651, _652, _656
    from mastapy._private.gears.rating import _373, _381, _382
    from mastapy._private.gears.rating.agma_gleason_conical import _586
    from mastapy._private.gears.rating.bevel import _575
    from mastapy._private.gears.rating.concept import _571, _572
    from mastapy._private.gears.rating.conical import _560, _561
    from mastapy._private.gears.rating.cylindrical import _482, _483, _499
    from mastapy._private.gears.rating.face import _468, _469
    from mastapy._private.gears.rating.hypoid import _459
    from mastapy._private.gears.rating.klingelnberg_conical import _432
    from mastapy._private.gears.rating.klingelnberg_hypoid import _429
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _426
    from mastapy._private.gears.rating.spiral_bevel import _423
    from mastapy._private.gears.rating.straight_bevel import _416
    from mastapy._private.gears.rating.straight_bevel_diff import _419
    from mastapy._private.gears.rating.worm import _394, _395
    from mastapy._private.gears.rating.zerol_bevel import _390
    from mastapy._private.utility.model_validation import _1852, _1853

    Self = TypeVar("Self", bound="AbstractGearSetAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearSetAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearSetAnalysis:
    """Special nested class for casting AbstractGearSetAnalysis to subclasses."""

    __parent__: "AbstractGearSetAnalysis"

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_373.AbstractGearSetRating":
        from mastapy._private.gears.rating import _373

        return self.__parent__._cast(_373.AbstractGearSetRating)

    @property
    def gear_set_duty_cycle_rating(self: "CastSelf") -> "_381.GearSetDutyCycleRating":
        from mastapy._private.gears.rating import _381

        return self.__parent__._cast(_381.GearSetDutyCycleRating)

    @property
    def gear_set_rating(self: "CastSelf") -> "_382.GearSetRating":
        from mastapy._private.gears.rating import _382

        return self.__parent__._cast(_382.GearSetRating)

    @property
    def zerol_bevel_gear_set_rating(self: "CastSelf") -> "_390.ZerolBevelGearSetRating":
        from mastapy._private.gears.rating.zerol_bevel import _390

        return self.__parent__._cast(_390.ZerolBevelGearSetRating)

    @property
    def worm_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_394.WormGearSetDutyCycleRating":
        from mastapy._private.gears.rating.worm import _394

        return self.__parent__._cast(_394.WormGearSetDutyCycleRating)

    @property
    def worm_gear_set_rating(self: "CastSelf") -> "_395.WormGearSetRating":
        from mastapy._private.gears.rating.worm import _395

        return self.__parent__._cast(_395.WormGearSetRating)

    @property
    def straight_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_416.StraightBevelGearSetRating":
        from mastapy._private.gears.rating.straight_bevel import _416

        return self.__parent__._cast(_416.StraightBevelGearSetRating)

    @property
    def straight_bevel_diff_gear_set_rating(
        self: "CastSelf",
    ) -> "_419.StraightBevelDiffGearSetRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _419

        return self.__parent__._cast(_419.StraightBevelDiffGearSetRating)

    @property
    def spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_423.SpiralBevelGearSetRating":
        from mastapy._private.gears.rating.spiral_bevel import _423

        return self.__parent__._cast(_423.SpiralBevelGearSetRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_426.KlingelnbergCycloPalloidSpiralBevelGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _426

        return self.__parent__._cast(
            _426.KlingelnbergCycloPalloidSpiralBevelGearSetRating
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_rating(
        self: "CastSelf",
    ) -> "_429.KlingelnbergCycloPalloidHypoidGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _429

        return self.__parent__._cast(_429.KlingelnbergCycloPalloidHypoidGearSetRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_432.KlingelnbergCycloPalloidConicalGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _432

        return self.__parent__._cast(_432.KlingelnbergCycloPalloidConicalGearSetRating)

    @property
    def hypoid_gear_set_rating(self: "CastSelf") -> "_459.HypoidGearSetRating":
        from mastapy._private.gears.rating.hypoid import _459

        return self.__parent__._cast(_459.HypoidGearSetRating)

    @property
    def face_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_468.FaceGearSetDutyCycleRating":
        from mastapy._private.gears.rating.face import _468

        return self.__parent__._cast(_468.FaceGearSetDutyCycleRating)

    @property
    def face_gear_set_rating(self: "CastSelf") -> "_469.FaceGearSetRating":
        from mastapy._private.gears.rating.face import _469

        return self.__parent__._cast(_469.FaceGearSetRating)

    @property
    def cylindrical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_482.CylindricalGearSetDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _482

        return self.__parent__._cast(_482.CylindricalGearSetDutyCycleRating)

    @property
    def cylindrical_gear_set_rating(
        self: "CastSelf",
    ) -> "_483.CylindricalGearSetRating":
        from mastapy._private.gears.rating.cylindrical import _483

        return self.__parent__._cast(_483.CylindricalGearSetRating)

    @property
    def reduced_cylindrical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_499.ReducedCylindricalGearSetDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _499

        return self.__parent__._cast(_499.ReducedCylindricalGearSetDutyCycleRating)

    @property
    def conical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_560.ConicalGearSetDutyCycleRating":
        from mastapy._private.gears.rating.conical import _560

        return self.__parent__._cast(_560.ConicalGearSetDutyCycleRating)

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "_561.ConicalGearSetRating":
        from mastapy._private.gears.rating.conical import _561

        return self.__parent__._cast(_561.ConicalGearSetRating)

    @property
    def concept_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_571.ConceptGearSetDutyCycleRating":
        from mastapy._private.gears.rating.concept import _571

        return self.__parent__._cast(_571.ConceptGearSetDutyCycleRating)

    @property
    def concept_gear_set_rating(self: "CastSelf") -> "_572.ConceptGearSetRating":
        from mastapy._private.gears.rating.concept import _572

        return self.__parent__._cast(_572.ConceptGearSetRating)

    @property
    def bevel_gear_set_rating(self: "CastSelf") -> "_575.BevelGearSetRating":
        from mastapy._private.gears.rating.bevel import _575

        return self.__parent__._cast(_575.BevelGearSetRating)

    @property
    def agma_gleason_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_586.AGMAGleasonConicalGearSetRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _586

        return self.__parent__._cast(_586.AGMAGleasonConicalGearSetRating)

    @property
    def cylindrical_manufactured_gear_set_duty_cycle(
        self: "CastSelf",
    ) -> "_651.CylindricalManufacturedGearSetDutyCycle":
        from mastapy._private.gears.manufacturing.cylindrical import _651

        return self.__parent__._cast(_651.CylindricalManufacturedGearSetDutyCycle)

    @property
    def cylindrical_manufactured_gear_set_load_case(
        self: "CastSelf",
    ) -> "_652.CylindricalManufacturedGearSetLoadCase":
        from mastapy._private.gears.manufacturing.cylindrical import _652

        return self.__parent__._cast(_652.CylindricalManufacturedGearSetLoadCase)

    @property
    def cylindrical_set_manufacturing_config(
        self: "CastSelf",
    ) -> "_656.CylindricalSetManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _656

        return self.__parent__._cast(_656.CylindricalSetManufacturingConfig)

    @property
    def conical_set_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_821.ConicalSetManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _821

        return self.__parent__._cast(_821.ConicalSetManufacturingAnalysis)

    @property
    def conical_set_manufacturing_config(
        self: "CastSelf",
    ) -> "_822.ConicalSetManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _822

        return self.__parent__._cast(_822.ConicalSetManufacturingConfig)

    @property
    def conical_set_micro_geometry_config(
        self: "CastSelf",
    ) -> "_823.ConicalSetMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _823

        return self.__parent__._cast(_823.ConicalSetMicroGeometryConfig)

    @property
    def conical_set_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_824.ConicalSetMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _824

        return self.__parent__._cast(_824.ConicalSetMicroGeometryConfigBase)

    @property
    def gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_877.GearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _877

        return self.__parent__._cast(_877.GearSetLoadDistributionAnalysis)

    @property
    def cylindrical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_891.CylindricalGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _891

        return self.__parent__._cast(_891.CylindricalGearSetLoadDistributionAnalysis)

    @property
    def face_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_893.FaceGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _893

        return self.__parent__._cast(_893.FaceGearSetLoadDistributionAnalysis)

    @property
    def conical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_899.ConicalGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _899

        return self.__parent__._cast(_899.ConicalGearSetLoadDistributionAnalysis)

    @property
    def gear_set_load_case_base(self: "CastSelf") -> "_905.GearSetLoadCaseBase":
        from mastapy._private.gears.load_case import _905

        return self.__parent__._cast(_905.GearSetLoadCaseBase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_908.WormGearSetLoadCase":
        from mastapy._private.gears.load_case.worm import _908

        return self.__parent__._cast(_908.WormGearSetLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_911.FaceGearSetLoadCase":
        from mastapy._private.gears.load_case.face import _911

        return self.__parent__._cast(_911.FaceGearSetLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_914.CylindricalGearSetLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _914

        return self.__parent__._cast(_914.CylindricalGearSetLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_917.ConicalGearSetLoadCase":
        from mastapy._private.gears.load_case.conical import _917

        return self.__parent__._cast(_917.ConicalGearSetLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_920.ConceptGearSetLoadCase":
        from mastapy._private.gears.load_case.concept import _920

        return self.__parent__._cast(_920.ConceptGearSetLoadCase)

    @property
    def bevel_set_load_case(self: "CastSelf") -> "_924.BevelSetLoadCase":
        from mastapy._private.gears.load_case.bevel import _924

        return self.__parent__._cast(_924.BevelSetLoadCase)

    @property
    def cylindrical_gear_set_tiff_analysis(
        self: "CastSelf",
    ) -> "_927.CylindricalGearSetTIFFAnalysis":
        from mastapy._private.gears.gear_two_d_fe_analysis import _927

        return self.__parent__._cast(_927.CylindricalGearSetTIFFAnalysis)

    @property
    def cylindrical_gear_set_tiff_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_928.CylindricalGearSetTIFFAnalysisDutyCycle":
        from mastapy._private.gears.gear_two_d_fe_analysis import _928

        return self.__parent__._cast(_928.CylindricalGearSetTIFFAnalysisDutyCycle)

    @property
    def face_gear_set_micro_geometry(
        self: "CastSelf",
    ) -> "_1028.FaceGearSetMicroGeometry":
        from mastapy._private.gears.gear_designs.face import _1028

        return self.__parent__._cast(_1028.FaceGearSetMicroGeometry)

    @property
    def cylindrical_gear_set_micro_geometry(
        self: "CastSelf",
    ) -> "_1148.CylindricalGearSetMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1148

        return self.__parent__._cast(_1148.CylindricalGearSetMicroGeometry)

    @property
    def cylindrical_gear_set_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1149.CylindricalGearSetMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1149

        return self.__parent__._cast(_1149.CylindricalGearSetMicroGeometryDutyCycle)

    @property
    def gear_set_fe_model(self: "CastSelf") -> "_1248.GearSetFEModel":
        from mastapy._private.gears.fe_model import _1248

        return self.__parent__._cast(_1248.GearSetFEModel)

    @property
    def cylindrical_gear_set_fe_model(
        self: "CastSelf",
    ) -> "_1251.CylindricalGearSetFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1251

        return self.__parent__._cast(_1251.CylindricalGearSetFEModel)

    @property
    def conical_set_fe_model(self: "CastSelf") -> "_1254.ConicalSetFEModel":
        from mastapy._private.gears.fe_model.conical import _1254

        return self.__parent__._cast(_1254.ConicalSetFEModel)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1274.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1274

        return self.__parent__._cast(_1274.GearSetDesignAnalysis)

    @property
    def gear_set_implementation_analysis(
        self: "CastSelf",
    ) -> "_1276.GearSetImplementationAnalysis":
        from mastapy._private.gears.analysis import _1276

        return self.__parent__._cast(_1276.GearSetImplementationAnalysis)

    @property
    def gear_set_implementation_analysis_abstract(
        self: "CastSelf",
    ) -> "_1277.GearSetImplementationAnalysisAbstract":
        from mastapy._private.gears.analysis import _1277

        return self.__parent__._cast(_1277.GearSetImplementationAnalysisAbstract)

    @property
    def gear_set_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1278.GearSetImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1278

        return self.__parent__._cast(_1278.GearSetImplementationAnalysisDutyCycle)

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1279.GearSetImplementationDetail":
        from mastapy._private.gears.analysis import _1279

        return self.__parent__._cast(_1279.GearSetImplementationDetail)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "AbstractGearSetAnalysis":
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
class AbstractGearSetAnalysis(_0.APIBase):
    """AbstractGearSetAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_SET_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    def all_status_errors(self: "Self") -> "List[_1853.StatusItem]":
        """List[mastapy.utility.model_validation.StatusItem]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllStatusErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def status(self: "Self") -> "_1852.Status":
        """mastapy.utility.model_validation.Status

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Status")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def cast_to(self: "Self") -> "_Cast_AbstractGearSetAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearSetAnalysis
        """
        return _Cast_AbstractGearSetAnalysis(self)
