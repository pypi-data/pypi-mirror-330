"""ConcentricOrParallelPartGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.part_groups import _2559

_CONCENTRIC_OR_PARALLEL_PART_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.PartGroups", "ConcentricOrParallelPartGroup"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.part_groups import _2554, _2557, _2558

    Self = TypeVar("Self", bound="ConcentricOrParallelPartGroup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConcentricOrParallelPartGroup._Cast_ConcentricOrParallelPartGroup",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConcentricOrParallelPartGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConcentricOrParallelPartGroup:
    """Special nested class for casting ConcentricOrParallelPartGroup to subclasses."""

    __parent__: "ConcentricOrParallelPartGroup"

    @property
    def part_group(self: "CastSelf") -> "_2559.PartGroup":
        return self.__parent__._cast(_2559.PartGroup)

    @property
    def concentric_part_group(self: "CastSelf") -> "_2554.ConcentricPartGroup":
        from mastapy._private.system_model.part_model.part_groups import _2554

        return self.__parent__._cast(_2554.ConcentricPartGroup)

    @property
    def parallel_part_group(self: "CastSelf") -> "_2557.ParallelPartGroup":
        from mastapy._private.system_model.part_model.part_groups import _2557

        return self.__parent__._cast(_2557.ParallelPartGroup)

    @property
    def parallel_part_group_selection(
        self: "CastSelf",
    ) -> "_2558.ParallelPartGroupSelection":
        from mastapy._private.system_model.part_model.part_groups import _2558

        return self.__parent__._cast(_2558.ParallelPartGroupSelection)

    @property
    def concentric_or_parallel_part_group(
        self: "CastSelf",
    ) -> "ConcentricOrParallelPartGroup":
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
class ConcentricOrParallelPartGroup(_2559.PartGroup):
    """ConcentricOrParallelPartGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCENTRIC_OR_PARALLEL_PART_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConcentricOrParallelPartGroup":
        """Cast to another type.

        Returns:
            _Cast_ConcentricOrParallelPartGroup
        """
        return _Cast_ConcentricOrParallelPartGroup(self)
