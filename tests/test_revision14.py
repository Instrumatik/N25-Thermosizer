"""Revisión 1.4: montaje en recipiente, ángulo, rosca NPT/G y guías de la biblioteca."""

from __future__ import annotations

import math
import os
from pathlib import Path

import pytest

from thermowell_sizer.autodesign import AUTO_BLOCKS
from thermowell_sizer.core.advisories import VESSEL_MIN_IMMERSION, advise
from thermowell_sizer.core.models import (
    CalcInput,
    CheckStatus,
    ConnectionType,
    FlowBasis,
    FlowCase,
    MountingOrientation,
    PipeData,
    ProcessConnection,
    ThreadType,
)
from thermowell_sizer.data.database import Library
from thermowell_sizer.data.reference import REFERENCE_TABLES
from thermowell_sizer.infocards.content import CARDS, card_for
from thermowell_sizer.infocards.render import render_card, search_text
from thermowell_sizer.project import load_project
from thermowell_sizer.services import evaluate

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
_QT_APP: object = None


@pytest.fixture(scope="module")
def library() -> Library:
    return Library()


def _water() -> tuple[object, object]:
    p = load_project(EXAMPLES / "ejemplo_1_agua.tws")
    return p, p.tags[0]


def _vessel_input(inp: CalcInput, depth: float | None = 1.0) -> CalcInput:
    pipe = PipeData.model_validate({
        **inp.pipe.model_dump(), "nominal_size": "Recipiente", "schedule": "",
        "inner_diameter": 2.0, "wall_thickness": 0.012, "liquid_depth": depth,
        "orientation": MountingOrientation.VESSEL})
    process = inp.process.model_copy(update={"flow_cases": (
        FlowCase(label="normal", basis=FlowBasis.VELOCITY, velocity=0.0),)})
    return inp.model_copy(update={"pipe": pipe, "process": process})


def _q(value: float, kind: object) -> str:
    return f"{value:g}"


def test_vessel_without_flow_passes_with_note(library: Library) -> None:
    p, rec = _water()
    vessel = rec.model_copy(update={"input": _vessel_input(rec.input)})  # type: ignore[attr-defined]
    ev = evaluate(vessel, library, p.settings)  # type: ignore[attr-defined]
    assert ev.result is not None
    assert ev.status is CheckStatus.PASS
    assert "note.vessel" in ev.result.notes
    freq = [c for c in ev.result.checks if c.criterion_id == "frequency_limit"]
    assert all(c.status is CheckStatus.NOT_APPLICABLE for c in freq)


def test_vessel_auto_design_reaches_the_liquid(library: Library) -> None:
    p, rec = _water()
    vessel = rec.model_copy(update={  # type: ignore[attr-defined]
        "input": _vessel_input(rec.input), "auto_blocks": AUTO_BLOCKS})  # type: ignore[attr-defined]
    ev = evaluate(vessel, library, p.settings)  # type: ignore[attr-defined]
    assert ev.status is CheckStatus.PASS
    g = ev.input.thermowell.geometry
    immersion = g.U - ev.input.pipe.nozzle_length
    assert immersion >= VESSEL_MIN_IMMERSION - 1e-6
    assert immersion <= 1.0


def test_tip_limit_and_radial_factor() -> None:
    _, rec = _water()
    inp = rec.input  # type: ignore[attr-defined]
    v = _vessel_input(inp, depth=0.3).pipe
    assert v.is_vessel and v.tip_limit == pytest.approx(0.3)
    angled = inp.pipe.model_copy(update={"orientation": MountingOrientation.ANGLED,
                                         "mount_angle": 30.0})
    assert angled.radial_factor == pytest.approx(math.sin(math.radians(30.0)))
    assert inp.pipe.radial_factor == 1.0


def test_vessel_short_immersion_and_missing_angle_advise() -> None:
    _, rec = _water()
    inp = _vessel_input(rec.input)  # type: ignore[attr-defined]
    assert "adv.vessel_immersion" in {a.key for a in advise(inp)}
    pipe = rec.input.pipe.model_copy(  # type: ignore[attr-defined]
        update={"orientation": MountingOrientation.ANGLED})
    angled = rec.input.model_copy(update={"pipe": pipe})  # type: ignore[attr-defined]
    assert "adv.angle_missing" in {a.key for a in advise(angled)}


