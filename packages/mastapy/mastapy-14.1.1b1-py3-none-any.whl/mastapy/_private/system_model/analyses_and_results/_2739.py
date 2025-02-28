"""CompoundDynamicModelForSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results import _2719

_COMPOUND_DYNAMIC_MODEL_FOR_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults",
    "CompoundDynamicModelForSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private import _7712

    Self = TypeVar(
        "Self", bound="CompoundDynamicModelForSteadyStateSynchronousResponse"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CompoundDynamicModelForSteadyStateSynchronousResponse._Cast_CompoundDynamicModelForSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CompoundDynamicModelForSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CompoundDynamicModelForSteadyStateSynchronousResponse:
    """Special nested class for casting CompoundDynamicModelForSteadyStateSynchronousResponse to subclasses."""

    __parent__: "CompoundDynamicModelForSteadyStateSynchronousResponse"

    @property
    def compound_analysis(self: "CastSelf") -> "_2719.CompoundAnalysis":
        return self.__parent__._cast(_2719.CompoundAnalysis)

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7712.MarshalByRefObjectPermanent":
        from mastapy._private import _7712

        return self.__parent__._cast(_7712.MarshalByRefObjectPermanent)

    @property
    def compound_dynamic_model_for_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "CompoundDynamicModelForSteadyStateSynchronousResponse":
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
class CompoundDynamicModelForSteadyStateSynchronousResponse(_2719.CompoundAnalysis):
    """CompoundDynamicModelForSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _COMPOUND_DYNAMIC_MODEL_FOR_STEADY_STATE_SYNCHRONOUS_RESPONSE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CompoundDynamicModelForSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_CompoundDynamicModelForSteadyStateSynchronousResponse
        """
        return _Cast_CompoundDynamicModelForSteadyStateSynchronousResponse(self)
