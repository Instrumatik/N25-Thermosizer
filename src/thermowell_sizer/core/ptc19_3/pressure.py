"""Presión externa admisible (subsección 6-13)."""

from __future__ import annotations

from thermowell_sizer.core import constants as k


def shank_pressure_rating(s: float, b: float, d: float) -> float:
    """Presión externa admisible del vástago (método simplificado), P_c, Pa (eq. 6-13-1)."""
    return k.PC_FACTOR * s * (k.PC_C1 / (2.0 * b / (b - d)) - k.PC_C2)


def tip_pressure_rating(s: float, t: float, d: float) -> float:
    """Presión externa admisible de la punta P_t = (S/0,13)(t/d)², Pa (eq. 6-13-2)."""
    return s / k.PT_DIVISOR * (t / d) ** 2


def pressure_rating(pc: float, pt: float, pf: float | None = None) -> float:
    """Presión externa nominal P_r: mínimo de P_c, P_t y P_f si hay brida (párr. 6-13, paso 3)."""
    candidates = [pc, pt] if pf is None else [pc, pt, pf]
    return min(candidates)
