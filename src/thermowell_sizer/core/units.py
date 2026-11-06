"""Conversión de unidades entre el sistema interno (SI) y los sistemas de presentación.

Política de unidades
--------------------
Todo el modelo de datos y el motor de cálculo trabajan **siempre en SI coherente**:
metro, kilogramo, segundo, pascal **absoluto** y kelvin. La interfaz y los reportes
convierten solo en el borde (entrada/salida). Así, conmutar entre SI e Imperial no
modifica ni redondea los datos guardados.

Los factores de conversión son definiciones exactas (NIST SP 811) salvo que se indique.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

# --- Definiciones exactas (NIST SP 811, apéndice B) ---------------------------------
INCH_M = 0.0254
"""1 in = 0,0254 m (exacto)."""
FOOT_M = 0.3048
"""1 ft = 0,3048 m (exacto)."""
POUND_KG = 0.45359237
"""1 lb (masa) = 0,453 592 37 kg (exacto)."""
STANDARD_GRAVITY = 9.80665
"""g_n = 9,806 65 m/s² (exacto, CGPM 1901)."""
POUND_FORCE_N = POUND_KG * STANDARD_GRAVITY
"""1 lbf = 4,448 221 615 260 5 N."""
PSI_PA = POUND_FORCE_N / INCH_M**2
"""1 psi = 6 894,757 Pa."""
BAR_PA = 1.0e5
"""1 bar = 100 000 Pa (exacto)."""
STANDARD_ATMOSPHERE_PA = 101_325.0
"""Atmósfera estándar, presión barométrica por defecto (exacto)."""
US_GALLON_M3 = 231.0 * INCH_M**3
"""1 galón US = 231 in³ (exacto)."""
CENTIPOISE_PA_S = 1.0e-3
"""1 cP = 0,001 Pa·s (exacto)."""
KELVIN_OFFSET = 273.15
"""T[K] = T[°C] + 273,15 (exacto)."""
RANKINE_PER_KELVIN = 1.8
"""1 K = 1,8 °R (exacto)."""
FAHRENHEIT_OFFSET = 459.67
"""T[°R] = T[°F] + 459,67 (exacto)."""
SECONDS_PER_HOUR = 3600.0
SECONDS_PER_MINUTE = 60.0
SECONDS_PER_DAY = 86_400.0
NORMAL_TO_STANDARD: Final = 288.15 / 273.15
"""1 Nm³ (0 °C) en Sm³ (15 °C), gas ideal a la misma presión de 101,325 kPa."""
SCF_TO_SM3: Final = FOOT_M**3 * 288.15 / (60.0 + FAHRENHEIT_OFFSET) * RANKINE_PER_KELVIN
"""1 pie³ estándar (60 °F, 14,696 psia) en Sm³ (15 °C, 101,325 kPa), gas ideal."""


class UnitSystem(StrEnum):
    """Sistema de unidades de presentación."""

    SI = "SI"
    IMPERIAL = "IMPERIAL"


class QuantityKind(StrEnum):
    """Magnitudes físicas que maneja la aplicación."""

    LENGTH = "length"
    DIAMETER = "diameter"
    PRESSURE = "pressure"
    TEMPERATURE = "temperature"
    TEMPERATURE_DIFFERENCE = "temperature_difference"
    DENSITY = "density"
    DYNAMIC_VISCOSITY = "dynamic_viscosity"
    KINEMATIC_VISCOSITY = "kinematic_viscosity"
    VELOCITY = "velocity"
    MASS_FLOW = "mass_flow"
    VOLUME_FLOW = "volume_flow"
    STANDARD_VOLUME_FLOW = "standard_volume_flow"
    STRESS = "stress"
    ELASTIC_MODULUS = "elastic_modulus"
    FREQUENCY = "frequency"
    MASS = "mass"
    FORCE = "force"
    MOMENT = "moment"
    TIME = "time"
    DIMENSIONLESS = "dimensionless"


@dataclass(frozen=True, slots=True)
class LinearUnit:
    """Unidad de presentación relacionada con el SI por ``si = valor * factor + offset``."""

    symbol: str
    factor: float
    offset: float = 0.0

    def to_si(self, value: float) -> float:
        """Convierte un valor de esta unidad al SI interno."""
        return value * self.factor + self.offset

    def from_si(self, value_si: float) -> float:
        """Convierte un valor SI interno a esta unidad."""
        return (value_si - self.offset) / self.factor


_C = LinearUnit("°C", 1.0, KELVIN_OFFSET)
_F = LinearUnit(
    "°F", 1.0 / RANKINE_PER_KELVIN, FAHRENHEIT_OFFSET / RANKINE_PER_KELVIN
)

#: Unidades de presentación por defecto de cada sistema. Las presiones se muestran
#: como absolutas aquí; la variante manométrica se resuelve en :func:`to_display`.
DEFAULT_UNITS: dict[UnitSystem, dict[QuantityKind, LinearUnit]] = {
    UnitSystem.SI: {
        QuantityKind.LENGTH: LinearUnit("mm", 1.0e-3),
        QuantityKind.DIAMETER: LinearUnit("mm", 1.0e-3),
        QuantityKind.PRESSURE: LinearUnit("bar", BAR_PA),
        QuantityKind.TEMPERATURE: _C,
        QuantityKind.TEMPERATURE_DIFFERENCE: LinearUnit("K", 1.0),
        QuantityKind.DENSITY: LinearUnit("kg/m³", 1.0),
        QuantityKind.DYNAMIC_VISCOSITY: LinearUnit("cP", CENTIPOISE_PA_S),
        QuantityKind.KINEMATIC_VISCOSITY: LinearUnit("cSt", 1.0e-6),
        QuantityKind.VELOCITY: LinearUnit("m/s", 1.0),
        QuantityKind.MASS_FLOW: LinearUnit("kg/h", 1.0 / SECONDS_PER_HOUR),
        QuantityKind.VOLUME_FLOW: LinearUnit("m³/h", 1.0 / SECONDS_PER_HOUR),
        QuantityKind.STANDARD_VOLUME_FLOW: LinearUnit("Sm³/h", 1.0 / SECONDS_PER_HOUR),
        QuantityKind.STRESS: LinearUnit("MPa", 1.0e6),
        QuantityKind.ELASTIC_MODULUS: LinearUnit("GPa", 1.0e9),
        QuantityKind.FREQUENCY: LinearUnit("Hz", 1.0),
        QuantityKind.MASS: LinearUnit("g", 1.0e-3),
        QuantityKind.FORCE: LinearUnit("N", 1.0),
        QuantityKind.MOMENT: LinearUnit("N·m", 1.0),
        QuantityKind.TIME: LinearUnit("s", 1.0),
        QuantityKind.DIMENSIONLESS: LinearUnit("", 1.0),
    },
    UnitSystem.IMPERIAL: {
        QuantityKind.LENGTH: LinearUnit("in", INCH_M),
        QuantityKind.DIAMETER: LinearUnit("in", INCH_M),
        QuantityKind.PRESSURE: LinearUnit("psi", PSI_PA),
        QuantityKind.TEMPERATURE: _F,
        QuantityKind.TEMPERATURE_DIFFERENCE: LinearUnit("°R", 1.0 / RANKINE_PER_KELVIN),
        QuantityKind.DENSITY: LinearUnit("lb/ft³", POUND_KG / FOOT_M**3),
        QuantityKind.DYNAMIC_VISCOSITY: LinearUnit("cP", CENTIPOISE_PA_S),
        QuantityKind.KINEMATIC_VISCOSITY: LinearUnit("ft²/s", FOOT_M**2),
        QuantityKind.VELOCITY: LinearUnit("ft/s", FOOT_M),
        QuantityKind.MASS_FLOW: LinearUnit("lb/h", POUND_KG / SECONDS_PER_HOUR),
        QuantityKind.VOLUME_FLOW: LinearUnit("gpm", US_GALLON_M3 / SECONDS_PER_MINUTE),
        QuantityKind.STANDARD_VOLUME_FLOW: LinearUnit("SCFM", SCF_TO_SM3 / SECONDS_PER_MINUTE),
        QuantityKind.STRESS: LinearUnit("ksi", 1.0e3 * PSI_PA),
        QuantityKind.ELASTIC_MODULUS: LinearUnit("Mpsi", 1.0e6 * PSI_PA),
        QuantityKind.FREQUENCY: LinearUnit("Hz", 1.0),
        QuantityKind.MASS: LinearUnit("lb", POUND_KG),
        QuantityKind.FORCE: LinearUnit("lbf", POUND_FORCE_N),
        QuantityKind.MOMENT: LinearUnit("in·lbf", INCH_M * POUND_FORCE_N),
        QuantityKind.TIME: LinearUnit("s", 1.0),
        QuantityKind.DIMENSIONLESS: LinearUnit("", 1.0),
    },
}

_GAUGE_SUFFIX: dict[UnitSystem, str] = {UnitSystem.SI: "g", UnitSystem.IMPERIAL: "g"}


def unit_for(kind: QuantityKind, system: UnitSystem) -> LinearUnit:
    """Devuelve la unidad de presentación por defecto de ``kind`` en ``system``."""
    return DEFAULT_UNITS[system][kind]


def to_display(
    value_si: float,
    kind: QuantityKind,
    system: UnitSystem,
    *,
    gauge: bool = False,
    barometric_pa: float = STANDARD_ATMOSPHERE_PA,
) -> tuple[float, str]:
    """Convierte un valor SI interno a (valor, símbolo) de presentación.

    Args:
        value_si: valor en SI (presiones en Pa absolutos, temperaturas en K).
        kind: magnitud física.
        system: sistema de presentación.
        gauge: solo para presiones; muestra presión manométrica (barg, psig).
        barometric_pa: presión barométrica local en Pa absolutos.

    Returns:
        Tupla con el valor convertido y su símbolo.

    """
    unit = unit_for(kind, system)
    if kind is QuantityKind.PRESSURE and gauge:
        return unit.from_si(value_si - barometric_pa), unit.symbol + _GAUGE_SUFFIX[system]
    return unit.from_si(value_si), unit.symbol


def from_display(
    value: float,
    kind: QuantityKind,
    system: UnitSystem,
    *,
    gauge: bool = False,
    barometric_pa: float = STANDARD_ATMOSPHERE_PA,
) -> float:
    """Convierte un valor de presentación al SI interno (inversa de :func:`to_display`)."""
    unit = unit_for(kind, system)
    value_si = unit.to_si(value)
    if kind is QuantityKind.PRESSURE and gauge:
        value_si += barometric_pa
    return value_si
