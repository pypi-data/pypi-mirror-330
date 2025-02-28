"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility_gui.charts._1913 import BubbleChartDefinition
    from mastapy._private.utility_gui.charts._1914 import ConstantLine
    from mastapy._private.utility_gui.charts._1915 import CustomLineChart
    from mastapy._private.utility_gui.charts._1916 import CustomTableAndChart
    from mastapy._private.utility_gui.charts._1917 import LegacyChartMathChartDefinition
    from mastapy._private.utility_gui.charts._1918 import MatrixVisualisationDefinition
    from mastapy._private.utility_gui.charts._1919 import ModeConstantLine
    from mastapy._private.utility_gui.charts._1920 import NDChartDefinition
    from mastapy._private.utility_gui.charts._1921 import (
        ParallelCoordinatesChartDefinition,
    )
    from mastapy._private.utility_gui.charts._1922 import PointsForSurface
    from mastapy._private.utility_gui.charts._1923 import ScatterChartDefinition
    from mastapy._private.utility_gui.charts._1924 import Series2D
    from mastapy._private.utility_gui.charts._1925 import SMTAxis
    from mastapy._private.utility_gui.charts._1926 import ThreeDChartDefinition
    from mastapy._private.utility_gui.charts._1927 import ThreeDVectorChartDefinition
    from mastapy._private.utility_gui.charts._1928 import TwoDChartDefinition
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility_gui.charts._1913": ["BubbleChartDefinition"],
        "_private.utility_gui.charts._1914": ["ConstantLine"],
        "_private.utility_gui.charts._1915": ["CustomLineChart"],
        "_private.utility_gui.charts._1916": ["CustomTableAndChart"],
        "_private.utility_gui.charts._1917": ["LegacyChartMathChartDefinition"],
        "_private.utility_gui.charts._1918": ["MatrixVisualisationDefinition"],
        "_private.utility_gui.charts._1919": ["ModeConstantLine"],
        "_private.utility_gui.charts._1920": ["NDChartDefinition"],
        "_private.utility_gui.charts._1921": ["ParallelCoordinatesChartDefinition"],
        "_private.utility_gui.charts._1922": ["PointsForSurface"],
        "_private.utility_gui.charts._1923": ["ScatterChartDefinition"],
        "_private.utility_gui.charts._1924": ["Series2D"],
        "_private.utility_gui.charts._1925": ["SMTAxis"],
        "_private.utility_gui.charts._1926": ["ThreeDChartDefinition"],
        "_private.utility_gui.charts._1927": ["ThreeDVectorChartDefinition"],
        "_private.utility_gui.charts._1928": ["TwoDChartDefinition"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BubbleChartDefinition",
    "ConstantLine",
    "CustomLineChart",
    "CustomTableAndChart",
    "LegacyChartMathChartDefinition",
    "MatrixVisualisationDefinition",
    "ModeConstantLine",
    "NDChartDefinition",
    "ParallelCoordinatesChartDefinition",
    "PointsForSurface",
    "ScatterChartDefinition",
    "Series2D",
    "SMTAxis",
    "ThreeDChartDefinition",
    "ThreeDVectorChartDefinition",
    "TwoDChartDefinition",
)
