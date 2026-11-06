"""Fase 8: caudal estándar, recomendaciones, diseños típicos, perfiles y plano acotado."""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path

import pytest

from thermowell_sizer.core.advisories import (
    AdvisoryLevel,
    advise,
    dial_range,
    erosional_velocity,
    inspection_plan,
)
from thermowell_sizer.core.designs import (
    BORE_260,
    DESIGNS_BY_ID,
    STANDARD_U,
    TYPICAL_DESIGNS,
    build_choice,
    load_profile,
    load_profiles,
    profile_choice,
    recommended_u,
    select_model,
)
from thermowell_sizer.core.models import (
    CalcInput,
    ConnectionType,
    FlowBasis,
    FlowCase,
    MountingOrientation,
    ShankProfile,
    ThermowellGeometry,
)
from thermowell_sizer.core.ptc19_3.verify import case_velocity, resolve_velocity
from thermowell_sizer.core.sketch import (
    SKETCH_LABELS_ES,
    Painter,
    SketchText,
    build_sketch,
    render,
)
from thermowell_sizer.core.tools.converter import convert
from thermowell_sizer.data.reference import REFERENCE_TABLES
from thermowell_sizer.i18n import Language, tr
from thermowell_sizer.services import default_input

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def _with_geometry(inp: CalcInput, **fields: object) -> CalcInput:
    g = inp.thermowell.geometry.model_copy(update=fields)
    return inp.model_copy(update={"thermowell": inp.thermowell.model_copy(
        update={"geometry": ThermowellGeometry.model_validate(g.model_dump())})})


# --- Caudal estándar ---------------------------------------------------------------
def test_standard_flow_uses_standard_density() -> None:
    case = FlowCase(label="max", basis=FlowBasis.STANDARD_VOLUME_FLOW,
                    standard_volume_flow=1.0)
    # 1 Sm³/s con ρstd = 0,7 kg/m³ → 0,7 kg/s; con ρ = 35 kg/m³ y A = 0,01 m² → 2 m/s
    area_d = (4 * 0.01 / 3.141592653589793) ** 0.5
    v = resolve_velocity(case, 35.0, area_d, standard_density=0.7)
    assert v == pytest.approx(2.0, rel=1e-9)


def test_standard_flow_requires_standard_density() -> None:
    case = FlowCase(label="max", basis=FlowBasis.STANDARD_VOLUME_FLOW,
                    standard_volume_flow=1.0)
    with pytest.raises(ValueError):
        resolve_velocity(case, 35.0, 0.1)


def test_converter_standard_flow() -> None:
    # 1 MMSCFD ≈ 1177 Sm³/h (15 °C)
    assert convert(1.0, "standard_volume_flow", "MMSCFD", "Sm³/h") == pytest.approx(1177.2,
                                                                                     rel=2e-3)
    # Nm³ (0 °C) → Sm³ (15 °C): factor 288,15 / 273,15
    assert convert(1.0, "standard_volume_flow", "Nm³/h", "Sm³/h") == pytest.approx(
        288.15 / 273.15, rel=1e-9)


# --- Recomendaciones ---------------------------------------------------------------
def test_erosional_velocity_api14e() -> None:
    # C = 100 lb/(ft·s²)^0,5 y ρ = 1000 kg/m³ → ≈ 3,86 m/s
    assert erosional_velocity(1000.0) == pytest.approx(3.86, rel=0.01)


def test_tip_hitting_wall_is_critical() -> None:
    inp = default_input("T")
    inp = _with_geometry(inp, L=0.9 * inp.pipe.inner_diameter + 0.05,
                         U=0.9 * inp.pipe.inner_diameter + 0.05)
    keys = {a.key: a.level for a in advise(inp)}
    assert keys.get("adv.tip_hits_wall") is AdvisoryLevel.CRITICAL


