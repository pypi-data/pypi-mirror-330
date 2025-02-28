"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility.hertzian_contact._1630 import ContactDampingModel
    from mastapy._private.math_utility.hertzian_contact._1631 import (
        HertzianContactDeflectionCalculationMethod,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility.hertzian_contact._1630": ["ContactDampingModel"],
        "_private.math_utility.hertzian_contact._1631": [
            "HertzianContactDeflectionCalculationMethod"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ContactDampingModel",
    "HertzianContactDeflectionCalculationMethod",
)
