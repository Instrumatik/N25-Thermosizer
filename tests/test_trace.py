import pytest

from thermowell_sizer.core.trace import CalcTrace
from thermowell_sizer.core.units import QuantityKind


def test_record_returns_value_and_keeps_order() -> None:
    trace = CalcTrace()
    v = trace.record(
        "Re", 1.5e5, kind=QuantityKind.DIMENSIONLESS, reference="ref", expression="Re=VB/\\nu",
        description_key="trace.re",
        inputs={"V": (10.0, QuantityKind.VELOCITY), "B": (0.02, QuantityKind.DIAMETER)},
    )
    trace.record("f_s", 50.0, kind=QuantityKind.FREQUENCY, reference="r", expression="",
                 description_key="trace.fs")
    assert v == 1.5e5
    assert [e.symbol for e in trace] == ["Re", "f_s"]
    assert len(trace) == 2
    assert "Re" in trace
    assert trace["Re"].inputs == {"V": 10.0, "B": 0.02}
    assert trace["Re"].input_kinds["V"] is QuantityKind.VELOCITY


def test_duplicate_symbol_rejected() -> None:
    trace = CalcTrace()
    trace.record("x", 1.0, kind=QuantityKind.LENGTH, reference="", expression="",
                 description_key="")
    with pytest.raises(ValueError, match="ya está registrado"):
        trace.record("x", 2.0, kind=QuantityKind.LENGTH, reference="", expression="",
                     description_key="")
