"""ConicalGearSetRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _382

_CONICAL_GEAR_SET_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Conical", "ConicalGearSetRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1265
    from mastapy._private.gears.gear_designs import _975
    from mastapy._private.gears.rating import _373
    from mastapy._private.gears.rating.agma_gleason_conical import _586
    from mastapy._private.gears.rating.bevel import _575
    from mastapy._private.gears.rating.hypoid import _459
    from mastapy._private.gears.rating.klingelnberg_conical import _432
    from mastapy._private.gears.rating.klingelnberg_hypoid import _429
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _426
    from mastapy._private.gears.rating.spiral_bevel import _423
    from mastapy._private.gears.rating.straight_bevel import _416
    from mastapy._private.gears.rating.straight_bevel_diff import _419
    from mastapy._private.gears.rating.zerol_bevel import _390

    Self = TypeVar("Self", bound="ConicalGearSetRating")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalGearSetRating._Cast_ConicalGearSetRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetRating:
    """Special nested class for casting ConicalGearSetRating to subclasses."""

    __parent__: "ConicalGearSetRating"

    @property
    def gear_set_rating(self: "CastSelf") -> "_382.GearSetRating":
        return self.__parent__._cast(_382.GearSetRating)

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_373.AbstractGearSetRating":
        from mastapy._private.gears.rating import _373

        return self.__parent__._cast(_373.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1265.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1265

        return self.__parent__._cast(_1265.AbstractGearSetAnalysis)

    @property
    def zerol_bevel_gear_set_rating(self: "CastSelf") -> "_390.ZerolBevelGearSetRating":
        from mastapy._private.gears.rating.zerol_bevel import _390

        return self.__parent__._cast(_390.ZerolBevelGearSetRating)

    @property
    def straight_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_416.StraightBevelGearSetRating":
        from mastapy._private.gears.rating.straight_bevel import _416

        return self.__parent__._cast(_416.StraightBevelGearSetRating)

    @property
    def straight_bevel_diff_gear_set_rating(
        self: "CastSelf",
    ) -> "_419.StraightBevelDiffGearSetRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _419

        return self.__parent__._cast(_419.StraightBevelDiffGearSetRating)

    @property
    def spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_423.SpiralBevelGearSetRating":
        from mastapy._private.gears.rating.spiral_bevel import _423

        return self.__parent__._cast(_423.SpiralBevelGearSetRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_426.KlingelnbergCycloPalloidSpiralBevelGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _426

        return self.__parent__._cast(
            _426.KlingelnbergCycloPalloidSpiralBevelGearSetRating
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_rating(
        self: "CastSelf",
    ) -> "_429.KlingelnbergCycloPalloidHypoidGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _429

        return self.__parent__._cast(_429.KlingelnbergCycloPalloidHypoidGearSetRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_432.KlingelnbergCycloPalloidConicalGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _432

        return self.__parent__._cast(_432.KlingelnbergCycloPalloidConicalGearSetRating)

    @property
    def hypoid_gear_set_rating(self: "CastSelf") -> "_459.HypoidGearSetRating":
        from mastapy._private.gears.rating.hypoid import _459

        return self.__parent__._cast(_459.HypoidGearSetRating)

    @property
    def bevel_gear_set_rating(self: "CastSelf") -> "_575.BevelGearSetRating":
        from mastapy._private.gears.rating.bevel import _575

        return self.__parent__._cast(_575.BevelGearSetRating)

    @property
    def agma_gleason_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_586.AGMAGleasonConicalGearSetRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _586

        return self.__parent__._cast(_586.AGMAGleasonConicalGearSetRating)

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "ConicalGearSetRating":
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
class ConicalGearSetRating(_382.GearSetRating):
    """ConicalGearSetRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rating_settings(self: "Self") -> "_975.BevelHypoidGearRatingSettingsItem":
        """mastapy.gears.gear_designs.BevelHypoidGearRatingSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSetRating":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetRating
        """
        return _Cast_ConicalGearSetRating(self)
