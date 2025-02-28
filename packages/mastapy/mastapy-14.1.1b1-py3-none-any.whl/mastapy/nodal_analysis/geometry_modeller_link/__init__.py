"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.nodal_analysis.geometry_modeller_link._163 import (
        BaseGeometryModellerDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._164 import (
        GearTipRadiusClashTest,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._165 import (
        GeometryModellerAngleDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._166 import (
        GeometryModellerCountDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._167 import (
        GeometryModellerDesignInformation,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._168 import (
        GeometryModellerDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._169 import (
        GeometryModellerDimensions,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._170 import (
        GeometryModellerDimensionType,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._171 import (
        GeometryModellerLengthDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._172 import (
        GeometryModellerSettings,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._173 import (
        GeometryModellerUnitlessDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._174 import (
        GeometryTypeForComponentImport,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._175 import MeshRequest
    from mastapy._private.nodal_analysis.geometry_modeller_link._176 import (
        MeshRequestResult,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._177 import (
        ProfileFromImport,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._178 import (
        RepositionComponentDetails,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.nodal_analysis.geometry_modeller_link._163": [
            "BaseGeometryModellerDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._164": [
            "GearTipRadiusClashTest"
        ],
        "_private.nodal_analysis.geometry_modeller_link._165": [
            "GeometryModellerAngleDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._166": [
            "GeometryModellerCountDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._167": [
            "GeometryModellerDesignInformation"
        ],
        "_private.nodal_analysis.geometry_modeller_link._168": [
            "GeometryModellerDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._169": [
            "GeometryModellerDimensions"
        ],
        "_private.nodal_analysis.geometry_modeller_link._170": [
            "GeometryModellerDimensionType"
        ],
        "_private.nodal_analysis.geometry_modeller_link._171": [
            "GeometryModellerLengthDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._172": [
            "GeometryModellerSettings"
        ],
        "_private.nodal_analysis.geometry_modeller_link._173": [
            "GeometryModellerUnitlessDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._174": [
            "GeometryTypeForComponentImport"
        ],
        "_private.nodal_analysis.geometry_modeller_link._175": ["MeshRequest"],
        "_private.nodal_analysis.geometry_modeller_link._176": ["MeshRequestResult"],
        "_private.nodal_analysis.geometry_modeller_link._177": ["ProfileFromImport"],
        "_private.nodal_analysis.geometry_modeller_link._178": [
            "RepositionComponentDetails"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BaseGeometryModellerDimension",
    "GearTipRadiusClashTest",
    "GeometryModellerAngleDimension",
    "GeometryModellerCountDimension",
    "GeometryModellerDesignInformation",
    "GeometryModellerDimension",
    "GeometryModellerDimensions",
    "GeometryModellerDimensionType",
    "GeometryModellerLengthDimension",
    "GeometryModellerSettings",
    "GeometryModellerUnitlessDimension",
    "GeometryTypeForComponentImport",
    "MeshRequest",
    "MeshRequestResult",
    "ProfileFromImport",
    "RepositionComponentDetails",
)
