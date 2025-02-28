"""CoefficientOfFrictionCalculator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_COEFFICIENT_OF_FRICTION_CALCULATOR = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "CoefficientOfFrictionCalculator"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.materials import (
        _603,
        _615,
        _619,
        _620,
        _621,
        _622,
        _623,
        _625,
        _631,
        _632,
        _638,
    )

    Self = TypeVar("Self", bound="CoefficientOfFrictionCalculator")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CoefficientOfFrictionCalculator._Cast_CoefficientOfFrictionCalculator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoefficientOfFrictionCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CoefficientOfFrictionCalculator:
    """Special nested class for casting CoefficientOfFrictionCalculator to subclasses."""

    __parent__: "CoefficientOfFrictionCalculator"

    @property
    def benedict_and_kelley_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_603.BenedictAndKelleyCoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _603

        return self.__parent__._cast(
            _603.BenedictAndKelleyCoefficientOfFrictionCalculator
        )

    @property
    def drozdov_and_gavrikov_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_615.DrozdovAndGavrikovCoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _615

        return self.__parent__._cast(
            _615.DrozdovAndGavrikovCoefficientOfFrictionCalculator
        )

    @property
    def instantaneous_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_619.InstantaneousCoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _619

        return self.__parent__._cast(_619.InstantaneousCoefficientOfFrictionCalculator)

    @property
    def iso14179_part_1_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_620.ISO14179Part1CoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _620

        return self.__parent__._cast(_620.ISO14179Part1CoefficientOfFrictionCalculator)

    @property
    def iso14179_part_2_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_621.ISO14179Part2CoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _621

        return self.__parent__._cast(_621.ISO14179Part2CoefficientOfFrictionCalculator)

    @property
    def iso14179_part_2_coefficient_of_friction_calculator_base(
        self: "CastSelf",
    ) -> "_622.ISO14179Part2CoefficientOfFrictionCalculatorBase":
        from mastapy._private.gears.materials import _622

        return self.__parent__._cast(
            _622.ISO14179Part2CoefficientOfFrictionCalculatorBase
        )

    @property
    def iso14179_part_2_coefficient_of_friction_calculator_with_martins_modification(
        self: "CastSelf",
    ) -> "_623.ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification":
        from mastapy._private.gears.materials import _623

        return self.__parent__._cast(
            _623.ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification
        )

    @property
    def isotc60_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_625.ISOTC60CoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _625

        return self.__parent__._cast(_625.ISOTC60CoefficientOfFrictionCalculator)

    @property
    def misharin_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_631.MisharinCoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _631

        return self.__parent__._cast(_631.MisharinCoefficientOfFrictionCalculator)

    @property
    def o_donoghue_and_cameron_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_632.ODonoghueAndCameronCoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _632

        return self.__parent__._cast(
            _632.ODonoghueAndCameronCoefficientOfFrictionCalculator
        )

    @property
    def script_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_638.ScriptCoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _638

        return self.__parent__._cast(_638.ScriptCoefficientOfFrictionCalculator)

    @property
    def coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "CoefficientOfFrictionCalculator":
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
class CoefficientOfFrictionCalculator(_0.APIBase):
    """CoefficientOfFrictionCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COEFFICIENT_OF_FRICTION_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_CoefficientOfFrictionCalculator":
        """Cast to another type.

        Returns:
            _Cast_CoefficientOfFrictionCalculator
        """
        return _Cast_CoefficientOfFrictionCalculator(self)
