"""CylindricalGearOptimisationStrategy"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.optimization import _2293, _2297

_CYLINDRICAL_GEAR_OPTIMISATION_STRATEGY = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization", "CylindricalGearOptimisationStrategy"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.optimization import _2298
    from mastapy._private.utility.databases import _1890

    Self = TypeVar("Self", bound="CylindricalGearOptimisationStrategy")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearOptimisationStrategy._Cast_CylindricalGearOptimisationStrategy",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearOptimisationStrategy",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearOptimisationStrategy:
    """Special nested class for casting CylindricalGearOptimisationStrategy to subclasses."""

    __parent__: "CylindricalGearOptimisationStrategy"

    @property
    def optimization_strategy(self: "CastSelf") -> "_2297.OptimizationStrategy":
        return self.__parent__._cast(_2297.OptimizationStrategy)

    @property
    def optimization_strategy_base(
        self: "CastSelf",
    ) -> "_2298.OptimizationStrategyBase":
        from mastapy._private.system_model.optimization import _2298

        return self.__parent__._cast(_2298.OptimizationStrategyBase)

    @property
    def named_database_item(self: "CastSelf") -> "_1890.NamedDatabaseItem":
        from mastapy._private.utility.databases import _1890

        return self.__parent__._cast(_1890.NamedDatabaseItem)

    @property
    def cylindrical_gear_optimisation_strategy(
        self: "CastSelf",
    ) -> "CylindricalGearOptimisationStrategy":
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
class CylindricalGearOptimisationStrategy(
    _2297.OptimizationStrategy[_2293.CylindricalGearOptimizationStep]
):
    """CylindricalGearOptimisationStrategy

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_OPTIMISATION_STRATEGY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearOptimisationStrategy":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearOptimisationStrategy
        """
        return _Cast_CylindricalGearOptimisationStrategy(self)
