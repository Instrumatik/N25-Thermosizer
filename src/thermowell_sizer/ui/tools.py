"""Calculadoras y conversor de unidades como ventanas flotantes no modales."""

from __future__ import annotations

import math
from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from thermowell_sizer.core.tools import converter, heat, sensors
from thermowell_sizer.core.units import KELVIN_OFFSET, QuantityKind
from thermowell_sizer.data.database import Library
from thermowell_sizer.i18n import Language, parse_number
from thermowell_sizer.properties.fluids import FluidPropertyError, fluid_state
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.text import t
from thermowell_sizer.ui.widgets import QuantityEdit, fmt, fmt_quantity

CATEGORY_NAMES = {
    "temperature": ("Temperatura", "Temperature"), "pressure": ("Presión", "Pressure"),
    "length": ("Longitud", "Length"), "mass_flow": ("Caudal másico", "Mass flow"),
    "volume_flow": ("Caudal volumétrico", "Volume flow"), "density": ("Densidad", "Density"),
    "dynamic_viscosity": ("Viscosidad dinámica", "Dynamic viscosity"),
    "kinematic_viscosity": ("Viscosidad cinemática", "Kinematic viscosity"),
    "velocity": ("Velocidad", "Velocity"), "stress": ("Esfuerzo", "Stress"),
    "frequency": ("Frecuencia", "Frequency"),
}
YEAR_FACTOR = 1e-3
"""Las tasas de corrosión se ingresan en mm/año."""
TABLE_MAX_ROWS = 2000
MPY_TO_MM_YEAR = 0.0254


def _name(pair: tuple[str, str]) -> str:
    return pair[0] if STATE.language is Language.ES else pair[1]


