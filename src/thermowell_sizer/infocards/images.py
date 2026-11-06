"""Imágenes de las fichas de ayuda: esquemas y curvas (matplotlib, PNG en memoria).

Todo se dibuja con redacción y trazos propios; no se reproducen figuras de normas.
"""

from __future__ import annotations

import io
import math
from collections.abc import Callable
from functools import lru_cache

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Polygon, Rectangle

INK = "#20242a"
METAL = "#dfe4ea"
ACCENT = "#c0392b"
PIPE = "#3f6fb5"
DPI = 110


def _png(fig: Figure) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return buf.getvalue()


def _dim(ax: Axes, x1: float, x2: float, y: float, text: str, *, color: str = INK,
         vertical: bool = False, side: str = "right", rotate: bool = False) -> None:
    style = {"arrowstyle": "<|-|>", "color": color, "lw": 0.9, "shrinkA": 0, "shrinkB": 0}
    if vertical:
        ax.annotate("", (y, x1), (y, x2), arrowprops=style)
        off = 0.15 if side == "right" else -0.15
        ax.text(y + off, (x1 + x2) / 2, text, color=color, va="center",
                ha="left" if side == "right" else "right", fontsize=8,
                rotation=90 if rotate else 0)
    else:
        ax.annotate("", (x1, y), (x2, y), arrowprops=style)
        ax.text((x1 + x2) / 2, y + 0.12, text, color=color, ha="center", va="bottom",
                fontsize=8)


_MOUNT_TEXT = {
    "es": {"title": "Montaje en la línea", "flange": "Brida de montaje",
           "well": "Brida del termopozo", "pipe": "Tubería", "hs": "Hs", "wall": "pared",
           "imm": "inmersión", "U": "U = L (desde la cara de la brida)", "head": "Cabezal",
           "flow": "flujo", "id": "D interno"},
    "en": {"title": "Line mounting", "flange": "Mounting flange", "well": "Thermowell flange",
           "pipe": "Pipe", "hs": "Hs", "wall": "wall", "imm": "immersion",
           "U": "U = L (from the flange face)", "head": "Head", "flow": "flow",
           "id": "inside D"},
}


@lru_cache(maxsize=4)
def mount_diagram(lang: str = "es") -> bytes:
    """Corte de la instalación: Hs, pared, inmersión y U."""
    tx = _MOUNT_TEXT["es" if lang == "es" else "en"]
    fig, ax = plt.subplots(figsize=(4.6, 5.0))
    ax.set_aspect("equal")
    ax.axis("off")
    # tubería (corte transversal parcial): pared superior e inferior
    wall, d_in = 0.5, 4.0
    top_out, top_in = 0.0, -wall
    bot_in, bot_out = top_in - d_in, top_in - d_in - wall
    for y0, y1 in ((top_in, top_out), (bot_out, bot_in)):
        ax.add_patch(Rectangle((-2.4, y0), 5.6, y1 - y0, fc=METAL, ec=INK, hatch="////", lw=0.8))
    ax.text(-2.3, bot_in + 0.25, f"{tx['pipe']} → {tx['flow']}", fontsize=8, color=PIPE,
            va="bottom")
    # niple y brida de montaje
    hs = 2.2
    ax.add_patch(Rectangle((-0.75, top_out), 1.5, hs - 0.35, fc=METAL, ec=INK, lw=0.8))
    ax.add_patch(Rectangle((-1.5, hs - 0.35), 3.0, 0.35, fc=METAL, ec=INK, lw=0.8))
    ax.text(1.6, hs - 0.2, tx["flange"], fontsize=8, va="center")
    # brida del termopozo y cabezal
    ax.add_patch(Rectangle((-1.5, hs), 3.0, 0.35, fc="#c9d3de", ec=INK, lw=0.8))
    ax.text(1.6, hs + 0.2, tx["well"], fontsize=8, va="center")
    ax.add_patch(Rectangle((-0.35, hs + 0.35), 0.7, 0.8, fc="#c9d3de", ec=INK, lw=0.8))
    ax.text(0.45, hs + 0.85, tx["head"], fontsize=8)
    # vástago
    tip = bot_in + 1.4
    ax.add_patch(Polygon([(-0.32, hs), (0.32, hs), (0.22, tip), (-0.22, tip)], fc="#c9d3de",
                         ec=INK, lw=0.9))
    ax.plot([0, 0], [hs + 1.2, tip - 0.2], color=INK, lw=0.5, ls="-.")
    # cotas
    x = -2.7
    _dim(ax, top_out, hs, x, tx["hs"], color=ACCENT, vertical=True, side="left")
    _dim(ax, top_in, top_out, x, tx["wall"], vertical=True, side="left")
    _dim(ax, tip, top_in, x, tx["imm"], vertical=True, side="left")
    _dim(ax, tip, hs, 3.4, tx["U"], color=ACCENT, vertical=True, rotate=True)
    _dim(ax, bot_in, top_in, 1.4, tx["id"], vertical=True)
    ax.set_xlim(-4.4, 4.2)
    ax.set_ylim(bot_out - 0.3, hs + 1.4)
    ax.set_title(tx["title"], fontsize=10)
    return _png(fig)


