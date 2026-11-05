"""Recorridos de la lógica de verificación (párrs. 6-3.6, 6-8, 6-12, 6-13)."""

from __future__ import annotations

import pytest

from thermowell_sizer.core.models import (
    CalcInput,
    CheckStatus,
    ConnectionType,
    Construction,
    EngineOptions,
    FatigueClass,
    FlowBasis,
    FlowCase,
    MaterialProperties,
    MountingOrientation,
    Phase,
    StrouhalMethod,
)
from thermowell_sizer.core.ptc19_3.verify import (
    ROOT_CORROSION,
    TIP_CORROSION,
    VerificationResult,
    verify,
)
from thermowell_sizer.core.units import KELVIN_OFFSET

F22 = MaterialProperties(
    material_id="F22", density=7850.0, elastic_modulus=180e9, elastic_modulus_reference=213e9,
    allowable_stress=120e6, fatigue_class=FatigueClass.A, max_temperature=600 + KELVIN_OFFSET,
)


def _with(inp: CalcInput, **process: object) -> CalcInput:
    return inp.model_copy(update={"process": inp.process.model_copy(update=process)})


def _props(inp: CalcInput, rho: float, mu: float) -> CalcInput:
    return _with(inp, properties=inp.process.properties.model_copy(
        update={"density": rho, "dynamic_viscosity": mu}))


def _velocity(inp: CalcInput, v: float, **extra: object) -> CalcInput:
    case = FlowCase(label="max", basis=FlowBasis.VELOCITY, velocity=v)
    return _with(inp, flow_cases=(case,), **extra)


def _keys(result: VerificationResult) -> set[str]:
    return {c.message_key for c in result.checks}


def test_flow_bases(calc_input: CalcInput) -> None:
    rho = calc_input.process.properties.density
    area = 3.141592653589793 * calc_input.pipe.inner_diameter**2 / 4
    cases = (
        FlowCase(label="min", basis=FlowBasis.MASS_FLOW, mass_flow=rho * area * 5.0),
        FlowCase(label="normal", basis=FlowBasis.VOLUME_FLOW, volume_flow=area * 7.0),
    )
    result = verify(_with(calc_input, flow_cases=cases), F22)
    assert result.trace.value("V", "min") == pytest.approx(5.0)
    assert result.trace.value("V", "normal") == pytest.approx(7.0)
    assert [c.flow_case for c in result.cases] == ["min", "normal"]


def test_low_velocity_exemption(calc_input: CalcInput) -> None:
    result = verify(_velocity(_props(calc_input, 990.0, 1e-3), 0.3), F22)
    assert "check.low_velocity_exempt" in _keys(result)
    assert result.cases[0].low_velocity_exempt
    assert result.worst("frequency_limit") is None


def test_no_vortex_shedding(calc_input: CalcInput) -> None:
    result = verify(_velocity(_props(calc_input, 950.0, 5.0), 2.0), F22)
    assert "check.no_vortex_shedding" in _keys(result)


def test_simplified_strouhal_and_general_hc(calc_input: CalcInput) -> None:
    opts = EngineOptions(strouhal_method=StrouhalMethod.SIMPLIFIED, support_stiffness=5e5)
    result = verify(calc_input, F22, opts)
    assert result.trace.value("N_S", "max") == 0.22
    assert result.trace.get("H_c", "max").reference.endswith("eq. (6-6-2)")
    assert result.trace.get("V_IR", "max").reference.endswith("eq. (6-8-5)")


def test_sanitary_and_supplier_rating(calc_input: CalcInput) -> None:
    conn = calc_input.thermowell.connection.model_copy(
        update={"type": ConnectionType.SANITARY, "rating_class": None})
    tw = calc_input.thermowell.model_copy(update={"connection": conn})
    result = verify(calc_input.model_copy(update={"thermowell": tw}), F22,
                    EngineOptions(supplier_rating=True))
    assert "note.sanitary_compliance" in result.notes
    assert "note.supplier_rating" in result.notes
    assert result.trace.value("H_af", "max") == 1.0
    assert result.trace.get("H_c", "max").reference.endswith("eq. (6-7-1)")


def test_scruton_all_suppressed(calc_input: CalcInput) -> None:
    inp = _velocity(_props(calc_input, 0.05, 1.5e-5), 5.0, phase=Phase.GAS)
    result = verify(inp, F22)
    assert "check.frequency_scruton_all" in _keys(result)
    assert "note.higher_modes" in result.notes


def test_inline_passage_allowed_for_gas(calc_input: CalcInput) -> None:
    opts = EngineOptions(allow_inline_passage=True, finite_life_fatigue_limit=1e12)
    inp = _velocity(calc_input, 15.0, phase=Phase.GAS)
    result = verify(inp, F22, opts)
    check = result.worst("frequency_limit")
    assert check is not None
    assert check.message_key == "check.frequency_inline_passage"
    assert check.status is CheckStatus.WARNING
    assert "note.inline_passage_conditions" in result.notes
    # Sin la opción, el límite vuelve a 0,4·f_n^c
    plain = verify(inp, F22).worst("frequency_limit")
    assert plain is not None
    assert plain.message_key == "check.frequency_inline_limited"


def test_inline_passage_rejected_for_liquid(calc_input: CalcInput) -> None:
    opts = EngineOptions(allow_inline_passage=True, finite_life_fatigue_limit=1e12)
    inp = _velocity(_props(calc_input, 900.0, 1e-3), 3.0, phase=Phase.LIQUID)
    check = verify(inp, F22, opts).worst("frequency_limit")
    assert check is not None
    assert check.message_key == "check.frequency_inline_limited"


