"""Advertencias y recomendaciones de ingeniería complementarias a ASME PTC 19.3 TW.

La verificación de la norma (frecuencias, esfuerzos, presión) está en ``ptc19_3``.
Este módulo agrega criterios de buena práctica que la norma no cubre: erosión,
inmersión, posición de la punta, huelgos, tobera, sensor, prueba hidráulica y
conexión. Cada aviso indica su fuente; son orientativos y no reemplazan el
criterio del ingeniero ni la especificación del proyecto.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Final

from thermowell_sizer.core.models import (
    CalcInput,
    ConnectionType,
    MountingOrientation,
    Phase,
    SensorType,
)
from thermowell_sizer.core.ptc19_3.verify import case_velocity
from thermowell_sizer.core.units import (
    FOOT_M,
    KELVIN_OFFSET,
    POUND_KG,
    STANDARD_ATMOSPHERE_PA,
    QuantityKind,
)


class AdvisoryLevel(StrEnum):
    """Gravedad del aviso."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class Advisory:
    """Un aviso con su texto (clave del catálogo), parámetros y fuente."""

    key: str
    level: AdvisoryLevel
    reference: str
    params: dict[str, float | str] = field(default_factory=dict)
    kinds: dict[str, QuantityKind] = field(default_factory=dict)
    """Magnitud de cada parámetro numérico, para mostrarlo en las unidades elegidas."""


# --- Erosión (API RP 14E) --------------------------------------------------------------
EROSIONAL_C_DEFAULT: Final = 100.0
"""Constante empírica C de API RP 14E para servicio continuo sin sólidos (unidades US)."""
_EROSIONAL_SI: Final = FOOT_M * math.sqrt(POUND_KG / FOOT_M**3)
"""Pasa Ve = C/√ρ de (ft/s, lb/ft³) a (m/s, kg/m³): Ve = 1,22·C/√ρ."""
EROSION_WATCH_RATIO: Final = 0.7
"""V/Ve a partir del cual hay riesgo de erosión."""
REF_EROSION: Final = "API RP 14E, §2.5 (criterio orientativo; no es parte de PTC 19.3)"


def erosional_velocity(density: float, c: float = EROSIONAL_C_DEFAULT) -> float:
    """Velocidad erosiva Ve = C/√ρ de API RP 14E, m/s (ρ en kg/m³)."""
    return _EROSIONAL_SI * c / math.sqrt(density)


# --- Inmersión ------------------------------------------------------------------------
SENSITIVE_LENGTH: Final[dict[str, float]] = {
    "rtd": 0.030,
    "tc": 0.006,
    "bimetallic": 0.051,
}
"""Largo sensible típico del elemento, m (RTD encapsulada, junta de termopar, bimetálico)."""
IMMERSION_FACTOR: Final[dict[Phase, float]] = {
    Phase.LIQUID: 4.0,
    Phase.GAS: 6.0,
    Phase.STEAM: 6.0,
    Phase.TWO_PHASE: 6.0,
}
"""Diámetros de punta que debe sumergirse la parte sensible (líquido 3 a 4, gas 4 a 6)."""
REF_PRACTICE: Final = "Buena práctica de la industria (catálogos de fabricantes)"

# --- Posición de la punta --------------------------------------------------------------
TIP_WALL_FRACTION: Final = 0.9
"""Si la parte expuesta supera esta fracción del diámetro interno, la punta toca la pared."""

# --- Huelgos --------------------------------------------------------------------------
BORE_GAP_MIN: Final = 0.25e-3
"""Huelgo diametral mínimo agujero-sensor, m (dilatación y montaje)."""
BORE_GAP_MAX: Final = 1.5e-3
"""Huelgo diametral máximo recomendado, m (por encima la respuesta se vuelve lenta)."""
NOZZLE_GAP_MIN: Final = 3.0e-3
"""Huelgo diametral mínimo entre el vástago (A) y el interior de la tobera, m."""

# --- Prueba hidráulica -----------------------------------------------------------------
HYDRO_TEST_FACTOR: Final = 1.5
REF_HYDRO: Final = "ASME B31.3, §345.4.2 (presión de prueba de referencia)"

