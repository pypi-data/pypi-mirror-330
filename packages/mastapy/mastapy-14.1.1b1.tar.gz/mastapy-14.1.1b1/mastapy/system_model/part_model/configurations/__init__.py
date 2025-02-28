"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.configurations._2688 import (
        ActiveFESubstructureSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2689 import (
        ActiveFESubstructureSelectionGroup,
    )
    from mastapy._private.system_model.part_model.configurations._2690 import (
        ActiveShaftDesignSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2691 import (
        ActiveShaftDesignSelectionGroup,
    )
    from mastapy._private.system_model.part_model.configurations._2692 import (
        BearingDetailConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2693 import (
        BearingDetailSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2694 import (
        DesignConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2695 import (
        PartDetailConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2696 import (
        PartDetailSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.configurations._2688": [
            "ActiveFESubstructureSelection"
        ],
        "_private.system_model.part_model.configurations._2689": [
            "ActiveFESubstructureSelectionGroup"
        ],
        "_private.system_model.part_model.configurations._2690": [
            "ActiveShaftDesignSelection"
        ],
        "_private.system_model.part_model.configurations._2691": [
            "ActiveShaftDesignSelectionGroup"
        ],
        "_private.system_model.part_model.configurations._2692": [
            "BearingDetailConfiguration"
        ],
        "_private.system_model.part_model.configurations._2693": [
            "BearingDetailSelection"
        ],
        "_private.system_model.part_model.configurations._2694": [
            "DesignConfiguration"
        ],
        "_private.system_model.part_model.configurations._2695": [
            "PartDetailConfiguration"
        ],
        "_private.system_model.part_model.configurations._2696": [
            "PartDetailSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ActiveFESubstructureSelection",
    "ActiveFESubstructureSelectionGroup",
    "ActiveShaftDesignSelection",
    "ActiveShaftDesignSelectionGroup",
    "BearingDetailConfiguration",
    "BearingDetailSelection",
    "DesignConfiguration",
    "PartDetailConfiguration",
    "PartDetailSelection",
)
