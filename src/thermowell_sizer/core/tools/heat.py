"""Estimaciones térmicas para preselección.

Velocidad en tubería, Reynolds, coeficiente de película, error por conducción
(inmersión) y constante de tiempo. Son modelos simplificados de ingeniería; no
forman parte de ASME PTC 19.3 TW y así se informa en los resultados.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Final

CB_RE_TRANSITION: Final = 282_000.0
"""Churchill-Bernstein (1977), cilindro en flujo cruzado, válida para Re·Pr > 0,2."""
DEFAULT_GAP_CONDUCTIVITY: Final = 0.026
"""Aire en el huelgo sensor-agujero, W/(m·K)."""
SENSOR_HEAT_CAPACITY: Final = 2.2e6
"""ρ·c volumétrico típico de un sensor con aislación mineral, J/(m³·K)."""

# Conductividad (W/m·K) y calor específico (J/kg·K) típicos por familia de material.
THERMAL_BY_FAMILY: Final[dict[str, tuple[float, float]]] = {
    "carbon": (51.0, 486.0),
    "low_alloy": (36.0, 473.0),
    "austenitic": (16.2, 500.0),
    "duplex": (17.0, 470.0),
    "nickel": (11.5, 444.0),
    "nickel_copper": (21.8, 427.0),
    "titanium": (21.9, 523.0),
    "refractory": (57.5, 140.0),
}


def pipe_area(inner_diameter: float) -> float:
    """Área de paso, m²."""
    return math.pi * inner_diameter**2 / 4.0


def velocity_from_mass_flow(mass_flow: float, density: float, inner_diameter: float) -> float:
    """V = ṁ / (ρ·A), m/s."""
    return mass_flow / (density * pipe_area(inner_diameter))


def velocity_from_volume_flow(volume_flow: float, inner_diameter: float) -> float:
    """V = Q / A, m/s."""
    return volume_flow / pipe_area(inner_diameter)


def reynolds(density: float, velocity: float, length: float, viscosity: float) -> float:
    """Re = ρ·V·D / μ."""
    return density * velocity * length / viscosity


def churchill_bernstein(re: float, pr: float) -> float:
    """Número de Nusselt medio de un cilindro en flujo cruzado."""
    if re <= 0:
        return 0.3
    lead = 0.62 * math.sqrt(re) * pr ** (1 / 3) / (1 + (0.4 / pr) ** (2 / 3)) ** 0.25
    return float(0.3 + lead * (1 + (re / CB_RE_TRANSITION) ** (5 / 8)) ** (4 / 5))


def film_coefficient(density: float, velocity: float, diameter: float, viscosity: float,
                     conductivity: float, specific_heat: float) -> float:
    """Coeficiente de película h (W/m²·K) sobre el vástago."""
    re = reynolds(density, velocity, diameter, viscosity)
    pr = specific_heat * viscosity / conductivity
    return churchill_bernstein(re, pr) * conductivity / diameter


@dataclass(frozen=True, slots=True)
class ImmersionResult:
    """Error por conducción a lo largo del termopozo (modelo de aleta)."""

    m: float
    """Parámetro de aleta, 1/m."""
    error: float
    """Diferencia punta-fluido, K (mismo signo que T_fluido − T_base)."""
    min_length: float | None
    """Inmersión mínima para que el error sea menor que la tolerancia, m."""


def immersion_error(
    *, fluid_temperature: float, base_temperature: float, h: float, length: float,
    outer_diameter: float, bore: float, conductivity: float, tolerance: float | None = None,
) -> ImmersionResult:
    """Aleta de sección anular con punta adiabática: θ_punta = θ_base / cosh(m·L).

    ``outer_diameter`` es el diámetro medio expuesto (para cónicos, (A + B)/2).
    """
    perimeter = math.pi * outer_diameter
    area = math.pi * (outer_diameter**2 - bore**2) / 4.0
    m = math.sqrt(h * perimeter / (conductivity * area))
    theta = fluid_temperature - base_temperature
    error = theta / math.cosh(m * length)
    min_len: float | None = None
    if tolerance is not None and tolerance > 0:
        ratio = abs(theta) / tolerance
        min_len = math.acosh(ratio) / m if ratio > 1 else 0.0
    return ImmersionResult(m, error, min_len)


@dataclass(frozen=True, slots=True)
class TimeConstant:
    """Constante de tiempo estimada y sus aportes, s."""

    film: float
    gap: float
    sensor: float

    @property
    def total(self) -> float:
        """Suma de aportes (aproximación de primer orden, 63,2 %)."""
        return self.film + self.gap + self.sensor

    @property
    def t90(self) -> float:
        """Tiempo al 90 % para un sistema de primer orden, s."""
        return self.total * math.log(10.0)


def time_constant(
    *, h: float, outer_diameter: float, bore: float, wall_density: float,
    wall_specific_heat: float, sensor_diameter: float,
    gap_conductivity: float = DEFAULT_GAP_CONDUCTIVITY, sensor_tau: float = 0.0,
    sensor_heat_capacity: float = SENSOR_HEAT_CAPACITY,
) -> TimeConstant:
    """Modelo de dos resistencias por unidad de longitud (película y huelgo).

    τ ≈ R_película·(C_pozo + C_sensor) + R_huelgo·C_sensor + τ_sensor.
    """
    c_wall = wall_density * wall_specific_heat * math.pi * (outer_diameter**2 - bore**2) / 4
    c_sensor = sensor_heat_capacity * math.pi * sensor_diameter**2 / 4
    r_film = 1.0 / (h * math.pi * outer_diameter)
    gap_ratio = max(bore / sensor_diameter, 1.0)
    r_gap = math.log(gap_ratio) / (2 * math.pi * gap_conductivity)
    return TimeConstant(r_film * (c_wall + c_sensor), r_gap * c_sensor, sensor_tau)


def corrosion_allowance(rate: float, years: float) -> float:
    """Sobreespesor necesario para la vida de diseño, m (``rate`` en m/año)."""
    return rate * years


def remaining_life(actual_thickness: float, required_thickness: float, rate: float) -> float:
    """Vida remanente, años; infinito si no hay corrosión."""
    if rate <= 0:
        return math.inf
    return max(actual_thickness - required_thickness, 0.0) / rate
