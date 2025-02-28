"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.face._1021 import FaceGearDesign
    from mastapy._private.gears.gear_designs.face._1022 import (
        FaceGearDiameterFaceWidthSpecificationMethod,
    )
    from mastapy._private.gears.gear_designs.face._1023 import FaceGearMeshDesign
    from mastapy._private.gears.gear_designs.face._1024 import FaceGearMeshMicroGeometry
    from mastapy._private.gears.gear_designs.face._1025 import FaceGearMicroGeometry
    from mastapy._private.gears.gear_designs.face._1026 import FaceGearPinionDesign
    from mastapy._private.gears.gear_designs.face._1027 import FaceGearSetDesign
    from mastapy._private.gears.gear_designs.face._1028 import FaceGearSetMicroGeometry
    from mastapy._private.gears.gear_designs.face._1029 import FaceGearWheelDesign
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.face._1021": ["FaceGearDesign"],
        "_private.gears.gear_designs.face._1022": [
            "FaceGearDiameterFaceWidthSpecificationMethod"
        ],
        "_private.gears.gear_designs.face._1023": ["FaceGearMeshDesign"],
        "_private.gears.gear_designs.face._1024": ["FaceGearMeshMicroGeometry"],
        "_private.gears.gear_designs.face._1025": ["FaceGearMicroGeometry"],
        "_private.gears.gear_designs.face._1026": ["FaceGearPinionDesign"],
        "_private.gears.gear_designs.face._1027": ["FaceGearSetDesign"],
        "_private.gears.gear_designs.face._1028": ["FaceGearSetMicroGeometry"],
        "_private.gears.gear_designs.face._1029": ["FaceGearWheelDesign"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FaceGearDesign",
    "FaceGearDiameterFaceWidthSpecificationMethod",
    "FaceGearMeshDesign",
    "FaceGearMeshMicroGeometry",
    "FaceGearMicroGeometry",
    "FaceGearPinionDesign",
    "FaceGearSetDesign",
    "FaceGearSetMicroGeometry",
    "FaceGearWheelDesign",
)
