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
              hlines: list[tuple[float, str]] | None = None, logx: bool = False) -> bytes:
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
