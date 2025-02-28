"""HypoidRateableMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.agma_gleason_conical import _587

_HYPOID_RATEABLE_MESH = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Hypoid.Standards", "HypoidRateableMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _386
    from mastapy._private.gears.rating.conical import _566

    Self = TypeVar("Self", bound="HypoidRateableMesh")
    CastSelf = TypeVar("CastSelf", bound="HypoidRateableMesh._Cast_HypoidRateableMesh")


__docformat__ = "restructuredtext en"
__all__ = ("HypoidRateableMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidRateableMesh:
    """Special nested class for casting HypoidRateableMesh to subclasses."""

    __parent__: "HypoidRateableMesh"

    @property
    def agma_gleason_conical_rateable_mesh(
        self: "CastSelf",
    ) -> "_587.AGMAGleasonConicalRateableMesh":
        return self.__parent__._cast(_587.AGMAGleasonConicalRateableMesh)

    @property
    def conical_rateable_mesh(self: "CastSelf") -> "_566.ConicalRateableMesh":
        from mastapy._private.gears.rating.conical import _566

        return self.__parent__._cast(_566.ConicalRateableMesh)

    @property
    def rateable_mesh(self: "CastSelf") -> "_386.RateableMesh":
        from mastapy._private.gears.rating import _386

        return self.__parent__._cast(_386.RateableMesh)

    @property
    def hypoid_rateable_mesh(self: "CastSelf") -> "HypoidRateableMesh":
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
class HypoidRateableMesh(_587.AGMAGleasonConicalRateableMesh):
    """HypoidRateableMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_RATEABLE_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_HypoidRateableMesh":
        """Cast to another type.

        Returns:
            _Cast_HypoidRateableMesh
        """
        return _Cast_HypoidRateableMesh(self)
