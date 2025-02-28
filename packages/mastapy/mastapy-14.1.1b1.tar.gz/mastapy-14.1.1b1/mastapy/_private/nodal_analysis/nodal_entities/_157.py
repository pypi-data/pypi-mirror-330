"""TorsionalFrictionNodePairSimpleLockedStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _156

_TORSIONAL_FRICTION_NODE_PAIR_SIMPLE_LOCKED_STIFFNESS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities",
    "TorsionalFrictionNodePairSimpleLockedStiffness",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _137,
        _138,
        _148,
        _149,
        _158,
    )

    Self = TypeVar("Self", bound="TorsionalFrictionNodePairSimpleLockedStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TorsionalFrictionNodePairSimpleLockedStiffness._Cast_TorsionalFrictionNodePairSimpleLockedStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorsionalFrictionNodePairSimpleLockedStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorsionalFrictionNodePairSimpleLockedStiffness:
    """Special nested class for casting TorsionalFrictionNodePairSimpleLockedStiffness to subclasses."""

    __parent__: "TorsionalFrictionNodePairSimpleLockedStiffness"

    @property
    def torsional_friction_node_pair(
        self: "CastSelf",
    ) -> "_156.TorsionalFrictionNodePair":
        return self.__parent__._cast(_156.TorsionalFrictionNodePair)

    @property
    def concentric_connection_nodal_component(
        self: "CastSelf",
    ) -> "_138.ConcentricConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _138

        return self.__parent__._cast(_138.ConcentricConnectionNodalComponent)

    @property
    def two_body_connection_nodal_component(
        self: "CastSelf",
    ) -> "_158.TwoBodyConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _158

        return self.__parent__._cast(_158.TwoBodyConnectionNodalComponent)

    @property
    def component_nodal_composite(self: "CastSelf") -> "_137.ComponentNodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _137

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
    def torsional_friction_node_pair_simple_locked_stiffness(
        self: "CastSelf",
    ) -> "TorsionalFrictionNodePairSimpleLockedStiffness":
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
class TorsionalFrictionNodePairSimpleLockedStiffness(_156.TorsionalFrictionNodePair):
    """TorsionalFrictionNodePairSimpleLockedStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORSIONAL_FRICTION_NODE_PAIR_SIMPLE_LOCKED_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_TorsionalFrictionNodePairSimpleLockedStiffness":
        """Cast to another type.

        Returns:
            _Cast_TorsionalFrictionNodePairSimpleLockedStiffness
        """
        return _Cast_TorsionalFrictionNodePairSimpleLockedStiffness(self)
