"""Memoria de cálculo en Word (versión editable, sin imágenes de ecuaciones)."""

from __future__ import annotations

import io
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.shared import Mm, Pt, RGBColor

from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.i18n import Language
from thermowell_sizer.reports.charts import sensitivity_png
from thermowell_sizer.reports.common import TagReport, advisory_lines, inspection_lines, short_ref
from thermowell_sizer.reports.datasheet import calc_rows, sections
from thermowell_sizer.reports.mathrender import plain, render_png
from thermowell_sizer.reports.overview import formatters
from thermowell_sizer.reports.pdfbase import logo_path
from thermowell_sizer.summary import (
    asme_status,
    auto_note,
    auto_rows,
    calculated_results,
    input_rows,
    label,
    length_convention,
    limit_text,
    value_text,
)

A4_W, A4_H = Mm(210), Mm(297)
EQ_WIDTH = Mm(55)


def build_word(rep: TagReport, path: Path) -> Path:
    """Genera la memoria en .docx."""
    f = rep.fmt
    ev = rep.evaluation
    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.PORTRAIT
    sec.page_width, sec.page_height = A4_W, A4_H
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, side, Mm(15))
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(9)
    header = sec.header.paragraphs[0]
    if logo_path().exists():
        header.add_run().add_picture(str(logo_path()), height=Mm(10))
    header.add_run(f"   {f.t('memo.title')} · {rep.tag} · "
                   f"{rep.project.info.document_number or ''}")
    foot = sec.footer.paragraphs[0]
    run = foot.add_run(f.disclaimer)
    run.bold = True
    run.font.size = Pt(7)
    run.font.color.rgb = RGBColor(0x8A, 0x4B, 0x00)

    doc.add_heading(f.t("memo.title"), 0)
    doc.add_paragraph(f"{rep.tag} — {ev.input.identification.service}".strip(" —"))
    doc.add_paragraph(f"{f.t('result')}: {f.status(ev.status)}").runs[0].bold = True
    doc.add_heading(f.t("m.scope"), 1)
    doc.add_paragraph(f.t("m.scope_text"))
    _overview(doc, rep)
    doc.add_heading(f.t("m.inputs"), 1)
    for title, rows in sections(rep):
        doc.add_heading(title, 2)
        _kv(doc, rows)
    doc.add_heading(f.t("m.auto"), 1)
    es = f.lang is Language.ES
    autos = auto_rows(ev, es, formatters(rep)[0])
    if autos:
        doc.add_paragraph(f.t("m.auto_text"))
        _grid(doc, [f.t("res.auto_field"), f.t("res.auto_value"), f.t("res.auto_reason")],
              [[f"{a.block} · {a.item}", a.value, a.reason + (
                  f" {f.t('res.auto_alt')}: {a.alternatives}." if a.alternatives else "")]
               for a in autos])
        doc.add_paragraph(auto_note(es))
    else:
        doc.add_paragraph(f.t("m.auto_none"))
    res = ev.result
    if res is not None:
        doc.add_heading(f.t("m.summary"), 1)
        t = doc.add_table(rows=1, cols=6)
        t.style = "Light Grid Accent 1"
        for cell, text in zip(t.rows[0].cells, [f.t("criterion"), f.t("case"), f.t("value"),
                                                f.t("limit"), f.t("margin"), f.t("status")],
                              strict=True):
            cell.text = text
        for c in res.checks:
            cells = t.add_row().cells
            cells[0].text = f.criterion(c.criterion_id)
            cells[1].text = f.scope(c.flow_case)
            cells[2].text = f.num(c.value)
            cells[3].text = f.num(c.limit)
            cells[4].text = f"{f.num(c.margin_pct, 1)} %"
            cells[5].text = f.status(c.status)
        _kv(doc, calc_rows(rep))
        doc.add_heading(f.t("m.trace"), 1)
        for scope in res.trace.scopes():
            doc.add_heading(f.t("m.common") if not scope else f.scope(scope), 2)
            t = doc.add_table(rows=1, cols=5)
            t.style = "Light Grid Accent 1"
            for cell, text in zip(t.rows[0].cells, [f.t("symbol"), f.t("description"),
                                                    f.t("expression"), f.t("value"),
                                                    f.t("reference")], strict=True):
                cell.text = text
            for e in (x for x in res.trace if x.scope == scope):
                cells = t.add_row().cells
                cells[0].text = e.symbol
                cells[1].text = f.t(e.description_key)
                png = render_png(e.expression) if e.expression else None
                if png is not None:
                    cells[2].paragraphs[0].add_run().add_picture(io.BytesIO(png), width=EQ_WIDTH)
                else:
                    cells[2].text = plain(e.expression)
                cells[3].text = f.q(e.value, e.kind)
                cells[4].text = short_ref(e.reference)
        png = sensitivity_png(ev, f)
        if png is not None:
            doc.add_heading(f.t("m.charts"), 1)
            doc.add_picture(io.BytesIO(png), width=Mm(175))
    if ev.thermal is not None:
        th = ev.thermal
        doc.add_heading(f.t("m.extra"), 1)
        doc.add_paragraph(f.t("extra_text"))
        _kv(doc, [(f.t("h"), f"{f.num(th.h, 0)} W/(m²·K)"),
                  (f.t("imm_err"), f.q(abs(th.immersion_error),
                                       QuantityKind.TEMPERATURE_DIFFERENCE)),
                  (f.t("tau"), f"{f.num(th.tau, 1)} s / {f.num(th.t90, 1)} s")])
    advice = advisory_lines(rep)
    if advice:
        doc.add_heading(f.t("adv.title"), 1)
        _kv(doc, [(f.t(f"adv.level.{level.value}"), text) for level, text in advice])
    doc.add_heading(f.t("insp.title"), 1)
    for text in inspection_lines(rep):
        doc.add_paragraph(text, style="List Bullet")
    doc.add_paragraph(f.disclaimer).runs[0].bold = True
    doc.save(str(path))
    return path


