"""Diálogo para cargar un diseño típico o un modelo de especificación de cliente."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from thermowell_sizer.core.designs import (
    BORE_260,
    BORE_385,
    DESIGN_NAMES,
    PROFILE_DIR,
    STANDARD_U,
    TYPICAL_DESIGNS,
    ClientProfile,
    DesignChoice,
    build_choice,
    load_profile,
    load_profiles,
    profile_choice,
    recommended_u,
    select_model,
)
from thermowell_sizer.core.models import ConnectionType, ShankProfile
from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.text import enum_text, t
from thermowell_sizer.ui.widgets import fmt_quantity


@dataclass(frozen=True)
class DesignContext:
    """Datos del tag que condicionan la elección."""

    pipe_id: float | None
    nozzle_length: float
    nps: str
    rating_class: int | None
    elbow: bool
    connection: ConnectionType


def profile_folder() -> Path | None:
    """Carpeta de perfiles del usuario (se crea si no existe)."""
    if STATE.data_folder is None:
        return None
    folder = STATE.data_folder / PROFILE_DIR
    folder.mkdir(parents=True, exist_ok=True)
    return folder


class DesignDialog(QDialog):
    """Elige ejecución, tamaño, agujero y U (catálogo) o un modelo de un perfil."""

    def __init__(self, ctx: DesignContext, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(t("des.title"))
        self.ctx = ctx
        self.choice: DesignChoice | None = None
        self.profiles: list[ClientProfile] = load_profiles(profile_folder())

        self.c_source = QComboBox()
        self.c_design = QComboBox()
        self.c_size = QComboBox()
        self.c_bore = QComboBox()
        self.c_u = QComboBox()
        self.c_model = QComboBox()
        self.info = QLabel()
        self.info.setWordWrap(True)
        self.summary = QLabel()
        self.summary.setWordWrap(True)
        note = QLabel(t("des.disclaimer"))
        note.setWordWrap(True)
        note.setObjectName("hintLabel")

        form = QFormLayout()
        form.addRow(t("des.source"), self.c_source)
        self.l_model = QLabel(t("des.model"))
        form.addRow(self.l_model, self.c_model)
        self.l_design = QLabel(t("des.design"))
        form.addRow(self.l_design, self.c_design)
        form.addRow(t("des.size"), self.c_size)
        self.l_bore = QLabel(t("des.bore"))
        form.addRow(self.l_bore, self.c_bore)
        self.l_u = QLabel(t("des.u"))
        form.addRow(self.l_u, self.c_u)

        btn_import = QPushButton(t("des.import"))
        btn_import.clicked.connect(self._import)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
        self.btn_apply = buttons.addButton(t("des.apply"),
                                           QDialogButtonBox.ButtonRole.AcceptRole)
        buttons.addButton(btn_import, QDialogButtonBox.ButtonRole.ActionRole)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        lay = QVBoxLayout(self)
        lay.addLayout(form)
        lay.addWidget(self.info)
        lay.addWidget(self.summary)
        lay.addWidget(note)
        lay.addWidget(buttons)
        self.setMinimumWidth(520)

        self._fill_sources()
        self.c_source.currentIndexChanged.connect(self._source_changed)
        self.c_design.currentIndexChanged.connect(self._design_changed)
        self.c_model.currentIndexChanged.connect(self._update)
        for combo in (self.c_size, self.c_bore, self.c_u):
            combo.currentIndexChanged.connect(self._update)
        self._source_changed()

    # --- Llenado de combos ------------------------------------------------------------
    def _fill_sources(self) -> None:
        self.c_source.blockSignals(True)
        self.c_source.clear()
        self.c_source.addItem(t("des.generic"), "")
        for p in self.profiles:
            self.c_source.addItem(p.name, p.id)
        self.c_source.blockSignals(False)

    def _profile(self) -> ClientProfile | None:
        pid = self.c_source.currentData()
        return next((p for p in self.profiles if p.id == pid), None)

    def _source_changed(self) -> None:
        profile = self._profile()
        generic = profile is None
        for w in (self.l_bore, self.c_bore, self.l_u, self.c_u, self.l_design,
                  self.c_design):
            w.setVisible(generic)
        self.l_model.setVisible(not generic)
        self.c_model.setVisible(not generic)
        self.c_design.blockSignals(True)
        self.c_design.clear()
        for d in TYPICAL_DESIGNS:
            self.c_design.addItem(DESIGN_NAMES[d.id][0 if STATE.language.value == "es" else 1],
                                  d.id)
        same = [i for i, d in enumerate(TYPICAL_DESIGNS) if d.connection is self.ctx.connection]
        self.c_design.setCurrentIndex(same[0] if same else 0)
        self.c_design.blockSignals(False)
        if profile is not None:
            self._fill_models(profile)
        self._design_changed()

    def _fill_models(self, profile: ClientProfile) -> None:
        sel = select_model(profile, connection=self.ctx.connection, nps=self.ctx.nps,
                           rating_class=self.ctx.rating_class, elbow=self.ctx.elbow)
        self.c_model.blockSignals(True)
        self.c_model.clear()
        for key, m in profile.models.items():
            self.c_model.addItem(f"{key}  (U = {m.U_mm:g} mm)", key)
        if sel.model:
            self.c_model.setCurrentIndex(max(self.c_model.findData(sel.model), 0))
            self.info.setText(t("des.auto_model", model=sel.model, nps=sel.nps_used))
        else:
            self.info.setText(t(f"des.{sel.reason}", nps=sel.nps_used))
        self.c_model.blockSignals(False)

    def _design_changed(self) -> None:
        design = TYPICAL_DESIGNS[max(self.c_design.currentIndex(), 0)]
        for combo, items in ((self.c_size, design.sizes),):
            combo.blockSignals(True)
            combo.clear()
            combo.addItems(list(items))
            combo.blockSignals(False)
        self.c_bore.blockSignals(True)
        self.c_bore.clear()
        for bore in design.diameters:
            label = '0,260" (6,6 mm)' if bore == BORE_260 else '0,385" (9,8 mm)'
            if bore not in (BORE_260, BORE_385):
                label = fmt_quantity(bore, QuantityKind.DIAMETER)
            self.c_bore.addItem(label, bore)
        self.c_bore.blockSignals(False)
        self.c_u.blockSignals(True)
        self.c_u.clear()
        rec = (recommended_u(self.ctx.pipe_id, self.ctx.nozzle_length)
               if self.ctx.pipe_id else None)
        if rec is not None:
            self.c_u.addItem(t("des.u_rec", u=fmt_quantity(rec, QuantityKind.LENGTH)), rec)
        for u in STANDARD_U:
            if u >= design.min_u and (rec is None or abs(u - rec) > 1e-6):
                self.c_u.addItem(fmt_quantity(u, QuantityKind.LENGTH), u)
        self.c_u.blockSignals(False)
        if self._profile() is None:
            needs_nozzle = design.connection not in (ConnectionType.WELD_IN,
                                                     ConnectionType.SOCKET_WELD)
            self.info.setText(t("des.no_nozzle") if needs_nozzle and not self.ctx.nozzle_length
                              else "")
        self._update()

    # --- Resultado --------------------------------------------------------------------
    def _compute(self) -> DesignChoice | None:
        profile = self._profile()
        rating = self.ctx.rating_class
        nozzle = self.ctx.nozzle_length
        if profile is not None:
            model = self.c_model.currentData()
            if model is None:
                return None
            nz = profile.nozzle_length(rating, str(model))
            return profile_choice(profile, str(model), size=self.c_size.currentText(),
                                  nozzle_length=nz if nz is not None and not nozzle else nozzle,
                                  rating_class=rating)
        design = TYPICAL_DESIGNS[max(self.c_design.currentIndex(), 0)]
        bore, u = self.c_bore.currentData(), self.c_u.currentData()
        if bore is None or u is None:
            return None
        return build_choice(design, size=self.c_size.currentText(), bore=float(bore),
                            U=float(u), nozzle_length=nozzle, rating_class=rating)

    def _update(self) -> None:
        profile = self._profile()
        if profile is not None:
            model = self.c_model.currentData()
            if model is not None:
                design_id = profile.models[str(model)].design
                self.c_design.blockSignals(True)
                idx = next(i for i, d in enumerate(TYPICAL_DESIGNS) if d.id == design_id)
                if self.c_design.currentIndex() != idx:
                    self.c_design.setCurrentIndex(idx)
                    self.c_size.clear()
                    self.c_size.addItems(list(TYPICAL_DESIGNS[idx].sizes))
                self.c_design.blockSignals(False)
        self.choice = self._compute()
        self.btn_apply.setEnabled(self.choice is not None)
        if self.choice is None:
            self.summary.setText("")
            return
        c = self.choice

        def q(v: float) -> str:
            return fmt_quantity(v, QuantityKind.LENGTH)

        extra = f", Ls = {q(c.Ls)}" if c.profile is ShankProfile.STEPPED else ""
        text = t("des.summary", profile=enum_text(c.profile.value),
                 conn=enum_text(c.connection.value), size=c.size, U=q(c.U), A=q(c.A),
                 B=q(c.B), d=q(c.d), t=q(c.t), extra=extra, L0=q(c.L0))
        for n in c.notes:
            text += "\n• " + (t(f"des.{n}") if n == "short_for_design" else n)
        self.summary.setText(text)

    def _import(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, t("des.import"), "", "JSON (*.json)")
        if not path:
            return
        try:
            profile = load_profile(Path(path))
        except ValueError as exc:
            QMessageBox.warning(self, t("des.import"), t("des.import_err", err=str(exc)))
            return
        folder = profile_folder()
        if folder is not None:
            shutil.copy(path, folder / f"{profile.id}.json")
        self.profiles = [p for p in self.profiles if p.id != profile.id] + [profile]
        self._fill_sources()
        self.c_source.setCurrentIndex(self.c_source.findData(profile.id))
