"""Esfuerzos de flexión, presión, von Mises y concentración (subsecciones 6-10 a 6-12)."""

from __future__ import annotations

import math
from collections.abc import Callable

from scipy import integrate

from thermowell_sizer.core import constants as k


def g_support_tapered(length: float, a: float, b: float, d: float, l0: float = 0.0) -> float:
    """Parámetro G_SP en el plano de soporte, vástago recto o cónico (eqs. 6-10-7 y 6-10-8)."""
    base = 16.0 * length**2 / (3.0 * math.pi * a**2 * (1.0 - (d / a) ** 4))
    s = l0 / length
    return base * (3.0 * (1.0 - s**2) + 2.0 * (b / a - 1.0) * (1.0 - s**3))


def g_support_stepped(
    length: float, a: float, b: float, d: float, ls: float, l0: float = 0.0
) -> float:
    """Parámetro G_SP en el plano de soporte, vástago escalonado (eqs. 6-10-9 y 6-10-11)."""
    denominator = math.pi * a**2 * (1.0 - (d / a) ** 4)
    s = l0 / length
    if l0 < length - ls:
        ba = b / a
        braces = ba + (1.0 - ba) * (1.0 - ls / length) ** 2 - s**2
        return 16.0 * length**2 / denominator * braces
    return 16.0 * b * length**2 / (denominator * a) * (1.0 - s**2)


def g_step_base(length: float, b: float, d: float, ls: float, l0: float = 0.0) -> float:
    """Parámetro G_RD en la base del tramo reducido (eqs. 6-10-10 y 6-10-12)."""
    denominator = math.pi * b**2 * (1.0 - (d / b) ** 4)
    if l0 <= length - ls:
        return 16.0 * ls**2 / denominator
    s = l0 / length
    return 16.0 * length**2 / denominator * (1.0 - s) * (2.0 * ls / length - 1.0 + s)


def g_numeric(
    diameter_at: Callable[[float], float], d: float, length: float, z_s: float, z_lower: float
) -> float:
    """Parámetro G por integración numérica de la definición (eq. 6-10-3).

    Sirve para perfiles no cubiertos por las fórmulas cerradas (exposición parcial,
    párr. 6-10.6) y para verificar esas fórmulas.

    Args:
        diameter_at: diámetro exterior D(z) en función de la distancia z desde el soporte.
        d: diámetro del agujero.
        length: longitud no soportada L.
        z_s: sección donde se evalúa el esfuerzo.
        z_lower: límite inferior de integración, max(z_s, L₀).
    """
    dz = diameter_at(z_s)
    moment, _ = integrate.quad(lambda z: diameter_at(z) * (z - z_s), z_lower, length, limit=200)
    return float(32.0 * dz / (math.pi * (dz**4 - d**4)) * moment)


def steady_drag_stress(g: float, pd: float) -> float:
    """Esfuerzo por arrastre estacionario S_D = G·P_D, Pa (eq. 6-10-4)."""
    return g * pd


def oscillating_stress(g: float, fm: float, p: float) -> float:
    """Amplitud de esfuerzo oscilante S = G·F_M·P, Pa (eqs. 6-10-5 y 6-10-6)."""
    return g * fm * p


def radial_pressure_stress(p: float) -> float:
    """Esfuerzo radial por presión externa S_r = P, Pa (eq. 6-11-1)."""
    return p


def tangential_pressure_stress(p: float, d: float, diameter: float) -> float:
    """Esfuerzo tangencial S_t = P·(1 + (d/D)²)/(1 − (d/D)²), Pa (eq. 6-11-2)."""
    ratio = (d / diameter) ** 2
    return p * (1.0 + ratio) / (1.0 - ratio)


def axial_pressure_stress(p: float, d: float, diameter: float) -> float:
    """Esfuerzo axial S_a = P/(1 − (d/D)²), Pa (eq. 6-11-3)."""
    return p / (1.0 - (d / diameter) ** 2)


def max_steady_stress(sd: float, sa: float) -> float:
    """Esfuerzo longitudinal máximo S_max = S_D + S_a, Pa (eq. 6-12-1)."""
    return sd + sa


def von_mises(s_max: float, s_r: float, s_t: float) -> float:
    """Esfuerzo equivalente de von Mises, lado izquierdo de la eq. (6-12-2), Pa."""
    return math.sqrt(((s_max - s_r) ** 2 + (s_max - s_t) ** 2 + (s_t - s_r) ** 2) / 2.0)


def stress_concentration(diameter: float, fillet: float, *, threaded: bool = False) -> float:
    """Factor de concentración K_t (párr. 6-12.3 y eq. 6-12-4).

    Con radio de acuerdo desconocido (``fillet`` = 0) o D/b ≥ 33 vale 2,2; en conexiones
    roscadas no puede ser menor que 2,3.
    """
    if fillet > 0.0 and diameter / fillet < k.KT_RATIO_LIMIT:
        kt = k.KT_C0 + k.KT_C1 * diameter / fillet
    else:
        kt = k.KT_DEFAULT
    return max(kt, k.KT_THREADED_MIN) if threaded else kt


def peak_oscillating_stress(kt: float, s_drag: float, s_lift: float) -> float:
    """Amplitud pico combinada S_o,max = K_t·√(S_d² + S_L²), Pa (eq. 6-12-3)."""
    return kt * math.hypot(s_drag, s_lift)
