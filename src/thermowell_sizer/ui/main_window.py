"""Ventana principal: menús, barra de herramientas, árbol de tags, editor y resultados."""

from __future__ import annotations

import functools
import importlib
import json
from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QPoint, QSettings, Qt, QTimer
from PySide6.QtGui import (
    QAction,
    QCloseEvent,
    QColor,
    QIcon,
    QKeySequence,
    QPixmap,
    QUndoCommand,
    QUndoStack,
)
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QFileDialog,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QSplitter,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)

from thermowell_sizer import __version__
from thermowell_sizer.core.analysis.optimize import (
    NO_COLLARS_NOTE,
    Alternative,
    propose_alternatives,
)
from thermowell_sizer.core.models import CalcInput, CheckStatus
from thermowell_sizer.core.units import UnitSystem
from thermowell_sizer.data.database import Library
from thermowell_sizer.i18n import Language
from thermowell_sizer.project import (
    FILE_EXTENSION,
    Project,
    ProjectFileError,
    ProjectInfo,
    TagRecord,
    load_project,
    save_project,
)
from thermowell_sizer.services import (
    Evaluation,
    default_input,
    evaluate,
    import_rows,
    read_table,
    template_csv,
)
from thermowell_sizer.ui.charts import SensitivityChart
from thermowell_sizer.ui.dialogs import AboutDialog, OptionsDialog, ProjectDialog
from thermowell_sizer.ui.help import STEP_TOPICS, HelpWindow
from thermowell_sizer.ui.library_ui import LibraryWindow, MaterialAssistant, SearchPalette
from thermowell_sizer.ui.preview import ThermowellPreview
from thermowell_sizer.ui.results import ResultsPanel
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.tag_editor import TagEditor
from thermowell_sizer.ui.text import t
from thermowell_sizer.ui.theme import apply_theme
from thermowell_sizer.ui.widgets import STATUS_COLORS

AUTOSAVE_MS = 3 * 60 * 1000
EDIT_DEBOUNCE_MS = 250
CALC_DEBOUNCE_MS = 500
MAX_RECENT = 8
AUTOSAVE_SUFFIX = ".autosave"
CLIPBOARD_MIME = "application/x-thermowell-tag"
Shortcut = str | QKeySequence | QKeySequence.StandardKey | None


def _status_icon(status: CheckStatus | None) -> QIcon:
    pix = QPixmap(12, 12)
    pix.fill(QColor(STATUS_COLORS[status]))
    return QIcon(pix)


class _Snapshot(QUndoCommand):
    """Paso de deshacer: guarda el proyecto completo antes y después del cambio."""

    def __init__(self, window: MainWindow, before: Project, after: Project, text: str,
                 merge_id: int) -> None:
        super().__init__(text)
        self.window = window
        self.before = before
        self.after = after
        self._merge_id = merge_id
        self._first = True

    def id(self) -> int:
        """Ediciones consecutivas del mismo tag se combinan en un único paso."""
        return self._merge_id

    def mergeWith(self, other: QUndoCommand) -> bool:  # noqa: N802 - API de Qt
        """Combina con el siguiente paso de edición del mismo tag."""
        if not isinstance(other, _Snapshot) or other.id() != self.id() or self.id() < 0:
            return False
        self.after = other.after
        return True

    def redo(self) -> None:
        """Aplica el estado posterior (la primera vez ya está aplicado)."""
        if self._first:
            self._first = False
            return
        self.window.set_project_state(self.after)

    def undo(self) -> None:
        """Restaura el estado anterior."""
        self.window.set_project_state(self.before)


