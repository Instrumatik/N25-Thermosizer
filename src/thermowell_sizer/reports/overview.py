"""Tablas de «Datos de entrada», «Resultados calculados», «Estado ASME» y convención de largos.

Las usan la hoja de datos (página 2) y la memoria de cálculo (al inicio).
"""

from __future__ import annotations

from typing import Any, Final
from xml.sax.saxutils import escape

from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Table, TableStyle

from thermowell_sizer.core.models import CheckStatus
from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.i18n import Language
from thermowell_sizer.reports.common import STATUS_RGB, TagReport
from thermowell_sizer.reports.pdfbase import FONT, FONT_BOLD, LINE, SHADE, STYLES
from thermowell_sizer.summary import (
    CaseResults,
    asme_status,
    auto_rows,
    calculated_results,
    input_rows,
    label,
    length_convention,
    limit_text,
    value_text,
)

FS = 7.2


def _hex(rgb: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{round(c * 255):02x}" for c in rgb)


def _p(text: str, *, bold: bool = False, raw: bool = False) -> Paragraph:
    body = text if raw else escape(text)
    return Paragraph(f"<b>{body}</b>" if bold else body, STYLES["cell"])


def _dot(status: CheckStatus | None) -> str:
    if status is None:
        return ""
    return f"<font color='{_hex(STATUS_RGB[status])}'>●</font> "


def _style(header: bool = True) -> list[tuple[object, ...]]:
    st: list[tuple[object, ...]] = [
        ("FONT", (0, 0), (-1, -1), FONT, FS), ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 1.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2)]
    if header:
        st += [("FONT", (0, 0), (-1, 0), FONT_BOLD, FS), ("BACKGROUND", (0, 0), (-1, 0), SHADE)]
    return st


def _es(rep: TagReport) -> bool:
    return rep.fmt.lang is Language.ES


def formatters(rep: TagReport) -> tuple[Any, Any]:
    """Formateadores de magnitud y de número adimensional del reporte."""
    f = rep.fmt

    def q(value: float, kind: QuantityKind) -> str:
        return f.q(value, kind, gauge=kind is QuantityKind.PRESSURE)

    def n(value: float, decimals: int) -> str:
        return f.num(value, decimals)

    return q, n


def status_table(rep: TagReport, width: float) -> Table | None:
    """Recuadro «Estado ASME» con el veredicto de cada tema."""
    lines = asme_status(rep.evaluation)
    if not lines:
        return None
    es, f = _es(rep), rep.fmt
    rows: list[list[Any]] = [[f.t("res.asme_status"), ""]]
    st = _style()
    st.append(("SPAN", (0, 0), (1, 0)))
    for i, ln in enumerate(lines, start=1):
        extra = f" (V/Ve = {f.num(ln.ratio, 2)})" if ln.ratio is not None else ""
        overall = ln.key == "topic.overall"
        rows.append([_p(label(ln.key, es), bold=overall),
                     _p(_dot(ln.status) + escape(label(ln.verdict, es) + extra),
                        bold=overall, raw=True)])
        if overall:
            st.append(("BACKGROUND", (0, i), (-1, i), SHADE))
    return Table(rows, colWidths=[0.45 * width, 0.55 * width], style=TableStyle(st))


MAX_CASES_PER_TABLE: Final = 3


def results_tables(rep: TagReport, width: float, *, base_only: bool = False) -> list[Table]:
    """«Resultados calculados» en tablas de hasta tres casos (legibles en A4).

    Con ``base_only`` se omiten las variantes con sobreespesor consumido (hoja de datos).
    """
    cases = calculated_results(rep.evaluation)
    if base_only:
        cases = [c for c in cases if "|" not in c.scope]
    out: list[Table] = []
    for i in range(0, len(cases), MAX_CASES_PER_TABLE):
        t = results_table(rep, width, cases[i:i + MAX_CASES_PER_TABLE])
        if t is not None:
            out.append(t)
    return out


