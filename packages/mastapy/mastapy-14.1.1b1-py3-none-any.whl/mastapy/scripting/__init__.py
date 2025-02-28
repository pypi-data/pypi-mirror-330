"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.scripting._7721 import ApiEnumForAttribute
    from mastapy._private.scripting._7722 import ApiVersion
    from mastapy._private.scripting._7723 import SMTBitmap
    from mastapy._private.scripting._7725 import MastaPropertyAttribute
    from mastapy._private.scripting._7726 import PythonCommand
    from mastapy._private.scripting._7727 import ScriptingCommand
    from mastapy._private.scripting._7728 import ScriptingExecutionCommand
    from mastapy._private.scripting._7729 import ScriptingObjectCommand
    from mastapy._private.scripting._7730 import ApiVersioning
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.scripting._7721": ["ApiEnumForAttribute"],
        "_private.scripting._7722": ["ApiVersion"],
        "_private.scripting._7723": ["SMTBitmap"],
        "_private.scripting._7725": ["MastaPropertyAttribute"],
        "_private.scripting._7726": ["PythonCommand"],
        "_private.scripting._7727": ["ScriptingCommand"],
        "_private.scripting._7728": ["ScriptingExecutionCommand"],
        "_private.scripting._7729": ["ScriptingObjectCommand"],
        "_private.scripting._7730": ["ApiVersioning"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ApiEnumForAttribute",
    "ApiVersion",
    "SMTBitmap",
    "MastaPropertyAttribute",
    "PythonCommand",
    "ScriptingCommand",
    "ScriptingExecutionCommand",
    "ScriptingObjectCommand",
    "ApiVersioning",
)
