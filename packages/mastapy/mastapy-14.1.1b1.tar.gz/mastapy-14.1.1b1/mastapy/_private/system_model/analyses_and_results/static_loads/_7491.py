"""StaticLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7490
from mastapy._private.system_model.part_model import _2545

_STATIC_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "StaticLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.gears import _359
    from mastapy._private.system_model.analyses_and_results import _2722, _2755
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7213,
        _7214,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _6945,
        _7008,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7694
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6716,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5882,
        _5886,
        _5887,
        _5891,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5781,
        _5782,
        _5783,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4757
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4485,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4216
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3960,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7497,
        _7503,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3167,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2899,
    )

    Self = TypeVar("Self", bound="StaticLoadCase")
    CastSelf = TypeVar("CastSelf", bound="StaticLoadCase._Cast_StaticLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("StaticLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StaticLoadCase:
    """Special nested class for casting StaticLoadCase to subclasses."""

    __parent__: "StaticLoadCase"

    @property
    def load_case(self: "CastSelf") -> "_7490.LoadCase":
        return self.__parent__._cast(_7490.LoadCase)

    @property
    def context(self: "CastSelf") -> "_2722.Context":
        from mastapy._private.system_model.analyses_and_results import _2722

        return self.__parent__._cast(_2722.Context)

    @property
    def parametric_study_static_load(
        self: "CastSelf",
    ) -> "_4485.ParametricStudyStaticLoad":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4485,
        )

        return self.__parent__._cast(_4485.ParametricStudyStaticLoad)

    @property
    def harmonic_analysis_with_varying_stiffness_static_load_case(
        self: "CastSelf",
    ) -> "_5891.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5891,
        )

        return self.__parent__._cast(
            _5891.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase
        )

    @property
    def advanced_time_stepping_analysis_for_modulation_static_load_case(
        self: "CastSelf",
    ) -> "_7497.AdvancedTimeSteppingAnalysisForModulationStaticLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7497,
        )

        return self.__parent__._cast(
            _7497.AdvancedTimeSteppingAnalysisForModulationStaticLoadCase
        )

    @property
    def static_load_case(self: "CastSelf") -> "StaticLoadCase":
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
class StaticLoadCase(_7490.LoadCase):
    """StaticLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STATIC_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def current_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CurrentTime")

        if temp is None:
            return 0.0

        return temp

    @current_time.setter
    @enforce_parameter_types
    def current_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CurrentTime", float(value) if value is not None else 0.0
        )

    @property
    def default_planetary_rating_load_sharing_method(
        self: "Self",
    ) -> "_359.PlanetaryRatingLoadSharingOption":
        """mastapy.gears.PlanetaryRatingLoadSharingOption"""
        temp = pythonnet_property_get(
            self.wrapped, "DefaultPlanetaryRatingLoadSharingMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.PlanetaryRatingLoadSharingOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._359", "PlanetaryRatingLoadSharingOption"
        )(value)

    @default_planetary_rating_load_sharing_method.setter
    @enforce_parameter_types
    def default_planetary_rating_load_sharing_method(
        self: "Self", value: "_359.PlanetaryRatingLoadSharingOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.PlanetaryRatingLoadSharingOption"
        )
        pythonnet_property_set(
            self.wrapped, "DefaultPlanetaryRatingLoadSharingMethod", value
        )

    @property
    def design_state(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignState")

        if temp is None:
            return ""

        return temp

    @property
    def duration(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Duration")

        if temp is None:
            return 0.0

        return temp

    @duration.setter
    @enforce_parameter_types
    def duration(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Duration", float(value) if value is not None else 0.0
        )

    @property
    def input_shaft_cycles(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InputShaftCycles")

        if temp is None:
            return 0.0

        return temp

    @input_shaft_cycles.setter
    @enforce_parameter_types
    def input_shaft_cycles(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "InputShaftCycles", float(value) if value is not None else 0.0
        )

    @property
    def is_stop_start_load_case(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsStopStartLoadCase")

        if temp is None:
            return False

        return temp

    @is_stop_start_load_case.setter
    @enforce_parameter_types
    def is_stop_start_load_case(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsStopStartLoadCase",
            bool(value) if value is not None else False,
        )

    @property
    def number_of_stop_start_cycles(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfStopStartCycles")

        if temp is None:
            return 0

        return temp

    @number_of_stop_start_cycles.setter
    @enforce_parameter_types
    def number_of_stop_start_cycles(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfStopStartCycles",
            int(value) if value is not None else 0,
        )

    @property
    def percentage_of_shaft_torque_alternating(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "PercentageOfShaftTorqueAlternating"
        )

        if temp is None:
            return 0.0

        return temp

    @percentage_of_shaft_torque_alternating.setter
    @enforce_parameter_types
    def percentage_of_shaft_torque_alternating(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PercentageOfShaftTorqueAlternating",
            float(value) if value is not None else 0.0,
        )

    @property
    def power_convergence_tolerance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PowerConvergenceTolerance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @power_convergence_tolerance.setter
    @enforce_parameter_types
    def power_convergence_tolerance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PowerConvergenceTolerance", value)

    @property
    def unbalanced_mass_inclusion(
        self: "Self",
    ) -> "overridable.Overridable_UnbalancedMassInclusionOption":
        """Overridable[mastapy.system_model.part_model.UnbalancedMassInclusionOption]"""
        temp = pythonnet_property_get(self.wrapped, "UnbalancedMassInclusion")

        if temp is None:
            return None

        value = overridable.Overridable_UnbalancedMassInclusionOption.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @unbalanced_mass_inclusion.setter
    @enforce_parameter_types
    def unbalanced_mass_inclusion(
        self: "Self",
        value: "Union[_2545.UnbalancedMassInclusionOption, Tuple[_2545.UnbalancedMassInclusionOption, bool]]",
    ) -> None:
        wrapper_type = (
            overridable.Overridable_UnbalancedMassInclusionOption.wrapper_type()
        )
        enclosed_type = (
            overridable.Overridable_UnbalancedMassInclusionOption.implicit_type()
        )
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UnbalancedMassInclusion", value)

    @property
    def advanced_system_deflection_options(
        self: "Self",
    ) -> "_7214.AdvancedSystemDeflectionOptions":
        """mastapy.system_model.analyses_and_results.advanced_system_deflections.AdvancedSystemDeflectionOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdvancedSystemDeflectionOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def harmonic_analysis_options(self: "Self") -> "_5887.HarmonicAnalysisOptions":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def harmonic_analysis_options_for_atsam(
        self: "Self",
    ) -> "_7008.HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation":
        """mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysisOptionsForATSAM")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def te_set_up_for_dynamic_analyses_options(
        self: "Self",
    ) -> "_2755.TESetUpForDynamicAnalysisOptions":
        """mastapy.system_model.analyses_and_results.TESetUpForDynamicAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TESetUpForDynamicAnalysesOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def clutch_engagements(self: "Self") -> "List[_5781.ClutchEngagementStatus]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.ClutchEngagementStatus]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClutchEngagements")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def concept_clutch_engagements(
        self: "Self",
    ) -> "List[_5782.ConceptSynchroGearEngagementStatus]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.ConceptSynchroGearEngagementStatus]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptClutchEngagements")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def advanced_system_deflection(self: "Self") -> "_7213.AdvancedSystemDeflection":
        """mastapy.system_model.analyses_and_results.advanced_system_deflections.AdvancedSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdvancedSystemDeflection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def advanced_time_stepping_analysis_for_modulation(
        self: "Self",
    ) -> "_6945.AdvancedTimeSteppingAnalysisForModulation":
        """mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.AdvancedTimeSteppingAnalysisForModulation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AdvancedTimeSteppingAnalysisForModulation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def critical_speed_analysis(self: "Self") -> "_6716.CriticalSpeedAnalysis":
        """mastapy.system_model.analyses_and_results.critical_speed_analyses.CriticalSpeedAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CriticalSpeedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def design_state_load_case_group(self: "Self") -> "_5783.DesignState":
        """mastapy.system_model.analyses_and_results.load_case_groups.DesignState

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignStateLoadCaseGroup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def harmonic_analysis(self: "Self") -> "_5882.HarmonicAnalysis":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def harmonic_analysis_for_advanced_time_stepping_analysis_for_modulation(
        self: "Self",
    ) -> "_5886.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def modal_analysis(self: "Self") -> "_4757.ModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ModalAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow(self: "Self") -> "_4216.PowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.PowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlow")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stability_analysis(self: "Self") -> "_3960.StabilityAnalysis":
        """mastapy.system_model.analyses_and_results.stability_analyses.StabilityAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StabilityAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def steady_state_synchronous_response(
        self: "Self",
    ) -> "_3167.SteadyStateSynchronousResponse":
        """mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.SteadyStateSynchronousResponse

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SteadyStateSynchronousResponse")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection(self: "Self") -> "_2899.SystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.SystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def analysis_of(
        self: "Self", analysis_type: "_7503.AnalysisType"
    ) -> "_7694.AnalysisCase":
        """mastapy.system_model.analyses_and_results.analysis_cases.AnalysisCase

        Args:
            analysis_type (mastapy.system_model.analyses_and_results.static_loads.AnalysisType)
        """
        analysis_type = conversion.mp_to_pn_enum(
            analysis_type,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.AnalysisType",
        )
        method_result = pythonnet_method_call(self.wrapped, "AnalysisOf", analysis_type)
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def create_time_series_load_case(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateTimeSeriesLoadCase")

    def run_power_flow(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RunPowerFlow")

    def set_face_widths_for_specified_safety_factors_from_power_flow(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "SetFaceWidthsForSpecifiedSafetyFactorsFromPowerFlow"
        )

    @enforce_parameter_types
    def duplicate(
        self: "Self", new_design_state_group: "_5783.DesignState", name: "str" = "None"
    ) -> "StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Args:
            new_design_state_group (mastapy.system_model.analyses_and_results.load_case_groups.DesignState)
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "Duplicate",
            new_design_state_group.wrapped if new_design_state_group else None,
            name if name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_StaticLoadCase":
        """Cast to another type.

        Returns:
            _Cast_StaticLoadCase
        """
        return _Cast_StaticLoadCase(self)
