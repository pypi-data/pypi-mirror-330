"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.bearing_designs.rolling._2197 import (
        AngularContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2198 import (
        AngularContactThrustBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2199 import (
        AsymmetricSphericalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2200 import (
        AxialThrustCylindricalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2201 import (
        AxialThrustNeedleRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2202 import BallBearing
    from mastapy._private.bearings.bearing_designs.rolling._2203 import (
        BallBearingShoulderDefinition,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2204 import (
        BarrelRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2205 import (
        BearingProtection,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2206 import (
        BearingProtectionDetailsModifier,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2207 import (
        BearingProtectionLevel,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2208 import (
        BearingTypeExtraInformation,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2209 import CageBridgeShape
    from mastapy._private.bearings.bearing_designs.rolling._2210 import (
        CrossedRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2211 import (
        CylindricalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2212 import (
        DeepGrooveBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2213 import DiameterSeries
    from mastapy._private.bearings.bearing_designs.rolling._2214 import (
        FatigueLoadLimitCalculationMethodEnum,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2215 import (
        FourPointContactAngleDefinition,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2216 import (
        FourPointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2217 import (
        GeometricConstants,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2218 import (
        GeometricConstantsForRollingFrictionalMoments,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2219 import (
        GeometricConstantsForSlidingFrictionalMoments,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2220 import HeightSeries
    from mastapy._private.bearings.bearing_designs.rolling._2221 import (
        MultiPointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2222 import (
        NeedleRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2223 import (
        NonBarrelRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2224 import RollerBearing
    from mastapy._private.bearings.bearing_designs.rolling._2225 import RollerEndShape
    from mastapy._private.bearings.bearing_designs.rolling._2226 import RollerRibDetail
    from mastapy._private.bearings.bearing_designs.rolling._2227 import RollingBearing
    from mastapy._private.bearings.bearing_designs.rolling._2228 import (
        RollingBearingElement,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2229 import (
        SelfAligningBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2230 import (
        SKFSealFrictionalMomentConstants,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2231 import SleeveType
    from mastapy._private.bearings.bearing_designs.rolling._2232 import (
        SphericalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2233 import (
        SphericalRollerThrustBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2234 import (
        TaperRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2235 import (
        ThreePointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2236 import (
        ThrustBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2237 import (
        ToroidalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2238 import WidthSeries
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.bearing_designs.rolling._2197": [
            "AngularContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2198": [
            "AngularContactThrustBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2199": [
            "AsymmetricSphericalRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2200": [
            "AxialThrustCylindricalRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2201": [
            "AxialThrustNeedleRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2202": ["BallBearing"],
        "_private.bearings.bearing_designs.rolling._2203": [
            "BallBearingShoulderDefinition"
        ],
        "_private.bearings.bearing_designs.rolling._2204": ["BarrelRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2205": ["BearingProtection"],
        "_private.bearings.bearing_designs.rolling._2206": [
            "BearingProtectionDetailsModifier"
        ],
        "_private.bearings.bearing_designs.rolling._2207": ["BearingProtectionLevel"],
        "_private.bearings.bearing_designs.rolling._2208": [
            "BearingTypeExtraInformation"
        ],
        "_private.bearings.bearing_designs.rolling._2209": ["CageBridgeShape"],
        "_private.bearings.bearing_designs.rolling._2210": ["CrossedRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2211": ["CylindricalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2212": ["DeepGrooveBallBearing"],
        "_private.bearings.bearing_designs.rolling._2213": ["DiameterSeries"],
        "_private.bearings.bearing_designs.rolling._2214": [
            "FatigueLoadLimitCalculationMethodEnum"
        ],
        "_private.bearings.bearing_designs.rolling._2215": [
            "FourPointContactAngleDefinition"
        ],
        "_private.bearings.bearing_designs.rolling._2216": [
            "FourPointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2217": ["GeometricConstants"],
        "_private.bearings.bearing_designs.rolling._2218": [
            "GeometricConstantsForRollingFrictionalMoments"
        ],
        "_private.bearings.bearing_designs.rolling._2219": [
            "GeometricConstantsForSlidingFrictionalMoments"
        ],
        "_private.bearings.bearing_designs.rolling._2220": ["HeightSeries"],
        "_private.bearings.bearing_designs.rolling._2221": [
            "MultiPointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2222": ["NeedleRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2223": ["NonBarrelRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2224": ["RollerBearing"],
        "_private.bearings.bearing_designs.rolling._2225": ["RollerEndShape"],
        "_private.bearings.bearing_designs.rolling._2226": ["RollerRibDetail"],
        "_private.bearings.bearing_designs.rolling._2227": ["RollingBearing"],
        "_private.bearings.bearing_designs.rolling._2228": ["RollingBearingElement"],
        "_private.bearings.bearing_designs.rolling._2229": ["SelfAligningBallBearing"],
        "_private.bearings.bearing_designs.rolling._2230": [
            "SKFSealFrictionalMomentConstants"
        ],
        "_private.bearings.bearing_designs.rolling._2231": ["SleeveType"],
        "_private.bearings.bearing_designs.rolling._2232": ["SphericalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2233": [
            "SphericalRollerThrustBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2234": ["TaperRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2235": [
            "ThreePointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2236": ["ThrustBallBearing"],
        "_private.bearings.bearing_designs.rolling._2237": ["ToroidalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2238": ["WidthSeries"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AngularContactBallBearing",
    "AngularContactThrustBallBearing",
    "AsymmetricSphericalRollerBearing",
    "AxialThrustCylindricalRollerBearing",
    "AxialThrustNeedleRollerBearing",
    "BallBearing",
    "BallBearingShoulderDefinition",
    "BarrelRollerBearing",
    "BearingProtection",
    "BearingProtectionDetailsModifier",
    "BearingProtectionLevel",
    "BearingTypeExtraInformation",
    "CageBridgeShape",
    "CrossedRollerBearing",
    "CylindricalRollerBearing",
    "DeepGrooveBallBearing",
    "DiameterSeries",
    "FatigueLoadLimitCalculationMethodEnum",
    "FourPointContactAngleDefinition",
    "FourPointContactBallBearing",
    "GeometricConstants",
    "GeometricConstantsForRollingFrictionalMoments",
    "GeometricConstantsForSlidingFrictionalMoments",
    "HeightSeries",
    "MultiPointContactBallBearing",
    "NeedleRollerBearing",
    "NonBarrelRollerBearing",
    "RollerBearing",
    "RollerEndShape",
    "RollerRibDetail",
    "RollingBearing",
    "RollingBearingElement",
    "SelfAligningBallBearing",
    "SKFSealFrictionalMomentConstants",
    "SleeveType",
    "SphericalRollerBearing",
    "SphericalRollerThrustBearing",
    "TaperRollerBearing",
    "ThreePointContactBallBearing",
    "ThrustBallBearing",
    "ToroidalRollerBearing",
    "WidthSeries",
)
