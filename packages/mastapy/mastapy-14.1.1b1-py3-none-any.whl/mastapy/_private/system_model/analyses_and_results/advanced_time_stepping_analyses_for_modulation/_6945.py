"""AdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7696

_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "AdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2722
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7694,
        _7709,
    )

    Self = TypeVar("Self", bound="AdvancedTimeSteppingAnalysisForModulation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AdvancedTimeSteppingAnalysisForModulation._Cast_AdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting AdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "AdvancedTimeSteppingAnalysisForModulation"

    @property
    def compound_analysis_case(self: "CastSelf") -> "_7696.CompoundAnalysisCase":
        return self.__parent__._cast(_7696.CompoundAnalysisCase)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7709.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7709,
        )

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
    def advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "AdvancedTimeSteppingAnalysisForModulation":
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
class AdvancedTimeSteppingAnalysisForModulation(_7696.CompoundAnalysisCase):
    """AdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_AdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_AdvancedTimeSteppingAnalysisForModulation(self)
