"""BeltDrive"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2543

_BELT_DRIVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "BeltDrive"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2266
    from mastapy._private.system_model.connections_and_sockets import _2331
    from mastapy._private.system_model.part_model import _2498, _2534
    from mastapy._private.system_model.part_model.couplings import _2647, _2657, _2662

    Self = TypeVar("Self", bound="BeltDrive")
    CastSelf = TypeVar("CastSelf", bound="BeltDrive._Cast_BeltDrive")


__docformat__ = "restructuredtext en"
__all__ = ("BeltDrive",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BeltDrive:
    """Special nested class for casting BeltDrive to subclasses."""

    __parent__: "BeltDrive"

    @property
    def specialised_assembly(self: "CastSelf") -> "_2543.SpecialisedAssembly":
        return self.__parent__._cast(_2543.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2498.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2498

        return self.__parent__._cast(_2498.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2534.Part":
        from mastapy._private.system_model.part_model import _2534

        return self.__parent__._cast(_2534.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2266.DesignEntity":
        from mastapy._private.system_model import _2266

        return self.__parent__._cast(_2266.DesignEntity)

    @property
    def cvt(self: "CastSelf") -> "_2657.CVT":
        from mastapy._private.system_model.part_model.couplings import _2657

        return self.__parent__._cast(_2657.CVT)

    @property
    def belt_drive(self: "CastSelf") -> "BeltDrive":
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
class BeltDrive(_2543.SpecialisedAssembly):
    """BeltDrive

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BELT_DRIVE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def belt_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BeltLength")

        if temp is None:
            return 0.0

        return temp

    @property
    def belt_mass(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BeltMass")

        if temp is None:
            return 0.0

        return temp

    @property
    def belt_mass_per_unit_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BeltMassPerUnitLength")

        if temp is None:
            return 0.0

        return temp

    @belt_mass_per_unit_length.setter
    @enforce_parameter_types
    def belt_mass_per_unit_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BeltMassPerUnitLength",
            float(value) if value is not None else 0.0,
        )

    @property
    def pre_tension(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PreTension")

        if temp is None:
            return 0.0

        return temp

    @pre_tension.setter
    @enforce_parameter_types
    def pre_tension(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PreTension", float(value) if value is not None else 0.0
        )

    @property
    def specify_stiffness_for_unit_length(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyStiffnessForUnitLength")

        if temp is None:
            return False

        return temp

    @specify_stiffness_for_unit_length.setter
    @enforce_parameter_types
    def specify_stiffness_for_unit_length(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyStiffnessForUnitLength",
            bool(value) if value is not None else False,
        )

    @property
    def stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Stiffness")

        if temp is None:
            return 0.0

        return temp

    @stiffness.setter
    @enforce_parameter_types
    def stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Stiffness", float(value) if value is not None else 0.0
        )

    @property
    def stiffness_for_unit_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StiffnessForUnitLength")

        if temp is None:
            return 0.0

        return temp

    @stiffness_for_unit_length.setter
    @enforce_parameter_types
    def stiffness_for_unit_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StiffnessForUnitLength",
            float(value) if value is not None else 0.0,
        )

    @property
    def type_of_belt(self: "Self") -> "_2647.BeltDriveType":
        """mastapy.system_model.part_model.couplings.BeltDriveType"""
        temp = pythonnet_property_get(self.wrapped, "TypeOfBelt")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PartModel.Couplings.BeltDriveType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model.couplings._2647", "BeltDriveType"
        )(value)

    @type_of_belt.setter
    @enforce_parameter_types
    def type_of_belt(self: "Self", value: "_2647.BeltDriveType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PartModel.Couplings.BeltDriveType"
        )
        pythonnet_property_set(self.wrapped, "TypeOfBelt", value)

    @property
    def belt_connections(self: "Self") -> "List[_2331.BeltConnection]":
        """List[mastapy.system_model.connections_and_sockets.BeltConnection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BeltConnections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def pulleys(self: "Self") -> "List[_2662.Pulley]":
        """List[mastapy.system_model.part_model.couplings.Pulley]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Pulleys")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BeltDrive":
        """Cast to another type.

        Returns:
            _Cast_BeltDrive
        """
        return _Cast_BeltDrive(self)