def _window(title: str) -> QWidget:
    w = QWidget(None, Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
    w.setWindowTitle(title)
    w.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    return w


def _result_label() -> QLabel:
    lbl = QLabel()
    lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    lbl.setWordWrap(True)
    lbl.setStyleSheet("font-size: 13pt; font-weight: bold; padding: 6px;")
    return lbl


class ConverterWindow(QWidget):
    """Conversor de unidades: un valor expresado en todas las unidades de la categoría."""

    def __init__(self) -> None:
        super().__init__(None, Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowTitle(t("act.converter"))
        self.resize(460, 480)
        self.category = QComboBox()
        for key, pair in CATEGORY_NAMES.items():
            self.category.addItem(_name(pair), key)
        self.value = QLineEdit("1")
        self.unit = QComboBox()
        self.baro = QuantityEdit(QuantityKind.PRESSURE, minimum=1.0)
        self.baro.set_value(STATE.barometric)
        self.table = QTableWidget(0, 2)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        form = QFormLayout()
        form.addRow(t("act.converter"), self.category)
        row = QHBoxLayout()
        row.addWidget(self.value, 1)
        row.addWidget(self.unit, 1)
        form.addRow(t("f.value"), row)
        form.addRow(t("dlg.barometric"), self.baro)
        lay = QVBoxLayout(self)
        lay.addLayout(form)
        lay.addWidget(self.table, 1)
        self.category.currentIndexChanged.connect(self._fill_units)
        self.unit.currentIndexChanged.connect(self.update_table)
        self.value.textChanged.connect(self.update_table)
        self.baro.changed.connect(self.update_table)
        self._fill_units()

    def _fill_units(self) -> None:
        self.unit.blockSignals(True)
        self.unit.clear()
        for u in converter.CATEGORIES[self.category.currentData()]:
            self.unit.addItem(u.symbol)
        self.unit.blockSignals(False)
        self.update_table()

    def update_table(self) -> None:
        """Recalcula todas las conversiones."""
        try:
            value = parse_number(self.value.text(), STATE.language)
        except ValueError:
            self.table.setRowCount(0)
            return
        rows = converter.convert_all(value, self.category.currentData(),
                                     self.unit.currentText(), self.baro.value() or 101_325.0)
        self.table.setRowCount(len(rows))
        for r, (sym, v) in enumerate(rows):
            num = QTableWidgetItem(fmt(v))
            num.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(r, 0, num)
            self.table.setItem(r, 1, QTableWidgetItem(sym))
        self.table.resizeColumnsToContents()


class _Calc(QWidget):
    """Pestaña de calculadora: formulario, botón y resultado."""

    def __init__(self, compute: Callable[[], str] | None = None) -> None:
        super().__init__()
        self.form = QFormLayout()
        self.result = _result_label()
        btn = QPushButton(t("act.calculate"))
        btn.clicked.connect(self.run)
        lay = QVBoxLayout(self)
        lay.addLayout(self.form)
        lay.addWidget(btn, 0, Qt.AlignmentFlag.AlignLeft)
        lay.addWidget(self.result)
        lay.addStretch(1)
        self._compute = compute

    def q(self, label: str, kind: QuantityKind, value: float | None = None,
          **kw: object) -> QuantityEdit:
        """Agrega un campo con unidades."""
        qe = QuantityEdit(kind, **kw)  # type: ignore[arg-type]
        qe.set_value(value)
        qe.changed.connect(self.run)
        self.form.addRow(label, qe)
        return qe

    def num(self, label: str, value: float, decimals: int = 3, maximum: float = 1e9
            ) -> QDoubleSpinBox:
        """Agrega un campo numérico simple."""
        sb = QDoubleSpinBox()
        sb.setDecimals(decimals)
        sb.setRange(0.0, maximum)
        sb.setValue(value)
        sb.valueChanged.connect(self.run)
        self.form.addRow(label, sb)
        return sb

    def run(self) -> None:
        """Calcula y muestra el resultado (o el error)."""
        if self._compute is None:
            return
        try:
            self.result.setText(self._compute())
        except (ValueError, TypeError, ZeroDivisionError, FluidPropertyError) as exc:
            self.result.setText(f"⚠ {exc}")


def _require(*values: float | None) -> list[float]:
    if any(v is None for v in values):
        raise ValueError(t("status.invalid"))
    return [float(v) for v in values if v is not None]


class CalculatorsWindow(QWidget):
    """Conjunto de calculadoras de ingeniería en pestañas."""

    def __init__(self, library: Library) -> None:
        super().__init__(None, Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.library = library
        self.setWindowTitle(t("act.calculators"))
        self.resize(560, 560)
        self.tabs = QTabWidget()
        self.tabs.addTab(self._velocity(), t("calc.velocity"))
        self.tabs.addTab(self._gas(), t("calc.gas"))
        self.tabs.addTab(self._flange(), t("calc.flange"))
        self.tabs.addTab(self._immersion(), t("calc.immersion"))
        self.tabs.addTab(self._tau(), t("calc.tau"))
        self.tabs.addTab(self._corrosion(), t("calc.corrosion"))
        self.tabs.addTab(self._rtd(), "Pt100")
        self.tabs.addTab(self._tc(), t("calc.tc"))
        note = QLabel(t("calc.note"))
        note.setWordWrap(True)
        note.setObjectName("warningLabel")
        lay = QVBoxLayout(self)
        lay.addWidget(self.tabs, 1)
        lay.addWidget(note)

    def _fluid_combo(self, tab: _Calc) -> QComboBox:
        combo = QComboBox()
        for f in self.library.fluids():
            combo.addItem(f.name_es if STATE.language is Language.ES else f.name_en, f.id)
        combo.currentIndexChanged.connect(tab.run)
        tab.form.addRow(t("f.fluid"), combo)
        return combo

    # --- Velocidad y Reynolds -------------------------------------------------------
    def _velocity(self) -> QWidget:
        tab = _Calc()
        mode = QComboBox()
        mode.addItem(t("calc.from_mass"), "mass")
        mode.addItem(t("calc.from_volume"), "volume")
        mode.currentIndexChanged.connect(tab.run)
        tab.form.addRow(t("f.basis"), mode)
        m = tab.q(t("calc.mass_flow"), QuantityKind.MASS_FLOW, 10.0, minimum=0.0)
        qv = tab.q(t("calc.volume_flow"), QuantityKind.VOLUME_FLOW, 0.01, minimum=0.0)
        rho = tab.q(t("f.density"), QuantityKind.DENSITY, 1000.0, minimum=1e-6)
        mu = tab.q(t("f.viscosity"), QuantityKind.DYNAMIC_VISCOSITY, 1e-3, minimum=1e-9)
        d = tab.q(t("f.pipe_id"), QuantityKind.DIAMETER, 0.1023, minimum=1e-4)
        b = tab.q(t("calc.body_diameter"), QuantityKind.DIAMETER, 0.019, minimum=1e-4)

        def compute() -> str:
            rho_v, mu_v, d_v, b_v = _require(rho.value(), mu.value(), d.value(), b.value())
            if mode.currentData() == "mass":
                (m_v,) = _require(m.value())
                v = heat.velocity_from_mass_flow(m_v, rho_v, d_v)
            else:
                (q_v,) = _require(qv.value())
                v = heat.velocity_from_volume_flow(q_v, d_v)
            re_pipe = heat.reynolds(rho_v, v, d_v, mu_v)
            re_tw = heat.reynolds(rho_v, v, b_v, mu_v)
            return (f"V = {fmt_quantity(v, QuantityKind.VELOCITY)}\n"
                    f"Re ({t('calc.pipe')}) = {fmt(re_pipe, 0)}\n"
                    f"Re ({t('calc.thermowell')}) = {fmt(re_tw, 0)}")

        tab._compute = compute
        tab.run()
        return tab

    # --- Densidad de gas ------------------------------------------------------------
    def _gas(self) -> QWidget:
        tab = _Calc()
        fluid = self._fluid_combo(tab)
        fluid.setCurrentIndex(max(fluid.findData("natural_gas"), 0))
        temp = tab.q(t("lib.temperature"), QuantityKind.TEMPERATURE, 293.15)
        pres = tab.q(t("lib.pressure") + " (abs)", QuantityKind.PRESSURE, 50e5, minimum=1.0)

        def compute() -> str:
            t_v, p_v = _require(temp.value(), pres.value())
            st = fluid_state(self.library, fluid.currentData(), t_v, p_v)
            z = "—" if st.compressibility is None else fmt(st.compressibility, 4)
            sat = ("" if st.saturation_temperature is None else
                   f"\nT_sat = {fmt_quantity(st.saturation_temperature, QuantityKind.TEMPERATURE)}")
            return (f"ρ = {fmt_quantity(st.properties.density, QuantityKind.DENSITY)}\n"
                    f"μ = {fmt_quantity(st.properties.dynamic_viscosity,
                                        QuantityKind.DYNAMIC_VISCOSITY)}\n"
                    f"Z = {z} · {t('f.phase')}: {st.phase.value}{sat}\n"
                    f"{st.properties.source_note}")

        tab._compute = compute
        tab.run()
        return tab

    # --- Bridas P-T ------------------------------------------------------------------
    def _flange(self) -> QWidget:
        tab = _Calc()
        group = QComboBox()
        group.addItems(self.library.flange_groups())
        group.currentIndexChanged.connect(tab.run)
        cls = QComboBox()
        for c in (150, 300, 600, 900, 1500, 2500):
            cls.addItem(str(c), c)
        cls.setCurrentIndex(1)
        cls.currentIndexChanged.connect(tab.run)
        tab.form.addRow(t("lib.group"), group)
        tab.form.addRow(t("f.rating"), cls)
        temp = tab.q(t("lib.temperature"), QuantityKind.TEMPERATURE, 473.15)

        def compute() -> str:
            (t_v,) = _require(temp.value())
            p = self.library.flange_rating(group.currentText(), cls.currentData(), t_v)
            if p is None:
                return t("calc.out_of_table")
            return (f"P = {fmt_quantity(p + STATE.barometric, QuantityKind.PRESSURE, gauge=True)}"
                    f"\n{t('lib.unverified')}")

        tab._compute = compute
        tab.run()
        return tab

    # --- Error de inmersión ----------------------------------------------------------
    def _immersion(self) -> QWidget:
        tab = _Calc()
        tf = tab.q(t("calc.t_fluid"), QuantityKind.TEMPERATURE, 573.15)
        tb = tab.q(t("calc.t_base"), QuantityKind.TEMPERATURE, 293.15)
        h = tab.num(t("calc.h") + " (W/m²·K)", 500.0, 0, 1e6)
        k = tab.num(t("calc.k_wall") + " (W/m·K)", 16.2, 1, 500)
        length = tab.q(t("calc.exposed"), QuantityKind.LENGTH, 0.15, minimum=1e-4)
        dm = tab.q(t("calc.mean_d"), QuantityKind.DIAMETER, 0.022, minimum=1e-4)
        bore = tab.q(t("f.d"), QuantityKind.DIAMETER, 0.0066, minimum=1e-5)
        tol = tab.q(t("calc.tolerance"), QuantityKind.TEMPERATURE_DIFFERENCE, 0.1, minimum=0.0)

        def compute() -> str:
            vals = _require(tf.value(), tb.value(), length.value(), dm.value(), bore.value())
            res = heat.immersion_error(
                fluid_temperature=vals[0], base_temperature=vals[1], h=h.value(),
                length=vals[2], outer_diameter=vals[3], bore=vals[4],
                conductivity=k.value(), tolerance=tol.value())
            lmin = ("—" if res.min_length is None
                    else fmt_quantity(res.min_length, QuantityKind.LENGTH))
            return (f"ΔT = {fmt_quantity(abs(res.error), QuantityKind.TEMPERATURE_DIFFERENCE)}\n"
                    f"m = {fmt(res.m)} 1/m\n{t('calc.min_immersion')}: {lmin}")

        tab._compute = compute
        tab.run()
        return tab

    # --- Constante de tiempo ---------------------------------------------------------
    def _tau(self) -> QWidget:
        tab = _Calc()
        h = tab.num(t("calc.h") + " (W/m²·K)", 1000.0, 0, 1e6)
        b = tab.q(t("f.B"), QuantityKind.DIAMETER, 0.019, minimum=1e-4)
        bore = tab.q(t("f.d"), QuantityKind.DIAMETER, 0.0066, minimum=1e-5)
        ds = tab.q(t("f.sheath"), QuantityKind.DIAMETER, 0.006, minimum=1e-5)
        rho = tab.q(t("calc.wall_density"), QuantityKind.DENSITY, 8000.0, minimum=1.0)
        cp = tab.num(t("calc.wall_cp") + " (J/kg·K)", 500.0, 0, 5000)
        gap = QComboBox()
        for label, k in ((t("calc.gap_air"), 0.026), (t("calc.gap_oil"), 0.15),
                         (t("calc.gap_paste"), 0.8)):
            gap.addItem(label, k)
        gap.currentIndexChanged.connect(tab.run)
        tab.form.addRow(t("calc.gap"), gap)
        tau_s = tab.num(t("calc.sensor_tau") + " (s)", 2.0, 1, 600)

        def compute() -> str:
            b_v, d_v, s_v, r_v = _require(b.value(), bore.value(), ds.value(), rho.value())
            res = heat.time_constant(h=h.value(), outer_diameter=b_v, bore=d_v,
                                     wall_density=r_v, wall_specific_heat=cp.value(),
                                     sensor_diameter=min(s_v, d_v),
                                     gap_conductivity=gap.currentData(),
                                     sensor_tau=tau_s.value())
            return (f"τ ≈ {fmt(res.total, 1)} s · t90 ≈ {fmt(res.t90, 1)} s\n"
                    f"({t('calc.film')}: {fmt(res.film, 1)} s, {t('calc.gap')}: "
                    f"{fmt(res.gap, 1)} s, sensor: {fmt(res.sensor, 1)} s)")

        tab._compute = compute
        tab.run()
        return tab

    # --- Corrosión -------------------------------------------------------------------
    def _corrosion(self) -> QWidget:
        tab = _Calc()
        rate = tab.num(t("calc.rate") + " (mm/año)", 0.1, 3, 100)
        years = tab.num(t("calc.life") + " (años)", 20.0, 1, 200)
        actual = tab.q(t("calc.actual"), QuantityKind.LENGTH, 0.006, minimum=0.0)
        required = tab.q(t("calc.required"), QuantityKind.LENGTH, 0.003, minimum=0.0)

        def compute() -> str:
            a_v, r_v = _require(actual.value(), required.value())
            r = rate.value() * YEAR_FACTOR
            ca = heat.corrosion_allowance(r, years.value())
            life = heat.remaining_life(a_v, r_v, r)
            life_txt = "∞" if math.isinf(life) else fmt(life, 1)
            mpy = rate.value() / MPY_TO_MM_YEAR
            return (f"c = {fmt_quantity(ca, QuantityKind.LENGTH)}\n"
                    f"{t('calc.remaining')}: {life_txt} {t('calc.years')}\n"
                    f"({fmt(mpy, 2)} mpy)")

        tab._compute = compute
        tab.run()
        return tab

    # --- Pt100 -----------------------------------------------------------------------
    def _rtd(self) -> QWidget:
        tab = _Calc()
        r0 = QComboBox()
        for v in ("100", "500", "1000"):
            r0.addItem(f"Pt{v}", v)
        r0.currentIndexChanged.connect(tab.run)
        tab.form.addRow("R0", r0)
        cls = QComboBox()
        for c in sensors.RtdClass:
            cls.addItem(c.value, c)
        cls.setCurrentIndex(1)
        cls.currentIndexChanged.connect(tab.run)
        tab.form.addRow(t("calc.class"), cls)
        temp = tab.q(t("lib.temperature"), QuantityKind.TEMPERATURE, 373.15)
        res_in = QLineEdit()
        res_in.setPlaceholderText("Ω → T")
        res_in.editingFinished.connect(tab.run)
        tab.form.addRow(t("calc.resistance") + " (Ω)", res_in)
        table = QTableWidget(0, 3)
        table.setHorizontalHeaderLabels(["T (°C)", "R (Ω)", "± (°C)"])
        table.verticalHeader().setVisible(False)

        def compute() -> str:
            ohm0 = float(r0.currentData())
            lines = []
            if temp.value() is not None:
                tc = float(temp.value() or 0.0) - KELVIN_OFFSET
                lines.append(f"R({fmt(tc, 2)} °C) = {fmt(sensors.rtd_resistance(tc, ohm0), 4)} Ω"
                             f" · ± {fmt(sensors.rtd_tolerance(tc, cls.currentData()), 3)} °C")
            if res_in.text().strip():
                r = parse_number(res_in.text(), STATE.language)
                lines.append(f"T({fmt(r, 3)} Ω) = {fmt(sensors.rtd_temperature(r, ohm0), 3)} °C")
            rows = sensors.table("rtd", str(ohm0), -200, 850, 50)
            table.setRowCount(len(rows))
            for i, (tt, rr) in enumerate(rows):
                for c, txt in enumerate((fmt(tt, 0), fmt(rr, 3),
                                         fmt(sensors.rtd_tolerance(tt, cls.currentData()), 2))):
                    table.setItem(i, c, QTableWidgetItem(txt))
            return "\n".join(lines)

        tab.layout().addWidget(table)  # type: ignore[union-attr]
        tab._compute = compute
        tab.run()
        return tab

    # --- Termopares -----------------------------------------------------------------
    def _tc(self) -> QWidget:
        tab = _Calc()
        typ = QComboBox()
        for k in sensors.TC_TYPES:
            typ.addItem(k, k)
        typ.setCurrentIndex(typ.findData("K"))
        typ.currentIndexChanged.connect(tab.run)
        tab.form.addRow(t("f.sensor_type"), typ)
        temp = tab.q(t("lib.temperature"), QuantityKind.TEMPERATURE, 773.15)
        cj = tab.q(t("calc.cold_junction"), QuantityKind.TEMPERATURE, 273.15)
        emf_in = QLineEdit()
        emf_in.setPlaceholderText("mV → T")
        emf_in.editingFinished.connect(tab.run)
        tab.form.addRow(t("calc.emf") + " (mV)", emf_in)
        step = tab.num(t("calc.step") + " (°C)", 50.0, 0, 500)
        table = QTableWidget(0, 2)
        table.setHorizontalHeaderLabels(["T (°C)", "E (mV)"])
        table.verticalHeader().setVisible(False)

        def compute() -> str:
            kind = typ.currentData()
            cj_c = (cj.value() or KELVIN_OFFSET) - KELVIN_OFFSET
            lines = []
            if temp.value() is not None:
                tc = float(temp.value() or 0.0) - KELVIN_OFFSET
                e = sensors.tc_emf(kind, tc) - sensors.tc_emf(kind, cj_c)
                lines.append(f"E({fmt(tc, 1)} °C) = {fmt(e, 4)} mV "
                             f"({t('calc.cold_junction')} {fmt(cj_c, 1)} °C)")
            if emf_in.text().strip():
                mv = parse_number(emf_in.text(), STATE.language)
                lines.append(f"T({fmt(mv, 4)} mV) = "
                             f"{fmt(sensors.tc_temperature(kind, mv, cj_c), 2)} °C")
            lo, hi = sensors.tc_range(kind)
            st = max(step.value(), 1.0)
            start = math.ceil(lo / st) * st
            rows = sensors.table("tc", kind, start, hi - (hi - start) % st, st)[:TABLE_MAX_ROWS]
            table.setRowCount(len(rows))
            for i, (tt, ee) in enumerate(rows):
                table.setItem(i, 0, QTableWidgetItem(fmt(tt, 0)))
                table.setItem(i, 1, QTableWidgetItem(fmt(ee, 3)))
            lines.append(f"{t('calc.range')}: {fmt(lo, 0)} … {fmt(hi, 0)} °C · NIST ITS-90")
            return "\n".join(lines)

        tab.layout().addWidget(table)  # type: ignore[union-attr]
        tab._compute = compute
        tab.run()
        return tab


def open_tool(name: str, library: Library) -> QWidget:
    """Abre una herramienta como ventana independiente."""
    win: QWidget = ConverterWindow() if name == "converter" else CalculatorsWindow(library)
    win.show()
    return win