def _kv(doc: object, rows: list[tuple[str, str]]) -> None:
    table = doc.add_table(rows=0, cols=2)  # type: ignore[attr-defined]
    table.style = "Light List Accent 1"
    for k, v in rows:
        cells = table.add_row().cells
        cells[0].text = k
        cells[1].text = v


def _grid(doc: object, head: list[str], rows: list[list[str]]) -> None:
    table = doc.add_table(rows=1, cols=len(head))  # type: ignore[attr-defined]
    table.style = "Light Grid Accent 1"
    for cell, text in zip(table.rows[0].cells, head, strict=True):
        cell.text = text
    for row in rows:
        for cell, text in zip(table.add_row().cells, row, strict=True):
            cell.text = text


def _overview(doc: object, rep: TagReport) -> None:
    """Resumen al inicio: datos de entrada, resultados calculados, estado y convención."""
    f, ev = rep.fmt, rep.evaluation
    es = f.lang is Language.ES
    q, n = formatters(rep)
    doc.add_heading(f.t("ov.title"), 1)  # type: ignore[attr-defined]
    doc.add_heading(f.t("ov.inputs_title"), 2)  # type: ignore[attr-defined]
    doc.add_paragraph(f.t("ov.inputs_text"))  # type: ignore[attr-defined]
    _grid(doc, ["#", f.t("ov.input"), f.t("value"), f.t("ov.origin"), f.t("ov.asme_use")],
          [[str(i), label(r.key, es), value_text(r.key, r.value, r.kind, q, n),
            label(r.source, es), label(r.use, es)]
           for i, r in enumerate(input_rows(ev, rep.record.auto_properties), start=1)])
    cases = calculated_results(ev)
    if cases:
        doc.add_heading(f.t("res.calculated"), 2)  # type: ignore[attr-defined]
        head = ["", ""]
        for c in cases:
            head += [f.scope(c.scope), f.t("limit")]
        rows = []
        for i, row in enumerate(cases[0].rows):
            line = [label(row.key, es), row.symbol]
            for c in cases:
                r = c.rows[i]
                line += [value_text(r.key, r.value, r.kind, q, n), limit_text(r, q, n)]
            rows.append(line)
        _grid(doc, head, rows)
    status = asme_status(ev)
    if status:
        doc.add_heading(f.t("res.asme_status"), 2)  # type: ignore[attr-defined]
        _kv(doc, [(label(s.key, es), label(s.verdict, es) + (
            f" (V/Ve = {f.num(s.ratio, 2)})" if s.ratio is not None else "")) for s in status])
    doc.add_heading(f.t("res.convention"), 2)  # type: ignore[attr-defined]
    _kv(doc, [(label(k, es), f.q(v, QuantityKind.LENGTH)) for k, v in length_convention(ev)])
    doc.add_paragraph(f.t("res.convention_note"))  # type: ignore[attr-defined]
