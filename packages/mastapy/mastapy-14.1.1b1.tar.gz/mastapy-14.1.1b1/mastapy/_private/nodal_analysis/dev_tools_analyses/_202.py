"""FEEntityGroupInteger"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.dev_tools_analyses import _201

_FE_ENTITY_GROUP_INTEGER = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "FEEntityGroupInteger"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.component_mode_synthesis import _246
    from mastapy._private.nodal_analysis.dev_tools_analyses import _200, _219

    Self = TypeVar("Self", bound="FEEntityGroupInteger")
    CastSelf = TypeVar(
        "CastSelf", bound="FEEntityGroupInteger._Cast_FEEntityGroupInteger"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEEntityGroupInteger",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEEntityGroupInteger:
    """Special nested class for casting FEEntityGroupInteger to subclasses."""

    __parent__: "FEEntityGroupInteger"

    @property
    def fe_entity_group(self: "CastSelf") -> "_201.FEEntityGroup":
        return self.__parent__._cast(_201.FEEntityGroup)

    @property
    def element_group(self: "CastSelf") -> "_200.ElementGroup":
        from mastapy._private.nodal_analysis.dev_tools_analyses import _200

        return self.__parent__._cast(_200.ElementGroup)

    @property
    def node_group(self: "CastSelf") -> "_219.NodeGroup":
        from mastapy._private.nodal_analysis.dev_tools_analyses import _219

        return self.__parent__._cast(_219.NodeGroup)

    @property
    def cms_node_group(self: "CastSelf") -> "_246.CMSNodeGroup":
        from mastapy._private.nodal_analysis.component_mode_synthesis import _246

        return self.__parent__._cast(_246.CMSNodeGroup)

    @property
    def fe_entity_group_integer(self: "CastSelf") -> "FEEntityGroupInteger":
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
class FEEntityGroupInteger(_201.FEEntityGroup[int]):
    """FEEntityGroupInteger

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_ENTITY_GROUP_INTEGER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FEEntityGroupInteger":
        """Cast to another type.

        Returns:
            _Cast_FEEntityGroupInteger
        """
        return _Cast_FEEntityGroupInteger(self)
