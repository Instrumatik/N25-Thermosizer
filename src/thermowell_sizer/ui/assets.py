"""Ubicación de recursos empaquetados (funciona también dentro del ejecutable)."""

from __future__ import annotations

import sys
from pathlib import Path


def asset_path(name: str) -> Path:
    """Ruta absoluta de un recurso de ``thermowell_sizer/assets``."""
    base = getattr(sys, "_MEIPASS", None)
    if base is not None:
        return Path(base) / "thermowell_sizer" / "assets" / name
    return Path(__file__).resolve().parents[1] / "assets" / name
