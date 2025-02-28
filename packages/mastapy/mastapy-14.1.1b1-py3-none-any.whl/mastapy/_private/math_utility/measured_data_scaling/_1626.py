"""DataScalingOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility import _1564
from mastapy._private.utility.units_and_measurements.measurements import (
    _1670,
    _1671,
    _1673,
    _1674,
    _1675,
    _1679,
    _1687,
    _1694,
    _1697,
    _1700,
    _1706,
    _1723,
    _1725,
    _1728,
    _1734,
    _1742,
    _1746,
    _1747,
    _1748,
    _1751,
    _1752,
    _1759,
    _1768,
    _1773,
    _1774,
    _1782,
    _1783,
    _1784,
    _1785,
    _1786,
    _1790,
    _1791,
)

_DATA_SCALING_OPTIONS = python_net_import(
    "SMT.MastaAPI.MathUtility.MeasuredDataScaling", "DataScalingOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1548
    from mastapy._private.math_utility.measured_data_scaling import _1627

    Self = TypeVar("Self", bound="DataScalingOptions")
    CastSelf = TypeVar("CastSelf", bound="DataScalingOptions._Cast_DataScalingOptions")


__docformat__ = "restructuredtext en"
__all__ = ("DataScalingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DataScalingOptions:
    """Special nested class for casting DataScalingOptions to subclasses."""

    __parent__: "DataScalingOptions"

    @property
    def data_scaling_options(self: "CastSelf") -> "DataScalingOptions":
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
class DataScalingOptions(_0.APIBase):
    """DataScalingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATA_SCALING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def dynamic_scaling(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling":
        """EnumWithSelectedValue[mastapy.math_utility.DynamicsResponseScaling]"""
        temp = pythonnet_property_get(self.wrapped, "DynamicScaling")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @dynamic_scaling.setter
    @enforce_parameter_types
    def dynamic_scaling(self: "Self", value: "_1564.DynamicsResponseScaling") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DynamicScaling", value)

    @property
    def weighting(self: "Self") -> "_1548.AcousticWeighting":
        """mastapy.math_utility.AcousticWeighting"""
        temp = pythonnet_property_get(self.wrapped, "Weighting")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.MathUtility.AcousticWeighting"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1548", "AcousticWeighting"
        )(value)

    @weighting.setter
    @enforce_parameter_types
    def weighting(self: "Self", value: "_1548.AcousticWeighting") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.MathUtility.AcousticWeighting"
        )
        pythonnet_property_set(self.wrapped, "Weighting", value)

    @property
    def acceleration_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1670.Acceleration]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Acceleration]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AccelerationReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1670.Acceleration](temp)

    @property
    def angle_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1671.Angle]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Angle]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngleReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1671.Angle](temp)

    @property
    def angular_acceleration_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1675.AngularAcceleration]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.AngularAcceleration]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngularAccelerationReferenceValues"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1675.AngularAcceleration](
            temp
        )

    @property
    def angular_velocity_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1679.AngularVelocity]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.AngularVelocity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularVelocityReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1679.AngularVelocity](temp)

    @property
    def damage_rate(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1687.DamageRate]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.DamageRate]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageRate")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1687.DamageRate](temp)

    @property
    def energy_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1694.Energy]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Energy]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnergyReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1694.Energy](temp)

    @property
    def force_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1700.Force]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Force]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1700.Force](temp)

    @property
    def frequency_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1706.Frequency]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Frequency]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1706.Frequency](temp)

    @property
    def linear_stiffness_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1734.LinearStiffness]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.LinearStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearStiffnessReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1734.LinearStiffness](temp)

    @property
    def mass_per_unit_time_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1742.MassPerUnitTime]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.MassPerUnitTime]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassPerUnitTimeReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1742.MassPerUnitTime](temp)

    @property
    def medium_length_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1723.LengthMedium]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.LengthMedium]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MediumLengthReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1723.LengthMedium](temp)

    @property
    def percentage(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1747.Percentage]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Percentage]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Percentage")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1747.Percentage](temp)

    @property
    def power_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1748.Power]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Power]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1748.Power](temp)

    @property
    def power_small_per_unit_area_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1752.PowerSmallPerArea]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.PowerSmallPerArea]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerSmallPerUnitAreaReferenceValues"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1752.PowerSmallPerArea](
            temp
        )

    @property
    def power_small_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1751.PowerSmall]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.PowerSmall]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerSmallReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1751.PowerSmall](temp)

    @property
    def pressure_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1759.PressureSmall]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.PressureSmall]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1759.PressureSmall](temp)

    @property
    def safety_factor(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1768.SafetyFactor]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.SafetyFactor]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1768.SafetyFactor](temp)

    @property
    def short_length_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1725.LengthShort]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShortLengthReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1725.LengthShort](temp)

    @property
    def short_time_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1782.TimeShort]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.TimeShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShortTimeReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1782.TimeShort](temp)

    @property
    def small_angle_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1673.AngleSmall]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.AngleSmall]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallAngleReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1673.AngleSmall](temp)

    @property
    def small_energy_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1697.EnergySmall]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.EnergySmall]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallEnergyReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1697.EnergySmall](temp)

    @property
    def small_velocity_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1791.VelocitySmall]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.VelocitySmall]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallVelocityReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1791.VelocitySmall](temp)

    @property
    def stress_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1773.Stress]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Stress]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1773.Stress](temp)

    @property
    def temperature_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1774.Temperature]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Temperature]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TemperatureReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1774.Temperature](temp)

    @property
    def torque_converter_inverse_k(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1785.TorqueConverterInverseK]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.TorqueConverterInverseK]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueConverterInverseK")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _1785.TorqueConverterInverseK
        ](temp)

    @property
    def torque_converter_k(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1786.TorqueConverterK]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.TorqueConverterK]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueConverterK")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1786.TorqueConverterK](
            temp
        )

    @property
    def torque_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1784.Torque]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Torque]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1784.Torque](temp)

    @property
    def unmeasureable(self: "Self") -> "_1627.DataScalingReferenceValues[_1746.Number]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Number]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Unmeasureable")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1746.Number](temp)

    @property
    def velocity_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1790.Velocity]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Velocity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VelocityReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1790.Velocity](temp)

    @property
    def very_short_length_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1728.LengthVeryShort]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.LengthVeryShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VeryShortLengthReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1728.LengthVeryShort](temp)

    @property
    def very_short_time_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1783.TimeVeryShort]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.TimeVeryShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VeryShortTimeReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1783.TimeVeryShort](temp)

    @property
    def very_small_angle_reference_values(
        self: "Self",
    ) -> "_1627.DataScalingReferenceValues[_1674.AngleVerySmall]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.AngleVerySmall]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VerySmallAngleReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1674.AngleVerySmall](temp)

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
    def cast_to(self: "Self") -> "_Cast_DataScalingOptions":
        """Cast to another type.

        Returns:
            _Cast_DataScalingOptions
        """
        return _Cast_DataScalingOptions(self)
