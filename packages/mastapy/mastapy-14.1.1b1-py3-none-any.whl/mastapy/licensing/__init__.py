"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.licensing._1547 import LicenceServer
    from mastapy._private.licensing._7731 import LicenceServerDetails
    from mastapy._private.licensing._7732 import ModuleDetails
    from mastapy._private.licensing._7733 import ModuleLicenceStatus
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.licensing._1547": ["LicenceServer"],
        "_private.licensing._7731": ["LicenceServerDetails"],
        "_private.licensing._7732": ["ModuleDetails"],
        "_private.licensing._7733": ["ModuleLicenceStatus"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "LicenceServer",
    "LicenceServerDetails",
    "ModuleDetails",
    "ModuleLicenceStatus",
)
