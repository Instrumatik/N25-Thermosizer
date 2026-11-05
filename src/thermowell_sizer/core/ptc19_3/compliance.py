"""Flexibilidad del soporte H_c y frecuencia natural instalada (subsecciones 6-6 y 6-7)."""

from __future__ import annotations

import math

from thermowell_sizer.core import constants as k


def support_stiffness_semi_infinite(e: float, diameter: float) -> float:
    """Rigidez rotacional de una base semi-infinita K_M = (E/0,787)(D/2)³, N·m/rad (eq. 6-6-4)."""
    return e / k.KM_BASE * (diameter / 2.0) ** 3


def hc_general(km: float, e: float, a: float, d: float, length: float, fillet: float) -> float:
    """H_c general a partir de la rigidez del soporte K_M (eq. 6-6-2)."""
    fillet_term = (1.0 + k.HC_FILLET * fillet / a) ** 2
    return 1.0 - (e / km) * math.pi * (a**4 - d**4) / (32.0 * length * fillet_term)


def hc_semi_infinite(a: float, length: float, fillet: float) -> float:
    """H_c para soporte en base semi-infinita (eq. 6-6-5): bridado, soldado, socket weld."""
    return 1.0 - k.HC_SEMI_INFINITE * (a / length) / (1.0 + k.HC_FILLET * fillet / a) ** 2


def hc_threaded(a: float, length: float) -> float:
    """H_c para conexión roscada (eq. 6-7-1)."""
    return 1.0 - k.HC_THREADED * a / length


def installed_frequency(hc: float, fn: float) -> float:
    """Frecuencia natural instalada f_n^c = H_c·f_n, Hz (eq. 6-6-1)."""
    return hc * fn
