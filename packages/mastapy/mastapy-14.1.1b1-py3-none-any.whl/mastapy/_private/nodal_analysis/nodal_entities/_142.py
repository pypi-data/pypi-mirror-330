"""GearMeshNodePair"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _129

_GEAR_MESH_NODE_PAIR = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "GearMeshNodePair"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _147, _149

    Self = TypeVar("Self", bound="GearMeshNodePair")
    CastSelf = TypeVar("CastSelf", bound="GearMeshNodePair._Cast_GearMeshNodePair")


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshNodePair",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshNodePair:
    """Special nested class for casting GearMeshNodePair to subclasses."""

    __parent__: "GearMeshNodePair"

    @property
    def arbitrary_nodal_component(self: "CastSelf") -> "_129.ArbitraryNodalComponent":
        return self.__parent__._cast(_129.ArbitraryNodalComponent)

    @property
    def nodal_component(self: "CastSelf") -> "_147.NodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _147

        return self.__parent__._cast(_147.NodalComponent)

    @property
    def nodal_entity(self: "CastSelf") -> "_149.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _149

        return self.__parent__._cast(_149.NodalEntity)

    @property
    def gear_mesh_node_pair(self: "CastSelf") -> "GearMeshNodePair":
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
class GearMeshNodePair(_129.ArbitraryNodalComponent):
    """GearMeshNodePair

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_NODE_PAIR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshNodePair":
        """Cast to another type.

        Returns:
            _Cast_GearMeshNodePair
        """
        return _Cast_GearMeshNodePair(self)
