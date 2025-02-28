"""AbstractShaftOrHousing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2508

_ABSTRACT_SHAFT_OR_HOUSING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaftOrHousing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2266
    from mastapy._private.system_model.part_model import _2499, _2517, _2534
    from mastapy._private.system_model.part_model.cycloidal import _2638
    from mastapy._private.system_model.part_model.shaft_model import _2549

    Self = TypeVar("Self", bound="AbstractShaftOrHousing")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractShaftOrHousing._Cast_AbstractShaftOrHousing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftOrHousing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftOrHousing:
    """Special nested class for casting AbstractShaftOrHousing to subclasses."""

    __parent__: "AbstractShaftOrHousing"

    @property
    def component(self: "CastSelf") -> "_2508.Component":
        return self.__parent__._cast(_2508.Component)

    @property
    def part(self: "CastSelf") -> "_2534.Part":
        from mastapy._private.system_model.part_model import _2534

        return self.__parent__._cast(_2534.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2266.DesignEntity":
        from mastapy._private.system_model import _2266

        return self.__parent__._cast(_2266.DesignEntity)

    @property
    def abstract_shaft(self: "CastSelf") -> "_2499.AbstractShaft":
        from mastapy._private.system_model.part_model import _2499

        return self.__parent__._cast(_2499.AbstractShaft)

    @property
    def fe_part(self: "CastSelf") -> "_2517.FEPart":
        from mastapy._private.system_model.part_model import _2517

        return self.__parent__._cast(_2517.FEPart)

    @property
    def shaft(self: "CastSelf") -> "_2549.Shaft":
        from mastapy._private.system_model.part_model.shaft_model import _2549

        return self.__parent__._cast(_2549.Shaft)

    @property
    def cycloidal_disc(self: "CastSelf") -> "_2638.CycloidalDisc":
        from mastapy._private.system_model.part_model.cycloidal import _2638

        return self.__parent__._cast(_2638.CycloidalDisc)

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "AbstractShaftOrHousing":
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
class AbstractShaftOrHousing(_2508.Component):
    """AbstractShaftOrHousing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_OR_HOUSING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftOrHousing":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftOrHousing
        """
        return _Cast_AbstractShaftOrHousing(self)
