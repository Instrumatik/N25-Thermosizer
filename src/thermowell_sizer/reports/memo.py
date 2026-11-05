"""Memoria de cálculo trazable en PDF, con índice, ecuaciones y gráficas."""

from __future__ import annotations

import io
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.tableofcontents import TableOfContents

from thermowell_sizer.core.models import CheckStatus
from thermowell_sizer.core.trace import TraceEntry
from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.reports.charts import sensitivity_png
from thermowell_sizer.reports.common import STATUS_RGB, Fmt, TagReport, short_ref
from thermowell_sizer.reports.datasheet import calc_rows, sections
from thermowell_sizer.reports.drawing import thermowell_drawing
from thermowell_sizer.reports.mathrender import plain, render_png
from thermowell_sizer.reports.pdfbase import (
    FONT,
    FONT_BOLD,
    FOOTER_H,
    HEADER_H,
    LINE,
    MARGIN,
    PAGE_H,
    PAGE_W,
    SHADE,
    STYLES,
    NumberedCanvas,
    footer,
    title_block,
)

BODY_W = PAGE_W - 2 * MARGIN
EQ_MAX_W = 51 * mm
EQ_SCALE = 0.36
"""Escala de las imágenes de ecuaciones (renderizadas a 200 ppp)."""


class _Doc(BaseDocTemplate):
    def afterFlowable(self, flowable: Flowable) -> None:  # noqa: N802 - API de ReportLab
        """Registra los títulos en el índice."""
        if isinstance(flowable, Paragraph) and flowable.style.name in ("h1", "h2"):
            level = 0 if flowable.style.name == "h1" else 1
            self.notify("TOCEntry", (level, flowable.getPlainText(), self.page))


def _table(data: list[list[Any]], widths: list[float], header: bool = True,
           extra: list[tuple[object, ...]] | None = None) -> Table:
    style: list[tuple[object, ...]] = [
        ("FONT", (0, 0), (-1, -1), FONT, 7.4), ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]
    if header:
        style += [("FONT", (0, 0), (-1, 0), FONT_BOLD, 7.4), ("BACKGROUND", (0, 0), (-1, 0), SHADE)]
    style += extra or []
    return Table(data, colWidths=widths, style=TableStyle(style), repeatRows=1 if header else 0)


def _p(text: str, style: str = "cell", *, raw: bool = False) -> Paragraph:
    """Párrafo; escapa el texto salvo que ya traiga marcado (``raw``)."""
    return Paragraph(text if raw else escape(text), STYLES[style])


def _equation(expr: str) -> Flowable:
    png = render_png(expr)
    if png is None:
        return _p(plain(expr))
    img = Image(io.BytesIO(png))
    w, h = img.imageWidth * EQ_SCALE, img.imageHeight * EQ_SCALE
    if w > EQ_MAX_W:
        h *= EQ_MAX_W / w
        w = EQ_MAX_W
    img.drawWidth, img.drawHeight = w, h
    return img


def _trace_rows(rep: TagReport, entries: list[TraceEntry]) -> Table:
    f = rep.fmt
    head = [f.t("symbol"), f.t("description"), f.t("expression"), f.t("substitution"),
            f.t("value"), f.t("reference")]
    rows: list[list[Any]] = [head]
    for e in entries:
        subs = "<br/>".join(
            escape(f"{k} = {f.q(v, e.input_kinds.get(k, QuantityKind.DIMENSIONLESS))}")
            for k, v in e.inputs.items())
        rows.append([_p(f"<b>{escape(e.symbol)}</b>", raw=True),
                     _p(f.t(e.description_key)),
                     _equation(e.expression) if e.expression else _p("—"),
                     _p(subs or "—", raw=True),
                     _p(f"<b>{escape(f.q(e.value, e.kind))}</b>", raw=True),
                     _p(short_ref(e.reference), "small")])
    widths = [17 * mm, 32 * mm, 54 * mm, 33 * mm, 22 * mm]
    widths.append(BODY_W - sum(widths))
    return _table(rows, widths)


