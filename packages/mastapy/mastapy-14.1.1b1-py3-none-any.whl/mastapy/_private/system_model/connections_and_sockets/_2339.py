"""CylindricalSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2359

_CYLINDRICAL_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CylindricalSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2329,
        _2330,
        _2337,
        _2342,
        _2343,
        _2345,
        _2346,
        _2347,
        _2348,
        _2349,
        _2351,
        _2352,
        _2353,
        _2356,
        _2357,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2406,
        _2408,
        _2410,
        _2412,
        _2414,
        _2416,
        _2417,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2396,
        _2397,
        _2399,
        _2400,
        _2402,
        _2403,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2373

    Self = TypeVar("Self", bound="CylindricalSocket")
    CastSelf = TypeVar("CastSelf", bound="CylindricalSocket._Cast_CylindricalSocket")


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalSocket:
    """Special nested class for casting CylindricalSocket to subclasses."""

    __parent__: "CylindricalSocket"

    @property
    def socket(self: "CastSelf") -> "_2359.Socket":
        return self.__parent__._cast(_2359.Socket)

    @property
    def bearing_inner_socket(self: "CastSelf") -> "_2329.BearingInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2329

        return self.__parent__._cast(_2329.BearingInnerSocket)

    @property
    def bearing_outer_socket(self: "CastSelf") -> "_2330.BearingOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2330

        return self.__parent__._cast(_2330.BearingOuterSocket)

    @property
    def cvt_pulley_socket(self: "CastSelf") -> "_2337.CVTPulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2337

        return self.__parent__._cast(_2337.CVTPulleySocket)

    @property
    def inner_shaft_socket(self: "CastSelf") -> "_2342.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2342

        return self.__parent__._cast(_2342.InnerShaftSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2343.InnerShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2343

        return self.__parent__._cast(_2343.InnerShaftSocketBase)

    @property
    def mountable_component_inner_socket(
        self: "CastSelf",
    ) -> "_2345.MountableComponentInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2345

        return self.__parent__._cast(_2345.MountableComponentInnerSocket)

    @property
    def mountable_component_outer_socket(
        self: "CastSelf",
    ) -> "_2346.MountableComponentOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2346

        return self.__parent__._cast(_2346.MountableComponentOuterSocket)

    @property
    def mountable_component_socket(
        self: "CastSelf",
    ) -> "_2347.MountableComponentSocket":
        from mastapy._private.system_model.connections_and_sockets import _2347

        return self.__parent__._cast(_2347.MountableComponentSocket)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2348.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2348

        return self.__parent__._cast(_2348.OuterShaftSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2349.OuterShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2349

        return self.__parent__._cast(_2349.OuterShaftSocketBase)

    @property
    def planetary_socket(self: "CastSelf") -> "_2351.PlanetarySocket":
        from mastapy._private.system_model.connections_and_sockets import _2351

        return self.__parent__._cast(_2351.PlanetarySocket)

    @property
    def planetary_socket_base(self: "CastSelf") -> "_2352.PlanetarySocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2352

        return self.__parent__._cast(_2352.PlanetarySocketBase)

    @property
    def pulley_socket(self: "CastSelf") -> "_2353.PulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2353

        return self.__parent__._cast(_2353.PulleySocket)

    @property
    def rolling_ring_socket(self: "CastSelf") -> "_2356.RollingRingSocket":
        from mastapy._private.system_model.connections_and_sockets import _2356

        return self.__parent__._cast(_2356.RollingRingSocket)

    @property
    def shaft_socket(self: "CastSelf") -> "_2357.ShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2357

        return self.__parent__._cast(_2357.ShaftSocket)

    @property
    def cylindrical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2373.CylindricalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2373

        return self.__parent__._cast(_2373.CylindricalGearTeethSocket)

    @property
    def cycloidal_disc_axial_left_socket(
        self: "CastSelf",
    ) -> "_2396.CycloidalDiscAxialLeftSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2396,
        )

        return self.__parent__._cast(_2396.CycloidalDiscAxialLeftSocket)

    @property
    def cycloidal_disc_axial_right_socket(
        self: "CastSelf",
    ) -> "_2397.CycloidalDiscAxialRightSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2397,
        )

        return self.__parent__._cast(_2397.CycloidalDiscAxialRightSocket)

    @property
    def cycloidal_disc_inner_socket(
        self: "CastSelf",
    ) -> "_2399.CycloidalDiscInnerSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2399,
        )

        return self.__parent__._cast(_2399.CycloidalDiscInnerSocket)

    @property
    def cycloidal_disc_outer_socket(
        self: "CastSelf",
    ) -> "_2400.CycloidalDiscOuterSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2400,
        )

        return self.__parent__._cast(_2400.CycloidalDiscOuterSocket)

    @property
    def cycloidal_disc_planetary_bearing_socket(
        self: "CastSelf",
    ) -> "_2402.CycloidalDiscPlanetaryBearingSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2402,
        )

        return self.__parent__._cast(_2402.CycloidalDiscPlanetaryBearingSocket)

    @property
    def ring_pins_socket(self: "CastSelf") -> "_2403.RingPinsSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2403,
        )

        return self.__parent__._cast(_2403.RingPinsSocket)

    @property
    def clutch_socket(self: "CastSelf") -> "_2406.ClutchSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2406,
        )

        return self.__parent__._cast(_2406.ClutchSocket)

    @property
    def concept_coupling_socket(self: "CastSelf") -> "_2408.ConceptCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2408,
        )

        return self.__parent__._cast(_2408.ConceptCouplingSocket)

    @property
    def coupling_socket(self: "CastSelf") -> "_2410.CouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2410,
        )

        return self.__parent__._cast(_2410.CouplingSocket)

    @property
    def part_to_part_shear_coupling_socket(
        self: "CastSelf",
    ) -> "_2412.PartToPartShearCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2412,
        )

        return self.__parent__._cast(_2412.PartToPartShearCouplingSocket)

    @property
    def spring_damper_socket(self: "CastSelf") -> "_2414.SpringDamperSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2414,
        )

        return self.__parent__._cast(_2414.SpringDamperSocket)

    @property
    def torque_converter_pump_socket(
        self: "CastSelf",
    ) -> "_2416.TorqueConverterPumpSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2416,
        )

        return self.__parent__._cast(_2416.TorqueConverterPumpSocket)

    @property
    def torque_converter_turbine_socket(
        self: "CastSelf",
    ) -> "_2417.TorqueConverterTurbineSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2417,
        )

        return self.__parent__._cast(_2417.TorqueConverterTurbineSocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "CylindricalSocket":
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
class CylindricalSocket(_2359.Socket):
    """CylindricalSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalSocket":
        """Cast to another type.

        Returns:
            _Cast_CylindricalSocket
        """
        return _Cast_CylindricalSocket(self)
