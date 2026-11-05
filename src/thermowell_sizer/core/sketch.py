"""Plano acotado del termopozo, independiente de la biblioteca gráfica.

Arma un corte longitudinal al estilo de los catálogos de fabricantes: cabezal con rosca
para el sensor, conexión a proceso (rosca, brida, socket weld, weld-in o Van Stone),
vástago en corte con el agujero y cotas de inserción U, largo de rosca, extensión T,
largo del agujero, largo total, espesor de punta y diámetros. La interfaz (Qt) y los
reportes (ReportLab) dibujan el mismo :class:`Sketch`, así pantalla y papel coinciden.

Coordenadas del modelo en metros: x a lo largo del eje (0 = extremo del cabezal, la
punta hacia +x) e y radial (0 = eje). Las medidas de cabezal, rosca y brida son
nominales y solo ilustrativas; las cotas del termopozo son las del cálculo.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Final

from thermowell_sizer.core.models import CalcInput, ConnectionType, FlangeFace, ShankProfile

MM: Final = 1e-3
INCH: Final = 0.0254

# --- Medidas nominales de conexión ---------------------------------------------------
NPT_OD: Final[dict[str, float]] = {
    "1/2": 21.3 * MM, "3/4": 26.7 * MM, "1": 33.4 * MM, "1-1/4": 42.2 * MM,
    "1-1/2": 48.3 * MM, "2": 60.3 * MM,
}
"""Diámetro exterior de la rosca NPT macho (= OD del caño), m."""
NPT_ENGAGEMENT: Final[dict[str, float]] = {
    "1/2": 20.0 * MM, "3/4": 21.5 * MM, "1": 25.0 * MM, "1-1/4": 26.0 * MM,
    "1-1/2": 26.5 * MM, "2": 27.5 * MM,
}
"""Largo de rosca de proceso habitual, m."""
HEX_ACROSS_FLATS: Final[dict[str, float]] = {
    "1/2": 7 / 8 * INCH, "3/4": 1.0625 * INCH, "1": 1.375 * INCH, "1-1/4": 1.75 * INCH,
    "1-1/2": 2.0 * INCH, "2": 2.5 * INCH,
}
HEX_LENGTH: Final = 25.0 * MM
"""Largo del hexágono del cabezal roscado."""
HEAD_THREAD: Final = "1/2"
"""Rosca interna del cabezal para el sensor o el cabezal de conexión (1/2" NPT)."""
HEAD_THREAD_DEPTH: Final = 19.0 * MM
FLANGE_HUB_LENGTH: Final = 1.75 * INCH
"""Distancia del extremo del cuello a la cara trasera de la brida (catálogos: 1 3/4")."""
FLANGE_HUB_DIAMETER: Final = 1.25 * INCH
SOCKET_BODY_LENGTH: Final = 1.75 * INCH
VAN_STONE_HUB_LENGTH: Final = 2.25 * INCH
VAN_STONE_COLLAR: Final = 9.5 * MM

# Bridas ASME B16.5 (diámetro exterior, espesor) por tamaño y clase, m. Valores
# nominales redondeados para el dibujo; no se usan en el cálculo.
FLANGE_DIMS: Final[dict[str, dict[int, tuple[float, float]]]] = {
    "1": {150: (108, 14.3), 300: (124, 17.5), 600: (124, 17.5), 900: (149, 28.6),
          1500: (149, 28.6), 2500: (159, 35.0)},
    "1-1/2": {150: (127, 17.5), 300: (156, 20.6), 600: (156, 22.4), 900: (178, 31.8),
              1500: (178, 31.8), 2500: (203, 44.5)},
    "2": {150: (152, 19.1), 300: (165, 22.4), 600: (165, 25.4), 900: (216, 38.1),
          1500: (216, 38.1), 2500: (235, 50.8)},
}
FLANGE_DRAW_MAX_RATIO: Final = 2.0
"""El radio dibujado de la brida se limita a 2·A para que el vástago se lea bien."""
RAISED_FACE: Final[dict[str, float]] = {"1": 50.8, "1-1/2": 73.2, "2": 92.1}
"""Diámetro del resalto RF, mm."""


def _size_key(text: str) -> str:
    """'1-1/2 in', '1 1/2"', '3/4 NPT' -> clave de tabla."""
    clean = text.replace('"', " ").replace("in", " ").replace("NPT", " ").replace("½", "-1/2")
    parts = clean.replace("-", " ").split()
    if len(parts) >= 2 and "/" in parts[1]:
        return f"{parts[0]}-{parts[1]}"
    return parts[0] if parts else ""


# --- Primitivas ------------------------------------------------------------------------
class Fill(StrEnum):
    """Relleno de un polígono."""

    SECTION = "section"
    """Metal cortado (rayado)."""
    BORE = "bore"
    """Hueco (fondo blanco)."""
    PLAIN = "plain"
    """Metal en vista (sin rayado)."""


@dataclass(frozen=True, slots=True)
class Poly:
    """Polígono cerrado en coordenadas del modelo."""

    points: tuple[tuple[float, float], ...]
    fill: Fill


@dataclass(frozen=True, slots=True)
class Stroke:
    """Línea suelta: ``style`` = solid | dashed | center | thread."""

    p1: tuple[float, float]
    p2: tuple[float, float]
    style: str = "solid"


@dataclass(frozen=True, slots=True)
class HDim:
    """Cota horizontal de x1 a x2. ``row`` > 0 debajo de la pieza, < 0 arriba."""

    x1: float
    x2: float
    row: int
    text: str
    outside: bool = False
    """Texto a la derecha de la cota (para cotas cortas en el extremo)."""


@dataclass(frozen=True, slots=True)
class VDim:
    """Cota vertical (diámetro) centrada en el eje, ubicada en x."""

    x: float
    half: float
    text: str


@dataclass(frozen=True, slots=True)
class Leader:
    """Nota con flecha a un punto. ``slot`` ordena las notas (arriba si slot < 0)."""

    x: float
    y: float
    slot: int
    text: str


@dataclass(slots=True)
class Sketch:
    """Dibujo completo, listo para renderizar."""

    polys: list[Poly] = field(default_factory=list)
    strokes: list[Stroke] = field(default_factory=list)
    hdims: list[HDim] = field(default_factory=list)
    vdims: list[VDim] = field(default_factory=list)
    leaders: list[Leader] = field(default_factory=list)
    x_min: float = 0.0
    x_max: float = 0.0
    half_height: float = 0.0

    @property
    def rows_below(self) -> int:
        """Filas de cotas debajo."""
        return max((d.row for d in self.hdims if d.row > 0), default=0)

    @property
    def rows_above(self) -> int:
        """Filas de cotas y notas arriba."""
        dims = max((-d.row for d in self.hdims if d.row < 0), default=0)
        notes = max((-n.slot for n in self.leaders if n.slot < 0), default=0)
        return max(dims, notes)

    @property
    def notes_below(self) -> int:
        """Notas debajo."""
        return max((n.slot for n in self.leaders if n.slot > 0), default=0)


def _rect(x1: float, x2: float, half: float, fill: Fill) -> Poly:
    return Poly(((x1, -half), (x2, -half), (x2, half), (x1, half)), fill)


def hatch_segments(points: Sequence[tuple[float, float]], spacing: float
                   ) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """Segmentos de rayado a 45° dentro de un polígono simple (regla par-impar)."""
    if spacing <= 0:
        return []
    # Rotamos para que las rayas queden horizontales: u = x - y (constante a 45°).
    us = [x - y for x, y in points]
    out: list[tuple[tuple[float, float], tuple[float, float]]] = []
    n = len(points)
    u = math.floor(min(us) / spacing) * spacing + spacing / 2
    while u < max(us):
        hits: list[float] = []
        for i in range(n):
            (x1, y1), (x2, y2) = points[i], points[(i + 1) % n]
            u1, u2 = x1 - y1, x2 - y2
            if (u1 <= u < u2) or (u2 <= u < u1):
                r = (u - u1) / (u2 - u1)
                hits.append(x1 + r * (x2 - x1))
        hits.sort()
        for a, b in zip(hits[::2], hits[1::2], strict=False):
            out.append(((a, a - u), (b, b - u)))
        u += spacing
    return out


# --- Armado ---------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class SketchText:
    """Textos y formatos que provee quien dibuja (idioma y unidades)."""

    length: Callable[[float], str]
    diameter: Callable[[float], str]
    labels: dict[str, str]

    def lab(self, key: str) -> str:
        """Etiqueta traducida."""
        return self.labels.get(key, key)


SKETCH_LABELS_ES: Final[dict[str, str]] = {
    "U": "U · Largo de inserción", "L": "L · Longitud no soportada",
    "I": "I · Largo de rosca", "T": "T · Extensión", "E": "E · Espesor de brida",
    "bore": "Largo del agujero", "total": "Largo total", "t": "t · punta",
    "Ls": "Ls · Tramo reducido", "L0": "L0 · Protegido", "A": "Ø raíz A",
    "B": "Ø punta B", "d": "Ø agujero d", "head": '1/2" NPT (cabezal)',
    "weld": "Soldadura", "pipe": "Pared interna de la tubería", "flow": "Flujo",
    "socket": "Socket weld", "weld_in": "Para soldar", "van_stone": "Van Stone",
    "sanitary": "Sanitaria", "threaded": "NPT", "flanged": "Brida",
}
SKETCH_LABELS_EN: Final[dict[str, str]] = {
    "U": "U · Insertion length", "L": "L · Unsupported length",
    "I": "I · Thread length", "T": "T · Lag extension", "E": "E · Flange thickness",
    "bore": "Bore depth", "total": "Overall length", "t": "t · tip",
    "Ls": "Ls · Reduced section", "L0": "L0 · Shielded", "A": "Root Ø A",
    "B": "Tip Ø B", "d": "Bore Ø d", "head": '1/2" NPT (head)',
    "weld": "Weld", "pipe": "Pipe inside wall", "flow": "Flow",
    "socket": "Socket weld", "weld_in": "Weld-in", "van_stone": "Van Stone",
    "sanitary": "Sanitary", "threaded": "NPT", "flanged": "Flange",
}


def build_sketch(inp: CalcInput, tx: SketchText) -> Sketch:
    """Corte longitudinal acotado del termopozo de ``inp``."""
    g = inp.thermowell.geometry
    conn = inp.thermowell.connection
    sk = Sketch()
    size = _size_key(conn.size) or "3/4"
    ra, rb, rd = g.A / 2, g.B / 2, g.d / 2
    lag = g.T_lag
    head_r = NPT_OD[HEAD_THREAD] / 2 * 0.86  # rosca interna del cabezal
    conn_text = ""
    x = 0.0  # avanza desde el cabezal hacia la punta

    if conn.type is ConnectionType.THREADED:
        hex_r = HEX_ACROSS_FLATS.get(size, max(1.3 * g.A, 22 * MM)) / 2
        thread_r = NPT_OD.get(size, max(g.A * 1.15, 21.3 * MM)) / 2
        thread_len = NPT_ENGAGEMENT.get(size, 21.5 * MM)
        sk.polys.append(_rect(0.0, HEX_LENGTH, hex_r, Fill.SECTION))
        x = HEX_LENGTH
        if lag > 0:
            sk.polys.append(_rect(x, x + lag, thread_r * 0.9, Fill.SECTION))
            sk.hdims.append(HDim(x, x + lag, -2, f"{tx.lab('T')} = {tx.length(lag)}"))
            x += lag
        conn_start = x
        sk.polys.append(_rect(x, x + thread_len, thread_r, Fill.SECTION))
        tick = thread_len / 8
        for i in range(8):
            xi = x + i * tick
            for sgn in (1, -1):
                sk.strokes.append(Stroke((xi, sgn * thread_r), (xi + tick / 2,
                                                                sgn * thread_r * 1.06),
                                         "thread"))
        sk.hdims.append(HDim(x, x + thread_len, -1,
                             f"{tx.lab('I')} = {tx.length(thread_len)}"))
        conn_text = f'{conn.size or size + chr(34)} {tx.lab("threaded")}'
        x += thread_len
        conn_r = thread_r
    elif conn.type in (ConnectionType.FLANGED, ConnectionType.VAN_STONE,
                       ConnectionType.SANITARY):
        cls = conn.rating_class or 150
        od_mm, e_mm = FLANGE_DIMS.get(size, FLANGE_DIMS["1-1/2"]).get(cls, (156, 20.6))
        hub_r = max(FLANGE_HUB_DIAMETER / 2, ra * 1.15)
        hub_len = (VAN_STONE_HUB_LENGTH if conn.type is ConnectionType.VAN_STONE
                   else FLANGE_HUB_LENGTH) + lag
        sk.polys.append(_rect(0.0, hub_len, hub_r, Fill.SECTION))
        if lag > 0:
            sk.hdims.append(HDim(hub_len - lag, hub_len, -2,
                                 f"{tx.lab('T')} = {tx.length(lag)}"))
        x = hub_len
        conn_start = x - VAN_STONE_COLLAR
        e = e_mm * MM
        if conn.type is ConnectionType.VAN_STONE:
            collar_r = RAISED_FACE.get(size, 73.2) / 2 * MM
            sk.polys.append(_rect(x - VAN_STONE_COLLAR, x, collar_r, Fill.SECTION))
            fl_r = od_mm / 2 * MM
            for sgn in (1, -1):  # brida loca, en línea de trazos
                y_in, y_out = sgn * collar_r * 0.8, sgn * fl_r
                sk.strokes += [Stroke((x - VAN_STONE_COLLAR - e, y_in), (x - VAN_STONE_COLLAR,
                                                                         y_in), "dashed"),
                               Stroke((x - VAN_STONE_COLLAR - e, y_out),
                                      (x - VAN_STONE_COLLAR, y_out), "dashed"),
                               Stroke((x - VAN_STONE_COLLAR - e, y_in),
                                      (x - VAN_STONE_COLLAR - e, y_out), "dashed")]
            conn_text = f'{tx.lab("van_stone")} {conn.size} {cls}#'
        else:
            fl_r = min(od_mm / 2 * MM, max(FLANGE_DRAW_MAX_RATIO * g.A, 30 * MM))
            sk.polys.append(_rect(x, x + e, fl_r, Fill.SECTION))
            sk.hdims.append(HDim(x, x + e, -1, f"{tx.lab('E')} ≈ {tx.length(e)}"))
            x += e
            if conn.face is FlangeFace.RF:
                rf_r = min(RAISED_FACE.get(size, 73.2) / 2 * MM, fl_r * 0.6)
                rf_t = (1.6 if cls <= 300 else 6.4) * MM
                sk.polys.append(_rect(x - rf_t, x, rf_r, Fill.SECTION))
            face = conn.face.value if conn.face else ""
            conn_text = f"{tx.lab('flanged')} {conn.size} {cls}# {face}".strip()
        conn_r = fl_r
    else:
        socket = conn.type is ConnectionType.SOCKET_WELD
        body_r = max(NPT_OD.get(size, 26.7 * MM) / 2 if socket else 19.05 * MM, ra * 1.1)
        body_len = SOCKET_BODY_LENGTH + lag
        sk.polys.append(_rect(0.0, body_len, body_r, Fill.SECTION))
        x = body_len
        conn_start = x - body_len / 3
        weld = body_r * 0.45
        for sgn in (1, -1):
            sk.polys.append(Poly(((x - weld, sgn * body_r), (x, sgn * body_r),
                                  (x, sgn * (body_r + weld))), Fill.PLAIN))
        conn_text = tx.lab("socket" if socket else "weld_in") + (f" {conn.size}"
                                                                   if conn.size else "")
        conn_r = body_r + weld

    conn_x = x - (x - conn_start) / 2
    x0 = x  # plano de conexión (cara de brida, fin de rosca o soldadura)
    u = g.U if g.U is not None else g.L
    tip = x0 + u

    # Vástago
    outline: list[tuple[float, float]] = [(x0, ra)]
    if g.profile is ShankProfile.STEPPED:
        sx = tip - g.Ls
        outline += [(sx, ra), (sx, rb)]
    outline += [(tip, rb), (tip, -rb)]
    if g.profile is ShankProfile.STEPPED:
        sx = tip - g.Ls
        outline += [(sx, -rb), (sx, -ra)]
    outline.append((x0, -ra))
    sk.polys.append(Poly(tuple(outline), Fill.SECTION))

    # Agujero: rosca del cabezal + agujero hasta el espesor de punta
    bore_end = tip - g.t
    sk.polys.append(_rect(0.0, HEAD_THREAD_DEPTH, head_r, Fill.BORE))
    sk.polys.append(_rect(HEAD_THREAD_DEPTH * 0.9, bore_end, rd, Fill.BORE))
    for i in range(6):
        xi = i * HEAD_THREAD_DEPTH / 6
        for sgn in (1, -1):
            sk.strokes.append(Stroke((xi, sgn * head_r), (xi + HEAD_THREAD_DEPTH / 12,
                                                          sgn * head_r * 0.9), "thread"))
    sk.strokes.append(Stroke((-3 * MM, 0.0), (tip + 3 * MM, 0.0), "center"))

    # Cotas horizontales
    sk.hdims.append(HDim(x0, tip, 1, f"{tx.lab('U')} = {tx.length(u)}"))
    sk.hdims.append(HDim(bore_end, tip, 2, f"{tx.lab('t')} = {tx.length(g.t)}",
                         outside=True))
    sk.hdims.append(HDim(0.0, bore_end, 2, f"{tx.lab('bore')} = {tx.length(bore_end)}"))
    sk.hdims.append(HDim(0.0, tip, 3, f"{tx.lab('total')} = {tx.length(tip)}"))
    top = -3 if lag > 0 else -2
    if g.profile is ShankProfile.STEPPED:
        sk.hdims.append(HDim(tip - g.Ls, tip, top, f"{tx.lab('Ls')} = {tx.length(g.Ls)}"))
        top -= 1
    if abs(g.L - u) > 1e-6:
        sk.hdims.append(HDim(tip - g.L, tip, top, f"{tx.lab('L')} = {tx.length(g.L)}"))
        top -= 1
    if g.L0 > 0:
        sk.hdims.append(HDim(tip - g.L, tip - g.L + g.L0, top,
                             f"{tx.lab('L0')} = {tx.length(g.L0)}"))

    # Diámetros
    gap = max(rb * 1.4, 3 * MM)
    sk.vdims.append(VDim(tip + gap, rb, f"{tx.lab('B')} = {tx.diameter(g.B)}"))
    top_dims = [d.row for d in sk.hdims if d.row < 0]
    first_note = min(top_dims, default=0) - 1
    sk.leaders.append(Leader(x0 + (tip - x0) * 0.12, ra, first_note,
                             f"{tx.lab('A')} = {tx.diameter(g.A)}"))
    sk.leaders.append(Leader(x0 + (bore_end - x0) * 0.55, rd * 0.5, first_note - 1,
                             f"{tx.lab('d')} = {tx.diameter(g.d)}"))
    sk.leaders.append(Leader(HEAD_THREAD_DEPTH * 0.5, head_r, first_note - 2, tx.lab("head")))
    sk.leaders.append(Leader(conn_x, conn_r * 0.95, first_note - 3, conn_text))

    # Pared interna de la tubería (si hay tobera, a continuación de ella)
    wall_x = x0 + inp.pipe.nozzle_length
    reach = max(ra, conn_r) * 1.1
    if wall_x < tip:
        sk.strokes.append(Stroke((wall_x, -reach), (wall_x, reach), "dashed"))
        far = wall_x + inp.pipe.inner_diameter
        if far <= tip * 1.25:
            sk.strokes.append(Stroke((far, -reach), (far, reach), "dashed"))

    sk.x_min = -3 * MM
    sk.x_max = tip + gap + 2 * MM
    sk.half_height = max(max(abs(y) for p in sk.polys for _, y in p.points), rb + 2 * MM)
    return sk


# --- Renderizado genérico --------------------------------------------------------------
class Painter:
    """Interfaz mínima que implementan Qt y ReportLab (dispositivo, y hacia abajo)."""

    def line(self, x1: float, y1: float, x2: float, y2: float, *, width: float = 0.8,
             dash: bool = False, color: str = "ink") -> None:
        """Segmento."""
        raise NotImplementedError

    def polygon(self, pts: Sequence[tuple[float, float]], *, fill: str,
                stroke: bool = True) -> None:
        """Polígono relleno (``fill``: metal | bore | plain)."""
        raise NotImplementedError

    def text(self, x: float, y: float, text: str, *, anchor: str = "start") -> None:
        """Texto con la línea base en y (``anchor``: start | middle | end)."""
        raise NotImplementedError

    def text_width(self, text: str) -> float:
        """Ancho aproximado del texto."""
        raise NotImplementedError


ARROW: Final = 5.0
HATCH_PX: Final = 4.5


def render(sk: Sketch, p: Painter, width: float, height: float, *, row_h: float = 14.0,
           margin: float = 8.0) -> None:
    """Dibuja ``sk`` ajustado al rectángulo (0, 0, width, height)."""
    below_notes = sorted({n.slot for n in sk.leaders if n.slot > 0})
    rows_below = sk.rows_below + len(below_notes)
    rows_above = sk.rows_above
    avail_h = height - 2 * margin - (rows_below + rows_above + 0.6) * row_h
    longest_v = max((p.text_width(v.text) for v in sk.vdims), default=0.0)
    avail_w = width - 2 * margin - longest_v - 6
    span_x = sk.x_max - sk.x_min
    s = max(min(avail_w / span_x, avail_h / (2 * sk.half_height)), 1e-6)
    ox = margin - sk.x_min * s
    used = (rows_below + rows_above + 0.6) * row_h + 2 * sk.half_height * s
    slack = max(height - 2 * margin - used, 0.0) / 2
    cy = margin + slack + rows_above * row_h + 0.3 * row_h + sk.half_height * s

    def X(x: float) -> float:  # noqa: N802 - transformación
        return ox + x * s

    def Y(y: float) -> float:  # noqa: N802
        return cy - y * s

    for poly in sk.polys:
        pts = [(X(x), Y(y)) for x, y in poly.points]
        if poly.fill is Fill.BORE:
            p.polygon(pts, fill="bore", stroke=True)
            continue
        p.polygon(pts, fill="metal" if poly.fill is Fill.SECTION else "plain")
        if poly.fill is Fill.SECTION:
            for (ax, ay), (bx, by) in hatch_segments(pts, HATCH_PX):
                p.line(ax, ay, bx, by, width=0.35, color="hatch")
    for st in sk.strokes:
        p.line(X(st.p1[0]), Y(st.p1[1]), X(st.p2[0]), Y(st.p2[1]),
               width=0.4 if st.style in ("thread", "center") else 0.8,
               dash=st.style in ("dashed", "center"),
               color="pipe" if st.style == "dashed" else "ink")

    y_bottom = Y(-sk.half_height)
    y_top = Y(sk.half_height)

    def hdim(d: HDim) -> None:
        y = y_bottom + d.row * row_h - 3 if d.row > 0 else y_top + d.row * row_h + 6
        x1, x2 = X(d.x1), X(d.x2)
        edge = y_bottom if d.row > 0 else y_top
        for xe in (x1, x2):
            p.line(xe, edge + (2 if d.row > 0 else -2), xe, y + (3 if d.row > 0 else -3),
                   width=0.35)
        p.line(x1, y, x2, y, width=0.5)
        if x2 - x1 > 2.5 * ARROW:
            _arrow(p, x1, y, 1)
            _arrow(p, x2, y, -1)
        else:  # cota corta: flechas por fuera
            p.line(x1 - 2 * ARROW, y, x1, y, width=0.5)
            p.line(x2, y, x2 + 2 * ARROW, y, width=0.5)
            _arrow(p, x1, y, -1)
            _arrow(p, x2, y, 1)
        tw = p.text_width(d.text)
        if d.outside:
            p.text(x2 + 2 * ARROW + 3, y + 3, d.text)
            return
        xc = min(max((x1 + x2) / 2, margin + tw / 2), width - margin - tw / 2)
        p.text(xc, y - 2, d.text, anchor="middle")

    for d in sk.hdims:
        hdim(d)
    for v in sk.vdims:
        x = X(v.x)
        y1, y2 = Y(v.half), Y(-v.half)
        p.line(x - 6, y1, x + 2, y1, width=0.35)
        p.line(x - 6, y2, x + 2, y2, width=0.35)
        p.line(x, y1 - 10, x, y2 + 10, width=0.5)
        _arrow_v(p, x, y1, -1)
        _arrow_v(p, x, y2, 1)
        p.text(x + 4, (y1 + y2) / 2 + 3, v.text)
    rank = {slot: i for i, slot in enumerate(below_notes)}
    for n in sk.leaders:
        ax, ay = X(n.x), Y(n.y)
        if n.slot < 0:
            ty = y_top + n.slot * row_h + 6
            p.line(ax, ay, ax + 10, ty + 2, width=0.4)
            p.line(ax + 10, ty + 2, ax + 14 + p.text_width(n.text), ty + 2, width=0.4)
            p.text(ax + 12, ty, n.text)
        else:
            ty = y_bottom + (sk.rows_below + rank[n.slot] + 1) * row_h - 3
            tx = max(ax - 10, margin + p.text_width(n.text))
            p.line(ax, ay, tx, ty - 2, width=0.4)
            p.line(tx, ty - 2, tx - p.text_width(n.text) - 2, ty - 2, width=0.4)
            p.text(tx - 1, ty - 4, n.text, anchor="end")


def _arrow(p: Painter, x: float, y: float, sgn: int) -> None:
    p.polygon([(x, y), (x + ARROW * sgn, y - 1.8), (x + ARROW * sgn, y + 1.8)], fill="ink",
              stroke=False)


def _arrow_v(p: Painter, x: float, y: float, sgn: int) -> None:
    p.polygon([(x, y), (x - 1.8, y + ARROW * sgn), (x + 1.8, y + ARROW * sgn)], fill="ink",
              stroke=False)
