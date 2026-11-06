"""Panel de resultados: semáforo global, criterios con margen, resumen, traza y gráficas."""

from __future__ import annotations

import html

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

from thermowell_sizer.core.advisories import AdvisoryLevel
from thermowell_sizer.core.analysis.optimize import Alternative
from thermowell_sizer.core.models import CheckResult, CheckStatus
from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.i18n import tr
from thermowell_sizer.reports.common import CRITERION_NAMES, SCOPE_NAMES
from thermowell_sizer.services import Evaluation, render_advisory
from thermowell_sizer.summary import (
    asme_status,
    auto_note,
    auto_rows,
    calculated_results,
    label,
    length_convention,
    limit_text,
    value_text,
)
from thermowell_sizer.ui.infocard_ui import show_card
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
    "inline_lockin_dwell": (QuantityKind.DIMENSIONLESS, False),
    "fatigue_data": (QuantityKind.STRESS, False),
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
    names = SCOPE_NAMES
    idx = 0 if STATE.language.value == "es" else 1
    text = names.get(base, (base, base))[idx]
    if variant:
        text += " · " + names.get(variant, (variant, variant))[idx]
    return text


def _q(value: float, kind: QuantityKind) -> str:
    return fmt_quantity(value, kind, gauge=kind is QuantityKind.PRESSURE and STATE.gauge)


def _n(value: float, decimals: int) -> str:
    return fmt(value, decimals)


