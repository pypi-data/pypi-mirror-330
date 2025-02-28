"""NeedleRollerBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs.rolling import _2211

_NEEDLE_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "NeedleRollerBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2192, _2193, _2196
    from mastapy._private.bearings.bearing_designs.rolling import _2223, _2224, _2227

    Self = TypeVar("Self", bound="NeedleRollerBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="NeedleRollerBearing._Cast_NeedleRollerBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("NeedleRollerBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NeedleRollerBearing:
    """Special nested class for casting NeedleRollerBearing to subclasses."""

    __parent__: "NeedleRollerBearing"

    @property
    def cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2211.CylindricalRollerBearing":
        return self.__parent__._cast(_2211.CylindricalRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2223.NonBarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2223

        return self.__parent__._cast(_2223.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2224.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2224

        return self.__parent__._cast(_2224.RollerBearing)

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
    def needle_roller_bearing(self: "CastSelf") -> "NeedleRollerBearing":
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
class NeedleRollerBearing(_2211.CylindricalRollerBearing):
    """NeedleRollerBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NEEDLE_ROLLER_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NeedleRollerBearing":
        """Cast to another type.

        Returns:
            _Cast_NeedleRollerBearing
        """
        return _Cast_NeedleRollerBearing(self)
