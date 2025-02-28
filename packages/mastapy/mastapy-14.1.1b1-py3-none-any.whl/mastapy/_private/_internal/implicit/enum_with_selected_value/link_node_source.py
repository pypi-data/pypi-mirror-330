"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.fe import _2462

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_LinkNodeSource")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_LinkNodeSource",)


class EnumWithSelectedValue_LinkNodeSource(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_LinkNodeSource

    A specific implementation of 'EnumWithSelectedValue' for 'LinkNodeSource' types.
    """

    __qualname__ = "LinkNodeSource"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_LinkNodeSource]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_LinkNodeSource]",
    ) -> "_2462.LinkNodeSource":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2462.LinkNodeSource
        """
        return _2462.LinkNodeSource

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_LinkNodeSource]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2462.LinkNodeSource.type_()

    @property
    def selected_value(self: "Self") -> "_2462.LinkNodeSource":
        """mastapy.system_model.fe.LinkNodeSource

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_2462.LinkNodeSource]":
        """List[mastapy.system_model.fe.LinkNodeSource]

        Note:
            This property is readonly.
        """
        return None
