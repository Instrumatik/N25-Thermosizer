"""Ventanas de biblioteca: navegador técnico, buscador global y asistente de material."""

from __future__ import annotations

from html import escape

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor, QKeyEvent
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.data import seed_tables
from thermowell_sizer.data.database import Library, MaterialInfo
from thermowell_sizer.data.reference import REFERENCE_TABLES, RefTable
from thermowell_sizer.data.reference import text as ref_text
from thermowell_sizer.data.selection import (
    MaterialEvaluation,
    ServiceConditions,
    Verdict,
    recommend_materials,
)
from thermowell_sizer.i18n import Language, tr
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.text import t
from thermowell_sizer.ui.widgets import QuantityEdit, fmt, fmt_quantity

VERDICT_COLORS = {Verdict.RECOMMENDED: "#2e9e44", Verdict.ACCEPTABLE: "#e0a100",
                  Verdict.NOT_RECOMMENDED: "#d0342c"}
COMPAT_COLORS = {"A": "#2e9e44", "B": "#e0a100", "C": "#d0342c", "N/D": "#8a8f98"}


def _es() -> bool:
    return STATE.language is Language.ES


def _table(headers: list[str]) -> QTableWidget:
    tbl = QTableWidget(0, len(headers))
    tbl.setHorizontalHeaderLabels(headers)
    tbl.verticalHeader().setVisible(False)
    tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    tbl.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    tbl.horizontalHeader().setStretchLastSection(True)
    return tbl


def _set_rows(tbl: QTableWidget, rows: list[list[str]]) -> None:
    tbl.setRowCount(len(rows))
    for r, row in enumerate(rows):
        for c, text in enumerate(row):
            tbl.setItem(r, c, QTableWidgetItem(text))
    tbl.resizeColumnsToContents()


def agent_name(agent: str) -> str:
    """Nombre traducido de un agente químico."""
    return tr(f"agent.{agent}", STATE.language)


def reason_text(reason: str) -> str:
    """Texto de un motivo de selección (``sel.clave`` o ``sel.clave:agente``)."""
    key, _, agent = reason.partition(":")
    return tr(key, STATE.language, agent=agent_name(agent)) if agent else tr(key,
                                                                            STATE.language)