def test_thread_types_and_datasheet_codes() -> None:
    npt = ProcessConnection(type=ConnectionType.THREADED, size="1 NPT")
    g = ProcessConnection(type=ConnectionType.THREADED, size="G 1", thread=ThreadType.G)
    assert npt.thread_type is ThreadType.NPT and npt.datasheet_code == "R"
    assert g.datasheet_code == "G"
    assert ProcessConnection(type=ConnectionType.FLANGED, size="1-1/2", rating_class=300
                             ).datasheet_code == "H"
    assert ProcessConnection(type=ConnectionType.WELD_IN).datasheet_code == "S"
    assert ProcessConnection(type=ConnectionType.SOCKET_WELD, size="1").datasheet_code == "S"
    assert ProcessConnection(type=ConnectionType.FLANGED, size="1", rating_class=150,
                             thread=None).thread_type is None


def test_g_thread_advisory() -> None:
    _, rec = _water()
    inp = rec.input  # type: ignore[attr-defined]
    conn = inp.thermowell.connection
    if conn.type is not ConnectionType.THREADED:
        conn = ProcessConnection(type=ConnectionType.THREADED, size="1 NPT")
    tw = inp.thermowell.model_copy(update={
        "connection": conn.model_copy(update={"thread": ThreadType.G, "size": "G 1"})})
    g_inp = inp.model_copy(update={"thermowell": tw})
    assert "adv.thread_g" in {a.key for a in advise(g_inp)}


def test_library_guides_have_tables_and_are_searchable() -> None:
    for cid in ("conn.threaded", "conn.flanged", "conn.socket_weld", "conn.weld_in",
                "conn.van_stone", "conn.sanitary", "profile.straight", "profile.tapered",
                "profile.stepped", "f.connection", "f.profile"):
        card = CARDS[cid]
        assert card.table, cid
        for row in card.table:
            for cell in row:
                assert cell[0] and cell[1], cid
    assert "1,10 a 1,25" in search_text(CARDS["profile.tapered"])
    assert "cip/sip" in search_text(CARDS["conn.sanitary"])
    html_es = render_card(CARDS["profile.stepped"], None, None, es=True, qfmt=_q,
                          images=False).html
    assert "<table" in html_es and "1,05 a 1,15" in html_es and "#fff3c4" in html_es
    html_en = render_card(CARDS["f.profile"], None, None, es=False, qfmt=_q, images=False).html
    assert "Relative cost" in html_en
    ids = {t.id for t in REFERENCE_TABLES}
    assert {"connection_use", "profile_guide"} <= ids
    for key in ("f.mount_angle", "f.liquid_depth", "f.thread"):
        assert card_for(key) is not None, key


def test_library_search_finds_the_guides() -> None:
    pytest.importorskip("PySide6")
    from thermowell_sizer.ui.library_ui import search_cards

    found = {cid for cid, _ in search_cards("Van Stone", es=True, limit=20)}
    assert "conn.van_stone" in found
    found = {cid for cid, _ in search_cards("escalonado", es=True, limit=20)}
    assert "profile.stepped" in found


def test_editor_vessel_and_thread_round_trip(library: Library) -> None:
    pytest.importorskip("PySide6")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication

    from thermowell_sizer.ui.tag_editor import VESSEL_PIPE, TagEditor

    global _QT_APP
    _QT_APP = QApplication.instance() or QApplication([])
    _, rec = _water()
    inp = _vessel_input(rec.input, depth=0.8)  # type: ignore[attr-defined]
    editor = TagEditor(library)
    editor.load(inp)
    assert editor.c_nps.currentText() == VESSEL_PIPE
    out = editor.to_input()
    assert out is not None
    assert out.pipe.is_vessel
    assert out.pipe.liquid_depth == pytest.approx(0.8)
    assert all((c.velocity or 0.0) == 0.0 for c in out.process.flow_cases)
