"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.cylindrical._640 import (
        CutterFlankSections,
    )
    from mastapy._private.gears.manufacturing.cylindrical._641 import (
        CylindricalCutterDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical._642 import (
        CylindricalGearBlank,
    )
    from mastapy._private.gears.manufacturing.cylindrical._643 import (
        CylindricalGearManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.cylindrical._644 import (
        CylindricalGearSpecifiedMicroGeometry,
    )
    from mastapy._private.gears.manufacturing.cylindrical._645 import (
        CylindricalGearSpecifiedProfile,
    )
    from mastapy._private.gears.manufacturing.cylindrical._646 import (
        CylindricalHobDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical._647 import (
        CylindricalManufacturedGearDutyCycle,
    )
    from mastapy._private.gears.manufacturing.cylindrical._648 import (
        CylindricalManufacturedGearLoadCase,
    )
    from mastapy._private.gears.manufacturing.cylindrical._649 import (
        CylindricalManufacturedGearMeshDutyCycle,
    )
    from mastapy._private.gears.manufacturing.cylindrical._650 import (
        CylindricalManufacturedGearMeshLoadCase,
    )
    from mastapy._private.gears.manufacturing.cylindrical._651 import (
        CylindricalManufacturedGearSetDutyCycle,
    )
    from mastapy._private.gears.manufacturing.cylindrical._652 import (
        CylindricalManufacturedGearSetLoadCase,
    )
    from mastapy._private.gears.manufacturing.cylindrical._653 import (
        CylindricalMeshManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.cylindrical._654 import (
        CylindricalMftFinishingMethods,
    )
    from mastapy._private.gears.manufacturing.cylindrical._655 import (
        CylindricalMftRoughingMethods,
    )
    from mastapy._private.gears.manufacturing.cylindrical._656 import (
        CylindricalSetManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.cylindrical._657 import (
        CylindricalShaperDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical._658 import Flank
    from mastapy._private.gears.manufacturing.cylindrical._659 import (
        GearManufacturingConfigurationViewModel,
    )
    from mastapy._private.gears.manufacturing.cylindrical._660 import (
        GearManufacturingConfigurationViewModelPlaceholder,
    )
    from mastapy._private.gears.manufacturing.cylindrical._661 import (
        GearSetConfigViewModel,
    )
    from mastapy._private.gears.manufacturing.cylindrical._662 import HobEdgeTypes
    from mastapy._private.gears.manufacturing.cylindrical._663 import (
        LeadModificationSegment,
    )
    from mastapy._private.gears.manufacturing.cylindrical._664 import (
        MicroGeometryInputs,
    )
    from mastapy._private.gears.manufacturing.cylindrical._665 import (
        MicroGeometryInputsLead,
    )
    from mastapy._private.gears.manufacturing.cylindrical._666 import (
        MicroGeometryInputsProfile,
    )
    from mastapy._private.gears.manufacturing.cylindrical._667 import (
        ModificationSegment,
    )
    from mastapy._private.gears.manufacturing.cylindrical._668 import (
        ProfileModificationSegment,
    )
    from mastapy._private.gears.manufacturing.cylindrical._669 import (
        SuitableCutterSetup,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.cylindrical._640": ["CutterFlankSections"],
        "_private.gears.manufacturing.cylindrical._641": ["CylindricalCutterDatabase"],
        "_private.gears.manufacturing.cylindrical._642": ["CylindricalGearBlank"],
        "_private.gears.manufacturing.cylindrical._643": [
            "CylindricalGearManufacturingConfig"
        ],
        "_private.gears.manufacturing.cylindrical._644": [
            "CylindricalGearSpecifiedMicroGeometry"
        ],
        "_private.gears.manufacturing.cylindrical._645": [
            "CylindricalGearSpecifiedProfile"
        ],
        "_private.gears.manufacturing.cylindrical._646": ["CylindricalHobDatabase"],
        "_private.gears.manufacturing.cylindrical._647": [
            "CylindricalManufacturedGearDutyCycle"
        ],
        "_private.gears.manufacturing.cylindrical._648": [
            "CylindricalManufacturedGearLoadCase"
        ],
        "_private.gears.manufacturing.cylindrical._649": [
            "CylindricalManufacturedGearMeshDutyCycle"
        ],
        "_private.gears.manufacturing.cylindrical._650": [
            "CylindricalManufacturedGearMeshLoadCase"
        ],
        "_private.gears.manufacturing.cylindrical._651": [
            "CylindricalManufacturedGearSetDutyCycle"
        ],
        "_private.gears.manufacturing.cylindrical._652": [
            "CylindricalManufacturedGearSetLoadCase"
        ],
        "_private.gears.manufacturing.cylindrical._653": [
            "CylindricalMeshManufacturingConfig"
        ],
        "_private.gears.manufacturing.cylindrical._654": [
            "CylindricalMftFinishingMethods"
        ],
        "_private.gears.manufacturing.cylindrical._655": [
            "CylindricalMftRoughingMethods"
        ],
        "_private.gears.manufacturing.cylindrical._656": [
            "CylindricalSetManufacturingConfig"
        ],
        "_private.gears.manufacturing.cylindrical._657": ["CylindricalShaperDatabase"],
        "_private.gears.manufacturing.cylindrical._658": ["Flank"],
        "_private.gears.manufacturing.cylindrical._659": [
            "GearManufacturingConfigurationViewModel"
        ],
        "_private.gears.manufacturing.cylindrical._660": [
            "GearManufacturingConfigurationViewModelPlaceholder"
        ],
        "_private.gears.manufacturing.cylindrical._661": ["GearSetConfigViewModel"],
        "_private.gears.manufacturing.cylindrical._662": ["HobEdgeTypes"],
        "_private.gears.manufacturing.cylindrical._663": ["LeadModificationSegment"],
        "_private.gears.manufacturing.cylindrical._664": ["MicroGeometryInputs"],
        "_private.gears.manufacturing.cylindrical._665": ["MicroGeometryInputsLead"],
        "_private.gears.manufacturing.cylindrical._666": ["MicroGeometryInputsProfile"],
        "_private.gears.manufacturing.cylindrical._667": ["ModificationSegment"],
        "_private.gears.manufacturing.cylindrical._668": ["ProfileModificationSegment"],
        "_private.gears.manufacturing.cylindrical._669": ["SuitableCutterSetup"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CutterFlankSections",
    "CylindricalCutterDatabase",
    "CylindricalGearBlank",
    "CylindricalGearManufacturingConfig",
    "CylindricalGearSpecifiedMicroGeometry",
    "CylindricalGearSpecifiedProfile",
    "CylindricalHobDatabase",
    "CylindricalManufacturedGearDutyCycle",
    "CylindricalManufacturedGearLoadCase",
    "CylindricalManufacturedGearMeshDutyCycle",
    "CylindricalManufacturedGearMeshLoadCase",
    "CylindricalManufacturedGearSetDutyCycle",
    "CylindricalManufacturedGearSetLoadCase",
    "CylindricalMeshManufacturingConfig",
    "CylindricalMftFinishingMethods",
    "CylindricalMftRoughingMethods",
    "CylindricalSetManufacturingConfig",
    "CylindricalShaperDatabase",
    "Flank",
    "GearManufacturingConfigurationViewModel",
    "GearManufacturingConfigurationViewModelPlaceholder",
    "GearSetConfigViewModel",
    "HobEdgeTypes",
    "LeadModificationSegment",
    "MicroGeometryInputs",
    "MicroGeometryInputsLead",
    "MicroGeometryInputsProfile",
    "ModificationSegment",
    "ProfileModificationSegment",
    "SuitableCutterSetup",
)