class LibraryWindow(QWidget):
    """Navegador de la biblioteca técnica (no modal)."""

    TABS = ("materials", "fluids", "flanges", "pipes", "glossary", "standards")

    def __init__(self, library: Library, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.library = library
        self.setWindowTitle(t("lib.title"))
        self.resize(980, 620)
        self.tabs = QTabWidget()
        self.tabs.addTab(self._materials(), t("act.materials"))
        self.tabs.addTab(self._fluids(), t("act.fluids"))
        self.tabs.addTab(self._flanges(), t("act.flanges"))
        self.tabs.addTab(self._pipes(), "B36.10M")
        self.tabs.addTab(self._glossary(), t("act.glossary"))
        self.tabs.addTab(self._standards(), t("act.standards"))
        self.tabs.addTab(self._references(), t("lib.references"))
        note = QLabel("⚠ " + t("lib.unverified"))
        note.setObjectName("warningLabel")
        lay = QVBoxLayout(self)
        lay.addWidget(self.tabs, 1)
        lay.addWidget(note)

    def show_item(self, kind: str, ref_id: str) -> None:
        """Abre la pestaña y el elemento pedido (desde el buscador)."""
        if kind in ("material", "coating"):
            self.tabs.setCurrentIndex(0)
            for r in range(self.mat_table.rowCount()):
                item = self.mat_table.item(r, 0)
                if item is not None and item.data(Qt.ItemDataRole.UserRole) == ref_id:
                    self.mat_table.selectRow(r)
        elif kind == "fluid":
            self.tabs.setCurrentIndex(1)
        elif kind == "glossary":
            self.tabs.setCurrentIndex(4)
            for i in range(self.gl_list.count()):
                if self.gl_list.item(i).data(Qt.ItemDataRole.UserRole) == ref_id:
                    self.gl_list.setCurrentRow(i)
        elif kind == "standard":
            self.tabs.setCurrentIndex(5)
            for i in range(self.std_list.count()):
                if self.std_list.item(i).data(Qt.ItemDataRole.UserRole) == ref_id:
                    self.std_list.setCurrentRow(i)
        self.show()
        self.raise_()
        self.activateWindow()

    # --- Materiales -----------------------------------------------------------------
    def _materials(self) -> QWidget:
        split = QSplitter()
        self.mat_table = _table([t("lib.name"), t("lib.spec"), "UNS", t("lib.tmax"),
                                 t("lib.class"), t("lib.nace"), t("lib.group")])
        mats = self.library.materials()
        self.mat_table.setRowCount(len(mats))
        for r, m in enumerate(mats):
            vals = [m.name, m.spec, m.uns, fmt_quantity(m.max_temperature,
                                                        QuantityKind.TEMPERATURE),
                    m.fatigue_class + ("" if m.fatigue_covered else " *"),
                    "✔" if m.nace_ok else "—", m.b16_5_group or "—"]
            for c, text in enumerate(vals):
                item = QTableWidgetItem(text)
                if c == 0:
                    item.setData(Qt.ItemDataRole.UserRole, m.id)
                self.mat_table.setItem(r, c, item)
        self.mat_table.resizeColumnsToContents()
        self.mat_detail = QTextBrowser()
        self.mat_table.currentCellChanged.connect(lambda r, *_: self._show_material(r))
        split.addWidget(self.mat_table)
        split.addWidget(self.mat_detail)
        split.setSizes([560, 400])
        return split

    def _show_material(self, row: int) -> None:
        item = self.mat_table.item(row, 0)
        if item is None:
            return
        m = self.library.material(item.data(Qt.ItemDataRole.UserRole))
        e = self.library.property_curve(m.id, "elastic_modulus")
        s = dict(self.library.property_curve(m.id, "allowable_stress"))
        temps = sorted({x for x, _ in e} | set(s))
        e_map = dict(e)
        rows = "".join(
            f"<tr><td>{fmt_quantity(tk, QuantityKind.TEMPERATURE)}</td>"
            f"<td>{fmt_quantity(e_map[tk], QuantityKind.ELASTIC_MODULUS) if tk in e_map else ''}"
            f"</td><td>{fmt_quantity(s[tk], QuantityKind.STRESS) if tk in s else ''}</td></tr>"
            for tk in temps)
        compat = self.library.compatibility(m.id)
        comp_rows = "".join(
            f"<tr><td>{agent_name(a)}</td><td style='color:{COMPAT_COLORS[r]}'><b>{r}</b></td>"
            "</tr>" for a, r in compat.items())
        notes = m.notes_es if _es() else m.notes_en
        self.mat_detail.setHtml(
            f"<h3>{m.name}</h3><p>{m.spec} · UNS {m.uns}</p><p>{notes}</p>"
            f"<p>ρ = {fmt_quantity(m.density, QuantityKind.DENSITY)}</p>"
            f"<table border='0' cellpadding='3'><tr><th>T</th><th>E</th><th>S</th></tr>{rows}"
            f"</table><h4>{t('lib.compat')}</h4><table cellpadding='2'>{comp_rows}</table>"
            f"<p><i>{t('lib.unverified')}</i></p>")

    # --- Fluidos ----------------------------------------------------------------------
    def _fluids(self) -> QWidget:
        self.fl_table = _table([t("lib.name"), t("f.phase"), t("lib.coolprop")])
        self.reload_fluids()
        return self.fl_table

    def reload_fluids(self) -> None:
        """Recarga la lista de fluidos."""
        rows = [[f.name_es if _es() else f.name_en, f.default_phase,
                 f.coolprop_name or "tabla" if not f.user_defined else "usuario"]
                for f in self.library.fluids()]
        _set_rows(self.fl_table, rows)

    # --- Bridas y tuberías ----------------------------------------------------------
    def _flanges(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        top = QHBoxLayout()
        self.fg_group = QComboBox()
        self.fg_group.addItems(self.library.flange_groups())
        top.addWidget(QLabel(t("lib.group")))
        top.addWidget(self.fg_group)
        top.addStretch(1)
        lay.addLayout(top)
        classes = (150, 300, 600, 900, 1500, 2500)
        self.fg_table = _table([t("lib.temperature"), *[f"Cl. {c}" for c in classes]])
        lay.addWidget(self.fg_table)

        def fill() -> None:
            group = self.fg_group.currentText()
            rows = []
            for tc in seed_tables.FLANGE_TEMPS_C:
                tk = tc + 273.15
                row = [fmt_quantity(tk, QuantityKind.TEMPERATURE)]
                for c in classes:
                    p = self.library.flange_rating(group, c, tk)
                    row.append(fmt_quantity(p + STATE.barometric, QuantityKind.PRESSURE,
                                            gauge=True) if p is not None else "—")
                rows.append(row)
            _set_rows(self.fg_table, rows)

        self.fg_group.currentIndexChanged.connect(fill)
        fill()
        return w

    def _pipes(self) -> QWidget:
        tbl = _table(["NPS", "DN", "Sch", t("lib.od"), t("lib.wall"), t("f.pipe_id")])
        rows = []
        for nps in self.library.pipe_sizes():
            for sch in self.library.schedules(nps):
                p = self.library.pipe(nps, sch)
                rows.append([nps, str(p.dn), sch,
                             fmt_quantity(p.outer_diameter, QuantityKind.DIAMETER),
                             fmt_quantity(p.wall_thickness, QuantityKind.LENGTH),
                             fmt_quantity(p.inner_diameter, QuantityKind.DIAMETER)])
        _set_rows(tbl, rows)
        return tbl

    # --- Glosario y normas -----------------------------------------------------------
    def _glossary(self) -> QWidget:
        split = QSplitter()
        self.gl_list = QListWidget()
        self.gl_view = QTextBrowser()
        self._terms = self.library.glossary()
        for g in self._terms:
            item = QListWidgetItem(g.term_es if _es() else g.term_en)
            item.setData(Qt.ItemDataRole.UserRole, g.id)
            self.gl_list.addItem(item)

        def show(row: int) -> None:
            if 0 <= row < len(self._terms):
                g = self._terms[row]
                other = g.term_en if _es() else g.term_es
                body = g.definition_es if _es() else g.definition_en
                formula = f"<p><code>{g.formula}</code></p>" if g.formula else ""
                self.gl_view.setHtml(f"<h3>{g.term_es if _es() else g.term_en}</h3>"
                                     f"<p><i>{other}</i></p><p>{body}</p>{formula}")

        self.gl_list.currentRowChanged.connect(show)
        split.addWidget(self.gl_list)
        split.addWidget(self.gl_view)
        split.setSizes([300, 660])
        return split

    def _references(self) -> QWidget:
        split = QSplitter()
        self.ref_list = QListWidget()
        self.ref_view = QTextBrowser()
        for table in REFERENCE_TABLES:
            item = QListWidgetItem(ref_text(table.title, _es()))
            item.setData(Qt.ItemDataRole.UserRole, table.id)
            self.ref_list.addItem(item)

        def show(row: int) -> None:
            if 0 <= row < len(REFERENCE_TABLES):
                self.ref_view.setHtml(reference_html(REFERENCE_TABLES[row], _es()))

        self.ref_list.currentRowChanged.connect(show)
        self.ref_list.setCurrentRow(0)
        split.addWidget(self.ref_list)
        split.addWidget(self.ref_view)
        split.setSizes([260, 700])
        return split

    def _standards(self) -> QWidget:
        split = QSplitter()
        self.std_list = QListWidget()
        self.std_view = QTextBrowser()
        stds = self.library.standards()
        for s in stds:
            item = QListWidgetItem(f"{s[1]} ({s[2]})")
            item.setData(Qt.ItemDataRole.UserRole, s[0])
            self.std_list.addItem(item)

        def show(row: int) -> None:
            if 0 <= row < len(stds):
                s = stds[row]
                self.std_view.setHtml(f"<h3>{s[1]}</h3><p>{t('lib.edition')}: {s[2]}</p>"
                                      f"<p>{s[3] if _es() else s[4]}</p>")

        self.std_list.currentRowChanged.connect(show)
        split.addWidget(self.std_list)
        split.addWidget(self.std_view)
        split.setSizes([300, 660])
        return split


def reference_html(table: RefTable, es: bool) -> str:
    """Tabla de referencia como HTML para el visor."""
    head = "".join(f"<th align='left'>{escape(ref_text(h, es))}</th>" for h in table.headers)
    body = "".join("<tr>" + "".join(f"<td>{escape(ref_text(c, es))}</td>" for c in row) + "</tr>"
                   for row in table.rows)
    return (f"<h3>{escape(ref_text(table.title, es))}</h3>"
            f"<table border='1' cellspacing='0' cellpadding='4'><tr>{head}</tr>{body}</table>"
            f"<p><i>{escape(ref_text(table.note, es))}</i></p>")


class SearchPalette(QDialog):
    """Buscador global (Ctrl+K) con tolerancia a errores de escritura."""

    selected = Signal(str, str)

    def __init__(self, library: Library, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.library = library
        self.setWindowTitle(t("act.search"))
        self.resize(560, 380)
        self.edit = QLineEdit()
        self.edit.setPlaceholderText(t("lib.search_hint"))
        self.results = QListWidget()
        lay = QVBoxLayout(self)
        lay.addWidget(self.edit)
        lay.addWidget(self.results)
        self.edit.textChanged.connect(self._search)
        self.results.itemActivated.connect(self._choose)
        self.edit.returnPressed.connect(self._choose_first)

    def _search(self, text: str) -> None:
        self.results.clear()
        kinds = {"material": "🔩", "coating": "🛡", "fluid": "💧", "glossary": "📖",
                 "standard": "📘"}
        for hit in self.library.search(text):
            item = QListWidgetItem(f"{kinds.get(hit.kind, '•')} {hit.title}")
            item.setData(Qt.ItemDataRole.UserRole, (hit.kind, hit.ref_id))
            self.results.addItem(item)
        if self.results.count():
            self.results.setCurrentRow(0)

    def _choose_first(self) -> None:
        item = self.results.currentItem()
        if item is not None:
            self._choose(item)

    def _choose(self, item: QListWidgetItem) -> None:
        kind, ref_id = item.data(Qt.ItemDataRole.UserRole)
        self.selected.emit(kind, ref_id)
        self.accept()

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802 - API de Qt
        """Flechas para moverse por los resultados sin dejar el campo de texto."""
        if event.key() in (Qt.Key.Key_Down, Qt.Key.Key_Up):
            delta = 1 if event.key() == Qt.Key.Key_Down else -1
            row = min(max(self.results.currentRow() + delta, 0), self.results.count() - 1)
            self.results.setCurrentRow(row)
            return
        super().keyPressEvent(event)


class MaterialAssistant(QWidget):
    """Asistente de selección de material (no modal)."""

    material_chosen = Signal(str)

    def __init__(self, library: Library, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.library = library
        self.setWindowTitle(t("sel.title"))
        self.resize(900, 560)
        form = QFormLayout()
        self.q_tmax = QuantityEdit(QuantityKind.TEMPERATURE)
        self.q_tmin = QuantityEdit(QuantityKind.TEMPERATURE, optional=True)
        self.q_h2s = QuantityEdit(QuantityKind.PRESSURE, optional=True)
        self.e_cl = QLineEdit("0")
        self.chk_nace = QCheckBox(t("f.nace"))
        self.chk_erosive = QCheckBox(t("f.erosive"))
        form.addRow(t("f.t_design"), self.q_tmax)
        form.addRow("T mín.", self.q_tmin)
        form.addRow(t("f.h2s"), self.q_h2s)
        form.addRow(t("f.chlorides"), self.e_cl)
        form.addRow(self.chk_nace)
        form.addRow(self.chk_erosive)
        agents_box = QGridLayout()
        self.agent_checks: dict[str, QCheckBox] = {}
        for i, agent in enumerate(seed_tables.AGENTS):
            chk = QCheckBox(agent_name(agent))
            self.agent_checks[agent] = chk
            agents_box.addWidget(chk, i // 2, i % 2)
        left = QVBoxLayout()
        left.addLayout(form)
        left.addWidget(QLabel(f"<b>{t('sel.agents')}</b>"))
        left.addLayout(agents_box)
        btn = QPushButton(t("sel.evaluate"))
        btn.clicked.connect(self.evaluate)
        self.btn_use = QPushButton(t("sel.use"))
        self.btn_use.clicked.connect(self._use)
        left.addWidget(btn)
        left.addWidget(self.btn_use)
        left.addStretch(1)
        self.table = _table([t("f.material"), t("sel.verdict"), t("sel.score"),
                             t("sel.reasons"), t("f.coating")])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        lay = QHBoxLayout(self)
        lw = QWidget()
        lw.setLayout(left)
        lw.setMaximumWidth(340)
        lay.addWidget(lw)
        lay.addWidget(self.table, 1)
        self.evaluations: list[MaterialEvaluation] = []

    def preset(self, design_t: float, min_t: float | None, h2s: float, chlorides: float,
               nace: bool, erosive: bool) -> None:
        """Carga las condiciones del tag activo."""
        self.q_tmax.set_value(design_t)
        self.q_tmin.set_value(min_t)
        self.q_h2s.set_value(h2s or None)
        self.e_cl.setText(fmt(chlorides, 0))
        self.chk_nace.setChecked(nace)
        self.chk_erosive.setChecked(erosive)
        self.evaluate()

    def evaluate(self) -> None:
        """Evalúa la matriz con las condiciones cargadas."""
        try:
            cl = float(self.e_cl.text().replace(",", ".") or 0)
        except ValueError:
            cl = 0.0
        cond = ServiceConditions(
            design_temperature=self.q_tmax.value() or 293.15,
            min_temperature=self.q_tmin.value(),
            nace_service=self.chk_nace.isChecked(),
            h2s_partial_pressure=self.q_h2s.value() or 0.0,
            chlorides_ppm=cl,
            agents=tuple(a for a, c in self.agent_checks.items() if c.isChecked()),
            erosive=self.chk_erosive.isChecked(),
        )
        self.evaluations = recommend_materials(self.library, cond)
        self.table.setRowCount(len(self.evaluations))
        coat_names = {c[0]: (c[1] if _es() else c[2]) for c in self.library.coatings()}
        for r, ev in enumerate(self.evaluations):
            verdict = QTableWidgetItem(t(f"sel.verdict.{ev.verdict.value}"))
            verdict.setForeground(QBrush(QColor(VERDICT_COLORS[ev.verdict])))
            cells = [QTableWidgetItem(ev.material.name), verdict,
                     QTableWidgetItem(fmt(ev.score, 0)),
                     QTableWidgetItem("; ".join(reason_text(x) for x in ev.reasons) or "—"),
                     QTableWidgetItem(", ".join(coat_names[c] for c in ev.coatings) or "—")]
            for c, item in enumerate(cells):
                self.table.setItem(r, c, item)
        self.table.resizeRowsToContents()

    def _use(self) -> None:
        row = self.table.currentRow()
        if 0 <= row < len(self.evaluations):
            info: MaterialInfo = self.evaluations[row].material
            self.material_chosen.emit(info.id)
