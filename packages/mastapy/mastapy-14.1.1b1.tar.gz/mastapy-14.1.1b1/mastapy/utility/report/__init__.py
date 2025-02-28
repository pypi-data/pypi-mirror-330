"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.report._1801 import AdHocCustomTable
    from mastapy._private.utility.report._1802 import AxisSettings
    from mastapy._private.utility.report._1803 import BlankRow
    from mastapy._private.utility.report._1804 import CadPageOrientation
    from mastapy._private.utility.report._1805 import CadPageSize
    from mastapy._private.utility.report._1806 import CadTableBorderType
    from mastapy._private.utility.report._1807 import ChartDefinition
    from mastapy._private.utility.report._1808 import SMTChartPointShape
    from mastapy._private.utility.report._1809 import CustomChart
    from mastapy._private.utility.report._1810 import CustomDrawing
    from mastapy._private.utility.report._1811 import CustomGraphic
    from mastapy._private.utility.report._1812 import CustomImage
    from mastapy._private.utility.report._1813 import CustomReport
    from mastapy._private.utility.report._1814 import CustomReportCadDrawing
    from mastapy._private.utility.report._1815 import CustomReportChart
    from mastapy._private.utility.report._1816 import CustomReportChartItem
    from mastapy._private.utility.report._1817 import CustomReportColumn
    from mastapy._private.utility.report._1818 import CustomReportColumns
    from mastapy._private.utility.report._1819 import CustomReportDefinitionItem
    from mastapy._private.utility.report._1820 import CustomReportHorizontalLine
    from mastapy._private.utility.report._1821 import CustomReportHtmlItem
    from mastapy._private.utility.report._1822 import CustomReportItem
    from mastapy._private.utility.report._1823 import CustomReportItemContainer
    from mastapy._private.utility.report._1824 import (
        CustomReportItemContainerCollection,
    )
    from mastapy._private.utility.report._1825 import (
        CustomReportItemContainerCollectionBase,
    )
    from mastapy._private.utility.report._1826 import (
        CustomReportItemContainerCollectionItem,
    )
    from mastapy._private.utility.report._1827 import CustomReportKey
    from mastapy._private.utility.report._1828 import CustomReportMultiPropertyItem
    from mastapy._private.utility.report._1829 import CustomReportMultiPropertyItemBase
    from mastapy._private.utility.report._1830 import CustomReportNameableItem
    from mastapy._private.utility.report._1831 import CustomReportNamedItem
    from mastapy._private.utility.report._1832 import CustomReportPropertyItem
    from mastapy._private.utility.report._1833 import CustomReportStatusItem
    from mastapy._private.utility.report._1834 import CustomReportTab
    from mastapy._private.utility.report._1835 import CustomReportTabs
    from mastapy._private.utility.report._1836 import CustomReportText
    from mastapy._private.utility.report._1837 import CustomRow
    from mastapy._private.utility.report._1838 import CustomSubReport
    from mastapy._private.utility.report._1839 import CustomTable
    from mastapy._private.utility.report._1840 import DefinitionBooleanCheckOptions
    from mastapy._private.utility.report._1841 import DynamicCustomReportItem
    from mastapy._private.utility.report._1842 import FontStyle
    from mastapy._private.utility.report._1843 import FontWeight
    from mastapy._private.utility.report._1844 import HeadingSize
    from mastapy._private.utility.report._1845 import SimpleChartDefinition
    from mastapy._private.utility.report._1846 import UserTextRow
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.report._1801": ["AdHocCustomTable"],
        "_private.utility.report._1802": ["AxisSettings"],
        "_private.utility.report._1803": ["BlankRow"],
        "_private.utility.report._1804": ["CadPageOrientation"],
        "_private.utility.report._1805": ["CadPageSize"],
        "_private.utility.report._1806": ["CadTableBorderType"],
        "_private.utility.report._1807": ["ChartDefinition"],
        "_private.utility.report._1808": ["SMTChartPointShape"],
        "_private.utility.report._1809": ["CustomChart"],
        "_private.utility.report._1810": ["CustomDrawing"],
        "_private.utility.report._1811": ["CustomGraphic"],
        "_private.utility.report._1812": ["CustomImage"],
        "_private.utility.report._1813": ["CustomReport"],
        "_private.utility.report._1814": ["CustomReportCadDrawing"],
        "_private.utility.report._1815": ["CustomReportChart"],
        "_private.utility.report._1816": ["CustomReportChartItem"],
        "_private.utility.report._1817": ["CustomReportColumn"],
        "_private.utility.report._1818": ["CustomReportColumns"],
        "_private.utility.report._1819": ["CustomReportDefinitionItem"],
        "_private.utility.report._1820": ["CustomReportHorizontalLine"],
        "_private.utility.report._1821": ["CustomReportHtmlItem"],
        "_private.utility.report._1822": ["CustomReportItem"],
        "_private.utility.report._1823": ["CustomReportItemContainer"],
        "_private.utility.report._1824": ["CustomReportItemContainerCollection"],
        "_private.utility.report._1825": ["CustomReportItemContainerCollectionBase"],
        "_private.utility.report._1826": ["CustomReportItemContainerCollectionItem"],
        "_private.utility.report._1827": ["CustomReportKey"],
        "_private.utility.report._1828": ["CustomReportMultiPropertyItem"],
        "_private.utility.report._1829": ["CustomReportMultiPropertyItemBase"],
        "_private.utility.report._1830": ["CustomReportNameableItem"],
        "_private.utility.report._1831": ["CustomReportNamedItem"],
        "_private.utility.report._1832": ["CustomReportPropertyItem"],
        "_private.utility.report._1833": ["CustomReportStatusItem"],
        "_private.utility.report._1834": ["CustomReportTab"],
        "_private.utility.report._1835": ["CustomReportTabs"],
        "_private.utility.report._1836": ["CustomReportText"],
        "_private.utility.report._1837": ["CustomRow"],
        "_private.utility.report._1838": ["CustomSubReport"],
        "_private.utility.report._1839": ["CustomTable"],
        "_private.utility.report._1840": ["DefinitionBooleanCheckOptions"],
        "_private.utility.report._1841": ["DynamicCustomReportItem"],
        "_private.utility.report._1842": ["FontStyle"],
        "_private.utility.report._1843": ["FontWeight"],
        "_private.utility.report._1844": ["HeadingSize"],
        "_private.utility.report._1845": ["SimpleChartDefinition"],
        "_private.utility.report._1846": ["UserTextRow"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdHocCustomTable",
    "AxisSettings",
    "BlankRow",
    "CadPageOrientation",
    "CadPageSize",
    "CadTableBorderType",
    "ChartDefinition",
    "SMTChartPointShape",
    "CustomChart",
    "CustomDrawing",
    "CustomGraphic",
    "CustomImage",
    "CustomReport",
    "CustomReportCadDrawing",
    "CustomReportChart",
    "CustomReportChartItem",
    "CustomReportColumn",
    "CustomReportColumns",
    "CustomReportDefinitionItem",
    "CustomReportHorizontalLine",
    "CustomReportHtmlItem",
    "CustomReportItem",
    "CustomReportItemContainer",
    "CustomReportItemContainerCollection",
    "CustomReportItemContainerCollectionBase",
    "CustomReportItemContainerCollectionItem",
    "CustomReportKey",
    "CustomReportMultiPropertyItem",
    "CustomReportMultiPropertyItemBase",
    "CustomReportNameableItem",
    "CustomReportNamedItem",
    "CustomReportPropertyItem",
    "CustomReportStatusItem",
    "CustomReportTab",
    "CustomReportTabs",
    "CustomReportText",
    "CustomRow",
    "CustomSubReport",
    "CustomTable",
    "DefinitionBooleanCheckOptions",
    "DynamicCustomReportItem",
    "FontStyle",
    "FontWeight",
    "HeadingSize",
    "SimpleChartDefinition",
    "UserTextRow",
)
