"""Constantes con nombre y referencia normativa.

Regla del proyecto: ningún número "mágico" en el motor. Cada constante lleva la
referencia a la norma de la que proviene. Se citan solo valores numéricos y números
de tabla o párrafo, nunca el texto de la norma.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from thermowell_sizer.core.units import INCH_M

STANDARD: Final = "ASME PTC 19.3 TW-2016"


def ref(item: str) -> str:
    """Devuelve una referencia normativa completa, p. ej. ``ref("eq. (6-4-1)")``."""
    return f"{STANDARD}, {item}"


@dataclass(frozen=True, slots=True)
class Range:
    """Intervalo cerrado; ``None`` indica que no hay límite en ese extremo."""

    minimum: float | None
    maximum: float | None

    def contains(self, value: float) -> bool:
        """Indica si ``value`` está dentro del intervalo."""
        if self.minimum is not None and value < self.minimum:
            return False
        return not (self.maximum is not None and value > self.maximum)


# --- Límites dimensionales, perfiles recto y cónico (tabla 4-1-1) ---------------------
TABLE_4_1_1: Final = ref("Table 4-1-1")
STRAIGHT_TAPERED_L: Final = Range(2.5 * INCH_M, 24.0 * INCH_M)
"""Longitud no soportada L, m. Por encima del máximo las ecuaciones siguen siendo válidas
(nota 2 de la tabla); por debajo del mínimo se requieren otros métodos (nota 1)."""
STRAIGHT_TAPERED_D_BORE: Final = Range(0.125 * INCH_M, 0.825 * INCH_M)
STRAIGHT_TAPERED_B: Final = Range(0.36 * INCH_M, 1.83 * INCH_M)
STRAIGHT_TAPERED_TAPER_RATIO: Final = Range(0.58, 1.0)
"""Relación B/A."""
STRAIGHT_TAPERED_BORE_RATIO: Final = Range(0.16, 0.71)
"""Relación d/B."""
STRAIGHT_TAPERED_ASPECT_RATIO: Final = Range(2.0, None)
"""Relación L/B."""
MIN_WALL_THICKNESS: Final = 0.12 * INCH_M
"""Espesor mínimo de pared (B − d)/2, m (tablas 4-1-1 y 4-2-1)."""
MIN_TIP_THICKNESS: Final = 0.12 * INCH_M
"""Espesor mínimo de punta t, m (tablas 4-1-1 y 4-2-1)."""

# --- Límites dimensionales, perfil escalonado (tabla 4-2-1) ---------------------------
TABLE_4_2_1: Final = ref("Table 4-2-1")
STEPPED_L: Final = Range(5.0 * INCH_M, 24.0 * INCH_M)
STEPPED_D_BORE: Final = Range(0.24 * INCH_M, 0.265 * INCH_M)
STEPPED_LENGTH_RATIO: Final = Range(0.0, 0.6)
"""Relación Ls/L."""
STEPPED_TIP_DIAMETERS: Final = (0.5 * INCH_M, 0.875 * INCH_M)
"""Diámetros de punta B admitidos por la correlación de frecuencia natural, m."""
STEPPED_STEP_RATIO_BY_TIP: Final = {
    STEPPED_TIP_DIAMETERS[0]: Range(0.5, 0.8),
    STEPPED_TIP_DIAMETERS[1]: Range(0.583, 0.875),
}
"""Relación B/A admitida según el diámetro de punta."""

# --- Tolerancias de fabricación (párr. 4-2) ------------------------------------------
PARA_4_2: Final = ref("para. 4-2")
TOLERANCE_LENGTH_REL: Final = 0.01
"""±1 % en L y Ls."""
TOLERANCE_DIAMETER_REL: Final = 0.03
"""±3 % en A, B y d."""
REFERENCE_SURFACE_FINISH_RA: Final = 0.81e-6
"""Rugosidad Ra máxima para la que valen los límites de esfuerzo de la subsección 6-12, m."""


# --- Flujo y Strouhal (subsecciones 6-3 y 6-4) ---------------------------------------
LOW_VELOCITY_LIMIT: Final = 0.64
"""Velocidad bajo la cual pueden omitirse los cálculos de vibración, m/s (párr. 6-3.6)."""
LOW_VELOCITY_MIN_A_MINUS_D: Final = 0.376 * INCH_M
"""A − d mínimo para la exención por baja velocidad, m (párr. 6-3.6)."""
LOW_VELOCITY_MAX_L: Final = 24.0 * INCH_M
"""L máximo para la exención por baja velocidad, m (párr. 6-3.6)."""
LOW_VELOCITY_MIN_B: Final = 0.5 * INCH_M
"""B mínimo para la exención por baja velocidad, m (párr. 6-3.6)."""
LOW_VELOCITY_MIN_S: Final = 69.0e6
"""S mínimo para la exención por baja velocidad, Pa (párr. 6-3.6)."""
LOW_VELOCITY_MIN_SF: Final = 21.0e6
"""Sf mínimo para la exención por baja velocidad, Pa (párr. 6-3.6)."""

RE_MIN_SHEDDING: Final = 22.0
"""Re mínimo de la correlación de Strouhal (eq. 6-4-2); debajo no hay desprendimiento."""
RE_TRANSITION_1: Final = 1300.0
"""Re₀, primer cambio de rama de la correlación de Strouhal (eqs. 6-4-2 y 6-8-4)."""
RE_TRANSITION_2: Final = 5.0e5
"""Segundo cambio de rama de la correlación de Strouhal (eq. 6-4-2)."""
RE_MAX_CORRELATION: Final = 5.0e7
"""Re máximo de la correlación de Strouhal (eq. 6-4-2)."""
STROUHAL_HIGH_RE: Final = 0.22
"""N_S para Re alto y aproximación conservadora (eqs. 6-4-2 y 6-4-4)."""
STROUHAL_MID_C0: Final = 0.213
STROUHAL_MID_C2: Final = 0.0248
STROUHAL_MID_C3: Final = 0.0095
"""Coeficientes de la rama intermedia de la eq. (6-4-2)."""
A_R_C2: Final = 0.0285
A_R_C1: Final = 0.0496
"""Coeficientes del polinomio a(R) de la eq. (6-8-4)."""

DRAG_COEFF_STEADY: Final = 1.4
"""C_D, arrastre estacionario (eq. 6-4-5)."""
DRAG_COEFF_OSC: Final = 0.1
"""C_d, arrastre oscilante en línea (eq. 6-4-5)."""
LIFT_COEFF_OSC: Final = 1.0
"""C_l, sustentación oscilante transversal (eq. 6-4-5)."""

# --- Frecuencia natural (subsecciones 6-5 a 6-7) -------------------------------------
CANTILEVER_EIGENVALUE: Final = 1.875
"""Primer autovalor de la viga en voladizo, λ₁L ≈ 1,875 (eq. 6-5-1)."""
DEFAULT_SENSOR_DENSITY: Final = 2700.0
"""ρs por defecto para sensores con aislamiento mineral, kg/m³ (párr. 6-5.3, paso 5)."""
HF_C0: Final = 0.99
HF_C1: Final = 1.1
HF_EXP_C: Final = 3.0
HF_EXP_D: Final = 0.8
"""Coeficientes de la correlación Hf para vástago recto o cónico (eq. 6-5-2)."""


@dataclass(frozen=True, slots=True)
class StepShankCoefficients:
    """Coeficientes c₁…c₁₀ de la eq. (6-5-3), tabla 6-5.3-1."""

    c: tuple[float, float, float, float, float, float, float, float, float, float]


TABLE_6_5_3_1: Final = ref("Table 6-5.3-1")
STEP_SHANK_COEFFS: Final = {
    STEPPED_TIP_DIAMETERS[1]: StepShankCoefficients(
        (1.410, -0.949, -0.091, 1.132, -1.714, 0.865, 0.861, 1.000, 9.275, -7.466)
    ),
    STEPPED_TIP_DIAMETERS[0]: StepShankCoefficients(
        (1.407, -0.839, -0.022, 1.022, -2.228, 1.594, 1.313, 0.362, 8.299, -5.376)
    ),
}
"""Coeficientes por diámetro de punta B (22,23 mm y 12,7 mm); no se permite interpolar."""

HC_SEMI_INFINITE: Final = 0.61
"""Coeficiente de Hc para base semi-infinita (eq. 6-6-5)."""
HC_FILLET: Final = 1.5
"""Coeficiente del radio de acuerdo en Hc (eqs. 6-6-2 y 6-6-5)."""
HC_THREADED: Final = 0.9
"""Coeficiente de Hc para conexión roscada (eq. 6-7-1)."""
KM_BASE: Final = 0.787
"""Divisor de la rigidez rotacional de base semi-infinita (eq. 6-6-4)."""

# --- Límites de frecuencia y magnificación (subsecciones 6-8 y 6-9) ----------------------
DEFAULT_DAMPING: Final = 0.0005
"""ζ, amortiguamiento intrínseco conservador (párr. 6-8.2)."""
SCRUTON_INLINE_SUPPRESSED: Final = 2.5
"""N_Sc por encima del cual se suprime la resonancia en línea si Re < 10⁵ (párr. 6-8.2)."""
SCRUTON_ALL_SUPPRESSED: Final = 64.0
"""N_Sc por encima del cual se suprimen ambas resonancias si Re < 10⁵ (párr. 6-8.2)."""
RE_LOW_DENSITY_LIMIT: Final = 1.0e5
"""Re máximo para aplicar los criterios de gases de baja densidad (párr. 6-8.2)."""
RATIO_TRANSVERSE_LIMIT: Final = 0.8
"""fs < 0,8 f_n^c (eqs. 6-8-2 y 6-8-6)."""
RATIO_INLINE_LIMIT: Final = 0.4
"""fs < 0,4 f_n^c (eqs. 6-8-7 y 6-8-8)."""
RATIO_LOCKIN_UPPER: Final = 0.6
"""Límite superior de la banda de captura en línea, 0,6 f_n^c (eq. 6-8-9, párr. 6-8.5)."""
LOCKIN_R_LOW: Final = 0.8
LOCKIN_R_HIGH: Final = 1.2
"""Banda de captura en términos de r o r′ (párr. 6-9.1)."""
INLINE_PASSAGE_MAX_CYCLES: Final = 1.0e11
"""Ciclos máximos al atravesar la resonancia en línea (párr. 6-8.5 c)."""
SUPERCRITICAL_MAX_DENSITY: Final = 1.0
"""Densidad bajo la cual se menciona la operación supercrítica, kg/m³ (párr. 6-12.5)."""

# --- Esfuerzos y fatiga (subsecciones 6-10 a 6-12) -----------------------------------
VON_MISES_FACTOR: Final = 1.5
"""Límite de von Mises 1,5·S (eq. 6-12-2)."""
KT_DEFAULT: Final = 2.2
"""Kt sin datos del radio de acuerdo, o con A/b ≥ 33 (párr. 6-12.3 a, eq. 6-12-4)."""
KT_THREADED_MIN: Final = 2.3
"""Kt mínimo para conexiones roscadas (párr. 6-12.3 b)."""
KT_C0: Final = 1.1
KT_C1: Final = 0.033
KT_RATIO_LIMIT: Final = 33.0
"""Coeficientes y límite de A/b de la eq. (6-12-4)."""

TABLE_6_12_3_1: Final = ref("Table 6-12.3-1")
FATIGUE_LIMIT_SF: Final = {
    ("A", "as_welded"): 20.7e6,
    ("A", "welded_machined"): 32.4e6,
    ("A", "no_welds"): 48.3e6,
    ("B", "as_welded"): 37.2e6,
    ("B", "welded_machined"): 62.8e6,
    ("B", "no_welds"): 93.8e6,
}
"""Sf por clase de material y estado del metal en la raíz, Pa (10¹¹ ciclos)."""
E_REF_CLASS_A: Final = 202.0e9
E_REF_CLASS_A_LOW_CR: Final = 213.0e9
E_REF_CLASS_B: Final = 195.0e9
E_REF_CLASS_B_NI_CU: Final = 179.0e9
"""Módulo de referencia E_ref para F_T (párr. 6-12.3), Pa."""
HIGH_TEMPERATURE_FE_WARNING: Final = 427.0 + 273.15
"""Sobre 427 °C puede requerirse F_E < 1 (párr. 6-12.3), K."""

# --- Presión externa (subsección 6-13) -----------------------------------------------
PC_FACTOR: Final = 0.66
PC_C1: Final = 2.167
PC_C2: Final = 0.0833
"""Coeficientes de la eq. (6-13-1)."""
PT_DIVISOR: Final = 0.13
"""Divisor de la eq. (6-13-2)."""
SIMPLIFIED_PRESSURE_LIMIT: Final = 103.0e6
"""Sobre 103 MPa se requieren otros códigos (párr. 6-13, paso 1), Pa."""

# --- Presentación de márgenes --------------------------------------------------------
DEFAULT_AMBER_MARGIN_PCT: Final = 10.0
"""Margen bajo el cual un criterio aprobado se muestra en ámbar (criterio del programa)."""
