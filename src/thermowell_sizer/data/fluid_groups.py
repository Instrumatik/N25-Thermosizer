"""Fluidos agrupados por tipo para el selector encadenado del paso Proceso.

Un fluido que se maneja en más de un estado aparece en cada grupo que corresponda; fuera
de su grupo natural lleva un sufijo («Estado Líquido», «Estado Vapor»).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from thermowell_sizer.core.models import Phase


@dataclass(frozen=True)
class FluidType:
    """Tipo de fluido: fase que implica y fluidos que lista."""

    id: str
    name: tuple[str, str]
    phase: Phase
    fluids: tuple[tuple[str, str], ...]
    """(id de fluido, sufijo: '' | 'liquid' | 'vapor' | 'steam')."""


_LIQUIDS = ("water", "nhexane", "nheptane", "benzene", "toluene", "methanol", "ethanol",
            "acetone", "crude_api30", "diesel", "glycol50")
_LIQUEFIED = ("propane", "nbutane", "isobutane", "propylene", "ethane", "ethylene", "ammonia",
              "co2", "r134a", "methane", "nitrogen", "oxygen", "argon", "h2s", "so2")
_GASES = ("air", "natural_gas", "nitrogen", "oxygen", "hydrogen", "methane", "ethane",
          "propane", "nbutane", "isobutane", "ethylene", "propylene", "co2", "co", "ammonia",
          "h2s", "so2", "helium", "argon", "r134a")
_VAPORS = ("methanol", "ethanol", "acetone", "benzene", "toluene", "nhexane", "nheptane")
_TWO_PHASE = ("water", "propane", "nbutane", "isobutane", "propylene", "ammonia", "co2",
              "r134a", "methanol", "ethanol")

FLUID_TYPES: Final[tuple[FluidType, ...]] = (
    FluidType("liquid", ("Líquidos", "Liquids"), Phase.LIQUID,
              tuple((f, "") for f in _LIQUIDS) + tuple((f, "liquid") for f in _LIQUEFIED)),
    FluidType("gas", ("Gases", "Gases"), Phase.GAS, tuple((f, "") for f in _GASES)),
    FluidType("vapor", ("Vapores", "Vapors"), Phase.GAS, tuple((f, "vapor") for f in _VAPORS)),
    FluidType("steam", ("Vapor de agua (steam)", "Steam"), Phase.STEAM, (("water", "steam"),)),
    FluidType("two_phase", ("Bifásico", "Two-phase"), Phase.TWO_PHASE,
              tuple((f, "") for f in _TWO_PHASE)),
)
TYPES_BY_ID: Final = {ft.id: ft for ft in FLUID_TYPES}

SUFFIX: Final[dict[str, tuple[str, str]]] = {
    "liquid": ("(Estado Líquido)", "(Liquid state)"),
    "vapor": ("(Estado Vapor)", "(Vapor state)"),
}
WATER_NAMES: Final[dict[str, tuple[str, str]]] = {
    "": ("Agua", "Water"), "steam": ("Vapor de agua (steam)", "Steam"),
}


def fluid_label(fluid_id: str, base_name: str, suffix: str, es: bool) -> str:
    """Nombre a mostrar en la lista del tipo elegido."""
    if fluid_id == "water":
        pair = WATER_NAMES.get(suffix, WATER_NAMES[""])
        return pair[0] if es else pair[1]
    if suffix in SUFFIX:
        return f"{base_name} {SUFFIX[suffix][0 if es else 1]}"
    return base_name


def type_for(fluid_id: str, phase: Phase) -> str:
    """Tipo de fluido que corresponde a un tag guardado (fluido y fase)."""
    if phase is Phase.STEAM:
        return "steam"
    if phase is Phase.TWO_PHASE:
        return "two_phase"
    if phase is Phase.LIQUID:
        return "liquid"
    if fluid_id in _VAPORS and fluid_id not in _GASES:
        return "vapor"
    return "gas"


def phase_mismatch(chosen: Phase, detected: Phase) -> bool:
    """La fase calculada con P y T contradice el tipo de fluido elegido."""
    if chosen is Phase.TWO_PHASE or chosen is detected:
        return False
    vapor_like = {Phase.GAS, Phase.STEAM}
    return not (chosen in vapor_like and detected in vapor_like)
