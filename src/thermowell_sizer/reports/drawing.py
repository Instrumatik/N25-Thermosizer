"""Plano esquemático del termopozo para los reportes (vectorial, ReportLab)."""

from __future__ import annotations

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors

from thermowell_sizer.core.models import ConnectionType, ShankProfile, ThermowellGeometry
from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.reports.common import Fmt
from thermowell_sizer.reports.pdfbase import FONT

METAL = colors.HexColor("#c4cad3")
INK = colors.HexColor("#20242a")
FLANGE_H_RATIO = 3.2
HEAD_RATIO = 0.18
PAD = 14.0


def thermowell_drawing(g: ThermowellGeometry, connection: ConnectionType, fmt: Fmt,
                       width: float, height: float) -> Drawing:
    """Vista lateral con cotas L, U, A, B y d."""
    d = Drawing(width, height)
    head = g.L * HEAD_RATIO + g.T_lag
    total = g.L + head
    s = min((width - 2 * PAD) / total, (height - 2 * PAD - 26) / (g.A * FLANGE_H_RATIO))
    cy = height / 2 + 8
    x0 = PAD + head * s
    tip = x0 + g.L * s
    ha, hb = g.A * s / 2, g.B * s / 2
    flanged = connection in (ConnectionType.FLANGED, ConnectionType.VAN_STONE)
    if flanged:
        fh = g.A * FLANGE_H_RATIO * s
        ft = max(g.L * s * 0.05, 4.0)
        d.add(Rect(x0 - ft, cy - fh / 2, ft, fh, fillColor=METAL, strokeColor=INK,
                   strokeWidth=0.8))
        d.add(Rect(PAD, cy - ha * 1.2, x0 - ft - PAD, ha * 2.4, fillColor=METAL,
                   strokeColor=INK, strokeWidth=0.8))
    else:
        hh = ha * (1.25 if connection is ConnectionType.THREADED else 1.5)
        d.add(Rect(PAD, cy - hh, x0 - PAD, 2 * hh, fillColor=METAL, strokeColor=INK,
                   strokeWidth=0.8))
    pts: list[float] = [x0, cy + ha]
    if g.profile is ShankProfile.STEPPED:
        sx = tip - g.Ls * s
        pts += [sx, cy + ha, sx, cy + hb]
    pts += [tip - hb * 0.3, cy + hb, tip, cy, tip - hb * 0.3, cy - hb]
    if g.profile is ShankProfile.STEPPED:
        sx = tip - g.Ls * s
        pts += [sx, cy - hb, sx, cy - ha]
    pts += [x0, cy - ha]
    d.add(Polygon(pts, fillColor=METAL, strokeColor=INK, strokeWidth=0.8))
    bore_end = x0 + (g.L - g.t) * s
    d.add(Rect(PAD, cy - g.d * s / 2, bore_end - PAD, g.d * s, fillColor=colors.white,
               strokeColor=INK, strokeWidth=0.5, strokeDashArray=[2, 1.5]))
    y_dim = cy - (g.A * FLANGE_H_RATIO * s / 2 if flanged else ha * 1.5) - 10
    _dim(d, x0, tip, y_dim, "L = " + fmt.q(g.L, QuantityKind.LENGTH))
    if g.U is not None and abs(g.U - g.L) > 1e-6:
        _dim(d, tip - g.U * s, tip, y_dim - 14, "U = " + fmt.q(g.U, QuantityKind.LENGTH))
    d.add(String(x0 + 3, cy + ha + 3, "A = " + fmt.q(g.A, QuantityKind.DIAMETER), fontName=FONT,
                 fontSize=6.5, fillColor=INK))
    d.add(String(tip - 4, cy + hb + 3, "B = " + fmt.q(g.B, QuantityKind.DIAMETER), fontName=FONT,
                 fontSize=6.5, fillColor=INK, textAnchor="end"))
    d.add(String(x0 + (tip - x0) * 0.35, cy - ha - 8, "d = " + fmt.q(g.d, QuantityKind.DIAMETER),
                 fontName=FONT, fontSize=6.5, fillColor=INK))
    return d


def _dim(d: Drawing, x1: float, x2: float, y: float, label: str) -> None:
    for x in (x1, x2):
        d.add(Line(x, y - 3, x, y + 3, strokeColor=INK, strokeWidth=0.5))
    d.add(Line(x1, y, x2, y, strokeColor=INK, strokeWidth=0.5))
    for x, sgn in ((x1, 1), (x2, -1)):
        d.add(Polygon([x, y, x + 4 * sgn, y + 1.6, x + 4 * sgn, y - 1.6], fillColor=INK,
                      strokeColor=INK, strokeWidth=0.1))
    d.add(String((x1 + x2) / 2, y - 8, label, fontName=FONT, fontSize=6.5, fillColor=INK,
                 textAnchor="middle"))
