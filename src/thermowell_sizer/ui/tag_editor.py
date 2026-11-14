"""Editor de un tag: asistente de cinco pasos o modo experto con todo a la vista."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from thermowell_sizer.autodesign import VESSEL_SIZE_NPS
from thermowell_sizer.core.designs import (
    CONNECTION_SIZES,
    DesignChoice,
    suggested_connection_size,
)
from thermowell_sizer.core.models import (
    CalcInput,
    ConnectionType,
    FlangeFace,
    FlowBasis,
    MountingOrientation,
    Phase,
    ProcessConnection,
    PropertySource,
    SensorType,
    ShankProfile,
    ThreadType,
)
from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.core.validation import Severity, validate_geometry
from thermowell_sizer.data.database import Library
from thermowell_sizer.data.fluid_groups import FLUID_TYPES, TYPES_BY_ID, fluid_label, type_for
from thermowell_sizer.i18n import tr
from thermowell_sizer.ui.design_ui import DesignContext, DesignDialog
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.text import enum_text, t
from thermowell_sizer.ui.widgets import EnumCombo, QuantityEdit, fmt, fmt_quantity

RATING_CLASSES = (150, 300, 600, 900, 1500, 2500)
CASE_LABELS = ("min", "normal", "max")
BASIS_KIND = {
    FlowBasis.VELOCITY: QuantityKind.VELOCITY,
    FlowBasis.MASS_FLOW: QuantityKind.MASS_FLOW,
    FlowBasis.VOLUME_FLOW: QuantityKind.VOLUME_FLOW,
    FlowBasis.STANDARD_VOLUME_FLOW: QuantityKind.STANDARD_VOLUME_FLOW,
}
STEP_KEYS = ("step.identification", "step.process", "step.pipe", "step.thermowell",
             "step.sensor")
MAX_FLOW_CASES = 6
CUSTOM_PIPE = "Otro / Other"
VESSEL_PIPE = "Recipiente / Vessel"
VESSEL_NPS = "Recipiente"
"""NPS guardado para un montaje en recipiente."""


class FlowCaseRow(QWidget):
    """Una fila de caso de flujo: etiqueta, dato y valor."""

    changed = Signal()
    remove = Signal(object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.label = QComboBox()
        self.label.setEditable(True)
        for key in CASE_LABELS:
            self.label.addItem(enum_text(key), key)
        self.basis = EnumCombo(list(FlowBasis))
        self.values = {b: QuantityEdit(k, minimum=0.0) for b, k in BASIS_KIND.items()}
        self.stack = QStackedWidget()
        for b in FlowBasis:
            self.stack.addWidget(self.values[b])
            self.values[b].changed.connect(self.changed)
        self.btn_remove = QPushButton("✕")
        self.btn_remove.setFixedWidth(28)
        self.btn_remove.setToolTip(t("f.remove_case"))
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.label, 1)
        lay.addWidget(self.basis, 1)
        lay.addWidget(self.stack, 2)
        lay.addWidget(self.btn_remove)
        self.basis.currentIndexChanged.connect(self._basis_changed)
        self.label.currentTextChanged.connect(lambda _: self.changed.emit())
        self.btn_remove.clicked.connect(lambda: self.remove.emit(self))
        self._basis_changed()

    def _basis_changed(self) -> None:
        self.stack.setCurrentWidget(self.values[FlowBasis(self.basis.value())])
        self.changed.emit()

    def label_value(self) -> str:
        """Etiqueta interna del caso (min, normal, max o texto libre)."""
        text = self.label.currentText().strip()
        for i in range(self.label.count()):
            if self.label.itemText(i) == text:
                return str(self.label.itemData(i))
        return text or "normal"

    def to_dict(self) -> dict[str, Any]:
        """Datos del caso para el modelo."""
        basis = FlowBasis(self.basis.value())
        return {"label": self.label_value(), "basis": basis.value,
                basis.value: self.values[basis].value()}

    def load(self, data: dict[str, Any]) -> None:
        """Carga un caso."""
        label = data["label"]
        idx = self.label.findData(label)
        self.label.blockSignals(True)
        if idx >= 0:
            self.label.setCurrentIndex(idx)
        else:
            self.label.setEditText(label)
        self.label.blockSignals(False)
        basis = FlowBasis(data["basis"])
        self.basis.set_value(basis)
        self.stack.setCurrentWidget(self.values[basis])
        for b in FlowBasis:
            self.values[b].set_value(data.get(b.value))

    def refresh_units(self) -> None:
        """Propaga el cambio de unidades."""
        for v in self.values.values():
            v.refresh_units()


def _top(widget: QWidget) -> QWidget:
    """Envuelve una sección para que quede arriba sin estirarse en alto."""
    page = QWidget()
    lay = QVBoxLayout(page)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.addWidget(widget)
    lay.addStretch(1)
    return page


def _form(group: QGroupBox) -> QFormLayout:
    form = QFormLayout(group)
    form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
    form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
    return form


class TagEditor(QWidget):
    """Formulario completo del tag.

    Emite :attr:`changed` ante cualquier edición, :attr:`calculate_requested` al pedir
    el cálculo, y mantiene la lista de errores de validación en tiempo real.
    """

    changed = Signal()
    calculate_requested = Signal()

    def __init__(self, library: Library, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.library = library
        self._loading = False
        self._base: CalcInput | None = None
        self.quantities: dict[str, QuantityEdit] = {}
        self.flow_rows: list[FlowCaseRow] = []
        self.mode_combos: dict[str, QComboBox] = {}
        self.pages = [self._page_identification(), self._page_process(), self._page_pipe(),
                      self._page_thermowell(), self._page_sensor()]

        self.steps = QListWidget()
        self.steps.setMaximumWidth(150)
        for key in STEP_KEYS:
            self.steps.addItem(t(key))
        self.stack = QStackedWidget()
        self.expert_container = QWidget()
        self.expert_layout = QVBoxLayout(self.expert_container)
        self.expert_scroll = QScrollArea()
        self.expert_scroll.setWidgetResizable(True)
        self.expert_scroll.setWidget(self.expert_container)
        self.wizard_scroll = QScrollArea()
        self.wizard_scroll.setWidgetResizable(True)
        self.wizard_scroll.setWidget(self.stack)

        self.btn_back = QPushButton(t("wiz.back"))
        self.btn_next = QPushButton(t("wiz.next"))
        self.btn_calc = QPushButton(t("wiz.calculate"))
        self.btn_calc.setDefault(True)
        self.error_label = QLabel()
        self.error_label.setWordWrap(True)
        self.error_label.setObjectName("errorLabel")
        nav = QHBoxLayout()
        nav.addWidget(self.btn_back)
        nav.addWidget(self.btn_next)
        nav.addStretch(1)
        nav.addWidget(self.btn_calc)

        body = QHBoxLayout()
        body.addWidget(self.steps)
        self.mode_stack = QStackedWidget()
        self.mode_stack.addWidget(self.wizard_scroll)
        self.mode_stack.addWidget(self.expert_scroll)
        body.addWidget(self.mode_stack, 1)
        root = QVBoxLayout(self)
        root.addLayout(body, 1)
        root.addWidget(self.error_label)
        root.addLayout(nav)

        self.steps.currentRowChanged.connect(self._goto)
        self.btn_back.clicked.connect(lambda: self.step(-1))
        self.btn_next.clicked.connect(lambda: self.step(1))
        self.btn_calc.clicked.connect(self.calculate_requested)
        self.expert = False
        self._compact_combos()
        self._place_pages()
        self.steps.setCurrentRow(0)

    # --- Construcción de páginas -------------------------------------------------------
    def _q(self, name: str, kind: QuantityKind, **kw: Any) -> QuantityEdit:
        q = QuantityEdit(kind, **kw)
        q.changed.connect(self._emit)
        q.setObjectName(name)
        self.quantities[name] = q
        return q

    def _compact_combos(self) -> None:
        """Evita que un texto largo en un combo ensanche todo el formulario."""
        for combo in self.findChildren(QComboBox):
            combo.setSizeAdjustPolicy(
                QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
            combo.setMinimumContentsLength(10)

    def _line(self) -> QLineEdit:
        e = QLineEdit()
        e.editingFinished.connect(self._emit)
        return e

    def _page_identification(self) -> QWidget:
        box = QGroupBox(t("step.identification"))
        f = _form(box)
        self.e_tag = self._line()
        self.e_service = self._line()
        self.e_line = self._line()
        self.e_pid = self._line()
        self.e_location = self._line()
        f.addRow(t("f.tag") + " *", self.e_tag)
        f.addRow(t("f.service"), self.e_service)
        f.addRow(t("f.line"), self.e_line)
        f.addRow(t("f.pid"), self.e_pid)
        f.addRow(t("f.location"), self.e_location)
        return _top(box)

    def _page_process(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        box = QGroupBox(t("step.process"))
        f = _form(box)
        f.addRow(t("f.mode_process"), self._mode_combo("process", t("mode.auto_process")))
        es = STATE.language.value == "es"
        self._fluid_names = {fl.id: fl.name_es if es else fl.name_en
                             for fl in self.library.fluids()}
        self.c_ftype = QComboBox()
        for ft in FLUID_TYPES:
            self.c_ftype.addItem(ft.name[0] if es else ft.name[1], ft.id)
        self.c_ftype.currentIndexChanged.connect(self._ftype_changed)
        self.c_fluid = QComboBox()
        self.c_fluid.currentIndexChanged.connect(self._emit)
        self.c_phase = EnumCombo(list(Phase))
        self.c_phase.setEnabled(False)
        self._fill_fluids("")
        f.addRow(t("f.fluid_type"), self.c_ftype)
        f.addRow(t("f.fluid"), self.c_fluid)
        f.addRow(t("f.phase_calc"), self.c_phase)
        f.addRow(t("f.p_op"), self._q("p_op", QuantityKind.PRESSURE, gauge_capable=True))
        f.addRow(t("f.p_design"), self._q("p_design", QuantityKind.PRESSURE,
                                           gauge_capable=True))
        f.addRow(t("f.t_op"), self._q("t_op", QuantityKind.TEMPERATURE))
        f.addRow(t("f.t_design"), self._q("t_design", QuantityKind.TEMPERATURE))
        self.chk_auto = QCheckBox(t("f.auto_props"))
        self.chk_auto.setChecked(True)
        self.chk_auto.toggled.connect(self._auto_toggled)
        self.chk_auto.hide()  # el modo del bloque se elige con el selector de arriba
        self.mode_combos["process"].setCurrentIndex(1)
        f.addRow(t("f.density"), self._q("density", QuantityKind.DENSITY, minimum=1e-9))
        f.addRow(t("f.viscosity"), self._q("viscosity", QuantityKind.DYNAMIC_VISCOSITY,
                                            minimum=1e-12))
        f.addRow(t("f.std_density"), self._q("std_density", QuantityKind.DENSITY,
                                              minimum=1e-9, optional=True))
        self.lbl_source = QLabel()
        self.lbl_source.setWordWrap(True)
        f.addRow(t("f.prop_source"), self.lbl_source)
        lay.addWidget(box)

        cases = QGroupBox(t("f.flow_cases"))
        self.cases_layout = QVBoxLayout(cases)
        head = QHBoxLayout()
        for key in ("f.case", "f.basis", "f.value"):
            head.addWidget(QLabel(f"<b>{t(key)}</b>"), 2 if key == "f.value" else 1)
        head.addSpacing(28)
        self.cases_layout.addLayout(head)
        self.btn_add_case = QPushButton(t("f.add_case"))
        self.btn_add_case.clicked.connect(lambda: self._add_case(emit=True))
        self.cases_layout.addWidget(self.btn_add_case, 0, Qt.AlignmentFlag.AlignLeft)
        lay.addWidget(cases)

        corr = QGroupBox(t("f.corrosion"))
        g = QGridLayout(corr)
        self.chk_nace = QCheckBox(t("f.nace"))
        self.chk_erosive = QCheckBox(t("f.erosive"))
        for chk in (self.chk_nace, self.chk_erosive):
            chk.toggled.connect(self._emit)
        g.addWidget(QLabel(t("f.h2s")), 0, 0)
        g.addWidget(self._q("h2s", QuantityKind.PRESSURE, minimum=0.0, optional=True), 0, 1)
        g.addWidget(QLabel(t("f.chlorides")), 1, 0)
        self.e_chlorides = self._line()
        g.addWidget(self.e_chlorides, 1, 1)
        g.addWidget(QLabel(t("f.ph")), 2, 0)
        self.e_ph = self._line()
        g.addWidget(self.e_ph, 2, 1)
        g.addWidget(self.chk_nace, 3, 0, 1, 2)
        g.addWidget(self.chk_erosive, 4, 0, 1, 2)
        lay.addWidget(corr)
        lay.addStretch(1)
        return page

    def _page_pipe(self) -> QWidget:
        box = QGroupBox(t("step.pipe"))
        f = _form(box)
        f.addRow(t("f.mode_pipe"), self._mode_combo("pipe", t("mode.auto_pipe")))
        self.mode_combos["pipe"].setCurrentIndex(1)
        self.c_nps = QComboBox()
        self.c_nps.addItems([*self.library.pipe_sizes(), VESSEL_PIPE, CUSTOM_PIPE])
        self.c_sch = QComboBox()
        self.c_nps.currentIndexChanged.connect(self._nps_changed)
        self.c_sch.currentIndexChanged.connect(self._pipe_changed)
        f.addRow(t("f.nps"), self.c_nps)
        f.addRow(t("f.schedule"), self.c_sch)
        f.addRow(t("f.pipe_od"), self._q("pipe_od", QuantityKind.DIAMETER, minimum=1e-4,
                                          optional=True))
        f.addRow(t("f.wall"), self._q("wall", QuantityKind.LENGTH, minimum=0.0, optional=True))
        f.addRow(t("f.pipe_id"), self._q("pipe_id", QuantityKind.DIAMETER, minimum=1e-4))
        self.l_vessel = QLabel(t("f.vessel_hint"))
        self.l_vessel.setWordWrap(True)
        self.l_vessel.setObjectName("hintLabel")
        f.addRow("", self.l_vessel)
        f.addRow(t("f.liquid_depth"), self._q("liquid_depth", QuantityKind.LENGTH,
                                               minimum=1e-3, optional=True))
        self.quantities["pipe_od"].changed.connect(self._custom_pipe_changed)
        self.quantities["wall"].changed.connect(self._custom_pipe_changed)
        self.c_orient = EnumCombo(list(MountingOrientation))
        self.c_orient.currentIndexChanged.connect(self._orientation_changed)
        f.addRow(t("f.orientation"), self.c_orient)
        self.s_angle = QDoubleSpinBox()
        self.s_angle.setRange(5.0, 90.0)
        self.s_angle.setDecimals(0)
        self.s_angle.setSingleStep(5.0)
        self.s_angle.setSuffix(" °")
        self.s_angle.setValue(45.0)
        self.s_angle.valueChanged.connect(self._emit)
        f.addRow(t("f.mount_angle"), self.s_angle)
        f.addRow(t("f.insulation"), self._q("insulation", QuantityKind.LENGTH, minimum=0.0))
        f.addRow(t("f.mount"), self._q("mount", QuantityKind.LENGTH, minimum=0.0))
        self.l_mount = QLabel()
        self.l_mount.setWordWrap(True)
        self.l_mount.setObjectName("hintLabel")
        f.addRow("", self.l_mount)
        f.addRow(t("f.nozzle_id"), self._q("nozzle_id", QuantityKind.DIAMETER, minimum=1e-4,
                                            optional=True))
        return _top(box)

    def _mode_combo(self, block: str, auto_text: str | None = None) -> QComboBox:
        combo = QComboBox()
        combo.setObjectName("modeCombo")
        combo.addItem(t("mode.manual"), False)
        combo.addItem(auto_text or t("mode.auto"), True)
        combo.setStyleSheet("QComboBox#modeCombo { font-weight: bold; }")
        combo.currentIndexChanged.connect(lambda: self._mode_changed(block))
        self.mode_combos[block] = combo
        return combo

    def _mode_changed(self, block: str) -> None:
        auto = bool(self.mode_combos[block].currentData())
        if block == "process":
            if self.chk_auto.isChecked() != auto:
                self.chk_auto.setChecked(auto)
            return
        if block == "pipe":
            if not hasattr(self, "c_nps"):  # aún construyendo la página
                return
            custom = self.c_nps.currentText() in (CUSTOM_PIPE, VESSEL_PIPE)
            if auto and custom:
                self.c_nps.setCurrentIndex(max(self.c_nps.findText("6"), 0))
            elif not auto and not custom:
                self.c_nps.setCurrentIndex(self.c_nps.findText(CUSTOM_PIPE))
            return
        self._emit()

    def _page_thermowell(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        hint = QLabel(t("mode.auto_hint"))
        hint.setWordWrap(True)
        hint.setObjectName("hintLabel")
        lay.addWidget(hint)
        conn_box = QGroupBox(t("blk.connection"))
        fc = _form(conn_box)
        fc.addRow(t("f.mode_connection"), self._mode_combo("connection"))
        mat_box = QGroupBox(t("blk.material"))
        fm = _form(mat_box)
        fm.addRow(t("f.mode_material"), self._mode_combo("material"))
        left = QGroupBox(t("blk.geometry"))
        f = _form(left)
        f.addRow(t("f.mode_geometry"), self._mode_combo("geometry"))
        self.c_profile = EnumCombo(list(ShankProfile))
        self.c_profile.currentIndexChanged.connect(self._profile_changed)
        self.c_conn = EnumCombo(list(ConnectionType))
        self.c_conn.currentIndexChanged.connect(self._conn_changed)
        self.e_conn_size = QComboBox()
        self.e_conn_size.setEditable(True)
        self.e_conn_size.currentTextChanged.connect(self._emit)
        self.c_rating = QComboBox()
        for r in RATING_CLASSES:
            self.c_rating.addItem(str(r), r)
        self.c_rating.currentIndexChanged.connect(self._emit)
        self.c_face = EnumCombo(list(FlangeFace))
        self.c_face.currentIndexChanged.connect(self._emit)
        self.c_thread = EnumCombo(list(ThreadType))
        self.c_thread.currentIndexChanged.connect(self._thread_changed)
        self.c_material = QComboBox()
        for m in self.library.materials():
            self.c_material.addItem(f"{m.name} ({m.spec})", m.id)
        self.c_material.currentIndexChanged.connect(self._emit)
        self.c_coating = QComboBox()
        self.c_coating.addItem(t("f.none"), "")
        for c in self.library.coatings():
            self.c_coating.addItem(c[1] if STATE.language.value == "es" else c[2], c[0])
        self.c_coating.currentIndexChanged.connect(self._emit)
        fc.addRow(t("f.connection"), self.c_conn)
        fc.addRow(t("f.conn_size"), self.e_conn_size)
        self.l_size_hint = QLabel()
        self.l_size_hint.setObjectName("hintLabel")
        fc.addRow("", self.l_size_hint)
        fc.addRow(t("f.thread"), self.c_thread)
        fc.addRow(t("f.rating"), self.c_rating)
        fc.addRow(t("f.face"), self.c_face)
        self.l_conn_code = QLabel()
        self.l_conn_code.setObjectName("hintLabel")
        fc.addRow("", self.l_conn_code)
        fm.addRow(t("f.material"), self.c_material)
        fm.addRow(t("f.coating"), self.c_coating)
        fm.addRow(t("f.E_manual"), self._q("mat_E", QuantityKind.ELASTIC_MODULUS, minimum=1e9,
                                            optional=True))
        fm.addRow(t("f.S_manual"), self._q("mat_S", QuantityKind.STRESS, minimum=1e5,
                                            optional=True))
        fm.addRow(t("f.ca"), self._q("g_ca", QuantityKind.LENGTH, minimum=0.0))
        self.l_mat_lib = QLabel()
        self.l_mat_lib.setObjectName("hintLabel")
        self.l_mat_lib.setWordWrap(True)
        fm.addRow("", self.l_mat_lib)
        f.addRow(t("f.profile"), self.c_profile)
        g = f
        self.geometry_rows: dict[str, QLabel] = {}
        for key, kind in (("L", QuantityKind.LENGTH), ("U", QuantityKind.LENGTH),
                          ("A", QuantityKind.DIAMETER), ("B", QuantityKind.DIAMETER),
                          ("d", QuantityKind.DIAMETER), ("t", QuantityKind.LENGTH),
                          ("b", QuantityKind.LENGTH), ("Ls", QuantityKind.LENGTH),
                          ("bs", QuantityKind.LENGTH), ("T_lag", QuantityKind.LENGTH),
                          ("L0", QuantityKind.LENGTH)):
            label = QLabel(t(f"f.{key}"))
            self.geometry_rows[key] = label
            optional = key in ("U",)
            g.addRow(label, self._q(f"g_{key}", kind, minimum=0.0, optional=optional))
        self.l_u_breakdown = QLabel()
        self.l_u_breakdown.setWordWrap(True)
        self.l_u_breakdown.setObjectName("hintLabel")
        g.addRow("", self.l_u_breakdown)
        self.btn_design = QPushButton(t("des.button"))
        self.btn_design.clicked.connect(self.open_design_dialog)
        f.insertRow(1, "", self.btn_design)
        lay.addWidget(conn_box)
        lay.addWidget(mat_box)
        lay.addWidget(left)
        lay.addStretch(1)
        return page

    def _page_sensor(self) -> QWidget:
        box = QGroupBox(t("step.sensor"))
        f = _form(box)
        f.addRow(t("f.mode_sensor"), self._mode_combo("sensor"))
        self.c_sensor = EnumCombo(list(SensorType))
        self.c_sensor.currentIndexChanged.connect(self._emit)
        f.addRow(t("f.sensor_type"), self.c_sensor)
        f.addRow(t("f.sheath"), self._q("sheath", QuantityKind.DIAMETER, minimum=1e-4))
        self.chk_spring = QCheckBox(t("f.spring"))
        self.chk_spring.toggled.connect(self._emit)
        f.addRow(self.chk_spring)
        f.addRow(t("f.sensor_mass"), self._q("sensor_mass", QuantityKind.MASS, minimum=0.0,
                                              optional=True))
        return _top(box)

    # --- Modo asistente / experto ----------------------------------------------------
    def set_expert(self, expert: bool) -> None:
        """Muestra todas las secciones a la vez (experto) o paso a paso (asistente)."""
        self.expert = expert
        self._place_pages()

    def _place_pages(self) -> None:
        for page in self.pages:
            page.setParent(None)
        if self.expert:
            for page in self.pages:
                self.expert_layout.addWidget(page)
            self.mode_stack.setCurrentWidget(self.expert_scroll)
        else:
            for page in self.pages:
                self.stack.addWidget(page)
            self.mode_stack.setCurrentWidget(self.wizard_scroll)
            self.stack.setCurrentIndex(max(self.steps.currentRow(), 0))
        self.steps.setVisible(not self.expert)
        self.btn_back.setVisible(not self.expert)
        self.btn_next.setVisible(not self.expert)

    def step(self, delta: int) -> None:
        """Avanza o retrocede un paso del asistente."""
        row = min(max(self.steps.currentRow() + delta, 0), len(self.pages) - 1)
        self.steps.setCurrentRow(row)

    def _goto(self, row: int) -> None:
        if not self.expert and row >= 0:
            self.stack.setCurrentIndex(row)
        self.btn_back.setEnabled(row > 0)
        self.btn_next.setEnabled(row < len(self.pages) - 1)

    # --- Reacciones internas ----------------------------------------------------------
    def _emit(self) -> None:
        if not self._loading:
            self._update_enabled()
            self.changed.emit()

    def _fill_fluids(self, current: str) -> None:
        """Lista solo los fluidos del tipo elegido (con su sufijo de estado)."""
        ftype = TYPES_BY_ID[str(self.c_ftype.currentData() or "liquid")]
        es = STATE.language.value == "es"
        self.c_fluid.blockSignals(True)
        self.c_fluid.clear()
        for fid, suffix in ftype.fluids:
            if fid in self._fluid_names:
                self.c_fluid.addItem(fluid_label(fid, self._fluid_names[fid], suffix, es), fid)
        self.c_fluid.setCurrentIndex(max(self.c_fluid.findData(current), 0))
        self.c_fluid.blockSignals(False)
        self.c_phase.set_value(ftype.phase)

    def _ftype_changed(self) -> None:
        self._fill_fluids(str(self.c_fluid.currentData() or ""))
        self._emit()

    def _auto_toggled(self) -> None:
        self._update_enabled()
        self._emit()

    def _profile_changed(self) -> None:
        if ShankProfile(self.c_profile.value()) is ShankProfile.STRAIGHT:
            a = self.quantities["g_A"].value()
            self.quantities["g_B"].set_value(a)
        self._emit()

    def _conn_changed(self) -> None:
        if not self._loading:
            conn = ConnectionType(self.c_conn.value())
            self._fill_sizes(conn, self._suggested_size(conn) or "")
        self._emit()

    def _update_conn_code(self) -> None:
        """Código de hoja de datos de la conexión elegida (H, S, R o G)."""
        conn = ConnectionType(self.c_conn.value())
        code = ProcessConnection(
            type=conn, rating_class=300,
            thread=ThreadType(self.c_thread.value()) if conn is ConnectionType.THREADED
            else None).datasheet_code
        self.l_conn_code.setText(t("f.conn_code", code=code) if code else "")

    def _thread_changed(self) -> None:
        """Cambia la designación del tamaño (NPT ↔ G) conservando la medida."""
        if not self._loading and ConnectionType(self.c_conn.value()) is ConnectionType.THREADED:
            size = self.e_conn_size.currentText().strip()
            if ThreadType(self.c_thread.value()) is ThreadType.G:
                size = "G " + size.replace(" NPT", "").replace("G ", "")
            else:
                size = size.replace("G ", "").replace(" NPT", "") + " NPT"
            self._fill_sizes(ConnectionType.THREADED, size.strip())
        self._emit()

    def _orientation_changed(self) -> None:
        """«En recipiente» en la orientación equivale a elegir «Recipiente» en el NPS."""
        vessel = MountingOrientation(self.c_orient.value()) is MountingOrientation.VESSEL
        if not self._loading and vessel != (self.c_nps.currentText() == VESSEL_PIPE):
            if vessel:
                self.c_nps.setCurrentIndex(self.c_nps.findText(VESSEL_PIPE))
            else:
                self.c_nps.setCurrentIndex(max(self.c_nps.findText("6"), 0))
        self._emit()

    def _set_vessel(self, vessel: bool) -> None:
        """Al pasar a recipiente: orientación «En recipiente» y un caso con velocidad 0."""
        orient = MountingOrientation(self.c_orient.value())
        if vessel and orient is not MountingOrientation.VESSEL:
            self.c_orient.set_value(MountingOrientation.VESSEL)
            for row in list(self.flow_rows):
                row.setParent(None)
            self.flow_rows.clear()
            self._add_case(emit=False).load({"label": "normal",
                                             "basis": FlowBasis.VELOCITY.value,
                                             "velocity": 0.0})
            if not self.quantities["pipe_id"].value():
                self.quantities["pipe_id"].set_value(2.0)
        elif not vessel and orient is MountingOrientation.VESSEL:
            self.c_orient.set_value(MountingOrientation.PERPENDICULAR)

    def _suggested_size(self, conn: ConnectionType) -> str | None:
        nps = self.c_nps.currentText()
        if nps == CUSTOM_PIPE:
            return None
        if nps == VESSEL_PIPE:
            nps = VESSEL_SIZE_NPS
        return suggested_connection_size(conn, nps, STATE.data_folder)

    def _fill_sizes(self, conn: ConnectionType, current: str) -> None:
        """Opciones de tamaño para el tipo de conexión, con ``current`` seleccionado."""
        combo = self.e_conn_size
        combo.blockSignals(True)
        combo.clear()
        suggested = self._suggested_size(conn)
        sizes = list(CONNECTION_SIZES[conn])
        if conn is ConnectionType.THREADED and ThreadType(self.c_thread.value()) is ThreadType.G:
            sizes = ["G " + x.replace(" NPT", "") for x in sizes]
        combo.addItems(sizes)
        idx = combo.findText(current)
        if idx < 0 and current:
            combo.addItem(current)
            idx = combo.count() - 1
        combo.setCurrentIndex(max(idx, 0))
        combo.blockSignals(False)
        self.l_size_hint.setText(t("f.suggested", size=suggested) if suggested else "")

    def _nps_changed(self) -> None:
        nps = self.c_nps.currentText()
        self.c_sch.blockSignals(True)
        self.c_sch.clear()
        if not self._loading:
            self._set_vessel(nps == VESSEL_PIPE)
        if nps not in (CUSTOM_PIPE, VESSEL_PIPE):
            self.c_sch.addItems(self.library.schedules(nps))
            idx = self.c_sch.findText("40")
            if idx < 0:
                idx = self.c_sch.findText("STD")
            self.c_sch.setCurrentIndex(max(idx, 0))
        self.c_sch.blockSignals(False)
        self._pipe_changed()

    def _pipe_changed(self) -> None:
        nps = self.c_nps.currentText()
        pipe_mode = self.mode_combos.get("pipe")
        if pipe_mode is not None:
            pipe_mode.blockSignals(True)
            pipe_mode.setCurrentIndex(0 if nps in (CUSTOM_PIPE, VESSEL_PIPE) else 1)
            pipe_mode.blockSignals(False)
        if nps not in (CUSTOM_PIPE, VESSEL_PIPE) and self.c_sch.currentText():
            pipe = self.library.pipe(nps, self.c_sch.currentText())
            self.quantities["pipe_id"].set_value(pipe.inner_diameter)
            self.quantities["pipe_od"].set_value(pipe.outer_diameter)
            self.quantities["wall"].set_value(pipe.wall_thickness)
        if hasattr(self, "l_size_hint"):
            suggested = self._suggested_size(ConnectionType(self.c_conn.value()))
            self.l_size_hint.setText(t("f.suggested", size=suggested) if suggested else "")
        self._emit()

    def _custom_pipe_changed(self) -> None:
        """Con «Otro», el diámetro interno sale del exterior y el espesor."""
        od, wall = self.quantities["pipe_od"].value(), self.quantities["wall"].value()
        if self.c_nps.currentText() == CUSTOM_PIPE and od and wall is not None and od > 2 * wall:
            self.quantities["pipe_id"].set_value(od - 2 * wall)

    def nozzle_to_inner_wall(self) -> float:
        """Distancia de la cara de la brida de montaje a la pared interna, m."""
        return (self.quantities["mount"].value() or 0.0) + (self.quantities["wall"].value()
                                                             or 0.0)

    def _update_mount_label(self) -> None:
        q = self.quantities
        hs, wall = q["mount"].value() or 0.0, q["wall"].value() or 0.0
        text = t("f.mount_sum", hs=fmt_quantity(hs, QuantityKind.LENGTH),
                 wall=fmt_quantity(wall, QuantityKind.LENGTH),
                 total=fmt_quantity(hs + wall, QuantityKind.LENGTH))
        u = q["g_U"].value() or q["g_L"].value()
        if u:
            imm = u - hs - wall
            text += "\n" + t("f.u_breakdown", hs=fmt_quantity(hs, QuantityKind.LENGTH),
                               wall=fmt_quantity(wall, QuantityKind.LENGTH),
                               imm=fmt_quantity(imm, QuantityKind.LENGTH),
                               u=fmt_quantity(u, QuantityKind.LENGTH))
        self.l_mount.setText(text)
        if hasattr(self, "l_u_breakdown"):
            self.l_u_breakdown.setText(text.split("\n")[-1] if u else "")

    def _update_enabled(self) -> None:
        for widgets in self._block_widgets().values():
            for w in widgets:
                w.setEnabled(True)
        auto = self.chk_auto.isChecked()
        self.quantities["density"].setEnabled(not auto)
        self.quantities["viscosity"].setEnabled(not auto)
        self.quantities["std_density"].setEnabled(not auto)
        profile = ShankProfile(self.c_profile.value())
        stepped = profile is ShankProfile.STEPPED
        for key in ("Ls", "bs"):
            self.quantities[f"g_{key}"].setEnabled(stepped)
            self.geometry_rows[key].setEnabled(stepped)
        self.quantities["g_B"].setEnabled(profile is not ShankProfile.STRAIGHT)
        flanged = ConnectionType(self.c_conn.value()) in (ConnectionType.FLANGED,
                                                           ConnectionType.VAN_STONE)
        self.c_rating.setEnabled(flanged)
        self.c_face.setEnabled(flanged)
        self.c_thread.setEnabled(ConnectionType(self.c_conn.value()) is ConnectionType.THREADED)
        self._update_conn_code()
        self._apply_modes()
        vessel = self.c_nps.currentText() == VESSEL_PIPE
        custom = self.c_nps.currentText() == CUSTOM_PIPE or vessel
        for block, auto in (("pipe", not custom), ("process", self.chk_auto.isChecked())):
            combo = self.mode_combos.get(block)
            if combo is not None and bool(combo.currentData()) != auto:
                combo.blockSignals(True)
                combo.setCurrentIndex(1 if auto else 0)
                combo.blockSignals(False)
        for key in ("pipe_id", "wall"):
            self.quantities[key].setEnabled(custom)
        self.quantities["pipe_od"].setEnabled(custom and not vessel)
        self.quantities["liquid_depth"].setEnabled(vessel)
        self.l_vessel.setVisible(vessel)
        orient = MountingOrientation(self.c_orient.value())
        self.s_angle.setEnabled(orient is MountingOrientation.ANGLED)
        self._update_mount_label()
        self.c_sch.setEnabled(not custom)
        self.btn_add_case.setEnabled(len(self.flow_rows) < MAX_FLOW_CASES)
        for row in self.flow_rows:
            row.btn_remove.setEnabled(len(self.flow_rows) > 1)

    def auto_blocks(self) -> tuple[str, ...]:
        """Bloques en «Automático», en el orden del motor."""
        return tuple(b for b in ("material", "connection", "geometry", "sensor")
                     if b in self.mode_combos and self.mode_combos[b].currentData())

    def _block_widgets(self) -> dict[str, list[QWidget]]:
        q = self.quantities
        return {
            "material": [self.c_material, self.c_coating, q["mat_E"], q["mat_S"], q["g_ca"]],
            "connection": [self.c_conn, self.e_conn_size, self.c_thread, self.c_rating,
                           self.c_face],
            "geometry": [self.c_profile, self.btn_design,
                         *(q[f"g_{k}"] for k in ("L", "U", "A", "B", "d", "t", "b", "Ls", "bs",
                                                 "T_lag", "L0"))],
            "sensor": [q["sheath"], self.chk_spring],
        }

    def _apply_modes(self) -> None:
        """Deshabilita los campos de los bloques automáticos (los completa el cálculo)."""
        auto = set(self.auto_blocks())
        for block, widgets in self._block_widgets().items():
            if block in auto:
                for w in widgets:
                    w.setEnabled(False)

    def show_auto(self, inp: CalcInput) -> None:
        """Muestra los valores que completó la selección automática."""
        self.load(inp, auto_properties=self.chk_auto.isChecked(),
                  auto_blocks=self.auto_blocks())

    def _add_case(self, *, emit: bool) -> FlowCaseRow:
        row = FlowCaseRow()
        row.changed.connect(self._emit)
        row.remove.connect(self._remove_case)
        self.flow_rows.append(row)
        self.cases_layout.insertWidget(self.cases_layout.count() - 1, row)
        if emit:
            self._emit()
        return row

    def _remove_case(self, row: FlowCaseRow) -> None:
        if len(self.flow_rows) <= 1:
            return
        self.flow_rows.remove(row)
        row.setParent(None)
        row.deleteLater()
        self._emit()

    # --- Diseños típicos -----------------------------------------------------------------
    def design_context(self) -> DesignContext:
        """Datos actuales del formulario que condicionan el diseño típico."""
        nps = self.c_nps.currentText()
        orient = MountingOrientation(self.c_orient.value())
        return DesignContext(
            pipe_id=self.quantities["pipe_id"].value(),
            nozzle_length=self.nozzle_to_inner_wall(),
            nps="" if nps == CUSTOM_PIPE else (VESSEL_SIZE_NPS if nps == VESSEL_PIPE else nps),
            rating_class=self.c_rating.currentData(),
            elbow=orient in (MountingOrientation.ELBOW_TIP_UPSTREAM,
                             MountingOrientation.ELBOW_TIP_DOWNSTREAM),
            connection=ConnectionType(self.c_conn.value()))

    def open_design_dialog(self) -> None:
        """Abre el diálogo de diseños típicos y aplica la elección."""
        dlg = DesignDialog(self.design_context(), self)
        if dlg.exec() and dlg.choice is not None:
            self.apply_design(dlg.choice)

    def apply_design(self, c: DesignChoice) -> None:
        """Carga en el formulario la geometría y la conexión de un diseño típico."""
        self._loading = True
        q = self.quantities
        self.c_profile.set_value(c.profile)
        self.c_conn.set_value(c.connection)
        self._fill_sizes(c.connection, c.size)
        if c.rating_class is not None:
            self.c_rating.setCurrentIndex(max(self.c_rating.findData(c.rating_class), 0))
        if c.L0 > 0 and not q["mount"].value():
            q["mount"].set_value(max(c.L0 - (q["wall"].value() or 0.0), 0.0))
        for key, value in (("L", c.L), ("U", c.U), ("A", c.A), ("B", c.B), ("d", c.d),
                           ("t", c.t), ("Ls", c.Ls), ("L0", c.L0)):
            q[f"g_{key}"].set_value(value)
        self._loading = False
        self._emit()
        self.validate()

    # --- Carga y lectura del modelo ---------------------------------------------------
    def load(self, inp: CalcInput, *, auto_properties: bool = True,
             auto_blocks: tuple[str, ...] = ()) -> None:
        """Muestra los datos de ``inp`` en el formulario."""
        self._loading = True
        for block in ("material", "connection", "geometry", "sensor"):
            if block in self.mode_combos:
                self.mode_combos[block].setCurrentIndex(1 if block in auto_blocks else 0)
        self._base = inp
        q = self.quantities
        idn, proc, pipe = inp.identification, inp.process, inp.pipe
        tw, sensor = inp.thermowell, inp.sensor
        g = tw.geometry
        self.e_tag.setText(idn.tag)
        self.e_service.setText(idn.service)
        self.e_line.setText(idn.line_or_equipment)
        self.e_pid.setText(idn.pid)
        self.e_location.setText(idn.location)
        self.c_ftype.blockSignals(True)
        self.c_ftype.setCurrentIndex(max(self.c_ftype.findData(type_for(proc.fluid_id,
                                                                         proc.phase)), 0))
        self.c_ftype.blockSignals(False)
        self._fill_fluids(proc.fluid_id)
        q["p_op"].set_value(proc.operating_pressure)
        q["p_design"].set_value(proc.design_pressure)
        q["t_op"].set_value(proc.operating_temperature)
        q["t_design"].set_value(proc.design_temperature)
        self.chk_auto.setChecked(auto_properties)
        self.mode_combos["process"].setCurrentIndex(1 if auto_properties else 0)
        self.show_properties(inp)
        for row in list(self.flow_rows):
            row.setParent(None)
        self.flow_rows.clear()
        for case in proc.flow_cases:
            self._add_case(emit=False).load(case.model_dump())
        corr = proc.corrosion
        q["h2s"].set_value(corr.h2s_partial_pressure or None)
        self.e_chlorides.setText(fmt(corr.chlorides_ppm, 0) if corr.chlorides_ppm else "")
        self.e_ph.setText(fmt(corr.ph, 1) if corr.ph is not None else "")
        self.chk_nace.setChecked(corr.nace_service)
        self.chk_erosive.setChecked(corr.solids_or_erosive)
        nps_idx = (self.c_nps.findText(VESSEL_PIPE) if pipe.is_vessel
                   else self.c_nps.findText(pipe.nominal_size))
        self.c_nps.blockSignals(True)
        self.c_nps.setCurrentIndex(nps_idx if nps_idx >= 0 else self.c_nps.findText(CUSTOM_PIPE))
        self.c_nps.blockSignals(False)
        self.c_sch.blockSignals(True)
        self.c_sch.clear()
        if self.c_nps.currentText() not in (CUSTOM_PIPE, VESSEL_PIPE):
            self.c_sch.addItems(self.library.schedules(pipe.nominal_size))
            self.c_sch.setCurrentIndex(max(self.c_sch.findText(pipe.schedule), 0))
        self.c_sch.blockSignals(False)
        q["pipe_id"].set_value(pipe.inner_diameter)
        wall = pipe.wall_thickness
        if wall is None and pipe.nominal_size and pipe.schedule:
            try:
                wall = self.library.pipe(pipe.nominal_size, pipe.schedule).wall_thickness
            except KeyError:
                wall = None
        q["wall"].set_value(wall)
        q["pipe_od"].set_value(pipe.inner_diameter + 2 * wall if wall is not None else None)
        self.c_orient.set_value(pipe.orientation)
        self.s_angle.blockSignals(True)
        self.s_angle.setValue(pipe.mount_angle or 45.0)
        self.s_angle.blockSignals(False)
        q["liquid_depth"].set_value(pipe.liquid_depth)
        q["insulation"].set_value(pipe.insulation_thickness)
        q["mount"].set_value(pipe.mount_height if pipe.mount_height is not None
                             else max(pipe.nozzle_length - (wall or 0.0), 0.0))
        q["nozzle_id"].set_value(pipe.nozzle_inner_diameter)
        self.c_profile.set_value(g.profile)
        self.c_conn.set_value(tw.connection.type)
        self.c_thread.set_value(tw.connection.thread or ThreadType.NPT)
        self._fill_sizes(tw.connection.type, tw.connection.size)
        if tw.connection.rating_class:
            self.c_rating.setCurrentIndex(max(self.c_rating.findData(tw.connection.rating_class),
                                              0))
        if tw.connection.face:
            self.c_face.set_value(tw.connection.face)
        self.c_material.setCurrentIndex(max(self.c_material.findData(tw.material.material_id),
                                            0))
        self.c_coating.setCurrentIndex(max(self.c_coating.findData(tw.material.coating), 0))
        q["mat_E"].set_value(tw.material.elastic_modulus)
        q["mat_S"].set_value(tw.material.allowable_stress)
        for key in ("L", "U", "A", "B", "d", "t", "b", "Ls", "bs", "T_lag", "L0"):
            q[f"g_{key}"].set_value(getattr(g, key))
        q["g_ca"].set_value(g.corrosion_allowance)
        self.c_sensor.set_value(sensor.type)
        q["sheath"].set_value(sensor.sheath_diameter)
        self.chk_spring.setChecked(sensor.spring_loaded)
        q["sensor_mass"].set_value(sensor.mass)
        self._loading = False
        self._update_enabled()
        self.validate()

    def show_material_hint(self, inp: CalcInput) -> None:
        """Muestra E y S de biblioteca para comparar con los cargados a mano."""
        proc = inp.process
        try:
            mat = self.library.material_properties(inp.thermowell.material.material_id,
                                                   proc.operating_temperature,
                                                   proc.design_temperature)
        except KeyError:
            self.l_mat_lib.setText("")
            return
        self.l_mat_lib.setText(t("f.mat_lib",
                                 E=fmt_quantity(mat.elastic_modulus,
                                                QuantityKind.ELASTIC_MODULUS),
                                 S=fmt_quantity(mat.allowable_stress, QuantityKind.STRESS)))

    def show_properties(self, inp: CalcInput) -> None:
        """Muestra ρ, μ y su fuente (tras recalcular con CoolProp)."""
        props = inp.process.properties
        self.quantities["density"].set_value(props.density)
        self.quantities["viscosity"].set_value(props.dynamic_viscosity)
        self.quantities["std_density"].set_value(props.standard_density)
        source = {PropertySource.COOLPROP: "CoolProp", PropertySource.LIBRARY: "Biblioteca",
                  PropertySource.USER: "Usuario"}[props.source]
        self.lbl_source.setText(props.source_note or source)
        if self.chk_auto.isChecked():
            self.c_phase.set_value(inp.process.phase)
        else:
            self.c_phase.set_value(TYPES_BY_ID[str(self.c_ftype.currentData())].phase)

    def _number(self, edit: QLineEdit) -> float | None:
        text = edit.text().strip()
        if not text:
            return None
        from thermowell_sizer.i18n import parse_number

        return parse_number(text, STATE.language)

    def _standard_density(self) -> float | None:
        """ρ estándar: de la biblioteca si las propiedades son automáticas."""
        value = self.quantities["std_density"].value()
        if self.chk_auto.isChecked() or value is None:
            from thermowell_sizer.properties.fluids import standard_density

            fluid = self.c_fluid.currentData()
            auto = standard_density(self.library, fluid) if fluid else None
            return auto if auto is not None else value
        return value

    def raw(self) -> dict[str, Any]:
        """Datos del formulario como diccionario compatible con :class:`CalcInput`."""
        q = self.quantities
        base = self._base
        conn = ConnectionType(self.c_conn.value())
        flanged = conn in (ConnectionType.FLANGED, ConnectionType.VAN_STONE)
        profile = ShankProfile(self.c_profile.value())
        a = q["g_A"].value()
        props: dict[str, Any] = {
            "density": q["density"].value(), "dynamic_viscosity": q["viscosity"].value(),
            "standard_density": self._standard_density(),
            "source": (base.process.properties.source.value if base and self.chk_auto.isChecked()
                       else PropertySource.USER.value),
            "source_note": base.process.properties.source_note if base else "",
        }
        nps = self.c_nps.currentText()
        return {
            "identification": {"tag": self.e_tag.text().strip(),
                               "service": self.e_service.text(),
                               "line_or_equipment": self.e_line.text(),
                               "pid": self.e_pid.text(), "location": self.e_location.text()},
            "process": {
                "fluid_id": self.c_fluid.currentData(),
                "phase": TYPES_BY_ID[str(self.c_ftype.currentData())].phase.value,
                "operating_pressure": q["p_op"].value(),
                "design_pressure": q["p_design"].value(),
                "operating_temperature": q["t_op"].value(),
                "design_temperature": q["t_design"].value(),
                "flow_cases": [r.to_dict() for r in self.flow_rows],
                "properties": props,
                "corrosion": {
                    "h2s_partial_pressure": q["h2s"].value() or 0.0,
                    "chlorides_ppm": self._number(self.e_chlorides) or 0.0,
                    "ph": self._number(self.e_ph),
                    "solids_or_erosive": self.chk_erosive.isChecked(),
                    "nace_service": self.chk_nace.isChecked(),
                },
            },
            "pipe": {
                "nominal_size": ("" if nps == CUSTOM_PIPE else
                                 VESSEL_NPS if nps == VESSEL_PIPE else nps),
                "schedule": "" if nps in (CUSTOM_PIPE, VESSEL_PIPE) else self.c_sch.currentText(),
                "inner_diameter": q["pipe_id"].value(),
                "orientation": self.c_orient.value().value,
                "mount_angle": (self.s_angle.value() if MountingOrientation(self.c_orient.value())
                                is MountingOrientation.ANGLED else None),
                "liquid_depth": q["liquid_depth"].value() if nps == VESSEL_PIPE else None,
                "insulation_thickness": q["insulation"].value() or 0.0,
                "wall_thickness": q["wall"].value(),
                "mount_height": q["mount"].value() or 0.0,
                "nozzle_inner_diameter": q["nozzle_id"].value(),
            },
            "thermowell": {
                "geometry": {
                    "profile": profile.value,
                    "L": q["g_L"].value(), "U": q["g_U"].value(), "A": a,
                    "B": a if profile is ShankProfile.STRAIGHT else q["g_B"].value(),
                    "d": q["g_d"].value(), "t": q["g_t"].value(),
                    "b": q["g_b"].value() or 0.0,
                    "Ls": (q["g_Ls"].value() or 0.0) if profile is ShankProfile.STEPPED else 0.0,
                    "bs": (q["g_bs"].value() or 0.0) if profile is ShankProfile.STEPPED else 0.0,
                    "T_lag": q["g_T_lag"].value() or 0.0, "L0": q["g_L0"].value() or 0.0,
                    "corrosion_allowance": q["g_ca"].value() or 0.0,
                },
                "material": {"material_id": self.c_material.currentData(),
                             "coating": self.c_coating.currentData(),
                             "elastic_modulus": q["mat_E"].value(),
                             "allowable_stress": q["mat_S"].value()},
                "connection": {
                    "type": conn.value, "size": self.e_conn_size.currentText().strip(),
                    "rating_class": self.c_rating.currentData() if flanged else None,
                    "face": self.c_face.value().value if flanged else None,
                    "thread": (self.c_thread.value().value if conn is ConnectionType.THREADED
                               else None),
                },
            },
            "sensor": {
                "type": self.c_sensor.value().value,
                "sheath_diameter": q["sheath"].value(),
                "mass": q["sensor_mass"].value(),
                "spring_loaded": self.chk_spring.isChecked(),
            },
        }

    def to_input(self) -> CalcInput | None:
        """Construye la entrada; si es inválida devuelve ``None`` y muestra los errores."""
        try:
            raw = self.raw()
        except ValueError as exc:
            self._show_errors([str(exc)])
            return None
        try:
            inp = CalcInput.model_validate(raw)
        except ValidationError as exc:
            messages = []
            for err in exc.errors():
                loc = ".".join(str(x) for x in err["loc"])
                messages.append(f"{loc}: {err['msg']}")
            self._show_errors(messages)
            return None
        return inp

    def validate(self) -> CalcInput | None:
        """Validación en tiempo real: marca campos y lista los problemas."""
        for qe in self.quantities.values():
            qe.set_error(None)
        inp = self.to_input()
        if inp is None:
            return None
        msgs: list[str] = []
        for issue in validate_geometry(inp.thermowell.geometry):
            params = {k: fmt(v) if isinstance(v, float) else v for k, v in issue.params.items()}
            text = tr(issue.message_key, STATE.language, **params)
            field = self.quantities.get(f"g_{issue.field}")
            if field is not None:
                field.set_error(text)
            icon = "⛔" if issue.severity is Severity.ERROR else "⚠"
            msgs.append(f"{icon} {issue.field}: {text} ({issue.reference})")
        self._show_errors(msgs, ok=True)
        return inp

    def _show_errors(self, messages: list[str], *, ok: bool = False) -> None:
        self.error_label.setProperty("ok", ok and not messages)
        self.error_label.setText("\n".join(messages[:6]))
        self.error_label.setVisible(bool(messages))

    def current_step(self) -> int:
        """Paso visible del asistente."""
        return self.steps.currentRow()

    def refresh_units(self) -> None:
        """Propaga un cambio de unidades a todos los campos."""
        for qe in self.quantities.values():
            qe.refresh_units()
        for row in self.flow_rows:
            row.refresh_units()
