"""GearMeshExcitationDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5799

_GEAR_MESH_EXCITATION_DETAIL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "GearMeshExcitationDetail",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5824,
        _5877,
        _5878,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4757
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2831,
    )
    from mastapy._private.system_model.part_model.gears import _2599

    Self = TypeVar("Self", bound="GearMeshExcitationDetail")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshExcitationDetail._Cast_GearMeshExcitationDetail"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshExcitationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshExcitationDetail:
    """Special nested class for casting GearMeshExcitationDetail to subclasses."""

    __parent__: "GearMeshExcitationDetail"

    @property
    def abstract_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5799.AbstractPeriodicExcitationDetail":
        return self.__parent__._cast(_5799.AbstractPeriodicExcitationDetail)

    @property
    def gear_mesh_misalignment_excitation_detail(
        self: "CastSelf",
    ) -> "_5877.GearMeshMisalignmentExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5877,
        )

        return self.__parent__._cast(_5877.GearMeshMisalignmentExcitationDetail)

    @property
    def gear_mesh_te_excitation_detail(
        self: "CastSelf",
    ) -> "_5878.GearMeshTEExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5878,
        )

        return self.__parent__._cast(_5878.GearMeshTEExcitationDetail)

    @property
    def gear_mesh_excitation_detail(self: "CastSelf") -> "GearMeshExcitationDetail":
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
class GearMeshExcitationDetail(_5799.AbstractPeriodicExcitationDetail):
    """GearMeshExcitationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_EXCITATION_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def uncoupled_modal_analysis(self: "Self") -> "_4757.ModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ModalAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UncoupledModalAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_mesh(self: "Self") -> "_2831.GearMeshSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.GearMeshSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def get_compliance_and_force_data(self: "Self") -> "_5824.ComplianceAndForceData":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.ComplianceAndForceData"""
        method_result = pythonnet_method_call(self.wrapped, "GetComplianceAndForceData")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def get_uncoupled_modal_participation_factors_for(
        self: "Self", gear: "_2599.Gear"
    ) -> "List[float]":
        """List[float]

        Args:
            gear (mastapy.system_model.part_model.gears.Gear)
        """
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped,
                "GetUncoupledModalParticipationFactorsFor",
                gear.wrapped if gear else None,
            ),
            float,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshExcitationDetail":
        """Cast to another type.

        Returns:
            _Cast_GearMeshExcitationDetail
        """
        return _Cast_GearMeshExcitationDetail(self)
