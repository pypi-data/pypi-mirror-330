"""NamedDatabaseItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_NAMED_DATABASE_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Databases", "NamedDatabaseItem"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings import _1942
    from mastapy._private.bearings.bearing_results.rolling import _2036
    from mastapy._private.bolts import _1525, _1527, _1529
    from mastapy._private.cycloidal import _1515, _1522
    from mastapy._private.detailed_rigid_connectors.splines import _1475
    from mastapy._private.electric_machines import _1338, _1356, _1371
    from mastapy._private.gears import _360
    from mastapy._private.gears.gear_designs import _973, _975, _978
    from mastapy._private.gears.gear_designs.cylindrical import _1052, _1060
    from mastapy._private.gears.manufacturing.bevel import _830
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _737,
        _738,
        _739,
        _740,
        _741,
        _743,
        _744,
        _745,
        _746,
        _749,
    )
    from mastapy._private.gears.materials import (
        _602,
        _605,
        _607,
        _612,
        _616,
        _624,
        _626,
        _629,
        _633,
        _636,
    )
    from mastapy._private.gears.rating.cylindrical import _473, _489
    from mastapy._private.materials import _264, _286, _288, _292
    from mastapy._private.math_utility.optimisation import _1606
    from mastapy._private.nodal_analysis import _53
    from mastapy._private.shafts import _24, _43, _46
    from mastapy._private.system_model.optimization import _2289, _2292, _2297, _2298
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2632,
    )
    from mastapy._private.utility import _1640
    from mastapy._private.utility.databases import _1891

    Self = TypeVar("Self", bound="NamedDatabaseItem")
    CastSelf = TypeVar("CastSelf", bound="NamedDatabaseItem._Cast_NamedDatabaseItem")


__docformat__ = "restructuredtext en"
__all__ = ("NamedDatabaseItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NamedDatabaseItem:
    """Special nested class for casting NamedDatabaseItem to subclasses."""

    __parent__: "NamedDatabaseItem"

    @property
    def shaft_material(self: "CastSelf") -> "_24.ShaftMaterial":
        from mastapy._private.shafts import _24

        return self.__parent__._cast(_24.ShaftMaterial)

    @property
    def shaft_settings_item(self: "CastSelf") -> "_43.ShaftSettingsItem":
        from mastapy._private.shafts import _43

        return self.__parent__._cast(_43.ShaftSettingsItem)

    @property
    def simple_shaft_definition(self: "CastSelf") -> "_46.SimpleShaftDefinition":
        from mastapy._private.shafts import _46

        return self.__parent__._cast(_46.SimpleShaftDefinition)

    @property
    def analysis_settings_item(self: "CastSelf") -> "_53.AnalysisSettingsItem":
        from mastapy._private.nodal_analysis import _53

        return self.__parent__._cast(_53.AnalysisSettingsItem)

    @property
    def bearing_material(self: "CastSelf") -> "_264.BearingMaterial":
        from mastapy._private.materials import _264

        return self.__parent__._cast(_264.BearingMaterial)

    @property
    def lubrication_detail(self: "CastSelf") -> "_286.LubricationDetail":
        from mastapy._private.materials import _286

        return self.__parent__._cast(_286.LubricationDetail)

    @property
    def material(self: "CastSelf") -> "_288.Material":
        from mastapy._private.materials import _288

        return self.__parent__._cast(_288.Material)

    @property
    def materials_settings_item(self: "CastSelf") -> "_292.MaterialsSettingsItem":
        from mastapy._private.materials import _292

        return self.__parent__._cast(_292.MaterialsSettingsItem)

    @property
    def pocketing_power_loss_coefficients(
        self: "CastSelf",
    ) -> "_360.PocketingPowerLossCoefficients":
        from mastapy._private.gears import _360

        return self.__parent__._cast(_360.PocketingPowerLossCoefficients)

    @property
    def cylindrical_gear_design_and_rating_settings_item(
        self: "CastSelf",
    ) -> "_473.CylindricalGearDesignAndRatingSettingsItem":
        from mastapy._private.gears.rating.cylindrical import _473

        return self.__parent__._cast(_473.CylindricalGearDesignAndRatingSettingsItem)

    @property
    def cylindrical_plastic_gear_rating_settings_item(
        self: "CastSelf",
    ) -> "_489.CylindricalPlasticGearRatingSettingsItem":
        from mastapy._private.gears.rating.cylindrical import _489

        return self.__parent__._cast(_489.CylindricalPlasticGearRatingSettingsItem)

    @property
    def agma_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_602.AGMACylindricalGearMaterial":
        from mastapy._private.gears.materials import _602

        return self.__parent__._cast(_602.AGMACylindricalGearMaterial)

    @property
    def bevel_gear_iso_material(self: "CastSelf") -> "_605.BevelGearISOMaterial":
        from mastapy._private.gears.materials import _605

        return self.__parent__._cast(_605.BevelGearISOMaterial)

    @property
    def bevel_gear_material(self: "CastSelf") -> "_607.BevelGearMaterial":
        from mastapy._private.gears.materials import _607

        return self.__parent__._cast(_607.BevelGearMaterial)

    @property
    def cylindrical_gear_material(self: "CastSelf") -> "_612.CylindricalGearMaterial":
        from mastapy._private.gears.materials import _612

        return self.__parent__._cast(_612.CylindricalGearMaterial)

    @property
    def gear_material(self: "CastSelf") -> "_616.GearMaterial":
        from mastapy._private.gears.materials import _616

        return self.__parent__._cast(_616.GearMaterial)

    @property
    def iso_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_624.ISOCylindricalGearMaterial":
        from mastapy._private.gears.materials import _624

        return self.__parent__._cast(_624.ISOCylindricalGearMaterial)

    @property
    def isotr1417912001_coefficient_of_friction_constants(
        self: "CastSelf",
    ) -> "_626.ISOTR1417912001CoefficientOfFrictionConstants":
        from mastapy._private.gears.materials import _626

        return self.__parent__._cast(_626.ISOTR1417912001CoefficientOfFrictionConstants)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_material(
        self: "CastSelf",
    ) -> "_629.KlingelnbergCycloPalloidConicalGearMaterial":
        from mastapy._private.gears.materials import _629

        return self.__parent__._cast(_629.KlingelnbergCycloPalloidConicalGearMaterial)

    @property
    def plastic_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_633.PlasticCylindricalGearMaterial":
        from mastapy._private.gears.materials import _633

        return self.__parent__._cast(_633.PlasticCylindricalGearMaterial)

    @property
    def raw_material(self: "CastSelf") -> "_636.RawMaterial":
        from mastapy._private.gears.materials import _636

        return self.__parent__._cast(_636.RawMaterial)

    @property
    def cylindrical_gear_abstract_cutter_design(
        self: "CastSelf",
    ) -> "_737.CylindricalGearAbstractCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _737

        return self.__parent__._cast(_737.CylindricalGearAbstractCutterDesign)

    @property
    def cylindrical_gear_form_grinding_wheel(
        self: "CastSelf",
    ) -> "_738.CylindricalGearFormGrindingWheel":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _738

        return self.__parent__._cast(_738.CylindricalGearFormGrindingWheel)

    @property
    def cylindrical_gear_grinding_worm(
        self: "CastSelf",
    ) -> "_739.CylindricalGearGrindingWorm":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _739

        return self.__parent__._cast(_739.CylindricalGearGrindingWorm)

    @property
    def cylindrical_gear_hob_design(
        self: "CastSelf",
    ) -> "_740.CylindricalGearHobDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _740

        return self.__parent__._cast(_740.CylindricalGearHobDesign)

    @property
    def cylindrical_gear_plunge_shaver(
        self: "CastSelf",
    ) -> "_741.CylindricalGearPlungeShaver":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _741

        return self.__parent__._cast(_741.CylindricalGearPlungeShaver)

    @property
    def cylindrical_gear_rack_design(
        self: "CastSelf",
    ) -> "_743.CylindricalGearRackDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _743

        return self.__parent__._cast(_743.CylindricalGearRackDesign)

    @property
    def cylindrical_gear_real_cutter_design(
        self: "CastSelf",
    ) -> "_744.CylindricalGearRealCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _744

        return self.__parent__._cast(_744.CylindricalGearRealCutterDesign)

    @property
    def cylindrical_gear_shaper(self: "CastSelf") -> "_745.CylindricalGearShaper":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _745

        return self.__parent__._cast(_745.CylindricalGearShaper)

    @property
    def cylindrical_gear_shaver(self: "CastSelf") -> "_746.CylindricalGearShaver":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _746

        return self.__parent__._cast(_746.CylindricalGearShaver)

    @property
    def involute_cutter_design(self: "CastSelf") -> "_749.InvoluteCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _749

        return self.__parent__._cast(_749.InvoluteCutterDesign)

    @property
    def manufacturing_machine(self: "CastSelf") -> "_830.ManufacturingMachine":
        from mastapy._private.gears.manufacturing.bevel import _830

        return self.__parent__._cast(_830.ManufacturingMachine)

    @property
    def bevel_hypoid_gear_design_settings_item(
        self: "CastSelf",
    ) -> "_973.BevelHypoidGearDesignSettingsItem":
        from mastapy._private.gears.gear_designs import _973

        return self.__parent__._cast(_973.BevelHypoidGearDesignSettingsItem)

    @property
    def bevel_hypoid_gear_rating_settings_item(
        self: "CastSelf",
    ) -> "_975.BevelHypoidGearRatingSettingsItem":
        from mastapy._private.gears.gear_designs import _975

        return self.__parent__._cast(_975.BevelHypoidGearRatingSettingsItem)

    @property
    def design_constraints_collection(
        self: "CastSelf",
    ) -> "_978.DesignConstraintsCollection":
        from mastapy._private.gears.gear_designs import _978

        return self.__parent__._cast(_978.DesignConstraintsCollection)

    @property
    def cylindrical_gear_design_constraints(
        self: "CastSelf",
    ) -> "_1052.CylindricalGearDesignConstraints":
        from mastapy._private.gears.gear_designs.cylindrical import _1052

        return self.__parent__._cast(_1052.CylindricalGearDesignConstraints)

    @property
    def cylindrical_gear_micro_geometry_settings_item(
        self: "CastSelf",
    ) -> "_1060.CylindricalGearMicroGeometrySettingsItem":
        from mastapy._private.gears.gear_designs.cylindrical import _1060

        return self.__parent__._cast(_1060.CylindricalGearMicroGeometrySettingsItem)

    @property
    def magnet_material(self: "CastSelf") -> "_1338.MagnetMaterial":
        from mastapy._private.electric_machines import _1338

        return self.__parent__._cast(_1338.MagnetMaterial)

    @property
    def stator_rotor_material(self: "CastSelf") -> "_1356.StatorRotorMaterial":
        from mastapy._private.electric_machines import _1356

        return self.__parent__._cast(_1356.StatorRotorMaterial)

    @property
    def winding_material(self: "CastSelf") -> "_1371.WindingMaterial":
        from mastapy._private.electric_machines import _1371

        return self.__parent__._cast(_1371.WindingMaterial)

    @property
    def spline_material(self: "CastSelf") -> "_1475.SplineMaterial":
        from mastapy._private.detailed_rigid_connectors.splines import _1475

        return self.__parent__._cast(_1475.SplineMaterial)

    @property
    def cycloidal_disc_material(self: "CastSelf") -> "_1515.CycloidalDiscMaterial":
        from mastapy._private.cycloidal import _1515

        return self.__parent__._cast(_1515.CycloidalDiscMaterial)

    @property
    def ring_pins_material(self: "CastSelf") -> "_1522.RingPinsMaterial":
        from mastapy._private.cycloidal import _1522

        return self.__parent__._cast(_1522.RingPinsMaterial)

    @property
    def bolted_joint_material(self: "CastSelf") -> "_1525.BoltedJointMaterial":
        from mastapy._private.bolts import _1525

        return self.__parent__._cast(_1525.BoltedJointMaterial)

    @property
    def bolt_geometry(self: "CastSelf") -> "_1527.BoltGeometry":
        from mastapy._private.bolts import _1527

        return self.__parent__._cast(_1527.BoltGeometry)

    @property
    def bolt_material(self: "CastSelf") -> "_1529.BoltMaterial":
        from mastapy._private.bolts import _1529

        return self.__parent__._cast(_1529.BoltMaterial)

    @property
    def pareto_optimisation_strategy(
        self: "CastSelf",
    ) -> "_1606.ParetoOptimisationStrategy":
        from mastapy._private.math_utility.optimisation import _1606

        return self.__parent__._cast(_1606.ParetoOptimisationStrategy)

    @property
    def bearing_settings_item(self: "CastSelf") -> "_1942.BearingSettingsItem":
        from mastapy._private.bearings import _1942

        return self.__parent__._cast(_1942.BearingSettingsItem)

    @property
    def iso14179_settings(self: "CastSelf") -> "_2036.ISO14179Settings":
        from mastapy._private.bearings.bearing_results.rolling import _2036

        return self.__parent__._cast(_2036.ISO14179Settings)

    @property
    def conical_gear_optimisation_strategy(
        self: "CastSelf",
    ) -> "_2289.ConicalGearOptimisationStrategy":
        from mastapy._private.system_model.optimization import _2289

        return self.__parent__._cast(_2289.ConicalGearOptimisationStrategy)

    @property
    def cylindrical_gear_optimisation_strategy(
        self: "CastSelf",
    ) -> "_2292.CylindricalGearOptimisationStrategy":
        from mastapy._private.system_model.optimization import _2292

        return self.__parent__._cast(_2292.CylindricalGearOptimisationStrategy)

    @property
    def optimization_strategy(self: "CastSelf") -> "_2297.OptimizationStrategy":
        from mastapy._private.system_model.optimization import _2297

        return self.__parent__._cast(_2297.OptimizationStrategy)

    @property
    def optimization_strategy_base(
        self: "CastSelf",
    ) -> "_2298.OptimizationStrategyBase":
        from mastapy._private.system_model.optimization import _2298

        return self.__parent__._cast(_2298.OptimizationStrategyBase)

    @property
    def supercharger_rotor_set(self: "CastSelf") -> "_2632.SuperchargerRotorSet":
        from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
            _2632,
        )

        return self.__parent__._cast(_2632.SuperchargerRotorSet)

    @property
    def named_database_item(self: "CastSelf") -> "NamedDatabaseItem":
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
class NamedDatabaseItem(_0.APIBase):
    """NamedDatabaseItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NAMED_DATABASE_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
        )

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
    def no_history(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NoHistory")

        if temp is None:
            return ""

        return temp

    @property
    def history(self: "Self") -> "_1640.FileHistory":
        """mastapy.utility.FileHistory

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "History")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def database_key(self: "Self") -> "_1891.NamedKey":
        """mastapy.utility.databases.NamedKey"""
        temp = pythonnet_property_get(self.wrapped, "DatabaseKey")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @database_key.setter
    @enforce_parameter_types
    def database_key(self: "Self", value: "_1891.NamedKey") -> None:
        pythonnet_property_set(self.wrapped, "DatabaseKey", value.wrapped)

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_NamedDatabaseItem":
        """Cast to another type.

        Returns:
            _Cast_NamedDatabaseItem
        """
        return _Cast_NamedDatabaseItem(self)