# --- Sensores -------------------------------------------------------------------------
SENSOR_RANGE_C: Final[dict[SensorType, tuple[float, float]]] = {
    SensorType.RTD_PT100: (-200.0, 600.0),
    SensorType.RTD_PT1000: (-200.0, 600.0),
    SensorType.TC_K: (-200.0, 1200.0),
    SensorType.TC_N: (-200.0, 1200.0),
    SensorType.TC_J: (-40.0, 750.0),
    SensorType.TC_T: (-200.0, 350.0),
    SensorType.TC_E: (-200.0, 900.0),
    SensorType.TC_R: (0.0, 1600.0),
    SensorType.TC_S: (0.0, 1600.0),
    SensorType.TC_B: (600.0, 1700.0),
    SensorType.BIMETALLIC: (-70.0, 500.0),
}
"""Rango de uso continuo habitual, °C (IEC 60751, IEC 60584-1/2, EN 13190)."""
CERAMIC_SHEATH_ABOVE_C: Final = 1100.0
"""Por encima de esta temperatura conviene una funda cerámica o un pozo especial."""

DIAL_RANGES_C: Final[tuple[tuple[float, float], ...]] = (
    (-70, 30), (-50, 50), (-30, 50), (-20, 60),
    (0, 60), (0, 80), (0, 100), (0, 120), (0, 160), (0, 200), (0, 250), (0, 300),
    (0, 400), (0, 500),
)
"""Escalas normalizadas de termómetros de cuadrante, °C (serie habitual EN 13190)."""
REF_DIAL: Final = "EN 13190 / ex DIN 16203: operación en el tercio central de la escala"

# --- Conexión roscada en servicios peligrosos -----------------------------------------
HAZARDOUS_FLUIDS: Final = frozenset({
    "methane", "ethane", "propane", "nbutane", "isobutane", "ethylene", "propylene",
    "hydrogen", "h2s", "co", "ammonia", "natural_gas", "nhexane", "nheptane", "benzene",
    "toluene", "methanol", "ethanol", "acetone", "so2", "crude_api30", "diesel", "oxygen",
})
"""Fluidos inflamables, tóxicos u oxidantes de la biblioteca."""
THREADED_PRESSURE_LIMIT: Final = 2.0e6
"""Presión manométrica de diseño por encima de la cual se desaconseja la conexión roscada, Pa."""
REF_CONNECTION: Final = "API RP 551 / práctica habitual de especificaciones de operadoras"


def _sensor_family(sensor: SensorType) -> str:
    if sensor is SensorType.BIMETALLIC:
        return "bimetallic"
    return "rtd" if sensor.value.startswith("rtd") else "tc"


def dial_range(t_op_c: float, t_design_c: float) -> tuple[float, float] | None:
    """Escala normalizada más chica con la operación en el tercio central y el diseño dentro."""
    for low, high in DIAL_RANGES_C:
        span = high - low
        if low + span / 3 <= t_op_c <= low + 2 * span / 3 and t_design_c <= high:
            return low, high
    return None


