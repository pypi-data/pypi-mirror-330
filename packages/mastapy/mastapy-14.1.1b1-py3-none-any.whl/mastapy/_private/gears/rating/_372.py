"""AbstractGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1263

_ABSTRACT_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "AbstractGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _376, _380
    from mastapy._private.gears.rating.agma_gleason_conical import _585
    from mastapy._private.gears.rating.bevel import _574
    from mastapy._private.gears.rating.concept import _567, _570
    from mastapy._private.gears.rating.conical import _557, _559
    from mastapy._private.gears.rating.cylindrical import _474, _479
    from mastapy._private.gears.rating.face import _464, _467
    from mastapy._private.gears.rating.hypoid import _458
    from mastapy._private.gears.rating.klingelnberg_conical import _431
    from mastapy._private.gears.rating.klingelnberg_hypoid import _428
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _425
    from mastapy._private.gears.rating.spiral_bevel import _422
    from mastapy._private.gears.rating.straight_bevel import _415
    from mastapy._private.gears.rating.straight_bevel_diff import _418
    from mastapy._private.gears.rating.worm import _391, _393
    from mastapy._private.gears.rating.zerol_bevel import _389

    Self = TypeVar("Self", bound="AbstractGearRating")
    CastSelf = TypeVar("CastSelf", bound="AbstractGearRating._Cast_AbstractGearRating")


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearRating:
    """Special nested class for casting AbstractGearRating to subclasses."""

    __parent__: "AbstractGearRating"

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1263.AbstractGearAnalysis":
        return self.__parent__._cast(_1263.AbstractGearAnalysis)

    @property
    def gear_duty_cycle_rating(self: "CastSelf") -> "_376.GearDutyCycleRating":
        from mastapy._private.gears.rating import _376

        return self.__parent__._cast(_376.GearDutyCycleRating)

    @property
    def gear_rating(self: "CastSelf") -> "_380.GearRating":
        from mastapy._private.gears.rating import _380

        return self.__parent__._cast(_380.GearRating)

    @property
    def zerol_bevel_gear_rating(self: "CastSelf") -> "_389.ZerolBevelGearRating":
        from mastapy._private.gears.rating.zerol_bevel import _389

        return self.__parent__._cast(_389.ZerolBevelGearRating)

    @property
    def worm_gear_duty_cycle_rating(self: "CastSelf") -> "_391.WormGearDutyCycleRating":
        from mastapy._private.gears.rating.worm import _391

        return self.__parent__._cast(_391.WormGearDutyCycleRating)

    @property
    def worm_gear_rating(self: "CastSelf") -> "_393.WormGearRating":
        from mastapy._private.gears.rating.worm import _393

        return self.__parent__._cast(_393.WormGearRating)

    @property
    def straight_bevel_gear_rating(self: "CastSelf") -> "_415.StraightBevelGearRating":
        from mastapy._private.gears.rating.straight_bevel import _415

        return self.__parent__._cast(_415.StraightBevelGearRating)

    @property
    def straight_bevel_diff_gear_rating(
        self: "CastSelf",
    ) -> "_418.StraightBevelDiffGearRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _418

        return self.__parent__._cast(_418.StraightBevelDiffGearRating)

    @property
    def spiral_bevel_gear_rating(self: "CastSelf") -> "_422.SpiralBevelGearRating":
        from mastapy._private.gears.rating.spiral_bevel import _422

        return self.__parent__._cast(_422.SpiralBevelGearRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_rating(
        self: "CastSelf",
    ) -> "_425.KlingelnbergCycloPalloidSpiralBevelGearRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _425

        return self.__parent__._cast(_425.KlingelnbergCycloPalloidSpiralBevelGearRating)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_rating(
        self: "CastSelf",
    ) -> "_428.KlingelnbergCycloPalloidHypoidGearRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _428

        return self.__parent__._cast(_428.KlingelnbergCycloPalloidHypoidGearRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_rating(
        self: "CastSelf",
    ) -> "_431.KlingelnbergCycloPalloidConicalGearRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _431

        return self.__parent__._cast(_431.KlingelnbergCycloPalloidConicalGearRating)

    @property
    def hypoid_gear_rating(self: "CastSelf") -> "_458.HypoidGearRating":
        from mastapy._private.gears.rating.hypoid import _458

        return self.__parent__._cast(_458.HypoidGearRating)

    @property
    def face_gear_duty_cycle_rating(self: "CastSelf") -> "_464.FaceGearDutyCycleRating":
        from mastapy._private.gears.rating.face import _464

        return self.__parent__._cast(_464.FaceGearDutyCycleRating)

    @property
    def face_gear_rating(self: "CastSelf") -> "_467.FaceGearRating":
        from mastapy._private.gears.rating.face import _467

        return self.__parent__._cast(_467.FaceGearRating)

    @property
    def cylindrical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_474.CylindricalGearDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _474

        return self.__parent__._cast(_474.CylindricalGearDutyCycleRating)

    @property
    def cylindrical_gear_rating(self: "CastSelf") -> "_479.CylindricalGearRating":
        from mastapy._private.gears.rating.cylindrical import _479

        return self.__parent__._cast(_479.CylindricalGearRating)

    @property
    def conical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_557.ConicalGearDutyCycleRating":
        from mastapy._private.gears.rating.conical import _557

        return self.__parent__._cast(_557.ConicalGearDutyCycleRating)

    @property
    def conical_gear_rating(self: "CastSelf") -> "_559.ConicalGearRating":
        from mastapy._private.gears.rating.conical import _559

        return self.__parent__._cast(_559.ConicalGearRating)

    @property
    def concept_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_567.ConceptGearDutyCycleRating":
        from mastapy._private.gears.rating.concept import _567

        return self.__parent__._cast(_567.ConceptGearDutyCycleRating)

    @property
    def concept_gear_rating(self: "CastSelf") -> "_570.ConceptGearRating":
        from mastapy._private.gears.rating.concept import _570

        return self.__parent__._cast(_570.ConceptGearRating)

    @property
    def bevel_gear_rating(self: "CastSelf") -> "_574.BevelGearRating":
        from mastapy._private.gears.rating.bevel import _574

        return self.__parent__._cast(_574.BevelGearRating)

    @property
    def agma_gleason_conical_gear_rating(
        self: "CastSelf",
    ) -> "_585.AGMAGleasonConicalGearRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _585

        return self.__parent__._cast(_585.AGMAGleasonConicalGearRating)

    @property
    def abstract_gear_rating(self: "CastSelf") -> "AbstractGearRating":
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
class AbstractGearRating(_1263.AbstractGearAnalysis):
    """AbstractGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bending_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    def bending_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingSafetyFactorForStatic")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactSafetyFactorForStatic")

        if temp is None:
            return 0.0

        return temp

    @property
    def cycles_to_fail(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CyclesToFail")

        if temp is None:
            return 0.0

        return temp

    @property
    def cycles_to_fail_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CyclesToFailBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def cycles_to_fail_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CyclesToFailContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def damage_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def damage_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_reliability_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearReliabilityBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_reliability_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearReliabilityContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_bending_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedBendingSafetyFactorForFatigue"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_bending_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedBendingSafetyFactorForStatic"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_contact_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedContactSafetyFactorForFatigue"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_contact_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedContactSafetyFactorForStatic"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalisedSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalisedSafetyFactorForStatic")

        if temp is None:
            return 0.0

        return temp

    @property
    def time_to_fail(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeToFail")

        if temp is None:
            return 0.0

        return temp

    @property
    def time_to_fail_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeToFailBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def time_to_fail_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeToFailContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_gear_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalGearReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractGearRating":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearRating
        """
        return _Cast_AbstractGearRating(self)
