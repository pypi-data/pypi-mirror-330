"""NodalEntity"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_NODAL_ENTITY = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "NodalEntity"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _129,
        _130,
        _131,
        _132,
        _133,
        _135,
        _136,
        _137,
        _138,
        _139,
        _140,
        _141,
        _142,
        _143,
        _144,
        _145,
        _146,
        _147,
        _148,
        _150,
        _151,
        _152,
        _153,
        _154,
        _155,
        _156,
        _157,
        _158,
    )
    from mastapy._private.nodal_analysis.nodal_entities.external_force import (
        _159,
        _160,
        _161,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2877,
    )

    Self = TypeVar("Self", bound="NodalEntity")
    CastSelf = TypeVar("CastSelf", bound="NodalEntity._Cast_NodalEntity")


__docformat__ = "restructuredtext en"
__all__ = ("NodalEntity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodalEntity:
    """Special nested class for casting NodalEntity to subclasses."""

    __parent__: "NodalEntity"

    @property
    def arbitrary_nodal_component(self: "CastSelf") -> "_129.ArbitraryNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _129

        return self.__parent__._cast(_129.ArbitraryNodalComponent)

    @property
    def bar(self: "CastSelf") -> "_130.Bar":
        from mastapy._private.nodal_analysis.nodal_entities import _130

        return self.__parent__._cast(_130.Bar)

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
    def bearing_axial_mounting_clearance(
        self: "CastSelf",
    ) -> "_135.BearingAxialMountingClearance":
        from mastapy._private.nodal_analysis.nodal_entities import _135

        return self.__parent__._cast(_135.BearingAxialMountingClearance)

    @property
    def cms_nodal_component(self: "CastSelf") -> "_136.CMSNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _136

        return self.__parent__._cast(_136.CMSNodalComponent)

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
    def distributed_rigid_bar_coupling(
        self: "CastSelf",
    ) -> "_139.DistributedRigidBarCoupling":
        from mastapy._private.nodal_analysis.nodal_entities import _139

        return self.__parent__._cast(_139.DistributedRigidBarCoupling)

    @property
    def friction_nodal_component(self: "CastSelf") -> "_140.FrictionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _140

        return self.__parent__._cast(_140.FrictionNodalComponent)

    @property
    def gear_mesh_nodal_component(self: "CastSelf") -> "_141.GearMeshNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _141

        return self.__parent__._cast(_141.GearMeshNodalComponent)

    @property
    def gear_mesh_node_pair(self: "CastSelf") -> "_142.GearMeshNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _142

        return self.__parent__._cast(_142.GearMeshNodePair)

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
    def inertial_force_component(self: "CastSelf") -> "_145.InertialForceComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _145

        return self.__parent__._cast(_145.InertialForceComponent)

    @property
    def line_contact_stiffness_entity(
        self: "CastSelf",
    ) -> "_146.LineContactStiffnessEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _146

        return self.__parent__._cast(_146.LineContactStiffnessEntity)

    @property
    def nodal_component(self: "CastSelf") -> "_147.NodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _147

        return self.__parent__._cast(_147.NodalComponent)

    @property
    def nodal_composite(self: "CastSelf") -> "_148.NodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _148

        return self.__parent__._cast(_148.NodalComposite)

    @property
    def null_nodal_entity(self: "CastSelf") -> "_150.NullNodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _150

        return self.__parent__._cast(_150.NullNodalEntity)

    @property
    def pid_control_nodal_component(
        self: "CastSelf",
    ) -> "_151.PIDControlNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _151

        return self.__parent__._cast(_151.PIDControlNodalComponent)

    @property
    def rigid_bar(self: "CastSelf") -> "_152.RigidBar":
        from mastapy._private.nodal_analysis.nodal_entities import _152

        return self.__parent__._cast(_152.RigidBar)

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
    def surface_to_surface_contact_stiffness_entity(
        self: "CastSelf",
    ) -> "_155.SurfaceToSurfaceContactStiffnessEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.SurfaceToSurfaceContactStiffnessEntity)

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
    def external_force_entity(self: "CastSelf") -> "_159.ExternalForceEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _159

        return self.__parent__._cast(_159.ExternalForceEntity)

    @property
    def external_force_line_contact_entity(
        self: "CastSelf",
    ) -> "_160.ExternalForceLineContactEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _160

        return self.__parent__._cast(_160.ExternalForceLineContactEntity)

    @property
    def external_force_single_point_entity(
        self: "CastSelf",
    ) -> "_161.ExternalForceSinglePointEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _161

        return self.__parent__._cast(_161.ExternalForceSinglePointEntity)

    @property
    def shaft_section_system_deflection(
        self: "CastSelf",
    ) -> "_2877.ShaftSectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2877,
        )

        return self.__parent__._cast(_2877.ShaftSectionSystemDeflection)

    @property
    def nodal_entity(self: "CastSelf") -> "NodalEntity":
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
class NodalEntity(_0.APIBase):
    """NodalEntity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODAL_ENTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_NodalEntity":
        """Cast to another type.

        Returns:
            _Cast_NodalEntity
        """
        return _Cast_NodalEntity(self)
