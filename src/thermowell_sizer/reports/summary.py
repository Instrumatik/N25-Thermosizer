"""Resumen de proyecto en PDF: tabla de todos los tags y lista de materiales."""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from thermowell_sizer.core.models import CheckStatus
from thermowell_sizer.reports.common import STATUS_RGB, TagReport
from thermowell_sizer.reports.excel import bom_rows, summary_rows
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


def _grid(data: list[list[object]], widths: list[float],
          extra: list[tuple[object, ...]]) -> Table:
    style: list[tuple[object, ...]] = [
        ("FONT", (0, 0), (-1, -1), FONT, 7), ("FONT", (0, 0), (-1, 0), FONT_BOLD, 7),
        ("BACKGROUND", (0, 0), (-1, 0), SHADE), ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), *extra]
    return Table(data, colWidths=widths, style=TableStyle(style), repeatRows=1)


def build_summary(reps: list[TagReport], path: Path) -> Path:
    """Genera el resumen del proyecto."""
    f = reps[0].fmt
    doc = SimpleDocTemplate(str(path), pagesize=(PAGE_W, PAGE_H), leftMargin=MARGIN,
                            rightMargin=MARGIN, topMargin=MARGIN + HEADER_H + 3 * mm,
                            bottomMargin=MARGIN + FOOTER_H, title=f.t("summary.title"))
    cell = STYLES["cell"]
    head, rows = summary_rows(reps)
    data: list[list[object]] = [[Paragraph(h, STYLES["cellb"]) for h in head]]
    extra: list[tuple[object, ...]] = []
    for i, r in enumerate(rows, 1):
        status = r[-1] if isinstance(r[-1], CheckStatus) else None
        data.append([Paragraph(escape(str(x)), cell) for x in r[:-1]] + [f.status(status)])
        if status is not None:
            rgb = STATUS_RGB[status]
            color = "#" + "".join(f"{round(c * 255):02x}" for c in rgb)
            extra += [("TEXTCOLOR", (-1, i), (-1, i), color),
                      ("FONT", (-1, i), (-1, i), FONT_BOLD, 7)]
    widths = [16 * mm, 28 * mm, 16 * mm, 26 * mm, 13 * mm, 14 * mm, 14 * mm, 13 * mm,
              18 * mm]
    widths.append(BODY_W - sum(widths))
    counts = {s: sum(1 for r in rows if r[-1] is s) for s in CheckStatus}
    story = [Paragraph(f"<b>{f.t('summary.title')}</b>", STYLES["h1"]),
             Paragraph(f"{len(rows)} tags · {f.status(CheckStatus.PASS)}: "
                       f"{counts[CheckStatus.PASS]} · {f.status(CheckStatus.WARNING)}: "
                       f"{counts[CheckStatus.WARNING]} · {f.status(CheckStatus.FAIL)}: "
                       f"{counts[CheckStatus.FAIL]}", STYLES["body"]),
             Spacer(1, 3 * mm), _grid(data, widths, extra),
             Spacer(1, 6 * mm), Paragraph(f"<b>{f.t('bom.title')}</b>", STYLES["h1"])]
    bhead, brows = bom_rows(reps)
    bdata: list[list[object]] = [[Paragraph(h, STYLES["cellb"]) for h in bhead]]
    bdata += [[Paragraph(escape(str(x)), cell) for x in r] for r in brows]
    bw = [10 * mm, 10 * mm, 52 * mm, 30 * mm, 50 * mm, 18 * mm]
    bw.append(BODY_W - sum(bw))
    story.append(_grid(bdata, bw, []))

    def decorate(c: NumberedCanvas, page: int, total: int) -> None:
        title_block(c, reps[0].project, f, f.t("summary.title"),
                    reps[0].project.info.client, page, total)
        footer(c, f)

    doc.build(story, canvasmaker=lambda *a, **k: NumberedCanvas(*a, decorate=decorate, **k))
    return path
