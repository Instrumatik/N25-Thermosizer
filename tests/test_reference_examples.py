"""Validación contra los ejemplos resueltos de la norma: desviación < 1 % en cada paso."""

from __future__ import annotations

import pytest

from reference_cases import EXPECTED_8_1, EXPECTED_8_2, example_8_1, example_8_2
from thermowell_sizer.core.models import CheckStatus
from thermowell_sizer.core.ptc19_3.verify import verify

TOLERANCE = 0.01


def _pressure_symbol(symbol: str) -> bool:
    return symbol in {"P_c", "P_t"}


@pytest.mark.parametrize(("symbol", "expected"), list(EXPECTED_8_1.items()))
def test_example_8_1(symbol: str, expected: float) -> None:
    result = verify(*example_8_1())
    scope = "" if _pressure_symbol(symbol) else "normal"
    assert result.trace.value(symbol, scope) == pytest.approx(expected, rel=TOLERANCE)


@pytest.mark.parametrize(("symbol", "expected"), list(EXPECTED_8_2.items()))
def test_example_8_2(symbol: str, expected: float) -> None:
    result = verify(*example_8_2())
    scope = "" if _pressure_symbol(symbol) else "normal"
    assert result.trace.value(symbol, scope) == pytest.approx(expected, rel=TOLERANCE)


def test_example_8_1_verdicts() -> None:
    result = verify(*example_8_1())
    assert result.status in (CheckStatus.PASS, CheckStatus.WARNING)
    freq = result.worst("frequency_limit")
    assert freq is not None
    assert freq.limit == pytest.approx(870.2, rel=TOLERANCE)  # 0,4·f_n^c (párr. 8-1.4)
    assert freq.status is CheckStatus.PASS
    case = result.cases[0]
    assert case.inline_stress_ok is False  # párr. 8-1.5, paso 6
    assert result.worst("steady_stress_support").status is CheckStatus.PASS  # type: ignore[union-attr]
    assert result.worst("dynamic_stress_support").status is CheckStatus.PASS  # type: ignore[union-attr]
    assert result.worst("pressure_rating").status is CheckStatus.PASS  # type: ignore[union-attr]


def test_example_8_2_verdicts() -> None:
    result = verify(*example_8_2())
    freq = result.worst("frequency_limit")
    assert freq is not None
    assert freq.limit == pytest.approx(218.0, rel=TOLERANCE)  # párr. 8-2.4
    assert result.cases[0].inline_stress_ok is False
    for criterion in ("steady_stress_support", "steady_stress_step",
                      "dynamic_stress_support", "dynamic_stress_step", "pressure_rating"):
        check = result.worst(criterion)
        assert check is not None
        assert check.status in (CheckStatus.PASS, CheckStatus.WARNING), criterion
    assert result.status is not CheckStatus.FAIL
