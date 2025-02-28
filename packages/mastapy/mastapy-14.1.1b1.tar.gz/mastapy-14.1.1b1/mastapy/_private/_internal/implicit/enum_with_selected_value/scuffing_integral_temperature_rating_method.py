"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.cylindrical import _501

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod",)


class EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ScuffingIntegralTemperatureRatingMethod' types.
    """

    __qualname__ = "ScuffingIntegralTemperatureRatingMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod]",
    ) -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod]",
    ) -> "_501.ScuffingIntegralTemperatureRatingMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _501.ScuffingIntegralTemperatureRatingMethod
        """
        return _501.ScuffingIntegralTemperatureRatingMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _501.ScuffingIntegralTemperatureRatingMethod.type_()

    @property
    def selected_value(self: "Self") -> "_501.ScuffingIntegralTemperatureRatingMethod":
        """mastapy.gears.rating.cylindrical.ScuffingIntegralTemperatureRatingMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(
        self: "Self",
    ) -> "List[_501.ScuffingIntegralTemperatureRatingMethod]":
        """List[mastapy.gears.rating.cylindrical.ScuffingIntegralTemperatureRatingMethod]

        Note:
            This property is readonly.
        """
        return None
