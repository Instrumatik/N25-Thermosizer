"""Número de Scruton, velocidad de resonancia en línea y magnificación (6-8 y 6-9)."""

from __future__ import annotations

import math

from thermowell_sizer.core import constants as k


def scruton(zeta: float, rho_m: float, rho: float, d: float, b: float) -> float:
    """Número de Scruton N_Sc = π²·ζ·(ρ_m/ρ)·[1 − (d/B)²] (eq. 6-8-1)."""
    return math.pi**2 * zeta * (rho_m / rho) * (1.0 - (d / b) ** 2)


def a_of_r(re: float) -> float:
    """Polinomio a(R) = 0,0285R² − 0,0496R con R = log₁₀(Re/1300) (eq. 6-8-4)."""
    r = math.log10(re / k.RE_TRANSITION_1)
    return k.A_R_C2 * r**2 - k.A_R_C1 * r


def inline_resonance_velocity_simplified(b: float, fnc: float, ns: float) -> float:
    """Velocidad de resonancia en línea V_IR = B·f_n^c/(2N_S), m/s (eq. 6-8-5)."""
    return b * fnc / (2.0 * ns)


def inline_resonance_velocity(
    b: float, fnc: float, ns: float, re: float, velocity: float, density: float, viscosity: float
) -> float:
    """Velocidad de resonancia en línea con la correlación de Strouhal (eq. 6-8-3).

    N_S y Re se evalúan a la velocidad de diseño ``velocity``; los factores de corrección
    compensan la diferencia de N_S entre V y V_IR.
    """
    base = b * fnc / (2.0 * ns)
    if re < k.RE_TRANSITION_1:
        nu_term = k.RE_MIN_SHEDDING * viscosity / (b * density)
        return base * (1.0 - nu_term / velocity) + nu_term
    if re < k.RE_TRANSITION_2:
        return base * (1.0 - a_of_r(re) / ns * math.log10(base / velocity))
    return base


def magnification(ratio: float, zeta: float) -> float:
    """Factor de magnificación F_M = 1/(1 − r²) o F′_M = 1/(1 − r′²) (eqs. 6-9-1 y 6-9-2).

    Dentro de la banda de captura 0,8 < r < 1,2 se usa el máximo 1/(2ζ) (eq. 6-9-3).
    Fuera de la banda y con r > 1,2 se usa el valor absoluto.
    """
    if k.LOCKIN_R_LOW < ratio < k.LOCKIN_R_HIGH:
        return 1.0 / (2.0 * zeta)
    return 1.0 / abs(1.0 - ratio**2)


def max_magnification(zeta: float) -> float:
    """Magnificación en resonancia 1/(2ζ) (eq. 6-9-3 y párr. 6-8.3, paso 1)."""
    return 1.0 / (2.0 * zeta)
