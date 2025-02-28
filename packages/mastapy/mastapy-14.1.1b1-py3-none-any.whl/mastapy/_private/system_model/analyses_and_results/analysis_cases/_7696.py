"""CompoundAnalysisCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7709

_COMPOUND_ANALYSIS_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases", "CompoundAnalysisCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2722
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _6945,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7694
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5882,
        _5886,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3167,
    )

    Self = TypeVar("Self", bound="CompoundAnalysisCase")
    CastSelf = TypeVar(
        "CastSelf", bound="CompoundAnalysisCase._Cast_CompoundAnalysisCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CompoundAnalysisCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CompoundAnalysisCase:
    """Special nested class for casting CompoundAnalysisCase to subclasses."""

    __parent__: "CompoundAnalysisCase"

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7709.StaticLoadAnalysisCase":
        return self.__parent__._cast(_7709.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7694.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7694,
        )

        return self.__parent__._cast(_7694.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2722.Context":
        from mastapy._private.system_model.analyses_and_results import _2722

        return self.__parent__._cast(_2722.Context)

    @property
    def steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3167.SteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3167,
        )

        return self.__parent__._cast(_3167.SteadyStateSynchronousResponse)

    @property
    def harmonic_analysis(self: "CastSelf") -> "_5882.HarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5882,
        )

        return self.__parent__._cast(_5882.HarmonicAnalysis)

    @property
    def harmonic_analysis_for_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_5886.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5886,
        )

        return self.__parent__._cast(
            _5886.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_6945.AdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _6945,
        )

        return self.__parent__._cast(_6945.AdvancedTimeSteppingAnalysisForModulation)

    @property
    def compound_analysis_case(self: "CastSelf") -> "CompoundAnalysisCase":
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
class CompoundAnalysisCase(_7709.StaticLoadAnalysisCase):
    """CompoundAnalysisCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPOUND_ANALYSIS_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CompoundAnalysisCase":
        """Cast to another type.

        Returns:
            _Cast_CompoundAnalysisCase
        """
        return _Cast_CompoundAnalysisCase(self)
