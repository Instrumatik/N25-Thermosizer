"""Base común de los PDF: fuentes Unicode, estilos, rótulo y pie de página."""

from __future__ import annotations

from pathlib import Path
from typing import Final

import matplotlib
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from thermowell_sizer.project import Project
from thermowell_sizer.reports.common import Fmt, current_revision

PAGE_W, PAGE_H = A4
MARGIN: Final = 12 * mm
HEADER_H: Final = 24 * mm
FOOTER_H: Final = 14 * mm
FONT: Final = "DejaVu"
FONT_BOLD: Final = "DejaVu-Bold"
LINE: Final = colors.HexColor("#4a4f57")
SHADE: Final = colors.HexColor("#e8ecf2")
ACCENT: Final = colors.HexColor("#1f4e8c")


def _register_fonts() -> None:
    if FONT in pdfmetrics.getRegisteredFontNames():
        return
    base = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    pdfmetrics.registerFont(TTFont(FONT, str(base / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, str(base / "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFontFamily(FONT, normal=FONT, bold=FONT_BOLD, italic=FONT,
                                  boldItalic=FONT_BOLD)


_register_fonts()


def logo_path() -> Path:
    """Logo de la empresa para el rótulo."""
    from thermowell_sizer.ui.assets import asset_path

    return asset_path("logo_tws.png")


STYLES: Final = {
    "body": ParagraphStyle("body", fontName=FONT, fontSize=8.5, leading=11),
    "small": ParagraphStyle("small", fontName=FONT, fontSize=7, leading=8.6),
    "cell": ParagraphStyle("cell", fontName=FONT, fontSize=7.4, leading=9),
    "cellb": ParagraphStyle("cellb", fontName=FONT_BOLD, fontSize=7.4, leading=9),
    "h1": ParagraphStyle("h1", fontName=FONT_BOLD, fontSize=12, leading=15, spaceBefore=8,
                         spaceAfter=5, textColor=ACCENT),
    "h2": ParagraphStyle("h2", fontName=FONT_BOLD, fontSize=9.5, leading=12, spaceBefore=6,
                         spaceAfter=3),
    "title": ParagraphStyle("title", fontName=FONT_BOLD, fontSize=18, leading=22,
                            alignment=TA_CENTER, spaceAfter=8),
    "center": ParagraphStyle("center", fontName=FONT, fontSize=9, leading=12,
                             alignment=TA_CENTER),
    "disclaimer": ParagraphStyle("disclaimer", fontName=FONT_BOLD, fontSize=7.2, leading=9,
                                 textColor=colors.HexColor("#8a4b00")),
}


def title_block(c: Canvas, project: Project, fmt: Fmt, title: str, subtitle: str,
                page: int, pages: int | None) -> None:
    """Rótulo superior tipo ISA: logo, título, documento, revisión, fecha y hoja."""
    x0, y_top = MARGIN, PAGE_H - MARGIN
    w = PAGE_W - 2 * MARGIN
    h = HEADER_H
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.rect(x0, y_top - h, w, h)
    logo_w = 42 * mm
    info_w = 50 * mm
    c.line(x0 + logo_w, y_top - h, x0 + logo_w, y_top)
    c.line(x0 + w - info_w, y_top - h, x0 + w - info_w, y_top)
    logo = logo_path()
    if logo.exists():
        c.drawImage(str(logo), x0 + 2 * mm, y_top - h + 3 * mm, width=logo_w - 4 * mm,
                    height=h - 6 * mm, preserveAspectRatio=True, mask="auto")
    cx = x0 + logo_w + (w - logo_w - info_w) / 2
    size = 12.0
    while size > 7 and c.stringWidth(title, FONT_BOLD, size) > w - logo_w - info_w - 4 * mm:
        size -= 0.5
    c.setFont(FONT_BOLD, size)
    c.drawCentredString(cx, y_top - 9 * mm, title)
    c.setFont(FONT, 8.5)
    c.drawCentredString(cx, y_top - 14.5 * mm, subtitle[:90])
    c.drawCentredString(cx, y_top - 19.5 * mm, project.info.name[:90])
    rev, rev_date = current_revision(project)
    rows = [(fmt.t("doc"), project.info.document_number or "—"), (fmt.t("rev"), rev),
            (fmt.t("date"), rev_date),
            (fmt.t("sheet"), f"{page} {fmt.t('of')} {pages}" if pages else str(page))]
    rh = h / len(rows)
    ix = x0 + w - info_w
    for i, (k, v) in enumerate(rows):
        y = y_top - (i + 1) * rh
        if i:
            c.line(ix, y + rh, x0 + w, y + rh)
        c.setFont(FONT, 6.5)
        c.drawString(ix + 1.5 * mm, y + rh - 2.6 * mm, k)
        c.setFont(FONT_BOLD, 8)
        c.drawRightString(x0 + w - 1.5 * mm, y + 1.4 * mm, v[:28])


WATERMARK_GRAY: Final = 0.45
WATERMARK_ALPHA: Final = 0.16
WATERMARK_SIZE: Final = 46
WATERMARK_ANGLE: Final = 52


def footer(c: Canvas, fmt: Fmt) -> None:
    """Pie: aviso de responsabilidad y versión; marca de agua si no hay licencia."""
    if fmt.licensee is None:
        c.saveState()
        c.setFillGray(WATERMARK_GRAY)
        c.setFillAlpha(WATERMARK_ALPHA)
        c.setFont(FONT_BOLD, WATERMARK_SIZE)
        c.translate(PAGE_W / 2, PAGE_H / 2)
        c.rotate(WATERMARK_ANGLE)
        c.drawCentredString(0, 0, fmt.t("evaluation"))
        c.restoreState()
    c.setFont(FONT_BOLD, 6.6)
    c.setFillColor(colors.HexColor("#8a4b00"))
    text = fmt.disclaimer
    words = text.split()
    lines: list[str] = []
    cur = ""
    max_w = PAGE_W - 2 * MARGIN
    for word in words:
        trial = f"{cur} {word}".strip()
        if c.stringWidth(trial, FONT_BOLD, 6.6) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    lines.append(cur)
    y = MARGIN + 6 * mm
    for line in lines[:2]:
        c.drawString(MARGIN, y, line)
        y -= 2.8 * mm
    c.setFillColor(colors.black)
    c.setFont(FONT, 6)
    c.drawRightString(PAGE_W - MARGIN, MARGIN - 1 * mm, fmt.footer())


class NumberedCanvas(Canvas):
    """Canvas que conoce el total de páginas para escribir "Hoja n de N"."""

    def __init__(self, *args: object, decorate: object = None, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self._saved: list[dict[str, object]] = []
        self.decorate = decorate

    def showPage(self) -> None:  # noqa: N802 - API de ReportLab
        """Guarda el estado de la página para completarla al final."""
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self) -> None:
        """Dibuja rótulos con el total de páginas y guarda."""
        total = len(self._saved)
        for state in self._saved:
            self.__dict__.update(state)
            if callable(self.decorate):
                self.decorate(self, self._pageNumber, total)
            super().showPage()
        super().save()
