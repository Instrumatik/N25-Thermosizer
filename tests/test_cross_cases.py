"""Casos cruzados 3 a 5: motor frente al recálculo independiente (desviación < 1 %)."""

from __future__ import annotations

import math

import pytest

from independent import tapered_case
from thermowell_sizer.core.models import (
    CalcInput,
    ConnectionType,
    EngineOptions,
    FatigueClass,
    FlowBasis,
    FlowCase,
    FluidProperties,
    Identification,
    MaterialProperties,
    MaterialRef,
    Phase,
    PipeData,
    ProcessConditions,
    ProcessConnection,
    PropertySource,
    SensorSpec,
    SensorType,
    ShankProfile,
    Thermowell,
    ThermowellGeometry,
)
from thermowell_sizer.core.ptc19_3.verify import verify
from thermowell_sizer.core.units import (
    INCH_M,
    KELVIN_OFFSET,
    STANDARD_ATMOSPHERE_PA,
    UnitSystem,
    from_display,
    to_display,
)
from thermowell_sizer.core.units import QuantityKind as Q

SS316 = MaterialProperties(
    material_id="SS316", density=7950.0, elastic_modulus=186e9,
    elastic_modulus_reference=195e9, allowable_stress=115e6, fatigue_class=FatigueClass.B,
)
CS = MaterialProperties(
    material_id="A105", density=7850.0, elastic_modulus=196e9,
    elastic_modulus_reference=202e9, allowable_stress=138e6, fatigue_class=FatigueClass.A,
)


def _input(
    *, profile: ShankProfile, A: float, B: float, d: float, L: float, t: float, b: float,
    L0: float, conn: ConnectionType, rho: float, mu: float, V: float, p_gauge: float,
    phase: Phase, c: float = 0.0, rating: int | None = None,
) -> CalcInput:
    p_abs = p_gauge + STANDARD_ATMOSPHERE_PA
    return CalcInput(
        identification=Identification(tag="CX"),
        process=ProcessConditions(
            fluid_id="custom", phase=phase, operating_pressure=p_abs, design_pressure=p_abs,
            operating_temperature=60 + KELVIN_OFFSET, design_temperature=60 + KELVIN_OFFSET,
            flow_cases=(FlowCase(label="max", basis=FlowBasis.VELOCITY, velocity=V),),
            properties=FluidProperties(density=rho, dynamic_viscosity=mu,
                                       source=PropertySource.USER),
        ),
        pipe=PipeData(nominal_size="NPS 10", inner_diameter=0.2545),
        thermowell=Thermowell(
            geometry=ThermowellGeometry(profile=profile, A=A, B=B, d=d, L=L, t=t, b=b, L0=L0,
                                        corrosion_allowance=c),
            material=MaterialRef(material_id="x"),
            connection=ProcessConnection(type=conn, rating_class=rating),
        ),
        sensor=SensorSpec(type=SensorType.TC_K, sheath_diameter=6e-3),
    )


CASES = {
    # 3: aire a baja presión, recto bridado: Re < 1e5 y N_Sc > 2,5 (párr. 6-8.2).
    "gas_recto_bridado": dict(
        profile=ShankProfile.STRAIGHT, A=0.75 * INCH_M, B=0.75 * INCH_M, d=0.26 * INCH_M,
        L=12 * INCH_M, t=0.25 * INCH_M, b=0.0625 * INCH_M, L0=0.0, conn=ConnectionType.FLANGED,
        rho=1.2, mu=1.8e-5, V=12.0, p_gauge=50e3, phase=Phase.GAS, rating=150,
        mat=SS316,
    ),
    # 4: aceite viscoso, Re entre 22 y 1300: primera rama de las eqs. 6-4-2 y 6-8-3.
    "liquido_viscoso_roscado": dict(
        profile=ShankProfile.TAPERED, A=0.875 * INCH_M, B=0.625 * INCH_M, d=0.26 * INCH_M,
        L=7.5 * INCH_M, t=0.25 * INCH_M, b=0.0, L0=0.0, conn=ConnectionType.THREADED,
        rho=890.0, mu=0.35, V=3.0, p_gauge=1.5e6, phase=Phase.LIQUID, mat=CS,
    ),
    # 5: agua de enfriamiento, cónico bridado con tramo protegido L0 (eq. 6-10-8).
    "agua_conico_protegido": dict(
        profile=ShankProfile.TAPERED, A=1.25 * INCH_M, B=0.875 * INCH_M, d=0.385 * INCH_M,
        L=10 * INCH_M, t=0.25 * INCH_M, b=0.1875 * INCH_M, L0=2.5 * INCH_M,
        conn=ConnectionType.FLANGED, rho=995.0, mu=0.8e-3, V=3.5, p_gauge=0.8e6,
        phase=Phase.LIQUID, rating=300, mat=SS316,
    ),
}


