"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.units_and_measurements._1660 import (
        DegreesMinutesSeconds,
    )
    from mastapy._private.utility.units_and_measurements._1661 import EnumUnit
    from mastapy._private.utility.units_and_measurements._1662 import InverseUnit
    from mastapy._private.utility.units_and_measurements._1663 import MeasurementBase
    from mastapy._private.utility.units_and_measurements._1664 import (
        MeasurementSettings,
    )
    from mastapy._private.utility.units_and_measurements._1665 import MeasurementSystem
    from mastapy._private.utility.units_and_measurements._1666 import SafetyFactorUnit
    from mastapy._private.utility.units_and_measurements._1667 import TimeUnit
    from mastapy._private.utility.units_and_measurements._1668 import Unit
    from mastapy._private.utility.units_and_measurements._1669 import UnitGradient
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.units_and_measurements._1660": ["DegreesMinutesSeconds"],
        "_private.utility.units_and_measurements._1661": ["EnumUnit"],
        "_private.utility.units_and_measurements._1662": ["InverseUnit"],
        "_private.utility.units_and_measurements._1663": ["MeasurementBase"],
        "_private.utility.units_and_measurements._1664": ["MeasurementSettings"],
        "_private.utility.units_and_measurements._1665": ["MeasurementSystem"],
        "_private.utility.units_and_measurements._1666": ["SafetyFactorUnit"],
        "_private.utility.units_and_measurements._1667": ["TimeUnit"],
        "_private.utility.units_and_measurements._1668": ["Unit"],
        "_private.utility.units_and_measurements._1669": ["UnitGradient"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DegreesMinutesSeconds",
    "EnumUnit",
    "InverseUnit",
    "MeasurementBase",
    "MeasurementSettings",
    "MeasurementSystem",
    "SafetyFactorUnit",
    "TimeUnit",
    "Unit",
    "UnitGradient",
)