def _fnc(inp: CalcInput) -> float:
    return verify(inp, F22).cases[0].fnc


def test_lockin_dwell_and_supercritical(calc_input: CalcInput) -> None:
    base = _props(calc_input, 2.0, 2e-7)
    fnc = _fnc(_velocity(base, 30.0))
    b = calc_input.thermowell.geometry.B
    v_mid = 0.5 * fnc * b / 0.22
    result = verify(_velocity(base, v_mid), F22)
    assert result.cases[0].inline_stress_ok is True
    assert "check.lockin_dwell" in _keys(result)
    v_low = 0.2 * fnc * b / 0.22
    assert "check.lockin_clear" in _keys(verify(_velocity(base, v_low), F22))
    v_super = 1.1 * fnc * b / 0.22
    sup = verify(_velocity(base, v_super), F22)
    assert "check.frequency_supercritical" in _keys(sup)
    assert sup.status is CheckStatus.FAIL


def test_flange_rating_paths(calc_input: CalcInput) -> None:
    missing = verify(calc_input, F22)
    flange = missing.worst("flange_rating")
    assert flange is not None
    assert flange.status is CheckStatus.NOT_APPLICABLE
    ok = verify(calc_input, F22, EngineOptions(flange_rating=5e6)).worst("flange_rating")
    assert ok is not None
    assert ok.message_key == "check.flange_rating"
    derated = verify(calc_input, F22, EngineOptions(flange_rating=1e12)).worst("flange_rating")
    assert derated is not None
    assert derated.message_key == "check.flange_derated"


def test_material_temperature_and_scope(calc_input: CalcInput) -> None:
    hot = _with(calc_input, design_temperature=700 + KELVIN_OFFSET)
    result = verify(hot, F22)
    assert result.worst("material_temperature").status is CheckStatus.FAIL  # type: ignore[union-attr]
    g = calc_input.thermowell.geometry.model_copy(update={"construction": Construction.FABRICATED})
    tw = calc_input.thermowell.model_copy(update={"geometry": g})
    fab = verify(calc_input.model_copy(update={"thermowell": tw}), F22)
    assert fab.worst("scope").status is CheckStatus.FAIL  # type: ignore[union-attr]
    assert fab.status is CheckStatus.FAIL


@pytest.mark.parametrize(
    ("orientation", "note"),
    [
        (MountingOrientation.ELBOW_TIP_DOWNSTREAM, "note.elbow_downstream"),
        (MountingOrientation.ELBOW_TIP_UPSTREAM, "note.elbow_upstream"),
        (MountingOrientation.ANGLED, "note.angled"),
    ],
)
def test_orientation_notes(
    calc_input: CalcInput, orientation: MountingOrientation, note: str
) -> None:
    pipe = calc_input.pipe.model_copy(update={"orientation": orientation})
    result = verify(calc_input.model_copy(update={"pipe": pipe}), F22)
    assert note in result.notes


def test_two_phase_and_high_temperature_notes(calc_input: CalcInput) -> None:
    hot = _with(calc_input, phase=Phase.TWO_PHASE, operating_temperature=450 + KELVIN_OFFSET,
                design_temperature=460 + KELVIN_OFFSET)
    notes = verify(hot, F22).notes
    assert "note.two_phase" in notes
    assert "note.high_temperature_fe" in notes


def test_corrosion_cases(calc_input: CalcInput) -> None:
    g = calc_input.thermowell.geometry.model_copy(update={"corrosion_allowance": 0.001})
    tw = calc_input.thermowell.model_copy(update={"geometry": g})
    inp = calc_input.model_copy(update={"thermowell": tw})
    result = verify(inp, F22)
    scopes = result.trace.scopes()
    assert ROOT_CORROSION in scopes
    assert f"max|{TIP_CORROSION}" in scopes
    assert result.trace.value("P_t", ROOT_CORROSION) < result.trace.value("P_t")
    assert len(verify(inp, F22, EngineOptions(corrosion_cases=False)).cases) == 1


def test_stepped_corrosion_keeps_table(calc_input: CalcInput) -> None:
    from reference_cases import example_8_2

    inp, mat, _ = example_8_2()
    g = inp.thermowell.geometry.model_copy(update={"corrosion_allowance": 0.0008})
    tw = inp.thermowell.model_copy(update={"geometry": g})
    result = verify(inp.model_copy(update={"thermowell": tw}), mat)
    assert result.trace.value("H_f", f"normal|{TIP_CORROSION}") > 0


def test_very_high_pressure_rating_warning(calc_input: CalcInput) -> None:
    strong = F22.model_copy(update={"allowable_stress": 2e9})
    result = verify(calc_input, strong)
    assert result.worst("pressure_high_service") is not None
    assert result.worst("does_not_exist") is None


def test_amber_margin(calc_input: CalcInput) -> None:
    result = verify(calc_input, F22, EngineOptions(amber_margin_pct=100.0))
    assert result.worst("pressure_rating").status is CheckStatus.WARNING  # type: ignore[union-attr]


def test_fatigue_not_covered(calc_input: CalcInput) -> None:
    ti = F22.model_copy(update={"fatigue_table_covered": False})
    result = verify(calc_input, ti)
    assert result.worst("fatigue_data").status is CheckStatus.WARNING  # type: ignore[union-attr]
    tested = ti.model_copy(update={"fatigue_limit_override": 30e6})
    res2 = verify(calc_input, tested)
    assert res2.worst("fatigue_data") is None
    assert res2.trace.value("S_f_adm", "max") == pytest.approx(30e6 * 180 / 213)