def curve_png(xs: list[float], series: list[tuple[str, list[float], str]], *, xlabel: str,
              ylabel: str, title: str, marks: list[tuple[float, float, str]] | None = None,
              hlines: list[tuple[float, str]] | None = None, logx: bool = False,
              logy: bool = False, ylim: tuple[float, float] | None = None) -> bytes:
    """Curva genérica con series, puntos marcados y líneas de límite."""
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    for label, ys, color in series:
        ax.plot(xs, ys, label=label, color=color, lw=1.6)
    for y, label in hlines or []:
        ax.axhline(y, color=ACCENT, ls="--", lw=1.0)
        ax.text(xs[0], y, f" {label}", color=ACCENT, fontsize=7, va="bottom")
    for x, y, label in marks or []:
        ax.plot([x], [y], "o", color=ACCENT)
        ax.annotate(label, (x, y), textcoords="offset points", xytext=(6, 6), fontsize=7,
                    color=ACCENT)
    if logx:
        ax.set_xscale("log")
    if logy:
        ax.set_yscale("log")
    if ylim is not None:
        ax.set_ylim(*ylim)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.set_title(title, fontsize=9)
    ax.tick_params(labelsize=7)
    ax.grid(alpha=0.3)
    if len(series) > 1:
        ax.legend(fontsize=7)
    return _png(fig)


def sample(fn: Callable[[float], float], lo: float, hi: float, n: int = 120,
           *, log: bool = False) -> tuple[list[float], list[float]]:
    """Muestra una función en [lo, hi] (lineal o logarítmica)."""
    if log:
        xs = [lo * (hi / lo) ** (i / (n - 1)) for i in range(n)]
    else:
        xs = [lo + (hi - lo) * i / (n - 1) for i in range(n)]
    ys = []
    for x in xs:
        try:
            ys.append(fn(x))
        except (ValueError, ZeroDivisionError, OverflowError):
            ys.append(math.nan)
    return xs, ys


_TW_TEXT = {
    "es": {"L": "L · largo no soportado", "U": "U · inserción", "A": "Ø A raíz",
           "B": "Ø B punta", "d": "Ø d agujero", "t": "t punta", "b": "b radio",
           "Ls": "Ls escalón", "bs": "bs radio escalón", "T_lag": "T lag",
           "L0": "L0 zona protegida", "ca": "sobreespesor", "flow": "flujo",
           "flange": "brida", "title": "Termopozo: cota resaltada"},
    "en": {"L": "L · unsupported length", "U": "U · insertion", "A": "Ø A root",
           "B": "Ø B tip", "d": "Ø d bore", "t": "t tip", "b": "b fillet",
           "Ls": "Ls step", "bs": "bs step fillet", "T_lag": "T lag",
           "L0": "L0 shielded zone", "ca": "corrosion allowance", "flow": "flow",
           "flange": "flange", "title": "Thermowell: highlighted dimension"},
}
THERMOWELL_DIMENSIONS = ("L", "U", "A", "B", "d", "t", "b", "Ls", "bs", "T_lag", "L0", "ca")


