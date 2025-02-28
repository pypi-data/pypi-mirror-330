"""AbstractAssembly"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model import _2534

_ABSTRACT_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractAssembly"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2266
    from mastapy._private.system_model.part_model import (
        _2497,
        _2507,
        _2508,
        _2518,
        _2529,
        _2541,
        _2543,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2646,
        _2648,
        _2651,
        _2654,
        _2657,
        _2659,
        _2670,
        _2677,
        _2679,
        _2684,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2637
    from mastapy._private.system_model.part_model.gears import (
        _2583,
        _2585,
        _2589,
        _2591,
        _2593,
        _2595,
        _2598,
        _2601,
        _2604,
        _2606,
        _2608,
        _2610,
        _2611,
        _2613,
        _2615,
        _2617,
        _2621,
        _2623,
    )

    Self = TypeVar("Self", bound="AbstractAssembly")
    CastSelf = TypeVar("CastSelf", bound="AbstractAssembly._Cast_AbstractAssembly")


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssembly:
    """Special nested class for casting AbstractAssembly to subclasses."""

    __parent__: "AbstractAssembly"

    @property
    def part(self: "CastSelf") -> "_2534.Part":
        return self.__parent__._cast(_2534.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2266.DesignEntity":
        from mastapy._private.system_model import _2266

        return self.__parent__._cast(_2266.DesignEntity)

    @property
    def assembly(self: "CastSelf") -> "_2497.Assembly":
        from mastapy._private.system_model.part_model import _2497

        return self.__parent__._cast(_2497.Assembly)

    @property
    def bolted_joint(self: "CastSelf") -> "_2507.BoltedJoint":
        from mastapy._private.system_model.part_model import _2507

        return self.__parent__._cast(_2507.BoltedJoint)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2518.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2518

        return self.__parent__._cast(_2518.FlexiblePinAssembly)

    @property
    def microphone_array(self: "CastSelf") -> "_2529.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2529

        return self.__parent__._cast(_2529.MicrophoneArray)

    @property
    def root_assembly(self: "CastSelf") -> "_2541.RootAssembly":
        from mastapy._private.system_model.part_model import _2541

        return self.__parent__._cast(_2541.RootAssembly)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2543.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2543

        return self.__parent__._cast(_2543.SpecialisedAssembly)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2583.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2583

        return self.__parent__._cast(_2583.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2585.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2585

        return self.__parent__._cast(_2585.BevelDifferentialGearSet)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2589.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2589

        return self.__parent__._cast(_2589.BevelGearSet)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2591.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2591

        return self.__parent__._cast(_2591.ConceptGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2593.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2593

        return self.__parent__._cast(_2593.ConicalGearSet)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2595.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2595

        return self.__parent__._cast(_2595.CylindricalGearSet)

    @property
    def face_gear_set(self: "CastSelf") -> "_2598.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2598

        return self.__parent__._cast(_2598.FaceGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2601.GearSet":
        from mastapy._private.system_model.part_model.gears import _2601

        return self.__parent__._cast(_2601.GearSet)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2604.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2604

        return self.__parent__._cast(_2604.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2606.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2606

        return self.__parent__._cast(_2606.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2608.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2608

        return self.__parent__._cast(_2608.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2610.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2610

        return self.__parent__._cast(_2610.KlingelnbergCycloPalloidSpiralBevelGearSet)

    @property
    def planetary_gear_set(self: "CastSelf") -> "_2611.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2611

        return self.__parent__._cast(_2611.PlanetaryGearSet)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2613.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2613

        return self.__parent__._cast(_2613.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2615.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2615

        return self.__parent__._cast(_2615.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2617.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2617

        return self.__parent__._cast(_2617.StraightBevelGearSet)

    @property
    def worm_gear_set(self: "CastSelf") -> "_2621.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2621

        return self.__parent__._cast(_2621.WormGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2623.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2623

        return self.__parent__._cast(_2623.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2637.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2637

        return self.__parent__._cast(_2637.CycloidalAssembly)

    @property
    def belt_drive(self: "CastSelf") -> "_2646.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2646

        return self.__parent__._cast(_2646.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2648.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2648

        return self.__parent__._cast(_2648.Clutch)

    @property
    def concept_coupling(self: "CastSelf") -> "_2651.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2651

        return self.__parent__._cast(_2651.ConceptCoupling)

    @property
    def coupling(self: "CastSelf") -> "_2654.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2654

        return self.__parent__._cast(_2654.Coupling)

    @property
    def cvt(self: "CastSelf") -> "_2657.CVT":
        from mastapy._private.system_model.part_model.couplings import _2657

        return self.__parent__._cast(_2657.CVT)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2659.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2659

        return self.__parent__._cast(_2659.PartToPartShearCoupling)

    @property
    def rolling_ring_assembly(self: "CastSelf") -> "_2670.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2670

        return self.__parent__._cast(_2670.RollingRingAssembly)

    @property
    def spring_damper(self: "CastSelf") -> "_2677.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2677

        return self.__parent__._cast(_2677.SpringDamper)

    @property
    def synchroniser(self: "CastSelf") -> "_2679.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2679

        return self.__parent__._cast(_2679.Synchroniser)

    @property
    def torque_converter(self: "CastSelf") -> "_2684.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2684

        return self.__parent__._cast(_2684.TorqueConverter)

    @property
    def abstract_assembly(self: "CastSelf") -> "AbstractAssembly":
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
class AbstractAssembly(_2534.Part):
    """AbstractAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def mass_of_assembly(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassOfAssembly")

        if temp is None:
            return 0.0

        return temp

    @property
    def components_with_unknown_mass_properties(
        self: "Self",
    ) -> "List[_2508.Component]":
        """List[mastapy.system_model.part_model.Component]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ComponentsWithUnknownMassProperties"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def components_with_zero_mass_properties(self: "Self") -> "List[_2508.Component]":
        """List[mastapy.system_model.part_model.Component]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentsWithZeroMassProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractAssembly":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssembly
        """
        return _Cast_AbstractAssembly(self)
