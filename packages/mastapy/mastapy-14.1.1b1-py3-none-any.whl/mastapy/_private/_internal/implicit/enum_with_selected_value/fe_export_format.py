"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.fe_export_utility import _180

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_FEExportFormat")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_FEExportFormat",)


class EnumWithSelectedValue_FEExportFormat(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_FEExportFormat

    A specific implementation of 'EnumWithSelectedValue' for 'FEExportFormat' types.
    """

    __qualname__ = "FEExportFormat"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_FEExportFormat]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_FEExportFormat]",
    ) -> "_180.FEExportFormat":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _180.FEExportFormat
        """
        return _180.FEExportFormat

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_FEExportFormat]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _180.FEExportFormat.type_()

    @property
    def selected_value(self: "Self") -> "_180.FEExportFormat":
        """mastapy.nodal_analysis.fe_export_utility.FEExportFormat

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_180.FEExportFormat]":
        """List[mastapy.nodal_analysis.fe_export_utility.FEExportFormat]

        Note:
            This property is readonly.
        """
        return None