@lru_cache(maxsize=64)
def thermowell_diagram(highlight: str = "", lang: str = "es") -> bytes:
    """Termopozo cónico esquemático con todas las cotas y una resaltada en rojo."""
    tx = _TW_TEXT["es" if lang == "es" else "en"]
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    ax.set_aspect("equal")
    ax.axis("off")

    def col(key: str) -> str:
        return ACCENT if key == highlight else "#8a929c"

    # brida y cuerpo (eje horizontal; la punta a la derecha)
    ax.add_patch(Rectangle((-0.6, -1.4), 0.6, 2.8, fc=METAL, ec=INK, lw=0.8))
    ax.text(-0.3, 1.55, tx["flange"], ha="center", fontsize=7)
    lag = 0.8
    ax.add_patch(Rectangle((0, -0.55), lag, 1.1, fc=METAL, ec=INK, lw=0.8))
    root, tip, length = 0.5, 0.33, 7.0
    x0 = lag
    ax.add_patch(Polygon([(x0, root), (x0 + length, tip), (x0 + length, -tip), (x0, -root)],
                         fc="#c9d3de", ec=INK, lw=0.9))
    # agujero
    bore = 0.13
    ax.add_patch(Rectangle((-0.6, -bore), 0.6 + x0 + length - 0.35, 2 * bore, fc="white",
                           ec=INK, lw=0.6, ls="--"))
    # zona protegida (dentro de la brida de montaje) y sobreespesor
    ax.add_patch(Rectangle((x0, root + 0.05), 1.4, 0.12, fc=col("L0"), ec="none", alpha=0.35))
    ax.add_patch(Rectangle((x0 + 2.0, -root - 0.17), length - 2.0, 0.08, fc=col("ca"),
                           ec="none", alpha=0.5))
    ax.text(x0 + 4.5, -root - 0.45, tx["ca"], color=col("ca"), fontsize=7, ha="center")
    # flujo
    ax.annotate("", (x0 + 5.6, -1.9), (x0 + 5.6, -1.3),
                arrowprops={"arrowstyle": "<-", "color": PIPE, "lw": 1.2})
    ax.text(x0 + 5.75, -1.75, tx["flow"], color=PIPE, fontsize=7)
    # cotas horizontales
    _dim(ax, x0, x0 + length, 1.25, tx["L"], color=col("L"))
    _dim(ax, 0, x0 + length, 1.85, tx["U"], color=col("U"))
    _dim(ax, 0, x0, -0.95, tx["T_lag"], color=col("T_lag"))
    _dim(ax, x0, x0 + 1.4, 0.75, tx["L0"], color=col("L0"))
    _dim(ax, x0 + length - 0.35, x0 + length, 0.6, tx["t"], color=col("t"))
    _dim(ax, x0 + 3.0, x0 + 4.2, -1.35, tx["Ls"], color=col("Ls"))
    # cotas verticales (diámetros)
    _dim(ax, -root, root, x0 + 0.25, tx["A"], color=col("A"), vertical=True)
    _dim(ax, -tip, tip, x0 + length + 0.3, tx["B"], color=col("B"), vertical=True)
    _dim(ax, -bore, bore, x0 + 2.4, tx["d"], color=col("d"), vertical=True)
    ax.text(x0 + 0.15, -root - 0.3, tx["b"], color=col("b"), fontsize=7)
    ax.text(x0 + 4.3, -1.3, tx["bs"], color=col("bs"), fontsize=7)
    ax.set_xlim(-0.9, x0 + length + 2.4)
    ax.set_ylim(-2.1, 2.4)
    ax.set_title(tx["title"], fontsize=9)
    return _png(fig)


_ORIENT_TEXT = {
    "es": ("Perpendicular", "Inclinado", "En codo", "flujo"),
    "en": ("Perpendicular", "Inclined", "In an elbow", "flow"),
}


