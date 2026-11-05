"""Punto de entrada de la aplicación de escritorio."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QSettings, QStandardPaths
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from thermowell_sizer import DISCLAIMER_EN, DISCLAIMER_ES
from thermowell_sizer.core.units import UnitSystem
from thermowell_sizer.data.database import Library
from thermowell_sizer.i18n import Language
from thermowell_sizer.ui.assets import asset_path
from thermowell_sizer.ui.main_window import MainWindow
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.theme import apply_theme

ORGANIZATION = "InstruMatik"
APPLICATION = "ThermoWellSizer"
LIBRARY_FILE = "biblioteca.sqlite"


def data_dir() -> Path:
    """Carpeta de datos del usuario (biblioteca, autoguardados)."""
    base = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
    path = Path(base)
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_preferences(settings: QSettings) -> None:
    """Carga idioma, unidades y tema guardados."""
    STATE.language = Language(str(settings.value("ui/language", Language.ES.value)))
    STATE.units = UnitSystem(str(settings.value("ui/units", UnitSystem.SI.value)))
    STATE.dark = bool(settings.value("ui/dark", False, type=bool))


class Application:
    """Mantiene la ventana principal y la reconstruye al cambiar el idioma."""

    def __init__(self, app: QApplication, library: Library, settings: QSettings) -> None:
        self.app = app
        self.library = library
        self.settings = settings
        self.window = MainWindow(library, settings, rebuild=self.rebuild)

    def rebuild(self, old: MainWindow) -> None:
        """Crea una ventana nueva en el idioma vigente conservando el proyecto."""
        new = MainWindow(self.library, self.settings, rebuild=self.rebuild)
        new.project = old.project
        new.path = old.path
        new.current = max(old.current, 0)
        new.evaluations.clear()
        new._fill_tree()
        new._load_current()
        new._set_dirty(old.dirty)
        new.setGeometry(old.geometry())
        new.show()
        old._rebuilding = True  # type: ignore[attr-defined]
        old.close()
        self.window = new


def first_run_disclaimer(settings: QSettings) -> None:
    """Muestra el aviso de responsabilidad la primera vez."""
    if settings.value("ui/disclaimer_ok", False, type=bool):
        return
    text = DISCLAIMER_ES if STATE.language is Language.ES else DISCLAIMER_EN
    QMessageBox.information(None, "ThermoWell Sizer", text)
    settings.setValue("ui/disclaimer_ok", True)


def main(argv: list[str] | None = None) -> int:
    """Arranca la interfaz. Acepta opcionalmente la ruta de un proyecto ``.tws``."""
    args = sys.argv if argv is None else argv
    app = QApplication(args)
    app.setOrganizationName(ORGANIZATION)
    app.setApplicationName(APPLICATION)
    app.setWindowIcon(QIcon(str(asset_path("logo_instrumatik.png"))))
    settings = QSettings()
    load_preferences(settings)
    apply_theme(app, STATE.dark)
    library = Library(data_dir() / LIBRARY_FILE)
    first_run_disclaimer(settings)
    shell = Application(app, library, settings)
    if len(args) > 1 and Path(args[1]).suffix == ".tws":
        shell.window.open_path(Path(args[1]))
    shell.window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
