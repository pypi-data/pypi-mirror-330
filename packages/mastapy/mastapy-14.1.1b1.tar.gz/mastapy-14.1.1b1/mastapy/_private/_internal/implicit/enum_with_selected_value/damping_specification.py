"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5851

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_DampingSpecification")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_DampingSpecification",)


class EnumWithSelectedValue_DampingSpecification(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_DampingSpecification

    A specific implementation of 'EnumWithSelectedValue' for 'DampingSpecification' types.
    """

    __qualname__ = "DampingSpecification"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_DampingSpecification]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_DampingSpecification]",
    ) -> "_5851.DampingSpecification":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _5851.DampingSpecification
        """
        return _5851.DampingSpecification

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_DampingSpecification]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _5851.DampingSpecification.type_()

    @property
    def selected_value(self: "Self") -> "_5851.DampingSpecification":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.DampingSpecification

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_5851.DampingSpecification]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.DampingSpecification]

        Note:
            This property is readonly.
        """
        return None
