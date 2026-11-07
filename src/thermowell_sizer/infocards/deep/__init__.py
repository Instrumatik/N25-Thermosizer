"""Contenido de profundidad de las fichas (revisión 1.5).

Cada módulo define ``DEEP``: secciones nuevas o reforzadas de fichas existentes, y ``NEW``:
fichas completas que no tienen campo en el editor (glosario y normas). El texto es una
explicación propia de ingeniería; de las normas solo se citan número de párrafo y un resumen.

Formato del texto: párrafos separados por línea en blanco; líneas que empiezan con «- »
forman una lista y las que empiezan con «1. » una lista numerada.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from thermowell_sizer.infocards.deep import (
    d_criteria,
    d_glossary,
    d_misc,
    d_pipe,
    d_process,
    d_results,
    d_standards,
    d_well,
)

_MODULES = (d_process, d_pipe, d_well, d_results, d_criteria, d_misc, d_glossary, d_standards)

GLOSSARY_CARD: dict[str, str] = {
    "bore": "f.d", "damping": "opt.damping", "lock_in": "g.lock_in",
    "standard_flow": "g.standard_flow", "velocity_collar": "g.velocity_collar",
    "time_constant": "g.time_constant", "vortex_shedding": "r.fs", "tip_diameter": "f.B",
    "root_diameter": "f.A", "immersion_error": "g.immersion_error",
    "allowable_stress": "f.S_manual", "von_mises": "r.von_mises",
    "stress_concentration": "g.stress_concentration", "magnification": "g.magnification",
    "compliance": "r.hc", "wake_frequency": "r.fs", "natural_frequency": "r.fn",
    "installed_frequency": "r.fnc", "lag": "f.T_lag", "insertion": "f.U",
    "unsupported_length": "f.L", "fatigue_limit": "g.fatigue_limit", "added_mass": "g.added_mass",
    "reynolds": "r.reynolds", "scruton": "r.scruton", "strouhal": "r.strouhal", "pmi": "g.pmi",
    "tapered": "profile.tapered", "stepped": "profile.stepped", "support_plane": "g.support_plane",
    "hydro_test": "g.hydro_test", "pt100": "g.pt100", "fillet": "f.b", "rating": "f.rating",
    "inline_resonance": "g.inline_resonance", "transverse_resonance": "g.transverse_resonance",
    "nace": "f.nace", "corrosion_allowance": "f.ca", "thermocouple": "g.thermocouple",
    "skin_point": "g.skin_point", "thermowell": "g.thermowell", "van_stone": "conn.van_stone",
    "flanged_well": "conn.flanged", "weld_in_well": "conn.weld_in",
    "threaded_well": "conn.threaded", "socket_weld_well": "conn.socket_weld",
    "bimetallic": "g.bimetallic", "ceramic_sheath": "g.ceramic_sheath",
    "erosional_velocity": "r.ve",
}
"""Término del glosario → ficha completa que lo explica."""

STANDARD_CARD: dict[str, str] = {
    "ASME-PTC-19.3-TW": "std.ptc193", "ASME-B16.5": "std.b165", "ASME-B40.9": "std.b40",
    "DIN-43772": "std.din43772", "ISA-TR20": "std.isatr20", "NACE-MR0175": "std.nace",
    "IEC-60751": "std.iec60751", "IEC-60584": "std.iec60584",
}
"""Norma de la biblioteca → ficha completa."""


def apply(cards: dict[str, Any], card_cls: type) -> None:
    """Agrega las fichas nuevas y completa las existentes con las secciones de profundidad."""
    for mod in _MODULES:
        for cid, fields in getattr(mod, "NEW", {}).items():
            cards[cid] = card_cls(cid, **fields)
    for mod in _MODULES:
        for cid, fields in getattr(mod, "DEEP", {}).items():
            if cid not in cards:
                raise KeyError(f"Ficha de profundidad sin ficha base: {cid}")
            cards[cid] = replace(cards[cid], **fields)
