"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility._1548 import AcousticWeighting
    from mastapy._private.math_utility._1549 import AlignmentAxis
    from mastapy._private.math_utility._1550 import Axis
    from mastapy._private.math_utility._1551 import CirclesOnAxis
    from mastapy._private.math_utility._1552 import ComplexMatrix
    from mastapy._private.math_utility._1553 import ComplexPartDisplayOption
    from mastapy._private.math_utility._1554 import ComplexVector
    from mastapy._private.math_utility._1555 import ComplexVector3D
    from mastapy._private.math_utility._1556 import ComplexVector6D
    from mastapy._private.math_utility._1557 import CoordinateSystem3D
    from mastapy._private.math_utility._1558 import CoordinateSystemEditor
    from mastapy._private.math_utility._1559 import CoordinateSystemForRotation
    from mastapy._private.math_utility._1560 import CoordinateSystemForRotationOrigin
    from mastapy._private.math_utility._1561 import DataPrecision
    from mastapy._private.math_utility._1562 import DegreeOfFreedom
    from mastapy._private.math_utility._1563 import DynamicsResponseScalarResult
    from mastapy._private.math_utility._1564 import DynamicsResponseScaling
    from mastapy._private.math_utility._1565 import Eigenmode
    from mastapy._private.math_utility._1566 import Eigenmodes
    from mastapy._private.math_utility._1567 import EulerParameters
    from mastapy._private.math_utility._1568 import ExtrapolationOptions
    from mastapy._private.math_utility._1569 import FacetedBody
    from mastapy._private.math_utility._1570 import FacetedSurface
    from mastapy._private.math_utility._1571 import FourierSeries
    from mastapy._private.math_utility._1572 import GenericMatrix
    from mastapy._private.math_utility._1573 import GriddedSurface
    from mastapy._private.math_utility._1574 import HarmonicValue
    from mastapy._private.math_utility._1575 import InertiaTensor
    from mastapy._private.math_utility._1576 import MassProperties
    from mastapy._private.math_utility._1577 import MaxMinMean
    from mastapy._private.math_utility._1578 import ComplexMagnitudeMethod
    from mastapy._private.math_utility._1579 import MultipleFourierSeriesInterpolator
    from mastapy._private.math_utility._1580 import Named2DLocation
    from mastapy._private.math_utility._1581 import PIDControlUpdateMethod
    from mastapy._private.math_utility._1582 import Quaternion
    from mastapy._private.math_utility._1583 import RealMatrix
    from mastapy._private.math_utility._1584 import RealVector
    from mastapy._private.math_utility._1585 import ResultOptionsFor3DVector
    from mastapy._private.math_utility._1586 import RotationAxis
    from mastapy._private.math_utility._1587 import RoundedOrder
    from mastapy._private.math_utility._1588 import SinCurve
    from mastapy._private.math_utility._1589 import SquareMatrix
    from mastapy._private.math_utility._1590 import StressPoint
    from mastapy._private.math_utility._1591 import TranslationRotation
    from mastapy._private.math_utility._1592 import Vector2DListAccessor
    from mastapy._private.math_utility._1593 import Vector6D
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility._1548": ["AcousticWeighting"],
        "_private.math_utility._1549": ["AlignmentAxis"],
        "_private.math_utility._1550": ["Axis"],
        "_private.math_utility._1551": ["CirclesOnAxis"],
        "_private.math_utility._1552": ["ComplexMatrix"],
        "_private.math_utility._1553": ["ComplexPartDisplayOption"],
        "_private.math_utility._1554": ["ComplexVector"],
        "_private.math_utility._1555": ["ComplexVector3D"],
        "_private.math_utility._1556": ["ComplexVector6D"],
        "_private.math_utility._1557": ["CoordinateSystem3D"],
        "_private.math_utility._1558": ["CoordinateSystemEditor"],
        "_private.math_utility._1559": ["CoordinateSystemForRotation"],
        "_private.math_utility._1560": ["CoordinateSystemForRotationOrigin"],
        "_private.math_utility._1561": ["DataPrecision"],
        "_private.math_utility._1562": ["DegreeOfFreedom"],
        "_private.math_utility._1563": ["DynamicsResponseScalarResult"],
        "_private.math_utility._1564": ["DynamicsResponseScaling"],
        "_private.math_utility._1565": ["Eigenmode"],
        "_private.math_utility._1566": ["Eigenmodes"],
        "_private.math_utility._1567": ["EulerParameters"],
        "_private.math_utility._1568": ["ExtrapolationOptions"],
        "_private.math_utility._1569": ["FacetedBody"],
        "_private.math_utility._1570": ["FacetedSurface"],
        "_private.math_utility._1571": ["FourierSeries"],
        "_private.math_utility._1572": ["GenericMatrix"],
        "_private.math_utility._1573": ["GriddedSurface"],
        "_private.math_utility._1574": ["HarmonicValue"],
        "_private.math_utility._1575": ["InertiaTensor"],
        "_private.math_utility._1576": ["MassProperties"],
        "_private.math_utility._1577": ["MaxMinMean"],
        "_private.math_utility._1578": ["ComplexMagnitudeMethod"],
        "_private.math_utility._1579": ["MultipleFourierSeriesInterpolator"],
        "_private.math_utility._1580": ["Named2DLocation"],
        "_private.math_utility._1581": ["PIDControlUpdateMethod"],
        "_private.math_utility._1582": ["Quaternion"],
        "_private.math_utility._1583": ["RealMatrix"],
        "_private.math_utility._1584": ["RealVector"],
        "_private.math_utility._1585": ["ResultOptionsFor3DVector"],
        "_private.math_utility._1586": ["RotationAxis"],
        "_private.math_utility._1587": ["RoundedOrder"],
        "_private.math_utility._1588": ["SinCurve"],
        "_private.math_utility._1589": ["SquareMatrix"],
        "_private.math_utility._1590": ["StressPoint"],
        "_private.math_utility._1591": ["TranslationRotation"],
        "_private.math_utility._1592": ["Vector2DListAccessor"],
        "_private.math_utility._1593": ["Vector6D"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AcousticWeighting",
    "AlignmentAxis",
    "Axis",
    "CirclesOnAxis",
    "ComplexMatrix",
    "ComplexPartDisplayOption",
    "ComplexVector",
    "ComplexVector3D",
    "ComplexVector6D",
    "CoordinateSystem3D",
    "CoordinateSystemEditor",
    "CoordinateSystemForRotation",
    "CoordinateSystemForRotationOrigin",
    "DataPrecision",
    "DegreeOfFreedom",
    "DynamicsResponseScalarResult",
    "DynamicsResponseScaling",
    "Eigenmode",
    "Eigenmodes",
    "EulerParameters",
    "ExtrapolationOptions",
    "FacetedBody",
    "FacetedSurface",
    "FourierSeries",
    "GenericMatrix",
    "GriddedSurface",
    "HarmonicValue",
    "InertiaTensor",
    "MassProperties",
    "MaxMinMean",
    "ComplexMagnitudeMethod",
    "MultipleFourierSeriesInterpolator",
    "Named2DLocation",
    "PIDControlUpdateMethod",
    "Quaternion",
    "RealMatrix",
    "RealVector",
    "ResultOptionsFor3DVector",
    "RotationAxis",
    "RoundedOrder",
    "SinCurve",
    "SquareMatrix",
    "StressPoint",
    "TranslationRotation",
    "Vector2DListAccessor",
    "Vector6D",
)
