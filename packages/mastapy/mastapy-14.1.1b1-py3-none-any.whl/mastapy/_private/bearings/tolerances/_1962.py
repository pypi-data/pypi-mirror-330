"""BearingConnectionComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_BEARING_CONNECTION_COMPONENT = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "BearingConnectionComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.tolerances import (
        _1967,
        _1968,
        _1969,
        _1970,
        _1972,
        _1973,
        _1974,
        _1977,
        _1978,
        _1981,
        _1983,
    )

    Self = TypeVar("Self", bound="BearingConnectionComponent")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingConnectionComponent._Cast_BearingConnectionComponent"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingConnectionComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingConnectionComponent:
    """Special nested class for casting BearingConnectionComponent to subclasses."""

    __parent__: "BearingConnectionComponent"

    @property
    def inner_ring_tolerance(self: "CastSelf") -> "_1967.InnerRingTolerance":
        from mastapy._private.bearings.tolerances import _1967

        return self.__parent__._cast(_1967.InnerRingTolerance)

    @property
    def inner_support_tolerance(self: "CastSelf") -> "_1968.InnerSupportTolerance":
        from mastapy._private.bearings.tolerances import _1968

        return self.__parent__._cast(_1968.InnerSupportTolerance)

    @property
    def interference_detail(self: "CastSelf") -> "_1969.InterferenceDetail":
        from mastapy._private.bearings.tolerances import _1969

        return self.__parent__._cast(_1969.InterferenceDetail)

    @property
    def interference_tolerance(self: "CastSelf") -> "_1970.InterferenceTolerance":
        from mastapy._private.bearings.tolerances import _1970

        return self.__parent__._cast(_1970.InterferenceTolerance)

    @property
    def mounting_sleeve_diameter_detail(
        self: "CastSelf",
    ) -> "_1972.MountingSleeveDiameterDetail":
        from mastapy._private.bearings.tolerances import _1972

        return self.__parent__._cast(_1972.MountingSleeveDiameterDetail)

    @property
    def outer_ring_tolerance(self: "CastSelf") -> "_1973.OuterRingTolerance":
        from mastapy._private.bearings.tolerances import _1973

        return self.__parent__._cast(_1973.OuterRingTolerance)

    @property
    def outer_support_tolerance(self: "CastSelf") -> "_1974.OuterSupportTolerance":
        from mastapy._private.bearings.tolerances import _1974

        return self.__parent__._cast(_1974.OuterSupportTolerance)

    @property
    def ring_detail(self: "CastSelf") -> "_1977.RingDetail":
        from mastapy._private.bearings.tolerances import _1977

        return self.__parent__._cast(_1977.RingDetail)

    @property
    def ring_tolerance(self: "CastSelf") -> "_1978.RingTolerance":
        from mastapy._private.bearings.tolerances import _1978

        return self.__parent__._cast(_1978.RingTolerance)

    @property
    def support_detail(self: "CastSelf") -> "_1981.SupportDetail":
        from mastapy._private.bearings.tolerances import _1981

        return self.__parent__._cast(_1981.SupportDetail)

    @property
    def support_tolerance(self: "CastSelf") -> "_1983.SupportTolerance":
        from mastapy._private.bearings.tolerances import _1983

        return self.__parent__._cast(_1983.SupportTolerance)

    @property
    def bearing_connection_component(self: "CastSelf") -> "BearingConnectionComponent":
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
class BearingConnectionComponent(_0.APIBase):
    """BearingConnectionComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_CONNECTION_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BearingConnectionComponent":
        """Cast to another type.

        Returns:
            _Cast_BearingConnectionComponent
        """
        return _Cast_BearingConnectionComponent(self)
