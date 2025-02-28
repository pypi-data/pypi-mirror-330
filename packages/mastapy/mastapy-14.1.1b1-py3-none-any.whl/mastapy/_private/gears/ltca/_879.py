"""GearStiffnessNode"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis import _70

_GEAR_STIFFNESS_NODE = python_net_import("SMT.MastaAPI.Gears.LTCA", "GearStiffnessNode")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.ltca import _865, _867
    from mastapy._private.gears.ltca.conical import _895, _897
    from mastapy._private.gears.ltca.cylindrical import _883, _885

    Self = TypeVar("Self", bound="GearStiffnessNode")
    CastSelf = TypeVar("CastSelf", bound="GearStiffnessNode._Cast_GearStiffnessNode")


__docformat__ = "restructuredtext en"
__all__ = ("GearStiffnessNode",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearStiffnessNode:
    """Special nested class for casting GearStiffnessNode to subclasses."""

    __parent__: "GearStiffnessNode"

    @property
    def fe_stiffness_node(self: "CastSelf") -> "_70.FEStiffnessNode":
        return self.__parent__._cast(_70.FEStiffnessNode)

    @property
    def gear_bending_stiffness_node(
        self: "CastSelf",
    ) -> "_865.GearBendingStiffnessNode":
        from mastapy._private.gears.ltca import _865

        return self.__parent__._cast(_865.GearBendingStiffnessNode)

    @property
    def gear_contact_stiffness_node(
        self: "CastSelf",
    ) -> "_867.GearContactStiffnessNode":
        from mastapy._private.gears.ltca import _867

        return self.__parent__._cast(_867.GearContactStiffnessNode)

    @property
    def cylindrical_gear_bending_stiffness_node(
        self: "CastSelf",
    ) -> "_883.CylindricalGearBendingStiffnessNode":
        from mastapy._private.gears.ltca.cylindrical import _883

        return self.__parent__._cast(_883.CylindricalGearBendingStiffnessNode)

    @property
    def cylindrical_gear_contact_stiffness_node(
        self: "CastSelf",
    ) -> "_885.CylindricalGearContactStiffnessNode":
        from mastapy._private.gears.ltca.cylindrical import _885

        return self.__parent__._cast(_885.CylindricalGearContactStiffnessNode)

    @property
    def conical_gear_bending_stiffness_node(
        self: "CastSelf",
    ) -> "_895.ConicalGearBendingStiffnessNode":
        from mastapy._private.gears.ltca.conical import _895

        return self.__parent__._cast(_895.ConicalGearBendingStiffnessNode)

    @property
    def conical_gear_contact_stiffness_node(
        self: "CastSelf",
    ) -> "_897.ConicalGearContactStiffnessNode":
        from mastapy._private.gears.ltca.conical import _897

        return self.__parent__._cast(_897.ConicalGearContactStiffnessNode)

    @property
    def gear_stiffness_node(self: "CastSelf") -> "GearStiffnessNode":
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
class GearStiffnessNode(_70.FEStiffnessNode):
    """GearStiffnessNode

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_STIFFNESS_NODE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearStiffnessNode":
        """Cast to another type.

        Returns:
            _Cast_GearStiffnessNode
        """
        return _Cast_GearStiffnessNode(self)
