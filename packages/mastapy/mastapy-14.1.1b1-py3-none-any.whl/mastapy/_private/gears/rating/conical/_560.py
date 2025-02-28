"""ConicalGearSetDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _381

_CONICAL_GEAR_SET_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Conical", "ConicalGearSetDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1265
    from mastapy._private.gears.rating import _373
    from mastapy._private.gears.rating.conical import _563

    Self = TypeVar("Self", bound="ConicalGearSetDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSetDutyCycleRating._Cast_ConicalGearSetDutyCycleRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetDutyCycleRating:
    """Special nested class for casting ConicalGearSetDutyCycleRating to subclasses."""

    __parent__: "ConicalGearSetDutyCycleRating"

    @property
    def gear_set_duty_cycle_rating(self: "CastSelf") -> "_381.GearSetDutyCycleRating":
        return self.__parent__._cast(_381.GearSetDutyCycleRating)

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_373.AbstractGearSetRating":
        from mastapy._private.gears.rating import _373

        return self.__parent__._cast(_373.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1265.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1265

        return self.__parent__._cast(_1265.AbstractGearSetAnalysis)

    @property
    def conical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "ConicalGearSetDutyCycleRating":
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
class ConicalGearSetDutyCycleRating(_381.GearSetDutyCycleRating):
    """ConicalGearSetDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def gear_mesh_duty_cycle_ratings(
        self: "Self",
    ) -> "List[_563.ConicalMeshDutyCycleRating]":
        """List[mastapy.gears.rating.conical.ConicalMeshDutyCycleRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMeshDutyCycleRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def conical_mesh_duty_cycle_ratings(
        self: "Self",
    ) -> "List[_563.ConicalMeshDutyCycleRating]":
        """List[mastapy.gears.rating.conical.ConicalMeshDutyCycleRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshDutyCycleRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSetDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetDutyCycleRating
        """
        return _Cast_ConicalGearSetDutyCycleRating(self)
