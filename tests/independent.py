"""Recálculo independiente para los casos cruzados.

Implementación deliberadamente distinta del motor: fórmulas escritas de corrido, sin
reutilizar ningún módulo de ``thermowell_sizer``, y el parámetro G obtenido por
integración numérica de su definición (eq. 6-10-3) en lugar de las fórmulas cerradas.
"""

from __future__ import annotations

import math

from scipy import integrate


def strouhal(re: float) -> float:
    if re < 22:
        return 0.0
    if re < 1300:
        return 0.22 * (1 - 22 / re)
    if re < 5e5:
        x = math.log10(re / 1300)
        return 0.213 - 0.0248 * x * x + 0.0095 * x**3
    return 0.22


def g_param(diam, d: float, length: float, z_s: float, l0: float) -> float:
    lower = max(z_s, l0)
    dz = diam(z_s)
    mom = integrate.quad(lambda z: diam(z) * (z - z_s), lower, length, limit=400)[0]
    return 32 * dz / (math.pi * (dz**4 - d**4)) * mom


def tapered_case(
    *, A: float, B: float, d: float, L: float, b: float, t: float, L0: float,
    E: float, Eref: float, rho_m: float, S: float, Sf: float, rho: float, mu: float,
    V: float, P: float, rho_s: float = 2700.0, zeta: float = 0.0005, kt_threaded: bool = False,
    hc_mode: str = "semi",
) -> dict[str, float]:
    """Recalcula un termopozo recto/cónico con la secuencia de la sección 7."""
    out: dict[str, float] = {}
    re = V * B * rho / mu
    ns = strouhal(re)
    fs = ns * V / B
    da = (A + B) / 2
    inertia = math.pi * (da**4 - d**4) / 64
    m = rho_m * math.pi * (da**2 - d**2) / 4
    fa = 1.875**2 / (2 * math.pi) * math.sqrt(E * inertia / m) / L**2
    hf = 0.99 * (1 + (1 - B / A) + (1 - B / A) ** 2) / (
        1 + 1.1 * (da / L) ** (3 * (1 - 0.8 * d / da))
    )
    haf = 1 - rho / (2 * rho_m)
    has = 1 - rho_s / (2 * rho_m) / ((da / d) ** 2 - 1)
    fn = hf * haf * has * fa
    hc = 1 - 0.9 * A / L if hc_mode == "threaded" else 1 - 0.61 * (A / L) / (1 + 1.5 * b / A) ** 2
    fnc = hc * fn
    nsc = math.pi**2 * zeta * rho_m / rho * (1 - (d / B) ** 2)
    g = g_param(lambda z: A + (B - A) * z / L, d, L, 0.0, L0)
    kt = 1.1 + 0.033 * A / b if b > 0 and A / b < 33 else 2.2
    if kt_threaded:
        kt = max(kt, 2.3)
    sr = P
    st = P * (1 + (d / A) ** 2) / (1 - (d / A) ** 2)
    sa = P / (1 - (d / A) ** 2)
    sd = g * 0.5 * 1.4 * rho * V**2
    smax = sd + sa
    vm = math.sqrt(((smax - sr) ** 2 + (smax - st) ** 2 + (st - sr) ** 2) / 2)

    def mag(rr: float) -> float:
        return 1 / (2 * zeta) if 0.8 < rr < 1.2 else 1 / abs(1 - rr * rr)

    fm, fmp = mag(fs / fnc), mag(2 * fs / fnc)
    s_d = g * fmp * 0.5 * 0.1 * rho * V**2
    s_l = g * fm * 0.5 * 1.0 * rho * V**2
    so = kt * math.sqrt(s_d**2 + s_l**2)
    allow = E / Eref * Sf
    pc = 0.66 * S * (2.167 / (2 * B / (B - d)) - 0.0833)
    pt = S / 0.13 * (t / d) ** 2
    out.update(
        Re=re, N_S=ns, f_s=fs, f_a=fa, H_f=hf, H_af=haf, H_as=has, f_n=fn, H_c=hc,
        f_nc=fnc, N_Sc=nsc, G_SP=g, S_vm_support=vm, S_o_support=so, S_f_adm=allow,
        P_c=pc, P_t=pt, K_t_SP=kt,
    )
    if re < 1e5 and nsc > 2.5:
        out["ratio_limit"] = 0.8
    else:
        if re < 1300:
            nu = 22 * mu / (B * rho)
            v_ir = B * fnc / (2 * ns) * (1 - nu / V) + nu
        elif re < 5e5:
            base = B * fnc / (2 * ns)
            rr = math.log10(re / 1300)
            a = 0.0285 * rr * rr - 0.0496 * rr
            v_ir = base * (1 - a / ns * math.log10(base / V))
        else:
            v_ir = B * fnc / (2 * ns)
        so_ir = kt * g * (1 / (2 * zeta)) * 0.5 * 0.1 * rho * v_ir**2
        out["V_IR"] = v_ir
        out["ratio_limit"] = 0.8 if so_ir < allow else 0.4
    return out
