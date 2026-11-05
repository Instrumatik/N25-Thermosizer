"""Panel de resultados: semáforo global, criterios con margen, resumen, traza y gráficas."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QListWidget,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from thermowell_sizer.core.analysis.optimize import Alternative
from thermowell_sizer.core.models import CheckResult, CheckStatus
from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.i18n import tr
from thermowell_sizer.services import Evaluation
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.text import t
from thermowell_sizer.ui.widgets import STATUS_COLORS, StatusLight, fmt, fmt_quantity

CRITERION_KIND: dict[str, tuple[QuantityKind, bool]] = {
    "material_temperature": (QuantityKind.TEMPERATURE, False),
    "pressure_rating": (QuantityKind.PRESSURE, True),
    "pressure_high_service": (QuantityKind.PRESSURE, True),
    "flange_rating": (QuantityKind.PRESSURE, True),
    "low_velocity": (QuantityKind.VELOCITY, False),
    "frequency_limit": (QuantityKind.FREQUENCY, False),
    "inline_lockin_dwell": (QuantityKind.FREQUENCY, False),
    "fatigue_data": (QuantityKind.STRESS, False),
}
CRITERION_NAMES: dict[str, tuple[str, str]] = {
    "scope": ("Alcance de la norma", "Scope of the standard"),
    "material_temperature": ("Temperatura del material", "Material temperature"),
    "fatigue_data": ("Datos de fatiga", "Fatigue data"),
    "pressure_rating": ("Presión externa", "External pressure"),
    "pressure_high_service": ("Servicio de alta presión", "High-pressure service"),
    "flange_rating": ("Rating de brida", "Flange rating"),
    "low_velocity": ("Exención por baja velocidad", "Low-velocity exemption"),
    "steady_stress_support": ("Esfuerzo estacionario (soporte)", "Steady stress (support)"),
    "steady_stress_step": ("Esfuerzo estacionario (escalón)", "Steady stress (step)"),
    "dynamic_stress_support": ("Esfuerzo dinámico (soporte)", "Dynamic stress (support)"),
    "dynamic_stress_step": ("Esfuerzo dinámico (escalón)", "Dynamic stress (step)"),
    "frequency_limit": ("Límite de frecuencia", "Frequency limit"),
    "inline_lockin_dwell": ("Captura en línea", "In-line lock-in"),
}
MARGIN_DECIMALS = 1


def short_reference(reference: str) -> str:
    """Referencia sin el prefijo de la norma, que es común a casi todas."""
    return reference.replace("ASME PTC 19.3 TW-2016, ", "PTC 19.3 TW ")


def criterion_name(cid: str) -> str:
    """Nombre legible del criterio."""
    pair = CRITERION_NAMES.get(cid, (cid, cid))
    return pair[0] if STATE.language.value == "es" else pair[1]


def format_check_value(check: CheckResult, value: float) -> str:
    """Valor del criterio en unidades de presentación."""
    kind, gauge_pa = CRITERION_KIND.get(check.criterion_id, (QuantityKind.STRESS, False))
    if check.criterion_id == "scope":
        return fmt(value)
    if gauge_pa:
        return fmt_quantity(value + STATE.barometric, kind, gauge=True)
    return fmt_quantity(value, kind)


def scope_label(scope: str) -> str:
    """Etiqueta de un caso, con la variante de corrosión si corresponde."""
    if not scope:
        return "—"
    base, _, variant = scope.partition("|")
    names = {"min": ("Mín.", "Min"), "normal": ("Normal", "Normal"), "max": ("Máx.", "Max"),
             "root_corrosion": ("corr. raíz", "root corr."),
             "tip_corrosion": ("corr. punta", "tip corr.")}
    idx = 0 if STATE.language.value == "es" else 1
    text = names.get(base, (base, base))[idx]
    if variant:
        text += " · " + names.get(variant, (variant, variant))[idx]
    return text


class ResultsPanel(QWidget):
    """Muestra una :class:`Evaluation`."""

    apply_alternative = Signal(object)
    optimize_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.light = StatusLight()
        self.lbl_summary = QLabel()
        self.lbl_summary.setWordWrap(True)
        top = QHBoxLayout()
        top.addWidget(self.light)
        top.addWidget(self.lbl_summary, 1)

        self.table = QTableWidget(0, 6)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.cases = QTableWidget(0, 0)
        self.cases.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.notes = QTextBrowser()
        self.trace = QTextBrowser()
        self.alt_list = QListWidget()
        self.btn_alt = QPushButton(t("act.optimize"))
        self.btn_apply = QPushButton(t("res.apply"))
        self.btn_apply.setEnabled(False)
        self.btn_alt.clicked.connect(self.optimize_requested)
        self.btn_apply.clicked.connect(self._apply)
        self.alt_list.currentRowChanged.connect(lambda r: self.btn_apply.setEnabled(r >= 0))
        alt = QWidget()
        alt_l = QVBoxLayout(alt)
        alt_l.addWidget(self.alt_list)
        row = QHBoxLayout()
        row.addWidget(self.btn_alt)
        row.addWidget(self.btn_apply)
        row.addStretch(1)
        alt_l.addLayout(row)
        self._alternatives: list[Alternative] = []

        self.tabs = QTabWidget()
        self.tabs.addTab(self.table, t("panel.results"))
        self.tabs.addTab(self.cases, t("res.summary"))
        self.tabs.addTab(self.notes, t("res.notes"))
        self.tabs.addTab(self.trace, t("res.trace"))
        self.tabs.addTab(alt, t("res.alternatives"))
        lay = QVBoxLayout(self)
        lay.addLayout(top)
        lay.addWidget(self.tabs, 1)
        self.clear()

    def add_tab(self, widget: QWidget, title: str) -> None:
        """Agrega una pestaña externa (p. ej. las gráficas)."""
        self.tabs.addTab(widget, title)

    def clear(self) -> None:
        """Estado sin calcular."""
        self.light.set_status(None)
        self.lbl_summary.setText(t("res.not_calculated"))
        self.table.setRowCount(0)
        self.cases.setRowCount(0)
        self.notes.clear()
        self.trace.clear()
        self.set_alternatives([])

    def show_evaluation(self, ev: Evaluation) -> None:
        """Rellena todas las pestañas."""
        res = ev.result
        if res is None:
            self.clear()
            self.notes.setPlainText("\n".join(t(k) for k in ev.errors + ev.warnings))
            return
        self.light.set_status(res.status)
        counts = {s: sum(1 for c in res.checks if c.status is s) for s in CheckStatus}
        fn = res.cases[0].fnc if res.cases else None
        parts = [f"✔ {counts[CheckStatus.PASS]}  ⚠ {counts[CheckStatus.WARNING]}  "
                 f"✖ {counts[CheckStatus.FAIL]}"]
        if fn is not None:
            parts.append(f"f_n,c = {fmt_quantity(fn, QuantityKind.FREQUENCY)}")
        if ev.material is not None:
            parts.append(ev.material.name)
        self.lbl_summary.setText(" · ".join(parts))
        self._fill_checks(res.checks)
        self._fill_cases(ev)
        notes = [tr(n, STATE.language) for n in res.notes]
        notes += [t(w) for w in ev.warnings]
        notes += [f"{i.field}: {tr(i.message_key, STATE.language)}" for i in res.issues]
        self.notes.setPlainText("\n\n".join(notes) if notes else "—")
        self._fill_trace(ev)

    def _fill_checks(self, checks: list[CheckResult]) -> None:
        heads = [t("res.criterion"), t("res.case"), t("res.value"), t("res.limit"),
                 t("res.margin"), t("res.ref")]
        self.table.setHorizontalHeaderLabels(heads)
        order = {CheckStatus.FAIL: 0, CheckStatus.WARNING: 1, CheckStatus.PASS: 2,
                 CheckStatus.NOT_APPLICABLE: 3}
        rows = sorted(checks, key=lambda c: (order[c.status], c.margin_pct))
        self.table.setRowCount(len(rows))
        for r, c in enumerate(rows):
            name = QTableWidgetItem(f"● {criterion_name(c.criterion_id)}")
            name.setForeground(QBrush(QColor(STATUS_COLORS[c.status])))
            name.setToolTip(tr(c.message_key, STATE.language))
            plain = c.criterion_id == "scope" or c.status is CheckStatus.NOT_APPLICABLE
            margin = "—" if plain else f"{fmt(c.margin_pct, MARGIN_DECIMALS)} %"
            values = [scope_label(c.flow_case),
                      "—" if plain else format_check_value(c, c.value),
                      "—" if plain else format_check_value(c, c.limit), margin,
                      short_reference(c.reference)]
            self.table.setItem(r, 0, name)
            for col, text in enumerate(values, start=1):
                item = QTableWidgetItem(text)
                if col in (2, 3, 4):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight
                                          | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(r, col, item)

    def _fill_cases(self, ev: Evaluation) -> None:
        res = ev.result
        assert res is not None
        heads = ["V", "Re", "N_S", "f_s", "f_n", "H_c", "f_n,c", "N_Sc", "f_s / f_n,c",
                 "V_IR"]
        self.cases.setColumnCount(len(heads))
        self.cases.setHorizontalHeaderLabels(heads)
        self.cases.setRowCount(len(res.cases))
        self.cases.setVerticalHeaderLabels([scope_label(c.scope) for c in res.cases])
        for r, c in enumerate(res.cases):
            vals = [fmt_quantity(c.velocity, QuantityKind.VELOCITY), fmt(c.reynolds, 0),
                    fmt(c.strouhal, 3), fmt_quantity(c.fs, QuantityKind.FREQUENCY),
                    fmt_quantity(c.fn, QuantityKind.FREQUENCY), fmt(c.hc, 3),
                    fmt_quantity(c.fnc, QuantityKind.FREQUENCY), fmt(c.scruton, 2),
                    fmt(c.fs / c.fnc, 3) if c.fnc else "—",
                    fmt_quantity(c.v_ir, QuantityKind.VELOCITY) if c.v_ir else "—"]
            for col, text in enumerate(vals):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.cases.setItem(r, col, item)
        self.cases.resizeColumnsToContents()

    def _fill_trace(self, ev: Evaluation) -> None:
        res = ev.result
        assert res is not None
        rows = []
        for e in res.trace:
            desc = tr(e.description_key, STATE.language) if e.description_key else ""
            val = fmt_quantity(e.value, e.kind)
            scope = scope_label(e.scope) if e.scope else ""
            ref = short_reference(e.reference)
            rows.append(f"<tr><td>{scope}</td><td><b>{e.symbol}</b></td><td>{desc}</td>"
                        f"<td align='right'>{val}</td><td><i>{ref}</i></td></tr>")
        self.trace.setHtml("<table cellspacing='0' cellpadding='3' width='100%'>"
                           + "".join(rows) + "</table>")

    def set_alternatives(self, alts: list[Alternative]) -> None:
        """Lista de alternativas propuestas."""
        self._alternatives = alts
        self.alt_list.clear()
        if not alts:
            self.btn_apply.setEnabled(False)
            return
        for a in alts:
            changes = ", ".join(
                f"{k} = {fmt_quantity(v, QuantityKind.LENGTH) if isinstance(v, float) else v}"
                for k, v in a.changes.items())
            self.alt_list.addItem(f"{tr(a.reason_key, STATE.language)} — {changes}")

    def show_no_alternatives(self) -> None:
        """Indica que no se encontraron alternativas."""
        self.alt_list.clear()
        self.alt_list.addItem(t("res.no_alternatives"))
        self._alternatives = []

    def _apply(self) -> None:
        row = self.alt_list.currentRow()
        if 0 <= row < len(self._alternatives):
            self.apply_alternative.emit(self._alternatives[row])
