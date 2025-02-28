"""GearDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _980

_GEAR_DESIGN = python_net_import("SMT.MastaAPI.Gears.GearDesigns", "GearDesign")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.fe_model import _1245
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1241
    from mastapy._private.gears.gear_designs.bevel import _1228
    from mastapy._private.gears.gear_designs.concept import _1224
    from mastapy._private.gears.gear_designs.conical import _1202
    from mastapy._private.gears.gear_designs.cylindrical import _1050, _1080
    from mastapy._private.gears.gear_designs.face import _1021, _1026, _1029
    from mastapy._private.gears.gear_designs.hypoid import _1017
    from mastapy._private.gears.gear_designs.klingelnberg_conical import _1013
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1009
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1005
    from mastapy._private.gears.gear_designs.spiral_bevel import _1001
    from mastapy._private.gears.gear_designs.straight_bevel import _993
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _997
    from mastapy._private.gears.gear_designs.worm import _988, _989, _992
    from mastapy._private.gears.gear_designs.zerol_bevel import _984

    Self = TypeVar("Self", bound="GearDesign")
    CastSelf = TypeVar("CastSelf", bound="GearDesign._Cast_GearDesign")


__docformat__ = "restructuredtext en"
__all__ = ("GearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearDesign:
    """Special nested class for casting GearDesign to subclasses."""

    __parent__: "GearDesign"

    @property
    def gear_design_component(self: "CastSelf") -> "_980.GearDesignComponent":
        return self.__parent__._cast(_980.GearDesignComponent)

    @property
    def zerol_bevel_gear_design(self: "CastSelf") -> "_984.ZerolBevelGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _984

        return self.__parent__._cast(_984.ZerolBevelGearDesign)

    @property
    def worm_design(self: "CastSelf") -> "_988.WormDesign":
        from mastapy._private.gears.gear_designs.worm import _988

        return self.__parent__._cast(_988.WormDesign)

    @property
    def worm_gear_design(self: "CastSelf") -> "_989.WormGearDesign":
        from mastapy._private.gears.gear_designs.worm import _989

        return self.__parent__._cast(_989.WormGearDesign)

    @property
    def worm_wheel_design(self: "CastSelf") -> "_992.WormWheelDesign":
        from mastapy._private.gears.gear_designs.worm import _992

        return self.__parent__._cast(_992.WormWheelDesign)

    @property
    def straight_bevel_gear_design(self: "CastSelf") -> "_993.StraightBevelGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _993

        return self.__parent__._cast(_993.StraightBevelGearDesign)

    @property
    def straight_bevel_diff_gear_design(
        self: "CastSelf",
    ) -> "_997.StraightBevelDiffGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _997

        return self.__parent__._cast(_997.StraightBevelDiffGearDesign)

    @property
    def spiral_bevel_gear_design(self: "CastSelf") -> "_1001.SpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1001

        return self.__parent__._cast(_1001.SpiralBevelGearDesign)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_design(
        self: "CastSelf",
    ) -> "_1005.KlingelnbergCycloPalloidSpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1005

        return self.__parent__._cast(
            _1005.KlingelnbergCycloPalloidSpiralBevelGearDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_design(
        self: "CastSelf",
    ) -> "_1009.KlingelnbergCycloPalloidHypoidGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1009

        return self.__parent__._cast(_1009.KlingelnbergCycloPalloidHypoidGearDesign)

    @property
    def klingelnberg_conical_gear_design(
        self: "CastSelf",
    ) -> "_1013.KlingelnbergConicalGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1013

        return self.__parent__._cast(_1013.KlingelnbergConicalGearDesign)

    @property
    def hypoid_gear_design(self: "CastSelf") -> "_1017.HypoidGearDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1017

        return self.__parent__._cast(_1017.HypoidGearDesign)

    @property
    def face_gear_design(self: "CastSelf") -> "_1021.FaceGearDesign":
        from mastapy._private.gears.gear_designs.face import _1021

        return self.__parent__._cast(_1021.FaceGearDesign)

    @property
    def face_gear_pinion_design(self: "CastSelf") -> "_1026.FaceGearPinionDesign":
        from mastapy._private.gears.gear_designs.face import _1026

        return self.__parent__._cast(_1026.FaceGearPinionDesign)

    @property
    def face_gear_wheel_design(self: "CastSelf") -> "_1029.FaceGearWheelDesign":
        from mastapy._private.gears.gear_designs.face import _1029

        return self.__parent__._cast(_1029.FaceGearWheelDesign)

    @property
    def cylindrical_gear_design(self: "CastSelf") -> "_1050.CylindricalGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1050

        return self.__parent__._cast(_1050.CylindricalGearDesign)

    @property
    def cylindrical_planet_gear_design(
        self: "CastSelf",
    ) -> "_1080.CylindricalPlanetGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1080

        return self.__parent__._cast(_1080.CylindricalPlanetGearDesign)

    @property
    def conical_gear_design(self: "CastSelf") -> "_1202.ConicalGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1202

        return self.__parent__._cast(_1202.ConicalGearDesign)

    @property
    def concept_gear_design(self: "CastSelf") -> "_1224.ConceptGearDesign":
        from mastapy._private.gears.gear_designs.concept import _1224

        return self.__parent__._cast(_1224.ConceptGearDesign)

    @property
    def bevel_gear_design(self: "CastSelf") -> "_1228.BevelGearDesign":
        from mastapy._private.gears.gear_designs.bevel import _1228

        return self.__parent__._cast(_1228.BevelGearDesign)

    @property
    def agma_gleason_conical_gear_design(
        self: "CastSelf",
    ) -> "_1241.AGMAGleasonConicalGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1241

        return self.__parent__._cast(_1241.AGMAGleasonConicalGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "GearDesign":
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
class GearDesign(_980.GearDesignComponent):
    """GearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def absolute_shaft_inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AbsoluteShaftInnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    @enforce_parameter_types
    def face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidth", float(value) if value is not None else 0.0
        )

    @property
    def mass(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return temp

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def names_of_meshing_gears(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NamesOfMeshingGears")

        if temp is None:
            return ""

        return temp

    @property
    def number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @number_of_teeth.setter
    @enforce_parameter_types
    def number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    def number_of_teeth_maintaining_ratio(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethMaintainingRatio")

        if temp is None:
            return 0

        return temp

    @number_of_teeth_maintaining_ratio.setter
    @enforce_parameter_types
    def number_of_teeth_maintaining_ratio(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTeethMaintainingRatio",
            int(value) if value is not None else 0,
        )

    @property
    def shaft_inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftInnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def shaft_outer_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftOuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def tifffe_model(self: "Self") -> "_1245.GearFEModel":
        """mastapy.gears.fe_model.GearFEModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TIFFFEModel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearDesign":
        """Cast to another type.

        Returns:
            _Cast_GearDesign
        """
        return _Cast_GearDesign(self)
