"""CADWoundFieldSynchronousRotor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.electric_machines import _1299

_CAD_WOUND_FIELD_SYNCHRONOUS_ROTOR = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "CADWoundFieldSynchronousRotor"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1348

    Self = TypeVar("Self", bound="CADWoundFieldSynchronousRotor")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CADWoundFieldSynchronousRotor._Cast_CADWoundFieldSynchronousRotor",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CADWoundFieldSynchronousRotor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CADWoundFieldSynchronousRotor:
    """Special nested class for casting CADWoundFieldSynchronousRotor to subclasses."""

    __parent__: "CADWoundFieldSynchronousRotor"

    @property
    def cad_rotor(self: "CastSelf") -> "_1299.CADRotor":
        return self.__parent__._cast(_1299.CADRotor)

    @property
    def rotor(self: "CastSelf") -> "_1348.Rotor":
        from mastapy._private.electric_machines import _1348

        return self.__parent__._cast(_1348.Rotor)

    @property
    def cad_wound_field_synchronous_rotor(
        self: "CastSelf",
    ) -> "CADWoundFieldSynchronousRotor":
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
class CADWoundFieldSynchronousRotor(_1299.CADRotor):
    """CADWoundFieldSynchronousRotor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CAD_WOUND_FIELD_SYNCHRONOUS_ROTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CADWoundFieldSynchronousRotor":
        """Cast to another type.

        Returns:
            _Cast_CADWoundFieldSynchronousRotor
        """
        return _Cast_CADWoundFieldSynchronousRotor(self)
