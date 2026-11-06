"""Curvas de las fichas, calculadas con los datos del tag actual."""

from __future__ import annotations

from collections.abc import Callable

from thermowell_sizer.core.advisories import EROSION_WATCH_RATIO, erosional_velocity
from thermowell_sizer.core.analysis.sensitivity import length_sweep, velocity_sweep
from thermowell_sizer.core.ptc19_3.flow import strouhal_correlation
from thermowell_sizer.core.ptc19_3.frequency_limits import magnification
from thermowell_sizer.infocards.images import curve_png, sample
from thermowell_sizer.services import Evaluation

CURVE_IDS = ("fs_v", "stress_v", "steady_v", "fn_L", "st_re", "fm_r", "ve_rho")

_T = {
    "fs_v": ("Frecuencia de estela vs. velocidad", "Wake frequency vs velocity"),
    "stress_v": ("Esfuerzo dinámico vs. velocidad", "Dynamic stress vs velocity"),
    "steady_v": ("Esfuerzo estacionario (von Mises) vs. velocidad",
                 "Steady stress (von Mises) vs velocity"),
    "fn_L": ("Frecuencia natural instalada vs. largo L", "Installed natural frequency vs L"),
    "st_re": ("Número de Strouhal vs. Reynolds", "Strouhal number vs Reynolds"),
    "fm_r": ("Factor de amplificación vs. relación de frecuencias",
             "Magnification factor vs frequency ratio"),
    "ve_rho": ("Velocidad erosional vs. densidad (API RP 14E, C = 100)",
               "Erosional velocity vs density (API RP 14E, C = 100)"),
    "v": ("Velocidad, m/s", "Velocity, m/s"),
    "hz": ("Frecuencia, Hz", "Frequency, Hz"),
    "mpa": ("Esfuerzo, MPa", "Stress, MPa"),
    "L": ("L, mm", "L, mm"),
    "re": ("Re", "Re"),
    "ns": ("N_S", "N_S"),
    "r": ("r = f_s / f_n,c", "r = f_s / f_n,c"),
    "fm": ("F_M", "F_M"),
    "rho": ("Densidad, kg/m³", "Density, kg/m³"),
    "this": ("este tag", "this tag"),
    "limit": ("límite", "limit"),
    "allow": ("admisible", "allowable"),
    "value": ("calculado", "calculated"),
}


def _t(key: str, es: bool) -> str:
    return _T[key][0 if es else 1]


def _velocities(ev: Evaluation) -> tuple[list[float], float]:
    assert ev.result is not None
    vmax = max((c.velocity for c in ev.result.cases), default=1.0)
    hi = max(1.6 * vmax, 1.0)
    xs = [hi * i / 40 for i in range(1, 41)]
    return xs, hi


def _fs_v(ev: Evaluation, es: bool) -> bytes | None:
    if ev.result is None or ev.material is None or not ev.result.cases:
        return None
    xs, _ = _velocities(ev)
    pts = velocity_sweep(ev.input, ev.material, xs, ev.options)
    fnc = ev.result.cases[0].fnc
    series = [("f_s", [p.fs for p in pts], "#1f6fb2")]
    lim = [p.fs_limit if p.fs_limit is not None else float("nan") for p in pts]
    series.append((_t("limit", es), lim, "#e0a000"))
    marks = [(c.velocity, c.fs, c.scope) for c in ev.result.cases]
    return curve_png(xs, series, xlabel=_t("v", es), ylabel=_t("hz", es),
                     title=_t("fs_v", es), marks=marks, hlines=[(fnc, "f_n,c")])


def _stress_v(ev: Evaluation, es: bool, steady: bool) -> bytes | None:
    if ev.result is None or ev.material is None or not ev.result.cases:
        return None
    xs, _ = _velocities(ev)
    pts = velocity_sweep(ev.input, ev.material, xs, ev.options)
    vals = [(p.steady_stress if steady else p.dynamic_stress) / 1e6 for p in pts]
    allow = [(p.steady_allowable if steady else p.dynamic_allowable) / 1e6 for p in pts]
    series = [(_t("value", es), vals, "#1f6fb2"), (_t("allow", es), allow, "#c0392b")]
    top = 3.0 * max(allow, default=1.0)
    return curve_png(xs, series, xlabel=_t("v", es), ylabel=_t("mpa", es),
                     title=_t("steady_v" if steady else "stress_v", es), ylim=(0.0, top))


