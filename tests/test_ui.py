"""Pruebas de humo de la interfaz (Qt en modo offscreen)."""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
pytest.importorskip("PySide6")

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from thermowell_sizer.core.models import CheckStatus
from thermowell_sizer.core.units import UnitSystem
from thermowell_sizer.data.database import Library
from thermowell_sizer.i18n import Language
from thermowell_sizer.project import load_project
from thermowell_sizer.ui.app import Application
from thermowell_sizer.ui.main_window import MainWindow
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.text import UI


@pytest.fixture(scope="module")
def app() -> QApplication:
    inst = QApplication.instance()
    return inst if isinstance(inst, QApplication) else QApplication([])


@pytest.fixture(scope="module")
def library() -> Library:
    return Library()


@pytest.fixture
def window(app: QApplication, library: Library, tmp_path: Path) -> Iterator[MainWindow]:
    STATE.language = Language.ES
    STATE.units = UnitSystem.SI
    settings = QSettings(str(tmp_path / "s.ini"), QSettings.Format.IniFormat)
    win = MainWindow(library, settings)
    yield win
    win.dirty = False
    win.close()


def test_menu_bar_complete(window: MainWindow) -> None:
    titles = [a.text().replace("&", "") for a in window.menuBar().actions()]
    assert titles == ["Archivo", "Editar", "Proyecto", "Cálculo", "Biblioteca",
                      "Herramientas", "Reportes", "Ayuda"]


def test_default_tag_calculates(window: MainWindow) -> None:
    ev = window.calculate()
    assert ev is not None and ev.status is CheckStatus.PASS
    assert window.results.table.rowCount() > 5
    assert ev.input.process.properties.source.value == "coolprop"
    assert ev.options.flange_rating is not None


def test_edit_geometry_undo_redo(window: MainWindow) -> None:
    q = window.editor.quantities["g_L"]
    q.edit.setText("450")
    q.edit.editingFinished.emit()
    window._flush_editor()
    assert pytest.approx(0.45) == window.project.tags[0].input.thermowell.geometry.L
    window.undo.undo()
    assert pytest.approx(0.150) == window.project.tags[0].input.thermowell.geometry.L
    window.undo.redo()
    assert pytest.approx(0.45) == window.project.tags[0].input.thermowell.geometry.L


def test_invalid_input_flags_error(window: MainWindow) -> None:
    q = window.editor.quantities["g_d"]
    q.edit.setText("40")  # agujero mayor que la punta
    q.edit.editingFinished.emit()
    assert window.editor.validate() is None
    assert window.editor.error_label.text()


def test_tags_and_clipboard(window: MainWindow) -> None:
    window.new_tag()
    window.duplicate_tag()
    names = [r.input.identification.tag for r in window.project.tags]
    assert len(names) == 3 and len(set(names)) == 3
    window.copy_tag()
    window.paste_tag()
    assert len(window.project.tags) == 4
    window.calculate_all()
    assert all(r.last_status is not None for r in window.project.tags)


def test_units_and_expert(window: MainWindow) -> None:
    window.set_units(UnitSystem.IMPERIAL)
    assert window.editor.quantities["g_L"].unit.text() == "in"
    assert window.editor.quantities["p_op"].unit.text() == "psig"
    window.set_units(UnitSystem.SI)
    window.act_expert.setChecked(True)
    window.toggle_expert()
    assert window.editor.mode_stack.currentWidget() is window.editor.expert_scroll
    window.act_expert.setChecked(False)
    window.toggle_expert()


def test_save_and_reopen(window: MainWindow, tmp_path: Path) -> None:
    window.calculate()
    window.path = tmp_path / "p.tws"
    assert window.save()
    assert not window.dirty
    project = load_project(tmp_path / "p.tws")
    assert project.tags[0].last_status is CheckStatus.PASS
    window.new_tag()
    window.autosave()
    assert (tmp_path / "p.tws.autosave").exists()
    window.dirty = False
    assert window.open_path(tmp_path / "p.tws", ask_recover=False)
    assert len(window.project.tags) == 1


def test_optimize_and_chart(window: MainWindow) -> None:
    q = window.editor.quantities["g_L"]
    q.edit.setText("600")
    q.edit.editingFinished.emit()
    window.editor.flow_rows[0].values[next(iter(window.editor.flow_rows[0].values))]
    case = window.editor.flow_rows[0]
    vel = case.values[case.basis.value()]
    vel.edit.setText("6")
    vel.edit.editingFinished.emit()
    ev = window.calculate()
    assert ev is not None and ev.status is CheckStatus.FAIL
    window.optimize()
    assert window.results.alt_list.count() >= 1
    if window.results._alternatives:
        window.results.alt_list.setCurrentRow(0)
        window.results._apply()
        assert window.evaluations[0].status is not CheckStatus.FAIL
    window.show_sensitivity()
    assert window.chart.evaluation is not None


def test_library_windows(window: MainWindow) -> None:
    window.open_library("glossary", ("glossary", "thermowell"))
    assert window.library_window is not None
    window.library_window._show_material(0)
    window.open_assistant()
    assert window.assistant is not None and window.assistant.table.rowCount() > 10
    window.assistant.table.selectRow(0)
    window.assistant._use()
    window.open_help()
    assert window.help_window is not None


