"""GearDesignComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GEAR_DESIGN_COMPONENT = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns", "GearDesignComponent"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _979, _981, _982
    from mastapy._private.gears.gear_designs.agma_gleason_conical import (
        _1241,
        _1242,
        _1243,
        _1244,
    )
    from mastapy._private.gears.gear_designs.bevel import _1228, _1229, _1230, _1231
    from mastapy._private.gears.gear_designs.concept import _1224, _1225, _1226
    from mastapy._private.gears.gear_designs.conical import _1202, _1203, _1204, _1207
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1050,
        _1056,
        _1066,
        _1079,
        _1080,
    )
    from mastapy._private.gears.gear_designs.face import (
        _1021,
        _1023,
        _1026,
        _1027,
        _1029,
    )
    from mastapy._private.gears.gear_designs.hypoid import _1017, _1018, _1019, _1020
    from mastapy._private.gears.gear_designs.klingelnberg_conical import (
        _1013,
        _1014,
        _1015,
        _1016,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import (
        _1009,
        _1010,
        _1011,
        _1012,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import (
        _1005,
        _1006,
        _1007,
        _1008,
    )
    from mastapy._private.gears.gear_designs.spiral_bevel import (
        _1001,
        _1002,
        _1003,
        _1004,
    )
    from mastapy._private.gears.gear_designs.straight_bevel import (
        _993,
        _994,
        _995,
        _996,
    )
    from mastapy._private.gears.gear_designs.straight_bevel_diff import (
        _997,
        _998,
        _999,
        _1000,
    )
    from mastapy._private.gears.gear_designs.worm import _988, _989, _990, _991, _992
    from mastapy._private.gears.gear_designs.zerol_bevel import _984, _985, _986, _987
    from mastapy._private.utility.scripting import _1800

    Self = TypeVar("Self", bound="GearDesignComponent")
    CastSelf = TypeVar(
        "CastSelf", bound="GearDesignComponent._Cast_GearDesignComponent"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearDesignComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearDesignComponent:
    """Special nested class for casting GearDesignComponent to subclasses."""

    __parent__: "GearDesignComponent"

    @property
    def gear_design(self: "CastSelf") -> "_979.GearDesign":
        from mastapy._private.gears.gear_designs import _979

        return self.__parent__._cast(_979.GearDesign)

    @property
    def gear_mesh_design(self: "CastSelf") -> "_981.GearMeshDesign":
        from mastapy._private.gears.gear_designs import _981

        return self.__parent__._cast(_981.GearMeshDesign)

    @property
    def gear_set_design(self: "CastSelf") -> "_982.GearSetDesign":
        from mastapy._private.gears.gear_designs import _982

        return self.__parent__._cast(_982.GearSetDesign)

    @property
    def zerol_bevel_gear_design(self: "CastSelf") -> "_984.ZerolBevelGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _984

        return self.__parent__._cast(_984.ZerolBevelGearDesign)

    @property
    def zerol_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_985.ZerolBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _985

        return self.__parent__._cast(_985.ZerolBevelGearMeshDesign)

    @property
    def zerol_bevel_gear_set_design(self: "CastSelf") -> "_986.ZerolBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _986

        return self.__parent__._cast(_986.ZerolBevelGearSetDesign)

    @property
    def zerol_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_987.ZerolBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _987

        return self.__parent__._cast(_987.ZerolBevelMeshedGearDesign)

    @property
    def worm_design(self: "CastSelf") -> "_988.WormDesign":
        from mastapy._private.gears.gear_designs.worm import _988

        return self.__parent__._cast(_988.WormDesign)

    @property
    def worm_gear_design(self: "CastSelf") -> "_989.WormGearDesign":
        from mastapy._private.gears.gear_designs.worm import _989

        return self.__parent__._cast(_989.WormGearDesign)

    @property
    def worm_gear_mesh_design(self: "CastSelf") -> "_990.WormGearMeshDesign":
        from mastapy._private.gears.gear_designs.worm import _990

        return self.__parent__._cast(_990.WormGearMeshDesign)

    @property
    def worm_gear_set_design(self: "CastSelf") -> "_991.WormGearSetDesign":
        from mastapy._private.gears.gear_designs.worm import _991

        return self.__parent__._cast(_991.WormGearSetDesign)

    @property
    def worm_wheel_design(self: "CastSelf") -> "_992.WormWheelDesign":
        from mastapy._private.gears.gear_designs.worm import _992

        return self.__parent__._cast(_992.WormWheelDesign)

    @property
    def straight_bevel_gear_design(self: "CastSelf") -> "_993.StraightBevelGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _993

        return self.__parent__._cast(_993.StraightBevelGearDesign)

    @property
    def straight_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_994.StraightBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _994

        return self.__parent__._cast(_994.StraightBevelGearMeshDesign)

    @property
    def straight_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_995.StraightBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _995

        return self.__parent__._cast(_995.StraightBevelGearSetDesign)

    @property
    def straight_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_996.StraightBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _996

        return self.__parent__._cast(_996.StraightBevelMeshedGearDesign)

    @property
    def straight_bevel_diff_gear_design(
        self: "CastSelf",
    ) -> "_997.StraightBevelDiffGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _997

        return self.__parent__._cast(_997.StraightBevelDiffGearDesign)

    @property
    def straight_bevel_diff_gear_mesh_design(
        self: "CastSelf",
    ) -> "_998.StraightBevelDiffGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _998

        return self.__parent__._cast(_998.StraightBevelDiffGearMeshDesign)

    @property
    def straight_bevel_diff_gear_set_design(
        self: "CastSelf",
    ) -> "_999.StraightBevelDiffGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _999

        return self.__parent__._cast(_999.StraightBevelDiffGearSetDesign)

    @property
    def straight_bevel_diff_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1000.StraightBevelDiffMeshedGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1000

        return self.__parent__._cast(_1000.StraightBevelDiffMeshedGearDesign)

    @property
    def spiral_bevel_gear_design(self: "CastSelf") -> "_1001.SpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1001

        return self.__parent__._cast(_1001.SpiralBevelGearDesign)

    @property
    def spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1002.SpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1002

        return self.__parent__._cast(_1002.SpiralBevelGearMeshDesign)

    @property
    def spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1003.SpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1003

        return self.__parent__._cast(_1003.SpiralBevelGearSetDesign)

    @property
    def spiral_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1004.SpiralBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1004

        return self.__parent__._cast(_1004.SpiralBevelMeshedGearDesign)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_design(
        self: "CastSelf",
    ) -> "_1005.KlingelnbergCycloPalloidSpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1005

        return self.__parent__._cast(
            _1005.KlingelnbergCycloPalloidSpiralBevelGearDesign
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1006.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1006

        return self.__parent__._cast(
            _1006.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1007.KlingelnbergCycloPalloidSpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1007

        return self.__parent__._cast(
            _1007.KlingelnbergCycloPalloidSpiralBevelGearSetDesign
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1008.KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1008

        return self.__parent__._cast(
            _1008.KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_design(
        self: "CastSelf",
    ) -> "_1009.KlingelnbergCycloPalloidHypoidGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1009

        return self.__parent__._cast(_1009.KlingelnbergCycloPalloidHypoidGearDesign)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1010.KlingelnbergCycloPalloidHypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1010

        return self.__parent__._cast(_1010.KlingelnbergCycloPalloidHypoidGearMeshDesign)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_design(
        self: "CastSelf",
    ) -> "_1011.KlingelnbergCycloPalloidHypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1011

        return self.__parent__._cast(_1011.KlingelnbergCycloPalloidHypoidGearSetDesign)

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1012.KlingelnbergCycloPalloidHypoidMeshedGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1012

        return self.__parent__._cast(
            _1012.KlingelnbergCycloPalloidHypoidMeshedGearDesign
        )

    @property
    def klingelnberg_conical_gear_design(
        self: "CastSelf",
    ) -> "_1013.KlingelnbergConicalGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1013

        return self.__parent__._cast(_1013.KlingelnbergConicalGearDesign)

    @property
    def klingelnberg_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1014.KlingelnbergConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1014

        return self.__parent__._cast(_1014.KlingelnbergConicalGearMeshDesign)

    @property
    def klingelnberg_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1015.KlingelnbergConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1015

        return self.__parent__._cast(_1015.KlingelnbergConicalGearSetDesign)

    @property
    def klingelnberg_conical_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1016.KlingelnbergConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1016

        return self.__parent__._cast(_1016.KlingelnbergConicalMeshedGearDesign)

    @property
    def hypoid_gear_design(self: "CastSelf") -> "_1017.HypoidGearDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1017

        return self.__parent__._cast(_1017.HypoidGearDesign)

    @property
    def hypoid_gear_mesh_design(self: "CastSelf") -> "_1018.HypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1018

        return self.__parent__._cast(_1018.HypoidGearMeshDesign)

    @property
    def hypoid_gear_set_design(self: "CastSelf") -> "_1019.HypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1019

        return self.__parent__._cast(_1019.HypoidGearSetDesign)

    @property
    def hypoid_meshed_gear_design(self: "CastSelf") -> "_1020.HypoidMeshedGearDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1020

        return self.__parent__._cast(_1020.HypoidMeshedGearDesign)

    @property
    def face_gear_design(self: "CastSelf") -> "_1021.FaceGearDesign":
        from mastapy._private.gears.gear_designs.face import _1021

        return self.__parent__._cast(_1021.FaceGearDesign)

    @property
    def face_gear_mesh_design(self: "CastSelf") -> "_1023.FaceGearMeshDesign":
        from mastapy._private.gears.gear_designs.face import _1023

        return self.__parent__._cast(_1023.FaceGearMeshDesign)

    @property
    def face_gear_pinion_design(self: "CastSelf") -> "_1026.FaceGearPinionDesign":
        from mastapy._private.gears.gear_designs.face import _1026

        return self.__parent__._cast(_1026.FaceGearPinionDesign)

    @property
    def face_gear_set_design(self: "CastSelf") -> "_1027.FaceGearSetDesign":
        from mastapy._private.gears.gear_designs.face import _1027

        return self.__parent__._cast(_1027.FaceGearSetDesign)

    @property
    def face_gear_wheel_design(self: "CastSelf") -> "_1029.FaceGearWheelDesign":
        from mastapy._private.gears.gear_designs.face import _1029

        return self.__parent__._cast(_1029.FaceGearWheelDesign)

    @property
    def cylindrical_gear_design(self: "CastSelf") -> "_1050.CylindricalGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1050

        return self.__parent__._cast(_1050.CylindricalGearDesign)

    @property
    def cylindrical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1056.CylindricalGearMeshDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1056

        return self.__parent__._cast(_1056.CylindricalGearMeshDesign)

    @property
    def cylindrical_gear_set_design(
        self: "CastSelf",
    ) -> "_1066.CylindricalGearSetDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1066

        return self.__parent__._cast(_1066.CylindricalGearSetDesign)

    @property
    def cylindrical_planetary_gear_set_design(
        self: "CastSelf",
    ) -> "_1079.CylindricalPlanetaryGearSetDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1079

        return self.__parent__._cast(_1079.CylindricalPlanetaryGearSetDesign)

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
    def conical_gear_mesh_design(self: "CastSelf") -> "_1203.ConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.conical import _1203

        return self.__parent__._cast(_1203.ConicalGearMeshDesign)

    @property
    def conical_gear_set_design(self: "CastSelf") -> "_1204.ConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.conical import _1204

        return self.__parent__._cast(_1204.ConicalGearSetDesign)

    @property
    def conical_meshed_gear_design(self: "CastSelf") -> "_1207.ConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1207

        return self.__parent__._cast(_1207.ConicalMeshedGearDesign)

    @property
    def concept_gear_design(self: "CastSelf") -> "_1224.ConceptGearDesign":
        from mastapy._private.gears.gear_designs.concept import _1224

        return self.__parent__._cast(_1224.ConceptGearDesign)

    @property
    def concept_gear_mesh_design(self: "CastSelf") -> "_1225.ConceptGearMeshDesign":
        from mastapy._private.gears.gear_designs.concept import _1225

        return self.__parent__._cast(_1225.ConceptGearMeshDesign)

    @property
    def concept_gear_set_design(self: "CastSelf") -> "_1226.ConceptGearSetDesign":
        from mastapy._private.gears.gear_designs.concept import _1226

        return self.__parent__._cast(_1226.ConceptGearSetDesign)

    @property
    def bevel_gear_design(self: "CastSelf") -> "_1228.BevelGearDesign":
        from mastapy._private.gears.gear_designs.bevel import _1228

        return self.__parent__._cast(_1228.BevelGearDesign)

    @property
    def bevel_gear_mesh_design(self: "CastSelf") -> "_1229.BevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.bevel import _1229

        return self.__parent__._cast(_1229.BevelGearMeshDesign)

    @property
    def bevel_gear_set_design(self: "CastSelf") -> "_1230.BevelGearSetDesign":
        from mastapy._private.gears.gear_designs.bevel import _1230

        return self.__parent__._cast(_1230.BevelGearSetDesign)

    @property
    def bevel_meshed_gear_design(self: "CastSelf") -> "_1231.BevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.bevel import _1231

        return self.__parent__._cast(_1231.BevelMeshedGearDesign)

    @property
    def agma_gleason_conical_gear_design(
        self: "CastSelf",
    ) -> "_1241.AGMAGleasonConicalGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1241

        return self.__parent__._cast(_1241.AGMAGleasonConicalGearDesign)

    @property
    def agma_gleason_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1242.AGMAGleasonConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1242

        return self.__parent__._cast(_1242.AGMAGleasonConicalGearMeshDesign)

    @property
    def agma_gleason_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1243.AGMAGleasonConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1243

        return self.__parent__._cast(_1243.AGMAGleasonConicalGearSetDesign)

    @property
    def agma_gleason_conical_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1244.AGMAGleasonConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1244

        return self.__parent__._cast(_1244.AGMAGleasonConicalMeshedGearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "GearDesignComponent":
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
class GearDesignComponent(_0.APIBase):
    """GearDesignComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_DESIGN_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    def user_specified_data(self: "Self") -> "_1800.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    def dispose(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Dispose")

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    def __enter__(self: "Self") -> None:
        return self

    def __exit__(
        self: "Self", exception_type: "Any", exception_value: "Any", traceback: "Any"
    ) -> None:
        self.dispose()

    @property
    def cast_to(self: "Self") -> "_Cast_GearDesignComponent":
        """Cast to another type.

        Returns:
            _Cast_GearDesignComponent
        """
        return _Cast_GearDesignComponent(self)
