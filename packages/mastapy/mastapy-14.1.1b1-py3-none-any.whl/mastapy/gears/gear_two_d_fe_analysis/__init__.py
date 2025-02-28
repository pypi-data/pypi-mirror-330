"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_two_d_fe_analysis._925 import (
        CylindricalGearMeshTIFFAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._926 import (
        CylindricalGearMeshTIFFAnalysisDutyCycle,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._927 import (
        CylindricalGearSetTIFFAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._928 import (
        CylindricalGearSetTIFFAnalysisDutyCycle,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._929 import (
        CylindricalGearTIFFAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._930 import (
        CylindricalGearTIFFAnalysisDutyCycle,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._931 import (
        CylindricalGearTwoDimensionalFEAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._932 import (
        FindleyCriticalPlaneAnalysis,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_two_d_fe_analysis._925": [
            "CylindricalGearMeshTIFFAnalysis"
        ],
        "_private.gears.gear_two_d_fe_analysis._926": [
            "CylindricalGearMeshTIFFAnalysisDutyCycle"
        ],
        "_private.gears.gear_two_d_fe_analysis._927": [
            "CylindricalGearSetTIFFAnalysis"
        ],
        "_private.gears.gear_two_d_fe_analysis._928": [
            "CylindricalGearSetTIFFAnalysisDutyCycle"
        ],
        "_private.gears.gear_two_d_fe_analysis._929": ["CylindricalGearTIFFAnalysis"],
        "_private.gears.gear_two_d_fe_analysis._930": [
            "CylindricalGearTIFFAnalysisDutyCycle"
        ],
        "_private.gears.gear_two_d_fe_analysis._931": [
            "CylindricalGearTwoDimensionalFEAnalysis"
        ],
        "_private.gears.gear_two_d_fe_analysis._932": ["FindleyCriticalPlaneAnalysis"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearMeshTIFFAnalysis",
    "CylindricalGearMeshTIFFAnalysisDutyCycle",
    "CylindricalGearSetTIFFAnalysis",
    "CylindricalGearSetTIFFAnalysisDutyCycle",
    "CylindricalGearTIFFAnalysis",
    "CylindricalGearTIFFAnalysisDutyCycle",
    "CylindricalGearTwoDimensionalFEAnalysis",
    "FindleyCriticalPlaneAnalysis",
)
