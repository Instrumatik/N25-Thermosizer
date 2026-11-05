"""Memoria de cálculo en Word (versión editable, sin imágenes de ecuaciones)."""

from __future__ import annotations

import io
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.shared import Mm, Pt, RGBColor

from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.reports.charts import sensitivity_png
from thermowell_sizer.reports.common import TagReport, short_ref
from thermowell_sizer.reports.datasheet import calc_rows, sections
from thermowell_sizer.reports.mathrender import plain, render_png
from thermowell_sizer.reports.pdfbase import logo_path

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
    doc.add_heading(f.t("m.inputs"), 1)
    for title, rows in sections(rep):
        doc.add_heading(title, 2)
        _kv(doc, rows)
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
