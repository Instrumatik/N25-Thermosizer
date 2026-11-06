"""Plano acotado del termopozo para los reportes (vectorial, ReportLab)."""

from __future__ import annotations

from collections.abc import Sequence

from reportlab.graphics.shapes import Drawing, Line, Polygon, String
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth

from thermowell_sizer.core.models import CalcInput
from thermowell_sizer.core.sketch import (
    SKETCH_LABELS_EN,
    SKETCH_LABELS_ES,
    Painter,
    SketchText,
    build_sketch,
    render,
)
from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.i18n import Language
from thermowell_sizer.reports.common import Fmt
from thermowell_sizer.reports.pdfbase import FONT

COLORS = {
    "ink": colors.HexColor("#20242a"), "hatch": colors.HexColor("#5a6270"),
    "pipe": colors.HexColor("#3f6fb5"), "metal": colors.HexColor("#e3e7ec"),
    "plain": colors.HexColor("#c4cad3"), "bore": colors.white,
}
FONT_SIZE = 6.3
ROW_H = 9.5


class _RLPainter(Painter):
    def __init__(self, d: Drawing) -> None:
        self.d = d
        self.h = d.height

    def line(self, x1: float, y1: float, x2: float, y2: float, *, width: float = 0.8,
             dash: bool = False, color: str = "ink") -> None:
        self.d.add(Line(x1, self.h - y1, x2, self.h - y2, strokeColor=COLORS[color],
                        strokeWidth=width * 0.75, strokeDashArray=[3, 2] if dash else None))

    def polygon(self, pts: Sequence[tuple[float, float]], *, fill: str,
                stroke: bool = True) -> None:
        flat = [c for x, y in pts for c in (x, self.h - y)]
        self.d.add(Polygon(flat, fillColor=COLORS[fill],
                           strokeColor=COLORS["ink"] if stroke else None,
                           strokeWidth=0.6 if stroke else 0))

    def text(self, x: float, y: float, text: str, *, anchor: str = "start") -> None:
        self.d.add(String(x, self.h - y, text, fontName=FONT, fontSize=FONT_SIZE,
                          fillColor=COLORS["ink"], textAnchor=anchor))

    def text_width(self, text: str) -> float:
        return float(stringWidth(text, FONT, FONT_SIZE))


def sketch_text(fmt: Fmt) -> SketchText:
    """Formatos y etiquetas del plano según el reporte."""
    return SketchText(
        length=lambda v: fmt.q(v, QuantityKind.LENGTH),
        diameter=lambda v: fmt.q(v, QuantityKind.DIAMETER),
        labels=SKETCH_LABELS_ES if fmt.lang is Language.ES else SKETCH_LABELS_EN,
    )


def thermowell_drawing(inp: CalcInput, fmt: Fmt, width: float, height: float) -> Drawing:
    """Corte longitudinal acotado del termopozo."""
    d = Drawing(width, height)
    render(build_sketch(inp, sketch_text(fmt)), _RLPainter(d), width, height, row_h=ROW_H,
           margin=4.0)
    return d
