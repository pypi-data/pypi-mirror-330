"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.units_and_measurements.measurements._1670 import (
        Acceleration,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1671 import Angle
    from mastapy._private.utility.units_and_measurements.measurements._1672 import (
        AnglePerUnitTemperature,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1673 import (
        AngleSmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1674 import (
        AngleVerySmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1675 import (
        AngularAcceleration,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1676 import (
        AngularCompliance,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1677 import (
        AngularJerk,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1678 import (
        AngularStiffness,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1679 import (
        AngularVelocity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1680 import Area
    from mastapy._private.utility.units_and_measurements.measurements._1681 import (
        AreaSmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1682 import (
        CarbonEmissionFactor,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1683 import (
        CurrentDensity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1684 import (
        CurrentPerLength,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1685 import (
        Cycles,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1686 import (
        Damage,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1687 import (
        DamageRate,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1688 import (
        DataSize,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1689 import (
        Decibel,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1690 import (
        Density,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1691 import (
        ElectricalResistance,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1692 import (
        ElectricalResistivity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1693 import (
        ElectricCurrent,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1694 import (
        Energy,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1695 import (
        EnergyPerUnitArea,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1696 import (
        EnergyPerUnitAreaSmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1697 import (
        EnergySmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1698 import Enum
    from mastapy._private.utility.units_and_measurements.measurements._1699 import (
        FlowRate,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1700 import Force
    from mastapy._private.utility.units_and_measurements.measurements._1701 import (
        ForcePerUnitLength,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1702 import (
        ForcePerUnitPressure,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1703 import (
        ForcePerUnitTemperature,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1704 import (
        FractionMeasurementBase,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1705 import (
        FractionPerTemperature,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1706 import (
        Frequency,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1707 import (
        FuelConsumptionEngine,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1708 import (
        FuelEfficiencyVehicle,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1709 import (
        Gradient,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1710 import (
        HeatConductivity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1711 import (
        HeatTransfer,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1712 import (
        HeatTransferCoefficientForPlasticGearTooth,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1713 import (
        HeatTransferResistance,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1714 import (
        Impulse,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1715 import Index
    from mastapy._private.utility.units_and_measurements.measurements._1716 import (
        Inductance,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1717 import (
        Integer,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1718 import (
        InverseShortLength,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1719 import (
        InverseShortTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1720 import Jerk
    from mastapy._private.utility.units_and_measurements.measurements._1721 import (
        KinematicViscosity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1722 import (
        LengthLong,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1723 import (
        LengthMedium,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1724 import (
        LengthPerUnitTemperature,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1725 import (
        LengthShort,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1726 import (
        LengthToTheFourth,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1727 import (
        LengthVeryLong,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1728 import (
        LengthVeryShort,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1729 import (
        LengthVeryShortPerLengthShort,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1730 import (
        LinearAngularDamping,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1731 import (
        LinearAngularStiffnessCrossTerm,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1732 import (
        LinearDamping,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1733 import (
        LinearFlexibility,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1734 import (
        LinearStiffness,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1735 import (
        MagneticFieldStrength,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1736 import (
        MagneticFlux,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1737 import (
        MagneticFluxDensity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1738 import (
        MagneticVectorPotential,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1739 import (
        MagnetomotiveForce,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1740 import Mass
    from mastapy._private.utility.units_and_measurements.measurements._1741 import (
        MassPerUnitLength,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1742 import (
        MassPerUnitTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1743 import (
        MomentOfInertia,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1744 import (
        MomentOfInertiaPerUnitLength,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1745 import (
        MomentPerUnitPressure,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1746 import (
        Number,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1747 import (
        Percentage,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1748 import Power
    from mastapy._private.utility.units_and_measurements.measurements._1749 import (
        PowerPerSmallArea,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1750 import (
        PowerPerUnitTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1751 import (
        PowerSmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1752 import (
        PowerSmallPerArea,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1753 import (
        PowerSmallPerMass,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1754 import (
        PowerSmallPerUnitAreaPerUnitTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1755 import (
        PowerSmallPerUnitTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1756 import (
        PowerSmallPerVolume,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1757 import (
        Pressure,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1758 import (
        PressurePerUnitTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1759 import (
        PressureSmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1760 import (
        PressureVelocityProduct,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1761 import (
        PressureViscosityCoefficient,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1762 import Price
    from mastapy._private.utility.units_and_measurements.measurements._1763 import (
        PricePerUnitMass,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1764 import (
        QuadraticAngularDamping,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1765 import (
        QuadraticDrag,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1766 import (
        RescaledMeasurement,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1767 import (
        Rotatum,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1768 import (
        SafetyFactor,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1769 import (
        SpecificAcousticImpedance,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1770 import (
        SpecificHeat,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1771 import (
        SquareRootOfUnitForcePerUnitArea,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1772 import (
        StiffnessPerUnitFaceWidth,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1773 import (
        Stress,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1774 import (
        Temperature,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1775 import (
        TemperatureDifference,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1776 import (
        TemperaturePerUnitTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1777 import Text
    from mastapy._private.utility.units_and_measurements.measurements._1778 import (
        ThermalContactCoefficient,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1779 import (
        ThermalExpansionCoefficient,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1780 import (
        ThermoElasticFactor,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1781 import Time
    from mastapy._private.utility.units_and_measurements.measurements._1782 import (
        TimeShort,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1783 import (
        TimeVeryShort,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1784 import (
        Torque,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1785 import (
        TorqueConverterInverseK,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1786 import (
        TorqueConverterK,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1787 import (
        TorquePerCurrent,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1788 import (
        TorquePerSquareRootOfPower,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1789 import (
        TorquePerUnitTemperature,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1790 import (
        Velocity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1791 import (
        VelocitySmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1792 import (
        Viscosity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1793 import (
        Voltage,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1794 import (
        VoltagePerAngularVelocity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1795 import (
        Volume,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1796 import (
        WearCoefficient,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1797 import Yank
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.units_and_measurements.measurements._1670": ["Acceleration"],
        "_private.utility.units_and_measurements.measurements._1671": ["Angle"],
        "_private.utility.units_and_measurements.measurements._1672": [
            "AnglePerUnitTemperature"
        ],
        "_private.utility.units_and_measurements.measurements._1673": ["AngleSmall"],
        "_private.utility.units_and_measurements.measurements._1674": [
            "AngleVerySmall"
        ],
        "_private.utility.units_and_measurements.measurements._1675": [
            "AngularAcceleration"
        ],
        "_private.utility.units_and_measurements.measurements._1676": [
            "AngularCompliance"
        ],
        "_private.utility.units_and_measurements.measurements._1677": ["AngularJerk"],
        "_private.utility.units_and_measurements.measurements._1678": [
            "AngularStiffness"
        ],
        "_private.utility.units_and_measurements.measurements._1679": [
            "AngularVelocity"
        ],
        "_private.utility.units_and_measurements.measurements._1680": ["Area"],
        "_private.utility.units_and_measurements.measurements._1681": ["AreaSmall"],
        "_private.utility.units_and_measurements.measurements._1682": [
            "CarbonEmissionFactor"
        ],
        "_private.utility.units_and_measurements.measurements._1683": [
            "CurrentDensity"
        ],
        "_private.utility.units_and_measurements.measurements._1684": [
            "CurrentPerLength"
        ],
        "_private.utility.units_and_measurements.measurements._1685": ["Cycles"],
        "_private.utility.units_and_measurements.measurements._1686": ["Damage"],
        "_private.utility.units_and_measurements.measurements._1687": ["DamageRate"],
        "_private.utility.units_and_measurements.measurements._1688": ["DataSize"],
        "_private.utility.units_and_measurements.measurements._1689": ["Decibel"],
        "_private.utility.units_and_measurements.measurements._1690": ["Density"],
        "_private.utility.units_and_measurements.measurements._1691": [
            "ElectricalResistance"
        ],
        "_private.utility.units_and_measurements.measurements._1692": [
            "ElectricalResistivity"
        ],
        "_private.utility.units_and_measurements.measurements._1693": [
            "ElectricCurrent"
        ],
        "_private.utility.units_and_measurements.measurements._1694": ["Energy"],
        "_private.utility.units_and_measurements.measurements._1695": [
            "EnergyPerUnitArea"
        ],
        "_private.utility.units_and_measurements.measurements._1696": [
            "EnergyPerUnitAreaSmall"
        ],
        "_private.utility.units_and_measurements.measurements._1697": ["EnergySmall"],
        "_private.utility.units_and_measurements.measurements._1698": ["Enum"],
        "_private.utility.units_and_measurements.measurements._1699": ["FlowRate"],
        "_private.utility.units_and_measurements.measurements._1700": ["Force"],
        "_private.utility.units_and_measurements.measurements._1701": [
            "ForcePerUnitLength"
        ],
        "_private.utility.units_and_measurements.measurements._1702": [
            "ForcePerUnitPressure"
        ],
        "_private.utility.units_and_measurements.measurements._1703": [
            "ForcePerUnitTemperature"
        ],
        "_private.utility.units_and_measurements.measurements._1704": [
            "FractionMeasurementBase"
        ],
        "_private.utility.units_and_measurements.measurements._1705": [
            "FractionPerTemperature"
        ],
        "_private.utility.units_and_measurements.measurements._1706": ["Frequency"],
        "_private.utility.units_and_measurements.measurements._1707": [
            "FuelConsumptionEngine"
        ],
        "_private.utility.units_and_measurements.measurements._1708": [
            "FuelEfficiencyVehicle"
        ],
        "_private.utility.units_and_measurements.measurements._1709": ["Gradient"],
        "_private.utility.units_and_measurements.measurements._1710": [
            "HeatConductivity"
        ],
        "_private.utility.units_and_measurements.measurements._1711": ["HeatTransfer"],
        "_private.utility.units_and_measurements.measurements._1712": [
            "HeatTransferCoefficientForPlasticGearTooth"
        ],
        "_private.utility.units_and_measurements.measurements._1713": [
            "HeatTransferResistance"
        ],
        "_private.utility.units_and_measurements.measurements._1714": ["Impulse"],
        "_private.utility.units_and_measurements.measurements._1715": ["Index"],
        "_private.utility.units_and_measurements.measurements._1716": ["Inductance"],
        "_private.utility.units_and_measurements.measurements._1717": ["Integer"],
        "_private.utility.units_and_measurements.measurements._1718": [
            "InverseShortLength"
        ],
        "_private.utility.units_and_measurements.measurements._1719": [
            "InverseShortTime"
        ],
        "_private.utility.units_and_measurements.measurements._1720": ["Jerk"],
        "_private.utility.units_and_measurements.measurements._1721": [
            "KinematicViscosity"
        ],
        "_private.utility.units_and_measurements.measurements._1722": ["LengthLong"],
        "_private.utility.units_and_measurements.measurements._1723": ["LengthMedium"],
        "_private.utility.units_and_measurements.measurements._1724": [
            "LengthPerUnitTemperature"
        ],
        "_private.utility.units_and_measurements.measurements._1725": ["LengthShort"],
        "_private.utility.units_and_measurements.measurements._1726": [
            "LengthToTheFourth"
        ],
        "_private.utility.units_and_measurements.measurements._1727": [
            "LengthVeryLong"
        ],
        "_private.utility.units_and_measurements.measurements._1728": [
            "LengthVeryShort"
        ],
        "_private.utility.units_and_measurements.measurements._1729": [
            "LengthVeryShortPerLengthShort"
        ],
        "_private.utility.units_and_measurements.measurements._1730": [
            "LinearAngularDamping"
        ],
        "_private.utility.units_and_measurements.measurements._1731": [
            "LinearAngularStiffnessCrossTerm"
        ],
        "_private.utility.units_and_measurements.measurements._1732": ["LinearDamping"],
        "_private.utility.units_and_measurements.measurements._1733": [
            "LinearFlexibility"
        ],
        "_private.utility.units_and_measurements.measurements._1734": [
            "LinearStiffness"
        ],
        "_private.utility.units_and_measurements.measurements._1735": [
            "MagneticFieldStrength"
        ],
        "_private.utility.units_and_measurements.measurements._1736": ["MagneticFlux"],
        "_private.utility.units_and_measurements.measurements._1737": [
            "MagneticFluxDensity"
        ],
        "_private.utility.units_and_measurements.measurements._1738": [
            "MagneticVectorPotential"
        ],
        "_private.utility.units_and_measurements.measurements._1739": [
            "MagnetomotiveForce"
        ],
        "_private.utility.units_and_measurements.measurements._1740": ["Mass"],
        "_private.utility.units_and_measurements.measurements._1741": [
            "MassPerUnitLength"
        ],
        "_private.utility.units_and_measurements.measurements._1742": [
            "MassPerUnitTime"
        ],
        "_private.utility.units_and_measurements.measurements._1743": [
            "MomentOfInertia"
        ],
        "_private.utility.units_and_measurements.measurements._1744": [
            "MomentOfInertiaPerUnitLength"
        ],
        "_private.utility.units_and_measurements.measurements._1745": [
            "MomentPerUnitPressure"
        ],
        "_private.utility.units_and_measurements.measurements._1746": ["Number"],
        "_private.utility.units_and_measurements.measurements._1747": ["Percentage"],
        "_private.utility.units_and_measurements.measurements._1748": ["Power"],
        "_private.utility.units_and_measurements.measurements._1749": [
            "PowerPerSmallArea"
        ],
        "_private.utility.units_and_measurements.measurements._1750": [
            "PowerPerUnitTime"
        ],
        "_private.utility.units_and_measurements.measurements._1751": ["PowerSmall"],
        "_private.utility.units_and_measurements.measurements._1752": [
            "PowerSmallPerArea"
        ],
        "_private.utility.units_and_measurements.measurements._1753": [
            "PowerSmallPerMass"
        ],
        "_private.utility.units_and_measurements.measurements._1754": [
            "PowerSmallPerUnitAreaPerUnitTime"
        ],
        "_private.utility.units_and_measurements.measurements._1755": [
            "PowerSmallPerUnitTime"
        ],
        "_private.utility.units_and_measurements.measurements._1756": [
            "PowerSmallPerVolume"
        ],
        "_private.utility.units_and_measurements.measurements._1757": ["Pressure"],
        "_private.utility.units_and_measurements.measurements._1758": [
            "PressurePerUnitTime"
        ],
        "_private.utility.units_and_measurements.measurements._1759": ["PressureSmall"],
        "_private.utility.units_and_measurements.measurements._1760": [
            "PressureVelocityProduct"
        ],
        "_private.utility.units_and_measurements.measurements._1761": [
            "PressureViscosityCoefficient"
        ],
        "_private.utility.units_and_measurements.measurements._1762": ["Price"],
        "_private.utility.units_and_measurements.measurements._1763": [
            "PricePerUnitMass"
        ],
        "_private.utility.units_and_measurements.measurements._1764": [
            "QuadraticAngularDamping"
        ],
        "_private.utility.units_and_measurements.measurements._1765": ["QuadraticDrag"],
        "_private.utility.units_and_measurements.measurements._1766": [
            "RescaledMeasurement"
        ],
        "_private.utility.units_and_measurements.measurements._1767": ["Rotatum"],
        "_private.utility.units_and_measurements.measurements._1768": ["SafetyFactor"],
        "_private.utility.units_and_measurements.measurements._1769": [
            "SpecificAcousticImpedance"
        ],
        "_private.utility.units_and_measurements.measurements._1770": ["SpecificHeat"],
        "_private.utility.units_and_measurements.measurements._1771": [
            "SquareRootOfUnitForcePerUnitArea"
        ],
        "_private.utility.units_and_measurements.measurements._1772": [
            "StiffnessPerUnitFaceWidth"
        ],
        "_private.utility.units_and_measurements.measurements._1773": ["Stress"],
        "_private.utility.units_and_measurements.measurements._1774": ["Temperature"],
        "_private.utility.units_and_measurements.measurements._1775": [
            "TemperatureDifference"
        ],
        "_private.utility.units_and_measurements.measurements._1776": [
            "TemperaturePerUnitTime"
        ],
        "_private.utility.units_and_measurements.measurements._1777": ["Text"],
        "_private.utility.units_and_measurements.measurements._1778": [
            "ThermalContactCoefficient"
        ],
        "_private.utility.units_and_measurements.measurements._1779": [
            "ThermalExpansionCoefficient"
        ],
        "_private.utility.units_and_measurements.measurements._1780": [
            "ThermoElasticFactor"
        ],
        "_private.utility.units_and_measurements.measurements._1781": ["Time"],
        "_private.utility.units_and_measurements.measurements._1782": ["TimeShort"],
        "_private.utility.units_and_measurements.measurements._1783": ["TimeVeryShort"],
        "_private.utility.units_and_measurements.measurements._1784": ["Torque"],
        "_private.utility.units_and_measurements.measurements._1785": [
            "TorqueConverterInverseK"
        ],
        "_private.utility.units_and_measurements.measurements._1786": [
            "TorqueConverterK"
        ],
        "_private.utility.units_and_measurements.measurements._1787": [
            "TorquePerCurrent"
        ],
        "_private.utility.units_and_measurements.measurements._1788": [
            "TorquePerSquareRootOfPower"
        ],
        "_private.utility.units_and_measurements.measurements._1789": [
            "TorquePerUnitTemperature"
        ],
        "_private.utility.units_and_measurements.measurements._1790": ["Velocity"],
        "_private.utility.units_and_measurements.measurements._1791": ["VelocitySmall"],
        "_private.utility.units_and_measurements.measurements._1792": ["Viscosity"],
        "_private.utility.units_and_measurements.measurements._1793": ["Voltage"],
        "_private.utility.units_and_measurements.measurements._1794": [
            "VoltagePerAngularVelocity"
        ],
        "_private.utility.units_and_measurements.measurements._1795": ["Volume"],
        "_private.utility.units_and_measurements.measurements._1796": [
            "WearCoefficient"
        ],
        "_private.utility.units_and_measurements.measurements._1797": ["Yank"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Acceleration",
    "Angle",
    "AnglePerUnitTemperature",
    "AngleSmall",
    "AngleVerySmall",
    "AngularAcceleration",
    "AngularCompliance",
    "AngularJerk",
    "AngularStiffness",
    "AngularVelocity",
    "Area",
    "AreaSmall",
    "CarbonEmissionFactor",
    "CurrentDensity",
    "CurrentPerLength",
    "Cycles",
    "Damage",
    "DamageRate",
    "DataSize",
    "Decibel",
    "Density",
    "ElectricalResistance",
    "ElectricalResistivity",
    "ElectricCurrent",
    "Energy",
    "EnergyPerUnitArea",
    "EnergyPerUnitAreaSmall",
    "EnergySmall",
    "Enum",
    "FlowRate",
    "Force",
    "ForcePerUnitLength",
    "ForcePerUnitPressure",
    "ForcePerUnitTemperature",
    "FractionMeasurementBase",
    "FractionPerTemperature",
    "Frequency",
    "FuelConsumptionEngine",
    "FuelEfficiencyVehicle",
    "Gradient",
    "HeatConductivity",
    "HeatTransfer",
    "HeatTransferCoefficientForPlasticGearTooth",
    "HeatTransferResistance",
    "Impulse",
    "Index",
    "Inductance",
    "Integer",
    "InverseShortLength",
    "InverseShortTime",
    "Jerk",
    "KinematicViscosity",
    "LengthLong",
    "LengthMedium",
    "LengthPerUnitTemperature",
    "LengthShort",
    "LengthToTheFourth",
    "LengthVeryLong",
    "LengthVeryShort",
    "LengthVeryShortPerLengthShort",
    "LinearAngularDamping",
    "LinearAngularStiffnessCrossTerm",
    "LinearDamping",
    "LinearFlexibility",
    "LinearStiffness",
    "MagneticFieldStrength",
    "MagneticFlux",
    "MagneticFluxDensity",
    "MagneticVectorPotential",
    "MagnetomotiveForce",
    "Mass",
    "MassPerUnitLength",
    "MassPerUnitTime",
    "MomentOfInertia",
    "MomentOfInertiaPerUnitLength",
    "MomentPerUnitPressure",
    "Number",
    "Percentage",
    "Power",
    "PowerPerSmallArea",
    "PowerPerUnitTime",
    "PowerSmall",
    "PowerSmallPerArea",
    "PowerSmallPerMass",
    "PowerSmallPerUnitAreaPerUnitTime",
    "PowerSmallPerUnitTime",
    "PowerSmallPerVolume",
    "Pressure",
    "PressurePerUnitTime",
    "PressureSmall",
    "PressureVelocityProduct",
    "PressureViscosityCoefficient",
    "Price",
    "PricePerUnitMass",
    "QuadraticAngularDamping",
    "QuadraticDrag",
    "RescaledMeasurement",
    "Rotatum",
    "SafetyFactor",
    "SpecificAcousticImpedance",
    "SpecificHeat",
    "SquareRootOfUnitForcePerUnitArea",
    "StiffnessPerUnitFaceWidth",
    "Stress",
    "Temperature",
    "TemperatureDifference",
    "TemperaturePerUnitTime",
    "Text",
    "ThermalContactCoefficient",
    "ThermalExpansionCoefficient",
    "ThermoElasticFactor",
    "Time",
    "TimeShort",
    "TimeVeryShort",
    "Torque",
    "TorqueConverterInverseK",
    "TorqueConverterK",
    "TorquePerCurrent",
    "TorquePerSquareRootOfPower",
    "TorquePerUnitTemperature",
    "Velocity",
    "VelocitySmall",
    "Viscosity",
    "Voltage",
    "VoltagePerAngularVelocity",
    "Volume",
    "WearCoefficient",
    "Yank",
)
