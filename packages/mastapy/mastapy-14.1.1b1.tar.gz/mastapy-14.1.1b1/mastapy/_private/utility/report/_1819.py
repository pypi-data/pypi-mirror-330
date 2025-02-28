"""CustomReportDefinitionItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1830

_CUSTOM_REPORT_DEFINITION_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportDefinitionItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2009
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4484,
    )
    from mastapy._private.utility.report import (
        _1801,
        _1809,
        _1810,
        _1811,
        _1812,
        _1821,
        _1822,
        _1833,
        _1836,
        _1838,
    )

    Self = TypeVar("Self", bound="CustomReportDefinitionItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportDefinitionItem._Cast_CustomReportDefinitionItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportDefinitionItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportDefinitionItem:
    """Special nested class for casting CustomReportDefinitionItem to subclasses."""

    __parent__: "CustomReportDefinitionItem"

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1830.CustomReportNameableItem":
        return self.__parent__._cast(_1830.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1822.CustomReportItem":
        from mastapy._private.utility.report import _1822

        return self.__parent__._cast(_1822.CustomReportItem)

    @property
    def ad_hoc_custom_table(self: "CastSelf") -> "_1801.AdHocCustomTable":
        from mastapy._private.utility.report import _1801

        return self.__parent__._cast(_1801.AdHocCustomTable)

    @property
    def custom_chart(self: "CastSelf") -> "_1809.CustomChart":
        from mastapy._private.utility.report import _1809

        return self.__parent__._cast(_1809.CustomChart)

    @property
    def custom_drawing(self: "CastSelf") -> "_1810.CustomDrawing":
        from mastapy._private.utility.report import _1810

        return self.__parent__._cast(_1810.CustomDrawing)

    @property
    def custom_graphic(self: "CastSelf") -> "_1811.CustomGraphic":
        from mastapy._private.utility.report import _1811

        return self.__parent__._cast(_1811.CustomGraphic)

    @property
    def custom_image(self: "CastSelf") -> "_1812.CustomImage":
        from mastapy._private.utility.report import _1812

        return self.__parent__._cast(_1812.CustomImage)

    @property
    def custom_report_html_item(self: "CastSelf") -> "_1821.CustomReportHtmlItem":
        from mastapy._private.utility.report import _1821

        return self.__parent__._cast(_1821.CustomReportHtmlItem)

    @property
    def custom_report_status_item(self: "CastSelf") -> "_1833.CustomReportStatusItem":
        from mastapy._private.utility.report import _1833

        return self.__parent__._cast(_1833.CustomReportStatusItem)

    @property
    def custom_report_text(self: "CastSelf") -> "_1836.CustomReportText":
        from mastapy._private.utility.report import _1836

        return self.__parent__._cast(_1836.CustomReportText)

    @property
    def custom_sub_report(self: "CastSelf") -> "_1838.CustomSubReport":
        from mastapy._private.utility.report import _1838

        return self.__parent__._cast(_1838.CustomSubReport)

    @property
    def loaded_bearing_chart_reporter(
        self: "CastSelf",
    ) -> "_2009.LoadedBearingChartReporter":
        from mastapy._private.bearings.bearing_results import _2009

        return self.__parent__._cast(_2009.LoadedBearingChartReporter)

    @property
    def parametric_study_histogram(
        self: "CastSelf",
    ) -> "_4484.ParametricStudyHistogram":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4484,
        )

        return self.__parent__._cast(_4484.ParametricStudyHistogram)

    @property
    def custom_report_definition_item(self: "CastSelf") -> "CustomReportDefinitionItem":
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
class CustomReportDefinitionItem(_1830.CustomReportNameableItem):
    """CustomReportDefinitionItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_DEFINITION_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportDefinitionItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportDefinitionItem
        """
        return _Cast_CustomReportDefinitionItem(self)
