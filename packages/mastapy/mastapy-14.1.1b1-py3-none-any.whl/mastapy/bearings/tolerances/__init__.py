"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.tolerances._1962 import BearingConnectionComponent
    from mastapy._private.bearings.tolerances._1963 import InternalClearanceClass
    from mastapy._private.bearings.tolerances._1964 import BearingToleranceClass
    from mastapy._private.bearings.tolerances._1965 import (
        BearingToleranceDefinitionOptions,
    )
    from mastapy._private.bearings.tolerances._1966 import FitType
    from mastapy._private.bearings.tolerances._1967 import InnerRingTolerance
    from mastapy._private.bearings.tolerances._1968 import InnerSupportTolerance
    from mastapy._private.bearings.tolerances._1969 import InterferenceDetail
    from mastapy._private.bearings.tolerances._1970 import InterferenceTolerance
    from mastapy._private.bearings.tolerances._1971 import ITDesignation
    from mastapy._private.bearings.tolerances._1972 import MountingSleeveDiameterDetail
    from mastapy._private.bearings.tolerances._1973 import OuterRingTolerance
    from mastapy._private.bearings.tolerances._1974 import OuterSupportTolerance
    from mastapy._private.bearings.tolerances._1975 import RaceRoundnessAtAngle
    from mastapy._private.bearings.tolerances._1976 import RadialSpecificationMethod
    from mastapy._private.bearings.tolerances._1977 import RingDetail
    from mastapy._private.bearings.tolerances._1978 import RingTolerance
    from mastapy._private.bearings.tolerances._1979 import RoundnessSpecification
    from mastapy._private.bearings.tolerances._1980 import RoundnessSpecificationType
    from mastapy._private.bearings.tolerances._1981 import SupportDetail
    from mastapy._private.bearings.tolerances._1982 import SupportMaterialSource
    from mastapy._private.bearings.tolerances._1983 import SupportTolerance
    from mastapy._private.bearings.tolerances._1984 import (
        SupportToleranceLocationDesignation,
    )
    from mastapy._private.bearings.tolerances._1985 import ToleranceCombination
    from mastapy._private.bearings.tolerances._1986 import TypeOfFit
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.tolerances._1962": ["BearingConnectionComponent"],
        "_private.bearings.tolerances._1963": ["InternalClearanceClass"],
        "_private.bearings.tolerances._1964": ["BearingToleranceClass"],
        "_private.bearings.tolerances._1965": ["BearingToleranceDefinitionOptions"],
        "_private.bearings.tolerances._1966": ["FitType"],
        "_private.bearings.tolerances._1967": ["InnerRingTolerance"],
        "_private.bearings.tolerances._1968": ["InnerSupportTolerance"],
        "_private.bearings.tolerances._1969": ["InterferenceDetail"],
        "_private.bearings.tolerances._1970": ["InterferenceTolerance"],
        "_private.bearings.tolerances._1971": ["ITDesignation"],
        "_private.bearings.tolerances._1972": ["MountingSleeveDiameterDetail"],
        "_private.bearings.tolerances._1973": ["OuterRingTolerance"],
        "_private.bearings.tolerances._1974": ["OuterSupportTolerance"],
        "_private.bearings.tolerances._1975": ["RaceRoundnessAtAngle"],
        "_private.bearings.tolerances._1976": ["RadialSpecificationMethod"],
        "_private.bearings.tolerances._1977": ["RingDetail"],
        "_private.bearings.tolerances._1978": ["RingTolerance"],
        "_private.bearings.tolerances._1979": ["RoundnessSpecification"],
        "_private.bearings.tolerances._1980": ["RoundnessSpecificationType"],
        "_private.bearings.tolerances._1981": ["SupportDetail"],
        "_private.bearings.tolerances._1982": ["SupportMaterialSource"],
        "_private.bearings.tolerances._1983": ["SupportTolerance"],
        "_private.bearings.tolerances._1984": ["SupportToleranceLocationDesignation"],
        "_private.bearings.tolerances._1985": ["ToleranceCombination"],
        "_private.bearings.tolerances._1986": ["TypeOfFit"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingConnectionComponent",
    "InternalClearanceClass",
    "BearingToleranceClass",
    "BearingToleranceDefinitionOptions",
    "FitType",
    "InnerRingTolerance",
    "InnerSupportTolerance",
    "InterferenceDetail",
    "InterferenceTolerance",
    "ITDesignation",
    "MountingSleeveDiameterDetail",
    "OuterRingTolerance",
    "OuterSupportTolerance",
    "RaceRoundnessAtAngle",
    "RadialSpecificationMethod",
    "RingDetail",
    "RingTolerance",
    "RoundnessSpecification",
    "RoundnessSpecificationType",
    "SupportDetail",
    "SupportMaterialSource",
    "SupportTolerance",
    "SupportToleranceLocationDesignation",
    "ToleranceCombination",
    "TypeOfFit",
)
