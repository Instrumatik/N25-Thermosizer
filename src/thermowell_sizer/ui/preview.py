"""Vista previa 2D del termopozo: corte acotado al estilo de catálogo, en tiempo real."""

from __future__ import annotations

from collections.abc import Sequence

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPaintEvent, QPen, QPolygonF
from PySide6.QtWidgets import QSizePolicy, QWidget

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
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.widgets import fmt_quantity

ROW_H = 15.0


class _QtPainter(Painter):
    def __init__(self, p: QPainter, colors: dict[str, QColor]) -> None:
        self.p = p
        self.colors = colors

    def line(self, x1: float, y1: float, x2: float, y2: float, *, width: float = 0.8,
             dash: bool = False, color: str = "ink") -> None:
        pen = QPen(self.colors[color], width * 1.2,
                   Qt.PenStyle.DashLine if dash else Qt.PenStyle.SolidLine)
        self.p.setPen(pen)
        self.p.drawLine(QPointF(x1, y1), QPointF(x2, y2))

    def polygon(self, pts: Sequence[tuple[float, float]], *, fill: str,
                stroke: bool = True) -> None:
        self.p.setPen(QPen(self.colors["ink"], 1.1) if stroke else Qt.PenStyle.NoPen)
        self.p.setBrush(self.colors[fill])
        self.p.drawPolygon(QPolygonF([QPointF(x, y) for x, y in pts]))

    def text(self, x: float, y: float, text: str, *, anchor: str = "start") -> None:
        w = self.text_width(text)
        dx = {"start": 0.0, "middle": -w / 2, "end": -w}[anchor]
        self.p.setPen(self.colors["ink"])
        self.p.drawText(QPointF(x + dx, y), text)

    def text_width(self, text: str) -> float:
        return float(self.p.fontMetrics().horizontalAdvance(text))


def sketch_text() -> SketchText:
    """Formatos y etiquetas del plano según el idioma y las unidades vigentes."""
    return SketchText(
        length=lambda v: fmt_quantity(v, QuantityKind.LENGTH),
        diameter=lambda v: fmt_quantity(v, QuantityKind.DIAMETER),
        labels=SKETCH_LABELS_ES if STATE.language is Language.ES else SKETCH_LABELS_EN,
    )


class ThermowellPreview(QWidget):
    """Corte longitudinal acotado del termopozo (mismo dibujo que la hoja de datos)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.input: CalcInput | None = None
        self.setMinimumSize(320, 220)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAccessibleName("Vista previa del termopozo")

    def set_input(self, inp: CalcInput | None) -> None:
        """Actualiza el dibujo."""
        self.input = inp
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802 - API de Qt
        """Dibuja la vista."""
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        pal = self.palette()
        p.fillRect(self.rect(), pal.base())
        if self.input is None:
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "—")
            p.end()
            return
        dark = pal.base().color().lightness() < 128
        colors = {
            "ink": pal.text().color(),
            "hatch": QColor("#9aa3b0") if dark else QColor("#5a6270"),
            "pipe": QColor("#5b8bd0"),
            "metal": QColor("#3c434d") if dark else QColor("#e3e7ec"),
            "plain": QColor("#596270") if dark else QColor("#c4cad3"),
            "bore": pal.base().color(),
        }
        font = p.font()
        font.setPointSizeF(max(font.pointSizeF() - 1, 7.0))
        p.setFont(font)
        render(build_sketch(self.input, sketch_text()), _QtPainter(p, colors),
               self.width(), self.height(), row_h=ROW_H, margin=8.0)
        p.end()
