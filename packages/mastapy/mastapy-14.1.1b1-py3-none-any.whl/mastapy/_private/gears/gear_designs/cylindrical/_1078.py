"""CylindricalMeshLinearBacklashSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical import _1031, _1124

_CYLINDRICAL_MESH_LINEAR_BACKLASH_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical",
    "CylindricalMeshLinearBacklashSpecification",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1075, _1107

    Self = TypeVar("Self", bound="CylindricalMeshLinearBacklashSpecification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalMeshLinearBacklashSpecification._Cast_CylindricalMeshLinearBacklashSpecification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMeshLinearBacklashSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalMeshLinearBacklashSpecification:
    """Special nested class for casting CylindricalMeshLinearBacklashSpecification to subclasses."""

    __parent__: "CylindricalMeshLinearBacklashSpecification"

    @property
    def toleranced_value_specification(
        self: "CastSelf",
    ) -> "_1124.TolerancedValueSpecification":
        return self.__parent__._cast(_1124.TolerancedValueSpecification)

    @property
    def relative_measurement_view_model(
        self: "CastSelf",
    ) -> "_1107.RelativeMeasurementViewModel":
        from mastapy._private.gears.gear_designs.cylindrical import _1107

        return self.__parent__._cast(_1107.RelativeMeasurementViewModel)

    @property
    def cylindrical_mesh_angular_backlash(
        self: "CastSelf",
    ) -> "_1075.CylindricalMeshAngularBacklash":
        from mastapy._private.gears.gear_designs.cylindrical import _1075

        return self.__parent__._cast(_1075.CylindricalMeshAngularBacklash)

    @property
    def cylindrical_mesh_linear_backlash_specification(
        self: "CastSelf",
    ) -> "CylindricalMeshLinearBacklashSpecification":
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
class CylindricalMeshLinearBacklashSpecification(
    _1124.TolerancedValueSpecification[_1031.BacklashSpecification]
):
    """CylindricalMeshLinearBacklashSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_MESH_LINEAR_BACKLASH_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def measurement_type(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeasurementType")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalMeshLinearBacklashSpecification":
        """Cast to another type.

        Returns:
            _Cast_CylindricalMeshLinearBacklashSpecification
        """
        return _Cast_CylindricalMeshLinearBacklashSpecification(self)
