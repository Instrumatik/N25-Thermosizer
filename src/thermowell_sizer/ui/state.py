"""Estado de presentación compartido por toda la interfaz: idioma, unidades y tema."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from thermowell_sizer.core.units import STANDARD_ATMOSPHERE_PA, UnitSystem
from thermowell_sizer.i18n import Language


@dataclass(slots=True)
class DisplayState:
    """Preferencias vigentes. Se modifica en un solo lugar (la ventana principal)."""

    language: Language = Language.ES
    units: UnitSystem = UnitSystem.SI
    gauge: bool = True
    barometric: float = STANDARD_ATMOSPHERE_PA
    dark: bool = False
    licensee: str | None = None
    """Titular de la licencia instalada; ``None`` = evaluación."""
    data_folder: Path | None = None
    """Carpeta de datos del usuario (licencia, biblioteca)."""


STATE = DisplayState()
