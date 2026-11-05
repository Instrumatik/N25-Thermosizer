"""Gráficas de sensibilidad como PNG para los reportes."""

from __future__ import annotations

import io

import matplotlib

matplotlib.use("Agg")
import numpy as np
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

from thermowell_sizer.core.analysis.sensitivity import (
    max_allowable_velocity,
    velocity_sweep,
)
from thermowell_sizer.core.ptc19_3.verify import resolve_velocity
from thermowell_sizer.core.units import QuantityKind, unit_for
from thermowell_sizer.reports.common import Fmt
from thermowell_sizer.services import Evaluation

POINTS = 50
DPI = 160


def sensitivity_png(ev: Evaluation, fmt: Fmt) -> bytes | None:
    """Frecuencias y esfuerzo dinámico frente a la velocidad, con los casos marcados."""
    if ev.material is None or ev.result is None:
        return None
    inp = ev.input
    rho = inp.process.properties.density
    v_cases = [resolve_velocity(c, rho, inp.pipe.inner_diameter) for c in inp.process.flow_cases]
    v_top = max(max(v_cases), 1.0) * 2
    vmax = max_allowable_velocity(inp, ev.material, ev.options, samples=120)
    if vmax is not None:
        v_top = max(v_top, vmax * 1.3)
    vs = np.linspace(v_top / POINTS, v_top, POINTS)
    pts = velocity_sweep(inp, ev.material, list(vs), ev.options)
    vu = unit_for(QuantityKind.VELOCITY, fmt.units)
    su = unit_for(QuantityKind.STRESS, fmt.units)
    x = [vu.from_si(p.x) for p in pts]
    fig = Figure(figsize=(7.2, 3.0), layout="constrained")
    ax1, ax2 = fig.subplots(1, 2)
    ax1.plot(x, [p.fs for p in pts], color="#2a6fdb", label="f_s")
    ax1.plot(x, [p.fnc for p in pts], color="#8a8f98", ls="-.", label="f_n,c")
    ax1.plot(x, [p.fs_limit if p.fs_limit is not None else np.nan for p in pts],
             color="#d0342c", ls="--", label="lím. f_s" if fmt.lang.value == "es" else "f_s limit")
    ax1.set_ylabel("Hz")
    ax2.plot(x, [su.from_si(p.dynamic_stress) for p in pts], color="#2a6fdb", label="S_o")
    ax2.plot(x, [su.from_si(p.dynamic_allowable) for p in pts], color="#d0342c", ls="--",
             label="S_adm" if fmt.lang.value == "es" else "S_allow")
    ax2.set_yscale("log")
    ax2.set_ylabel(su.symbol)
    tick = FuncFormatter(lambda v, _p: fmt.num(v))
    for ax in (ax1, ax2):
        for v in v_cases:
            ax.axvline(vu.from_si(v), color="#e0a100", ls=":", lw=1.4)
        if vmax is not None:
            ax.axvline(vu.from_si(vmax), color="#d0342c", lw=0.8, alpha=0.5)
        ax.set_xlabel(f"V [{vu.symbol}]")
        ax.xaxis.set_major_formatter(tick)
        ax.grid(alpha=0.25)
        ax.legend(fontsize=7)
    ax1.yaxis.set_major_formatter(tick)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=DPI)
    return buf.getvalue()
