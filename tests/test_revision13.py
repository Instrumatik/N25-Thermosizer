"""Revisión 1.3: selección automática por bloque (material, conexión, geometría, sensor)."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from thermowell_sizer.autodesign import AUTO_BLOCKS, _es
from thermowell_sizer.core.designs import BORE_260, TYPICAL_DESIGNS, build_choice
from thermowell_sizer.core.models import CheckStatus, ConnectionType, ShankProfile
from thermowell_sizer.data.database import Library
from thermowell_sizer.project import Project, TagRecord, load_project, save_project
from thermowell_sizer.services import Evaluation, evaluate
from thermowell_sizer.summary import auto_rows, input_rows

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
_QT_APP: object = None


@pytest.fixture(scope="module")
def library() -> Library:
    return Library()


def _auto(name: str, library: Library, blocks: tuple[str, ...] = AUTO_BLOCKS) -> Evaluation:
    p = load_project(EXAMPLES / f"{name}.tws")
    rec = p.tags[0].model_copy(update={"auto_blocks": blocks})
    return evaluate(rec, library, p.settings)


def _q(value: float, kind: object) -> str:
    return f"{value:g}"


def test_spanish_decimals_keep_standard_names() -> None:
    assert _es("ASME PTC 19.3 TW-2016 y ASME B16.5 grupo 2.2") == (
        "ASME PTC 19.3 TW-2016 y ASME B16.5 grupo 2.2")
    assert _es("B36.10M / B36.19M") == "B36.10M / B36.19M"
    assert _es("U = 114.3 mm, V/Ve 0.72") == "U = 114,3 mm, V/Ve 0,72"


def test_flanged_stepped_design_is_within_the_correlation() -> None:
    design = next(d for d in TYPICAL_DESIGNS if d.id == "flanged_stepped")
    a, b = design.diameters[BORE_260]
    assert b in (0.5 * 0.0254, 0.875 * 0.0254)
    assert 0.583 <= b / a <= 0.875
    choice = build_choice(design, size="1-1/2", bore=BORE_260, U=0.2)
    assert choice.profile is ShankProfile.STEPPED


def test_water_example_auto(library: Library) -> None:
    ev = _auto("ejemplo_1_agua", library)
    assert ev.status is CheckStatus.PASS
    assert {d.block for d in ev.decisions} == set(AUTO_BLOCKS)
    tw = ev.input.thermowell
    assert tw.material.material_id == "SS316"
    assert tw.connection.type is ConnectionType.THREADED  # agua ≤ 20 barg y ≤ 200 °C
    assert ev.input.sensor.sheath_diameter < tw.geometry.d


def test_steam_example_auto(library: Library) -> None:
    ev = _auto("ejemplo_2_vapor", library)
    assert ev.status is CheckStatus.PASS
    tw = ev.input.thermowell
    assert tw.connection.type is ConnectionType.FLANGED
    assert tw.connection.rating_class == 600
    assert tw.material.coating  # V/Ve ≥ 0,7: recargue duro
    assert tw.geometry.corrosion_allowance == pytest.approx(1e-3)
    rows = auto_rows(ev, True, _q)
    assert rows and all(r.reason for r in rows)
    assert any("Inoxidable" in r.value for r in rows)


def test_failing_example_reports_best_and_warns(library: Library) -> None:
    ev = _auto("ejemplo_3_gas_no_cumple", library)
    assert ev.status is CheckStatus.FAIL
    assert any(d.field == "f.L" for d in ev.decisions)  # «ningún diseño normalizado cumple»
    # la geometría respeta la altura de montaje: la punta queda dentro del caño
    g, pipe = ev.input.thermowell.geometry, ev.input.pipe
    assert pipe.nozzle_length < g.L


def test_only_selected_blocks_change(library: Library) -> None:
    base = load_project(EXAMPLES / "ejemplo_2_vapor.tws").tags[0].input
    ev = _auto("ejemplo_2_vapor", library, ("material",))
    assert {d.block for d in ev.decisions} == {"material"}
    assert ev.input.thermowell.geometry.A == base.thermowell.geometry.A
    assert ev.input.thermowell.connection == base.thermowell.connection
    rows = {r.key: r for r in input_rows(ev, True)}
    assert rows["in.E"].source == "src.auto"
    assert rows["in.root"].source == "src.entered"


def test_auto_blocks_persist(tmp_path: Path) -> None:
    p = load_project(EXAMPLES / "ejemplo_1_agua.tws")
    rec = p.tags[0].model_copy(update={"auto_blocks": ("material", "geometry")})
    path = tmp_path / "x.tws"
    save_project(p.model_copy(update={"tags": (rec,)}), path)
    assert load_project(path).tags[0].auto_blocks == ("material", "geometry")
    assert TagRecord(input=rec.input).auto_blocks == ()


def test_memo_has_auto_section(library: Library, tmp_path: Path) -> None:
    pytest.importorskip("docx")
    from docx import Document

    from thermowell_sizer.reports.common import tag_report
    from thermowell_sizer.reports.word import build_word

    p: Project = load_project(EXAMPLES / "ejemplo_2_vapor.tws")
    for blocks, expected in ((AUTO_BLOCKS, "Selección automática"), ((), "modo «Manual»")):
        proj = p.model_copy(update={"tags": (p.tags[0].model_copy(
            update={"auto_blocks": blocks}),)})
        out = build_word(tag_report(proj, 0, library), tmp_path / "m.docx")
        text = "\n".join(par.text for par in Document(str(out)).paragraphs)
        assert "4. Selección automática y justificación" in text
        assert expected in text


def test_editor_mode_selectors(library: Library) -> None:
    pytest.importorskip("PySide6")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication

    from thermowell_sizer.ui.tag_editor import TagEditor

    global _QT_APP  # la aplicación debe vivir hasta el final de la sesión
    _QT_APP = QApplication.instance() or QApplication([])
    editor = TagEditor(library)
    inp = load_project(EXAMPLES / "ejemplo_1_agua.tws").tags[0].input
    editor.load(inp, auto_blocks=("material", "sensor"))
    assert editor.auto_blocks() == ("material", "sensor")
    assert not editor.c_material.isEnabled()
    assert not editor.quantities["sheath"].isEnabled()
    assert editor.c_profile.isEnabled()
    editor.mode_combos["material"].setCurrentIndex(0)
    assert editor.c_material.isEnabled()
    for key in ("f.mode_material", "f.mode_connection", "f.mode_geometry", "f.mode_sensor"):
        assert key in editor.info_keys, key
    editor.deleteLater()
    QApplication.processEvents()
