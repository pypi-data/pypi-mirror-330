"""FaceGearSetLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.load_case import _905

_FACE_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.Gears.LoadCase.Face", "FaceGearSetLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1265, _1274

    Self = TypeVar("Self", bound="FaceGearSetLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="FaceGearSetLoadCase._Cast_FaceGearSetLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearSetLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearSetLoadCase:
    """Special nested class for casting FaceGearSetLoadCase to subclasses."""

    __parent__: "FaceGearSetLoadCase"

    @property
    def gear_set_load_case_base(self: "CastSelf") -> "_905.GearSetLoadCaseBase":
        return self.__parent__._cast(_905.GearSetLoadCaseBase)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1274.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1274

        return self.__parent__._cast(_1274.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1265.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1265

        return self.__parent__._cast(_1265.AbstractGearSetAnalysis)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "FaceGearSetLoadCase":
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
class FaceGearSetLoadCase(_905.GearSetLoadCaseBase):
    """FaceGearSetLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_SET_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearSetLoadCase":
        """Cast to another type.

        Returns:
            _Cast_FaceGearSetLoadCase
        """
        return _Cast_FaceGearSetLoadCase(self)
