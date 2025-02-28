"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.fe_tools.vis_tools_global.vis_tools_global_enums._1283 import (
        BeamSectionType,
    )
    from mastapy._private.fe_tools.vis_tools_global.vis_tools_global_enums._1284 import (
        ContactPairConstrainedSurfaceType,
    )
    from mastapy._private.fe_tools.vis_tools_global.vis_tools_global_enums._1285 import (
        ContactPairReferenceSurfaceType,
    )
    from mastapy._private.fe_tools.vis_tools_global.vis_tools_global_enums._1286 import (
        ElementPropertiesShellWallType,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.fe_tools.vis_tools_global.vis_tools_global_enums._1283": [
            "BeamSectionType"
        ],
        "_private.fe_tools.vis_tools_global.vis_tools_global_enums._1284": [
            "ContactPairConstrainedSurfaceType"
        ],
        "_private.fe_tools.vis_tools_global.vis_tools_global_enums._1285": [
            "ContactPairReferenceSurfaceType"
        ],
        "_private.fe_tools.vis_tools_global.vis_tools_global_enums._1286": [
            "ElementPropertiesShellWallType"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BeamSectionType",
    "ContactPairConstrainedSurfaceType",
    "ContactPairReferenceSurfaceType",
    "ElementPropertiesShellWallType",
)
