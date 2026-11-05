"""Pruebas unitarias de las funciones puras de cada subsección."""

from __future__ import annotations

import math

import pytest

from thermowell_sizer.core.models import ShankProfile
from thermowell_sizer.core.ptc19_3 import (
    compliance,
    flow,
    frequency_limits,
    natural_frequency,
    stresses,
)
from thermowell_sizer.core.units import INCH_M


def test_velocity_from_flows() -> None:
    area = flow.pipe_area(0.1)
    assert flow.velocity_from_volume_flow(area * 2.0, 0.1) == pytest.approx(2.0)
    assert flow.velocity_from_mass_flow(1000.0 * area * 3.0, 1000.0, 0.1) == pytest.approx(3.0)


def test_strouhal_branches_and_continuity() -> None:
    assert flow.strouhal_correlation(10.0) == 0.0
    assert flow.strouhal_correlation(100.0) == pytest.approx(0.22 * (1 - 0.22))
    assert flow.strouhal_correlation(1e6) == 0.22
    assert flow.strouhal_correlation(1e8) == 0.22
    # La correlación es casi continua en Re = 1300 y 5e5
    assert flow.strouhal_correlation(1299.999) == pytest.approx(
        flow.strouhal_correlation(1300.0), abs=0.01
    )
    assert flow.strouhal_correlation(5e5 - 1) == pytest.approx(0.22, abs=0.01)


def test_hf_limits() -> None:
    # Viga esbelta recta: H_f ≈ 0,99 (párr. 6-5.3)
    hf = natural_frequency.hf_straight_tapered(0.02, 0.02, 0.0066, 2.0, 0.02)
    assert hf == pytest.approx(0.99, abs=0.005)


def test_hf_stepped_requires_table_diameter() -> None:
    assert natural_frequency.step_shank_coefficients(0.0150) is None
    with pytest.raises(ValueError, match="12,7"):
        natural_frequency.hf_stepped(0.03, 0.015, 0.05, 0.2)
    assert natural_frequency.average_diameter(ShankProfile.STEPPED, 0.03, 0.02) == 0.03


def test_hc_general_matches_semi_infinite() -> None:
    """La eq. (6-6-2) con K_M de la eq. (6-6-4) reproduce la eq. (6-6-5) (párr. 6-6)."""
    e, a, length, b = 200e9, 0.0254, 0.25, 0.003
    d = 0.01**0.25 * a  # A⁴ − d⁴ = 0,99·A⁴, como en la deducción de la norma
    km = compliance.support_stiffness_semi_infinite(e, a)
    general = compliance.hc_general(km, e, a, d, length, b)
    assert general == pytest.approx(compliance.hc_semi_infinite(a, length, b), rel=0.002)


def test_inline_resonance_velocity_branches() -> None:
    b, fnc = 0.02, 300.0
    simple = frequency_limits.inline_resonance_velocity_simplified(b, fnc, 0.22)
    assert frequency_limits.inline_resonance_velocity(b, fnc, 0.22, 1e6, 10, 1, 1) == simple
    low = frequency_limits.inline_resonance_velocity(b, fnc, 0.2, 500.0, 2.0, 900.0, 0.05)
    assert low > 0


def test_magnification() -> None:
    assert frequency_limits.magnification(0.5, 0.0005) == pytest.approx(1 / 0.75)
    assert frequency_limits.magnification(1.0, 0.0005) == 1000.0
    assert frequency_limits.magnification(2.0, 0.0005) == pytest.approx(1 / 3)


@pytest.mark.parametrize("l0_frac", [0.0, 0.2, 0.5])
def test_g_tapered_matches_numeric(l0_frac: float) -> None:
    a, b, d, length = 1.25 * INCH_M, 0.875 * INCH_M, 0.26 * INCH_M, 10 * INCH_M
    l0 = l0_frac * length
    closed = stresses.g_support_tapered(length, a, b, d, l0)
    numeric = stresses.g_numeric(lambda z: a + (b - a) * z / length, d, length, 0.0, l0)
    assert closed == pytest.approx(numeric, rel=1e-6)


@pytest.mark.parametrize("l0_frac", [0.0, 0.3, 0.75])
def test_g_stepped_matches_numeric(l0_frac: float) -> None:
    a, b, d, length, ls = 0.0222, 0.0127, 0.0066, 0.19, 0.0635
    l0 = l0_frac * length

    def diam(z: float) -> float:
        return a if z < length - ls else b

    sp = stresses.g_support_stepped(length, a, b, d, ls, l0)
    # D(z) es discontinuo: se integra con D(z_s)=A en el soporte
    lower = l0
    num_sp = 32 * a / (math.pi * (a**4 - d**4)) * _piecewise_moment(a, b, length, ls, 0.0, lower)
    assert sp == pytest.approx(num_sp, rel=1e-9)
    z_step = length - ls
    rd = stresses.g_step_base(length, b, d, ls, l0)
    num_rd = (
        32 * b / (math.pi * (b**4 - d**4))
        * _piecewise_moment(b, b, length, ls, z_step, max(z_step, l0))
    )
    assert rd == pytest.approx(num_rd, rel=1e-9)
    assert diam(0.0) == a


def _piecewise_moment(a: float, b: float, length: float, ls: float, zs: float, lo: float) -> float:
    step = length - ls

    def part(d_val: float, z1: float, z2: float) -> float:
        if z2 <= z1:
            return 0.0
        return d_val * (((z2 - zs) ** 2) - ((z1 - zs) ** 2)) / 2

    return part(a, lo, step) + part(b, max(lo, step), length)


def test_stress_concentration() -> None:
    assert stresses.stress_concentration(0.03, 0.0) == 2.2
    assert stresses.stress_concentration(0.03, 0.003) == pytest.approx(1.1 + 0.033 * 10)
    assert stresses.stress_concentration(0.03, 0.0005) == 2.2  # A/b ≥ 33
    assert stresses.stress_concentration(0.03, 0.003, threaded=True) == 2.3
