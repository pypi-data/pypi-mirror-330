"""MaterialDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.databases import _1889

_MATERIAL_DATABASE = python_net_import("SMT.MastaAPI.Materials", "MaterialDatabase")

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.cycloidal import _1516, _1523
    from mastapy._private.electric_machines import _1339, _1357, _1372
    from mastapy._private.gears.materials import _604, _606, _610, _611, _613, _614
    from mastapy._private.materials import _288
    from mastapy._private.shafts import _25
    from mastapy._private.utility.databases import _1885, _1892

    Self = TypeVar("Self", bound="MaterialDatabase")
    CastSelf = TypeVar("CastSelf", bound="MaterialDatabase._Cast_MaterialDatabase")

T = TypeVar("T", bound="_288.Material")

__docformat__ = "restructuredtext en"
__all__ = ("MaterialDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MaterialDatabase:
    """Special nested class for casting MaterialDatabase to subclasses."""

    __parent__: "MaterialDatabase"

    @property
    def named_database(self: "CastSelf") -> "_1889.NamedDatabase":
        return self.__parent__._cast(_1889.NamedDatabase)

    @property
    def sql_database(self: "CastSelf") -> "_1892.SQLDatabase":
        pass

        from mastapy._private.utility.databases import _1892

        return self.__parent__._cast(_1892.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_1885.Database":
        pass

        from mastapy._private.utility.databases import _1885

        return self.__parent__._cast(_1885.Database)

    @property
    def shaft_material_database(self: "CastSelf") -> "_25.ShaftMaterialDatabase":
        from mastapy._private.shafts import _25

        return self.__parent__._cast(_25.ShaftMaterialDatabase)

    @property
    def bevel_gear_abstract_material_database(
        self: "CastSelf",
    ) -> "_604.BevelGearAbstractMaterialDatabase":
        from mastapy._private.gears.materials import _604

        return self.__parent__._cast(_604.BevelGearAbstractMaterialDatabase)

    @property
    def bevel_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_606.BevelGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _606

        return self.__parent__._cast(_606.BevelGearISOMaterialDatabase)

    @property
    def cylindrical_gear_agma_material_database(
        self: "CastSelf",
    ) -> "_610.CylindricalGearAGMAMaterialDatabase":
        from mastapy._private.gears.materials import _610

        return self.__parent__._cast(_610.CylindricalGearAGMAMaterialDatabase)

    @property
    def cylindrical_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_611.CylindricalGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _611

        return self.__parent__._cast(_611.CylindricalGearISOMaterialDatabase)

    @property
    def cylindrical_gear_material_database(
        self: "CastSelf",
    ) -> "_613.CylindricalGearMaterialDatabase":
        from mastapy._private.gears.materials import _613

        return self.__parent__._cast(_613.CylindricalGearMaterialDatabase)

    @property
    def cylindrical_gear_plastic_material_database(
        self: "CastSelf",
    ) -> "_614.CylindricalGearPlasticMaterialDatabase":
        from mastapy._private.gears.materials import _614

        return self.__parent__._cast(_614.CylindricalGearPlasticMaterialDatabase)

    @property
    def magnet_material_database(self: "CastSelf") -> "_1339.MagnetMaterialDatabase":
        from mastapy._private.electric_machines import _1339

        return self.__parent__._cast(_1339.MagnetMaterialDatabase)

    @property
    def stator_rotor_material_database(
        self: "CastSelf",
    ) -> "_1357.StatorRotorMaterialDatabase":
        from mastapy._private.electric_machines import _1357

        return self.__parent__._cast(_1357.StatorRotorMaterialDatabase)

    @property
    def winding_material_database(self: "CastSelf") -> "_1372.WindingMaterialDatabase":
        from mastapy._private.electric_machines import _1372

        return self.__parent__._cast(_1372.WindingMaterialDatabase)

    @property
    def cycloidal_disc_material_database(
        self: "CastSelf",
    ) -> "_1516.CycloidalDiscMaterialDatabase":
        from mastapy._private.cycloidal import _1516

        return self.__parent__._cast(_1516.CycloidalDiscMaterialDatabase)

    @property
    def ring_pins_material_database(
        self: "CastSelf",
    ) -> "_1523.RingPinsMaterialDatabase":
        from mastapy._private.cycloidal import _1523

        return self.__parent__._cast(_1523.RingPinsMaterialDatabase)

    @property
    def material_database(self: "CastSelf") -> "MaterialDatabase":
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
class MaterialDatabase(_1889.NamedDatabase[T]):
    """MaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _MATERIAL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MaterialDatabase":
        """Cast to another type.

        Returns:
            _Cast_MaterialDatabase
        """
        return _Cast_MaterialDatabase(self)
