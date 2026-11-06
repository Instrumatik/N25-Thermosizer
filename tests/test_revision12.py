"""Revisión 1.2: tuberías, fluidos por tipo, conexión sugerida, E/S manuales, Hs, resumen ASME
y fichas «ⓘ»."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from thermowell_sizer.core.designs import CONNECTION_SIZES, suggested_connection_size
from thermowell_sizer.core.models import (
    CheckStatus,
    ConnectionType,
    MaterialRef,
    Phase,
    PipeData,
)
from thermowell_sizer.data.database import Library
from thermowell_sizer.data.fluid_groups import (
    FLUID_TYPES,
    TYPES_BY_ID,
    fluid_label,
    phase_mismatch,
    type_for,
)
from thermowell_sizer.infocards.content import ALIASES, CARDS, SECTIONS, card_for
from thermowell_sizer.infocards.curves import CURVE_IDS, curve
from thermowell_sizer.infocards.render import render_card
from thermowell_sizer.project import ProjectSettings, TagRecord, load_project
from thermowell_sizer.services import default_input, evaluate, with_wall_thickness
from thermowell_sizer.summary import (
    LABELS,
    asme_status,
    calculated_results,
    input_rows,
    length_convention,
)

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


@pytest.fixture(scope="module")
def library() -> Library:
    return Library()


@pytest.fixture(scope="module")
def evaluations(library: Library) -> dict[str, object]:
    out: dict[str, object] = {}
    for path in sorted(EXAMPLES.glob("*.tws")):
        p = load_project(path)
        out[path.stem] = evaluate(p.tags[0], library, p.settings)
    return out


# --- Tuberías -------------------------------------------------------------------------------
def test_schedules_sorted_by_wall(library: Library) -> None:
    for nps in library.pipe_sizes():
        walls = [library.pipe(nps, s).wall_thickness for s in library.schedules(nps)]
        assert walls == sorted(walls), nps


def test_mount_height_adds_wall() -> None:
    pipe = PipeData(nominal_size="6", schedule="40", inner_diameter=0.154,
                    wall_thickness=0.00711, mount_height=0.15)
    assert pipe.nozzle_length == pytest.approx(0.15711)


def test_wall_filled_from_schedule(library: Library) -> None:
    inp = default_input("T")
    assert inp.pipe.wall_thickness is None
    filled = with_wall_thickness(inp, library)
    assert filled.pipe.wall_thickness == pytest.approx(
        library.pipe("6", "40").wall_thickness)


# --- Fluidos ----------------------------------------------------------------------------------
def test_fluid_types_only_contain_known_fluids(library: Library) -> None:
    known = {f.id for f in library.fluids()}
    for ft in FLUID_TYPES:
        for fid, _ in ft.fluids:
            assert fid in known, (ft.id, fid)


def test_fluid_labels() -> None:
    assert fluid_label("water", "Agua", "", True) == "Agua"
    assert fluid_label("water", "Agua", "steam", True) == "Vapor de agua (steam)"
    assert fluid_label("propane", "Propano", "liquid", True) == "Propano (Estado Líquido)"
    assert type_for("water", Phase.STEAM) == "steam"
    assert TYPES_BY_ID["liquid"].phase is Phase.LIQUID


def test_phase_mismatch() -> None:
    assert phase_mismatch(Phase.LIQUID, Phase.GAS)
    assert not phase_mismatch(Phase.GAS, Phase.STEAM)
    assert not phase_mismatch(Phase.TWO_PHASE, Phase.LIQUID)


# --- Conexión sugerida -------------------------------------------------------------------------
def test_suggested_size_in_list(tmp_path: Path) -> None:
    for conn in ConnectionType:
        for nps in ("1", "2", "4", "12", "30"):
            size = suggested_connection_size(conn, nps)
            assert size in CONNECTION_SIZES[conn], (conn, nps, size)
    (tmp_path / "tamanos_conexion.json").write_text(json.dumps({"flanged": [[0, "2"]]}),
                                                    encoding="utf-8")
    assert suggested_connection_size(ConnectionType.FLANGED, "6", tmp_path) == "2"


# --- E y S manuales ---------------------------------------------------------------------------
def test_manual_material_override(library: Library) -> None:
    inp = default_input("T")
    tw = inp.thermowell.model_copy(update={"material": MaterialRef(
        material_id="SS316", elastic_modulus=150e9, allowable_stress=100e6)})
    ev = evaluate(TagRecord(input=inp.model_copy(update={"thermowell": tw})), library,
                  ProjectSettings())
    assert ev.material is not None
    assert ev.material.elastic_modulus == pytest.approx(150e9)
    assert ev.material.allowable_stress == pytest.approx(100e6)
    rows = {r.key: r for r in input_rows(ev, True)}
    assert rows["in.E"].source == "src.manual"


# --- Resumen ASME -------------------------------------------------------------------------------
def test_summary_tables(evaluations: dict[str, object]) -> None:
    for name, ev in evaluations.items():
        cases = calculated_results(ev)  # type: ignore[arg-type]
        assert cases, name
        keys = [r.key for r in cases[0].rows]
        assert keys == ["q_actual", "velocity", "ve", "v_ve", "reynolds", "strouhal", "fs",
                        "fnc", "ratio", "steady", "dynamic", "von_mises"]
        status = asme_status(ev)  # type: ignore[arg-type]
        assert status[-1].key == "topic.overall"
        assert len(input_rows(ev, True)) == 15  # type: ignore[arg-type]
        conv = dict(length_convention(ev))  # type: ignore[arg-type]
        assert conv["conv.L"] == pytest.approx(conv["conv.hs"] + conv["conv.insertion"])
        for key in [*keys, *(s.key for s in status), *(s.verdict for s in status)]:
            assert key in LABELS


def test_failing_example_is_no_cumple(evaluations: dict[str, object]) -> None:
    ev = evaluations["ejemplo_3_gas_no_cumple"]
    overall = asme_status(ev)[-1]  # type: ignore[arg-type]
    assert overall.status is CheckStatus.FAIL
    freq = next(s for s in asme_status(ev) if s.key == "topic.frequency")  # type: ignore[arg-type]
    assert freq.verdict == "v.resonance"


# --- Fichas «ⓘ» --------------------------------------------------------------------------------
def test_every_card_is_complete_in_both_languages() -> None:
    for cid, card in CARDS.items():
        for lang in (0, 1):
            assert card.title[lang], cid
            assert card.what[lang], cid
            assert card.role[lang], cid
        for sec in SECTIONS:
            pair = getattr(card, sec)
            assert bool(pair[0]) == bool(pair[1]), (cid, sec)


def test_aliases_and_criteria_resolve(evaluations: dict[str, object]) -> None:
    for alias in ALIASES:
        assert card_for(alias) is not None, alias
    for ev in evaluations.values():
        for c in ev.result.checks:  # type: ignore[attr-defined]
            assert card_for(c.criterion_id) is not None, c.criterion_id
        for case in calculated_results(ev):  # type: ignore[arg-type]
            for row in case.rows:
                assert card_for(row.key) is not None, row.key
        for s in asme_status(ev):  # type: ignore[arg-type]
            assert card_for(s.key) is not None, s.key


def test_curves_render(evaluations: dict[str, object]) -> None:
    ev = evaluations["ejemplo_1_agua"]
    for cid in CURVE_IDS:
        png = curve(cid, ev, True)  # type: ignore[arg-type]
        assert png is not None and png.startswith(b"\x89PNG"), cid


def test_render_card_with_example(evaluations: dict[str, object]) -> None:
    ev = evaluations["ejemplo_1_agua"]
    out = render_card(CARDS["r.ratio"], ev, None, es=True,  # type: ignore[arg-type]
                      qfmt=lambda v, k: f"{v:g}", tag="TW-101", images=False)
    assert "Ejemplo resuelto" in out.html and "TW-101" in out.html


def test_every_editor_field_has_a_card(library: Library) -> None:
    """Ningún campo del editor, de las opciones ni del proyecto queda sin ficha."""
    pytest.importorskip("PySide6")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication, QCheckBox, QFormLayout, QLabel

    from thermowell_sizer.core.models import EngineOptions
    from thermowell_sizer.project import ProjectInfo
    from thermowell_sizer.ui.dialogs import OptionsDialog, ProjectDialog
    from thermowell_sizer.ui.tag_editor import TagEditor

    _app = QApplication.instance() or QApplication([])
    editor = TagEditor(library)
    widgets = [*editor.pages, OptionsDialog(EngineOptions()),
               ProjectDialog(ProjectInfo(name="x"), ProjectSettings())]
    missing: list[str] = []
    for w in widgets:
        for form in w.findChildren(QFormLayout):
            for row in range(form.rowCount()):
                item = form.itemAt(row, QFormLayout.ItemRole.LabelRole)
                if item is not None and isinstance(item.widget(), QLabel):
                    text = item.widget().text()  # type: ignore[union-attr]
                    if text:
                        missing.append(text)
                span = form.itemAt(row, QFormLayout.ItemRole.SpanningRole)
                if span is not None and isinstance(span.widget(), QCheckBox):
                    missing.append(span.widget().text())  # type: ignore[union-attr]
    assert not missing, missing
    assert len(set(editor.info_keys)) >= 50
    del _app


def test_logo_and_icon_assets() -> None:
    root = Path(__file__).resolve().parents[1]
    assets = root / "src" / "thermowell_sizer" / "assets"
    for name in ("logo_tws.png", "icon_tws.png", "icon_t.png"):
        assert (assets / name).is_file(), name
    ico = (root / "packaging" / "thermowell_sizer.ico").read_bytes()
    assert ico[:4] == b"\x00\x00\x01\x00"
    assert int.from_bytes(ico[4:6], "little") == 7  # 16, 24, 32, 48, 64, 128, 256 px