@lru_cache(maxsize=2)
def orientation_diagram(lang: str = "es") -> bytes:
    """Esquemas de instalación: perpendicular, inclinado y en codo."""
    names = _ORIENT_TEXT["es" if lang == "es" else "en"]
    fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.3))
    for ax, name in zip(axes, names[:3], strict=True):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(name, fontsize=8)
    # perpendicular
    a = axes[0]
    a.add_patch(Rectangle((-2, -1), 4, 2, fc="#eef3fa", ec=INK, lw=0.8))
    a.add_patch(Polygon([(-0.12, 1.6), (0.12, 1.6), (0.08, -0.2), (-0.08, -0.2)],
                        fc="#c9d3de", ec=INK))
    a.annotate("", (1.6, -0.6), (-1.6, -0.6), arrowprops={"arrowstyle": "->", "color": PIPE})
    a.set_xlim(-2.2, 2.2)
    a.set_ylim(-1.2, 1.8)
    # inclinado (contra el flujo)
    a = axes[1]
    a.add_patch(Rectangle((-2, -1), 4, 2, fc="#eef3fa", ec=INK, lw=0.8))
    a.add_patch(Polygon([(0.9, 1.6), (1.1, 1.5), (0.1, -0.3), (-0.05, -0.2)],
                        fc="#c9d3de", ec=INK))
    a.annotate("", (1.6, -0.6), (-1.6, -0.6), arrowprops={"arrowstyle": "->", "color": PIPE})
    a.set_xlim(-2.2, 2.2)
    a.set_ylim(-1.2, 1.8)
    # en codo (punta enfrentando el flujo)
    a = axes[2]
    a.add_patch(Rectangle((-2, -1), 3, 2, fc="#eef3fa", ec=INK, lw=0.8))
    a.add_patch(Rectangle((1, -1), 1.0, 2.8, fc="#eef3fa", ec=INK, lw=0.8))
    a.add_patch(Polygon([(2.3, 0.12), (2.3, -0.12), (-0.2, -0.08), (-0.2, 0.08)],
                        fc="#c9d3de", ec=INK))
    a.annotate("", (0.6, 0.6), (-1.6, 0.6), arrowprops={"arrowstyle": "->", "color": PIPE})
    a.text(-1.6, 0.7, names[3], fontsize=7, color=PIPE)
    a.set_xlim(-2.2, 2.6)
    a.set_ylim(-1.2, 1.9)
    return _png(fig)


_CONN_TEXT = {
    "es": ("Roscada", "Bridada", "Para soldar", "Socket weld", "Van Stone", "Sanitaria"),
    "en": ("Threaded", "Flanged", "Weld-in", "Socket weld", "Van Stone", "Sanitary"),
}


@lru_cache(maxsize=2)
def connection_diagram(lang: str = "es") -> bytes:
    """Esquema de los tipos de conexión al proceso."""
    names = _CONN_TEXT["es" if lang == "es" else "en"]
    fig, axes = plt.subplots(1, 6, figsize=(7.2, 2.0))
    for ax, name in zip(axes, names, strict=True):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(name, fontsize=7)
        ax.add_patch(Polygon([(-0.25, 0), (0.25, 0), (0.15, -2.4), (-0.15, -2.4)],
                             fc="#c9d3de", ec=INK, lw=0.7))
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-2.6, 1.2)
    # roscada: dientes
    for i in range(6):
        y = -0.1 - 0.12 * i
        axes[0].plot([-0.45, -0.3, -0.45], [y, y - 0.06, y - 0.12], color=INK, lw=0.6)
        axes[0].plot([0.45, 0.3, 0.45], [y, y - 0.06, y - 0.12], color=INK, lw=0.6)
    axes[0].add_patch(Rectangle((-0.5, 0), 1.0, 0.4, fc=METAL, ec=INK, lw=0.7))
    # bridada
    axes[1].add_patch(Rectangle((-1.0, 0), 2.0, 0.3, fc=METAL, ec=INK, lw=0.7))
    axes[1].add_patch(Rectangle((-0.35, 0.3), 0.7, 0.5, fc=METAL, ec=INK, lw=0.7))
    # para soldar
    axes[2].add_patch(Rectangle((-0.6, -0.2), 1.2, 0.3, fc="#b0b8c2", ec=INK, lw=0.7))
    axes[2].plot([-0.6, -0.8], [-0.2, 0.1], color=ACCENT, lw=1.2)
    axes[2].plot([0.6, 0.8], [-0.2, 0.1], color=ACCENT, lw=1.2)
    # socket weld
    axes[3].add_patch(Rectangle((-0.55, -0.6), 1.1, 0.9, fc=METAL, ec=INK, lw=0.7))
    axes[3].plot([-0.55, -0.7], [0.3, 0.45], color=ACCENT, lw=1.2)
    axes[3].plot([0.55, 0.7], [0.3, 0.45], color=ACCENT, lw=1.2)
    # Van Stone: brida loca
    axes[4].add_patch(Rectangle((-0.5, 0), 1.0, 0.2, fc="#b0b8c2", ec=INK, lw=0.7))
    axes[4].add_patch(Rectangle((-1.0, 0.2), 2.0, 0.3, fc=METAL, ec=INK, lw=0.7))
    # sanitaria (clamp)
    axes[5].add_patch(Polygon([(-0.7, 0), (0.7, 0), (0.5, 0.35), (-0.5, 0.35)], fc=METAL,
                              ec=INK, lw=0.7))
    return _png(fig)
