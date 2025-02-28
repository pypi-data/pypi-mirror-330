"""ActiveShaftDesignSelectionGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.shafts import _46
from mastapy._private.system_model.part_model.configurations import _2690, _2695
from mastapy._private.system_model.part_model.shaft_model import _2549

_ACTIVE_SHAFT_DESIGN_SELECTION_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Configurations",
    "ActiveShaftDesignSelectionGroup",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ActiveShaftDesignSelectionGroup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ActiveShaftDesignSelectionGroup._Cast_ActiveShaftDesignSelectionGroup",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ActiveShaftDesignSelectionGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ActiveShaftDesignSelectionGroup:
    """Special nested class for casting ActiveShaftDesignSelectionGroup to subclasses."""

    __parent__: "ActiveShaftDesignSelectionGroup"

    @property
    def part_detail_configuration(self: "CastSelf") -> "_2695.PartDetailConfiguration":
        return self.__parent__._cast(_2695.PartDetailConfiguration)

    @property
    def active_shaft_design_selection_group(
        self: "CastSelf",
    ) -> "ActiveShaftDesignSelectionGroup":
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
class ActiveShaftDesignSelectionGroup(
    _2695.PartDetailConfiguration[
        _2690.ActiveShaftDesignSelection, _2549.Shaft, _46.SimpleShaftDefinition
    ]
):
    """ActiveShaftDesignSelectionGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ACTIVE_SHAFT_DESIGN_SELECTION_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ActiveShaftDesignSelectionGroup":
        """Cast to another type.

        Returns:
            _Cast_ActiveShaftDesignSelectionGroup
        """
        return _Cast_ActiveShaftDesignSelectionGroup(self)
