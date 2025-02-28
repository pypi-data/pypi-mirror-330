"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.units_and_measurements._7719 import MeasurementType
    from mastapy._private.units_and_measurements._7720 import MeasurementTypeExtensions
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.units_and_measurements._7719": ["MeasurementType"],
        "_private.units_and_measurements._7720": ["MeasurementTypeExtensions"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "MeasurementType",
    "MeasurementTypeExtensions",
)