def test_advisories_sorted_by_severity() -> None:
    inp = default_input("T")
    inp = _with_geometry(inp, L=0.5, U=0.5)
    levels = [a.level for a in advise(inp)]
    order = [AdvisoryLevel.CRITICAL, AdvisoryLevel.WARNING, AdvisoryLevel.INFO]
    assert levels == sorted(levels, key=order.index)


def test_dial_range_middle_third() -> None:
    low, high = dial_range(80.0, 100.0) or (0.0, 0.0)
    assert low + (high - low) / 3 <= 80.0 <= low + 2 * (high - low) / 3
    assert high >= 100.0


def test_all_advisory_texts_exist() -> None:
    inp = default_input("T")
    for adv in [*advise(inp), *inspection_plan(inp)]:
        for lang in Language:
            assert tr(adv.key, lang) != adv.key
            assert tr(f"{adv.key}_short", lang) != f"{adv.key}_short" or \
                not adv.key.startswith("insp.")


def test_inspection_plan_follows_connection() -> None:
    inp = default_input("T")
    keys = [a.key for a in inspection_plan(inp)]
    assert "insp.hydro" in keys and "insp.marking" in keys
    assert ("insp.weld_flange" in keys) == (
        inp.thermowell.connection.type is ConnectionType.FLANGED)


# --- Diseños típicos y perfiles ------------------------------------------------------
@pytest.mark.parametrize("design", TYPICAL_DESIGNS, ids=lambda d: d.id)
def test_typical_designs_build_valid_geometry(design: object) -> None:
    from thermowell_sizer.core.designs import TypicalDesign

    assert isinstance(design, TypicalDesign)
    for bore in design.diameters:
        u = max(STANDARD_U[2], design.min_u)
        c = build_choice(design, size=design.sizes[0], bore=bore, U=u, nozzle_length=0.1,
                         rating_class=300)
        g = ThermowellGeometry(profile=c.profile, L=c.L, U=c.U, A=c.A, B=c.B, d=c.d, t=c.t,
                               Ls=c.Ls, L0=c.L0)
        assert pytest.approx(u) == g.L
        assert pytest.approx(0.1) == c.L0
        assert (c.rating_class is not None) == design.rating_required


def test_unlisted_bore_keeps_minimum_wall() -> None:
    design = DESIGNS_BY_ID["threaded_stepped"]
    c = build_choice(design, size="3/4 NPT", bore=0.012, U=0.2)
    assert c.B - c.d >= 2 * 3.2e-3 - 1e-12


def test_recommended_u_is_standard_and_inside_pipe() -> None:
    u = recommended_u(0.30323, 0.15)
    assert any(u == pytest.approx(s) for s in STANDARD_U)
    assert 0.15 + 0.30323 / 3 <= u <= 0.15 + 0.9 * 0.30323


def test_example_profile_selection() -> None:
    profile = load_profile(EXAMPLES / "perfil_ejemplo.json")
    sel = select_model(profile, connection=ConnectionType.FLANGED, nps="10", rating_class=300,
                       elbow=False)
    assert sel.model == "F2" and sel.nps_used == "8"
    big = select_model(profile, connection=ConnectionType.FLANGED, nps="24", rating_class=150,
                       elbow=False)
    assert big.model == "F3" and big.nps_used == "12"
    small = select_model(profile, connection=ConnectionType.FLANGED, nps="2",
                         rating_class=150, elbow=False)
    assert small.model is None and small.reason == "line_too_small"
    banned = select_model(profile, connection=ConnectionType.THREADED, nps="2",
                          rating_class=150, elbow=False)
    assert banned.model is None and banned.reason == "not_allowed"
    none = select_model(profile, connection=ConnectionType.FLANGED, nps="6", rating_class=2500,
                        elbow=False)
    assert none.reason == "no_rule"


