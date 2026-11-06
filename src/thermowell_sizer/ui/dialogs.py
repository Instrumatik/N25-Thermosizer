"""Diálogos: opciones de cálculo, datos del proyecto y acerca de."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from thermowell_sizer import DISCLAIMER_EN, DISCLAIMER_ES, __version__
from thermowell_sizer.core.models import EngineOptions, MetalState, StrouhalMethod
from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.i18n import Language
from thermowell_sizer.project import ProjectInfo, ProjectSettings
from thermowell_sizer.ui.assets import asset_path
from thermowell_sizer.ui.infocard_ui import add_info_buttons
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.text import enum_text, t
from thermowell_sizer.ui.widgets import QuantityEdit

DAMPING_DECIMALS = 5
DAMPING_MAX = 0.05


def _buttons(dlg: QDialog) -> QDialogButtonBox:
    box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                           | QDialogButtonBox.StandardButton.Cancel)
    box.accepted.connect(dlg.accept)
    box.rejected.connect(dlg.reject)
    return box


class OptionsDialog(QDialog):
    """Opciones del motor para el tag activo."""

    def __init__(self, options: EngineOptions, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(t("opt.title"))
        self._base = options
        f = QFormLayout(self)
        self.damping = QDoubleSpinBox()
        self.damping.setDecimals(DAMPING_DECIMALS)
        self.damping.setRange(1e-5, DAMPING_MAX)
        self.damping.setSingleStep(1e-4)
        self.damping.setValue(options.damping)
        self.strouhal = QComboBox()
        self.strouhal.addItem(t("opt.strouhal_corr"), StrouhalMethod.CORRELATION)
        self.strouhal.addItem(t("opt.strouhal_simple"), StrouhalMethod.SIMPLIFIED)
        self.strouhal.setCurrentIndex(self.strouhal.findData(options.strouhal_method))
        self.fe = QDoubleSpinBox()
        self.fe.setRange(0.01, 1.0)
        self.fe.setSingleStep(0.05)
        self.fe.setValue(options.environmental_factor)
        self.metal = QComboBox()
        self.metal.addItem(t("opt.auto"), None)
        for m in MetalState:
            self.metal.addItem(enum_text(m.value), m)
        self.metal.setCurrentIndex(max(self.metal.findData(options.metal_state), 0))
        self.inline = QCheckBox(t("opt.inline"))
        self.inline.setChecked(options.allow_inline_passage)
        self.corr = QCheckBox(t("opt.corrosion_cases"))
        self.corr.setChecked(options.corrosion_cases)
        self.supplier = QCheckBox(t("opt.supplier"))
        self.supplier.setChecked(options.supplier_rating)
        self.amber = QDoubleSpinBox()
        self.amber.setRange(0.0, 50.0)
        self.amber.setValue(options.amber_margin_pct)
        self.flange = QuantityEdit(QuantityKind.PRESSURE, optional=True, minimum=0.0)
        if options.flange_rating is not None:
            self.flange.set_value(options.flange_rating + STATE.barometric)
        f.addRow(t("opt.damping"), self.damping)
        f.addRow(t("opt.strouhal"), self.strouhal)
        f.addRow(t("opt.fe"), self.fe)
        f.addRow(t("opt.metal_state"), self.metal)
        f.addRow(t("opt.amber"), self.amber)
        f.addRow(t("opt.flange_manual") + " (g)", self.flange)
        f.addRow(self.inline)
        f.addRow(self.corr)
        f.addRow(self.supplier)
        add_info_buttons(f)
        f.addRow(_buttons(self))

    def options(self) -> EngineOptions:
        """Opciones editadas."""
        flange_abs = self.flange.value()
        return self._base.model_copy(update={
            "damping": self.damping.value(),
            "strouhal_method": self.strouhal.currentData(),
            "environmental_factor": self.fe.value(),
            "metal_state": self.metal.currentData(),
            "allow_inline_passage": self.inline.isChecked(),
            "corrosion_cases": self.corr.isChecked(),
            "supplier_rating": self.supplier.isChecked(),
            "amber_margin_pct": self.amber.value(),
            "flange_rating": (max(flange_abs - STATE.barometric, 1.0)
                              if flange_abs is not None else None),
        })


class ProjectDialog(QDialog):
    """Datos generales del proyecto y preferencias de presión."""

    def __init__(self, info: ProjectInfo, settings: ProjectSettings,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(t("act.project_info"))
        self._info = info
        self._settings = settings
        f = QFormLayout(self)
        self.name = QLineEdit(info.name)
        self.client = QLineEdit(info.client)
        self.plant = QLineEdit(info.plant)
        self.doc = QLineEdit(info.document_number)
        self.baro = QuantityEdit(QuantityKind.PRESSURE, minimum=1.0)
        self.baro.set_value(settings.barometric_pressure)
        self.gauge = QCheckBox(t("dlg.gauge"))
        self.gauge.setChecked(settings.pressure_as_gauge)
        f.addRow(t("dlg.project_name"), self.name)
        f.addRow(t("dlg.client"), self.client)
        f.addRow(t("dlg.plant"), self.plant)
        f.addRow(t("dlg.doc_number"), self.doc)
        f.addRow(t("dlg.barometric") + " (abs)", self.baro)
        f.addRow(self.gauge)
        add_info_buttons(f)
        f.addRow(_buttons(self))

    def result_data(self) -> tuple[ProjectInfo, ProjectSettings]:
        """Datos editados."""
        info = self._info.model_copy(update={
            "name": self.name.text().strip() or self._info.name,
            "client": self.client.text(), "plant": self.plant.text(),
            "document_number": self.doc.text()})
        settings = self._settings.model_copy(update={
            "barometric_pressure": self.baro.value() or self._settings.barometric_pressure,
            "pressure_as_gauge": self.gauge.isChecked()})
        return info, settings


class AboutDialog(QDialog):
    """Acerca de, con el aviso de responsabilidad."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(t("act.about"))
        lay = QVBoxLayout(self)
        logo = QLabel()
        pix = QPixmap(str(asset_path("logo_tws.png")))
        if not pix.isNull():
            logo.setPixmap(pix.scaledToWidth(260, Qt.TransformationMode.SmoothTransformation))
        lay.addWidget(logo, 0, Qt.AlignmentFlag.AlignHCenter)
        disclaimer = DISCLAIMER_ES if STATE.language is Language.ES else DISCLAIMER_EN
        text = QLabel(
            f"<h2>ThermoWell Sizer {__version__}</h2>"
            "<p>ASME PTC 19.3 TW-2016 · InstruMatik</p>"
            f"<p style='color:#b06000'>{disclaimer}</p>"
            "<p>CoolProp (MIT), Qt for Python (LGPL), NumPy, SciPy, matplotlib.</p>")
        text.setWordWrap(True)
        lay.addWidget(text)
        box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        box.accepted.connect(self.accept)
        lay.addWidget(box)