def test_language_rebuild(app: QApplication, library: Library, tmp_path: Path) -> None:
    STATE.language = Language.ES
    settings = QSettings(str(tmp_path / "s.ini"), QSettings.Format.IniFormat)
    shell = Application(app, library, settings)
    old = shell.window
    old.set_language(Language.EN)
    assert shell.window is not old
    titles = [a.text().replace("&", "") for a in shell.window.menuBar().actions()]
    assert titles[0] == "File"
    shell.window.dirty = False
    shell.window.close()
    STATE.language = Language.ES


def test_ui_text_pairs_complete() -> None:
    for key, pair in UI.items():
        assert len(pair) == 2 and all(pair), key


def test_tool_windows(app: QApplication, library: Library) -> None:
    from thermowell_sizer.ui import tools

    conv = tools.open_tool("converter", library)
    assert isinstance(conv, tools.ConverterWindow)
    conv.category.setCurrentIndex(conv.category.findData("temperature"))
    conv.value.setText("100")
    assert conv.table.rowCount() == 4
    calcs = tools.open_tool("calculators", library)
    assert isinstance(calcs, tools.CalculatorsWindow)
    for i in range(calcs.tabs.count()):
        tab = calcs.tabs.widget(i)
        tab.run()  # type: ignore[attr-defined]
        assert "⚠" not in tab.result.text(), calcs.tabs.tabText(i)  # type: ignore[attr-defined]
    conv.close()
    calcs.close()


def test_thermal_estimate_shown(window: MainWindow) -> None:
    ev = window.calculate()
    assert ev is not None and ev.thermal is not None
    assert "τ" in window.results.lbl_summary.text()


def test_report_generation(window: MainWindow, tmp_path: Path) -> None:
    from thermowell_sizer.ui import report_actions

    window.calculate()
    for kind, ext in (("datasheet", ".pdf"), ("excel", ".xlsx"), ("bom", ".xlsx"),
                      ("project_report", ".pdf")):
        out = report_actions.generate(window, kind, tmp_path / f"{kind}{ext}")
        assert out.stat().st_size > 1000


def test_license_dialog(window: MainWindow, tmp_path: Path,
                        monkeypatch: pytest.MonkeyPatch) -> None:
    from thermowell_sizer.ui import license_ui, report_actions
    from thermowell_sizer.ui.state import STATE

    monkeypatch.setattr(STATE, "data_folder", tmp_path)
    dlg = license_ui.LicenseDialog(window)
    assert STATE.licensee is None
    assert "evaluación" in dlg.status.text() or "Evaluation" in dlg.status.text()
    assert len(dlg.fingerprint.text()) == 16
    dlg.code.setPlainText("TWS1.no.valida")
    assert dlg.install(quiet=True) is None
    assert report_actions.current_fmt(window).licensee is None
    monkeypatch.setattr(STATE, "licensee", "Planta Norte")
    assert "Planta Norte" in report_actions.current_fmt(window).footer()
    dlg.deleteLater()


def test_smoke_test_mode(window: MainWindow) -> None:
    from thermowell_sizer.ui.app import smoke_test

    assert smoke_test(window) == 0


def test_design_dialog_applies_typical_and_profile(window: MainWindow,
                                                   tmp_path: Path) -> None:
    from thermowell_sizer.ui.design_ui import DesignDialog

    STATE.data_folder = tmp_path
    (tmp_path / "perfiles").mkdir()
    examples = Path(__file__).resolve().parents[1] / "examples"
    (tmp_path / "perfiles" / "ejemplo.json").write_text(
        (examples / "perfil_ejemplo.json").read_text(encoding="utf-8"), encoding="utf-8")
    try:
        editor = window.editor
        dlg = DesignDialog(editor.design_context(), window)
        assert dlg.choice is not None
        editor.apply_design(dlg.choice)
        inp = editor.to_input()
        assert inp is not None
        assert pytest.approx(dlg.choice.U) == inp.thermowell.geometry.U
        dlg.c_source.setCurrentIndex(dlg.c_source.findData("ejemplo"))
        assert dlg.c_model.isVisibleTo(dlg)
        assert dlg.choice is not None and dlg.choice.model
        editor.apply_design(dlg.choice)
        inp = editor.to_input()
        assert inp is not None
        assert inp.thermowell.geometry.d == pytest.approx(0.0066)
    finally:
        STATE.data_folder = None


def test_library_reference_tab(window: MainWindow, library: Library) -> None:
    from thermowell_sizer.ui.library_ui import LibraryWindow

    dlg = LibraryWindow(library, window)
    assert dlg.ref_list.count() >= 8
    dlg.ref_list.setCurrentRow(4)
    assert "<table" in dlg.ref_view.toHtml()


def test_library_glossary_and_standards_show_full_card(window: MainWindow,
                                                       library: Library) -> None:
    from thermowell_sizer.ui.library_ui import LibraryWindow

    dlg = LibraryWindow(library, window)
    dlg.gl_list.setCurrentRow(0)
    assert "Ejemplo num" in dlg.gl_view.toHtml() or "Numerical example" in dlg.gl_view.toHtml()
    dlg.std_list.setCurrentRow(0)
    html = dlg.std_view.toHtml()
    assert "Errores comunes" in html or "Common mistakes" in html
