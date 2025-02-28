"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.nodal_analysis.component_mode_synthesis._242 import (
        AddNodeToGroupByID,
    )
    from mastapy._private.nodal_analysis.component_mode_synthesis._243 import (
        CMSElementFaceGroup,
    )
    from mastapy._private.nodal_analysis.component_mode_synthesis._244 import (
        CMSElementFaceGroupOfAllFreeFaces,
    )
    from mastapy._private.nodal_analysis.component_mode_synthesis._245 import CMSModel
    from mastapy._private.nodal_analysis.component_mode_synthesis._246 import (
        CMSNodeGroup,
    )
    from mastapy._private.nodal_analysis.component_mode_synthesis._247 import CMSOptions
    from mastapy._private.nodal_analysis.component_mode_synthesis._248 import CMSResults
    from mastapy._private.nodal_analysis.component_mode_synthesis._249 import (
        HarmonicCMSResults,
    )
    from mastapy._private.nodal_analysis.component_mode_synthesis._250 import (
        ModalCMSResults,
    )
    from mastapy._private.nodal_analysis.component_mode_synthesis._251 import (
        RealCMSResults,
    )
    from mastapy._private.nodal_analysis.component_mode_synthesis._252 import (
        ReductionModeType,
    )
    from mastapy._private.nodal_analysis.component_mode_synthesis._253 import (
        SoftwareUsedForReductionType,
    )
    from mastapy._private.nodal_analysis.component_mode_synthesis._254 import (
        StaticCMSResults,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.nodal_analysis.component_mode_synthesis._242": ["AddNodeToGroupByID"],
        "_private.nodal_analysis.component_mode_synthesis._243": [
            "CMSElementFaceGroup"
        ],
        "_private.nodal_analysis.component_mode_synthesis._244": [
            "CMSElementFaceGroupOfAllFreeFaces"
        ],
        "_private.nodal_analysis.component_mode_synthesis._245": ["CMSModel"],
        "_private.nodal_analysis.component_mode_synthesis._246": ["CMSNodeGroup"],
        "_private.nodal_analysis.component_mode_synthesis._247": ["CMSOptions"],
        "_private.nodal_analysis.component_mode_synthesis._248": ["CMSResults"],
        "_private.nodal_analysis.component_mode_synthesis._249": ["HarmonicCMSResults"],
        "_private.nodal_analysis.component_mode_synthesis._250": ["ModalCMSResults"],
        "_private.nodal_analysis.component_mode_synthesis._251": ["RealCMSResults"],
        "_private.nodal_analysis.component_mode_synthesis._252": ["ReductionModeType"],
        "_private.nodal_analysis.component_mode_synthesis._253": [
            "SoftwareUsedForReductionType"
        ],
        "_private.nodal_analysis.component_mode_synthesis._254": ["StaticCMSResults"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AddNodeToGroupByID",
    "CMSElementFaceGroup",
    "CMSElementFaceGroupOfAllFreeFaces",
    "CMSModel",
    "CMSNodeGroup",
    "CMSOptions",
    "CMSResults",
    "HarmonicCMSResults",
    "ModalCMSResults",
    "RealCMSResults",
    "ReductionModeType",
    "SoftwareUsedForReductionType",
    "StaticCMSResults",
)
