"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.zerol_bevel._984 import (
        ZerolBevelGearDesign,
    )
    from mastapy._private.gears.gear_designs.zerol_bevel._985 import (
        ZerolBevelGearMeshDesign,
    )
    from mastapy._private.gears.gear_designs.zerol_bevel._986 import (
        ZerolBevelGearSetDesign,
    )
    from mastapy._private.gears.gear_designs.zerol_bevel._987 import (
        ZerolBevelMeshedGearDesign,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.zerol_bevel._984": ["ZerolBevelGearDesign"],
        "_private.gears.gear_designs.zerol_bevel._985": ["ZerolBevelGearMeshDesign"],
        "_private.gears.gear_designs.zerol_bevel._986": ["ZerolBevelGearSetDesign"],
        "_private.gears.gear_designs.zerol_bevel._987": ["ZerolBevelMeshedGearDesign"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ZerolBevelGearDesign",
    "ZerolBevelGearMeshDesign",
    "ZerolBevelGearSetDesign",
    "ZerolBevelMeshedGearDesign",
)
