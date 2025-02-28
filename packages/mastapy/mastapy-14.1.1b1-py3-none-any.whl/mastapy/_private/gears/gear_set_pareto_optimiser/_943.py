"""GearSetParetoOptimiser"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.gears.gear_set_pareto_optimiser import _937, _942
from mastapy._private.gears.rating import _373

_GEAR_SET_PARETO_OPTIMISER = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "GearSetParetoOptimiser"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _982
    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _936,
        _939,
        _944,
        _970,
        _971,
    )

    Self = TypeVar("Self", bound="GearSetParetoOptimiser")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetParetoOptimiser._Cast_GearSetParetoOptimiser"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetParetoOptimiser",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetParetoOptimiser:
    """Special nested class for casting GearSetParetoOptimiser to subclasses."""

    __parent__: "GearSetParetoOptimiser"

    @property
    def design_space_search_base(self: "CastSelf") -> "_937.DesignSpaceSearchBase":
        return self.__parent__._cast(_937.DesignSpaceSearchBase)

    @property
    def cylindrical_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_936.CylindricalGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _936

        return self.__parent__._cast(_936.CylindricalGearSetParetoOptimiser)

    @property
    def face_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_939.FaceGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _939

        return self.__parent__._cast(_939.FaceGearSetParetoOptimiser)

    @property
    def hypoid_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_944.HypoidGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _944

        return self.__parent__._cast(_944.HypoidGearSetParetoOptimiser)

    @property
    def spiral_bevel_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_970.SpiralBevelGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _970

        return self.__parent__._cast(_970.SpiralBevelGearSetParetoOptimiser)

    @property
    def straight_bevel_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_971.StraightBevelGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _971

        return self.__parent__._cast(_971.StraightBevelGearSetParetoOptimiser)

    @property
    def gear_set_pareto_optimiser(self: "CastSelf") -> "GearSetParetoOptimiser":
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
class GearSetParetoOptimiser(
    _937.DesignSpaceSearchBase[
        _373.AbstractGearSetRating, _942.GearSetOptimiserCandidate
    ]
):
    """GearSetParetoOptimiser

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_PARETO_OPTIMISER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def number_of_designs_with_gears_which_cannot_be_manufactured_from_cutters(
        self: "Self",
    ) -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfDesignsWithGearsWhichCannotBeManufacturedFromCutters"
        )

        if temp is None:
            return 0

        return temp

    @property
    def remove_candidates_which_cannot_be_manufactured_with_cutters_from_database(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "RemoveCandidatesWhichCannotBeManufacturedWithCuttersFromDatabase",
        )

        if temp is None:
            return False

        return temp

    @remove_candidates_which_cannot_be_manufactured_with_cutters_from_database.setter
    @enforce_parameter_types
    def remove_candidates_which_cannot_be_manufactured_with_cutters_from_database(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RemoveCandidatesWhichCannotBeManufacturedWithCuttersFromDatabase",
            bool(value) if value is not None else False,
        )

    @property
    def remove_candidates_with_warnings(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RemoveCandidatesWithWarnings")

        if temp is None:
            return False

        return temp

    @remove_candidates_with_warnings.setter
    @enforce_parameter_types
    def remove_candidates_with_warnings(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RemoveCandidatesWithWarnings",
            bool(value) if value is not None else False,
        )

    @property
    def selected_candidate_geometry(self: "Self") -> "_982.GearSetDesign":
        """mastapy.gears.gear_designs.GearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedCandidateGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def all_candidate_gear_sets(self: "Self") -> "List[_982.GearSetDesign]":
        """List[mastapy.gears.gear_designs.GearSetDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllCandidateGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def candidate_gear_sets(self: "Self") -> "List[_982.GearSetDesign]":
        """List[mastapy.gears.gear_designs.GearSetDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CandidateGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def add_chart(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddChart")

    def reset_charts(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ResetCharts")

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetParetoOptimiser":
        """Cast to another type.

        Returns:
            _Cast_GearSetParetoOptimiser
        """
        return _Cast_GearSetParetoOptimiser(self)