def advise(inp: CalcInput, *, coating_max_temperature: float | None = None,
           erosional_c: float = EROSIONAL_C_DEFAULT) -> list[Advisory]:
    """Avisos de buena práctica para la entrada (ordenados de más a menos grave)."""
    out: list[Advisory] = []
    proc = inp.process
    g = inp.thermowell.geometry
    pipe = inp.pipe
    sensor = inp.sensor
    rho = proc.properties.density

    # Erosión: V/Ve para el caso de mayor velocidad.
    v = max(case_velocity(inp, c) for c in proc.flow_cases)
    ve = erosional_velocity(rho, erosional_c)
    ratio = v / ve
    erosion_params: dict[str, float | str] = {"v": v, "ve": ve, "ratio": ratio}
    erosion_kinds = {"v": QuantityKind.VELOCITY, "ve": QuantityKind.VELOCITY}
    liquid_like = proc.phase in (Phase.LIQUID, Phase.TWO_PHASE)
    if ratio >= 1.0:
        level = (AdvisoryLevel.CRITICAL if liquid_like or proc.corrosion.solids_or_erosive
                 else AdvisoryLevel.WARNING)
        out.append(Advisory("adv.erosion", level, REF_EROSION, erosion_params, erosion_kinds))
    elif ratio >= EROSION_WATCH_RATIO:
        out.append(Advisory("adv.erosion_watch", AdvisoryLevel.WARNING, REF_EROSION,
                            erosion_params, erosion_kinds))
    if proc.corrosion.solids_or_erosive:
        out.append(Advisory("adv.solids", AdvisoryLevel.WARNING, REF_EROSION))

    # Inmersión de la parte sensible: lo que queda dentro de la tubería.
    exposed = g.L - max(g.L0, pipe.nozzle_length)
    family = _sensor_family(sensor.type)
    factor = IMMERSION_FACTOR.get(proc.phase, IMMERSION_FACTOR[Phase.GAS])
    needed = SENSITIVE_LENGTH[family] + factor * g.B
    if exposed < needed:
        out.append(Advisory("adv.immersion_short", AdvisoryLevel.WARNING, REF_PRACTICE,
                            {"exposed": exposed, "needed": needed, "factor": factor},
                            {"exposed": QuantityKind.LENGTH, "needed": QuantityKind.LENGTH}))

    # Posición de la punta en montaje perpendicular.
    if pipe.orientation is MountingOrientation.PERPENDICULAR:
        if exposed >= pipe.inner_diameter:
            out.append(Advisory("adv.tip_hits_wall", AdvisoryLevel.CRITICAL, REF_PRACTICE,
                                {"exposed": exposed, "id": pipe.inner_diameter},
                                {"exposed": QuantityKind.LENGTH, "id": QuantityKind.LENGTH}))
        elif exposed > TIP_WALL_FRACTION * pipe.inner_diameter:
            out.append(Advisory("adv.tip_near_wall", AdvisoryLevel.WARNING, REF_PRACTICE,
                                {"exposed": exposed, "id": pipe.inner_diameter},
                                {"exposed": QuantityKind.LENGTH, "id": QuantityKind.LENGTH}))
    if pipe.nozzle_length > 0 and g.L0 == 0:
        out.append(Advisory("adv.shielded_length", AdvisoryLevel.INFO,
                            "ASME PTC 19.3 TW-2016, longitud protegida L0",
                            {"nozzle": pipe.nozzle_length}, {"nozzle": QuantityKind.LENGTH}))

    # Tobera: el vástago tiene que pasar con holgura.
    if pipe.nozzle_inner_diameter is not None:
        gap = pipe.nozzle_inner_diameter - g.A
        params: dict[str, float | str] = {"nozzle_id": pipe.nozzle_inner_diameter, "a": g.A}
        kinds = {"nozzle_id": QuantityKind.DIAMETER, "a": QuantityKind.DIAMETER}
        if gap <= 0:
            out.append(Advisory("adv.nozzle_blocked", AdvisoryLevel.CRITICAL, REF_PRACTICE,
                                params, kinds))
        elif gap < NOZZLE_GAP_MIN:
            out.append(Advisory("adv.nozzle_tight", AdvisoryLevel.WARNING, REF_PRACTICE,
                                params, kinds))

    # Huelgo entre el agujero y la vaina del sensor.
    bore_gap = g.d - sensor.sheath_diameter
    bore_params: dict[str, float | str] = {"d": g.d, "sensor": sensor.sheath_diameter}
    bore_kinds = {"d": QuantityKind.DIAMETER, "sensor": QuantityKind.DIAMETER}
    if bore_gap <= 0:
        out.append(Advisory("adv.sensor_no_fit", AdvisoryLevel.CRITICAL, REF_PRACTICE,
                            bore_params, bore_kinds))
    elif bore_gap < BORE_GAP_MIN:
        out.append(Advisory("adv.sensor_tight", AdvisoryLevel.WARNING, REF_PRACTICE,
                            bore_params, bore_kinds))
    elif bore_gap > BORE_GAP_MAX:
        out.append(Advisory("adv.sensor_loose", AdvisoryLevel.WARNING, REF_PRACTICE,
                            bore_params, bore_kinds))
    if not sensor.spring_loaded and sensor.type is not SensorType.BIMETALLIC:
        out.append(Advisory("adv.spring", AdvisoryLevel.INFO, REF_PRACTICE))

    # Sensor adecuado a la temperatura.
    t_op_c = proc.operating_temperature - KELVIN_OFFSET
    t_design_c = proc.design_temperature - KELVIN_OFFSET
    low, high = SENSOR_RANGE_C[sensor.type]
    t_min_c = min(t_op_c, t_design_c)
    if t_design_c > high or t_min_c < low:
        out.append(Advisory("adv.sensor_range", AdvisoryLevel.WARNING,
                            "IEC 60751 / IEC 60584 / EN 13190",
                            {"low": low + KELVIN_OFFSET, "high": high + KELVIN_OFFSET},
                            {"low": QuantityKind.TEMPERATURE,
                             "high": QuantityKind.TEMPERATURE}))
    if t_design_c > CERAMIC_SHEATH_ABOVE_C:
        out.append(Advisory("adv.ceramic", AdvisoryLevel.INFO, REF_PRACTICE))
    if sensor.type is SensorType.BIMETALLIC:
        scale = dial_range(t_op_c, t_design_c)
        if scale is None:
            out.append(Advisory("adv.dial_none", AdvisoryLevel.WARNING, REF_DIAL))
        else:
            out.append(Advisory("adv.dial_range", AdvisoryLevel.INFO, REF_DIAL,
                                {"low": scale[0] + KELVIN_OFFSET,
                                 "high": scale[1] + KELVIN_OFFSET},
                                {"low": QuantityKind.TEMPERATURE,
                                 "high": QuantityKind.TEMPERATURE}))

    # Recubrimiento por encima de su temperatura máxima.
    if coating_max_temperature is not None and proc.design_temperature > coating_max_temperature:
        out.append(Advisory("adv.coating_temperature", AdvisoryLevel.CRITICAL, REF_PRACTICE,
                            {"limit": coating_max_temperature},
                            {"limit": QuantityKind.TEMPERATURE}))

    # Conexión roscada en servicio peligroso o de presión elevada.
    design_gauge = proc.design_pressure - STANDARD_ATMOSPHERE_PA
    if inp.thermowell.connection.type is ConnectionType.THREADED and (
            proc.fluid_id in HAZARDOUS_FLUIDS or design_gauge > THREADED_PRESSURE_LIMIT):
        out.append(Advisory("adv.threaded_service", AdvisoryLevel.WARNING, REF_CONNECTION))

    # Prueba hidráulica de referencia.
    out.append(Advisory("adv.hydro_test", AdvisoryLevel.INFO, REF_HYDRO,
                        {"p": HYDRO_TEST_FACTOR * max(design_gauge, 0.0)
                         + STANDARD_ATMOSPHERE_PA},
                        {"p": QuantityKind.PRESSURE}))

    order = {AdvisoryLevel.CRITICAL: 0, AdvisoryLevel.WARNING: 1, AdvisoryLevel.INFO: 2}
    return sorted(out, key=lambda a: order[a.level])