def test_profile_choice_overrides_and_nozzle() -> None:
    profile = load_profile(EXAMPLES / "perfil_ejemplo.json")
    c = profile_choice(profile, "F3", nozzle_length=profile.nozzle_length(300, "F3") or 0.0,
                       rating_class=300)
    assert pytest.approx((0.027, 0.019, 0.4, 0.15)) == (c.A, c.B, c.U, c.L0)
    assert c.d == pytest.approx(0.0066)
    assert profile.nozzle_length(300, "T1") == pytest.approx(0.05)
    assert profile.nozzle_length(900) == pytest.approx(0.2)


def test_invalid_profiles_are_rejected(tmp_path: Path) -> None:
    data = json.loads((EXAMPLES / "perfil_ejemplo.json").read_text(encoding="utf-8"))
    data["rules"][0]["by_nps"]["3"] = "ZZ"
    bad = tmp_path / "malo.json"
    bad.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="ZZ"):
        load_profile(bad)
    (tmp_path / "roto.json").write_text("{", encoding="utf-8")
    assert load_profiles(tmp_path) == []
    assert load_profiles(None) == []


# --- Plano acotado -------------------------------------------------------------------
class _Recorder(Painter):
    def __init__(self) -> None:
        self.texts: list[str] = []

    def line(self, x1: float, y1: float, x2: float, y2: float, *, width: float = 0.8,
             dash: bool = False, color: str = "ink") -> None:
        pass

    def polygon(self, pts: Sequence[tuple[float, float]], *, fill: str,
                stroke: bool = True) -> None:
        pass

    def text(self, x: float, y: float, text: str, *, anchor: str = "start") -> None:
        self.texts.append(text)

    def text_width(self, text: str) -> float:
        return 5.0 * len(text)


@pytest.mark.parametrize("conn", list(ConnectionType))
@pytest.mark.parametrize("profile", list(ShankProfile))
def test_sketch_dimensions_every_connection(conn: ConnectionType,
                                            profile: ShankProfile) -> None:
    inp = default_input("T")
    tw = inp.thermowell
    g = tw.geometry.model_copy(update={
        "profile": profile, "B": tw.geometry.A if profile is ShankProfile.STRAIGHT
        else tw.geometry.B, "Ls": 0.05 if profile is ShankProfile.STEPPED else 0.0,
        "T_lag": 0.04})
    rating = 300 if conn in (ConnectionType.FLANGED, ConnectionType.VAN_STONE) else None
    well = tw.model_copy(update={"geometry": g, "connection": tw.connection.model_copy(
        update={"type": conn, "rating_class": rating})})
    pipe = inp.pipe.model_copy(update={"orientation": MountingOrientation.PERPENDICULAR})
    inp = inp.model_copy(update={"thermowell": well, "pipe": pipe})
    tx = SketchText(length=lambda v: f"{v * 1000:.1f} mm",
                    diameter=lambda v: f"{v * 1000:.2f} mm", labels=SKETCH_LABELS_ES)
    sk = build_sketch(inp, tx)
    rec = _Recorder()
    render(sk, rec, 600, 320)
    joined = " | ".join(rec.texts)
    for label in ("U · Largo de inserción", "Largo total", "Ø raíz A", "Ø punta B",
                  "Ø agujero d"):
        assert label in joined
    if conn is ConnectionType.THREADED:
        assert "I · Largo de rosca" in joined
    if conn is ConnectionType.FLANGED:
        assert "E · Espesor de brida" in joined


# --- Referencias --------------------------------------------------------------------
def test_reference_tables_are_rectangular() -> None:
    ids = set()
    for table in REFERENCE_TABLES:
        ids.add(table.id)
        assert table.rows
        for row in table.rows:
            assert len(row) == len(table.headers), table.id
    assert {"tc_colors", "rtd_classes", "designs", "corrosion"} <= ids


def test_case_velocity_matches_resolve() -> None:
    inp = default_input("T")
    for case in inp.process.flow_cases:
        assert case_velocity(inp, case) > 0
    assert pytest.approx(0.006604) == BORE_260
