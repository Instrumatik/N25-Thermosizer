"""Conversor de unidades por categoría.

Cada unidad se define por un factor a SI y, para temperaturas, un desplazamiento:
``SI = valor · factor + offset``. Las presiones manométricas se manejan aparte porque
dependen de la presión barométrica.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from thermowell_sizer.core.units import (
    BAR_PA,
    CENTIPOISE_PA_S,
    FOOT_M,
    INCH_M,
    KELVIN_OFFSET,
    NORMAL_TO_STANDARD,
    POUND_KG,
    PSI_PA,
    SCF_TO_SM3,
    SECONDS_PER_HOUR,
    SECONDS_PER_MINUTE,
    STANDARD_ATMOSPHERE_PA,
    US_GALLON_M3,
)

GRAVITY: Final = 9.806_65
"""Aceleración normal de la gravedad, m/s² (exacta por definición)."""
WATER_DENSITY_4C: Final = 999.972
"""Densidad del agua para columnas de agua convencionales, kg/m³."""
MMHG_PA: Final = 133.322_387_415
KGF_CM2_PA: Final = GRAVITY * 1.0e4
RANKINE_FACTOR: Final = 5.0 / 9.0
IMPERIAL_GALLON_M3: Final = 4.546_09e-3
BARREL_M3: Final = 42 * US_GALLON_M3
MILE_M: Final = 1609.344
KNOT_M_S: Final = 1852.0 / SECONDS_PER_HOUR
SECONDS_PER_DAY: Final = 86_400.0


@dataclass(frozen=True, slots=True)
class Unit:
    """Unidad de una categoría."""

    symbol: str
    factor: float
    offset: float = 0.0
    gauge: bool = False

    def to_si(self, value: float, barometric: float = STANDARD_ATMOSPHERE_PA) -> float:
        """Valor en SI (presiones manométricas → absolutas)."""
        si = value * self.factor + self.offset
        return si + barometric if self.gauge else si

    def from_si(self, value_si: float, barometric: float = STANDARD_ATMOSPHERE_PA) -> float:
        """Valor en esta unidad."""
        if self.gauge:
            value_si -= barometric
        return (value_si - self.offset) / self.factor


def _p(symbol: str, factor: float) -> tuple[Unit, Unit]:
    return Unit(f"{symbol} (abs)", factor), Unit(f"{symbol}(g)", factor, gauge=True)


_PRESSURE: list[Unit] = []
for _sym, _fac in (("Pa", 1.0), ("kPa", 1e3), ("MPa", 1e6), ("bar", BAR_PA),
                   ("mbar", 100.0), ("psi", PSI_PA), ("kgf/cm²", KGF_CM2_PA),
                   ("atm", STANDARD_ATMOSPHERE_PA), ("mmHg", MMHG_PA),
                   ("inH₂O", INCH_M * WATER_DENSITY_4C * GRAVITY),
                   ("mH₂O", WATER_DENSITY_4C * GRAVITY)):
    _PRESSURE.extend(_p(_sym, _fac))

CATEGORIES: Final[dict[str, tuple[Unit, ...]]] = {
    "temperature": (
        Unit("°C", 1.0, KELVIN_OFFSET), Unit("K", 1.0),
        Unit("°F", RANKINE_FACTOR, KELVIN_OFFSET - 32.0 * RANKINE_FACTOR),
        Unit("°R", RANKINE_FACTOR),
    ),
    "pressure": tuple(_PRESSURE),
    "length": (Unit("m", 1.0), Unit("mm", 1e-3), Unit("cm", 1e-2), Unit("µm", 1e-6),
               Unit("in", INCH_M), Unit("ft", FOOT_M), Unit("mil", INCH_M / 1000)),
    "mass_flow": (Unit("kg/s", 1.0), Unit("kg/h", 1 / SECONDS_PER_HOUR),
                  Unit("t/h", 1000 / SECONDS_PER_HOUR), Unit("lb/h", POUND_KG / SECONDS_PER_HOUR),
                  Unit("lb/s", POUND_KG)),
    "volume_flow": (Unit("m³/s", 1.0), Unit("m³/h", 1 / SECONDS_PER_HOUR),
                    Unit("L/min", 1e-3 / SECONDS_PER_MINUTE), Unit("L/s", 1e-3),
                    Unit("gpm (US)", US_GALLON_M3 / SECONDS_PER_MINUTE),
                    Unit("gpm (UK)", IMPERIAL_GALLON_M3 / SECONDS_PER_MINUTE),
                    Unit("bbl/d", BARREL_M3 / SECONDS_PER_DAY),
                    Unit("ft³/min", FOOT_M**3 / SECONDS_PER_MINUTE)),
    "standard_volume_flow": (
        Unit("Sm³/s", 1.0), Unit("Sm³/h", 1 / SECONDS_PER_HOUR),
        Unit("Sm³/d", 1 / SECONDS_PER_DAY), Unit("Nm³/h", NORMAL_TO_STANDARD / SECONDS_PER_HOUR),
        Unit("Nm³/d", NORMAL_TO_STANDARD / SECONDS_PER_DAY),
        Unit("SCFM", SCF_TO_SM3 / SECONDS_PER_MINUTE), Unit("SCFH", SCF_TO_SM3 / SECONDS_PER_HOUR),
        Unit("MSCFD", 1e3 * SCF_TO_SM3 / SECONDS_PER_DAY),
        Unit("MMSCFD", 1e6 * SCF_TO_SM3 / SECONDS_PER_DAY),
    ),
    "density": (Unit("kg/m³", 1.0), Unit("g/cm³", 1000.0), Unit("lb/ft³", POUND_KG / FOOT_M**3),
                Unit("lb/gal (US)", POUND_KG / US_GALLON_M3)),
    "dynamic_viscosity": (Unit("Pa·s", 1.0), Unit("cP", CENTIPOISE_PA_S), Unit("P", 0.1),
                          Unit("lb/(ft·s)", POUND_KG / FOOT_M)),
    "kinematic_viscosity": (Unit("m²/s", 1.0), Unit("cSt", 1e-6), Unit("St", 1e-4),
                            Unit("ft²/s", FOOT_M**2)),
    "velocity": (Unit("m/s", 1.0), Unit("km/h", 1000 / SECONDS_PER_HOUR), Unit("ft/s", FOOT_M),
                 Unit("ft/min", FOOT_M / SECONDS_PER_MINUTE),
                 Unit("mph", MILE_M / SECONDS_PER_HOUR), Unit("kn", KNOT_M_S)),
    "stress": (Unit("Pa", 1.0), Unit("MPa", 1e6), Unit("N/mm²", 1e6), Unit("GPa", 1e9),
               Unit("psi", PSI_PA), Unit("ksi", 1e3 * PSI_PA), Unit("kgf/mm²", GRAVITY * 1e6)),
    "frequency": (Unit("Hz", 1.0), Unit("kHz", 1e3), Unit("rpm", 1 / SECONDS_PER_MINUTE),
                  Unit("rad/s", 1 / (2 * 3.141_592_653_589_793))),
}


def convert(value: float, category: str, from_symbol: str, to_symbol: str,
            barometric: float = STANDARD_ATMOSPHERE_PA) -> float:
    """Convierte ``value`` entre dos unidades de la misma categoría.

    Raises:
        KeyError: si la categoría o alguna unidad no existe.
    """
    units = {u.symbol: u for u in CATEGORIES[category]}
    return units[to_symbol].from_si(units[from_symbol].to_si(value, barometric), barometric)


def convert_all(value: float, category: str, from_symbol: str,
                barometric: float = STANDARD_ATMOSPHERE_PA) -> list[tuple[str, float]]:
    """Valor expresado en todas las unidades de la categoría."""
    units = CATEGORIES[category]
    si = {u.symbol: u for u in units}[from_symbol].to_si(value, barometric)
    return [(u.symbol, u.from_si(si, barometric)) for u in units]
