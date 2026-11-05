"""Calculadoras auxiliares: conversor, sensores y estimaciones térmicas."""

from __future__ import annotations

import math

import pytest

from thermowell_sizer.core.tools import converter, heat, sensors

# Valores de referencia de las tablas NIST ITS-90 (FEM en mV, unión fría a 0 °C).
NIST_POINTS = [
    ("K", 100.0, 4.096), ("K", 500.0, 20.644), ("K", 1000.0, 41.276), ("K", -100.0, -3.554),
    ("J", 200.0, 10.779), ("J", 760.0, 42.919), ("T", 100.0, 4.279), ("T", -200.0, -5.603),
    ("E", 300.0, 21.036), ("N", 600.0, 20.613), ("R", 1000.0, 10.506), ("S", 1000.0, 9.587),
    ("B", 1000.0, 4.834),
]


@pytest.mark.parametrize(("typ", "temp", "emf"), NIST_POINTS)
def test_tc_emf_matches_nist(typ: str, temp: float, emf: float) -> None:
    assert sensors.tc_emf(typ, temp) == pytest.approx(emf, abs=1.5e-3)
    assert sensors.tc_temperature(typ, sensors.tc_emf(typ, temp)) == pytest.approx(temp,
                                                                                   abs=1e-4)


def test_tc_cold_junction_and_errors() -> None:
    e = sensors.tc_emf("K", 300) - sensors.tc_emf("K", 25)
    assert sensors.tc_temperature("K", e, 25) == pytest.approx(300, abs=1e-4)
    with pytest.raises(ValueError):
        sensors.tc_emf("T", 500)
    with pytest.raises(ValueError):
        sensors.tc_temperature("T", 50.0)
    assert sensors.tc_range("K") == (-270.0, 1372.0)


def test_rtd_cvd() -> None:
    assert sensors.rtd_resistance(0) == pytest.approx(100.0)
    assert sensors.rtd_resistance(100) == pytest.approx(138.5055, abs=1e-4)
    assert sensors.rtd_resistance(-100) == pytest.approx(60.2558, abs=1e-4)
    assert sensors.rtd_resistance(850) == pytest.approx(390.4811, abs=1e-3)
    for temp in (-150.0, -20.0, 0.0, 250.0, 700.0):
        r = sensors.rtd_resistance(temp, 1000.0)
        assert sensors.rtd_temperature(r, 1000.0) == pytest.approx(temp, abs=1e-6)
    assert sensors.rtd_tolerance(100, sensors.RtdClass.A) == pytest.approx(0.35)
    assert sensors.rtd_tolerance(-100, sensors.RtdClass.B) == pytest.approx(0.8)
    with pytest.raises(ValueError):
        sensors.rtd_resistance(900)
    with pytest.raises(ValueError):
        sensors.rtd_temperature(10.0)
    with pytest.raises(ValueError):
        sensors.rtd_temperature(500.0)


def test_tables() -> None:
    rows = sensors.table("rtd", "100", -200, 850, 50)
    assert len(rows) == 22 and rows[4][0] == 0 and rows[4][1] == pytest.approx(100)
    tc_rows = sensors.table("tc", "J", 0, 100, 10)
    assert len(tc_rows) == 11


@pytest.mark.parametrize(("cat", "a", "b", "value", "expected"), [
    ("temperature", "°C", "°F", 100.0, 212.0),
    ("temperature", "K", "°R", 100.0, 180.0),
    ("pressure", "bar(g)", "bar (abs)", 0.0, 1.01325),
    ("pressure", "psi(g)", "kPa (abs)", 14.5038, 201.325),
    ("length", "in", "mm", 1.0, 25.4),
    ("volume_flow", "m³/h", "L/min", 6.0, 100.0),
    ("dynamic_viscosity", "cP", "Pa·s", 1.0, 1e-3),
    ("velocity", "ft/s", "m/s", 1.0, 0.3048),
    ("stress", "ksi", "MPa", 1.0, 6.894757),
    ("frequency", "rpm", "Hz", 60.0, 1.0),
    ("density", "g/cm³", "kg/m³", 1.0, 1000.0),
])
def test_converter(cat: str, a: str, b: str, value: float, expected: float) -> None:
    assert converter.convert(value, cat, a, b) == pytest.approx(expected, rel=2e-5)


def test_converter_all_round_trip() -> None:
    for cat, units in converter.CATEGORIES.items():
        first = units[0].symbol
        for sym, val in converter.convert_all(7.0, cat, first):
            assert converter.convert(val, cat, sym, first) == pytest.approx(7.0)


def test_flow_and_reynolds() -> None:
    v = heat.velocity_from_mass_flow(10.0, 1000.0, 0.1)
    assert v == pytest.approx(10.0 / (1000 * math.pi * 0.0025))
    assert heat.velocity_from_volume_flow(0.01, 0.1) == pytest.approx(v)
    assert heat.reynolds(1000, 1, 0.1, 1e-3) == pytest.approx(1e5)


def test_churchill_bernstein() -> None:
    # Re = 1e4, Pr = 0,7, calculado a mano con la correlación: Nu = 53,33.
    assert heat.churchill_bernstein(1e4, 0.7) == pytest.approx(53.33, rel=1e-3)
    assert heat.churchill_bernstein(0.0, 0.7) == 0.3
    h = heat.film_coefficient(1.2, 10, 0.02, 1.8e-5, 0.026, 1005)
    assert 50 < h < 200


def test_immersion_and_tau() -> None:
    res = heat.immersion_error(fluid_temperature=500, base_temperature=300, h=100,
                               length=0.1, outer_diameter=0.02, bore=0.006,
                               conductivity=16, tolerance=0.1)
    assert 0 < res.error < 200
    assert res.min_length is not None and res.min_length > 0.1
    assert res.error == pytest.approx(200 / math.cosh(res.m * 0.1))
    short = heat.immersion_error(fluid_temperature=300.05, base_temperature=300, h=100,
                                 length=0.1, outer_diameter=0.02, bore=0.006, conductivity=16,
                                 tolerance=0.1)
    assert short.min_length == 0.0
    tau = heat.time_constant(h=1000, outer_diameter=0.019, bore=0.0066, wall_density=8000,
                             wall_specific_heat=500, sensor_diameter=0.006, sensor_tau=2)
    assert tau.total == pytest.approx(tau.film + tau.gap + 2)
    assert tau.t90 == pytest.approx(tau.total * math.log(10))


def test_corrosion() -> None:
    assert heat.corrosion_allowance(1e-4, 20) == pytest.approx(2e-3)
    assert heat.remaining_life(6e-3, 3e-3, 1e-4) == pytest.approx(30)
    assert math.isinf(heat.remaining_life(6e-3, 3e-3, 0))
