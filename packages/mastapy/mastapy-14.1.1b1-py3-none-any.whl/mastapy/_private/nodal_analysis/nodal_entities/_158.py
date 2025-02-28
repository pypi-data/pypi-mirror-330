"""TwoBodyConnectionNodalComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _137

_TWO_BODY_CONNECTION_NODAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "TwoBodyConnectionNodalComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _138,
        _143,
        _148,
        _149,
        _153,
        _156,
        _157,
    )

    Self = TypeVar("Self", bound="TwoBodyConnectionNodalComponent")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TwoBodyConnectionNodalComponent._Cast_TwoBodyConnectionNodalComponent",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TwoBodyConnectionNodalComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TwoBodyConnectionNodalComponent:
    """Special nested class for casting TwoBodyConnectionNodalComponent to subclasses."""

    __parent__: "TwoBodyConnectionNodalComponent"

    @property
    def component_nodal_composite(self: "CastSelf") -> "_137.ComponentNodalComposite":
        return self.__parent__._cast(_137.ComponentNodalComposite)

    @property
    def nodal_composite(self: "CastSelf") -> "_148.NodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _148

        return self.__parent__._cast(_148.NodalComposite)

    @property
    def nodal_entity(self: "CastSelf") -> "_149.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _149

        return self.__parent__._cast(_149.NodalEntity)

    @property
    def concentric_connection_nodal_component(
        self: "CastSelf",
    ) -> "_138.ConcentricConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _138

        return self.__parent__._cast(_138.ConcentricConnectionNodalComponent)

    @property
    def gear_mesh_point_on_flank_contact(
        self: "CastSelf",
    ) -> "_143.GearMeshPointOnFlankContact":
        from mastapy._private.nodal_analysis.nodal_entities import _143

        return self.__parent__._cast(_143.GearMeshPointOnFlankContact)

    @property
    def simple_bar(self: "CastSelf") -> "_153.SimpleBar":
        from mastapy._private.nodal_analysis.nodal_entities import _153

        return self.__parent__._cast(_153.SimpleBar)

    @property
    def torsional_friction_node_pair(
        self: "CastSelf",
    ) -> "_156.TorsionalFrictionNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _156

        return self.__parent__._cast(_156.TorsionalFrictionNodePair)

    @property
    def torsional_friction_node_pair_simple_locked_stiffness(
        self: "CastSelf",
    ) -> "_157.TorsionalFrictionNodePairSimpleLockedStiffness":
        from mastapy._private.nodal_analysis.nodal_entities import _157

        return self.__parent__._cast(
            _157.TorsionalFrictionNodePairSimpleLockedStiffness
        )

    @property
    def two_body_connection_nodal_component(
        self: "CastSelf",
    ) -> "TwoBodyConnectionNodalComponent":
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
class TwoBodyConnectionNodalComponent(_137.ComponentNodalComposite):
    """TwoBodyConnectionNodalComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TWO_BODY_CONNECTION_NODAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_TwoBodyConnectionNodalComponent":
        """Cast to another type.

        Returns:
            _Cast_TwoBodyConnectionNodalComponent
        """
        return _Cast_TwoBodyConnectionNodalComponent(self)
