"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model._2263 import Design
    from mastapy._private.system_model._2264 import ComponentDampingOption
    from mastapy._private.system_model._2265 import (
        ConceptCouplingSpeedRatioSpecificationMethod,
    )
    from mastapy._private.system_model._2266 import DesignEntity
    from mastapy._private.system_model._2267 import DesignEntityId
    from mastapy._private.system_model._2268 import DesignSettings
    from mastapy._private.system_model._2269 import DutyCycleImporter
    from mastapy._private.system_model._2270 import DutyCycleImporterDesignEntityMatch
    from mastapy._private.system_model._2271 import ExternalFullFELoader
    from mastapy._private.system_model._2272 import HypoidWindUpRemovalMethod
    from mastapy._private.system_model._2273 import IncludeDutyCycleOption
    from mastapy._private.system_model._2274 import MAAElectricMachineGroup
    from mastapy._private.system_model._2275 import MASTASettings
    from mastapy._private.system_model._2276 import MemorySummary
    from mastapy._private.system_model._2277 import MeshStiffnessModel
    from mastapy._private.system_model._2278 import (
        PlanetPinManufacturingErrorsCoordinateSystem,
    )
    from mastapy._private.system_model._2279 import (
        PowerLoadDragTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2280 import (
        PowerLoadInputTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2281 import PowerLoadPIDControlSpeedInputType
    from mastapy._private.system_model._2282 import PowerLoadType
    from mastapy._private.system_model._2283 import RelativeComponentAlignment
    from mastapy._private.system_model._2284 import RelativeOffsetOption
    from mastapy._private.system_model._2285 import SystemReporting
    from mastapy._private.system_model._2286 import (
        ThermalExpansionOptionForGroundedNodes,
    )
    from mastapy._private.system_model._2287 import TransmissionTemperatureSet
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model._2263": ["Design"],
        "_private.system_model._2264": ["ComponentDampingOption"],
        "_private.system_model._2265": ["ConceptCouplingSpeedRatioSpecificationMethod"],
        "_private.system_model._2266": ["DesignEntity"],
        "_private.system_model._2267": ["DesignEntityId"],
        "_private.system_model._2268": ["DesignSettings"],
        "_private.system_model._2269": ["DutyCycleImporter"],
        "_private.system_model._2270": ["DutyCycleImporterDesignEntityMatch"],
        "_private.system_model._2271": ["ExternalFullFELoader"],
        "_private.system_model._2272": ["HypoidWindUpRemovalMethod"],
        "_private.system_model._2273": ["IncludeDutyCycleOption"],
        "_private.system_model._2274": ["MAAElectricMachineGroup"],
        "_private.system_model._2275": ["MASTASettings"],
        "_private.system_model._2276": ["MemorySummary"],
        "_private.system_model._2277": ["MeshStiffnessModel"],
        "_private.system_model._2278": ["PlanetPinManufacturingErrorsCoordinateSystem"],
        "_private.system_model._2279": ["PowerLoadDragTorqueSpecificationMethod"],
        "_private.system_model._2280": ["PowerLoadInputTorqueSpecificationMethod"],
        "_private.system_model._2281": ["PowerLoadPIDControlSpeedInputType"],
        "_private.system_model._2282": ["PowerLoadType"],
        "_private.system_model._2283": ["RelativeComponentAlignment"],
        "_private.system_model._2284": ["RelativeOffsetOption"],
        "_private.system_model._2285": ["SystemReporting"],
        "_private.system_model._2286": ["ThermalExpansionOptionForGroundedNodes"],
        "_private.system_model._2287": ["TransmissionTemperatureSet"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Design",
    "ComponentDampingOption",
    "ConceptCouplingSpeedRatioSpecificationMethod",
    "DesignEntity",
    "DesignEntityId",
    "DesignSettings",
    "DutyCycleImporter",
    "DutyCycleImporterDesignEntityMatch",
    "ExternalFullFELoader",
    "HypoidWindUpRemovalMethod",
    "IncludeDutyCycleOption",
    "MAAElectricMachineGroup",
    "MASTASettings",
    "MemorySummary",
    "MeshStiffnessModel",
    "PlanetPinManufacturingErrorsCoordinateSystem",
    "PowerLoadDragTorqueSpecificationMethod",
    "PowerLoadInputTorqueSpecificationMethod",
    "PowerLoadPIDControlSpeedInputType",
    "PowerLoadType",
    "RelativeComponentAlignment",
    "RelativeOffsetOption",
    "SystemReporting",
    "ThermalExpansionOptionForGroundedNodes",
    "TransmissionTemperatureSet",
)
