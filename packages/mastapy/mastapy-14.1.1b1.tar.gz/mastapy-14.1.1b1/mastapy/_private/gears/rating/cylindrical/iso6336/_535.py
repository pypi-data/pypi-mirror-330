"""ISO63362019MeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.cylindrical.iso6336 import _533

_ISO63362019_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336", "ISO63362019MeshSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _385
    from mastapy._private.gears.rating.cylindrical import _486
    from mastapy._private.gears.rating.cylindrical.iso6336 import _537, _539

    Self = TypeVar("Self", bound="ISO63362019MeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO63362019MeshSingleFlankRating._Cast_ISO63362019MeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO63362019MeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO63362019MeshSingleFlankRating:
    """Special nested class for casting ISO63362019MeshSingleFlankRating to subclasses."""

    __parent__: "ISO63362019MeshSingleFlankRating"

    @property
    def iso63362006_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_533.ISO63362006MeshSingleFlankRating":
        return self.__parent__._cast(_533.ISO63362006MeshSingleFlankRating)

    @property
    def iso6336_abstract_metal_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_539.ISO6336AbstractMetalMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _539

        return self.__parent__._cast(_539.ISO6336AbstractMetalMeshSingleFlankRating)

    @property
    def iso6336_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_537.ISO6336AbstractMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _537

        return self.__parent__._cast(_537.ISO6336AbstractMeshSingleFlankRating)

    @property
    def cylindrical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_486.CylindricalMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical import _486

        return self.__parent__._cast(_486.CylindricalMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_385.MeshSingleFlankRating":
        from mastapy._private.gears.rating import _385

        return self.__parent__._cast(_385.MeshSingleFlankRating)

    @property
    def iso63362019_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "ISO63362019MeshSingleFlankRating":
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
class ISO63362019MeshSingleFlankRating(_533.ISO63362006MeshSingleFlankRating):
    """ISO63362019MeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO63362019_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def micro_geometry_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicroGeometryFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def rating_standard_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingStandardName")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO63362019MeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ISO63362019MeshSingleFlankRating
        """
        return _Cast_ISO63362019MeshSingleFlankRating(self)
