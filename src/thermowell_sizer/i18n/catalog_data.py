"""Textos de la capa de datos: selección de materiales y agentes químicos."""

from __future__ import annotations

from typing import Final

DATA_ES: Final[dict[str, str]] = {
    "sel.temp_exceeded": "La temperatura de diseño supera la máxima admitida por el material.",
    "sel.temp_near_limit": "Opera cerca de su temperatura máxima.",
    "sel.low_temp": "La temperatura mínima está por debajo de la admitida por el material.",
    "sel.nace_ok": "Admitido para servicio ácido según NACE MR0175/ISO 15156 (con dureza "
                   "controlada).",
    "sel.nace_not_listed": "No figura como apto para servicio ácido (NACE MR0175).",
    "sel.chloride_scc": "Riesgo de corrosión bajo tensión por cloruros a esta temperatura.",
    "sel.agent_c": "No recomendado frente a {agent}.",
    "sel.agent_unknown": "Sin datos de compatibilidad frente a {agent}.",
    "sel.fatigue_not_covered": "No figura en la tabla de fatiga de PTC 19.3 TW: requiere "
                               "límite de fatiga justificado.",
    "sel.erosion_coating": "Servicio erosivo: considerar recubrimiento duro.",
    "sel.verdict.recommended": "Recomendado",
    "sel.verdict.acceptable": "Aceptable",
    "sel.verdict.not_recommended": "No recomendado",
    "agent.chlorides": "cloruros",
    "agent.seawater": "agua de mar",
    "agent.h2s_wet": "H₂S húmedo",
    "agent.co2_wet": "CO₂ húmedo",
    "agent.hcl": "ácido clorhídrico",
    "agent.h2so4_dil": "ácido sulfúrico diluido",
    "agent.hno3": "ácido nítrico",
    "agent.naoh": "soda cáustica",
    "agent.nh3": "amoníaco",
    "agent.hf": "ácido fluorhídrico",
    "agent.organic_acids": "ácidos orgánicos",
}

DATA_EN: Final[dict[str, str]] = {
    "sel.temp_exceeded": "Design temperature exceeds the material maximum.",
    "sel.temp_near_limit": "Operates close to its maximum temperature.",
    "sel.low_temp": "Minimum temperature is below the material limit.",
    "sel.nace_ok": "Accepted for sour service per NACE MR0175/ISO 15156 (hardness "
                   "controlled).",
    "sel.nace_not_listed": "Not listed as suitable for sour service (NACE MR0175).",
    "sel.chloride_scc": "Chloride stress-corrosion cracking risk at this temperature.",
    "sel.agent_c": "Not recommended for {agent}.",
    "sel.agent_unknown": "No compatibility data for {agent}.",
    "sel.fatigue_not_covered": "Not in the PTC 19.3 TW fatigue table: a justified fatigue "
                               "limit is required.",
    "sel.erosion_coating": "Erosive service: consider hardfacing.",
    "sel.verdict.recommended": "Recommended",
    "sel.verdict.acceptable": "Acceptable",
    "sel.verdict.not_recommended": "Not recommended",
    "agent.chlorides": "chlorides",
    "agent.seawater": "seawater",
    "agent.h2s_wet": "wet H₂S",
    "agent.co2_wet": "wet CO₂",
    "agent.hcl": "hydrochloric acid",
    "agent.h2so4_dil": "dilute sulfuric acid",
    "agent.hno3": "nitric acid",
    "agent.naoh": "caustic soda",
    "agent.nh3": "ammonia",
    "agent.hf": "hydrofluoric acid",
    "agent.organic_acids": "organic acids",
}
