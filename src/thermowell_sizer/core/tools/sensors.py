"""Sensores: Pt100 (Callendar-Van Dusen, IEC 60751) y termopares (NIST ITS-90)."""

from __future__ import annotations

import math
from enum import StrEnum
from typing import Final

from scipy.optimize import brentq

from thermowell_sizer.core.tools.thermocouple_data import NIST_ITS90

# --- RTD Pt100 (IEC 60751) ------------------------------------------------------------
CVD_A: Final = 3.9083e-3
CVD_B: Final = -5.775e-7
CVD_C: Final = -4.183e-12
PT_MIN_C: Final = -200.0
PT_MAX_C: Final = 850.0


class RtdClass(StrEnum):
    """Clases de tolerancia de IEC 60751."""

    AA = "AA"
    A = "A"
    B = "B"
    C = "C"


RTD_TOLERANCE: Final[dict[RtdClass, tuple[float, float]]] = {
    # ±(a + b·|t|) °C
    RtdClass.AA: (0.10, 0.0017),
    RtdClass.A: (0.15, 0.002),
    RtdClass.B: (0.30, 0.005),
    RtdClass.C: (0.60, 0.010),
}


def rtd_resistance(t_c: float, r0: float = 100.0) -> float:
    """Resistencia de un RTD de platino a ``t_c`` °C (Ω).

    Raises:
        ValueError: fuera de −200 a 850 °C.
    """
    if not PT_MIN_C <= t_c <= PT_MAX_C:
        raise ValueError(f"Temperatura fuera del rango de IEC 60751: {t_c} °C")
    r = 1.0 + CVD_A * t_c + CVD_B * t_c**2
    if t_c < 0:
        r += CVD_C * (t_c - 100.0) * t_c**3
    return r0 * r


def rtd_temperature(resistance: float, r0: float = 100.0) -> float:
    """Temperatura (°C) a partir de la resistencia (inversa de :func:`rtd_resistance`)."""
    ratio = resistance / r0
    if ratio >= 1.0:
        t = (-CVD_A + math.sqrt(CVD_A**2 - 4 * CVD_B * (1 - ratio))) / (2 * CVD_B)
        if t > PT_MAX_C:
            raise ValueError("Resistencia fuera de rango")
        return t
    low = rtd_resistance(PT_MIN_C, r0)
    if resistance < low:
        raise ValueError("Resistencia fuera de rango")
    return float(brentq(lambda x: rtd_resistance(x, r0) - resistance, PT_MIN_C, 0.0,
                        xtol=1e-9))


def rtd_tolerance(t_c: float, cls: RtdClass) -> float:
    """Tolerancia ± (°C) de la clase a la temperatura dada."""
    a, b = RTD_TOLERANCE[cls]
    return a + b * abs(t_c)


# --- Termopares (NIST ITS-90) ----------------------------------------------------------
TC_TYPES: Final = tuple(sorted(NIST_ITS90))
TYPE_B_INVERSE_MIN_C: Final = 50.0
"""La FEM del tipo B no es monótona por debajo de unos 42 °C."""


def tc_range(tc_type: str) -> tuple[float, float]:
    """Rango de validez de la función de referencia (°C)."""
    segs = NIST_ITS90[tc_type]
    return segs[0][0], segs[-1][1]


def tc_emf(tc_type: str, t_c: float) -> float:
    """FEM de referencia (mV) con unión fría a 0 °C.

    Raises:
        KeyError: tipo desconocido.
        ValueError: temperatura fuera de rango.
    """
    for lo, hi, coeffs, gauss in NIST_ITS90[tc_type]:
        if lo <= t_c <= hi:
            emf = 0.0
            for c in coeffs:
                emf = emf * t_c + c
            if gauss is not None:
                a0, a1, a2 = gauss
                emf += a0 * math.exp(a1 * (t_c - a2) ** 2)
            return emf
    lo, hi = tc_range(tc_type)
    raise ValueError(f"Temperatura fuera del rango del tipo {tc_type}: {lo} a {hi} °C")


def tc_temperature(tc_type: str, emf_mv: float, cold_junction_c: float = 0.0) -> float:
    """Temperatura (°C) a partir de la FEM medida y la temperatura de la unión fría."""
    target = emf_mv + tc_emf(tc_type, cold_junction_c)
    lo, hi = tc_range(tc_type)
    if tc_type == "B":
        lo = TYPE_B_INVERSE_MIN_C
    f_lo = tc_emf(tc_type, lo) - target
    f_hi = tc_emf(tc_type, hi) - target
    if f_lo * f_hi > 0:
        raise ValueError("FEM fuera del rango de la función de referencia")
    return float(brentq(lambda x: tc_emf(tc_type, x) - target, lo, hi, xtol=1e-7))


def table(func_name: str, kind: str, start: float, stop: float, step: float,
          ) -> list[tuple[float, float]]:
    """Tabla (T, valor) para RTD (``kind`` = R0 en Ω como texto) o termopar (tipo)."""
    rows: list[tuple[float, float]] = []
    n = round((stop - start) / step) + 1
    for i in range(max(n, 1)):
        t = start + i * step
        if func_name == "rtd":
            rows.append((t, rtd_resistance(t, float(kind))))
        else:
            rows.append((t, tc_emf(kind, t)))
    return rows
