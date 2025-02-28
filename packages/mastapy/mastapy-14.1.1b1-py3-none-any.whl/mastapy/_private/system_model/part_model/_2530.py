"""MountableComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2508

_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2266
    from mastapy._private.system_model.connections_and_sockets import (
        _2332,
        _2335,
        _2339,
    )
    from mastapy._private.system_model.part_model import (
        _2499,
        _2503,
        _2509,
        _2511,
        _2526,
        _2527,
        _2532,
        _2534,
        _2535,
        _2537,
        _2538,
        _2544,
        _2546,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2649,
        _2652,
        _2655,
        _2658,
        _2660,
        _2662,
        _2669,
        _2671,
        _2678,
        _2681,
        _2682,
        _2683,
        _2685,
        _2687,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2639
    from mastapy._private.system_model.part_model.gears import (
        _2582,
        _2584,
        _2586,
        _2587,
        _2588,
        _2590,
        _2592,
        _2594,
        _2596,
        _2597,
        _2599,
        _2603,
        _2605,
        _2607,
        _2609,
        _2612,
        _2614,
        _2616,
        _2618,
        _2619,
        _2620,
        _2622,
    )

    Self = TypeVar("Self", bound="MountableComponent")
    CastSelf = TypeVar("CastSelf", bound="MountableComponent._Cast_MountableComponent")


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponent:
    """Special nested class for casting MountableComponent to subclasses."""

    __parent__: "MountableComponent"

    @property
    def component(self: "CastSelf") -> "_2508.Component":
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
    def bearing(self: "CastSelf") -> "_2503.Bearing":
        from mastapy._private.system_model.part_model import _2503

        return self.__parent__._cast(_2503.Bearing)

    @property
    def connector(self: "CastSelf") -> "_2511.Connector":
        from mastapy._private.system_model.part_model import _2511

        return self.__parent__._cast(_2511.Connector)

    @property
    def mass_disc(self: "CastSelf") -> "_2526.MassDisc":
        from mastapy._private.system_model.part_model import _2526

        return self.__parent__._cast(_2526.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2527.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2527

        return self.__parent__._cast(_2527.MeasurementComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2532.OilSeal":
        from mastapy._private.system_model.part_model import _2532

        return self.__parent__._cast(_2532.OilSeal)

    @property
    def planet_carrier(self: "CastSelf") -> "_2535.PlanetCarrier":
        from mastapy._private.system_model.part_model import _2535

        return self.__parent__._cast(_2535.PlanetCarrier)

    @property
    def point_load(self: "CastSelf") -> "_2537.PointLoad":
        from mastapy._private.system_model.part_model import _2537

        return self.__parent__._cast(_2537.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2538.PowerLoad":
        from mastapy._private.system_model.part_model import _2538

        return self.__parent__._cast(_2538.PowerLoad)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2544.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2544

        return self.__parent__._cast(_2544.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2546.VirtualComponent":
        from mastapy._private.system_model.part_model import _2546

        return self.__parent__._cast(_2546.VirtualComponent)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2582.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2582

        return self.__parent__._cast(_2582.AGMAGleasonConicalGear)

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
    def concept_gear(self: "CastSelf") -> "_2590.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2590

        return self.__parent__._cast(_2590.ConceptGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2592.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2592

        return self.__parent__._cast(_2592.ConicalGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2594.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2594

        return self.__parent__._cast(_2594.CylindricalGear)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2596.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2596

        return self.__parent__._cast(_2596.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2597.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2597

        return self.__parent__._cast(_2597.FaceGear)

    @property
    def gear(self: "CastSelf") -> "_2599.Gear":
        from mastapy._private.system_model.part_model.gears import _2599

        return self.__parent__._cast(_2599.Gear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2603.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2603

        return self.__parent__._cast(_2603.HypoidGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2605.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2605

        return self.__parent__._cast(_2605.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2607.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2607

        return self.__parent__._cast(_2607.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2609.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2609

        return self.__parent__._cast(_2609.KlingelnbergCycloPalloidSpiralBevelGear)

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
    def worm_gear(self: "CastSelf") -> "_2620.WormGear":
        from mastapy._private.system_model.part_model.gears import _2620

        return self.__parent__._cast(_2620.WormGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2622.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2622

        return self.__parent__._cast(_2622.ZerolBevelGear)

    @property
    def ring_pins(self: "CastSelf") -> "_2639.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2639

        return self.__parent__._cast(_2639.RingPins)

    @property
    def clutch_half(self: "CastSelf") -> "_2649.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2649

        return self.__parent__._cast(_2649.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2652.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2652

        return self.__parent__._cast(_2652.ConceptCouplingHalf)

    @property
    def coupling_half(self: "CastSelf") -> "_2655.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2655

        return self.__parent__._cast(_2655.CouplingHalf)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2658.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2658

        return self.__parent__._cast(_2658.CVTPulley)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2660.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2660

        return self.__parent__._cast(_2660.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2662.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2662

        return self.__parent__._cast(_2662.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2669.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2669

        return self.__parent__._cast(_2669.RollingRing)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2671.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2671

        return self.__parent__._cast(_2671.ShaftHubConnection)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2678.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2678

        return self.__parent__._cast(_2678.SpringDamperHalf)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2681.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2681

        return self.__parent__._cast(_2681.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2682.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2682

        return self.__parent__._cast(_2682.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2683.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2683

        return self.__parent__._cast(_2683.SynchroniserSleeve)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2685.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2685

        return self.__parent__._cast(_2685.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2687.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2687

        return self.__parent__._cast(_2687.TorqueConverterTurbine)

    @property
    def mountable_component(self: "CastSelf") -> "MountableComponent":
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
class MountableComponent(_2508.Component):
    """MountableComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rotation_about_axis(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAboutAxis")

        if temp is None:
            return 0.0

        return temp

    @rotation_about_axis.setter
    @enforce_parameter_types
    def rotation_about_axis(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotationAboutAxis",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_component(self: "Self") -> "_2499.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerComponent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_connection(self: "Self") -> "_2335.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerConnection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_socket(self: "Self") -> "_2339.CylindricalSocket":
        """mastapy.system_model.connections_and_sockets.CylindricalSocket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerSocket")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def is_mounted(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsMounted")

        if temp is None:
            return False

        return temp

    @enforce_parameter_types
    def mount_on(
        self: "Self", shaft: "_2499.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2332.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def try_mount_on(
        self: "Self", shaft: "_2499.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2509.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryMountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponent":
        """Cast to another type.

        Returns:
            _Cast_MountableComponent
        """
        return _Cast_MountableComponent(self)
