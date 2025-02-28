"""SQLDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.databases import _1885

_SQL_DATABASE = python_net_import("SMT.MastaAPI.Utility.Databases", "SQLDatabase")

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.bearings import _1941, _1954
    from mastapy._private.bearings.bearing_results.rolling import _2037
    from mastapy._private.bolts import _1526, _1528, _1530, _1535
    from mastapy._private.cycloidal import _1516, _1523
    from mastapy._private.electric_machines import _1339, _1357, _1372
    from mastapy._private.gears import _361
    from mastapy._private.gears.gear_designs import _972, _974, _977
    from mastapy._private.gears.gear_designs.cylindrical import _1053, _1059
    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _950,
        _952,
        _953,
        _955,
        _956,
        _957,
        _958,
        _959,
        _960,
        _961,
        _962,
        _963,
        _965,
        _966,
        _967,
        _968,
    )
    from mastapy._private.gears.manufacturing.bevel import _831
    from mastapy._private.gears.manufacturing.cylindrical import _641, _646, _657
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _736,
        _742,
        _747,
        _748,
    )
    from mastapy._private.gears.materials import (
        _604,
        _606,
        _608,
        _610,
        _611,
        _613,
        _614,
        _617,
        _627,
        _628,
        _637,
    )
    from mastapy._private.gears.rating.cylindrical import _472, _488
    from mastapy._private.materials import _265, _268, _287, _289, _291
    from mastapy._private.math_utility.optimisation import _1597, _1609
    from mastapy._private.nodal_analysis import _52
    from mastapy._private.shafts import _25, _42
    from mastapy._private.system_model.optimization import _2291, _2299
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2633,
    )
    from mastapy._private.utility.databases import _1887, _1889

    Self = TypeVar("Self", bound="SQLDatabase")
    CastSelf = TypeVar("CastSelf", bound="SQLDatabase._Cast_SQLDatabase")

TKey = TypeVar("TKey", bound="_1887.DatabaseKey")
TValue = TypeVar("TValue", bound="_0.APIBase")

__docformat__ = "restructuredtext en"
__all__ = ("SQLDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SQLDatabase:
    """Special nested class for casting SQLDatabase to subclasses."""

    __parent__: "SQLDatabase"

    @property
    def database(self: "CastSelf") -> "_1885.Database":
        return self.__parent__._cast(_1885.Database)

    @property
    def shaft_material_database(self: "CastSelf") -> "_25.ShaftMaterialDatabase":
        from mastapy._private.shafts import _25

        return self.__parent__._cast(_25.ShaftMaterialDatabase)

    @property
    def shaft_settings_database(self: "CastSelf") -> "_42.ShaftSettingsDatabase":
        from mastapy._private.shafts import _42

        return self.__parent__._cast(_42.ShaftSettingsDatabase)

    @property
    def analysis_settings_database(self: "CastSelf") -> "_52.AnalysisSettingsDatabase":
        from mastapy._private.nodal_analysis import _52

        return self.__parent__._cast(_52.AnalysisSettingsDatabase)

    @property
    def bearing_material_database(self: "CastSelf") -> "_265.BearingMaterialDatabase":
        from mastapy._private.materials import _265

        return self.__parent__._cast(_265.BearingMaterialDatabase)

    @property
    def component_material_database(
        self: "CastSelf",
    ) -> "_268.ComponentMaterialDatabase":
        from mastapy._private.materials import _268

        return self.__parent__._cast(_268.ComponentMaterialDatabase)

    @property
    def lubrication_detail_database(
        self: "CastSelf",
    ) -> "_287.LubricationDetailDatabase":
        from mastapy._private.materials import _287

        return self.__parent__._cast(_287.LubricationDetailDatabase)

    @property
    def material_database(self: "CastSelf") -> "_289.MaterialDatabase":
        from mastapy._private.materials import _289

        return self.__parent__._cast(_289.MaterialDatabase)

    @property
    def materials_settings_database(
        self: "CastSelf",
    ) -> "_291.MaterialsSettingsDatabase":
        from mastapy._private.materials import _291

        return self.__parent__._cast(_291.MaterialsSettingsDatabase)

    @property
    def pocketing_power_loss_coefficients_database(
        self: "CastSelf",
    ) -> "_361.PocketingPowerLossCoefficientsDatabase":
        from mastapy._private.gears import _361

        return self.__parent__._cast(_361.PocketingPowerLossCoefficientsDatabase)

    @property
    def cylindrical_gear_design_and_rating_settings_database(
        self: "CastSelf",
    ) -> "_472.CylindricalGearDesignAndRatingSettingsDatabase":
        from mastapy._private.gears.rating.cylindrical import _472

        return self.__parent__._cast(
            _472.CylindricalGearDesignAndRatingSettingsDatabase
        )

    @property
    def cylindrical_plastic_gear_rating_settings_database(
        self: "CastSelf",
    ) -> "_488.CylindricalPlasticGearRatingSettingsDatabase":
        from mastapy._private.gears.rating.cylindrical import _488

        return self.__parent__._cast(_488.CylindricalPlasticGearRatingSettingsDatabase)

    @property
    def bevel_gear_abstract_material_database(
        self: "CastSelf",
    ) -> "_604.BevelGearAbstractMaterialDatabase":
        from mastapy._private.gears.materials import _604

        return self.__parent__._cast(_604.BevelGearAbstractMaterialDatabase)

    @property
    def bevel_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_606.BevelGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _606

        return self.__parent__._cast(_606.BevelGearISOMaterialDatabase)

    @property
    def bevel_gear_material_database(
        self: "CastSelf",
    ) -> "_608.BevelGearMaterialDatabase":
        from mastapy._private.gears.materials import _608

        return self.__parent__._cast(_608.BevelGearMaterialDatabase)

    @property
    def cylindrical_gear_agma_material_database(
        self: "CastSelf",
    ) -> "_610.CylindricalGearAGMAMaterialDatabase":
        from mastapy._private.gears.materials import _610

        return self.__parent__._cast(_610.CylindricalGearAGMAMaterialDatabase)

    @property
    def cylindrical_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_611.CylindricalGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _611

        return self.__parent__._cast(_611.CylindricalGearISOMaterialDatabase)

    @property
    def cylindrical_gear_material_database(
        self: "CastSelf",
    ) -> "_613.CylindricalGearMaterialDatabase":
        from mastapy._private.gears.materials import _613

        return self.__parent__._cast(_613.CylindricalGearMaterialDatabase)

    @property
    def cylindrical_gear_plastic_material_database(
        self: "CastSelf",
    ) -> "_614.CylindricalGearPlasticMaterialDatabase":
        from mastapy._private.gears.materials import _614

        return self.__parent__._cast(_614.CylindricalGearPlasticMaterialDatabase)

    @property
    def gear_material_database(self: "CastSelf") -> "_617.GearMaterialDatabase":
        from mastapy._private.gears.materials import _617

        return self.__parent__._cast(_617.GearMaterialDatabase)

    @property
    def isotr1417912001_coefficient_of_friction_constants_database(
        self: "CastSelf",
    ) -> "_627.ISOTR1417912001CoefficientOfFrictionConstantsDatabase":
        from mastapy._private.gears.materials import _627

        return self.__parent__._cast(
            _627.ISOTR1417912001CoefficientOfFrictionConstantsDatabase
        )

    @property
    def klingelnberg_conical_gear_material_database(
        self: "CastSelf",
    ) -> "_628.KlingelnbergConicalGearMaterialDatabase":
        from mastapy._private.gears.materials import _628

        return self.__parent__._cast(_628.KlingelnbergConicalGearMaterialDatabase)

    @property
    def raw_material_database(self: "CastSelf") -> "_637.RawMaterialDatabase":
        from mastapy._private.gears.materials import _637

        return self.__parent__._cast(_637.RawMaterialDatabase)

    @property
    def cylindrical_cutter_database(
        self: "CastSelf",
    ) -> "_641.CylindricalCutterDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _641

        return self.__parent__._cast(_641.CylindricalCutterDatabase)

    @property
    def cylindrical_hob_database(self: "CastSelf") -> "_646.CylindricalHobDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _646

        return self.__parent__._cast(_646.CylindricalHobDatabase)

    @property
    def cylindrical_shaper_database(
        self: "CastSelf",
    ) -> "_657.CylindricalShaperDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _657

        return self.__parent__._cast(_657.CylindricalShaperDatabase)

    @property
    def cylindrical_formed_wheel_grinder_database(
        self: "CastSelf",
    ) -> "_736.CylindricalFormedWheelGrinderDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _736

        return self.__parent__._cast(_736.CylindricalFormedWheelGrinderDatabase)

    @property
    def cylindrical_gear_plunge_shaver_database(
        self: "CastSelf",
    ) -> "_742.CylindricalGearPlungeShaverDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _742

        return self.__parent__._cast(_742.CylindricalGearPlungeShaverDatabase)

    @property
    def cylindrical_gear_shaver_database(
        self: "CastSelf",
    ) -> "_747.CylindricalGearShaverDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _747

        return self.__parent__._cast(_747.CylindricalGearShaverDatabase)

    @property
    def cylindrical_worm_grinder_database(
        self: "CastSelf",
    ) -> "_748.CylindricalWormGrinderDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _748

        return self.__parent__._cast(_748.CylindricalWormGrinderDatabase)

    @property
    def manufacturing_machine_database(
        self: "CastSelf",
    ) -> "_831.ManufacturingMachineDatabase":
        from mastapy._private.gears.manufacturing.bevel import _831

        return self.__parent__._cast(_831.ManufacturingMachineDatabase)

    @property
    def micro_geometry_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_950.MicroGeometryDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _950

        return self.__parent__._cast(
            _950.MicroGeometryDesignSpaceSearchStrategyDatabase
        )

    @property
    def micro_geometry_gear_set_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_952.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _952

        return self.__parent__._cast(
            _952.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase
        )

    @property
    def micro_geometry_gear_set_duty_cycle_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_953.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _953

        return self.__parent__._cast(
            _953.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase
        )

    @property
    def pareto_conical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_955.ParetoConicalRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _955

        return self.__parent__._cast(
            _955.ParetoConicalRatingOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_956.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _956

        return self.__parent__._cast(
            _956.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_957.ParetoCylindricalGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _957

        return self.__parent__._cast(
            _957.ParetoCylindricalGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_958.ParetoCylindricalRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _958

        return self.__parent__._cast(
            _958.ParetoCylindricalRatingOptimisationStrategyDatabase
        )

    @property
    def pareto_face_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_959.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _959

        return self.__parent__._cast(
            _959.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_face_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_960.ParetoFaceGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _960

        return self.__parent__._cast(_960.ParetoFaceGearSetOptimisationStrategyDatabase)

    @property
    def pareto_face_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_961.ParetoFaceRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _961

        return self.__parent__._cast(_961.ParetoFaceRatingOptimisationStrategyDatabase)

    @property
    def pareto_hypoid_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_962.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _962

        return self.__parent__._cast(
            _962.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_hypoid_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_963.ParetoHypoidGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _963

        return self.__parent__._cast(
            _963.ParetoHypoidGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_965.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _965

        return self.__parent__._cast(
            _965.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_966.ParetoSpiralBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _966

        return self.__parent__._cast(
            _966.ParetoSpiralBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_967.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _967

        return self.__parent__._cast(
            _967.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_968.ParetoStraightBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _968

        return self.__parent__._cast(
            _968.ParetoStraightBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def bevel_hypoid_gear_design_settings_database(
        self: "CastSelf",
    ) -> "_972.BevelHypoidGearDesignSettingsDatabase":
        from mastapy._private.gears.gear_designs import _972

        return self.__parent__._cast(_972.BevelHypoidGearDesignSettingsDatabase)

    @property
    def bevel_hypoid_gear_rating_settings_database(
        self: "CastSelf",
    ) -> "_974.BevelHypoidGearRatingSettingsDatabase":
        from mastapy._private.gears.gear_designs import _974

        return self.__parent__._cast(_974.BevelHypoidGearRatingSettingsDatabase)

    @property
    def design_constraint_collection_database(
        self: "CastSelf",
    ) -> "_977.DesignConstraintCollectionDatabase":
        from mastapy._private.gears.gear_designs import _977

        return self.__parent__._cast(_977.DesignConstraintCollectionDatabase)

    @property
    def cylindrical_gear_design_constraints_database(
        self: "CastSelf",
    ) -> "_1053.CylindricalGearDesignConstraintsDatabase":
        from mastapy._private.gears.gear_designs.cylindrical import _1053

        return self.__parent__._cast(_1053.CylindricalGearDesignConstraintsDatabase)

    @property
    def cylindrical_gear_micro_geometry_settings_database(
        self: "CastSelf",
    ) -> "_1059.CylindricalGearMicroGeometrySettingsDatabase":
        from mastapy._private.gears.gear_designs.cylindrical import _1059

        return self.__parent__._cast(_1059.CylindricalGearMicroGeometrySettingsDatabase)

    @property
    def magnet_material_database(self: "CastSelf") -> "_1339.MagnetMaterialDatabase":
        from mastapy._private.electric_machines import _1339

        return self.__parent__._cast(_1339.MagnetMaterialDatabase)

    @property
    def stator_rotor_material_database(
        self: "CastSelf",
    ) -> "_1357.StatorRotorMaterialDatabase":
        from mastapy._private.electric_machines import _1357

        return self.__parent__._cast(_1357.StatorRotorMaterialDatabase)

    @property
    def winding_material_database(self: "CastSelf") -> "_1372.WindingMaterialDatabase":
        from mastapy._private.electric_machines import _1372

        return self.__parent__._cast(_1372.WindingMaterialDatabase)

    @property
    def cycloidal_disc_material_database(
        self: "CastSelf",
    ) -> "_1516.CycloidalDiscMaterialDatabase":
        from mastapy._private.cycloidal import _1516

        return self.__parent__._cast(_1516.CycloidalDiscMaterialDatabase)

    @property
    def ring_pins_material_database(
        self: "CastSelf",
    ) -> "_1523.RingPinsMaterialDatabase":
        from mastapy._private.cycloidal import _1523

        return self.__parent__._cast(_1523.RingPinsMaterialDatabase)

    @property
    def bolted_joint_material_database(
        self: "CastSelf",
    ) -> "_1526.BoltedJointMaterialDatabase":
        from mastapy._private.bolts import _1526

        return self.__parent__._cast(_1526.BoltedJointMaterialDatabase)

    @property
    def bolt_geometry_database(self: "CastSelf") -> "_1528.BoltGeometryDatabase":
        from mastapy._private.bolts import _1528

        return self.__parent__._cast(_1528.BoltGeometryDatabase)

    @property
    def bolt_material_database(self: "CastSelf") -> "_1530.BoltMaterialDatabase":
        from mastapy._private.bolts import _1530

        return self.__parent__._cast(_1530.BoltMaterialDatabase)

    @property
    def clamped_section_material_database(
        self: "CastSelf",
    ) -> "_1535.ClampedSectionMaterialDatabase":
        from mastapy._private.bolts import _1535

        return self.__parent__._cast(_1535.ClampedSectionMaterialDatabase)

    @property
    def design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1597.DesignSpaceSearchStrategyDatabase":
        from mastapy._private.math_utility.optimisation import _1597

        return self.__parent__._cast(_1597.DesignSpaceSearchStrategyDatabase)

    @property
    def pareto_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1609.ParetoOptimisationStrategyDatabase":
        from mastapy._private.math_utility.optimisation import _1609

        return self.__parent__._cast(_1609.ParetoOptimisationStrategyDatabase)

    @property
    def named_database(self: "CastSelf") -> "_1889.NamedDatabase":
        from mastapy._private.utility.databases import _1889

        return self.__parent__._cast(_1889.NamedDatabase)

    @property
    def bearing_settings_database(self: "CastSelf") -> "_1941.BearingSettingsDatabase":
        from mastapy._private.bearings import _1941

        return self.__parent__._cast(_1941.BearingSettingsDatabase)

    @property
    def rolling_bearing_database(self: "CastSelf") -> "_1954.RollingBearingDatabase":
        from mastapy._private.bearings import _1954

        return self.__parent__._cast(_1954.RollingBearingDatabase)

    @property
    def iso14179_settings_database(
        self: "CastSelf",
    ) -> "_2037.ISO14179SettingsDatabase":
        from mastapy._private.bearings.bearing_results.rolling import _2037

        return self.__parent__._cast(_2037.ISO14179SettingsDatabase)

    @property
    def conical_gear_optimization_strategy_database(
        self: "CastSelf",
    ) -> "_2291.ConicalGearOptimizationStrategyDatabase":
        from mastapy._private.system_model.optimization import _2291

        return self.__parent__._cast(_2291.ConicalGearOptimizationStrategyDatabase)

    @property
    def optimization_strategy_database(
        self: "CastSelf",
    ) -> "_2299.OptimizationStrategyDatabase":
        from mastapy._private.system_model.optimization import _2299

        return self.__parent__._cast(_2299.OptimizationStrategyDatabase)

    @property
    def supercharger_rotor_set_database(
        self: "CastSelf",
    ) -> "_2633.SuperchargerRotorSetDatabase":
        from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
            _2633,
        )

        return self.__parent__._cast(_2633.SuperchargerRotorSetDatabase)

    @property
    def sql_database(self: "CastSelf") -> "SQLDatabase":
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
class SQLDatabase(_1885.Database[TKey, TValue]):
    """SQLDatabase

    This is a mastapy class.

    Generic Types:
        TKey
        TValue
    """

    TYPE: ClassVar["Type"] = _SQL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def allow_network_database(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowNetworkDatabase")

        if temp is None:
            return False

        return temp

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def uses_database(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UsesDatabase")

        if temp is None:
            return False

        return temp

    @enforce_parameter_types
    def delete(self: "Self", key: "TKey") -> None:
        """Method does not return.

        Args:
            key (TKey)
        """
        pythonnet_method_call(self.wrapped, "Delete", key)

    def reload(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Reload")

    @enforce_parameter_types
    def save(self: "Self", item: "TValue") -> None:
        """Method does not return.

        Args:
            item (TValue)
        """
        pythonnet_method_call(self.wrapped, "Save", item)

    @property
    def cast_to(self: "Self") -> "_Cast_SQLDatabase":
        """Cast to another type.

        Returns:
            _Cast_SQLDatabase
        """
        return _Cast_SQLDatabase(self)
