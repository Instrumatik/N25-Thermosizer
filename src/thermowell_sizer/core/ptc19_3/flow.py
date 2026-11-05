"""Velocidad, Reynolds, Strouhal y presiones dinámicas (subsecciones 6-3, 6-4 y 7-3).

Todas las funciones son puras y trabajan en SI.
"""

from __future__ import annotations

import math

from thermowell_sizer.core import constants as k


def pipe_area(inner_diameter: float) -> float:
    """Área interna de la tubería, m²."""
    return math.pi * inner_diameter**2 / 4.0


def velocity_from_mass_flow(mass_flow: float, density: float, inner_diameter: float) -> float:
    """Velocidad media V = ṁ / (ρ·A_tubería), m/s.

    Args:
        mass_flow: caudal másico, kg/s.
        density: densidad del fluido, kg/m³.
        inner_diameter: diámetro interno de la tubería, m.
    """
    return mass_flow / (density * pipe_area(inner_diameter))


def velocity_from_volume_flow(volume_flow: float, inner_diameter: float) -> float:
    """Velocidad media V = Q / A_tubería, m/s (Q en m³/s a condiciones de flujo)."""
    return volume_flow / pipe_area(inner_diameter)


def reynolds(velocity: float, tip_diameter: float, density: float, viscosity: float) -> float:
    """Número de Reynolds sobre el diámetro de punta, Re = V·B·ρ/μ (eq. 6-4-3)."""
    return velocity * tip_diameter * density / viscosity


def strouhal_correlation(re: float) -> float:
    """Número de Strouhal en función de Re (eq. 6-4-2).

    Para Re por encima del rango de la correlación se usa 0,22, el mismo valor de la
    rama superior. Para Re < 22 no hay desprendimiento de vórtices y se devuelve 0.
    """
    if re < k.RE_MIN_SHEDDING:
        return 0.0
    if re < k.RE_TRANSITION_1:
        return k.STROUHAL_HIGH_RE * (1.0 - k.RE_MIN_SHEDDING / re)
    if re < k.RE_TRANSITION_2:
        x = math.log10(re / k.RE_TRANSITION_1)
        return k.STROUHAL_MID_C0 - k.STROUHAL_MID_C2 * x**2 + k.STROUHAL_MID_C3 * x**3
    return k.STROUHAL_HIGH_RE


def shedding_frequency(strouhal: float, velocity: float, tip_diameter: float) -> float:
    """Frecuencia de desprendimiento de vórtices fs = N_S·V/B, Hz (eq. 6-4-1)."""
    return strouhal * velocity / tip_diameter


def dynamic_pressure(coefficient: float, density: float, velocity: float) -> float:
    """Fuerza por unidad de área P_β = ½·C_β·ρ·V², Pa (eq. 6-3-3)."""
    return 0.5 * coefficient * density * velocity**2
