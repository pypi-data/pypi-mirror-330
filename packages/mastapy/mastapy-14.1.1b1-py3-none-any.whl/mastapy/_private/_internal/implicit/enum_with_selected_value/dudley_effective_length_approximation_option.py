"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.detailed_rigid_connectors.splines import _1453

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption",)


class EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption

    A specific implementation of 'EnumWithSelectedValue' for 'DudleyEffectiveLengthApproximationOption' types.
    """

    __qualname__ = "DudleyEffectiveLengthApproximationOption"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption]",
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
        cls: "Type[EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption]",
    ) -> "_1453.DudleyEffectiveLengthApproximationOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1453.DudleyEffectiveLengthApproximationOption
        """
        return _1453.DudleyEffectiveLengthApproximationOption

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1453.DudleyEffectiveLengthApproximationOption.type_()

    @property
    def selected_value(
        self: "Self",
    ) -> "_1453.DudleyEffectiveLengthApproximationOption":
        """mastapy.detailed_rigid_connectors.splines.DudleyEffectiveLengthApproximationOption

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(
        self: "Self",
    ) -> "List[_1453.DudleyEffectiveLengthApproximationOption]":
        """List[mastapy.detailed_rigid_connectors.splines.DudleyEffectiveLengthApproximationOption]

        Note:
            This property is readonly.
        """
        return None
