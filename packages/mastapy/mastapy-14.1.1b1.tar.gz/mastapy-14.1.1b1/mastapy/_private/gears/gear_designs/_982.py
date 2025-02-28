"""GearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _980

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_GEAR_SET_DESIGN = python_net_import("SMT.MastaAPI.Gears.GearDesigns", "GearSetDesign")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _346
    from mastapy._private.gears.fe_model import _1248
    from mastapy._private.gears.gear_designs import _979
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1243
    from mastapy._private.gears.gear_designs.bevel import _1230
    from mastapy._private.gears.gear_designs.concept import _1226
    from mastapy._private.gears.gear_designs.conical import _1204
    from mastapy._private.gears.gear_designs.cylindrical import _1066, _1079
    from mastapy._private.gears.gear_designs.face import _1027
    from mastapy._private.gears.gear_designs.hypoid import _1019
    from mastapy._private.gears.gear_designs.klingelnberg_conical import _1015
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1011
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1007
    from mastapy._private.gears.gear_designs.spiral_bevel import _1003
    from mastapy._private.gears.gear_designs.straight_bevel import _995
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _999
    from mastapy._private.gears.gear_designs.worm import _991
    from mastapy._private.gears.gear_designs.zerol_bevel import _986

    Self = TypeVar("Self", bound="GearSetDesign")
    CastSelf = TypeVar("CastSelf", bound="GearSetDesign._Cast_GearSetDesign")


__docformat__ = "restructuredtext en"
__all__ = ("GearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetDesign:
    """Special nested class for casting GearSetDesign to subclasses."""

    __parent__: "GearSetDesign"

    @property
    def gear_design_component(self: "CastSelf") -> "_980.GearDesignComponent":
        return self.__parent__._cast(_980.GearDesignComponent)

    @property
    def zerol_bevel_gear_set_design(self: "CastSelf") -> "_986.ZerolBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _986

        return self.__parent__._cast(_986.ZerolBevelGearSetDesign)

    @property
    def worm_gear_set_design(self: "CastSelf") -> "_991.WormGearSetDesign":
        from mastapy._private.gears.gear_designs.worm import _991

        return self.__parent__._cast(_991.WormGearSetDesign)

    @property
    def straight_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_995.StraightBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _995

        return self.__parent__._cast(_995.StraightBevelGearSetDesign)

    @property
    def straight_bevel_diff_gear_set_design(
        self: "CastSelf",
    ) -> "_999.StraightBevelDiffGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _999

        return self.__parent__._cast(_999.StraightBevelDiffGearSetDesign)

    @property
    def spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1003.SpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1003

        return self.__parent__._cast(_1003.SpiralBevelGearSetDesign)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1007.KlingelnbergCycloPalloidSpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1007

        return self.__parent__._cast(
            _1007.KlingelnbergCycloPalloidSpiralBevelGearSetDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_design(
        self: "CastSelf",
    ) -> "_1011.KlingelnbergCycloPalloidHypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1011

        return self.__parent__._cast(_1011.KlingelnbergCycloPalloidHypoidGearSetDesign)

    @property
    def klingelnberg_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1015.KlingelnbergConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1015

        return self.__parent__._cast(_1015.KlingelnbergConicalGearSetDesign)

    @property
    def hypoid_gear_set_design(self: "CastSelf") -> "_1019.HypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1019

        return self.__parent__._cast(_1019.HypoidGearSetDesign)

    @property
    def face_gear_set_design(self: "CastSelf") -> "_1027.FaceGearSetDesign":
        from mastapy._private.gears.gear_designs.face import _1027

        return self.__parent__._cast(_1027.FaceGearSetDesign)

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
    def conical_gear_set_design(self: "CastSelf") -> "_1204.ConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.conical import _1204

        return self.__parent__._cast(_1204.ConicalGearSetDesign)

    @property
    def concept_gear_set_design(self: "CastSelf") -> "_1226.ConceptGearSetDesign":
        from mastapy._private.gears.gear_designs.concept import _1226

        return self.__parent__._cast(_1226.ConceptGearSetDesign)

    @property
    def bevel_gear_set_design(self: "CastSelf") -> "_1230.BevelGearSetDesign":
        from mastapy._private.gears.gear_designs.bevel import _1230

        return self.__parent__._cast(_1230.BevelGearSetDesign)

    @property
    def agma_gleason_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1243.AGMAGleasonConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1243

        return self.__parent__._cast(_1243.AGMAGleasonConicalGearSetDesign)

    @property
    def gear_set_design(self: "CastSelf") -> "GearSetDesign":
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
class GearSetDesign(_980.GearDesignComponent):
    """GearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def axial_contact_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialContactRatioRatingForNVH")

        if temp is None:
            return 0.0

        return temp

    @property
    def fe_model(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "FEModel", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @fe_model.setter
    @enforce_parameter_types
    def fe_model(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "FEModel",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def gear_set_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def has_errors_or_warnings(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasErrorsOrWarnings")

        if temp is None:
            return False

        return temp

    @property
    def largest_mesh_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LargestMeshRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def largest_number_of_teeth(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LargestNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @property
    def long_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LongName")

        if temp is None:
            return ""

        return temp

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
    def name_including_tooth_numbers(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NameIncludingToothNumbers")

        if temp is None:
            return ""

        return temp

    @property
    def required_safety_factor_for_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RequiredSafetyFactorForBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def required_safety_factor_for_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RequiredSafetyFactorForContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def required_safety_factor_for_static_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForStaticBending"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def required_safety_factor_for_static_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForStaticContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def smallest_number_of_teeth(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallestNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @property
    def transverse_contact_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseContactRatioRatingForNVH"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_and_axial_contact_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseAndAxialContactRatioRatingForNVH"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def use_script_to_provide_mesh_efficiency(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseScriptToProvideMeshEfficiency")

        if temp is None:
            return False

        return temp

    @use_script_to_provide_mesh_efficiency.setter
    @enforce_parameter_types
    def use_script_to_provide_mesh_efficiency(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseScriptToProvideMeshEfficiency",
            bool(value) if value is not None else False,
        )

    @property
    def active_ltcafe_model(self: "Self") -> "_1248.GearSetFEModel":
        """mastapy.gears.fe_model.GearSetFEModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveLTCAFEModel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def tifffe_model(self: "Self") -> "_1248.GearSetFEModel":
        """mastapy.gears.fe_model.GearSetFEModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TIFFFEModel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def transmission_properties_gears(self: "Self") -> "_346.GearSetDesignGroup":
        """mastapy.gears.GearSetDesignGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransmissionPropertiesGears")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gears(self: "Self") -> "List[_979.GearDesign]":
        """List[mastapy.gears.gear_designs.GearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def ltcafe_models(self: "Self") -> "List[_1248.GearSetFEModel]":
        """List[mastapy.gears.fe_model.GearSetFEModel]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LTCAFEModels")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def create_new_tifffe_model(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateNewTIFFFEModel")

    def create_new_fe_model(self: "Self") -> "_1248.GearSetFEModel":
        """mastapy.gears.fe_model.GearSetFEModel"""
        method_result = pythonnet_method_call(self.wrapped, "CreateNewFEModel")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def copy(self: "Self", include_fe: "bool" = False) -> "GearSetDesign":
        """mastapy.gears.gear_designs.GearSetDesign

        Args:
            include_fe (bool, optional)
        """
        include_fe = bool(include_fe)
        method_result = pythonnet_method_call(
            self.wrapped, "Copy", include_fe if include_fe else False
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_GearSetDesign
        """
        return _Cast_GearSetDesign(self)
