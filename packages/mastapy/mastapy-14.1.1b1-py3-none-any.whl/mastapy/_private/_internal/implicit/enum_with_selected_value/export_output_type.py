"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5866

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ExportOutputType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ExportOutputType",)


class EnumWithSelectedValue_ExportOutputType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ExportOutputType

    A specific implementation of 'EnumWithSelectedValue' for 'ExportOutputType' types.
    """

    __qualname__ = "ExportOutputType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ExportOutputType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ExportOutputType]",
    ) -> "_5866.ExportOutputType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _5866.ExportOutputType
        """
        return _5866.ExportOutputType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_ExportOutputType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _5866.ExportOutputType.type_()

    @property
    def selected_value(self: "Self") -> "_5866.ExportOutputType":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.ExportOutputType

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_5866.ExportOutputType]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ExportOutputType]

        Note:
            This property is readonly.
        """
        return None
