"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.fe_tools.vfx_tools.vfx_enums._1288 import ProSolveMpcType
    from mastapy._private.fe_tools.vfx_tools.vfx_enums._1289 import ProSolveSolverType
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.fe_tools.vfx_tools.vfx_enums._1288": ["ProSolveMpcType"],
        "_private.fe_tools.vfx_tools.vfx_enums._1289": ["ProSolveSolverType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ProSolveMpcType",
    "ProSolveSolverType",
)