def build_memo(rep: TagReport, path: Path) -> Path:
    """Genera la memoria de cálculo completa."""
    f = rep.fmt
    ev = rep.evaluation
    inp = ev.input
    doc = _Doc(str(path), pagesize=(PAGE_W, PAGE_H), title=f"{f.t('memo.title')} {rep.tag}",
               author="InstruMatik · ThermoWell Sizer")
    frame = Frame(MARGIN, MARGIN + FOOTER_H, BODY_W,
                  PAGE_H - 2 * MARGIN - HEADER_H - FOOTER_H - 4 * mm, id="body")
    doc.addPageTemplates([PageTemplate(id="page", frames=[frame])])

    story: list[Flowable] = [Spacer(1, 25 * mm), _p(f.t("memo.title"), "title"),
                             _p(f"<b>{escape(rep.tag)}</b>" + (
                                 f" — {escape(inp.identification.service)}"
                                 if inp.identification.service else ""), "center", raw=True),
                             Spacer(1, 6 * mm),
                             thermowell_drawing(inp.thermowell.geometry,
                                                inp.thermowell.connection.type, f, BODY_W,
                                                70 * mm),
                             Spacer(1, 6 * mm)]
    status = ev.status
    rgb = STATUS_RGB.get(status, (0.5, 0.5, 0.5)) if status else (0.5, 0.5, 0.5)
    story.append(_table([[f"{f.t('result')}: {f.status(status)}"]], [BODY_W], header=False,
                        extra=[("FONT", (0, 0), (-1, -1), FONT_BOLD, 14),
                               ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                               ("TEXTCOLOR", (0, 0), (-1, -1), "#ffffff"),
                               ("BACKGROUND", (0, 0), (-1, -1), _hex(rgb))]))
    story += [Spacer(1, 6 * mm), _p(f.disclaimer, "disclaimer"), PageBreak()]

    toc = TableOfContents()
    toc.levelStyles = [STYLES["body"], STYLES["small"]]
    story += [_p(f.t("toc"), "h1"), toc, PageBreak()]

    story += [_p(f.t("m.scope"), "h1"), _p(f.t("m.scope_text"), "body")]

    story.append(_p(f.t("m.inputs"), "h1"))
    for title, rows in sections(rep):
        story.append(_p(title, "h2"))
        story.append(_table([[_p(k), _p(v)] for k, v in rows], [70 * mm, BODY_W - 70 * mm],
                            header=False))
    story.append(_p(f"{f.t('props_source')}: {inp.process.properties.source_note or '—'}",
                    "small"))

    story.append(_p(f.t("m.material"), "h1"))
    mat = ev.material
    if mat is not None:
        story.append(_table([
            [_p(f.t("material")), _p(mat.name)],
            [_p(f.t("rho_m")), _p(f.q(mat.density, QuantityKind.DENSITY))],
            [_p(f.t("E")), _p(f.q(mat.elastic_modulus, QuantityKind.ELASTIC_MODULUS))],
            [_p(f.t("E_ref")), _p(f.q(mat.elastic_modulus_reference,
                                      QuantityKind.ELASTIC_MODULUS))],
            [_p(f.t("S")), _p(f.q(mat.allowable_stress, QuantityKind.STRESS))],
            [_p(f.t("S_design")), _p(f.q(mat.allowable_stress_design, QuantityKind.STRESS))],
            [_p(f.t("fatigue_class")), _p(mat.fatigue_class.value)],
            [_p(f.t("source")), _p(mat.source_note)],
        ], [70 * mm, BODY_W - 70 * mm], header=False))

    story.append(_p(f.t("m.options"), "h1"))
    o = ev.options
    yes, no = f.t("yes"), f.t("no")
    story.append(_table([
        [_p(f.t("damping")), _p(f.num(o.damping))],
        [_p(f.t("strouhal")), _p(o.strouhal_method.value)],
        [_p(f.t("fe")), _p(f.num(o.environmental_factor))],
        [_p(f.t("metal_state")), _p(o.metal_state.value if o.metal_state else f.t("auto"))],
        [_p(f.t("flange_pf")), _p(f.q(o.flange_rating + f.barometric, QuantityKind.PRESSURE,
                                      gauge=True) if o.flange_rating else "—")],
        [_p(f.t("inline")), _p(yes if o.allow_inline_passage else no)],
    ], [70 * mm, BODY_W - 70 * mm], header=False))

    res = ev.result
    if res is not None:
        story.append(_p(f.t("m.summary"), "h1"))
        order = {CheckStatus.FAIL: 0, CheckStatus.WARNING: 1, CheckStatus.PASS: 2,
                 CheckStatus.NOT_APPLICABLE: 3}
        checks: list[list[Any]] = [[f.t("criterion"), f.t("case"), f.t("value"), f.t("limit"),
                                    f.t("margin"), f.t("status"), f.t("reference")]]
        extra: list[tuple[object, ...]] = []
        for i, c in enumerate(sorted(res.checks, key=lambda c: order[c.status]), start=1):
            plain_row = c.criterion_id == "scope" or c.status is CheckStatus.NOT_APPLICABLE
            checks.append([_p(f.criterion(c.criterion_id)), _p(f.scope(c.flow_case)),
                         _p("—" if plain_row else _check_value(f, c.criterion_id, c.value)),
                         _p("—" if plain_row else _check_value(f, c.criterion_id, c.limit)),
                         "—" if plain_row else f"{f.num(c.margin_pct, 1)} %",
                         f.status(c.status), _p(short_ref(c.reference), "small")])
            extra.append(("TEXTCOLOR", (5, i), (5, i), _hex(STATUS_RGB[c.status])))
        widths = [40 * mm, 22 * mm, 26 * mm, 26 * mm, 16 * mm, 20 * mm]
        widths.append(BODY_W - sum(widths))
        story.append(_table(checks, widths, extra=extra))
        story.append(Spacer(1, 3 * mm))
        story.append(_table([[_p(k), _p(v)] for k, v in calc_rows(rep)],
                            [70 * mm, BODY_W - 70 * mm], header=False))

        story.append(_p(f.t("m.cases"), "h1"))
        head = [f.t("case"), "V", "Re", "N_S", "f_s", "f_n", "H_c", "f_n,c", "N_Sc", "f_s/f_n,c"]
        crow: list[list[Any]] = [head]
        for cs in res.cases:
            crow.append([_p(f.scope(cs.scope)), f.q(cs.velocity, QuantityKind.VELOCITY),
                         f.num(cs.reynolds, 0), f.num(cs.strouhal, 3),
                         f.q(cs.fs, QuantityKind.FREQUENCY), f.q(cs.fn, QuantityKind.FREQUENCY),
                         f.num(cs.hc, 3), f.q(cs.fnc, QuantityKind.FREQUENCY),
                         f.num(cs.scruton, 2), f.num(cs.fs / cs.fnc, 3) if cs.fnc else "—"])
        story.append(_table(crow, [26 * mm] + [(BODY_W - 26 * mm) / 9] * 9))

        story.append(_p(f.t("m.trace"), "h1"))
        for scope in res.trace.scopes():
            entries = [e for e in res.trace if e.scope == scope]
            title = f.t("m.common") if not scope else f.scope(scope)
            story.append(_p(title, "h2"))
            story.append(_trace_rows(rep, entries))

        png = sensitivity_png(ev, f)
        if png is not None:
            img = Image(io.BytesIO(png))
            ratio = BODY_W / img.imageWidth
            img.drawWidth, img.drawHeight = BODY_W, img.imageHeight * ratio
            story += [_p(f.t("m.charts"), "h1"), img]

    th = ev.thermal
    if th is not None:
        story += [_p(f.t("m.extra"), "h1"), _p(f.t("extra_text"), "body"),
                  _table([[_p(f.t("h")), _p(f"{f.num(th.h, 0)} W/(m²·K)")],
                          [_p(f.t("imm_err")), _p(f.q(abs(th.immersion_error),
                                                      QuantityKind.TEMPERATURE_DIFFERENCE))],
                          [_p(f.t("imm_min")), _p(f.q(th.min_immersion, QuantityKind.LENGTH))],
                          [_p(f.t("tau")), _p(f"{f.num(th.tau, 1)} s / {f.num(th.t90, 1)} s")]],
                         [70 * mm, BODY_W - 70 * mm], header=False)]

    notes = [f.t(w) for w in ev.warnings]
    if res is not None:
        notes += [f.t(n) for n in res.notes]
        notes += [f"{i.field}: {f.t(i.message_key)} ({i.reference})" for i in res.issues]
    story.append(KeepTogether([_p(f.t("m.notes"), "h1")] +
                              [_p(f"{i}. {n}", "body") for i, n in enumerate(notes, 1)] +
                              [Spacer(1, 4 * mm), _p(f.disclaimer, "disclaimer")]))

    def decorate(c: NumberedCanvas, page: int, total: int) -> None:
        title_block(c, rep.project, f, f.t("memo.title"),
                    f"{rep.tag} — {inp.identification.service}".strip(" —"), page, total)
        footer(c, f)

    doc.multiBuild(story, canvasmaker=lambda *a, **k: NumberedCanvas(*a, decorate=decorate, **k))
    return path


def _hex(rgb: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{round(c * 255):02x}" for c in rgb)


def _check_value(f: Fmt, cid: str, value: float) -> str:
    kind, gauge = _check_kind(cid)
    return f.q(value + (f.barometric if gauge else 0.0), kind, gauge=gauge)


def _check_kind(cid: str) -> tuple[QuantityKind, bool]:
    if cid in ("pressure_rating", "pressure_high_service", "flange_rating"):
        return QuantityKind.PRESSURE, True
    return {"material_temperature": (QuantityKind.TEMPERATURE, False),
            "low_velocity": (QuantityKind.VELOCITY, False),
            "frequency_limit": (QuantityKind.FREQUENCY, False),
            "inline_lockin_dwell": (QuantityKind.FREQUENCY, False)}.get(
        cid, (QuantityKind.STRESS, False))
