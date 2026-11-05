"""Orquestador de la verificación según ASME PTC 19.3 TW-2016 (sección 7).

Recorre cada caso de flujo (mín./normal/máx.) y, si hay sobreespesor de corrosión,
los tres casos geométricos del párr. 6-2. En cada paso llama a las funciones puras de
los módulos hermanos, registra el resultado en la traza y arma los criterios con su
semáforo y su margen.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from thermowell_sizer.core import constants as k
from thermowell_sizer.core.models import (
    CalcInput,
    CheckResult,
    CheckStatus,
    ConnectionType,
    EngineOptions,
    FlowBasis,
    FlowCase,
    MaterialProperties,
    MetalState,
    MountingOrientation,
    Phase,
    ShankProfile,
    StrouhalMethod,
)
from thermowell_sizer.core.ptc19_3 import (
    compliance,
    fatigue,
    flow,
    frequency_limits,
    natural_frequency,
    pressure,
    stresses,
)
from thermowell_sizer.core.trace import CalcTrace
from thermowell_sizer.core.units import QuantityKind as Q
from thermowell_sizer.core.validation import Severity, ValidationIssue, validate_geometry

ROOT_CORROSION = "root_corrosion"
TIP_CORROSION = "tip_corrosion"
_STATUS_ORDER = {
    CheckStatus.NOT_APPLICABLE: 0,
    CheckStatus.PASS: 1,
    CheckStatus.WARNING: 2,
    CheckStatus.FAIL: 3,
}
_WELDED_SUPPORT = (ConnectionType.SOCKET_WELD, ConnectionType.WELD_IN)
_DEFAULT_METAL_STATE = {
    ConnectionType.THREADED: MetalState.AS_WELDED,
    ConnectionType.WELD_IN: MetalState.AS_WELDED,
    ConnectionType.SOCKET_WELD: MetalState.AS_WELDED,
    ConnectionType.FLANGED: MetalState.WELDED_MACHINED,
    ConnectionType.VAN_STONE: MetalState.NO_WELDS,
    ConnectionType.SANITARY: MetalState.NO_WELDS,
}


@dataclass(frozen=True, slots=True)
class _Geometry:
    """Geometría de un caso de cálculo (nominal o con corrosión, párr. 6-2)."""

    label: str
    profile: ShankProfile
    L: float
    A: float
    B: float
    d: float
    t: float
    b: float
    Ls: float
    bs: float
    L0: float
    B_nominal: float


@dataclass(frozen=True, slots=True)
class CaseSummary:
    """Valores clave de un caso, para el panel de resultados y las gráficas."""

    scope: str
    flow_case: str
    geometry_case: str
    velocity: float
    reynolds: float
    strouhal: float
    fs: float
    fn: float
    hc: float
    fnc: float
    scruton: float
    frequency_ratio_limit: float | None
    v_ir: float | None
    inline_stress_ok: bool | None
    low_velocity_exempt: bool


@dataclass(slots=True)
class VerificationResult:
    """Resultado completo de un tag."""

    status: CheckStatus
    checks: list[CheckResult]
    cases: list[CaseSummary]
    trace: CalcTrace
    issues: list[ValidationIssue]
    notes: list[str] = field(default_factory=list)

    def worst(self, criterion_id: str) -> CheckResult | None:
        """Devuelve el peor resultado de un criterio entre todos los casos."""
        matching = [c for c in self.checks if c.criterion_id == criterion_id]
        if not matching:
            return None
        return max(matching, key=lambda c: (_STATUS_ORDER[c.status], -c.margin_pct))


def _status(value: float, limit: float, amber_pct: float, *, strict: bool) -> CheckStatus:
    exceeded = value >= limit if strict else value > limit
    if exceeded:
        return CheckStatus.FAIL
    margin = (limit - value) / limit * 100.0
    return CheckStatus.WARNING if margin < amber_pct else CheckStatus.PASS


def _make_check(
    criterion_id: str,
    scope: str,
    value: float,
    limit: float,
    reference: str,
    message_key: str,
    options: EngineOptions,
    *,
    strict: bool = True,
    status: CheckStatus | None = None,
) -> CheckResult:
    margin = (limit - value) / limit * 100.0 if limit else 0.0
    return CheckResult(
        criterion_id=criterion_id,
        flow_case=scope,
        status=status or _status(value, limit, options.amber_margin_pct, strict=strict),
        value=value,
        limit=limit,
        margin_pct=margin,
        reference=reference,
        message_key=message_key,
    )


def _not_applicable(criterion_id: str, scope: str, reference: str, key: str) -> CheckResult:
    return CheckResult(
        criterion_id=criterion_id,
        flow_case=scope,
        status=CheckStatus.NOT_APPLICABLE,
        value=0.0,
        limit=0.0,
        margin_pct=0.0,
        reference=reference,
        message_key=key,
    )


def resolve_velocity(case: FlowCase, density: float, pipe_inner_diameter: float,
                     standard_density: float | None = None) -> float:
    """Velocidad del fluido para un caso de flujo, m/s (párr. 7-3).

    Para caudal estándar se pasa a caudal másico con la densidad estándar:
    ṁ = Q_std·ρ_std.

    Raises:
        ValueError: caudal estándar sin densidad estándar.
    """
    if case.basis is FlowBasis.VELOCITY:
        assert case.velocity is not None
        return case.velocity
    if case.basis is FlowBasis.MASS_FLOW:
        assert case.mass_flow is not None
        return flow.velocity_from_mass_flow(case.mass_flow, density, pipe_inner_diameter)
    if case.basis is FlowBasis.STANDARD_VOLUME_FLOW:
        assert case.standard_volume_flow is not None
        if standard_density is None:
            raise ValueError("Caudal estándar sin densidad en condiciones estándar")
        return flow.velocity_from_mass_flow(case.standard_volume_flow * standard_density,
                                            density, pipe_inner_diameter)
    assert case.volume_flow is not None
    return flow.velocity_from_volume_flow(case.volume_flow, pipe_inner_diameter)


def case_velocity(inp: CalcInput, case: FlowCase) -> float:
    """Velocidad de un caso de flujo con las propiedades del fluido de la entrada, m/s."""
    props = inp.process.properties
    return resolve_velocity(case, props.density, inp.pipe.inner_diameter,
                            props.standard_density)


def _geometry_cases(inp: CalcInput, options: EngineOptions) -> list[_Geometry]:
    g = inp.thermowell.geometry
    nominal = _Geometry(
        label="",
        profile=g.profile,
        L=g.L,
        A=g.A,
        B=g.B,
        d=g.d,
        t=g.t,
        b=g.b,
        Ls=g.Ls,
        bs=g.bs,
        L0=g.L0,
        B_nominal=g.B,
    )
    cases = [nominal]
    c = g.corrosion_allowance
    if c > 0.0 and options.corrosion_cases:
        # Párr. 6-2 (b) y (c): A y t, o B y t, reducidos en c; el resto nominal.
        cases.append(_replace(nominal, label=ROOT_CORROSION, A=g.A - c, t=g.t - c))
        cases.append(_replace(nominal, label=TIP_CORROSION, B=g.B - c, t=g.t - c))
    return cases


def _replace(g: _Geometry, **changes: float | str) -> _Geometry:
    data = {name: getattr(g, name) for name in g.__dataclass_fields__}
    data.update(changes)
    return _Geometry(**data)


def _scope(flow_label: str, geom_label: str) -> str:
    return f"{flow_label}|{geom_label}" if geom_label else flow_label


def verify(
    inp: CalcInput,
    material: MaterialProperties,
    options: EngineOptions | None = None,
) -> VerificationResult:
    """Verifica un termopozo según ASME PTC 19.3 TW-2016.

    Args:
        inp: datos del tag.
        material: propiedades del material evaluadas a las temperaturas del cálculo.
        options: opciones del motor; por defecto valores conservadores.

    Returns:
        Resultado con el estado global, los criterios, los casos y la traza.
    """
    opts = options or EngineOptions()
    trace = CalcTrace()
    checks: list[CheckResult] = []
    cases: list[CaseSummary] = []
    notes: list[str] = []
    issues = validate_geometry(inp.thermowell.geometry)
    _general_checks(inp, material, opts, issues, checks, notes)

    geometries = _geometry_cases(inp, opts)
    for geom in geometries:
        _pressure_checks(inp, material, opts, geom, trace, checks)
        for flow_case in inp.process.flow_cases:
            summary = _evaluate_case(inp, material, opts, geom, flow_case, trace, checks, notes)
            cases.append(summary)

    status = max(
        (c.status for c in checks),
        key=lambda s: _STATUS_ORDER[s],
        default=CheckStatus.NOT_APPLICABLE,
    )
    return VerificationResult(
        status=status,
        checks=checks,
        cases=cases,
        trace=trace,
        issues=issues,
        notes=list(dict.fromkeys(notes)),
    )


def _general_checks(
    inp: CalcInput,
    material: MaterialProperties,
    opts: EngineOptions,
    issues: list[ValidationIssue],
    checks: list[CheckResult],
    notes: list[str],
) -> None:
    errors = [i for i in issues if i.severity is Severity.ERROR]
    checks.append(
        CheckResult(
            criterion_id="scope",
            flow_case="",
            status=CheckStatus.FAIL if errors else CheckStatus.PASS,
            value=float(len(errors)),
            limit=0.0,
            margin_pct=0.0,
            reference=k.ref("Section 1, Tables 4-1-1 and 4-2-1"),
            message_key="check.scope_fail" if errors else "check.scope_ok",
        )
    )
    if material.max_temperature is not None:
        checks.append(
            _make_check(
                "material_temperature",
                "",
                inp.process.design_temperature,
                material.max_temperature,
                material.source_note or k.ref("Section 5"),
                "check.material_temperature",
                opts,
                strict=False,
            )
        )
    process = inp.process
    if process.phase is Phase.TWO_PHASE:
        notes.append("note.two_phase")
    orientation = inp.pipe.orientation
    if orientation is MountingOrientation.ELBOW_TIP_DOWNSTREAM:
        notes.append("note.elbow_downstream")
    elif orientation is MountingOrientation.ELBOW_TIP_UPSTREAM:
        notes.append("note.elbow_upstream")
    elif orientation is MountingOrientation.ANGLED:
        notes.append("note.angled")
    if inp.thermowell.connection.type is ConnectionType.SANITARY:
        notes.append("note.sanitary_compliance")
    if process.operating_temperature > k.HIGH_TEMPERATURE_FE_WARNING:
        notes.append("note.high_temperature_fe")
    if opts.supplier_rating:
        notes.append("note.supplier_rating")
    if not material.fatigue_table_covered and material.fatigue_limit_override is None:
        checks.append(
            CheckResult(
                criterion_id="fatigue_data",
                flow_case="",
                status=CheckStatus.WARNING,
                value=0.0,
                limit=0.0,
                margin_pct=0.0,
                reference=k.ref("para. 6-12.3"),
                message_key="check.fatigue_data_missing",
            )
        )


def _pressure_checks(
    inp: CalcInput,
    material: MaterialProperties,
    opts: EngineOptions,
    g: _Geometry,
    trace: CalcTrace,
    checks: list[CheckResult],
) -> None:
    scope = g.label
    s = material.allowable_stress_design or material.allowable_stress
    p_design = max(inp.process.design_pressure - opts.barometric_pressure, 0.0)
    pc = trace.record(
        "P_c",
        pressure.shank_pressure_rating(s, g.B, g.d),
        kind=Q.PRESSURE,
        reference=k.ref("eq. (6-13-1)"),
        expression=r"P_c = 0.66\,S\left[\frac{2.167}{2B/(B-d)} - 0.0833\right]",
        description_key="trace.pc",
        inputs={"S": (s, Q.STRESS), "B": (g.B, Q.DIAMETER), "d": (g.d, Q.DIAMETER)},
        scope=scope,
    )
    pt = trace.record(
        "P_t",
        pressure.tip_pressure_rating(s, g.t, g.d),
        kind=Q.PRESSURE,
        reference=k.ref("eq. (6-13-2)"),
        expression=r"P_t = \frac{S}{0.13}\left(\frac{t}{d}\right)^2",
        description_key="trace.pt",
        inputs={"S": (s, Q.STRESS), "t": (g.t, Q.LENGTH), "d": (g.d, Q.DIAMETER)},
        scope=scope,
    )
    flanged = inp.thermowell.connection.type in (ConnectionType.FLANGED, ConnectionType.VAN_STONE)
    pf = opts.flange_rating if flanged else None
    pr = trace.record(
        "P_r",
        pressure.pressure_rating(pc, pt, pf),
        kind=Q.PRESSURE,
        reference=k.ref("para. 6-13, Step 3"),
        expression=r"P_r = \min(P_c,\ P_t,\ P_f)" if pf else r"P_r = \min(P_c,\ P_t)",
        description_key="trace.pr",
        inputs={"P_c": (pc, Q.PRESSURE), "P_t": (pt, Q.PRESSURE)}
        | ({"P_f": (pf, Q.PRESSURE)} if pf else {}),
        scope=scope,
    )
    checks.append(
        _make_check(
            "pressure_rating",
            scope,
            p_design,
            pr,
            k.ref("subsection 6-13"),
            "check.pressure_rating",
            opts,
            strict=False,
        )
    )
    if pr > k.SIMPLIFIED_PRESSURE_LIMIT:
        checks.append(
            _make_check(
                "pressure_high_service",
                scope,
                pr,
                k.SIMPLIFIED_PRESSURE_LIMIT,
                k.ref("para. 6-13, Step 1"),
                "check.pressure_high_service",
                opts,
                status=CheckStatus.WARNING,
            )
        )
    if flanged and not g.label:
        if pf is None:
            checks.append(
                _not_applicable(
                    "flange_rating", scope, "ASME B16.5", "check.flange_rating_missing"
                )
            )
        else:
            key = "check.flange_derated" if pf > min(pc, pt) else "check.flange_rating"
            checks.append(
                _make_check("flange_rating", scope, p_design, pf, "ASME B16.5", key, opts,
                            strict=False)
            )


def _low_velocity_exempt(
    v: float, g: _Geometry, material: MaterialProperties, sf: float
) -> bool:
    """Exención por baja velocidad (párr. 6-3.6)."""
    return (
        v < k.LOW_VELOCITY_LIMIT
        and g.A - g.d >= k.LOW_VELOCITY_MIN_A_MINUS_D
        and g.L <= k.LOW_VELOCITY_MAX_L
        and g.A >= g.B >= k.LOW_VELOCITY_MIN_B
        and material.allowable_stress >= k.LOW_VELOCITY_MIN_S
        and sf >= k.LOW_VELOCITY_MIN_SF
        and not material.stress_corrosion_susceptible
    )


def _evaluate_case(
    inp: CalcInput,
    material: MaterialProperties,
    opts: EngineOptions,
    g: _Geometry,
    flow_case: FlowCase,
    trace: CalcTrace,
    checks: list[CheckResult],
    notes: list[str],
) -> CaseSummary:
    scope = _scope(flow_case.label, g.label)
    proc = inp.process
    rho = proc.properties.density
    mu = proc.properties.dynamic_viscosity
    conn = inp.thermowell.connection.type
    threaded = conn is ConnectionType.THREADED
    stepped = g.profile is ShankProfile.STEPPED
    rho_m = material.density
    e = material.elastic_modulus

    def rec(
        symbol: str,
        value: float,
        kind: Q,
        eq: str,
        expr: str,
        desc: str,
        inputs: dict[str, tuple[float, Q]] | None = None,
    ) -> float:
        return trace.record(
            symbol,
            value,
            kind=kind,
            reference=k.ref(eq),
            expression=expr,
            description_key=desc,
            inputs=inputs,
            scope=scope,
        )

    # --- 7-3 / 7-5: velocidad, Reynolds y Strouhal -------------------------------------
    v = rec(
        "V",
        resolve_velocity(flow_case, rho, inp.pipe.inner_diameter,
                         inp.process.properties.standard_density),
        Q.VELOCITY,
        "para. 7-3",
        r"V = \dot m/(\rho A_p)\ \text{o}\ V = Q/A_p",
        "trace.v",
    )
    re = rec(
        "Re",
        flow.reynolds(v, g.B, rho, mu),
        Q.DIMENSIONLESS,
        "eq. (6-4-3)",
        r"Re = \frac{V B \rho}{\mu}",
        "trace.re",
        {"V": (v, Q.VELOCITY), "B": (g.B, Q.DIAMETER), "ρ": (rho, Q.DENSITY),
         "μ": (mu, Q.DYNAMIC_VISCOSITY)},
    )
    if opts.strouhal_method is StrouhalMethod.SIMPLIFIED:
        ns = rec("N_S", k.STROUHAL_HIGH_RE, Q.DIMENSIONLESS, "eq. (6-4-4)", r"N_S = 0.22",
                 "trace.ns")
    else:
        ns = rec(
            "N_S",
            flow.strouhal_correlation(re),
            Q.DIMENSIONLESS,
            "eq. (6-4-2)",
            r"N_S = f(Re)",
            "trace.ns",
            {"Re": (re, Q.DIMENSIONLESS)},
        )
    fs = rec(
        "f_s",
        flow.shedding_frequency(ns, v, g.B),
        Q.FREQUENCY,
        "eq. (6-4-1)",
        r"f_s = N_S \frac{V}{B}",
        "trace.fs",
        {"N_S": (ns, Q.DIMENSIONLESS), "V": (v, Q.VELOCITY), "B": (g.B, Q.DIAMETER)},
    )

    # --- 6-5: frecuencia natural con soporte ideal -------------------------------------
    da = rec(
        "D_a",
        natural_frequency.average_diameter(g.profile, g.A, g.B),
        Q.DIAMETER,
        "para. 6-5.3, Step 1",
        r"D_a = (A+B)/2\ \text{(cónico)};\ D_a = A",
        "trace.da",
        {"A": (g.A, Q.DIAMETER), "B": (g.B, Q.DIAMETER)},
    )
    inertia = rec(
        "I",
        natural_frequency.second_moment(da, g.d),
        Q.DIMENSIONLESS,
        "eq. (6-5-1)",
        r"I = \pi (D_a^4 - d^4)/64",
        "trace.i",
        {"D_a": (da, Q.DIAMETER), "d": (g.d, Q.DIAMETER)},
    )
    m = rec(
        "m",
        natural_frequency.mass_per_length(rho_m, da, g.d),
        Q.DIMENSIONLESS,
        "eq. (6-5-1)",
        r"m = \rho_m \pi (D_a^2 - d^2)/4",
        "trace.m",
        {"ρ_m": (rho_m, Q.DENSITY), "D_a": (da, Q.DIAMETER), "d": (g.d, Q.DIAMETER)},
    )
    fa = rec(
        "f_a",
        natural_frequency.approximate_frequency(e, inertia, m, g.L),
        Q.FREQUENCY,
        "eq. (6-5-1)",
        r"f_a = \frac{1.875^2}{2\pi}\sqrt{\frac{EI}{m}}\frac{1}{L^2}",
        "trace.fa",
        {"E": (e, Q.ELASTIC_MODULUS), "L": (g.L, Q.LENGTH)},
    )
    if stepped:
        hf_value = natural_frequency.hf_stepped(g.A, g.B, g.Ls, g.L, table_b=g.B_nominal)
        hf = rec(
            "H_f",
            hf_value,
            Q.DIMENSIONLESS,
            "eq. (6-5-3)",
            r"H_f = (y_1^{-\beta} + y_2^{-\beta})^{-1/\beta}",
            "trace.hf",
            {"A/B": (g.A / g.B, Q.DIMENSIONLESS), "L_s/L": (g.Ls / g.L, Q.DIMENSIONLESS)},
        )
    else:
        hf = rec(
            "H_f",
            natural_frequency.hf_straight_tapered(g.A, g.B, g.d, g.L, da),
            Q.DIMENSIONLESS,
            "eq. (6-5-2)",
            r"H_f = \frac{0.99[1+(1-B/A)+(1-B/A)^2]}{1+1.1(D_a/L)^{3[1-0.8(d/D_a)]}}",
            "trace.hf",
            {"B/A": (g.B / g.A, Q.DIMENSIONLESS), "D_a/L": (da / g.L, Q.DIMENSIONLESS),
             "d/D_a": (g.d / da, Q.DIMENSIONLESS)},
        )
    if opts.supplier_rating:
        haf = rec("H_af", 1.0, Q.DIMENSIONLESS, "para. 9-2", r"H_{a,f} = 1", "trace.haf")
    else:
        haf = rec(
            "H_af",
            natural_frequency.h_fluid_mass(rho, rho_m),
            Q.DIMENSIONLESS,
            "eq. (6-5-4)",
            r"H_{a,f} = 1 - \frac{\rho}{2\rho_m}",
            "trace.haf",
            {"ρ": (rho, Q.DENSITY), "ρ_m": (rho_m, Q.DENSITY)},
        )
    rho_s = inp.sensor.density or k.DEFAULT_SENSOR_DENSITY
    has = rec(
        "H_as",
        natural_frequency.h_sensor_mass(rho_s, rho_m, da, g.d),
        Q.DIMENSIONLESS,
        "eq. (6-5-5)",
        r"H_{a,s} = 1 - \frac{\rho_s}{2\rho_m}\left[\frac{1}{(D_a/d)^2 - 1}\right]",
        "trace.has",
        {"ρ_s": (rho_s, Q.DENSITY), "ρ_m": (rho_m, Q.DENSITY),
         "D_a/d": (da / g.d, Q.DIMENSIONLESS)},
    )
    fn = rec(
        "f_n",
        natural_frequency.natural_frequency(hf, haf, has, fa),
        Q.FREQUENCY,
        "eq. (6-5-6)",
        r"f_n = H_f H_{a,f} H_{a,s} f_a",
        "trace.fn",
        {"H_f": (hf, Q.DIMENSIONLESS), "H_af": (haf, Q.DIMENSIONLESS),
         "H_as": (has, Q.DIMENSIONLESS), "f_a": (fa, Q.FREQUENCY)},
    )

    # --- 6-6 / 6-7: flexibilidad del soporte -------------------------------------------
    fillet = 0.0 if (threaded or conn in _WELDED_SUPPORT) else g.b
    if opts.support_stiffness is not None:
        hc = rec(
            "H_c",
            compliance.hc_general(opts.support_stiffness, e, g.A, g.d, g.L, fillet),
            Q.DIMENSIONLESS,
            "eq. (6-6-2)",
            r"H_c = 1 - \frac{E}{K_M}\frac{\pi(A^4-d^4)}{32L[1+1.5(b/A)]^2}",
            "trace.hc",
            {"K_M": (opts.support_stiffness, Q.MOMENT), "b": (fillet, Q.LENGTH)},
        )
    elif threaded or conn is ConnectionType.SANITARY:
        hc = rec(
            "H_c",
            compliance.hc_threaded(g.A, g.L),
            Q.DIMENSIONLESS,
            "eq. (6-7-1)",
            r"H_c = 1 - 0.9\,(A/L)",
            "trace.hc",
            {"A/L": (g.A / g.L, Q.DIMENSIONLESS)},
        )
    else:
        hc = rec(
            "H_c",
            compliance.hc_semi_infinite(g.A, g.L, fillet),
            Q.DIMENSIONLESS,
            "eq. (6-6-5)",
            r"H_c = 1 - 0.61\frac{A/L}{[1+1.5(b/A)]^2}",
            "trace.hc",
            {"A/L": (g.A / g.L, Q.DIMENSIONLESS), "b/A": (fillet / g.A, Q.DIMENSIONLESS)},
        )
    fnc = rec(
        "f_nc",
        compliance.installed_frequency(hc, fn),
        Q.FREQUENCY,
        "eq. (6-6-1)",
        r"f_n^c = H_c f_n",
        "trace.fnc",
        {"H_c": (hc, Q.DIMENSIONLESS), "f_n": (fn, Q.FREQUENCY)},
    )
    nsc = rec(
        "N_Sc",
        frequency_limits.scruton(opts.damping, rho_m, rho, g.d, g.B),
        Q.DIMENSIONLESS,
        "eq. (6-8-1)",
        r"N_{Sc} = \pi^2 \zeta (\rho_m/\rho)[1-(d/B)^2]",
        "trace.nsc",
        {"ζ": (opts.damping, Q.DIMENSIONLESS), "ρ_m/ρ": (rho_m / rho, Q.DIMENSIONLESS),
         "d/B": (g.d / g.B, Q.DIMENSIONLESS)},
    )

    # --- Fatiga: límite admisible --------------------------------------------------------
    state = opts.metal_state or _DEFAULT_METAL_STATE[conn]
    sf = material.fatigue_limit_override or fatigue.fatigue_endurance_limit(
        material.fatigue_class, state
    )
    ft = rec(
        "F_T",
        fatigue.temperature_factor(e, material.elastic_modulus_reference),
        Q.DIMENSIONLESS,
        "eq. (6-12-6)",
        r"F_T = E(T)/E_{ref}",
        "trace.ft",
        {"E": (e, Q.ELASTIC_MODULUS), "E_ref": (material.elastic_modulus_reference,
                                                Q.ELASTIC_MODULUS)},
    )
    s_allow_dyn = rec(
        "S_f_adm",
        fatigue.allowable_amplitude(ft, opts.environmental_factor, sf),
        Q.STRESS,
        "eq. (6-12-5)",
        r"F_T F_E S_f",
        "trace.sf_allow",
        {"F_T": (ft, Q.DIMENSIONLESS), "F_E": (opts.environmental_factor, Q.DIMENSIONLESS),
         "S_f": (sf, Q.STRESS)},
    )

    summary_kwargs: dict[str, float | bool | None] = {
        "frequency_ratio_limit": None, "v_ir": None, "inline_stress_ok": None,
    }

    # --- 6-3.6: exención por baja velocidad --------------------------------------------
    if _low_velocity_exempt(v, g, material, sf):
        checks.append(
            _make_check("low_velocity", scope, v, k.LOW_VELOCITY_LIMIT, k.ref("para. 6-3.6"),
                        "check.low_velocity_exempt", opts, status=CheckStatus.PASS)
        )
        return CaseSummary(scope, flow_case.label, g.label, v, re, ns, fs, fn, hc, fnc, nsc,
                           None, None, None, low_velocity_exempt=True)

    # --- 6-10: parámetros geométricos G --------------------------------------------------
    locations: list[tuple[str, float, float, float]] = []  # (id, G, D, Kt)
    if stepped:
        g_sp = rec(
            "G_SP",
            stresses.g_support_stepped(g.L, g.A, g.B, g.d, g.Ls, g.L0),
            Q.DIMENSIONLESS,
            "eqs. (6-10-9), (6-10-11)",
            r"G_{SP} = \frac{16L^2}{\pi A^2[1-(d/A)^4]}\{B/A + [1-B/A][1-L_s/L]^2\}",
            "trace.gsp",
        )
        g_rd = rec(
            "G_RD",
            stresses.g_step_base(g.L, g.B, g.d, g.Ls, g.L0),
            Q.DIMENSIONLESS,
            "eqs. (6-10-10), (6-10-12)",
            r"G_{RD} = \frac{16L_s^2}{\pi B^2[1-(d/B)^4]}",
            "trace.grd",
        )
    else:
        g_sp = rec(
            "G_SP",
            stresses.g_support_tapered(g.L, g.A, g.B, g.d, g.L0),
            Q.DIMENSIONLESS,
            "eqs. (6-10-7), (6-10-8)",
            r"G_{SP} = \frac{16L^2}{3\pi A^2[1-(d/A)^4]}[1 + 2(B/A)]",
            "trace.gsp",
        )
    kt_sp = rec(
        "K_t_SP",
        stresses.stress_concentration(g.A, fillet, threaded=threaded),
        Q.DIMENSIONLESS,
        "eq. (6-12-4)",
        r"K_t = 1.1 + 0.033(A/b)\ \text{o}\ 2.2",
        "trace.kt",
        {"A": (g.A, Q.DIAMETER), "b": (fillet, Q.LENGTH)},
    )
    locations.append(("support", g_sp, g.A, kt_sp))
    if stepped:
        kt_rd = rec(
            "K_t_RD",
            stresses.stress_concentration(g.B, g.bs),
            Q.DIMENSIONLESS,
            "eq. (6-12-4), para. 6-12.4",
            r"K_t = 1.1 + 0.033(B/b_s)\ \text{o}\ 2.2",
            "trace.kt",
            {"B": (g.B, Q.DIAMETER), "b_s": (g.bs, Q.LENGTH)},
        )
        locations.append(("step", g_rd, g.B, kt_rd))

    # --- 6-11 / 6-12.2: esfuerzo estacionario -----------------------------------------
    p_op = max(proc.operating_pressure - opts.barometric_pressure, 0.0)
    pd_steady = rec(
        "P_D",
        flow.dynamic_pressure(k.DRAG_COEFF_STEADY, rho, v),
        Q.PRESSURE,
        "eq. (6-3-3)",
        r"P_D = \tfrac12 \rho C_D V^2",
        "trace.pd_steady",
        {"ρ": (rho, Q.DENSITY), "C_D": (k.DRAG_COEFF_STEADY, Q.DIMENSIONLESS),
         "V": (v, Q.VELOCITY)},
    )
    s_static_limit = k.VON_MISES_FACTOR * material.allowable_stress
    for loc, g_val, diameter, _ in locations:
        sr = rec(f"S_r_{loc}", stresses.radial_pressure_stress(p_op), Q.STRESS, "eq. (6-11-1)",
                 r"S_r = P", "trace.sr", {"P": (p_op, Q.PRESSURE)})
        st = rec(f"S_t_{loc}", stresses.tangential_pressure_stress(p_op, g.d, diameter),
                 Q.STRESS, "eq. (6-11-2)", r"S_t = P\frac{1+(d/D)^2}{1-(d/D)^2}", "trace.st",
                 {"P": (p_op, Q.PRESSURE), "d/D": (g.d / diameter, Q.DIMENSIONLESS)})
        sa = rec(f"S_a_{loc}", stresses.axial_pressure_stress(p_op, g.d, diameter), Q.STRESS,
                 "eq. (6-11-3)", r"S_a = \frac{P}{1-(d/D)^2}", "trace.sa",
                 {"P": (p_op, Q.PRESSURE), "d/D": (g.d / diameter, Q.DIMENSIONLESS)})
        sd = rec(f"S_D_{loc}", stresses.steady_drag_stress(g_val, pd_steady), Q.STRESS,
                 "eq. (6-10-4)", r"S_D = G P_D", "trace.sd_steady",
                 {"G": (g_val, Q.DIMENSIONLESS), "P_D": (pd_steady, Q.PRESSURE)})
        smax = rec(f"S_max_{loc}", stresses.max_steady_stress(sd, sa), Q.STRESS,
                   "eq. (6-12-1)", r"S_{max} = S_D + S_a", "trace.smax")
        vm = rec(f"S_vm_{loc}", stresses.von_mises(smax, sr, st), Q.STRESS, "eq. (6-12-2)",
                 r"\sqrt{\tfrac12[(S_{max}-S_r)^2+(S_{max}-S_t)^2+(S_t-S_r)^2]}",
                 "trace.vm")
        checks.append(
            _make_check(f"steady_stress_{loc}", scope, vm, s_static_limit,
                        k.ref("eq. (6-12-2)"), "check.steady_stress", opts, strict=False)
        )

    # --- Sin desprendimiento de vórtices ------------------------------------------------
    if ns <= 0.0:
        checks.append(_not_applicable("frequency_limit", scope, k.ref("eq. (6-4-2)"),
                                      "check.no_vortex_shedding"))
        return CaseSummary(scope, flow_case.label, g.label, v, re, ns, fs, fn, hc, fnc, nsc,
                           None, None, None, low_velocity_exempt=False)

    # --- 6-9 / 6-10 / 6-12.3: esfuerzo dinámico a la velocidad de diseño ---------------
    r = rec("r", fs / fnc, Q.DIMENSIONLESS, "eq. (6-9-1)", r"r = f_s/f_n^c", "trace.r")
    r_inline = rec("r_prime", 2.0 * fs / fnc, Q.DIMENSIONLESS, "eq. (6-9-2)",
                   r"r' = 2f_s/f_n^c", "trace.r_prime")
    fm = rec("F_M", frequency_limits.magnification(r, opts.damping), Q.DIMENSIONLESS,
             "eqs. (6-9-1), (6-9-3)", r"F_M = \frac{1}{1-r^2}", "trace.fm")
    fm_inline = rec("F_M_prime", frequency_limits.magnification(r_inline, opts.damping),
                    Q.DIMENSIONLESS, "eqs. (6-9-2), (6-9-3)", r"F'_M = \frac{1}{1-r'^2}",
                    "trace.fm_prime")
    pd_osc = rec("P_d", flow.dynamic_pressure(k.DRAG_COEFF_OSC, rho, v), Q.PRESSURE,
                 "eq. (6-3-3)", r"P_d = \tfrac12 \rho C_d V^2", "trace.pd_osc")
    pl_osc = rec("P_l", flow.dynamic_pressure(k.LIFT_COEFF_OSC, rho, v), Q.PRESSURE,
                 "eq. (6-3-3)", r"P_l = \tfrac12 \rho C_l V^2", "trace.pl_osc")
    for loc, g_val, _, kt in locations:
        s_d = rec(f"S_d_{loc}", stresses.oscillating_stress(g_val, fm_inline, pd_osc),
                  Q.STRESS, "eq. (6-10-6)", r"S_d = G F'_M P_d", "trace.sd_osc")
        s_l = rec(f"S_L_{loc}", stresses.oscillating_stress(g_val, fm, pl_osc), Q.STRESS,
                  "eq. (6-10-5)", r"S_L = G F_M P_l", "trace.sl_osc")
        s_o = rec(f"S_o_{loc}", stresses.peak_oscillating_stress(kt, s_d, s_l), Q.STRESS,
                  "eq. (6-12-3)", r"S_{o,max} = K_t\sqrt{S_d^2 + S_L^2}", "trace.so",
                  {"K_t": (kt, Q.DIMENSIONLESS), "S_d": (s_d, Q.STRESS),
                   "S_L": (s_l, Q.STRESS)})
        checks.append(
            _make_check(f"dynamic_stress_{loc}", scope, s_o, s_allow_dyn,
                        k.ref("eq. (6-12-5)"), "check.dynamic_stress", opts)
        )

    # --- 6-8: límite de frecuencia ------------------------------------------------------
    ratio_limit, message, extra_status = _frequency_limit(
        inp, opts, g, scope, locations, rec, re, ns, nsc, fnc, v, rho, mu, s_allow_dyn,
        ft, summary_kwargs, notes,
    )
    summary_kwargs["frequency_ratio_limit"] = ratio_limit
    if fs >= fnc:
        message = "check.frequency_supercritical"
    checks.append(
        _make_check("frequency_limit", scope, fs, ratio_limit * fnc,
                    k.ref("subsection 6-8"), message, opts, status=extra_status
                    if extra_status is not None and fs < ratio_limit * fnc else None)
    )
    if ratio_limit == k.RATIO_TRANSVERSE_LIMIT and summary_kwargs["inline_stress_ok"] is not None:
        in_band = k.RATIO_INLINE_LIMIT * fnc <= fs <= k.RATIO_LOCKIN_UPPER * fnc
        checks.append(
            CheckResult(
                criterion_id="inline_lockin_dwell",
                flow_case=scope,
                status=CheckStatus.FAIL if in_band else CheckStatus.PASS,
                value=fs / fnc,
                limit=k.RATIO_INLINE_LIMIT,
                margin_pct=0.0,
                reference=k.ref("eqs. (6-8-8), (6-8-9)"),
                message_key="check.lockin_dwell" if in_band else "check.lockin_clear",
            )
        )
    return CaseSummary(
        scope, flow_case.label, g.label, v, re, ns, fs, fn, hc, fnc, nsc,
        ratio_limit,
        summary_kwargs["v_ir"],
        summary_kwargs["inline_stress_ok"],  # type: ignore[arg-type]
        low_velocity_exempt=False,
    )


class _Recorder(Protocol):
    def __call__(
        self,
        symbol: str,
        value: float,
        kind: Q,
        eq: str,
        expr: str,
        desc: str,
        inputs: dict[str, tuple[float, Q]] | None = None,
    ) -> float: ...


def _frequency_limit(
    inp: CalcInput,
    opts: EngineOptions,
    g: _Geometry,
    scope: str,
    locations: list[tuple[str, float, float, float]],
    rec: _Recorder,
    re: float,
    ns: float,
    nsc: float,
    fnc: float,
    v: float,
    rho: float,
    mu: float,
    s_allow_dyn: float,
    ft: float,
    summary: dict[str, float | bool | None],
    notes: list[str],
) -> tuple[float, str, CheckStatus | None]:
    """Determina la relación fs/f_n^c admisible (párrs. 6-8.2 a 6-8.5)."""
    if re < k.RE_LOW_DENSITY_LIMIT and nsc > k.SCRUTON_ALL_SUPPRESSED:
        notes.append("note.higher_modes")
        return k.RATIO_TRANSVERSE_LIMIT, "check.frequency_scruton_all", None
    if re < k.RE_LOW_DENSITY_LIMIT and nsc > k.SCRUTON_INLINE_SUPPRESSED:
        return k.RATIO_TRANSVERSE_LIMIT, "check.frequency_scruton_inline", None

    # Caso general (párr. 6-8.3): esfuerzo cíclico en la resonancia en línea.
    if opts.strouhal_method is StrouhalMethod.SIMPLIFIED:
        v_ir = rec("V_IR", frequency_limits.inline_resonance_velocity_simplified(g.B, fnc, ns),
                   Q.VELOCITY, "eq. (6-8-5)", r"V_{IR} = \frac{B f_n^c}{2N_S}", "trace.vir")
    else:
        v_ir = rec(
            "V_IR",
            frequency_limits.inline_resonance_velocity(g.B, fnc, ns, re, v, rho, mu),
            Q.VELOCITY,
            "eqs. (6-8-3), (6-8-4)",
            r"V_{IR} = \frac{B f_n^c}{2N_S}[\ldots]",
            "trace.vir",
            {"B": (g.B, Q.DIAMETER), "f_n^c": (fnc, Q.FREQUENCY), "N_S": (ns, Q.DIMENSIONLESS),
             "Re": (re, Q.DIMENSIONLESS)},
        )
    summary["v_ir"] = v_ir
    fm_max = frequency_limits.max_magnification(opts.damping)
    pd_ir = rec("P_d_IR", flow.dynamic_pressure(k.DRAG_COEFF_OSC, rho, v_ir), Q.PRESSURE,
                "eq. (6-3-3)", r"P_d = \tfrac12 \rho C_d V_{IR}^2", "trace.pd_ir")
    ir_stresses: list[float] = []
    for loc, g_val, _, kt in locations:
        s_d_ir = rec(f"S_d_IR_{loc}", stresses.oscillating_stress(g_val, fm_max, pd_ir),
                     Q.STRESS, "eq. (6-10-6), para. 6-8.3", r"S_d = G\,\frac{1}{2\zeta}\,P_d",
                     "trace.sd_ir")
        s_o_ir = rec(f"S_o_IR_{loc}", stresses.peak_oscillating_stress(kt, s_d_ir, 0.0),
                     Q.STRESS, "eq. (6-12-3), para. 6-8.3", r"S_{o,max} = K_t S_d",
                     "trace.so_ir")
        ir_stresses.append(s_o_ir)
    ok = max(ir_stresses) < s_allow_dyn
    summary["inline_stress_ok"] = ok
    if ok:
        return k.RATIO_TRANSVERSE_LIMIT, "check.frequency_inline_ok", None

    passage_allowed = (
        opts.allow_inline_passage
        and inp.process.phase in (Phase.GAS, Phase.STEAM)
        and opts.finite_life_fatigue_limit is not None
    )
    if passage_allowed:
        assert opts.finite_life_fatigue_limit is not None
        limit = fatigue.allowable_amplitude(
            ft, opts.environmental_factor, opts.finite_life_fatigue_limit
        )
        if max(ir_stresses) < limit:
            notes.append("note.inline_passage_conditions")
            summary["inline_stress_ok"] = False
            return k.RATIO_TRANSVERSE_LIMIT, "check.frequency_inline_passage", CheckStatus.WARNING
    return k.RATIO_INLINE_LIMIT, "check.frequency_inline_limited", None

