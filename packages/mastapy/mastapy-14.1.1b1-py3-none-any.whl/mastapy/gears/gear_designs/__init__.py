"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs._972 import (
        BevelHypoidGearDesignSettingsDatabase,
    )
    from mastapy._private.gears.gear_designs._973 import (
        BevelHypoidGearDesignSettingsItem,
    )
    from mastapy._private.gears.gear_designs._974 import (
        BevelHypoidGearRatingSettingsDatabase,
    )
    from mastapy._private.gears.gear_designs._975 import (
        BevelHypoidGearRatingSettingsItem,
    )
    from mastapy._private.gears.gear_designs._976 import DesignConstraint
    from mastapy._private.gears.gear_designs._977 import (
        DesignConstraintCollectionDatabase,
    )
    from mastapy._private.gears.gear_designs._978 import DesignConstraintsCollection
    from mastapy._private.gears.gear_designs._979 import GearDesign
    from mastapy._private.gears.gear_designs._980 import GearDesignComponent
    from mastapy._private.gears.gear_designs._981 import GearMeshDesign
    from mastapy._private.gears.gear_designs._982 import GearSetDesign
    from mastapy._private.gears.gear_designs._983 import (
        SelectedDesignConstraintsCollection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs._972": ["BevelHypoidGearDesignSettingsDatabase"],
        "_private.gears.gear_designs._973": ["BevelHypoidGearDesignSettingsItem"],
        "_private.gears.gear_designs._974": ["BevelHypoidGearRatingSettingsDatabase"],
        "_private.gears.gear_designs._975": ["BevelHypoidGearRatingSettingsItem"],
        "_private.gears.gear_designs._976": ["DesignConstraint"],
        "_private.gears.gear_designs._977": ["DesignConstraintCollectionDatabase"],
        "_private.gears.gear_designs._978": ["DesignConstraintsCollection"],
        "_private.gears.gear_designs._979": ["GearDesign"],
        "_private.gears.gear_designs._980": ["GearDesignComponent"],
        "_private.gears.gear_designs._981": ["GearMeshDesign"],
        "_private.gears.gear_designs._982": ["GearSetDesign"],
        "_private.gears.gear_designs._983": ["SelectedDesignConstraintsCollection"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BevelHypoidGearDesignSettingsDatabase",
    "BevelHypoidGearDesignSettingsItem",
    "BevelHypoidGearRatingSettingsDatabase",
    "BevelHypoidGearRatingSettingsItem",
    "DesignConstraint",
    "DesignConstraintCollectionDatabase",
    "DesignConstraintsCollection",
    "GearDesign",
    "GearDesignComponent",
    "GearMeshDesign",
    "GearSetDesign",
    "SelectedDesignConstraintsCollection",
)
