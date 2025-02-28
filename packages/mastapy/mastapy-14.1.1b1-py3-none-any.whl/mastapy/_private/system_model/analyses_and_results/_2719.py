"""CompoundAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _7712
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_TASK_PROGRESS = python_net_import("SMT.MastaAPIUtility", "TaskProgress")
_COMPOUND_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "CompoundAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Iterable, Type, TypeVar

    from mastapy._private import _7718
    from mastapy._private.system_model import _2266
    from mastapy._private.system_model.analyses_and_results import (
        _2730,
        _2731,
        _2732,
        _2733,
        _2734,
        _2735,
        _2736,
        _2737,
        _2738,
        _2739,
        _2740,
        _2741,
        _2742,
        _2743,
        _2744,
        _2745,
        _2746,
        _2747,
        _2748,
        _2749,
        _2750,
        _2751,
        _2752,
        _2753,
        _2754,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7702

    Self = TypeVar("Self", bound="CompoundAnalysis")
    CastSelf = TypeVar("CastSelf", bound="CompoundAnalysis._Cast_CompoundAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("CompoundAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CompoundAnalysis:
    """Special nested class for casting CompoundAnalysis to subclasses."""

    __parent__: "CompoundAnalysis"

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7712.MarshalByRefObjectPermanent":
        return self.__parent__._cast(_7712.MarshalByRefObjectPermanent)

    @property
    def compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_2730.CompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results import _2730

        return self.__parent__._cast(_2730.CompoundAdvancedSystemDeflection)

    @property
    def compound_advanced_system_deflection_sub_analysis(
        self: "CastSelf",
    ) -> "_2731.CompoundAdvancedSystemDeflectionSubAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2731

        return self.__parent__._cast(_2731.CompoundAdvancedSystemDeflectionSubAnalysis)

    @property
    def compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_2732.CompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results import _2732

        return self.__parent__._cast(
            _2732.CompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_2733.CompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2733

        return self.__parent__._cast(_2733.CompoundCriticalSpeedAnalysis)

    @property
    def compound_dynamic_analysis(self: "CastSelf") -> "_2734.CompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2734

        return self.__parent__._cast(_2734.CompoundDynamicAnalysis)

    @property
    def compound_dynamic_model_at_a_stiffness(
        self: "CastSelf",
    ) -> "_2735.CompoundDynamicModelAtAStiffness":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.CompoundDynamicModelAtAStiffness)

    @property
    def compound_dynamic_model_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_2736.CompoundDynamicModelForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2736

        return self.__parent__._cast(_2736.CompoundDynamicModelForHarmonicAnalysis)

    @property
    def compound_dynamic_model_for_modal_analysis(
        self: "CastSelf",
    ) -> "_2737.CompoundDynamicModelForModalAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2737

        return self.__parent__._cast(_2737.CompoundDynamicModelForModalAnalysis)

    @property
    def compound_dynamic_model_for_stability_analysis(
        self: "CastSelf",
    ) -> "_2738.CompoundDynamicModelForStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.CompoundDynamicModelForStabilityAnalysis)

    @property
    def compound_dynamic_model_for_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_2739.CompoundDynamicModelForSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results import _2739

        return self.__parent__._cast(
            _2739.CompoundDynamicModelForSteadyStateSynchronousResponse
        )

    @property
    def compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_2740.CompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.CompoundHarmonicAnalysis)

    @property
    def compound_harmonic_analysis_for_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_2741.CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results import _2741

        return self.__parent__._cast(
            _2741.CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_2742.CompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results import _2742

        return self.__parent__._cast(_2742.CompoundHarmonicAnalysisOfSingleExcitation)

    @property
    def compound_modal_analysis(self: "CastSelf") -> "_2743.CompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2743

        return self.__parent__._cast(_2743.CompoundModalAnalysis)

    @property
    def compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_2744.CompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results import _2744

        return self.__parent__._cast(_2744.CompoundModalAnalysisAtASpeed)

    @property
    def compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_2745.CompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results import _2745

        return self.__parent__._cast(_2745.CompoundModalAnalysisAtAStiffness)

    @property
    def compound_modal_analysis_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_2746.CompoundModalAnalysisForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2746

        return self.__parent__._cast(_2746.CompoundModalAnalysisForHarmonicAnalysis)

    @property
    def compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_2747.CompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2747

        return self.__parent__._cast(_2747.CompoundMultibodyDynamicsAnalysis)

    @property
    def compound_power_flow(self: "CastSelf") -> "_2748.CompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results import _2748

        return self.__parent__._cast(_2748.CompoundPowerFlow)

    @property
    def compound_stability_analysis(
        self: "CastSelf",
    ) -> "_2749.CompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2749

        return self.__parent__._cast(_2749.CompoundStabilityAnalysis)

    @property
    def compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_2750.CompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results import _2750

        return self.__parent__._cast(_2750.CompoundSteadyStateSynchronousResponse)

    @property
    def compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_2751.CompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results import _2751

        return self.__parent__._cast(
            _2751.CompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_2752.CompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results import _2752

        return self.__parent__._cast(
            _2752.CompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def compound_system_deflection(
        self: "CastSelf",
    ) -> "_2753.CompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results import _2753

        return self.__parent__._cast(_2753.CompoundSystemDeflection)

    @property
    def compound_torsional_system_deflection(
        self: "CastSelf",
    ) -> "_2754.CompoundTorsionalSystemDeflection":
        from mastapy._private.system_model.analyses_and_results import _2754

        return self.__parent__._cast(_2754.CompoundTorsionalSystemDeflection)

    @property
    def compound_analysis(self: "CastSelf") -> "CompoundAnalysis":
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
class CompoundAnalysis(_7712.MarshalByRefObjectPermanent):
    """CompoundAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPOUND_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def results_ready(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsReady")

        if temp is None:
            return False

        return temp

    def perform_analysis(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PerformAnalysis")

    @enforce_parameter_types
    def perform_analysis_with_progress(
        self: "Self", progress: "_7718.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            progress (mastapy.TaskProgress)
        """
        pythonnet_method_call_overload(
            self.wrapped,
            "PerformAnalysis",
            [_TASK_PROGRESS],
            progress.wrapped if progress else None,
        )

    @enforce_parameter_types
    def results_for(
        self: "Self", design_entity: "_2266.DesignEntity"
    ) -> "Iterable[_7702.DesignEntityCompoundAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.analysis_cases.DesignEntityCompoundAnalysis]

        Args:
            design_entity (mastapy.system_model.DesignEntity)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call(
                self.wrapped,
                "ResultsFor",
                design_entity.wrapped if design_entity else None,
            )
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CompoundAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CompoundAnalysis
        """
        return _Cast_CompoundAnalysis(self)
