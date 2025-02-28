"""NodalComposite"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _149

_NODAL_COMPOSITE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "NodalComposite"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _131,
        _132,
        _133,
        _137,
        _138,
        _141,
        _143,
        _144,
        _153,
        _154,
        _156,
        _157,
        _158,
    )

    Self = TypeVar("Self", bound="NodalComposite")
    CastSelf = TypeVar("CastSelf", bound="NodalComposite._Cast_NodalComposite")


__docformat__ = "restructuredtext en"
__all__ = ("NodalComposite",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodalComposite:
    """Special nested class for casting NodalComposite to subclasses."""

    __parent__: "NodalComposite"

    @property
    def nodal_entity(self: "CastSelf") -> "_149.NodalEntity":
        return self.__parent__._cast(_149.NodalEntity)

    @property
    def bar_elastic_mbd(self: "CastSelf") -> "_131.BarElasticMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _131

        return self.__parent__._cast(_131.BarElasticMBD)

    @property
    def bar_mbd(self: "CastSelf") -> "_132.BarMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _132

        return self.__parent__._cast(_132.BarMBD)

    @property
    def bar_rigid_mbd(self: "CastSelf") -> "_133.BarRigidMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _133

        return self.__parent__._cast(_133.BarRigidMBD)

    @property
    def component_nodal_composite(self: "CastSelf") -> "_137.ComponentNodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _137

        return self.__parent__._cast(_137.ComponentNodalComposite)

    @property
    def concentric_connection_nodal_component(
        self: "CastSelf",
    ) -> "_138.ConcentricConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _138

        return self.__parent__._cast(_138.ConcentricConnectionNodalComponent)

    @property
    def gear_mesh_nodal_component(self: "CastSelf") -> "_141.GearMeshNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _141

        return self.__parent__._cast(_141.GearMeshNodalComponent)

    @property
    def gear_mesh_point_on_flank_contact(
        self: "CastSelf",
    ) -> "_143.GearMeshPointOnFlankContact":
        from mastapy._private.nodal_analysis.nodal_entities import _143

        return self.__parent__._cast(_143.GearMeshPointOnFlankContact)

    @property
    def gear_mesh_single_flank_contact(
        self: "CastSelf",
    ) -> "_144.GearMeshSingleFlankContact":
        from mastapy._private.nodal_analysis.nodal_entities import _144

        return self.__parent__._cast(_144.GearMeshSingleFlankContact)

    @property
    def simple_bar(self: "CastSelf") -> "_153.SimpleBar":
        from mastapy._private.nodal_analysis.nodal_entities import _153

        return self.__parent__._cast(_153.SimpleBar)

    @property
    def spline_contact_nodal_component(
        self: "CastSelf",
    ) -> "_154.SplineContactNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _154

        return self.__parent__._cast(_154.SplineContactNodalComponent)

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
    ) -> "_158.TwoBodyConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _158

        return self.__parent__._cast(_158.TwoBodyConnectionNodalComponent)

    @property
    def nodal_composite(self: "CastSelf") -> "NodalComposite":
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
class NodalComposite(_149.NodalEntity):
    """NodalComposite

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODAL_COMPOSITE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NodalComposite":
        """Cast to another type.

        Returns:
            _Cast_NodalComposite
        """
        return _Cast_NodalComposite(self)
