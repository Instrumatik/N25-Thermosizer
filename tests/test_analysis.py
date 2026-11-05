from __future__ import annotations

import pytest

from thermowell_sizer.core.analysis.optimize import AlternativeKind, propose_alternatives
from thermowell_sizer.core.analysis.sensitivity import (
    length_sweep,
    max_allowable_velocity,
    velocity_sweep,
)
from thermowell_sizer.core.models import (
    CalcInput,
    CheckStatus,
    ConnectionType,
    FatigueClass,
    MaterialProperties,
    ShankProfile,
)
from thermowell_sizer.core.ptc19_3.verify import verify
from thermowell_sizer.core.units import INCH_M

F22 = MaterialProperties(
    material_id="F22", density=7850.0, elastic_modulus=180e9, elastic_modulus_reference=213e9,
    allowable_stress=120e6, fatigue_class=FatigueClass.A,
)
INCONEL = MaterialProperties(
    material_id="N06625", density=8440.0, elastic_modulus=190e9,
    elastic_modulus_reference=195e9, allowable_stress=200e6, fatigue_class=FatigueClass.B,
)


def test_velocity_sweep_is_linear_in_fs(calc_input: CalcInput) -> None:
    points = velocity_sweep(calc_input, F22, [5.0, 10.0, 20.0])
    assert points[1].fs == pytest.approx(2 * points[0].fs, rel=0.05)
    assert all(p.fnc == pytest.approx(points[0].fnc) for p in points)
    assert points[0].fs_limit is not None


def test_length_sweep_stress_grows_with_length(calc_input: CalcInput) -> None:
    points = length_sweep(calc_input, F22, [6 * INCH_M, 8 * INCH_M, 10 * INCH_M], 20.0)
    assert points[0].steady_stress < points[1].steady_stress < points[2].steady_stress
    assert points[0].fnc > points[2].fnc


def test_max_allowable_velocity(calc_input: CalcInput) -> None:
    v = max_allowable_velocity(calc_input, F22, v_max=100.0, samples=100)
    assert v is not None
    assert 1.0 < v < 100.0
    assert max_allowable_velocity(calc_input, F22, v_max=0.5, samples=5) is None


def test_no_alternatives_when_passing(calc_input: CalcInput) -> None:
    case = calc_input.process.flow_cases[0].model_copy(update={"velocity": 5.0})
    slow = calc_input.model_copy(update={"process": calc_input.process.model_copy(
        update={"flow_cases": (case,)})})
    assert verify(slow, F22).status is not CheckStatus.FAIL
    assert propose_alternatives(slow, F22) == []


def _failing(calc_input: CalcInput) -> CalcInput:
    case = calc_input.process.flow_cases[0].model_copy(update={"velocity": 75.0})
    process = calc_input.process.model_copy(update={"flow_cases": (case,)})
    return calc_input.model_copy(update={"process": process})


def test_alternatives_order_and_validity(calc_input: CalcInput) -> None:
    inp = _failing(calc_input)
    assert verify(inp, F22).status is CheckStatus.FAIL
    alts = propose_alternatives(inp, F22, candidate_materials=[F22, INCONEL])
    kinds = [a.kind for a in alts]
    assert kinds[0] is AlternativeKind.REDUCE_LENGTH
    assert alts[0].changes["L"] < inp.thermowell.geometry.L
    for alt in alts:
        assert alt.result.status is not CheckStatus.FAIL
        assert alt.reason_key.startswith("opt.reason.")


def test_straight_and_threaded_alternatives(calc_input: CalcInput) -> None:
    inp = _failing(calc_input)
    g = inp.thermowell.geometry.model_copy(
        update={"profile": ShankProfile.STRAIGHT, "A": inp.thermowell.geometry.B,
                "L": 7 * INCH_M}
    )
    conn = inp.thermowell.connection.model_copy(
        update={"type": ConnectionType.THREADED, "rating_class": None, "face": None}
    )
    tw = inp.thermowell.model_copy(update={"geometry": g, "connection": conn})
    case = inp.process.flow_cases[0].model_copy(update={"velocity": 15.0})
    straight = inp.model_copy(update={
        "thermowell": tw,
        "process": inp.process.model_copy(update={"flow_cases": (case,)}),
    })
    assert verify(straight, F22).status is CheckStatus.FAIL
    kinds = {a.kind for a in propose_alternatives(straight, F22, min_length=6.9 * INCH_M)}
    assert AlternativeKind.TAPERED_PROFILE in kinds
    assert AlternativeKind.CHANGE_CONNECTION in kinds


def test_stepped_root_increase() -> None:
    from reference_cases import example_8_2

    inp, mat, _ = example_8_2()
    case = inp.process.flow_cases[0].model_copy(update={"velocity": 12.0})
    fast = inp.model_copy(update={"process": inp.process.model_copy(
        update={"flow_cases": (case,)})})
    assert verify(fast, mat).status is CheckStatus.FAIL
    alts = propose_alternatives(fast, mat, min_length=0.189)
    assert [a.kind for a in alts] == [AlternativeKind.CHANGE_CONNECTION]
