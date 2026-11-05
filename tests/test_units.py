import math

import pytest

from thermowell_sizer.core.units import (
    PSI_PA,
    QuantityKind,
    UnitSystem,
    from_display,
    to_display,
)


def test_temperature_round_trip() -> None:
    k = from_display(212.0, QuantityKind.TEMPERATURE, UnitSystem.IMPERIAL)
    assert k == pytest.approx(373.15)
    value, symbol = to_display(k, QuantityKind.TEMPERATURE, UnitSystem.SI)
    assert value == pytest.approx(100.0)
    assert symbol == "°C"


def test_psi_definition() -> None:
    assert pytest.approx(6894.757293168361, rel=1e-12) == PSI_PA


def test_gauge_pressure() -> None:
    pa = from_display(10.0, QuantityKind.PRESSURE, UnitSystem.SI, gauge=True)
    assert pa == pytest.approx(1_101_325.0)
    value, symbol = to_display(pa, QuantityKind.PRESSURE, UnitSystem.IMPERIAL, gauge=True)
    assert symbol == "psig"
    assert value == pytest.approx(145.0377, rel=1e-6)


@pytest.mark.parametrize("kind", list(QuantityKind))
@pytest.mark.parametrize("system", list(UnitSystem))
def test_every_unit_round_trips(kind: QuantityKind, system: UnitSystem) -> None:
    original = 123.456
    si = from_display(original, kind, system)
    back, _ = to_display(si, kind, system)
    assert math.isclose(back, original, rel_tol=1e-12)


def test_switching_systems_does_not_lose_data() -> None:
    si = 0.254
    inches, _ = to_display(si, QuantityKind.LENGTH, UnitSystem.IMPERIAL)
    assert inches == pytest.approx(10.0)
    assert from_display(inches, QuantityKind.LENGTH, UnitSystem.IMPERIAL) == pytest.approx(si)