def results_table(rep: TagReport, width: float,
                  cases: list[CaseResults] | None = None) -> Table | None:
    """«Resultados calculados» por caso de flujo, con el límite de cada valor."""
    if cases is None:
        cases = calculated_results(rep.evaluation)
    if not cases:
        return None
    es, f = _es(rep), rep.fmt
    q, n = formatters(rep)
    head: list[Any] = [f.t("res.calculated"), ""]
    for c in cases:
        head += [f.scope(c.scope), f.t("limit")]
    rows: list[list[Any]] = [head]
    for i, row in enumerate(cases[0].rows):
        line: list[Any] = [_p(label(row.key, es)), _p(row.symbol)]
        for c in cases:
            r = c.rows[i]
            line += [_p(_dot(r.status) + escape(value_text(r.key, r.value, r.kind, q, n)),
                        raw=True), _p(limit_text(r, q, n))]
        rows.append(line)
    sym_w = 15 * mm
    name_w = 50 * mm if len(cases) < 3 else 42 * mm
    col = (width - name_w - sym_w) / (2 * len(cases))
    st = _style()
    st += [("SPAN", (0, 0), (1, 0)), ("ALIGN", (2, 0), (-1, 0), "CENTER")]
    return Table(rows, colWidths=[name_w, sym_w] + [col] * (2 * len(cases)),
                 style=TableStyle(st), repeatRows=1)


def inputs_table(rep: TagReport, width: float) -> Table:
    """Los 15 datos de entrada de la planilla con su origen y uso en el cálculo ASME."""
    es, f = _es(rep), rep.fmt
    q, n = formatters(rep)
    rows: list[list[Any]] = [["#", f.t("ov.input"), f.t("value"), f.t("ov.origin"),
                              f.t("ov.asme_use")]]
    for i, r in enumerate(input_rows(rep.evaluation, rep.record.auto_properties), start=1):
        rows.append([str(i), _p(label(r.key, es)),
                     _p(value_text(r.key, r.value, r.kind, q, n)),
                     _p(label(r.source, es)), _p(label(r.use, es))])
    w = [7 * mm, 0, 28 * mm, 36 * mm, 32 * mm]
    w[1] = width - sum(w)
    st = _style()
    st.append(("ALIGN", (0, 1), (0, -1), "CENTER"))
    return Table(rows, colWidths=w, style=TableStyle(st), repeatRows=1)


def convention_table(rep: TagReport, width: float) -> Table:
    """Equivalencia Hs + inserción (planilla) ↔ U = L desde la cara de la brida (programa)."""
    es, f = _es(rep), rep.fmt
    rows: list[list[Any]] = [[f.t("res.convention"), ""]]
    for key, value in length_convention(rep.evaluation):
        rows.append([_p(label(key, es)), f.q(value, QuantityKind.LENGTH)])
    st = _style()
    st += [("SPAN", (0, 0), (1, 0)), ("ALIGN", (1, 1), (1, -1), "RIGHT")]
    return Table(rows, colWidths=[width - 30 * mm, 30 * mm], style=TableStyle(st))


def auto_table(rep: TagReport, width: float, *, compact: bool = False) -> Table | None:
    """«Selección automática y justificación»: dato, valor elegido y por qué."""
    es, f = _es(rep), rep.fmt
    q, _ = formatters(rep)
    autos = auto_rows(rep.evaluation, es, q)
    if not autos:
        return None
    rows: list[list[Any]] = [[f.t("res.auto_field"), f.t("res.auto_value"),
                              f.t("res.auto_reason")]]
    st = _style()
    last = ""
    for ar in autos:
        if ar.block != last:
            rows.append([_p(ar.block, bold=True), "", ""])
            n = len(rows) - 1
            st += [("SPAN", (0, n), (-1, n)), ("BACKGROUND", (0, n), (-1, n), SHADE)]
            last = ar.block
        reason = escape(ar.reason)
        if ar.alternatives and not compact:
            reason += f"<br/><i>{escape(f.t('res.auto_alt'))}: {escape(ar.alternatives)}</i>"
        rows.append([_p(ar.item), _p(ar.value), _p(reason, raw=True)])
    w = [34 * mm, 42 * mm, 0.0]
    w[2] = width - w[0] - w[1]
    return Table(rows, colWidths=w, style=TableStyle(st), repeatRows=1)