# --- Ensayos y documentación ----------------------------------------------------------
REF_INSPECTION: Final = "Buena práctica de compra e inspección de termopozos"


def inspection_plan(inp: CalcInput) -> list[Advisory]:
    """Ensayos, certificados y marcado sugeridos para la hoja de datos.

    Es una lista de buena práctica que se adapta a la conexión y al servicio; la
    especificación del proyecto manda.
    """
    proc = inp.process
    conn = inp.thermowell.connection
    design_gauge = max(proc.design_pressure - STANDARD_ATMOSPHERE_PA, 0.0)
    out = [Advisory("insp.hydro", AdvisoryLevel.INFO, REF_INSPECTION,
                    {"p": HYDRO_TEST_FACTOR * design_gauge + STANDARD_ATMOSPHERE_PA},
                    {"p": QuantityKind.PRESSURE})]
    if conn.type is ConnectionType.FLANGED:
        out.append(Advisory("insp.weld_flange", AdvisoryLevel.INFO, REF_INSPECTION))
    elif conn.type in (ConnectionType.WELD_IN, ConnectionType.SOCKET_WELD):
        out.append(Advisory("insp.weld_field", AdvisoryLevel.INFO, REF_INSPECTION))
    out.append(Advisory("insp.pmi", AdvisoryLevel.INFO, REF_INSPECTION))
    out.append(Advisory("insp.certificates", AdvisoryLevel.INFO, REF_INSPECTION))
    if proc.corrosion.nace_service or proc.corrosion.h2s_partial_pressure > 0:
        out.append(Advisory("insp.nace", AdvisoryLevel.INFO, REF_INSPECTION))
    out.append(Advisory("insp.dimensional", AdvisoryLevel.INFO, REF_INSPECTION))
    out.append(Advisory("insp.marking", AdvisoryLevel.INFO, REF_INSPECTION,
                        {"tag": inp.identification.tag}))
    out.append(Advisory("insp.calc_report", AdvisoryLevel.INFO, REF_INSPECTION))
    return out
