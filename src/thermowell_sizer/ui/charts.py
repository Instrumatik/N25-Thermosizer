"""Gráficas de sensibilidad (matplotlib embebido en Qt)."""

from __future__ import annotations

import numpy as np
from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from thermowell_sizer.core.analysis.sensitivity import (
    SweepPoint,
    length_sweep,
    max_allowable_velocity,
    velocity_sweep,
)
from thermowell_sizer.core.ptc19_3.verify import case_velocity
from thermowell_sizer.core.units import QuantityKind, unit_for
from thermowell_sizer.services import Evaluation
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.text import t
from thermowell_sizer.ui.widgets import fmt, fmt_quantity

SWEEP_POINTS = 60
VELOCITY_SPAN = 2.0
"""El barrido llega al menos hasta el doble de la velocidad máxima del tag..."""
VMAX_SPAN = 1.3
"""...y un 30 % por encima de la velocidad máxima admisible, para ver el cruce."""
LENGTH_SPAN = (0.4, 1.6)
COLORS = {"fs": "#2a6fdb", "limit": "#d0342c", "fnc": "#8a8f98", "allow": "#d0342c",
          "dyn": "#2a6fdb", "case": "#e0a100"}


class SensitivityChart(QWidget):
    """Barridos en velocidad y longitud con el punto de operación marcado."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.figure = Figure(figsize=(6, 4), layout="constrained")
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.mode = QComboBox()
        self.mode.addItem(t("chart.freq"), "freq")
        self.mode.addItem(t("chart.stress"), "stress")
        self.mode.addItem(t("chart.length"), "length")
        self.mode.currentIndexChanged.connect(self.redraw)
        self.lbl_vmax = QLabel()
        top = QHBoxLayout()
        top.addWidget(self.mode)
        top.addStretch(1)
        top.addWidget(self.lbl_vmax)
        lay = QVBoxLayout(self)
        lay.addLayout(top)
        lay.addWidget(self.canvas, 1)
        self.evaluation: Evaluation | None = None
        self.vmax: float | None = None

    def set_evaluation(self, ev: Evaluation | None) -> None:
        """Guarda la evaluación y redibuja."""
        self.evaluation = ev
        self.vmax = None
        self.lbl_vmax.setText("")
        if ev is not None and ev.material is not None:
            vmax = max_allowable_velocity(ev.input, ev.material, ev.options, samples=120)
            self.vmax = vmax
            text = fmt_quantity(vmax, QuantityKind.VELOCITY) if vmax is not None else "> 200 m/s"
            self.lbl_vmax.setText(f"{t('res.max_velocity')}: {text}")
        self.redraw()

    def _style(self) -> tuple[str, str]:
        return ("#1e2128", "#e6e8eb") if STATE.dark else ("#ffffff", "#20242a")

    def redraw(self) -> None:
        """Vuelve a calcular el barrido elegido y dibuja."""
        bg, fg = self._style()
        self.figure.clear()
        self.figure.set_facecolor(bg)
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(bg)
        for spine in ax.spines.values():
            spine.set_color(fg)
        ax.tick_params(colors=fg)
        ev = self.evaluation
        if ev is None or ev.material is None or ev.result is None:
            self.canvas.draw_idle()
            return
        inp = ev.input
        velocities_now = [case_velocity(inp, c)
                          for c in inp.process.flow_cases]
        v_case = max(velocities_now)
        mode = self.mode.currentData()
        vel_unit = unit_for(QuantityKind.VELOCITY, STATE.units)
        if mode == "length":
            g = inp.thermowell.geometry
            xs = np.linspace(g.L * LENGTH_SPAN[0], g.L * LENGTH_SPAN[1], SWEEP_POINTS // 2)
            pts = length_sweep(inp, ev.material, list(xs), v_case, ev.options)
            len_unit = unit_for(QuantityKind.LENGTH, STATE.units)
            x = [len_unit.from_si(p.x) for p in pts]
            self._plot_frequency(ax, x, pts)
            ax.axvline(len_unit.from_si(g.L), color=COLORS["case"], ls=":", lw=1.5)
            ax.set_xlabel(f"{t('chart.length')} [{len_unit.symbol}]", color=fg)
        else:
            v_top = max(v_case, 1.0) * VELOCITY_SPAN
            if self.vmax is not None:
                v_top = max(v_top, self.vmax * VMAX_SPAN)
            vs = np.linspace(v_top / SWEEP_POINTS, v_top, SWEEP_POINTS)
            pts = velocity_sweep(inp, ev.material, list(vs), ev.options)
            x = [vel_unit.from_si(p.x) for p in pts]
            if mode == "freq":
                self._plot_frequency(ax, x, pts)
            else:
                st = unit_for(QuantityKind.STRESS, STATE.units)
                ax.plot(x, [st.from_si(p.dynamic_stress) for p in pts], color=COLORS["dyn"],
                        label="S_o")
                ax.plot(x, [st.from_si(p.dynamic_allowable) for p in pts],
                        color=COLORS["allow"], ls="--", label=t("chart.allowable"))
                ax.set_ylabel(f"[{st.symbol}]", color=fg)
                ax.set_yscale("log")
            for v in velocities_now:
                ax.axvline(vel_unit.from_si(v), color=COLORS["case"], ls=":", lw=1.5)
            ax.set_xlabel(f"{t('chart.velocity')} [{vel_unit.symbol}]", color=fg)
        tick = FuncFormatter(lambda v, _pos: fmt(v))
        ax.xaxis.set_major_formatter(tick)
        if ax.get_yscale() == "linear":
            ax.yaxis.set_major_formatter(tick)
        legend = ax.legend(facecolor=bg, edgecolor=fg)
        for text in legend.get_texts():
            text.set_color(fg)
        ax.grid(alpha=0.25)
        self.canvas.draw_idle()

    @staticmethod
    def _plot_frequency(ax: Axes, x: list[float], pts: list[SweepPoint]) -> None:
        ax.plot(x, [p.fs for p in pts], color=COLORS["fs"], label="f_s")
        ax.plot(x, [p.fnc for p in pts], color=COLORS["fnc"], ls="-.",
                label="f_n,c")
        ax.plot(x, [p.fs_limit if p.fs_limit is not None else np.nan for p in pts],
                color=COLORS["limit"], ls="--", label=t("chart.limit"))
        ax.set_ylabel("[Hz]")
