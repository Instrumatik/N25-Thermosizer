"""Resultados calculados por caso, estado ASME por tema, datos de entrada y convención de largos.

Reúne en tablas simples lo que la planilla de referencia muestra en sus bloques «CALCULATED
RESULTS», «ASME STATUS» e «INPUT PARAMETER», a partir de una :class:`Evaluation` ya hecha.
Los textos vienen en español e inglés; el formato numérico lo pone quien muestra la tabla.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

from thermowell_sizer.core.advisories import (
    EROSION_WATCH_RATIO,
    AdvisoryLevel,
    erosional_velocity,
)
from thermowell_sizer.core.models import CheckResult, CheckStatus, FlowBasis
from thermowell_sizer.core.ptc19_3.verify import CaseSummary
from thermowell_sizer.core.units import QuantityKind as Q
from thermowell_sizer.services import Evaluation

_ORDER: Final = {CheckStatus.FAIL: 0, CheckStatus.WARNING: 1, CheckStatus.PASS: 2,
                 CheckStatus.NOT_APPLICABLE: 3}

LABELS: Final[dict[str, tuple[str, str]]] = {
    # resultados calculados
    "q_actual": ("Caudal volumétrico real", "Actual volumetric flow"),
    "velocity": ("Velocidad del fluido", "Process fluid velocity"),
    "ve": ("Velocidad erosional (API RP 14E)", "Erosional velocity (API RP 14E)"),
    "v_ve": ("Relación V/Ve", "Velocity ratio V/Ve"),
    "reynolds": ("Número de Reynolds", "Reynolds number"),
    "strouhal": ("Número de Strouhal", "Strouhal number"),
    "fs": ("Frecuencia de estela", "Wake frequency"),
    "fnc": ("Frecuencia natural instalada", "Installed natural frequency"),
    "ratio": ("Relación de frecuencias", "Frequency ratio"),
    "steady": ("Esfuerzo estacionario (arrastre + presión axial)",
               "Steady-state stress (drag + axial pressure)"),
    "dynamic": ("Esfuerzo dinámico (pico oscilante)", "Dynamic stress (peak oscillating)"),
    "von_mises": ("Esfuerzo de von Mises (estacionario)", "Von Mises stress (steady)"),
    # estado ASME
    "topic.erosion": ("Evaluación de erosión", "Erosion evaluation"),
    "topic.frequency": ("Frecuencia de estela", "Wake frequency"),
    "topic.stress": ("Esfuerzos", "Stresses"),
    "topic.pressure": ("Presión y rating", "Pressure and rating"),
    "topic.overall": ("Estado ASME global", "Overall ASME status"),
    "v.no_erosion": ("No erosivo", "Non-erosive"),
    "v.erosion_watch": ("Vigilar", "Monitor"),
    "v.erosive": ("Erosivo", "Erosive"),
    "v.pass": ("Cumple", "Pass"),
    "v.pass_low_margin": ("Cumple (margen bajo)", "Pass (low margin)"),
    "v.fail": ("No cumple", "Fail"),
    "v.resonance": ("Riesgo de resonancia", "Resonance risk"),
    "v.no_shedding": ("No aplica (sin desprendimiento de vórtices)",
                      "Not applicable (no vortex shedding)"),
    "v.review": ("Requiere revisión de ingeniería", "Requires engineering review"),
    "v.na": ("No aplica", "Not applicable"),
    # datos de entrada
    "in.flow": ("Caudal", "Flow rate"),
    "in.pressure": ("Presión de operación", "Operating pressure"),
    "in.temperature": ("Temperatura de operación", "Operating temperature"),
    "in.density": ("Densidad del fluido", "Fluid density"),
    "in.viscosity": ("Viscosidad dinámica", "Dynamic viscosity"),
    "in.pipe_id": ("Diámetro interno de la tubería", "Pipe ID"),
    "in.insertion": ("Inserción desde la superficie externa de la tubería",
                     "Insertion length from the pipe outer surface"),
    "in.unsupported": ("Longitud no soportada L (= U desde la cara de la brida)",
                       "Unsupported length L (= U from the flange face)"),
    "in.hs": ("Hs, altura de la brida de montaje", "Hs, mounting flange height"),
    "in.nozzle_id": ("Diámetro interno de la conexión de montaje",
                     "Mounting connection ID"),
    "in.root": ("Diámetro de raíz A", "Root diameter A"),
    "in.tip": ("Diámetro de punta B", "Tip diameter B"),
    "in.bore": ("Diámetro del agujero d", "Bore diameter d"),
    "in.E": ("Módulo de elasticidad E", "Elastic modulus E"),
    "in.S": ("Esfuerzo admisible S", "Allowable stress S"),
    "src.entered": ("Cargado", "Entered"),
    "src.calculated": ("Calculado", "Calculated"),
    "src.coolprop": ("Calculado (CoolProp)", "Calculated (CoolProp)"),
    "src.schedule": ("Calculado (NPS y schedule)", "Calculated (NPS and schedule)"),
    "src.library": ("Biblioteca de materiales", "Material library"),
    "src.manual": ("Cargado a mano", "Entered by hand"),
    "src.missing": ("No cargado", "Not entered"),
    "src.auto": ("Automático (selección del programa)", "Automatic (program selection)"),
    "use.asme": ("Sí", "Yes"),
    "use.advice": ("Solo recomendaciones", "Recommendations only"),
    "use.info": ("Informativo", "Informative"),
    # convención de largos
    "conv.hs": ("Hs, de la superficie externa de la tubería a la cara de la brida",
                "Hs, from the pipe outer surface to the flange face"),
    "conv.wall": ("Espesor de pared de la tubería", "Pipe wall thickness"),
    "conv.immersion": ("Inmersión desde la pared interna", "Immersion from the inner wall"),
    "conv.insertion": ("Inserción desde la superficie externa (planilla)",
                       "Insertion from the outer surface (spreadsheet)"),
    "conv.L": ("L = U, desde la cara de la brida (programa) = Hs + inserción (planilla)",
               "L = U, from the flange face (program) = Hs + insertion (spreadsheet)"),
}


def label(key: str, es: bool = True) -> str:
    """Texto de una etiqueta de este módulo."""
    pair = LABELS.get(key)
    return key if pair is None else pair[0 if es else 1]


@dataclass(frozen=True, slots=True)
class ResultRow:
    """Una fila de «Resultados calculados»."""

    key: str
    symbol: str
    value: float | None
    kind: Q
    limit: float | None = None
    limit_prefix: str = ""
    status: CheckStatus | None = None


@dataclass(frozen=True, slots=True)
class CaseResults:
    """Resultados calculados de un caso de flujo."""

    scope: str
    rows: tuple[ResultRow, ...]


@dataclass(frozen=True, slots=True)
class StatusLine:
    """Veredicto de un tema del «Estado ASME»."""

    key: str
    verdict: str
    status: CheckStatus
    ratio: float | None = None
    """V/Ve más alto (solo para la erosión)."""


@dataclass(frozen=True, slots=True)
class InputRow:
    """Una fila de «Datos de entrada»."""

    key: str
    value: float | str | None
    kind: Q | None
    source: str
    use: str


def _worst(checks: list[CheckResult]) -> CheckResult | None:
    applicable = [c for c in checks if c.status is not CheckStatus.NOT_APPLICABLE]
    pool = applicable or checks
    return min(pool, key=lambda c: (_ORDER[c.status], c.margin_pct)) if pool else None


def _trace_max(ev: Evaluation, prefix: str, scope: str) -> float | None:
    assert ev.result is not None
    vals = [e.value for e in ev.result.trace
            if e.scope == scope and e.symbol.startswith(prefix) and "_IR" not in e.symbol]
    return max(vals) if vals else None


def erosion_ratio(ev: Evaluation, velocity: float) -> tuple[float, float]:
    """Velocidad erosional y relación V/Ve."""
    rho = ev.input.process.properties.density
    ve = erosional_velocity(rho)
    return ve, velocity / ve if ve else 0.0


def _erosion_status(ratio: float) -> CheckStatus:
    if ratio >= 1.0:
        return CheckStatus.FAIL
    return CheckStatus.WARNING if ratio >= EROSION_WATCH_RATIO else CheckStatus.PASS


def calculated_results(ev: Evaluation) -> list[CaseResults]:
    """Resultados calculados de cada caso, con su límite y estado cuando lo tienen."""
    if ev.result is None:
        return []
    pid = ev.input.pipe.inner_diameter
    area = math.pi * pid**2 / 4 if pid else None
    out: list[CaseResults] = []
    for case in ev.result.cases:
        out.append(CaseResults(case.scope, tuple(_case_rows(ev, case, area))))
    return out


def _case_rows(ev: Evaluation, c: CaseSummary, area: float | None) -> list[ResultRow]:
    assert ev.result is not None
    checks = [k for k in ev.result.checks if k.flow_case == c.scope]
    ve, ratio_e = erosion_ratio(ev, c.velocity)
    rows = [
        ResultRow("q_actual", "Q", c.velocity * area if area else None, Q.VOLUME_FLOW),
        ResultRow("velocity", "V", c.velocity, Q.VELOCITY),
        ResultRow("ve", "V_e", ve, Q.VELOCITY),
        ResultRow("v_ve", "V/V_e", ratio_e, Q.DIMENSIONLESS, 1.0, "<",
                  _erosion_status(ratio_e)),
        ResultRow("reynolds", "Re", c.reynolds, Q.DIMENSIONLESS),
        ResultRow("strouhal", "N_S", c.strouhal, Q.DIMENSIONLESS),
        ResultRow("fs", "f_s", c.fs, Q.FREQUENCY),
        ResultRow("fnc", "f_n,c", c.fnc, Q.FREQUENCY),
    ]
    freq = _worst([k for k in checks if k.criterion_id == "frequency_limit"])
    ratio = c.fs / c.fnc if c.fnc else None
    if freq is not None and freq.status is not CheckStatus.NOT_APPLICABLE and c.fnc:
        rows.append(ResultRow("ratio", "f_s/f_n,c", ratio, Q.DIMENSIONLESS,
                              freq.limit / c.fnc, "<", freq.status))
    else:
        rows.append(ResultRow("ratio", "f_s/f_n,c", ratio, Q.DIMENSIONLESS,
                              status=None if freq is None else freq.status))
    rows.append(ResultRow("steady", "S_max", _trace_max(ev, "S_max_", c.scope), Q.STRESS))
    dyn = _worst([k for k in checks if k.criterion_id.startswith("dynamic_stress_")])
    rows.append(ResultRow("dynamic", "S_o", dyn.value if dyn else None, Q.STRESS,
                          dyn.limit if dyn else None, "≤", dyn.status if dyn else None))
    vm = _worst([k for k in checks if k.criterion_id.startswith("steady_stress_")])
    rows.append(ResultRow("von_mises", "S_vm", vm.value if vm else None, Q.STRESS,
                          vm.limit if vm else None, "≤", vm.status if vm else None))
    return rows


def _verdict(status: CheckStatus) -> str:
    return {CheckStatus.PASS: "v.pass", CheckStatus.WARNING: "v.pass_low_margin",
            CheckStatus.FAIL: "v.fail", CheckStatus.NOT_APPLICABLE: "v.na"}[status]


def asme_status(ev: Evaluation) -> list[StatusLine]:
    """Veredicto por tema: erosión, frecuencia de estela, esfuerzos, presión y global."""
    if ev.result is None:
        return []
    res = ev.result
    lines: list[StatusLine] = []
    # erosión (orientativa, API RP 14E)
    ratios = [erosion_ratio(ev, c.velocity)[1] for c in res.cases]
    worst_ratio = max(ratios, default=0.0)
    e_status = _erosion_status(worst_ratio)
    e_key = {CheckStatus.PASS: "v.no_erosion", CheckStatus.WARNING: "v.erosion_watch",
             CheckStatus.FAIL: "v.erosive"}[e_status]
    lines.append(StatusLine("topic.erosion", e_key, e_status, worst_ratio))
    # frecuencia de estela
    freq = [c for c in res.checks
            if c.criterion_id in ("frequency_limit", "inline_lockin_dwell")]
    fw = _worst(freq)
    if fw is None or fw.status is CheckStatus.NOT_APPLICABLE:
        lines.append(StatusLine("topic.frequency", "v.no_shedding",
                                CheckStatus.NOT_APPLICABLE))
    elif fw.status is CheckStatus.PASS:
        lines.append(StatusLine("topic.frequency", "v.pass", CheckStatus.PASS))
    else:
        lines.append(StatusLine("topic.frequency", "v.resonance", fw.status))
    # esfuerzos
    sw = _worst([c for c in res.checks
                 if c.criterion_id.startswith(("steady_stress_", "dynamic_stress_"))
                 or c.criterion_id == "fatigue_data"])
    if sw is not None:
        lines.append(StatusLine("topic.stress", _verdict(sw.status), sw.status))
    # presión, rating y temperatura del material
    pw = _worst([c for c in res.checks if c.criterion_id in (
        "pressure_rating", "flange_rating", "material_temperature")])
    if pw is not None:
        lines.append(StatusLine("topic.pressure", _verdict(pw.status), pw.status))
    # global
    critical = any(a.level is AdvisoryLevel.CRITICAL for a in ev.advisories)
    statuses = [ln.status for ln in lines if ln.key != "topic.erosion"]
    if res.status is CheckStatus.FAIL or CheckStatus.FAIL in statuses:
        overall = StatusLine("topic.overall", "v.fail", CheckStatus.FAIL)
    elif (res.status is CheckStatus.WARNING or CheckStatus.WARNING in statuses
          or e_status is not CheckStatus.PASS or critical):
        overall = StatusLine("topic.overall", "v.review", CheckStatus.WARNING)
    else:
        overall = StatusLine("topic.overall", "v.pass", CheckStatus.PASS)
    lines.append(overall)
    return lines


def input_rows(ev: Evaluation, auto_properties: bool) -> list[InputRow]:
    """Los 15 datos de entrada de la planilla, con su origen y si entran en el cálculo ASME."""
    inp = ev.input
    proc, pipe, g = inp.process, inp.pipe, inp.thermowell.geometry
    case = next((c for c in proc.flow_cases if c.label == "normal"), proc.flow_cases[0]
                if proc.flow_cases else None)
    flow: float | None = None
    flow_kind = Q.VELOCITY
    if case is not None:
        flow_kind, flow = {
            FlowBasis.VELOCITY: (Q.VELOCITY, case.velocity),
            FlowBasis.MASS_FLOW: (Q.MASS_FLOW, case.mass_flow),
            FlowBasis.VOLUME_FLOW: (Q.VOLUME_FLOW, case.volume_flow),
            FlowBasis.STANDARD_VOLUME_FLOW: (Q.STANDARD_VOLUME_FLOW,
                                             case.standard_volume_flow),
        }[case.basis]
    prop_src = "src.coolprop" if auto_properties else "src.entered"
    pipe_src = "src.schedule" if pipe.schedule and pipe.nominal_size else "src.entered"
    wall = pipe.wall_thickness or 0.0
    hs = pipe.mount_height if pipe.mount_height is not None else max(
        pipe.nozzle_length - wall, 0.0)
    u = g.U or g.L
    ref = inp.thermowell.material
    mat = ev.material
    e_src = "src.manual" if ref.elastic_modulus is not None else "src.library"
    s_src = "src.manual" if ref.allowable_stress is not None else "src.library"
    auto = set(ev.auto_blocks)
    if "material" in auto:
        e_src = s_src = "src.auto"
    geo_src = "src.auto" if "geometry" in auto else "src.entered"
    return [
        InputRow("in.flow", flow, flow_kind, "src.entered", "use.asme"),
        InputRow("in.pressure", proc.operating_pressure, Q.PRESSURE, "src.entered",
                 "use.asme"),
        InputRow("in.temperature", proc.operating_temperature, Q.TEMPERATURE,
                 "src.entered", "use.asme"),
        InputRow("in.density", proc.properties.density, Q.DENSITY, prop_src, "use.asme"),
        InputRow("in.viscosity", proc.properties.dynamic_viscosity, Q.DYNAMIC_VISCOSITY,
                 prop_src, "use.asme"),
        InputRow("in.pipe_id", pipe.inner_diameter, Q.DIAMETER, pipe_src, "use.asme"),
        InputRow("in.insertion", max(u - hs, 0.0), Q.LENGTH, "src.calculated", "use.info"),
        InputRow("in.unsupported", u, Q.LENGTH, geo_src, "use.asme"),
        InputRow("in.hs", hs, Q.LENGTH,
                 "src.entered" if pipe.mount_height is not None else "src.calculated",
                 "use.advice"),
        InputRow("in.nozzle_id", pipe.nozzle_inner_diameter, Q.DIAMETER,
                 "src.entered" if pipe.nozzle_inner_diameter else "src.missing",
                 "use.advice"),
        InputRow("in.root", g.A, Q.DIAMETER, geo_src, "use.asme"),
        InputRow("in.tip", g.B, Q.DIAMETER, geo_src, "use.asme"),
        InputRow("in.bore", g.d, Q.DIAMETER, geo_src, "use.asme"),
        InputRow("in.E", mat.elastic_modulus if mat else ref.elastic_modulus,
                 Q.ELASTIC_MODULUS, e_src, "use.asme"),
        InputRow("in.S", mat.allowable_stress if mat else ref.allowable_stress, Q.STRESS,
                 s_src, "use.asme"),
    ]


def length_convention(ev: Evaluation) -> list[tuple[str, float]]:
    """Equivalencia entre la convención de la planilla (Hs + inserción) y la del programa."""
    pipe, g = ev.input.pipe, ev.input.thermowell.geometry
    wall = pipe.wall_thickness or 0.0
    hs = pipe.mount_height if pipe.mount_height is not None else max(
        pipe.nozzle_length - wall, 0.0)
    u = g.U or g.L
    return [
        ("conv.hs", hs),
        ("conv.wall", wall),
        ("conv.immersion", max(u - hs - wall, 0.0)),
        ("conv.insertion", max(u - hs, 0.0)),
        ("conv.L", u),
    ]


_DECIMALS: Final = {"reynolds": 0, "strouhal": 3, "v_ve": 2, "ratio": 3}


def value_text(key: str, value: float | str | None, kind: Q | None,
               qfmt: Callable[[float, Q], str], nfmt: Callable[[float, int], str]) -> str:
    """Valor con su unidad (o adimensional con los decimales de la fila)."""
    if value is None:
        return "—"
    if isinstance(value, str):
        return value
    if kind is None or kind is Q.DIMENSIONLESS:
        return nfmt(value, _DECIMALS.get(key, 3))
    return qfmt(value, kind)


def limit_text(row: ResultRow, qfmt: Callable[[float, Q], str],
               nfmt: Callable[[float, int], str]) -> str:
    """Límite con el signo de comparación, o «—» si la fila no tiene límite."""
    if row.limit is None:
        return "—"
    return f"{row.limit_prefix} {value_text(row.key, row.limit, row.kind, qfmt, nfmt)}"


@dataclass(frozen=True, slots=True)
class AutoRow:
    """Una fila de «Selección automática y justificación»."""

    block: str
    item: str
    value: str
    reason: str
    alternatives: str


def auto_rows(ev: Evaluation, es: bool, qfmt: Callable[[float, Q], str]) -> list[AutoRow]:
    """Decisiones de la selección automática, listas para tablas (pantalla y reportes)."""
    from thermowell_sizer.autodesign import BLOCK_NAMES
    from thermowell_sizer.ui.text import UI  # textos compartidos con la interfaz

    lang = 0 if es else 1
    out: list[AutoRow] = []
    for d in ev.decisions:
        block = BLOCK_NAMES.get(d.block, (d.block, d.block))[lang]
        item = UI.get(d.field, (d.field, d.field))[lang]
        out.append(AutoRow(block, item, d.shown(es, qfmt), d.text(es),
                           d.alternatives[lang]))
    return out


def auto_note(es: bool) -> str:
    """Advertencia que acompaña a toda selección automática."""
    return ("Recomendaciones orientativas del programa a partir de la biblioteca y de los "
            "resultados; deben ser revisadas por un ingeniero calificado antes de su uso."
            if es else "Program guidance based on the library and the results; it must be "
            "reviewed by a qualified engineer before use.")

