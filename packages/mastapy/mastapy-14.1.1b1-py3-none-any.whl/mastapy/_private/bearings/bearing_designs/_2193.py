"""DetailedBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs import _2196

_DETAILED_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns", "DetailedBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2192
    from mastapy._private.bearings.bearing_designs.fluid_film import (
        _2250,
        _2252,
        _2254,
        _2256,
        _2257,
        _2258,
    )
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2197,
        _2198,
        _2199,
        _2200,
        _2201,
        _2202,
        _2204,
        _2210,
        _2211,
        _2212,
        _2216,
        _2221,
        _2222,
        _2223,
        _2224,
        _2227,
        _2229,
        _2232,
        _2233,
        _2234,
        _2235,
        _2236,
        _2237,
    )

    Self = TypeVar("Self", bound="DetailedBearing")
    CastSelf = TypeVar("CastSelf", bound="DetailedBearing._Cast_DetailedBearing")


__docformat__ = "restructuredtext en"
__all__ = ("DetailedBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DetailedBearing:
    """Special nested class for casting DetailedBearing to subclasses."""

    __parent__: "DetailedBearing"

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2196.NonLinearBearing":
        return self.__parent__._cast(_2196.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2192.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2192

        return self.__parent__._cast(_2192.BearingDesign)

    @property
    def angular_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2197.AngularContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2197

        return self.__parent__._cast(_2197.AngularContactBallBearing)

    @property
    def angular_contact_thrust_ball_bearing(
        self: "CastSelf",
    ) -> "_2198.AngularContactThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2198

        return self.__parent__._cast(_2198.AngularContactThrustBallBearing)

    @property
    def asymmetric_spherical_roller_bearing(
        self: "CastSelf",
    ) -> "_2199.AsymmetricSphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2199

        return self.__parent__._cast(_2199.AsymmetricSphericalRollerBearing)

    @property
    def axial_thrust_cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2200.AxialThrustCylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2200

        return self.__parent__._cast(_2200.AxialThrustCylindricalRollerBearing)

    @property
    def axial_thrust_needle_roller_bearing(
        self: "CastSelf",
    ) -> "_2201.AxialThrustNeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2201

        return self.__parent__._cast(_2201.AxialThrustNeedleRollerBearing)

    @property
    def ball_bearing(self: "CastSelf") -> "_2202.BallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2202

        return self.__parent__._cast(_2202.BallBearing)

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2204.BarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2204

        return self.__parent__._cast(_2204.BarrelRollerBearing)

    @property
    def crossed_roller_bearing(self: "CastSelf") -> "_2210.CrossedRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2210

        return self.__parent__._cast(_2210.CrossedRollerBearing)

    @property
    def cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2211.CylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2211

        return self.__parent__._cast(_2211.CylindricalRollerBearing)

    @property
    def deep_groove_ball_bearing(self: "CastSelf") -> "_2212.DeepGrooveBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2212

        return self.__parent__._cast(_2212.DeepGrooveBallBearing)

    @property
    def four_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2216.FourPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2216

        return self.__parent__._cast(_2216.FourPointContactBallBearing)

    @property
    def multi_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2221.MultiPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2221

        return self.__parent__._cast(_2221.MultiPointContactBallBearing)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "_2222.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2222

        return self.__parent__._cast(_2222.NeedleRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2223.NonBarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2223

        return self.__parent__._cast(_2223.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2224.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2224

        return self.__parent__._cast(_2224.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2227.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2227

        return self.__parent__._cast(_2227.RollingBearing)

    @property
    def self_aligning_ball_bearing(self: "CastSelf") -> "_2229.SelfAligningBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2229

        return self.__parent__._cast(_2229.SelfAligningBallBearing)

    @property
    def spherical_roller_bearing(self: "CastSelf") -> "_2232.SphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2232

        return self.__parent__._cast(_2232.SphericalRollerBearing)

    @property
    def spherical_roller_thrust_bearing(
        self: "CastSelf",
    ) -> "_2233.SphericalRollerThrustBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2233

        return self.__parent__._cast(_2233.SphericalRollerThrustBearing)

    @property
    def taper_roller_bearing(self: "CastSelf") -> "_2234.TaperRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2234

        return self.__parent__._cast(_2234.TaperRollerBearing)

    @property
    def three_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2235.ThreePointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2235

        return self.__parent__._cast(_2235.ThreePointContactBallBearing)

    @property
    def thrust_ball_bearing(self: "CastSelf") -> "_2236.ThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2236

        return self.__parent__._cast(_2236.ThrustBallBearing)

    @property
    def toroidal_roller_bearing(self: "CastSelf") -> "_2237.ToroidalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2237

        return self.__parent__._cast(_2237.ToroidalRollerBearing)

    @property
    def pad_fluid_film_bearing(self: "CastSelf") -> "_2250.PadFluidFilmBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2250

        return self.__parent__._cast(_2250.PadFluidFilmBearing)

    @property
    def plain_grease_filled_journal_bearing(
        self: "CastSelf",
    ) -> "_2252.PlainGreaseFilledJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2252

        return self.__parent__._cast(_2252.PlainGreaseFilledJournalBearing)

    @property
    def plain_journal_bearing(self: "CastSelf") -> "_2254.PlainJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2254

        return self.__parent__._cast(_2254.PlainJournalBearing)

    @property
    def plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2256.PlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2256

        return self.__parent__._cast(_2256.PlainOilFedJournalBearing)

    @property
    def tilting_pad_journal_bearing(
        self: "CastSelf",
    ) -> "_2257.TiltingPadJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2257

        return self.__parent__._cast(_2257.TiltingPadJournalBearing)

    @property
    def tilting_pad_thrust_bearing(self: "CastSelf") -> "_2258.TiltingPadThrustBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2258

        return self.__parent__._cast(_2258.TiltingPadThrustBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "DetailedBearing":
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
class DetailedBearing(_2196.NonLinearBearing):
    """DetailedBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DETAILED_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DetailedBearing":
        """Cast to another type.

        Returns:
            _Cast_DetailedBearing
        """
        return _Cast_DetailedBearing(self)
