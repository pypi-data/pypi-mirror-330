"""AngularContactThrustBallBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_designs.rolling import _2197

_ANGULAR_CONTACT_THRUST_BALL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "AngularContactThrustBallBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2192, _2193, _2196
    from mastapy._private.bearings.bearing_designs.rolling import _2202, _2227

    Self = TypeVar("Self", bound="AngularContactThrustBallBearing")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AngularContactThrustBallBearing._Cast_AngularContactThrustBallBearing",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AngularContactThrustBallBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AngularContactThrustBallBearing:
    """Special nested class for casting AngularContactThrustBallBearing to subclasses."""

    __parent__: "AngularContactThrustBallBearing"

    @property
    def angular_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2197.AngularContactBallBearing":
        return self.__parent__._cast(_2197.AngularContactBallBearing)

    @property
    def ball_bearing(self: "CastSelf") -> "_2202.BallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2202

        return self.__parent__._cast(_2202.BallBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2227.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2227

        return self.__parent__._cast(_2227.RollingBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2193.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2193

        return self.__parent__._cast(_2193.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2196.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2196

        return self.__parent__._cast(_2196.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2192.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2192

        return self.__parent__._cast(_2192.BearingDesign)

    @property
    def angular_contact_thrust_ball_bearing(
        self: "CastSelf",
    ) -> "AngularContactThrustBallBearing":
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
class AngularContactThrustBallBearing(_2197.AngularContactBallBearing):
    """AngularContactThrustBallBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ANGULAR_CONTACT_THRUST_BALL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AngularContactThrustBallBearing":
        """Cast to another type.

        Returns:
            _Cast_AngularContactThrustBallBearing
        """
        return _Cast_AngularContactThrustBallBearing(self)
