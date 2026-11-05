"""Ecuaciones LaTeX de la traza como imágenes PNG (mathtext de matplotlib)."""

from __future__ import annotations

import io
import re
from functools import lru_cache

import matplotlib

matplotlib.use("Agg")
from matplotlib import mathtext
from matplotlib.font_manager import FontProperties

RENDER_DPI = 200
FONT_SIZE = 10
_TEXT = re.compile(r"\\text\{([^}]*)\}")


def _mathtext_friendly(expr: str) -> str:
    """Adapta LaTeX a lo que entiende mathtext."""
    expr = _TEXT.sub(lambda m: r"\mathrm{" + m.group(1).replace(" ", r"\ ") + "}", expr)
    expr = expr.replace(r"\tfrac12", r"\frac{1}{2}").replace(r"\tfrac", r"\frac")
    return expr.replace(r"\left", "").replace(r"\right", "").replace(r"\dot m", r"\dot{m}")


def plain(expr: str) -> str:
    """Versión en texto plano, por si la imagen no puede generarse."""
    text = _TEXT.sub(lambda m: m.group(1), expr)
    for a, b in ((r"\left", ""), (r"\right", ""), (r"\,", " "), (r"\ ", " "), (r"\cdot", "·"),
                 (r"\sqrt", "√"), (r"\pi", "π"), (r"\rho", "ρ"), (r"\mu", "μ"),
                 (r"\zeta", "ζ"), (r"\min", "min"), (r"\max", "max"), (r"\frac", "frac"),
                 ("{", "("), ("}", ")"), ("\\", "")):
        text = text.replace(a, b)
    return text


@lru_cache(maxsize=512)
def render_png(expr: str) -> bytes | None:
    """PNG de la expresión, o ``None`` si mathtext no la soporta."""
    buf = io.BytesIO()
    try:
        mathtext.math_to_image(f"${_mathtext_friendly(expr)}$", buf, dpi=RENDER_DPI,
                               format="png", prop=FontProperties(size=FONT_SIZE))
    except (ValueError, RuntimeError):
        return None
    return buf.getvalue()
