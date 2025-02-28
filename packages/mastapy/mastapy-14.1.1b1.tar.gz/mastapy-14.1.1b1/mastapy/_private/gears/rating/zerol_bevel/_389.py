"""ZerolBevelGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.bevel import _574

_ZEROL_BEVEL_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.ZerolBevel", "ZerolBevelGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1263
    from mastapy._private.gears.gear_designs.zerol_bevel import _984
    from mastapy._private.gears.rating import _372, _380
    from mastapy._private.gears.rating.agma_gleason_conical import _585
    from mastapy._private.gears.rating.conical import _559

    Self = TypeVar("Self", bound="ZerolBevelGearRating")
    CastSelf = TypeVar(
        "CastSelf", bound="ZerolBevelGearRating._Cast_ZerolBevelGearRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearRating:
    """Special nested class for casting ZerolBevelGearRating to subclasses."""

    __parent__: "ZerolBevelGearRating"

    @property
    def bevel_gear_rating(self: "CastSelf") -> "_574.BevelGearRating":
        return self.__parent__._cast(_574.BevelGearRating)

    @property
    def agma_gleason_conical_gear_rating(
        self: "CastSelf",
    ) -> "_585.AGMAGleasonConicalGearRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _585

        return self.__parent__._cast(_585.AGMAGleasonConicalGearRating)

    @property
    def conical_gear_rating(self: "CastSelf") -> "_559.ConicalGearRating":
        from mastapy._private.gears.rating.conical import _559

        return self.__parent__._cast(_559.ConicalGearRating)

    @property
    def gear_rating(self: "CastSelf") -> "_380.GearRating":
        from mastapy._private.gears.rating import _380

        return self.__parent__._cast(_380.GearRating)

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_372.AbstractGearRating":
        from mastapy._private.gears.rating import _372

        return self.__parent__._cast(_372.AbstractGearRating)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1263.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1263

        return self.__parent__._cast(_1263.AbstractGearAnalysis)

    @property
    def zerol_bevel_gear_rating(self: "CastSelf") -> "ZerolBevelGearRating":
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
class ZerolBevelGearRating(_574.BevelGearRating):
    """ZerolBevelGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def zerol_bevel_gear(self: "Self") -> "_984.ZerolBevelGearDesign":
        """mastapy.gears.gear_designs.zerol_bevel.ZerolBevelGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ZerolBevelGearRating":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearRating
        """
        return _Cast_ZerolBevelGearRating(self)
