"""AGMAGleasonConicalGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.gears import _2592

_AGMA_GLEASON_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2266
    from mastapy._private.system_model.part_model import _2508, _2530, _2534
    from mastapy._private.system_model.part_model.gears import (
        _2584,
        _2586,
        _2587,
        _2588,
        _2599,
        _2603,
        _2612,
        _2614,
        _2616,
        _2618,
        _2619,
        _2622,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGear")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGear:
    """Special nested class for casting AGMAGleasonConicalGear to subclasses."""

    __parent__: "AGMAGleasonConicalGear"

    @property
    def conical_gear(self: "CastSelf") -> "_2592.ConicalGear":
        return self.__parent__._cast(_2592.ConicalGear)

    @property
    def gear(self: "CastSelf") -> "_2599.Gear":
        from mastapy._private.system_model.part_model.gears import _2599

        return self.__parent__._cast(_2599.Gear)

    @property
    def mountable_component(self: "CastSelf") -> "_2530.MountableComponent":
        from mastapy._private.system_model.part_model import _2530

        return self.__parent__._cast(_2530.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2508.Component":
        from mastapy._private.system_model.part_model import _2508

        return self.__parent__._cast(_2508.Component)

    @property
    def part(self: "CastSelf") -> "_2534.Part":
        from mastapy._private.system_model.part_model import _2534

        return self.__parent__._cast(_2534.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2266.DesignEntity":
        from mastapy._private.system_model import _2266

        return self.__parent__._cast(_2266.DesignEntity)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2584.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2584

        return self.__parent__._cast(_2584.BevelDifferentialGear)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2586.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2586

        return self.__parent__._cast(_2586.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2587.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2587

        return self.__parent__._cast(_2587.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2588.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2588

        return self.__parent__._cast(_2588.BevelGear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2603.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2603

        return self.__parent__._cast(_2603.HypoidGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2612.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2612

        return self.__parent__._cast(_2612.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2614.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2614

        return self.__parent__._cast(_2614.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2616.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2616

        return self.__parent__._cast(_2616.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2618.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2618

        return self.__parent__._cast(_2618.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2619.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2619

        return self.__parent__._cast(_2619.StraightBevelSunGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2622.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2622

        return self.__parent__._cast(_2622.ZerolBevelGear)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "AGMAGleasonConicalGear":
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
class AGMAGleasonConicalGear(_2592.ConicalGear):
    """AGMAGleasonConicalGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGear":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGear
        """
        return _Cast_AGMAGleasonConicalGear(self)
