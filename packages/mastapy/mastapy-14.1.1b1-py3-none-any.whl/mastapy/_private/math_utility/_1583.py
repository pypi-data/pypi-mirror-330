"""RealMatrix"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility import _1572

_REAL_MATRIX = python_net_import("SMT.MastaAPI.MathUtility", "RealMatrix")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1567, _1582, _1584, _1589, _1593

    Self = TypeVar("Self", bound="RealMatrix")
    CastSelf = TypeVar("CastSelf", bound="RealMatrix._Cast_RealMatrix")


__docformat__ = "restructuredtext en"
__all__ = ("RealMatrix",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RealMatrix:
    """Special nested class for casting RealMatrix to subclasses."""

    __parent__: "RealMatrix"

    @property
    def generic_matrix(self: "CastSelf") -> "_1572.GenericMatrix":
        pass

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
    def real_vector(self: "CastSelf") -> "_1584.RealVector":
        from mastapy._private.math_utility import _1584

        return self.__parent__._cast(_1584.RealVector)

    @property
    def square_matrix(self: "CastSelf") -> "_1589.SquareMatrix":
        from mastapy._private.math_utility import _1589

        return self.__parent__._cast(_1589.SquareMatrix)

    @property
    def vector_6d(self: "CastSelf") -> "_1593.Vector6D":
        from mastapy._private.math_utility import _1593

        return self.__parent__._cast(_1593.Vector6D)

    @property
    def real_matrix(self: "CastSelf") -> "RealMatrix":
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
class RealMatrix(_1572.GenericMatrix[float, "RealMatrix"]):
    """RealMatrix

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _REAL_MATRIX

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @enforce_parameter_types
    def get_column_at(self: "Self", index: "int") -> "List[float]":
        """List[float]

        Args:
            index (int)
        """
        index = int(index)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(self.wrapped, "GetColumnAt", index if index else 0),
            float,
        )

    @enforce_parameter_types
    def get_row_at(self: "Self", index: "int") -> "List[float]":
        """List[float]

        Args:
            index (int)
        """
        index = int(index)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(self.wrapped, "GetRowAt", index if index else 0),
            float,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RealMatrix":
        """Cast to another type.

        Returns:
            _Cast_RealMatrix
        """
        return _Cast_RealMatrix(self)
