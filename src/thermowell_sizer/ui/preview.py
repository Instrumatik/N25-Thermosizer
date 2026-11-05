"""Vista previa 2D del termopozo con cotas, actualizada en tiempo real."""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPaintEvent, QPen, QPolygonF
from PySide6.QtWidgets import QSizePolicy, QWidget

from thermowell_sizer.core.models import ConnectionType, ShankProfile, ThermowellGeometry
from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.ui.text import t
from thermowell_sizer.ui.widgets import fmt_quantity

MARGIN = 36.0
FLANGE_THICKNESS_RATIO = 0.18
"""Espesor dibujado de la brida respecto de L (solo ilustrativo)."""
FLANGE_HEIGHT_RATIO = 3.2
"""Diámetro dibujado de la brida respecto de A."""
HEAD_LENGTH_RATIO = 0.12


def _outline(g: ThermowellGeometry, x0: float, s: float, cy: float) -> QPolygonF:
    """Contorno exterior (vista lateral) desde el soporte x0 hacia la punta."""
    half_a = g.A * s / 2
    half_b = g.B * s / 2
    tip_x = x0 + g.L * s
    pts: list[QPointF] = [QPointF(x0, cy - half_a)]
    if g.profile is ShankProfile.STEPPED:
        step_x = tip_x - g.Ls * s
        pts += [QPointF(step_x, cy - half_a), QPointF(step_x, cy - half_b)]
    pts.append(QPointF(tip_x - half_b * 0.3, cy - half_b))
    pts.append(QPointF(tip_x, cy))
    pts.append(QPointF(tip_x - half_b * 0.3, cy + half_b))
    if g.profile is ShankProfile.STEPPED:
        step_x = tip_x - g.Ls * s
        pts += [QPointF(step_x, cy + half_b), QPointF(step_x, cy + half_a)]
    pts.append(QPointF(x0, cy + half_a))
    return QPolygonF(pts)


class ThermowellPreview(QWidget):
    """Dibujo esquemático: tubería, conexión, vástago, agujero y cotas principales."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.geometry_: ThermowellGeometry | None = None
        self.connection = ConnectionType.FLANGED
        self.pipe_id: float | None = None
        self.setMinimumSize(320, 200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAccessibleName("Vista previa del termopozo")

    def set_data(
        self, geometry: ThermowellGeometry | None, connection: ConnectionType,
        pipe_id: float | None,
    ) -> None:
        """Actualiza el dibujo."""
        self.geometry_ = geometry
        self.connection = connection
        self.pipe_id = pipe_id
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802 - API de Qt
        """Dibuja la vista."""
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        pal = self.palette()
        p.fillRect(self.rect(), pal.base())
        g = self.geometry_
        if g is None:
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "—")
            p.end()
            return
        fg = pal.text().color()
        head = g.L * HEAD_LENGTH_RATIO + g.T_lag
        total = g.L + head
        avail_w = self.width() - 2 * MARGIN
        avail_h = self.height() - 2 * MARGIN - 30
        s = min(avail_w / total, avail_h / (g.A * FLANGE_HEIGHT_RATIO))
        cy = MARGIN + avail_h / 2 + 4
        x0 = MARGIN + head * s

        # Pared de tubería (si cabe en el dibujo): el termopozo entra desde la izquierda.
        if self.pipe_id:
            wall_pen = QPen(QColor("#5b8bd0"), 1, Qt.PenStyle.DashLine)
            p.setPen(wall_pen)
            p.drawLine(QPointF(x0 + g.L0 * s, MARGIN - 10), QPointF(x0 + g.L0 * s,
                                                                    self.height() - MARGIN))
            far = x0 + self.pipe_id * s
            if far < self.width() - 4:
                p.drawLine(QPointF(far, MARGIN - 10), QPointF(far, self.height() - MARGIN))
            p.setPen(QColor("#5b8bd0"))
            arrow_y = MARGIN - 4
            p.drawText(QPointF(x0 + g.L0 * s + 6, arrow_y), t("preview.flow"))

        metal = QColor("#b8bec7") if pal.base().color().lightness() > 128 else QColor("#596270")
        p.setPen(QPen(fg, 1.4))
        p.setBrush(metal)
        # Conexión
        if self.connection in (ConnectionType.FLANGED, ConnectionType.VAN_STONE):
            fh = g.A * FLANGE_HEIGHT_RATIO * s
            ft = max(g.L * FLANGE_THICKNESS_RATIO * s * 0.4, 6.0)
            p.drawRect(QRectF(x0 - ft, cy - fh / 2, ft, fh))
            p.drawRect(QRectF(MARGIN, cy - g.A * s * 0.6, x0 - ft - MARGIN, g.A * s * 1.2))
        elif self.connection is ConnectionType.THREADED:
            th = g.A * 1.25 * s
            p.drawRect(QRectF(MARGIN, cy - th / 2, x0 - MARGIN, th))
            p.setPen(QPen(fg, 0.6))
            step = 4.0
            x = x0 - (x0 - MARGIN) * 0.5
            while x < x0:
                p.drawLine(QPointF(x, cy - th / 2), QPointF(x + step / 2, cy - th / 2 - 3))
                x += step
            p.setPen(QPen(fg, 1.4))
        else:
            p.drawRect(QRectF(MARGIN, cy - g.A * s * 0.75, x0 - MARGIN, g.A * s * 1.5))
        # Vástago
        p.drawPolygon(_outline(g, x0, s, cy))
        # Agujero
        p.setBrush(pal.base())
        p.setPen(QPen(fg, 0.8, Qt.PenStyle.DashLine))
        bore_end = x0 + (g.L - g.t) * s
        p.drawRect(QRectF(MARGIN, cy - g.d * s / 2, bore_end - MARGIN, g.d * s))

        # Cotas
        p.setPen(QPen(fg, 0.8))
        y_dim = cy + g.A * FLANGE_HEIGHT_RATIO * s / 2 + 16
        self._dim(p, x0, x0 + g.L * s, y_dim, "L = " + fmt_quantity(g.L, QuantityKind.LENGTH))
        tip_x = x0 + g.L * s
        p.drawText(QPointF(x0 + 4, cy - g.A * s / 2 - 6),
                   "A = " + fmt_quantity(g.A, QuantityKind.DIAMETER))
        p.drawText(QPointF(tip_x - 90, cy + g.B * s / 2 + 14),
                   "B = " + fmt_quantity(g.B, QuantityKind.DIAMETER))
        p.drawText(QPointF(x0 + g.L * s * 0.3, cy + g.A * s / 2 + 14),
                   "d = " + fmt_quantity(g.d, QuantityKind.DIAMETER))
        p.end()

    @staticmethod
    def _dim(p: QPainter, x1: float, x2: float, y: float, label: str) -> None:
        p.drawLine(QPointF(x1, y - 6), QPointF(x1, y + 6))
        p.drawLine(QPointF(x2, y - 6), QPointF(x2, y + 6))
        p.drawLine(QPointF(x1, y), QPointF(x2, y))
        arrow = QPainterPath()
        for xa, sign in ((x1, 1), (x2, -1)):
            arrow.moveTo(xa, y)
            arrow.lineTo(xa + 6 * sign, y - 3)
            arrow.moveTo(xa, y)
            arrow.lineTo(xa + 6 * sign, y + 3)
        p.drawPath(arrow)
        p.drawText(QRectF(x1, y + 2, x2 - x1, 18), Qt.AlignmentFlag.AlignHCenter, label)
