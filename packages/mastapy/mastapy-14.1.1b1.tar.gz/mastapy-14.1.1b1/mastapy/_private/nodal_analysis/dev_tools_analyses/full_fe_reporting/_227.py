"""ElementPropertiesBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ELEMENT_PROPERTIES_BASE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "ElementPropertiesBase",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.fe_tools.enums import _1290
    from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
        _228,
        _229,
        _230,
        _231,
        _232,
        _233,
        _234,
        _235,
    )

    Self = TypeVar("Self", bound="ElementPropertiesBase")
    CastSelf = TypeVar(
        "CastSelf", bound="ElementPropertiesBase._Cast_ElementPropertiesBase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementPropertiesBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementPropertiesBase:
    """Special nested class for casting ElementPropertiesBase to subclasses."""

    __parent__: "ElementPropertiesBase"

    @property
    def element_properties_beam(self: "CastSelf") -> "_228.ElementPropertiesBeam":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _228,
        )

        return self.__parent__._cast(_228.ElementPropertiesBeam)

    @property
    def element_properties_interface(
        self: "CastSelf",
    ) -> "_229.ElementPropertiesInterface":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _229,
        )

        return self.__parent__._cast(_229.ElementPropertiesInterface)

    @property
    def element_properties_mass(self: "CastSelf") -> "_230.ElementPropertiesMass":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _230,
        )

        return self.__parent__._cast(_230.ElementPropertiesMass)

    @property
    def element_properties_rigid(self: "CastSelf") -> "_231.ElementPropertiesRigid":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _231,
        )

        return self.__parent__._cast(_231.ElementPropertiesRigid)

    @property
    def element_properties_shell(self: "CastSelf") -> "_232.ElementPropertiesShell":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _232,
        )

        return self.__parent__._cast(_232.ElementPropertiesShell)

    @property
    def element_properties_solid(self: "CastSelf") -> "_233.ElementPropertiesSolid":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _233,
        )

        return self.__parent__._cast(_233.ElementPropertiesSolid)

    @property
    def element_properties_spring_dashpot(
        self: "CastSelf",
    ) -> "_234.ElementPropertiesSpringDashpot":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _234,
        )

        return self.__parent__._cast(_234.ElementPropertiesSpringDashpot)

    @property
    def element_properties_with_material(
        self: "CastSelf",
    ) -> "_235.ElementPropertiesWithMaterial":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _235,
        )

        return self.__parent__._cast(_235.ElementPropertiesWithMaterial)

    @property
    def element_properties_base(self: "CastSelf") -> "ElementPropertiesBase":
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
class ElementPropertiesBase(_0.APIBase):
    """ElementPropertiesBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_PROPERTIES_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def class_(self: "Self") -> "_1290.ElementPropertyClass":
        """mastapy.fe_tools.enums.ElementPropertyClass

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Class")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.FETools.Enums.ElementPropertyClass"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.fe_tools.enums._1290", "ElementPropertyClass"
        )(value)

    @property
    def id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ID")

        if temp is None:
            return 0

        return temp

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
    def cast_to(self: "Self") -> "_Cast_ElementPropertiesBase":
        """Cast to another type.

        Returns:
            _Cast_ElementPropertiesBase
        """
        return _Cast_ElementPropertiesBase(self)
