"""RealVector"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility import _1583

_REAL_VECTOR = python_net_import("SMT.MastaAPI.MathUtility", "RealVector")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1567, _1572, _1582, _1593

    Self = TypeVar("Self", bound="RealVector")
    CastSelf = TypeVar("CastSelf", bound="RealVector._Cast_RealVector")


__docformat__ = "restructuredtext en"
__all__ = ("RealVector",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RealVector:
    """Special nested class for casting RealVector to subclasses."""

    __parent__: "RealVector"

    @property
    def real_matrix(self: "CastSelf") -> "_1583.RealMatrix":
        return self.__parent__._cast(_1583.RealMatrix)

    @property
    def generic_matrix(self: "CastSelf") -> "_1572.GenericMatrix":
        from mastapy._private.math_utility import _1572

        return self.__parent__._cast(_1572.GenericMatrix)

    @property
    def euler_parameters(self: "CastSelf") -> "_1567.EulerParameters":
        from mastapy._private.math_utility import _1567

        return self.__parent__._cast(_1567.EulerParameters)

    @property
    def quaternion(self: "CastSelf") -> "_1582.Quaternion":
        from mastapy._private.math_utility import _1582

        return self.__parent__._cast(_1582.Quaternion)

    @property
    def vector_6d(self: "CastSelf") -> "_1593.Vector6D":
        from mastapy._private.math_utility import _1593

        return self.__parent__._cast(_1593.Vector6D)

    @property
    def real_vector(self: "CastSelf") -> "RealVector":
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
class RealVector(_1583.RealMatrix):
    """RealVector

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _REAL_VECTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RealVector":
        """Cast to another type.

        Returns:
            _Cast_RealVector
        """
        return _Cast_RealVector(self)