class MainWindow(QMainWindow):
    """Ventana principal de ThermoWell Sizer."""

    def __init__(self, library: Library, settings: QSettings,
                 rebuild: Callable[[MainWindow], None] | None = None) -> None:
        super().__init__()
        self.library = library
        self.settings = settings
        self._rebuild = rebuild
        self.project = Project(info=ProjectInfo(name=t("dlg.untitled")))
        self.path: Path | None = None
        self.dirty = False
        self.current = -1
        self.evaluations: dict[int, Evaluation] = {}
        self.undo = QUndoStack(self)
        self._restoring = False
        self.help_window: HelpWindow | None = None
        self.library_window: LibraryWindow | None = None
        self.assistant: MaterialAssistant | None = None
        self.tool_windows: list[QWidget] = []

        self.editor = TagEditor(library)
        self.preview = ThermowellPreview()
        self.results = ResultsPanel()
        self.chart = SensitivityChart()
        self.results.add_tab(self.chart, t("res.chart"))
        right = QSplitter(Qt.Orientation.Vertical)
        right.addWidget(self.preview)
        right.addWidget(self.results)
        right.setSizes([220, 480])
        split = QSplitter()
        split.addWidget(self.editor)
        split.addWidget(right)
        split.setSizes([700, 560])
        split.setStretchFactor(0, 1)
        split.setStretchFactor(1, 1)
        self.setCentralWidget(split)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._tree_menu)
        self.tree.currentItemChanged.connect(self._tree_selected)
        dock = QDockWidget(t("panel.tags"), self)
        dock.setObjectName("tagsDock")
        dock.setWidget(self.tree)
        self.tree.setMinimumWidth(150)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        self.tags_dock = dock

        self.lbl_file = QLabel()
        self.lbl_units = QLabel()
        self.lbl_status = QLabel()
        self.statusBar().addPermanentWidget(self.lbl_status)
        self.statusBar().addPermanentWidget(self.lbl_units)
        self.statusBar().addPermanentWidget(self.lbl_file)

        self._edit_timer = QTimer(self, singleShot=True, interval=EDIT_DEBOUNCE_MS)
        self._edit_timer.timeout.connect(self._editor_settled)
        self._calc_timer = QTimer(self, singleShot=True, interval=CALC_DEBOUNCE_MS)
        self._calc_timer.timeout.connect(self.calculate)
        self._autosave = QTimer(self, interval=AUTOSAVE_MS)
        self._autosave.timeout.connect(self.autosave)
        self._autosave.start()

        self.editor.changed.connect(self._edit_timer.start)
        self.editor.calculate_requested.connect(self.calculate)
        self.results.optimize_requested.connect(self.optimize)
        self.results.apply_alternative.connect(self.apply_alternative)
        self.results.tabs.currentChanged.connect(self._results_tab)
        self.undo.cleanChanged.connect(self._clean_changed)

        self._build_actions()
        self._build_menus()
        self._build_toolbar()
        self.editor.set_expert(self.act_expert.isChecked())
        self.new_tag()
        self.undo.clear()
        self._set_dirty(False)
        self._refresh_status()
        self.resize(1440, 860)
        geometry = settings.value("window/geometry")
        if geometry is not None:
            self.restoreGeometry(geometry)

    # --- Acciones y menús ------------------------------------------------------------
    def _action(self, key: str, slot: Callable[[], object], shortcut: Shortcut = None, *,
                checkable: bool = False) -> QAction:
        act = QAction(t(key), self)
        if shortcut is not None:
            act.setShortcut(QKeySequence(shortcut))
        act.setCheckable(checkable)
        act.triggered.connect(lambda *_: slot())
        return act

    def _build_actions(self) -> None:
        sk = QKeySequence.StandardKey
        a = self._action
        self.act_new = a("act.new", self.new_project, sk.New)
        self.act_open = a("act.open", self.open_dialog, sk.Open)
        self.act_save = a("act.save", self.save, sk.Save)
        self.act_save_as = a("act.save_as", self.save_as, sk.SaveAs)
        self.act_import = a("act.import_csv", self.import_table)
        self.act_template = a("act.import_template", self.save_template)
        self.act_export_json = a("act.export_json", self.export_tag_json)
        self.act_export_project = a("act.export_project_json", self.export_project_json)
        self.act_quit = a("act.quit", self.close, sk.Quit)
        self.act_undo = self.undo.createUndoAction(self, t("act.undo"))
        self.act_undo.setShortcut(sk.Undo)
        self.act_redo = self.undo.createRedoAction(self, t("act.redo"))
        self.act_redo.setShortcuts([QKeySequence(sk.Redo), QKeySequence("Ctrl+Y")])
        self.act_copy = a("act.copy_tag", self.copy_tag, "Ctrl+Shift+C")
        self.act_paste = a("act.paste_tag", self.paste_tag, "Ctrl+Shift+V")
        self.act_prefs = a("act.project_info", self.edit_project)
        self.act_new_tag = a("act.new_tag", self.new_tag, "Ctrl+T")
        self.act_dup = a("act.duplicate_tag", self.duplicate_tag, "Ctrl+D")
        self.act_del = a("act.delete_tag", self.delete_tag, sk.Delete)
        self.act_rename = a("act.rename_tag", self.rename_tag, "F2")
        self.act_calc = a("act.calculate", self.calculate, "F5")
        self.act_calc_all = a("act.calculate_all", self.calculate_all, "Shift+F5")
        self.act_opt = a("act.optimize", self.optimize, "Ctrl+Shift+O")
        self.act_sens = a("act.sensitivity", self.show_sensitivity)
        self.act_options = a("act.options", self.edit_options, "Ctrl+Shift+P")
        self.act_select = a("act.select_material", self.open_assistant)
        self.act_lib = {k: a(f"act.{k}", functools.partial(self.open_library, k))
                        for k in ("materials", "fluids", "flanges", "glossary", "standards")}
        self.act_search = a("act.search", self.open_search, "Ctrl+K")
        self.act_converter = a("act.converter", self.open_converter, "Ctrl+Shift+U")
        self.act_calcs = a("act.calculators", self.open_calculators)
        self.act_si = a("act.units_si", lambda: self.set_units(UnitSystem.SI), checkable=True)
        self.act_imp = a("act.units_imperial", lambda: self.set_units(UnitSystem.IMPERIAL),
                         checkable=True)
        self.act_toggle_units = a("act.units_si", self.toggle_units, "Ctrl+U")
        self.act_es = a("act.lang_es", lambda: self.set_language(Language.ES), checkable=True)
        self.act_en = a("act.lang_en", lambda: self.set_language(Language.EN), checkable=True)
        self.act_dark = a("act.theme_dark", self.toggle_theme, checkable=True)
        self.act_dark.setChecked(STATE.dark)
        self.act_expert = a("act.expert", self.toggle_expert, "Ctrl+E", checkable=True)
        self.act_expert.setChecked(bool(self.settings.value("ui/expert", False, type=bool)))
        self.act_prev_step = a("wiz.back", lambda: self.editor.step(-1), "Ctrl+PgUp")
        self.act_next_step = a("wiz.next", lambda: self.editor.step(1), "Ctrl+PgDown")
        self.act_reports = {k: a(f"act.{k}", functools.partial(self.report, k))
                            for k in ("datasheet", "memo", "excel", "word", "project_report",
                                      "bom")}
        self.act_help = a("act.help", self.open_help, sk.HelpContents)
        self.act_shortcuts = a("act.shortcuts", self.show_shortcuts)
        self.act_about = a("act.about", lambda: AboutDialog(self).exec())
        self.act_license = a("act.license", self.show_license)
        self.act_disclaimer = a("act.disclaimer", lambda: self.open_help("disclaimer"))
        for act in (self.act_si, self.act_imp, self.act_es, self.act_en):
            act.setCheckable(True)
        self._sync_checks()
        for act in (self.act_toggle_units, self.act_prev_step, self.act_next_step):
            self.addAction(act)

    def _build_menus(self) -> None:
        mb = self.menuBar()
        m = mb.addMenu(t("menu.file"))
        m.addActions([self.act_new, self.act_open])
        self.recent_menu = m.addMenu(t("menu.recent"))
        self._fill_recent()
        m.addSeparator()
        m.addActions([self.act_save, self.act_save_as])
        m.addSeparator()
        imp = m.addMenu(t("menu.import"))
        imp.addActions([self.act_import, self.act_template])
        exp = m.addMenu(t("menu.export"))
        exp.addActions([self.act_export_json, self.act_export_project])
        m.addSeparator()
        m.addAction(self.act_quit)

        m = mb.addMenu(t("menu.edit"))
        m.addActions([self.act_undo, self.act_redo])
        m.addSeparator()
        m.addActions([self.act_copy, self.act_paste])
        m.addSeparator()
        m.addAction(self.act_search)

        m = mb.addMenu(t("menu.project"))
        m.addActions([self.act_new_tag, self.act_dup, self.act_rename, self.act_del])
        m.addSeparator()
        m.addAction(self.act_prefs)

        m = mb.addMenu(t("menu.calc"))
        m.addActions([self.act_calc, self.act_calc_all])
        m.addSeparator()
        m.addActions([self.act_opt, self.act_sens, self.act_select])
        m.addSeparator()
        m.addAction(self.act_options)

        m = mb.addMenu(t("menu.library"))
        m.addActions(list(self.act_lib.values()))
        m.addSeparator()
        m.addAction(self.act_search)

        m = mb.addMenu(t("menu.tools"))
        m.addActions([self.act_converter, self.act_calcs])
        m.addSeparator()
        m.addActions([self.act_si, self.act_imp])
        m.addSeparator()
        m.addActions([self.act_es, self.act_en])
        m.addSeparator()
        m.addActions([self.act_dark, self.act_expert])

        m = mb.addMenu(t("menu.reports"))
        m.addActions(list(self.act_reports.values()))

        m = mb.addMenu(t("menu.help"))
        m.addActions([self.act_help, self.act_shortcuts])
        m.addSeparator()
        m.addActions([self.act_disclaimer, self.act_license, self.act_about])

    def _build_toolbar(self) -> None:
        tb = self.addToolBar("main")
        tb.setObjectName("mainToolbar")
        tb.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        tb.addActions([self.act_new, self.act_open, self.act_save])
        tb.addSeparator()
        tb.addActions([self.act_undo, self.act_redo])
        tb.addSeparator()
        tb.addActions([self.act_new_tag, self.act_dup])
        tb.addSeparator()
        tb.addActions([self.act_calc, self.act_calc_all, self.act_opt])
        tb.addSeparator()
        tb.addActions([self.act_reports["datasheet"], self.act_reports["memo"]])
        tb.addSeparator()
        tb.addActions([self.act_search, self.act_converter, self.act_expert])

    def _sync_checks(self) -> None:
        self.act_si.setChecked(STATE.units is UnitSystem.SI)
        self.act_imp.setChecked(STATE.units is UnitSystem.IMPERIAL)
        self.act_es.setChecked(STATE.language is Language.ES)
        self.act_en.setChecked(STATE.language is Language.EN)

    # --- Estado del proyecto ----------------------------------------------------------
    def _commit(self, project: Project, text: str, merge_id: int = -1) -> None:
        """Registra un cambio del proyecto en la pila de deshacer."""
        before = self.project
        self.project = project
        self.undo.push(_Snapshot(self, before, project, text, merge_id))

    def set_project_state(self, project: Project) -> None:
        """Restaura un estado (deshacer/rehacer) y refresca la vista."""
        self._restoring = True
        self.project = project
        self.evaluations.clear()
        self.current = min(max(self.current, 0), len(project.tags) - 1)
        self._fill_tree()
        if self.current >= 0:
            self._load_current()
        self._restoring = False

    def _clean_changed(self, clean: bool) -> None:
        self._set_dirty(not clean)

    def _set_dirty(self, dirty: bool) -> None:
        self.dirty = dirty
        name = self.path.name if self.path else self.project.info.name
        self.setWindowTitle(f"{'● ' if dirty else ''}{name} — ThermoWell Sizer {__version__}")
        self.lbl_file.setText(str(self.path) if self.path else t("dlg.untitled"))

    def _refresh_status(self, message: str | None = None) -> None:
        self.lbl_units.setText(f"{t('status.units')}: {STATE.units.value}"
                               f"{' (g)' if STATE.gauge else ''}")
        ev = self.evaluations.get(self.current)
        status = ev.status if ev else None
        self.lbl_status.setText("● " + (t(f"status.{status.value}") if status
                                        else t("res.not_calculated")))
        self.lbl_status.setStyleSheet(f"color: {STATUS_COLORS[status]}; font-weight: bold;")
        if message:
            self.statusBar().showMessage(message, 4000)

    # --- Árbol de tags --------------------------------------------------------------
    def _fill_tree(self) -> None:
        self.tree.blockSignals(True)
        self.tree.clear()
        root = QTreeWidgetItem([self.project.info.name])
        self.tree.addTopLevelItem(root)
        for i, rec in enumerate(self.project.tags):
            item = QTreeWidgetItem([rec.input.identification.tag])
            item.setData(0, Qt.ItemDataRole.UserRole, i)
            ev = self.evaluations.get(i)
            item.setIcon(0, _status_icon(ev.status if ev else rec.last_status))
            item.setToolTip(0, rec.input.identification.service)
            root.addChild(item)
            if i == self.current:
                self.tree.setCurrentItem(item)
        root.setExpanded(True)
        self.tree.blockSignals(False)

    def _tree_selected(self, item: QTreeWidgetItem | None, _prev: object = None) -> None:
        if item is None:
            return
        idx = item.data(0, Qt.ItemDataRole.UserRole)
        if idx is None or idx == self.current:
            return
        self._flush_editor()
        self.current = int(idx)
        self._load_current()

    def _tree_menu(self, pos: QPoint) -> None:
        menu = QMenu(self)
        menu.addActions([self.act_new_tag, self.act_dup, self.act_rename, self.act_del,
                         self.act_copy, self.act_paste])
        menu.exec(self.tree.viewport().mapToGlobal(pos))

    def _load_current(self) -> None:
        rec = self.project.tags[self.current]
        self.editor.load(rec.input, auto_properties=rec.auto_properties)
        self._update_preview(rec.input)
        ev = self.evaluations.get(self.current)
        if ev is None:
            self.results.clear()
            self.chart.set_evaluation(None)
        else:
            self.results.show_evaluation(ev)
            self._chart_if_visible(ev)
        self._refresh_status()

    def _update_preview(self, inp: CalcInput | None) -> None:
        if inp is None:
            return
        self.preview.set_data(inp.thermowell.geometry, inp.thermowell.connection.type,
                              inp.pipe.inner_diameter)

    # --- Edición ------------------------------------------------------------------------
    def _editor_settled(self) -> None:
        """Tras una pausa en la edición: valida, actualiza la vista y guarda en el proyecto."""
        if self._restoring or self.current < 0:
            return
        inp = self.editor.validate()
        if inp is None:
            self._refresh_status(t("status.invalid"))
            return
        self._update_preview(inp)
        rec = self.project.tags[self.current]
        new_rec = rec.model_copy(update={"input": inp,
                                         "auto_properties": self.editor.chk_auto.isChecked()})
        if new_rec != rec:
            self._replace_tag(self.current, new_rec, t("status.modified"), merge=True)
            self.evaluations.pop(self.current, None)
            self._calc_timer.start()

    def _flush_editor(self) -> None:
        if self._edit_timer.isActive():
            self._edit_timer.stop()
            self._editor_settled()

    def _replace_tag(self, index: int, rec: TagRecord, text: str, *, merge: bool = False) -> None:
        tags = list(self.project.tags)
        tags[index] = rec
        self._commit(self.project.model_copy(update={"tags": tuple(tags)}), text,
                     merge_id=1000 + index if merge else -1)
        item = self._tree_item(index)
        if item is not None:
            item.setText(0, rec.input.identification.tag)

    def _tree_item(self, index: int) -> QTreeWidgetItem | None:
        root = self.tree.topLevelItem(0)
        if root is None or index >= root.childCount():
            return None
        return root.child(index)

    def _unique_tag(self, base: str) -> str:
        names = {r.input.identification.tag for r in self.project.tags}
        if base not in names:
            return base
        n = 2
        while f"{base}-{n}" in names:
            n += 1
        return f"{base}-{n}"

    def _with_tag_name(self, inp: CalcInput, name: str) -> CalcInput:
        idn = inp.identification.model_copy(update={"tag": name})
        return inp.model_copy(update={"identification": idn})

    def new_tag(self) -> None:
        """Agrega un tag con la plantilla por defecto."""
        self._flush_editor()
        name = self._unique_tag(f"TW-{len(self.project.tags) + 1:03d}")
        self._insert_tag(TagRecord(input=default_input(name)), t("act.new_tag"))

    def _insert_tag(self, rec: TagRecord, text: str) -> None:
        tags = (*self.project.tags, rec)
        self._commit(self.project.model_copy(update={"tags": tags}), text)
        self.current = len(tags) - 1
        self._fill_tree()
        self._load_current()

    def duplicate_tag(self) -> None:
        """Duplica el tag activo."""
        if self.current < 0:
            return
        self._flush_editor()
        rec = self.project.tags[self.current]
        name = self._unique_tag(rec.input.identification.tag)
        self._insert_tag(rec.model_copy(update={"input": self._with_tag_name(rec.input, name),
                                                "last_status": None}),
                         t("act.duplicate_tag"))

    def delete_tag(self) -> None:
        """Elimina el tag activo (con confirmación)."""
        if self.current < 0 or len(self.project.tags) <= 1:
            return
        tag = self.project.tags[self.current].input.identification.tag
        if QMessageBox.question(self, t("act.delete_tag"), t("dlg.delete_tag", tag=tag)) \
                is not QMessageBox.StandardButton.Yes:
            return
        tags = list(self.project.tags)
        del tags[self.current]
        self._commit(self.project.model_copy(update={"tags": tuple(tags)}), t("act.delete_tag"))
        self.evaluations.clear()
        self.current = min(self.current, len(tags) - 1)
        self._fill_tree()
        self._load_current()

    def rename_tag(self) -> None:
        """Renombra el tag activo."""
        if self.current < 0:
            return
        rec = self.project.tags[self.current]
        name, ok = QInputDialog.getText(self, t("act.rename_tag"), t("dlg.rename"),
                                        text=rec.input.identification.tag)
        if ok and name.strip():
            new = rec.model_copy(update={"input": self._with_tag_name(rec.input, name.strip())})
            self._replace_tag(self.current, new, t("act.rename_tag"))
            self.editor.e_tag.setText(name.strip())

    def copy_tag(self) -> None:
        """Copia el tag activo al portapapeles como JSON."""
        if self.current >= 0:
            QApplication.clipboard().setText(self.project.tags[self.current].model_dump_json())

    def paste_tag(self) -> None:
        """Pega un tag copiado (JSON) como tag nuevo."""
        text = QApplication.clipboard().text()
        try:
            rec = TagRecord.model_validate_json(text)
        except ValueError:
            return
        name = self._unique_tag(rec.input.identification.tag)
        self._insert_tag(rec.model_copy(update={"input": self._with_tag_name(rec.input, name)}),
                         t("act.paste_tag"))

    # --- Cálculo ------------------------------------------------------------------------
    def calculate(self) -> Evaluation | None:
        """Calcula el tag activo."""
        self._calc_timer.stop()
        if self._edit_timer.isActive():
            self._edit_timer.stop()
            self._editor_settled()
            self._calc_timer.stop()
        if self.current < 0 or self.editor.validate() is None:
            self._refresh_status(t("status.invalid"))
            return None
        rec = self.project.tags[self.current]
        ev = evaluate(rec, self.library, self.project.settings)
        self.evaluations[self.current] = ev
        if rec.auto_properties:
            self.editor.show_properties(ev.input)
        self.results.show_evaluation(ev)
        self._chart_if_visible(ev)
        if ev.status is not None and ev.status != rec.last_status:
            tags = list(self.project.tags)
            tags[self.current] = rec.model_copy(update={"last_status": ev.status,
                                                        "input": ev.input})
            self.project = self.project.model_copy(update={"tags": tuple(tags)})
        item = self._tree_item(self.current)
        if item is not None:
            item.setIcon(0, _status_icon(ev.status))
        self._refresh_status(t("status.ready"))
        return ev

    def calculate_all(self) -> None:
        """Calcula todos los tags del proyecto."""
        self._flush_editor()
        tags = list(self.project.tags)
        for i, rec in enumerate(tags):
            ev = evaluate(rec, self.library, self.project.settings)
            self.evaluations[i] = ev
            tags[i] = rec.model_copy(update={"last_status": ev.status})
        self.project = self.project.model_copy(update={"tags": tuple(tags)})
        self._fill_tree()
        self._load_current()

    def optimize(self) -> None:
        """Propone alternativas para el tag activo (sin collares de velocidad)."""
        ev = self.evaluations.get(self.current) or self.calculate()
        if ev is None or ev.material is None:
            return
        cands = []
        for m in self.library.materials():
            if m.id != ev.material.material_id:
                try:
                    cands.append(self.library.material_properties(
                        m.id, ev.input.process.operating_temperature,
                        ev.input.process.design_temperature))
                except KeyError:
                    continue
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            alts = propose_alternatives(ev.input, ev.material, ev.options,
                                        candidate_materials=cands)
        finally:
            QApplication.restoreOverrideCursor()
        if alts:
            self.results.set_alternatives(alts)
        else:
            self.results.show_no_alternatives()
        self.results.alt_list.setToolTip(NO_COLLARS_NOTE)
        self.results.tabs.setCurrentIndex(4)

    def apply_alternative(self, alt: Alternative) -> None:
        """Aplica una alternativa al tag activo."""
        inp = alt.input
        if "material_id" in alt.changes:
            mat = inp.thermowell.material.model_copy(
                update={"material_id": str(alt.changes["material_id"])})
            inp = inp.model_copy(update={"thermowell": inp.thermowell.model_copy(
                update={"material": mat})})
        rec = self.project.tags[self.current].model_copy(update={"input": inp})
        self._replace_tag(self.current, rec, t("res.apply"))
        self.evaluations.pop(self.current, None)
        self._load_current()
        self.calculate()

    def show_sensitivity(self) -> None:
        """Abre la pestaña de gráficas."""
        self.results.tabs.setCurrentWidget(self.chart)

    def _results_tab(self, _index: int) -> None:
        ev = self.evaluations.get(self.current)
        if ev is not None:
            self._chart_if_visible(ev)

    def _chart_if_visible(self, ev: Evaluation) -> None:
        if self.results.tabs.currentWidget() is self.chart and ev is not self.chart.evaluation:
            self.chart.set_evaluation(ev)

    def edit_options(self) -> None:
        """Edita las opciones de cálculo del tag activo."""
        if self.current < 0:
            return
        rec = self.project.tags[self.current]
        dlg = OptionsDialog(rec.options, self)
        if dlg.exec():
            self._replace_tag(self.current, rec.model_copy(update={"options": dlg.options()}),
                              t("act.options"))
            self.calculate()

    def edit_project(self) -> None:
        """Edita los datos del proyecto y la presión barométrica."""
        dlg = ProjectDialog(self.project.info, self.project.settings, self)
        if dlg.exec():
            info, settings = dlg.result_data()
            self._commit(self.project.model_copy(update={"info": info, "settings": settings}),
                         t("act.project_info"))
            self._apply_project_settings()
            self._fill_tree()
            self._load_current()

    def _apply_project_settings(self) -> None:
        STATE.barometric = self.project.settings.barometric_pressure
        STATE.gauge = self.project.settings.pressure_as_gauge
        self.editor.refresh_units()

    # --- Archivo ---------------------------------------------------------------------
    def _confirm_discard(self) -> bool:
        if not self.dirty:
            return True
        answer = QMessageBox.question(
            self, "ThermoWell Sizer", t("dlg.unsaved"),
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel)
        if answer is QMessageBox.StandardButton.Save:
            return self.save()
        return answer is QMessageBox.StandardButton.Discard

    def new_project(self) -> None:
        """Proyecto nuevo con un tag."""
        if not self._confirm_discard():
            return
        self.project = Project(info=ProjectInfo(name=t("dlg.untitled")))
        self.path = None
        self.evaluations.clear()
        self.current = -1
        self.new_tag()
        self.undo.clear()
        self._set_dirty(False)

    def open_dialog(self) -> None:
        """Pide un archivo y lo abre."""
        if not self._confirm_discard():
            return
        name, _ = QFileDialog.getOpenFileName(self, t("act.open"), self._last_dir(),
                                              t("dlg.files"))
        if name:
            self.open_path(Path(name))

    def open_path(self, path: Path, *, ask_recover: bool = True) -> bool:
        """Abre un proyecto; ofrece recuperar un autoguardado más reciente."""
        source = path
        auto = path.with_name(path.name + AUTOSAVE_SUFFIX)
        if ask_recover and auto.exists() and auto.stat().st_mtime > path.stat().st_mtime:
            answer = QMessageBox.question(self, "ThermoWell Sizer", t("dlg.recover"))
            if answer is QMessageBox.StandardButton.Yes:
                source = auto
        try:
            project = load_project(source)
        except ProjectFileError as exc:
            QMessageBox.warning(self, t("dlg.open_error"), str(exc))
            return False
        if not project.tags:
            project = project.model_copy(update={"tags": (TagRecord(input=default_input()),)})
        self.project = project
        self.path = path
        self.evaluations.clear()
        self.current = 0
        self._apply_project_settings()
        self._fill_tree()
        self._load_current()
        self.undo.clear()
        self._set_dirty(source != path)
        self._add_recent(path)
        return True

    def save(self) -> bool:
        """Guarda el proyecto (pide nombre si no tiene)."""
        self._flush_editor()
        if self.path is None:
            return self.save_as()
        save_project(self.project, self.path)
        self.path.with_name(self.path.name + AUTOSAVE_SUFFIX).unlink(missing_ok=True)
        self.undo.setClean()
        self._set_dirty(False)
        self._add_recent(self.path)
        self._refresh_status(t("status.saved"))
        return True

    def save_as(self) -> bool:
        """Guarda con otro nombre."""
        name, _ = QFileDialog.getSaveFileName(self, t("act.save_as"), self._last_dir(),
                                              t("dlg.files"))
        if not name:
            return False
        path = Path(name)
        if path.suffix != FILE_EXTENSION:
            path = path.with_suffix(FILE_EXTENSION)
        self.path = path
        return self.save()

    def autosave(self) -> None:
        """Guarda una copia de seguridad sin tocar el archivo original."""
        if not self.dirty:
            return
        self._flush_editor()
        if self.path is not None:
            target = self.path.with_name(self.path.name + AUTOSAVE_SUFFIX)
        else:
            target = Path(self.settings.fileName()).parent / ("sin_titulo" + FILE_EXTENSION
                                                              + AUTOSAVE_SUFFIX)
        target.parent.mkdir(parents=True, exist_ok=True)
        save_project(self.project, target)
        self._refresh_status(t("status.autosaved"))

    def _last_dir(self) -> str:
        return str(self.settings.value("files/last_dir", str(Path.home())))

    def _add_recent(self, path: Path) -> None:
        recent = [p for p in self._recent() if p != str(path)]
        recent.insert(0, str(path))
        self.settings.setValue("files/recent", recent[:MAX_RECENT])
        self.settings.setValue("files/last_dir", str(path.parent))
        self._fill_recent()

    def _recent(self) -> list[str]:
        value = self.settings.value("files/recent", [])
        if isinstance(value, str):
            return [value]
        return [str(v) for v in value] if isinstance(value, list) else []

    def _fill_recent(self) -> None:
        self.recent_menu.clear()
        for p in self._recent():
            act = self.recent_menu.addAction(p)
            act.triggered.connect(lambda *_, p=p: self._confirm_discard()
                                  and self.open_path(Path(p)))
        self.recent_menu.setEnabled(bool(self._recent()))

    def import_table(self) -> None:
        """Importa tags desde CSV o Excel."""
        name, _ = QFileDialog.getOpenFileName(self, t("act.import_csv"), self._last_dir(),
                                              "CSV / Excel (*.csv *.txt *.xlsx)")
        if not name:
            return
        records, errors = import_rows(read_table(Path(name)), self.library,
                                      self.project.settings.barometric_pressure)
        if records:
            renamed = [r.model_copy(update={"input": self._with_tag_name(
                r.input, self._unique_tag(r.input.identification.tag))}) for r in records]
            self._commit(self.project.model_copy(update={"tags": (*self.project.tags,
                                                                  *renamed)}),
                         t("act.import_csv"))
            self._fill_tree()
        msg = t("dlg.import_done", n=len(records))
        if errors:
            QMessageBox.warning(self, t("dlg.import_errors"), msg + "\n\n" + "\n".join(errors[:20]))
        else:
            QMessageBox.information(self, t("act.import_csv"), msg)

    def save_template(self) -> None:
        """Guarda la plantilla CSV de importación."""
        name, _ = QFileDialog.getSaveFileName(self, t("act.import_template"),
                                              str(Path(self._last_dir()) / "plantilla_tags.csv"),
                                              "CSV (*.csv)")
        if name:
            Path(name).write_text(template_csv(), encoding="utf-8-sig")

    def tag_export(self, index: int) -> dict[str, object]:
        """Datos de entrada y resultados de un tag, listos para JSON."""
        rec = self.project.tags[index]
        ev = self.evaluations.get(index) or evaluate(rec, self.library, self.project.settings)
        res = ev.result
        return {
            "input": json.loads(ev.input.model_dump_json()),
            "options": json.loads(ev.options.model_dump_json()),
            "status": res.status.value if res else None,
            "checks": [json.loads(c.model_dump_json()) for c in res.checks] if res else [],
            "units": "SI (m, kg, s, Pa abs, K)",
        }

    def export_tag_json(self) -> None:
        """Exporta el tag activo con sus resultados a JSON."""
        if self.current < 0:
            return
        tag = self.project.tags[self.current].input.identification.tag
        name, _ = QFileDialog.getSaveFileName(self, t("act.export_json"),
                                              str(Path(self._last_dir()) / f"{tag}.json"),
                                              "JSON (*.json)")
        if name:
            Path(name).write_text(json.dumps(self.tag_export(self.current), indent=2,
                                             ensure_ascii=False), encoding="utf-8")

    def export_project_json(self) -> None:
        """Exporta todo el proyecto con resultados a JSON."""
        name, _ = QFileDialog.getSaveFileName(self, t("act.export_project_json"),
                                              str(Path(self._last_dir()) / "proyecto.json"),
                                              "JSON (*.json)")
        if name:
            data = {"project": json.loads(self.project.info.model_dump_json()),
                    "tags": [self.tag_export(i) for i in range(len(self.project.tags))]}
            Path(name).write_text(json.dumps(data, indent=2, ensure_ascii=False),
                                  encoding="utf-8")

    # --- Preferencias de presentación ----------------------------------------------------
    def set_units(self, system: UnitSystem) -> None:
        """Cambia el sistema de unidades de toda la interfaz."""
        self._flush_editor()
        STATE.units = system
        self.settings.setValue("ui/units", system.value)
        self._sync_checks()
        self.editor.refresh_units()
        self._load_current()

    def toggle_units(self) -> None:
        """Alterna SI / imperial."""
        self.set_units(UnitSystem.IMPERIAL if STATE.units is UnitSystem.SI else UnitSystem.SI)

    def set_language(self, lang: Language) -> None:
        """Cambia el idioma reconstruyendo la ventana con el mismo proyecto."""
        self._sync_checks()
        if lang is STATE.language:
            return
        self._flush_editor()
        STATE.language = lang
        self.settings.setValue("ui/language", lang.value)
        if self._rebuild is not None:
            self._rebuild(self)

    def toggle_theme(self) -> None:
        """Alterna tema claro / oscuro."""
        STATE.dark = self.act_dark.isChecked()
        self.settings.setValue("ui/dark", STATE.dark)
        app = QApplication.instance()
        if isinstance(app, QApplication):
            apply_theme(app, STATE.dark)
        self.chart.redraw()
        self.preview.update()

    def toggle_expert(self) -> None:
        """Alterna asistente / modo experto."""
        self.settings.setValue("ui/expert", self.act_expert.isChecked())
        self.editor.set_expert(self.act_expert.isChecked())

    # --- Ventanas auxiliares ----------------------------------------------------------
    def open_help(self, topic: str | None = None) -> None:
        """Ayuda contextual: abre el tema del paso visible del asistente."""
        if self.help_window is None:
            self.help_window = HelpWindow()
        if topic is None:
            step = self.editor.current_step()
            topic = STEP_TOPICS[step] if 0 <= step < len(STEP_TOPICS) else "start"
        self.help_window.show_topic(topic)

    def open_library(self, tab: str = "materials", ref: tuple[str, str] | None = None) -> None:
        """Abre el navegador de la biblioteca."""
        if self.library_window is None:
            self.library_window = LibraryWindow(self.library)
        self.library_window.tabs.setCurrentIndex(LibraryWindow.TABS.index(tab)
                                                 if tab in LibraryWindow.TABS else 0)
        if ref is not None:
            self.library_window.show_item(*ref)
        self.library_window.show()
        self.library_window.raise_()

    def open_search(self) -> None:
        """Buscador global."""
        dlg = SearchPalette(self.library, self)
        dlg.selected.connect(lambda kind, ref: self.open_library(kind, (kind, ref)))
        dlg.exec()

    def open_assistant(self) -> None:
        """Asistente de selección de material con las condiciones del tag."""
        if self.assistant is None:
            self.assistant = MaterialAssistant(self.library)
            self.assistant.material_chosen.connect(self._use_material)
        if self.current >= 0:
            proc = self.project.tags[self.current].input.process
            c = proc.corrosion
            self.assistant.preset(proc.design_temperature, None, c.h2s_partial_pressure,
                                  c.chlorides_ppm, c.nace_service, c.solids_or_erosive)
        self.assistant.show()
        self.assistant.raise_()

    def _use_material(self, material_id: str) -> None:
        idx = self.editor.c_material.findData(material_id)
        if idx >= 0:
            self.editor.c_material.setCurrentIndex(idx)

    def open_converter(self) -> None:
        """Conversor de unidades (Fase 5)."""
        self._open_tool("converter")

    def open_calculators(self) -> None:
        """Calculadoras (Fase 5)."""
        self._open_tool("calculators")

    def _open_tool(self, name: str) -> None:
        try:
            tools = importlib.import_module("thermowell_sizer.ui.tools")
        except ImportError:
            QMessageBox.information(self, "ThermoWell Sizer", t("dlg.feature_later"))
            return
        win = tools.open_tool(name, self.library)
        self.tool_windows.append(win)

    def report(self, kind: str) -> None:
        """Genera un reporte (Fase 6)."""
        try:
            report_actions = importlib.import_module("thermowell_sizer.ui.report_actions")
        except ImportError:
            QMessageBox.information(self, "ThermoWell Sizer", t("dlg.feature_later"))
            return
        report_actions.run(self, kind)

    def show_shortcuts(self) -> None:
        """Lista de atajos de teclado."""
        QMessageBox.information(self, t("act.shortcuts"),
                                t("dlg.shortcuts_text").replace(" · ", "\n"))

    def show_license(self) -> None:
        """Estado de la licencia e instalación de una nueva."""
        importlib.import_module("thermowell_sizer.ui.license_ui").show(self)

    # --- Cierre -------------------------------------------------------------------------
    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802 - API de Qt
        """Pide confirmación si hay cambios y guarda la geometría de la ventana."""
        if getattr(self, "_rebuilding", False) or self._confirm_discard():
            self.settings.setValue("window/geometry", self.saveGeometry())
            for w in (self.help_window, self.library_window, self.assistant,
                      *self.tool_windows):
                if w is not None:
                    w.close()
            event.accept()
        else:
            event.ignore()

