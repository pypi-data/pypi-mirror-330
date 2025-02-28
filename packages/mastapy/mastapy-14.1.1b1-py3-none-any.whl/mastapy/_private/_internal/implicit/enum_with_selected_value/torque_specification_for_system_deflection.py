"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.static_loads import _7666

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_TorqueSpecificationForSystemDeflection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_TorqueSpecificationForSystemDeflection",)


class EnumWithSelectedValue_TorqueSpecificationForSystemDeflection(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_TorqueSpecificationForSystemDeflection

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueSpecificationForSystemDeflection' types.
    """

    __qualname__ = "TorqueSpecificationForSystemDeflection"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_TorqueSpecificationForSystemDeflection]",
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
        cls: "Type[EnumWithSelectedValue_TorqueSpecificationForSystemDeflection]",
    ) -> "_7666.TorqueSpecificationForSystemDeflection":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _7666.TorqueSpecificationForSystemDeflection
        """
        return _7666.TorqueSpecificationForSystemDeflection

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_TorqueSpecificationForSystemDeflection]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _7666.TorqueSpecificationForSystemDeflection.type_()

    @property
    def selected_value(self: "Self") -> "_7666.TorqueSpecificationForSystemDeflection":
        """mastapy.system_model.analyses_and_results.static_loads.TorqueSpecificationForSystemDeflection

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(
        self: "Self",
    ) -> "List[_7666.TorqueSpecificationForSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.static_loads.TorqueSpecificationForSystemDeflection]

        Note:
            This property is readonly.
        """
        return None
