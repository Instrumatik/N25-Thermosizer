"""Límites de fatiga (párr. 6-12.3)."""

from __future__ import annotations

from thermowell_sizer.core import constants as k
from thermowell_sizer.core.models import FatigueClass, MetalState


def fatigue_endurance_limit(fatigue_class: FatigueClass, state: MetalState) -> float:
    """Límite de fatiga S_f a 10¹¹ ciclos, Pa (tabla 6-12.3-1)."""
    return k.FATIGUE_LIMIT_SF[(fatigue_class.value, state.value)]


def temperature_factor(e_operating: float, e_reference: float) -> float:
    """Factor de temperatura F_T = E(T)/E_ref (eq. 6-12-6)."""
    return e_operating / e_reference


def allowable_amplitude(ft: float, fe: float, sf: float) -> float:
    """Amplitud admisible F_T·F_E·S_f, Pa (lado derecho de la eq. 6-12-5)."""
    return ft * fe * sf
