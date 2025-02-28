"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe.version_comparer._2476 import DesignResults
    from mastapy._private.system_model.fe.version_comparer._2477 import (
        FESubstructureResults,
    )
    from mastapy._private.system_model.fe.version_comparer._2478 import (
        FESubstructureVersionComparer,
    )
    from mastapy._private.system_model.fe.version_comparer._2479 import LoadCaseResults
    from mastapy._private.system_model.fe.version_comparer._2480 import LoadCasesToRun
    from mastapy._private.system_model.fe.version_comparer._2481 import (
        NodeComparisonResult,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe.version_comparer._2476": ["DesignResults"],
        "_private.system_model.fe.version_comparer._2477": ["FESubstructureResults"],
        "_private.system_model.fe.version_comparer._2478": [
            "FESubstructureVersionComparer"
        ],
        "_private.system_model.fe.version_comparer._2479": ["LoadCaseResults"],
        "_private.system_model.fe.version_comparer._2480": ["LoadCasesToRun"],
        "_private.system_model.fe.version_comparer._2481": ["NodeComparisonResult"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DesignResults",
    "FESubstructureResults",
    "FESubstructureVersionComparer",
    "LoadCaseResults",
    "LoadCasesToRun",
    "NodeComparisonResult",
)
