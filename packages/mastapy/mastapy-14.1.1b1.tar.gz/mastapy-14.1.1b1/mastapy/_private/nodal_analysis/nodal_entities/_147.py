"""NodalComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _149

_NODAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "NodalComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _129,
        _130,
        _135,
        _136,
        _139,
        _140,
        _142,
        _145,
        _146,
        _151,
        _152,
        _155,
    )
    from mastapy._private.nodal_analysis.nodal_entities.external_force import (
        _159,
        _160,
        _161,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2877,
    )

    Self = TypeVar("Self", bound="NodalComponent")
    CastSelf = TypeVar("CastSelf", bound="NodalComponent._Cast_NodalComponent")


__docformat__ = "restructuredtext en"
__all__ = ("NodalComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodalComponent:
    """Special nested class for casting NodalComponent to subclasses."""

    __parent__: "NodalComponent"

    @property
    def nodal_entity(self: "CastSelf") -> "_149.NodalEntity":
        return self.__parent__._cast(_149.NodalEntity)

    @property
    def arbitrary_nodal_component(self: "CastSelf") -> "_129.ArbitraryNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _129

        return self.__parent__._cast(_129.ArbitraryNodalComponent)

    @property
    def bar(self: "CastSelf") -> "_130.Bar":
        from mastapy._private.nodal_analysis.nodal_entities import _130

        return self.__parent__._cast(_130.Bar)

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
    def gear_mesh_node_pair(self: "CastSelf") -> "_142.GearMeshNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _142

        return self.__parent__._cast(_142.GearMeshNodePair)

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
    def surface_to_surface_contact_stiffness_entity(
        self: "CastSelf",
    ) -> "_155.SurfaceToSurfaceContactStiffnessEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.SurfaceToSurfaceContactStiffnessEntity)

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
    def nodal_component(self: "CastSelf") -> "NodalComponent":
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
class NodalComponent(_149.NodalEntity):
    """NodalComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NodalComponent":
        """Cast to another type.

        Returns:
            _Cast_NodalComponent
        """
        return _Cast_NodalComponent(self)
