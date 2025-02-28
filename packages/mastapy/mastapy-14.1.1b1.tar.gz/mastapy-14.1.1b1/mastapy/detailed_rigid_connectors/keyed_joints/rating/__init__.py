"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.detailed_rigid_connectors.keyed_joints.rating._1500 import (
        KeywayHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.keyed_joints.rating._1501 import (
        KeywayRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.detailed_rigid_connectors.keyed_joints.rating._1500": [
            "KeywayHalfRating"
        ],
        "_private.detailed_rigid_connectors.keyed_joints.rating._1501": [
            "KeywayRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "KeywayHalfRating",
    "KeywayRating",
)
