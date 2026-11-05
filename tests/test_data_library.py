"""Biblioteca de datos, propiedades de fluidos y selección de materiales."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from thermowell_sizer.core.models import FatigueClass, Phase, PropertySource
from thermowell_sizer.core.ptc19_3.verify import verify
from thermowell_sizer.data import seed_materials
from thermowell_sizer.data.database import Library
from thermowell_sizer.data.selection import ServiceConditions, Verdict, recommend_materials
from thermowell_sizer.i18n.catalog import CATALOG
from thermowell_sizer.properties.fluids import FluidPropertyError, fluid_state, gas_density

C = 273.15


@pytest.fixture(scope="module")
def lib() -> Library:
    return Library()


def test_all_seed_materials_loaded(lib: Library) -> None:
    ids = {m.id for m in lib.materials()}
    assert ids == {m.id for m in seed_materials.MATERIALS}
    assert all(not m.verified for m in lib.materials())


def test_material_interpolation(lib: Library) -> None:
    props = lib.material_properties("SS316", 300 + C, 325 + C)
    assert props.elastic_modulus == pytest.approx(176e9)
    assert props.allowable_stress == pytest.approx(124e6)
    assert props.allowable_stress_design == pytest.approx(122.5e6)
    assert props.fatigue_class is FatigueClass.B
    assert props.stress_corrosion_susceptible
    # Fuera del rango se toma el extremo.
    assert lib.property_at("A105", "allowable_stress", 600 + C) == pytest.approx(74e6)


def test_material_errors(lib: Library) -> None:
    with pytest.raises(KeyError):
        lib.material("XX")
    with pytest.raises(KeyError):
        lib.property_at("A105", "yield_strength", 300.0)


def test_library_material_runs_engine(lib: Library, calc_input) -> None:  # type: ignore[no-untyped-def]
    props = lib.material_properties("F22", 400 + C, 420 + C)
    result = verify(calc_input, props)
    assert result.checks


def test_ti_fatigue_not_covered(lib: Library, calc_input) -> None:  # type: ignore[no-untyped-def]
    props = lib.material_properties("TI2", 100 + C, 120 + C)
    assert not props.fatigue_table_covered


def test_flange_ratings(lib: Library) -> None:
    assert lib.flange_rating("1.1", 150, 38 + C) == pytest.approx(19.6e5)
    assert lib.flange_rating("1.1", 600, 38 + C) == pytest.approx(102.2e5)
    mid = lib.flange_rating("2.2", 300, 75 + C)
    assert mid == pytest.approx((48.1e5 + 42.2e5) / 2)
    assert lib.flange_rating("1.1", 300, 600 + C) is None
    assert lib.flange_rating(None, 300, 300.0) is None
    assert lib.flange_rating("9.9", 300, 300.0) is None
    assert "2.1" in lib.flange_groups()


def test_pipes(lib: Library) -> None:
    pipe = lib.pipe("4", "40")
    assert pipe.dn == 100
    assert pipe.inner_diameter == pytest.approx(4.026 * 0.0254)
    sizes = lib.pipe_sizes()
    assert sizes[0] == "1/2" and sizes[-1] == "24"
    assert "160" in lib.schedules("2")
    with pytest.raises(KeyError):
        lib.pipe("4", "999")


def test_fluids_and_sensors(lib: Library) -> None:
    assert lib.fluid("water").coolprop_name == "Water"
    with pytest.raises(KeyError):
        lib.fluid("nope")
    assert lib.tabulated_fluid("water", 300.0) is None
    rho, mu = lib.tabulated_fluid("diesel", 15 + C) or (0, 0)
    assert rho == pytest.approx(840) and mu == pytest.approx(4e-3)
    assert len(lib.sensors()) >= 10


def test_glossary_standards_compat(lib: Library) -> None:
    assert len(lib.glossary()) > 30
    assert any(s[0] == "ASME-PTC-19.3-TW" for s in lib.standards())
    assert lib.compatibility("N04400")["hf"] == "A"
    assert {"STELLITE6", "STELLITE1", "WC_HVOF", "PTFE", "PVDF", "TANTALUM",
            "CERAMIC"} <= {c[0] for c in lib.coatings()}


@pytest.mark.parametrize(("query", "ref"), [
    ("termopozo", "thermowell"), ("termoposo", "thermowell"), ("estelita", "STELLITE6"),
    ("316", "SS316"), ("Hastelloy", "N10276"),
])
def test_search(lib: Library, query: str, ref: str) -> None:
    assert ref in [h.ref_id for h in lib.search(query)]


def test_search_empty(lib: Library) -> None:
    assert lib.search("   ") == []


def test_user_data_survives_reseed(tmp_path: Path) -> None:
    db = tmp_path / "lib.sqlite"
    lib = Library(db)
    base = lib.material("SS316")
    info = replace(base, id="MY316", name="Mi 316", user_defined=True)
    lib.add_user_material(info, 195e9, [(293.15, 195e9), (873.15, 153e9)],
                          [(293.15, 138e6), (873.15, 90e6)])
    lib.add_user_fluid("custom:aceite", "Aceite", "liquid",
                       [(293.15, 900.0, 0.05), (373.15, 850.0, 0.01)])
    lib.conn.execute("UPDATE meta SET value = 'old' WHERE key = 'seed_version'")
    lib.conn.commit()
    lib.close()
    again = Library(db)
    assert again.material("MY316").user_defined
    assert again.property_at("MY316", "elastic_modulus", 873.15) == pytest.approx(153e9)
    state = fluid_state(again, "custom:aceite", 293.15, 1e5)
    assert state.properties.source is PropertySource.USER
    assert len(again.materials()) == len(seed_materials.MATERIALS) + 1
    again.close()


def test_coolprop_water_phases(lib: Library) -> None:
    liquid = fluid_state(lib, "water", 300 + C, 10e6)
    assert liquid.phase is Phase.LIQUID
    assert liquid.properties.density == pytest.approx(715.3, rel=1e-3)
    steam = fluid_state(lib, "water", 400 + C, 10e6)
    assert steam.phase is Phase.STEAM
    assert steam.saturation_temperature == pytest.approx(584.15, abs=0.1)


def test_coolprop_gas_and_mixture(lib: Library) -> None:
    air = fluid_state(lib, "air", 300.0, 101_325.0)
    assert air.phase is Phase.GAS
    assert air.compressibility == pytest.approx(1.0, abs=1e-3)
    ng = fluid_state(lib, "natural_gas", 300.0, 5e6)
    assert ng.properties.source is PropertySource.COOLPROP
    assert 0.8 < (ng.compressibility or 0) < 0.95


def test_fluid_errors(lib: Library) -> None:
    with pytest.raises(FluidPropertyError):
        fluid_state(lib, "nope", 300.0, 1e5)
    with pytest.raises(FluidPropertyError):
        fluid_state(lib, "water", -5.0, 1e5)


def test_gas_density() -> None:
    assert gas_density(273.15, 101_325.0, 0.028_964_7) == pytest.approx(1.2922, rel=1e-3)


def test_selection_sour_chlorides(lib: Library) -> None:
    cond = ServiceConditions(80 + C, nace_service=True, chlorides_ppm=500)
    evals = recommend_materials(lib, cond)
    by_id = {e.material.id: e for e in evals}
    assert by_id["F91"].verdict is Verdict.NOT_RECOMMENDED
    assert "sel.chloride_scc" in by_id["SS316"].reasons
    assert evals[0].verdict is Verdict.RECOMMENDED
    assert evals[0].material.id in {"D2205", "SD2507", "N06625", "N10276"}


def test_selection_temperature_and_agents(lib: Library) -> None:
    hot = {e.material.id: e for e in recommend_materials(lib, ServiceConditions(550 + C))}
    assert hot["D2205"].verdict is Verdict.NOT_RECOMMENDED
    assert "sel.temp_near_limit" in hot["F22"].reasons
    cold = {e.material.id: e for e in recommend_materials(
        lib, ServiceConditions(20 + C, min_temperature=-100 + C, agents=("hf", "xyz")))}
    assert cold["A105"].verdict is Verdict.NOT_RECOMMENDED
    assert "sel.agent_unknown:xyz" in cold["N04400"].reasons
    assert "sel.agent_c:hf" in cold["SS316"].reasons


def test_selection_erosive(lib: Library) -> None:
    ev = recommend_materials(lib, ServiceConditions(600 + C, erosive=True))
    ss = next(e for e in ev if e.material.id == "SS316")
    assert set(ss.coatings) == {"STELLITE6", "STELLITE1", "CRC_HVOF"}
    assert "sel.fatigue_not_covered" in next(e for e in ev if e.material.id == "TA").reasons


def test_selection_keys_translated() -> None:
    for key in ("sel.temp_exceeded", "sel.agent_c", "agent.hf", "sel.verdict.acceptable"):
        assert key in CATALOG["es"] and key in CATALOG["en"]
