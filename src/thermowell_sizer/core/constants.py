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
