"""Matriz de selección de material.

Puntúa los materiales de la biblioteca según temperatura, servicio ácido (NACE
MR0175/ISO 15156), cloruros, agentes químicos y erosión. Es una ayuda orientativa:
la decisión final corresponde al ingeniero de materiales.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from thermowell_sizer.data.database import Library, MaterialInfo

CHLORIDE_SCC_PPM = 50.0
"""Cloruros a partir de los cuales se penaliza a los austeníticos (orientativo)."""
CHLORIDE_SCC_TEMPERATURE = 333.15
"""60 °C: umbral habitual de corrosión bajo tensión por cloruros en austeníticos."""
H2S_SOUR_PARTIAL_PRESSURE = 345.0
"""0,05 psia: presión parcial de H₂S a partir de la cual aplica NACE MR0175."""
RATING_SCORE = {"A": 3, "B": 1, "C": -100, "N/D": 0}
TEMPERATURE_MARGIN = 0.9
"""Se prefiere operar por debajo del 90 % de la temperatura máxima (en K sobre 0 °C)."""


class Verdict(StrEnum):
    """Resultado de la evaluación de un material."""

    RECOMMENDED = "recommended"
    ACCEPTABLE = "acceptable"
    NOT_RECOMMENDED = "not_recommended"


@dataclass(frozen=True, slots=True)
class ServiceConditions:
    """Condiciones que influyen en la selección."""

    design_temperature: float
    min_temperature: float | None = None
    nace_service: bool = False
    h2s_partial_pressure: float = 0.0
    chlorides_ppm: float = 0.0
    agents: tuple[str, ...] = ()
    erosive: bool = False


@dataclass(frozen=True, slots=True)
class MaterialEvaluation:
    """Evaluación de un material para el servicio."""

    material: MaterialInfo
    verdict: Verdict
    score: float
    reasons: tuple[str, ...] = field(default=())
    coatings: tuple[str, ...] = field(default=())


def _celsius_margin(t: float, t_max: float) -> bool:
    zero_c = 273.15
    return (t - zero_c) <= TEMPERATURE_MARGIN * (t_max - zero_c)


def evaluate(
    library: Library, material: MaterialInfo, cond: ServiceConditions
) -> MaterialEvaluation:
    """Evalúa un material. Las razones son claves de traducción ``sel.*``."""
    reasons: list[str] = []
    score = 0.0
    blocked = False

    if cond.design_temperature > material.max_temperature:
        reasons.append("sel.temp_exceeded")
        blocked = True
    elif not _celsius_margin(cond.design_temperature, material.max_temperature):
        reasons.append("sel.temp_near_limit")
        score -= 2
    else:
        score += 2
    if (cond.min_temperature is not None and material.min_temperature is not None
            and cond.min_temperature < material.min_temperature):
        reasons.append("sel.low_temp")
        blocked = True

    sour = cond.nace_service or cond.h2s_partial_pressure >= H2S_SOUR_PARTIAL_PRESSURE
    if sour:
        if material.nace_ok:
            reasons.append("sel.nace_ok")
            score += 1
        else:
            reasons.append("sel.nace_not_listed")
            blocked = True

    if (cond.chlorides_ppm >= CHLORIDE_SCC_PPM and material.scc_chlorides
            and cond.design_temperature >= CHLORIDE_SCC_TEMPERATURE):
        reasons.append("sel.chloride_scc")
        score -= 4

    compat = library.compatibility(material.id)
    agents = list(cond.agents)
    if cond.chlorides_ppm >= CHLORIDE_SCC_PPM and "chlorides" not in agents:
        agents.append("chlorides")
    for agent in agents:
        rating = compat.get(agent, "N/D")
        score += RATING_SCORE[rating]
        if rating == "C":
            reasons.append(f"sel.agent_c:{agent}")
            blocked = True
        elif rating == "N/D":
            reasons.append(f"sel.agent_unknown:{agent}")

    if not material.fatigue_covered:
        reasons.append("sel.fatigue_not_covered")
        score -= 1

    coatings: tuple[str, ...] = ()
    if cond.erosive:
        coatings = tuple(
            c[0] for c in library.coatings()
            if c[3] == "erosion" and c[4] >= cond.design_temperature
        )
        reasons.append("sel.erosion_coating")

    if blocked:
        verdict = Verdict.NOT_RECOMMENDED
    elif score >= 3:
        verdict = Verdict.RECOMMENDED
    else:
        verdict = Verdict.ACCEPTABLE
    return MaterialEvaluation(material, verdict, score, tuple(reasons), coatings)


def recommend_materials(
    library: Library, cond: ServiceConditions
) -> list[MaterialEvaluation]:
    """Evalúa todos los materiales y los ordena del más al menos conveniente."""
    order = {Verdict.RECOMMENDED: 0, Verdict.ACCEPTABLE: 1, Verdict.NOT_RECOMMENDED: 2}
    evals = [evaluate(library, m, cond) for m in library.materials()]
    evals.sort(key=lambda e: (order[e.verdict], -e.score))
    return evals
