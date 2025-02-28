"""IndependentReportablePropertiesBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_INDEPENDENT_REPORTABLE_PROPERTIES_BASE = python_net_import(
    "SMT.MastaAPI.Utility", "IndependentReportablePropertiesBase"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.bearings.bearing_results import _2007
    from mastapy._private.bearings.bearing_results.rolling import _2038, _2132
    from mastapy._private.bearings.tolerances import _1979
    from mastapy._private.electric_machines import _1311
    from mastapy._private.electric_machines.load_cases_and_analyses import _1435
    from mastapy._private.gears import _364
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1058,
        _1089,
        _1097,
        _1098,
        _1101,
        _1102,
        _1111,
        _1119,
        _1121,
        _1125,
        _1129,
    )
    from mastapy._private.geometry import _327
    from mastapy._private.materials.efficiency import _316
    from mastapy._private.math_utility.measured_data import _1623, _1624, _1625
    from mastapy._private.system_model.analyses_and_results.static_loads import _7496
    from mastapy._private.utility import _1657

    Self = TypeVar("Self", bound="IndependentReportablePropertiesBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
    )

T = TypeVar("T", bound="IndependentReportablePropertiesBase")

__docformat__ = "restructuredtext en"
__all__ = ("IndependentReportablePropertiesBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_IndependentReportablePropertiesBase:
    """Special nested class for casting IndependentReportablePropertiesBase to subclasses."""

    __parent__: "IndependentReportablePropertiesBase"

    @property
    def oil_pump_detail(self: "CastSelf") -> "_316.OilPumpDetail":
        from mastapy._private.materials.efficiency import _316

        return self.__parent__._cast(_316.OilPumpDetail)

    @property
    def packaging_limits(self: "CastSelf") -> "_327.PackagingLimits":
        from mastapy._private.geometry import _327

        return self.__parent__._cast(_327.PackagingLimits)

    @property
    def specification_for_the_effect_of_oil_kinematic_viscosity(
        self: "CastSelf",
    ) -> "_364.SpecificationForTheEffectOfOilKinematicViscosity":
        from mastapy._private.gears import _364

        return self.__parent__._cast(
            _364.SpecificationForTheEffectOfOilKinematicViscosity
        )

    @property
    def cylindrical_gear_micro_geometry_settings(
        self: "CastSelf",
    ) -> "_1058.CylindricalGearMicroGeometrySettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1058

        return self.__parent__._cast(_1058.CylindricalGearMicroGeometrySettings)

    @property
    def hardened_material_properties(
        self: "CastSelf",
    ) -> "_1089.HardenedMaterialProperties":
        from mastapy._private.gears.gear_designs.cylindrical import _1089

        return self.__parent__._cast(_1089.HardenedMaterialProperties)

    @property
    def ltca_load_case_modifiable_settings(
        self: "CastSelf",
    ) -> "_1097.LTCALoadCaseModifiableSettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1097

        return self.__parent__._cast(_1097.LTCALoadCaseModifiableSettings)

    @property
    def ltca_settings(self: "CastSelf") -> "_1098.LTCASettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1098

        return self.__parent__._cast(_1098.LTCASettings)

    @property
    def micropitting(self: "CastSelf") -> "_1101.Micropitting":
        from mastapy._private.gears.gear_designs.cylindrical import _1101

        return self.__parent__._cast(_1101.Micropitting)

    @property
    def muller_residual_stress_definition(
        self: "CastSelf",
    ) -> "_1102.MullerResidualStressDefinition":
        from mastapy._private.gears.gear_designs.cylindrical import _1102

        return self.__parent__._cast(_1102.MullerResidualStressDefinition)

    @property
    def scuffing(self: "CastSelf") -> "_1111.Scuffing":
        from mastapy._private.gears.gear_designs.cylindrical import _1111

        return self.__parent__._cast(_1111.Scuffing)

    @property
    def surface_roughness(self: "CastSelf") -> "_1119.SurfaceRoughness":
        from mastapy._private.gears.gear_designs.cylindrical import _1119

        return self.__parent__._cast(_1119.SurfaceRoughness)

    @property
    def tiff_analysis_settings(self: "CastSelf") -> "_1121.TiffAnalysisSettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1121

        return self.__parent__._cast(_1121.TiffAnalysisSettings)

    @property
    def tooth_flank_fracture_analysis_settings(
        self: "CastSelf",
    ) -> "_1125.ToothFlankFractureAnalysisSettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1125

        return self.__parent__._cast(_1125.ToothFlankFractureAnalysisSettings)

    @property
    def usage(self: "CastSelf") -> "_1129.Usage":
        from mastapy._private.gears.gear_designs.cylindrical import _1129

        return self.__parent__._cast(_1129.Usage)

    @property
    def eccentricity(self: "CastSelf") -> "_1311.Eccentricity":
        from mastapy._private.electric_machines import _1311

        return self.__parent__._cast(_1311.Eccentricity)

    @property
    def temperatures(self: "CastSelf") -> "_1435.Temperatures":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1435

        return self.__parent__._cast(_1435.Temperatures)

    @property
    def lookup_table_base(self: "CastSelf") -> "_1623.LookupTableBase":
        from mastapy._private.math_utility.measured_data import _1623

        return self.__parent__._cast(_1623.LookupTableBase)

    @property
    def onedimensional_function_lookup_table(
        self: "CastSelf",
    ) -> "_1624.OnedimensionalFunctionLookupTable":
        from mastapy._private.math_utility.measured_data import _1624

        return self.__parent__._cast(_1624.OnedimensionalFunctionLookupTable)

    @property
    def twodimensional_function_lookup_table(
        self: "CastSelf",
    ) -> "_1625.TwodimensionalFunctionLookupTable":
        from mastapy._private.math_utility.measured_data import _1625

        return self.__parent__._cast(_1625.TwodimensionalFunctionLookupTable)

    @property
    def skf_loss_moment_multipliers(
        self: "CastSelf",
    ) -> "_1657.SKFLossMomentMultipliers":
        from mastapy._private.utility import _1657

        return self.__parent__._cast(_1657.SKFLossMomentMultipliers)

    @property
    def roundness_specification(self: "CastSelf") -> "_1979.RoundnessSpecification":
        from mastapy._private.bearings.tolerances import _1979

        return self.__parent__._cast(_1979.RoundnessSpecification)

    @property
    def equivalent_load_factors(self: "CastSelf") -> "_2007.EquivalentLoadFactors":
        from mastapy._private.bearings.bearing_results import _2007

        return self.__parent__._cast(_2007.EquivalentLoadFactors)

    @property
    def iso14179_settings_per_bearing_type(
        self: "CastSelf",
    ) -> "_2038.ISO14179SettingsPerBearingType":
        from mastapy._private.bearings.bearing_results.rolling import _2038

        return self.__parent__._cast(_2038.ISO14179SettingsPerBearingType)

    @property
    def rolling_bearing_friction_coefficients(
        self: "CastSelf",
    ) -> "_2132.RollingBearingFrictionCoefficients":
        from mastapy._private.bearings.bearing_results.rolling import _2132

        return self.__parent__._cast(_2132.RollingBearingFrictionCoefficients)

    @property
    def additional_acceleration_options(
        self: "CastSelf",
    ) -> "_7496.AdditionalAccelerationOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7496,
        )

        return self.__parent__._cast(_7496.AdditionalAccelerationOptions)

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "IndependentReportablePropertiesBase":
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
class IndependentReportablePropertiesBase(_0.APIBase, Generic[T]):
    """IndependentReportablePropertiesBase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _INDEPENDENT_REPORTABLE_PROPERTIES_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_IndependentReportablePropertiesBase":
        """Cast to another type.

        Returns:
            _Cast_IndependentReportablePropertiesBase
        """
        return _Cast_IndependentReportablePropertiesBase(self)
