"""PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _510

_PLASTIC_VDI2736_GEAR_SINGLE_FLANK_RATING_IN_A_METAL_PLASTIC_OR_A_PLASTIC_METAL_MESH = (
    python_net_import(
        "SMT.MastaAPI.Gears.Rating.Cylindrical.PlasticVDI2736",
        "PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh",
    )
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _383
    from mastapy._private.gears.rating.cylindrical import _484
    from mastapy._private.gears.rating.cylindrical.iso6336 import _536

    Self = TypeVar(
        "Self",
        bound="PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh._Cast_PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh:
    """Special nested class for casting PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh to subclasses."""

    __parent__: "PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh"

    @property
    def plastic_gear_vdi2736_abstract_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_510.PlasticGearVDI2736AbstractGearSingleFlankRating":
        return self.__parent__._cast(
            _510.PlasticGearVDI2736AbstractGearSingleFlankRating
        )

    @property
    def iso6336_abstract_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_536.ISO6336AbstractGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _536

        return self.__parent__._cast(_536.ISO6336AbstractGearSingleFlankRating)

    @property
    def cylindrical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_484.CylindricalGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical import _484

        return self.__parent__._cast(_484.CylindricalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_383.GearSingleFlankRating":
        from mastapy._private.gears.rating import _383

        return self.__parent__._cast(_383.GearSingleFlankRating)

    @property
    def plastic_vdi2736_gear_single_flank_rating_in_a_metal_plastic_or_a_plastic_metal_mesh(
        self: "CastSelf",
    ) -> "PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh":
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
class PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh(
    _510.PlasticGearVDI2736AbstractGearSingleFlankRating
):
    """PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _PLASTIC_VDI2736_GEAR_SINGLE_FLANK_RATING_IN_A_METAL_PLASTIC_OR_A_PLASTIC_METAL_MESH
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh":
        """Cast to another type.

        Returns:
            _Cast_PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh
        """
        return (
            _Cast_PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh(
                self
            )
        )