def _fn_l(ev: Evaluation, es: bool) -> bytes | None:
    if ev.result is None or ev.material is None or not ev.result.cases:
        return None
    g = ev.input.thermowell.geometry
    lo, hi = max(0.3 * g.L, 0.03), 2.0 * g.L
    ls = [lo + (hi - lo) * i / 30 for i in range(31)]
    pts = length_sweep(ev.input, ev.material, ls, ev.result.cases[0].velocity, ev.options)
    xs = [x * 1000 for x in ls]
    series = [("f_n,c", [p.fnc for p in pts], "#1f6fb2"), ("f_s", [p.fs for p in pts], "#888")]
    marks = [(g.L * 1000, ev.result.cases[0].fnc, _t("this", es))]
    return curve_png(xs, series, xlabel=_t("L", es), ylabel=_t("hz", es),
                     title=_t("fn_L", es), marks=marks)


def _st_re(ev: Evaluation, es: bool) -> bytes:
    xs, ys = sample(strouhal_correlation, 100.0, 5e7, log=True)
    marks = []
    if ev.result is not None:
        marks = [(c.reynolds, c.strouhal, c.scope) for c in ev.result.cases
                 if 100.0 <= c.reynolds <= 5e7]
    return curve_png(xs, [("N_S", ys, "#1f6fb2")], xlabel=_t("re", es), ylabel=_t("ns", es),
                     title=_t("st_re", es), marks=marks, logx=True)


def _fm_r(ev: Evaluation, es: bool) -> bytes:
    zeta = ev.options.damping
    ratios = [c.fs / c.fnc for c in (ev.result.cases if ev.result else []) if c.fnc]
    hi = max([1.6, *[1.1 * r for r in ratios]])
    xs, ys = sample(lambda r: max(magnification(r, zeta), 1e-3), 0.0, hi, n=400)
    marks = [(r, max(magnification(r, zeta), 1e-3), "") for r in ratios]
    return curve_png(xs, [("F_M", ys, "#1f6fb2")], xlabel=_t("r", es), ylabel=_t("fm", es),
                     title=_t("fm_r", es), marks=marks, logy=True)


def _ve_rho(ev: Evaluation, es: bool) -> bytes:
    xs, ys = sample(erosional_velocity, 0.5, 1500.0, log=True)
    watch = [EROSION_WATCH_RATIO * y for y in ys]
    rho = ev.input.process.properties.density
    marks = []
    if ev.result is not None:
        marks = [(rho, c.velocity, f"V {c.scope}") for c in ev.result.cases]
    return curve_png(xs, [("V_e", ys, "#c0392b"), ("0,7 V_e" if es else "0.7 V_e", watch,
                                                    "#e0a000")],
                     xlabel=_t("rho", es), ylabel=_t("v", es), title=_t("ve_rho", es),
                     marks=marks, logx=True)


_BUILDERS: dict[str, Callable[[Evaluation, bool], bytes | None]] = {
    "fs_v": _fs_v,
    "stress_v": lambda ev, es: _stress_v(ev, es, steady=False),
    "steady_v": lambda ev, es: _stress_v(ev, es, steady=True),
    "fn_L": _fn_l,
    "st_re": _st_re,
    "fm_r": _fm_r,
    "ve_rho": _ve_rho,
}


def curve(curve_id: str, ev: Evaluation, es: bool) -> bytes | None:
    """PNG de la curva pedida con los datos del tag; ``None`` si no se puede trazar."""
    try:
        return _BUILDERS[curve_id](ev, es)
    except (ValueError, ZeroDivisionError, OverflowError, KeyError):
        return None
