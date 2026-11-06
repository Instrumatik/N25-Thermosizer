"""Diálogo Ayuda > Licencia: estado, huella del equipo e instalación de un código."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from thermowell_sizer import licensing
from thermowell_sizer.ui.assets import asset_path
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.text import t

if TYPE_CHECKING:
    from pathlib import Path

    from thermowell_sizer.ui.main_window import MainWindow


def license_folder() -> Path:
    """Carpeta donde se guarda ``licencia.txt``."""
    if STATE.data_folder is None:
        from thermowell_sizer.ui.app import data_dir

        STATE.data_folder = data_dir()
    return STATE.data_folder


def status_text(lic: licensing.License | None) -> str:
    """Descripción legible del estado de la licencia."""
    if lic is None:
        return t("lic.none")
    return t("lic.licensed").format(
        holder=lic.holder, edition=lic.edition.value.capitalize(), issued=lic.issued,
        expires=lic.expires or t("lic.never"), machine=lic.machine or t("lic.any"))


class LicenseDialog(QDialog):
    """Muestra la licencia vigente y permite instalar otra."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(t("lic.title"))
        self.setMinimumWidth(520)
        lay = QVBoxLayout(self)
        logo = QLabel()
        pix = QPixmap(str(asset_path("logo_tws.png")))
        if not pix.isNull():
            logo.setPixmap(pix.scaledToWidth(180, Qt.TransformationMode.SmoothTransformation))
        lay.addWidget(logo, 0, Qt.AlignmentFlag.AlignHCenter)
        self.status = QLabel()
        self.status.setWordWrap(True)
        lay.addWidget(self.status)
        lay.addWidget(QLabel(t("lic.fingerprint")))
        row = QHBoxLayout()
        self.fingerprint = QLineEdit(licensing.machine_fingerprint())
        self.fingerprint.setReadOnly(True)
        copy = QPushButton(t("lic.copy"))
        copy.clicked.connect(self._copy)
        row.addWidget(self.fingerprint)
        row.addWidget(copy)
        lay.addLayout(row)
        self.code = QPlainTextEdit()
        self.code.setPlaceholderText(t("lic.paste"))
        self.code.setMaximumHeight(110)
        lay.addWidget(self.code)
        self.install_button = QPushButton(t("lic.install"))
        self.install_button.clicked.connect(self.install)
        lay.addWidget(self.install_button)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)
        self.refresh()

    def refresh(self) -> None:
        """Relee la licencia instalada."""
        lic = licensing.load(license_folder())
        STATE.licensee = lic.holder if lic else None
        self.status.setText(status_text(lic))

    def _copy(self) -> None:
        QApplication.clipboard().setText(self.fingerprint.text())

    def install(self, *, quiet: bool = False) -> licensing.License | None:
        """Valida y guarda el código pegado. ``quiet`` evita los mensajes (pruebas)."""
        try:
            lic = licensing.install(license_folder(), self.code.toPlainText())
        except licensing.LicenseError as exc:
            if not quiet:
                QMessageBox.warning(self, t("lic.title"), t("lic.error").format(error=exc))
            return None
        self.refresh()
        self.code.clear()
        if not quiet:
            QMessageBox.information(self, t("lic.title"), t("lic.ok").format(holder=lic.holder))
        return lic


def show(window: MainWindow) -> None:
    """Abre el diálogo de licencia (modal)."""
    LicenseDialog(window).exec()
