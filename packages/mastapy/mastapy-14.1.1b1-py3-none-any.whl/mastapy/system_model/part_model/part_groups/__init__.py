"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.part_groups._2553 import (
        ConcentricOrParallelPartGroup,
    )
    from mastapy._private.system_model.part_model.part_groups._2554 import (
        ConcentricPartGroup,
    )
    from mastapy._private.system_model.part_model.part_groups._2555 import (
        ConcentricPartGroupParallelToThis,
    )
    from mastapy._private.system_model.part_model.part_groups._2556 import (
        DesignMeasurements,
    )
    from mastapy._private.system_model.part_model.part_groups._2557 import (
        ParallelPartGroup,
    )
    from mastapy._private.system_model.part_model.part_groups._2558 import (
        ParallelPartGroupSelection,
    )
    from mastapy._private.system_model.part_model.part_groups._2559 import PartGroup
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.part_groups._2553": [
            "ConcentricOrParallelPartGroup"
        ],
        "_private.system_model.part_model.part_groups._2554": ["ConcentricPartGroup"],
        "_private.system_model.part_model.part_groups._2555": [
            "ConcentricPartGroupParallelToThis"
        ],
        "_private.system_model.part_model.part_groups._2556": ["DesignMeasurements"],
        "_private.system_model.part_model.part_groups._2557": ["ParallelPartGroup"],
        "_private.system_model.part_model.part_groups._2558": [
            "ParallelPartGroupSelection"
        ],
        "_private.system_model.part_model.part_groups._2559": ["PartGroup"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConcentricOrParallelPartGroup",
    "ConcentricPartGroup",
    "ConcentricPartGroupParallelToThis",
    "DesignMeasurements",
    "ParallelPartGroup",
    "ParallelPartGroupSelection",
    "PartGroup",
)
