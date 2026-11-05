"""Frecuencia natural del termopozo con soporte ideal (subsección 6-5)."""

from __future__ import annotations

import math

from thermowell_sizer.core import constants as k
from thermowell_sizer.core.models import ShankProfile


def average_diameter(profile: ShankProfile, a: float, b: float) -> float:
    """Diámetro medio D_a (párr. 6-5.3, paso 1): (A+B)/2 cónico, A recto o escalonado."""
    if profile is ShankProfile.TAPERED:
        return (a + b) / 2.0
    return a


def second_moment(da: float, d: float) -> float:
    """Momento de inercia de la sección anular I = π(D_a⁴ − d⁴)/64, m⁴."""
    return math.pi * (da**4 - d**4) / 64.0


def mass_per_length(rho_m: float, da: float, d: float) -> float:
    """Masa por unidad de longitud m = ρ_m·π(D_a² − d²)/4, kg/m."""
    return rho_m * math.pi * (da**2 - d**2) / 4.0


def approximate_frequency(e: float, i: float, m: float, length: float) -> float:
    """Frecuencia aproximada del voladizo f_a = (1,875²/2π)·√(EI/m)/L², Hz (eq. 6-5-1)."""
    return k.CANTILEVER_EIGENVALUE**2 / (2.0 * math.pi) * math.sqrt(e * i / m) / length**2


def hf_straight_tapered(a: float, b: float, d: float, length: float, da: float) -> float:
    """Factor H_f para vástago recto o cónico (eq. 6-5-2)."""
    taper = 1.0 - b / a
    numerator = k.HF_C0 * (1.0 + taper + taper**2)
    exponent = k.HF_EXP_C * (1.0 - k.HF_EXP_D * d / da)
    return float(numerator / (1.0 + k.HF_C1 * (da / length) ** exponent))


def step_shank_coefficients(b: float) -> k.StepShankCoefficients | None:
    """Coeficientes de la tabla 6-5.3-1 para el diámetro de punta ``b``.

    Acepta la tolerancia de fabricación de ±3 % sobre B (párr. 4-2). Devuelve ``None`` si
    B no corresponde a ninguno de los dos diámetros tabulados (no se permite interpolar).
    """
    for tip, coeffs in k.STEP_SHANK_COEFFS.items():
        if math.isclose(b, tip, rel_tol=k.TOLERANCE_DIAMETER_REL):
            return coeffs
    return None


def hf_stepped(
    a: float, b: float, ls: float, length: float, table_b: float | None = None
) -> float:
    """Factor H_f para vástago escalonado (eq. 6-5-3).

    Args:
        a: diámetro en la raíz.
        b: diámetro de punta.
        ls: longitud del tramo reducido.
        length: longitud no soportada.
        table_b: diámetro con el que se eligen los coeficientes; por defecto ``b``. Se usa
            el nominal cuando ``b`` se reduce por corrosión.

    Raises:
        ValueError: si B no es uno de los diámetros de la tabla 6-5.3-1.
    """
    coeffs = step_shank_coefficients(b if table_b is None else table_b)
    if coeffs is None:
        raise ValueError("La correlación escalonada solo admite B = 12,7 mm o 22,23 mm")
    c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = coeffs.c
    ab = a / b
    lr = ls / length
    y1 = (c1 * ab + c2) * lr + (c3 * ab + c4)
    y2 = (c5 * ab + c6) * lr + (c7 * ab + c8)
    beta = c9 * ab + c10
    return float((y1**-beta + y2**-beta) ** (-1.0 / beta))


def h_fluid_mass(rho: float, rho_m: float) -> float:
    """Factor de masa añadida del fluido H_a,f = 1 − ρ/(2ρ_m) (eq. 6-5-4)."""
    return 1.0 - rho / (2.0 * rho_m)


def h_sensor_mass(rho_s: float, rho_m: float, da: float, d: float) -> float:
    """Factor de masa del sensor H_a,s = 1 − (ρ_s/2ρ_m)·1/((D_a/d)² − 1) (eq. 6-5-5)."""
    return 1.0 - rho_s / (2.0 * rho_m) / ((da / d) ** 2 - 1.0)


def natural_frequency(hf: float, haf: float, has: float, fa: float) -> float:
    """Frecuencia natural con soporte ideal f_n = H_f·H_a,f·H_a,s·f_a, Hz (eq. 6-5-6)."""
    return hf * haf * has * fa