def overview_html(ev: Evaluation) -> str:
    """HTML de la pestaña «Resumen ASME»."""
    es = STATE.language.value == "es"
    out = [f"<h3>{t('res.asme_status')}</h3><table cellspacing='0' cellpadding='4'>"]
    for line in asme_status(ev):
        color = STATUS_COLORS[line.status]
        extra = f" (V/Ve = {fmt(line.ratio, 2)})" if line.ratio is not None else ""
        bold = ("<b>", "</b>") if line.key == "topic.overall" else ("", "")
        out.append(f"<tr><td>{bold[0]}{label(line.key, es)}{bold[1]}</td>"
                   f"<td><span style='color:{color}'>●</span> {bold[0]}"
                   f"{label(line.verdict, es)}{bold[1]}{extra}</td></tr>")
    out.append("</table>")
    autos = auto_rows(ev, es, _q)
    if autos:
        out.append(f"<h3>{t('res.auto_title')}</h3>"
                   "<table cellspacing='0' cellpadding='3' border='1' "
                   "style='border-collapse:collapse'><tr>"
                   f"<th width='20%'>{t('res.auto_field')}</th>"
                   f"<th width='22%'>{t('res.auto_value')}</th>"
                   f"<th width='58%'>{t('res.auto_reason')}</th></tr>")
        last = ""
        for ar in autos:
            if ar.block != last:
                out.append(f"<tr><td colspan='3'><b>{html.escape(ar.block)}</b></td></tr>")
                last = ar.block
            alt = (f"<br/><i>{t('res.auto_alt')}: {html.escape(ar.alternatives)}</i>"
                   if ar.alternatives else "")
            out.append(f"<tr><td>{html.escape(ar.item)}</td><td><b>{html.escape(ar.value)}</b>"
                       f"</td><td>{html.escape(ar.reason)}{alt}</td></tr>")
        out.append(f"</table><p><small>{html.escape(auto_note(es))}</small></p>")
    cases = calculated_results(ev)
    if cases:
        out.append(f"<h3>{t('res.calculated')}</h3>"
                   "<table cellspacing='0' cellpadding='3' border='1' "
                   "style='border-collapse:collapse'><tr><th></th><th></th>")
        for c in cases:
            out.append(f"<th>{html.escape(scope_label(c.scope))}</th>"
                       f"<th>{t('res.limit')}</th>")
        out.append("</tr>")
        for i, row in enumerate(cases[0].rows):
            out.append(f"<tr><td>{label(row.key, es)}</td>"
                       f"<td><i>{row.symbol}</i></td>")
            for c in cases:
                r = c.rows[i]
                rc = STATUS_COLORS[r.status] if r.status is not None else None
                dot = f"<span style='color:{rc}'>● </span>" if rc else ""
                out.append(f"<td align='right'>{dot}{value_text(r.key, r.value, r.kind, _q, _n)}"
                           f"</td><td align='right'>{html.escape(limit_text(r, _q, _n))}</td>")
            out.append("</tr>")
        out.append("</table>")
    out.append(f"<h3>{t('res.convention')}</h3>"
               "<table cellspacing='0' cellpadding='3'>")
    for key, value in length_convention(ev):
        out.append(f"<tr><td>{label(key, es)}</td><td align='right'>"
                   f"{fmt_quantity(value, QuantityKind.LENGTH)}</td></tr>")
    out.append(f"</table><p><small>{t('res.convention_note')}</small></p>")
    return "".join(out)


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
        self.cases.horizontalHeader().sectionClicked.connect(self._case_header_clicked)
        self.table.cellDoubleClicked.connect(self._check_clicked)
        self._check_ids: list[str] = []
        self.notes = QTextBrowser()
        self.advice = QTextBrowser()
        self.trace = QTextBrowser()
        self.overview = QTextBrowser()
        self.alt_list = QListWidget()
        self.btn_alt = QPushButton(t("act.optimize"))
        self.btn_apply = QPushButton(t("res.apply"))
        self.btn_apply.setEnabled(False)
        self.btn_alt.clicked.connect(self.optimize_requested)
        self.btn_apply.clicked.connect(self._apply)
        self.alt_list.currentRowChanged.connect(lambda r: self.btn_apply.setEnabled(r >= 0))
        alt = QWidget()
        self.alt_page = alt
        alt_l = QVBoxLayout(alt)
        alt_l.addWidget(self.alt_list)
        row = QHBoxLayout()
        row.addWidget(self.btn_alt)
        row.addWidget(self.btn_apply)
        row.addStretch(1)
        alt_l.addLayout(row)
        self._alternatives: list[Alternative] = []

        self.tabs = QTabWidget()
        self.tabs.addTab(self.overview, t("res.overview"))
        self.tabs.addTab(self.table, t("panel.results"))
        self.tabs.addTab(self.cases, t("res.summary"))
        self.tabs.addTab(self.advice, t("res.advice"))
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
        self.advice.clear()
        self.trace.clear()
        self.overview.clear()
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
        th = ev.thermal
        if th is not None:
            parts.append(t("res.thermal", tau=fmt(th.tau, 0), t90=fmt(th.t90, 0),
                           err=(f"{fmt(0.0, 2)} K" if abs(th.immersion_error) < 0.01 else
                                fmt_quantity(abs(th.immersion_error),
                                             QuantityKind.TEMPERATURE_DIFFERENCE))))
        self.lbl_summary.setText(" · ".join(parts))
        self._fill_checks(res.checks)
        self._fill_cases(ev)
        notes = [tr(n, STATE.language) for n in res.notes]
        notes += [t(w) for w in ev.warnings]
        if th is not None:
            notes.append(t("res.thermal_note", h=fmt(th.h, 0),
                           lmin=fmt_quantity(th.min_immersion or 0.0, QuantityKind.LENGTH))
                         + (" " + t("res.thermal_generic") if th.generic_fluid_data else ""))
        notes += [f"{i.field}: {tr(i.message_key, STATE.language)}" for i in res.issues]
        self.notes.setPlainText("\n\n".join(notes) if notes else "—")
        self._fill_advice(ev)
        self._fill_trace(ev)
        self._fill_overview(ev)

    def _fill_advice(self, ev: Evaluation) -> None:
        """Advertencias y recomendaciones complementarias, con su fuente."""
        icons = {AdvisoryLevel.CRITICAL: ("⛔", STATUS_COLORS[CheckStatus.FAIL]),
                 AdvisoryLevel.WARNING: ("⚠", STATUS_COLORS[CheckStatus.WARNING]),
                 AdvisoryLevel.INFO: ("ℹ", "#1f6fb2")}

        def qfmt(value: float, kind: QuantityKind) -> str:
            return fmt_quantity(value, kind,
                                gauge=kind is QuantityKind.PRESSURE and STATE.gauge)

        items = []
        for adv in ev.advisories:
            icon, color = icons[adv.level]
            text = html.escape(render_advisory(adv, STATE.language, qfmt, fmt))
            items.append(f"<p><span style='color:{color}'><b>{icon} "
                         f"{t('adv.level.' + adv.level.value)}</b></span> {text}"
                         f"<br/><small><i>{html.escape(adv.reference)}</i></small></p>")
        self.advice.setHtml("".join(items) or "—")
        worst = sum(1 for a in ev.advisories if a.level is not AdvisoryLevel.INFO)
        idx = self.tabs.indexOf(self.advice)
        self.tabs.setTabText(idx, t("res.advice") + (f" ({worst})" if worst else ""))

    def _fill_overview(self, ev: Evaluation) -> None:
        """Estado ASME por tema, resultados calculados por caso y convención de largos."""
        self.overview.setHtml(overview_html(ev))

    def _fill_checks(self, checks: list[CheckResult]) -> None:
        heads = [t("res.criterion"), t("res.case"), t("res.value"), t("res.limit"),
                 t("res.margin"), t("res.ref")]
        self.table.setHorizontalHeaderLabels(heads)
        order = {CheckStatus.FAIL: 0, CheckStatus.WARNING: 1, CheckStatus.PASS: 2,
                 CheckStatus.NOT_APPLICABLE: 3}
        rows = sorted(checks, key=lambda c: (order[c.status], c.margin_pct))
        self._check_ids = [c.criterion_id for c in rows]
        self.table.setRowCount(len(rows))
        for r, c in enumerate(rows):
            name = QTableWidgetItem(f"● {criterion_name(c.criterion_id)}")
            name.setForeground(QBrush(QColor(STATUS_COLORS[c.status])))
            name.setToolTip(tr(c.message_key, STATE.language) + "\n\n" + t("res.card_hint"))
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

    def _check_clicked(self, row: int, _col: int) -> None:
        if 0 <= row < len(self._check_ids):
            show_card(self._check_ids[row], self)

    def _case_header_clicked(self, col: int) -> None:
        item = self.cases.horizontalHeaderItem(col)
        if item is not None:
            show_card(item.text(), self)

    def _fill_cases(self, ev: Evaluation) -> None:
        res = ev.result
        assert res is not None
        heads = ["V", "Re", "N_S", "f_s", "f_n", "H_c", "f_n,c", "N_Sc", "f_s / f_n,c",
                 "V_IR"]
        self.cases.setColumnCount(len(heads))
        self.cases.setHorizontalHeaderLabels(heads)
        self.cases.horizontalHeader().setToolTip(t("res.card_hint"))
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
