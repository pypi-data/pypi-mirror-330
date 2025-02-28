"""GearSetDesignAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1265

_GEAR_SET_DESIGN_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearSetDesignAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1276, _1277, _1278, _1279
    from mastapy._private.gears.fe_model import _1248
    from mastapy._private.gears.fe_model.conical import _1254
    from mastapy._private.gears.fe_model.cylindrical import _1251
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1148,
        _1149,
    )
    from mastapy._private.gears.gear_designs.face import _1028
    from mastapy._private.gears.gear_two_d_fe_analysis import _927, _928
    from mastapy._private.gears.load_case import _905
    from mastapy._private.gears.load_case.bevel import _924
    from mastapy._private.gears.load_case.concept import _920
    from mastapy._private.gears.load_case.conical import _917
    from mastapy._private.gears.load_case.cylindrical import _914
    from mastapy._private.gears.load_case.face import _911
    from mastapy._private.gears.load_case.worm import _908
    from mastapy._private.gears.ltca import _877
    from mastapy._private.gears.ltca.conical import _899
    from mastapy._private.gears.ltca.cylindrical import _891, _893
    from mastapy._private.gears.manufacturing.bevel import _821, _822, _823, _824
    from mastapy._private.gears.manufacturing.cylindrical import _651, _652, _656

    Self = TypeVar("Self", bound="GearSetDesignAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetDesignAnalysis._Cast_GearSetDesignAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetDesignAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetDesignAnalysis:
    """Special nested class for casting GearSetDesignAnalysis to subclasses."""

    __parent__: "GearSetDesignAnalysis"

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1265.AbstractGearSetAnalysis":
        return self.__parent__._cast(_1265.AbstractGearSetAnalysis)

    @property
    def cylindrical_manufactured_gear_set_duty_cycle(
        self: "CastSelf",
    ) -> "_651.CylindricalManufacturedGearSetDutyCycle":
        from mastapy._private.gears.manufacturing.cylindrical import _651

        return self.__parent__._cast(_651.CylindricalManufacturedGearSetDutyCycle)

    @property
    def cylindrical_manufactured_gear_set_load_case(
        self: "CastSelf",
    ) -> "_652.CylindricalManufacturedGearSetLoadCase":
        from mastapy._private.gears.manufacturing.cylindrical import _652

        return self.__parent__._cast(_652.CylindricalManufacturedGearSetLoadCase)

    @property
    def cylindrical_set_manufacturing_config(
        self: "CastSelf",
    ) -> "_656.CylindricalSetManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _656

        return self.__parent__._cast(_656.CylindricalSetManufacturingConfig)

    @property
    def conical_set_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_821.ConicalSetManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _821

        return self.__parent__._cast(_821.ConicalSetManufacturingAnalysis)

    @property
    def conical_set_manufacturing_config(
        self: "CastSelf",
    ) -> "_822.ConicalSetManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _822

        return self.__parent__._cast(_822.ConicalSetManufacturingConfig)

    @property
    def conical_set_micro_geometry_config(
        self: "CastSelf",
    ) -> "_823.ConicalSetMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _823

        return self.__parent__._cast(_823.ConicalSetMicroGeometryConfig)

    @property
    def conical_set_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_824.ConicalSetMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _824

        return self.__parent__._cast(_824.ConicalSetMicroGeometryConfigBase)

    @property
    def gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_877.GearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _877

        return self.__parent__._cast(_877.GearSetLoadDistributionAnalysis)

    @property
    def cylindrical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_891.CylindricalGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _891

        return self.__parent__._cast(_891.CylindricalGearSetLoadDistributionAnalysis)

    @property
    def face_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_893.FaceGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _893

        return self.__parent__._cast(_893.FaceGearSetLoadDistributionAnalysis)

    @property
    def conical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_899.ConicalGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _899

        return self.__parent__._cast(_899.ConicalGearSetLoadDistributionAnalysis)

    @property
    def gear_set_load_case_base(self: "CastSelf") -> "_905.GearSetLoadCaseBase":
        from mastapy._private.gears.load_case import _905

        return self.__parent__._cast(_905.GearSetLoadCaseBase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_908.WormGearSetLoadCase":
        from mastapy._private.gears.load_case.worm import _908

        return self.__parent__._cast(_908.WormGearSetLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_911.FaceGearSetLoadCase":
        from mastapy._private.gears.load_case.face import _911

        return self.__parent__._cast(_911.FaceGearSetLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_914.CylindricalGearSetLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _914

        return self.__parent__._cast(_914.CylindricalGearSetLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_917.ConicalGearSetLoadCase":
        from mastapy._private.gears.load_case.conical import _917

        return self.__parent__._cast(_917.ConicalGearSetLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_920.ConceptGearSetLoadCase":
        from mastapy._private.gears.load_case.concept import _920

        return self.__parent__._cast(_920.ConceptGearSetLoadCase)

    @property
    def bevel_set_load_case(self: "CastSelf") -> "_924.BevelSetLoadCase":
        from mastapy._private.gears.load_case.bevel import _924

        return self.__parent__._cast(_924.BevelSetLoadCase)

    @property
    def cylindrical_gear_set_tiff_analysis(
        self: "CastSelf",
    ) -> "_927.CylindricalGearSetTIFFAnalysis":
        from mastapy._private.gears.gear_two_d_fe_analysis import _927

        return self.__parent__._cast(_927.CylindricalGearSetTIFFAnalysis)

    @property
    def cylindrical_gear_set_tiff_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_928.CylindricalGearSetTIFFAnalysisDutyCycle":
        from mastapy._private.gears.gear_two_d_fe_analysis import _928

        return self.__parent__._cast(_928.CylindricalGearSetTIFFAnalysisDutyCycle)

    @property
    def face_gear_set_micro_geometry(
        self: "CastSelf",
    ) -> "_1028.FaceGearSetMicroGeometry":
        from mastapy._private.gears.gear_designs.face import _1028

        return self.__parent__._cast(_1028.FaceGearSetMicroGeometry)

    @property
    def cylindrical_gear_set_micro_geometry(
        self: "CastSelf",
    ) -> "_1148.CylindricalGearSetMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1148

        return self.__parent__._cast(_1148.CylindricalGearSetMicroGeometry)

    @property
    def cylindrical_gear_set_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1149.CylindricalGearSetMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1149

        return self.__parent__._cast(_1149.CylindricalGearSetMicroGeometryDutyCycle)

    @property
    def gear_set_fe_model(self: "CastSelf") -> "_1248.GearSetFEModel":
        from mastapy._private.gears.fe_model import _1248

        return self.__parent__._cast(_1248.GearSetFEModel)

    @property
    def cylindrical_gear_set_fe_model(
        self: "CastSelf",
    ) -> "_1251.CylindricalGearSetFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1251

        return self.__parent__._cast(_1251.CylindricalGearSetFEModel)

    @property
    def conical_set_fe_model(self: "CastSelf") -> "_1254.ConicalSetFEModel":
        from mastapy._private.gears.fe_model.conical import _1254

        return self.__parent__._cast(_1254.ConicalSetFEModel)

    @property
    def gear_set_implementation_analysis(
        self: "CastSelf",
    ) -> "_1276.GearSetImplementationAnalysis":
        from mastapy._private.gears.analysis import _1276

        return self.__parent__._cast(_1276.GearSetImplementationAnalysis)

    @property
    def gear_set_implementation_analysis_abstract(
        self: "CastSelf",
    ) -> "_1277.GearSetImplementationAnalysisAbstract":
        from mastapy._private.gears.analysis import _1277

        return self.__parent__._cast(_1277.GearSetImplementationAnalysisAbstract)

    @property
    def gear_set_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1278.GearSetImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1278

        return self.__parent__._cast(_1278.GearSetImplementationAnalysisDutyCycle)

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1279.GearSetImplementationDetail":
        from mastapy._private.gears.analysis import _1279

        return self.__parent__._cast(_1279.GearSetImplementationDetail)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "GearSetDesignAnalysis":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class GearSetDesignAnalysis(_1265.AbstractGearSetAnalysis):
    """GearSetDesignAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_DESIGN_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetDesignAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearSetDesignAnalysis
        """
        return _Cast_GearSetDesignAnalysis(self)
