"""RateableMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_RATEABLE_MESH = python_net_import("SMT.MastaAPI.Gears.Rating", "RateableMesh")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.agma_gleason_conical import _587
    from mastapy._private.gears.rating.bevel.standards import _583
    from mastapy._private.gears.rating.conical import _566
    from mastapy._private.gears.rating.cylindrical import _490
    from mastapy._private.gears.rating.cylindrical.agma import _555
    from mastapy._private.gears.rating.cylindrical.iso6336 import _541, _542
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _512,
        _517,
        _518,
        _519,
    )
    from mastapy._private.gears.rating.hypoid.standards import _463
    from mastapy._private.gears.rating.iso_10300 import _446
    from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _434

    Self = TypeVar("Self", bound="RateableMesh")
    CastSelf = TypeVar("CastSelf", bound="RateableMesh._Cast_RateableMesh")


__docformat__ = "restructuredtext en"
__all__ = ("RateableMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RateableMesh:
    """Special nested class for casting RateableMesh to subclasses."""

    __parent__: "RateableMesh"

    @property
    def klingelnberg_conical_rateable_mesh(
        self: "CastSelf",
    ) -> "_434.KlingelnbergConicalRateableMesh":
        from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _434

        return self.__parent__._cast(_434.KlingelnbergConicalRateableMesh)

    @property
    def iso10300_rateable_mesh(self: "CastSelf") -> "_446.ISO10300RateableMesh":
        from mastapy._private.gears.rating.iso_10300 import _446

        return self.__parent__._cast(_446.ISO10300RateableMesh)

    @property
    def hypoid_rateable_mesh(self: "CastSelf") -> "_463.HypoidRateableMesh":
        from mastapy._private.gears.rating.hypoid.standards import _463

        return self.__parent__._cast(_463.HypoidRateableMesh)

    @property
    def cylindrical_rateable_mesh(self: "CastSelf") -> "_490.CylindricalRateableMesh":
        from mastapy._private.gears.rating.cylindrical import _490

        return self.__parent__._cast(_490.CylindricalRateableMesh)

    @property
    def plastic_gear_vdi2736_abstract_rateable_mesh(
        self: "CastSelf",
    ) -> "_512.PlasticGearVDI2736AbstractRateableMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _512

        return self.__parent__._cast(_512.PlasticGearVDI2736AbstractRateableMesh)

    @property
    def vdi2736_metal_plastic_rateable_mesh(
        self: "CastSelf",
    ) -> "_517.VDI2736MetalPlasticRateableMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _517

        return self.__parent__._cast(_517.VDI2736MetalPlasticRateableMesh)

    @property
    def vdi2736_plastic_metal_rateable_mesh(
        self: "CastSelf",
    ) -> "_518.VDI2736PlasticMetalRateableMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _518

        return self.__parent__._cast(_518.VDI2736PlasticMetalRateableMesh)

    @property
    def vdi2736_plastic_plastic_rateable_mesh(
        self: "CastSelf",
    ) -> "_519.VDI2736PlasticPlasticRateableMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _519

        return self.__parent__._cast(_519.VDI2736PlasticPlasticRateableMesh)

    @property
    def iso6336_metal_rateable_mesh(
        self: "CastSelf",
    ) -> "_541.ISO6336MetalRateableMesh":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _541

        return self.__parent__._cast(_541.ISO6336MetalRateableMesh)

    @property
    def iso6336_rateable_mesh(self: "CastSelf") -> "_542.ISO6336RateableMesh":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _542

        return self.__parent__._cast(_542.ISO6336RateableMesh)

    @property
    def agma2101_rateable_mesh(self: "CastSelf") -> "_555.AGMA2101RateableMesh":
        from mastapy._private.gears.rating.cylindrical.agma import _555

        return self.__parent__._cast(_555.AGMA2101RateableMesh)

    @property
    def conical_rateable_mesh(self: "CastSelf") -> "_566.ConicalRateableMesh":
        from mastapy._private.gears.rating.conical import _566

        return self.__parent__._cast(_566.ConicalRateableMesh)

    @property
    def spiral_bevel_rateable_mesh(self: "CastSelf") -> "_583.SpiralBevelRateableMesh":
        from mastapy._private.gears.rating.bevel.standards import _583

        return self.__parent__._cast(_583.SpiralBevelRateableMesh)

    @property
    def agma_gleason_conical_rateable_mesh(
        self: "CastSelf",
    ) -> "_587.AGMAGleasonConicalRateableMesh":
        from mastapy._private.gears.rating.agma_gleason_conical import _587

        return self.__parent__._cast(_587.AGMAGleasonConicalRateableMesh)

    @property
    def rateable_mesh(self: "CastSelf") -> "RateableMesh":
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
class RateableMesh(_0.APIBase):
    """RateableMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RATEABLE_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RateableMesh":
        """Cast to another type.

        Returns:
            _Cast_RateableMesh
        """
        return _Cast_RateableMesh(self)