@pytest.mark.parametrize("name", list(CASES))
def test_cross_case(name: str) -> None:
    spec = dict(CASES[name])
    mat: MaterialProperties = spec.pop("mat")  # type: ignore[assignment]
    inp = _input(**spec)  # type: ignore[arg-type]
    result = verify(inp, mat, EngineOptions())
    sf = 62.8e6 if spec["conn"] is ConnectionType.FLANGED else 20.7e6
    expected = tapered_case(
        A=spec["A"], B=spec["B"], d=spec["d"], L=spec["L"], b=spec["b"], t=spec["t"],
        L0=spec["L0"], E=mat.elastic_modulus, Eref=mat.elastic_modulus_reference,
        rho_m=mat.density, S=mat.allowable_stress, Sf=sf, rho=spec["rho"], mu=spec["mu"],
        V=spec["V"], P=spec["p_gauge"], kt_threaded=spec["conn"] is ConnectionType.THREADED,
        hc_mode="threaded" if spec["conn"] is ConnectionType.THREADED else "semi",
    )
    ratio_limit = expected.pop("ratio_limit")
    for symbol, value in expected.items():
        scope = "" if symbol in ("P_c", "P_t") else "max"
        assert result.trace.value(symbol, scope) == pytest.approx(value, rel=0.01), symbol
    assert result.cases[0].frequency_ratio_limit == ratio_limit


def test_case_3_uses_low_density_rule() -> None:
    spec = dict(CASES["gas_recto_bridado"])
    mat = spec.pop("mat")
    result = verify(_input(**spec), mat)  # type: ignore[arg-type]
    freq = result.worst("frequency_limit")
    assert freq is not None
    assert freq.message_key == "check.frequency_scruton_inline"
    assert result.cases[0].v_ir is None


def test_case_4_low_reynolds_branch() -> None:
    spec = dict(CASES["liquido_viscoso_roscado"])
    mat = spec.pop("mat")
    result = verify(_input(**spec), mat)  # type: ignore[arg-type]
    re = result.trace.value("Re", "max")
    assert 22 < re < 1300
    assert result.trace.value("K_t_SP", "max") == 2.3


def test_si_imperial_invariance() -> None:
    """El resultado no depende del sistema de unidades en que se cargaron los datos."""
    spec = dict(CASES["agua_conico_protegido"])
    mat = spec.pop("mat")
    a = verify(_input(**spec), mat)  # type: ignore[arg-type]
    kinds = {"A": Q.DIAMETER, "B": Q.DIAMETER, "d": Q.DIAMETER, "L": Q.LENGTH, "t": Q.LENGTH,
             "b": Q.LENGTH, "L0": Q.LENGTH, "rho": Q.DENSITY, "mu": Q.DYNAMIC_VISCOSITY,
             "V": Q.VELOCITY, "p_gauge": Q.PRESSURE}
    imperial = dict(spec)
    for key, kind in kinds.items():
        shown, _ = to_display(spec[key], kind, UnitSystem.IMPERIAL)  # type: ignore[arg-type]
        imperial[key] = from_display(shown, kind, UnitSystem.IMPERIAL)
    b = verify(_input(**imperial), mat)  # type: ignore[arg-type]
    for e1, e2 in zip(a.trace, b.trace, strict=True):
        assert math.isclose(e1.value, e2.value, rel_tol=1e-9)
