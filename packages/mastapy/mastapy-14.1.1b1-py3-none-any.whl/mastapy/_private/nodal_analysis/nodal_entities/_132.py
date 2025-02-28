"""BarMBD"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _137

_BAR_MBD = python_net_import("SMT.MastaAPI.NodalAnalysis.NodalEntities", "BarMBD")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _131, _133, _148, _149

    Self = TypeVar("Self", bound="BarMBD")
    CastSelf = TypeVar("CastSelf", bound="BarMBD._Cast_BarMBD")


__docformat__ = "restructuredtext en"
__all__ = ("BarMBD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BarMBD:
    """Special nested class for casting BarMBD to subclasses."""

    __parent__: "BarMBD"

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
    def bar_elastic_mbd(self: "CastSelf") -> "_131.BarElasticMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _131

        return self.__parent__._cast(_131.BarElasticMBD)

    @property
    def bar_rigid_mbd(self: "CastSelf") -> "_133.BarRigidMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _133

        return self.__parent__._cast(_133.BarRigidMBD)

    @property
    def bar_mbd(self: "CastSelf") -> "BarMBD":
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
class BarMBD(_137.ComponentNodalComposite):
    """BarMBD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BAR_MBD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BarMBD":
        """Cast to another type.

        Returns:
            _Cast_BarMBD
        """
        return _Cast_BarMBD(self)
