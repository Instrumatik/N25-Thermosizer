"""Acciones del menú Reportes: piden destino, generan el archivo y lo abren."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from thermowell_sizer.reports.common import Fmt, TagReport, tag_report
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.text import t

if TYPE_CHECKING:
    from thermowell_sizer.ui.main_window import MainWindow

SPECS: dict[str, tuple[str, str, bool]] = {
    # tipo: (sufijo de archivo, filtro, todos los tags)
    "datasheet": ("HD", "PDF (*.pdf)", False),
    "memo": ("MC", "PDF (*.pdf)", False),
    "word": ("MC", "Word (*.docx)", False),
    "excel": ("resultados", "Excel (*.xlsx)", True),
    "project_report": ("resumen", "PDF (*.pdf)", True),
    "bom": ("BOM", "Excel (*.xlsx)", True),
}


def current_fmt(window: MainWindow) -> Fmt:
    """Formato con el idioma y las unidades de la interfaz."""
    s = window.project.settings
    return Fmt(STATE.language, STATE.units, s.barometric_pressure, s.pressure_as_gauge,
               STATE.licensee)


def generate(window: MainWindow, kind: str, path: Path) -> Path:
    """Genera el reporte ``kind`` en ``path`` (sin diálogos; también para pruebas)."""
    fmt = current_fmt(window)
    project = window.project

    def rep(i: int) -> TagReport:
        return tag_report(project, i, window.library, fmt, window.evaluations.get(i))

    if kind == "datasheet":
        from thermowell_sizer.reports.datasheet import build_datasheet

        return build_datasheet(rep(window.current), path)
    if kind == "memo":
        from thermowell_sizer.reports.memo import build_memo

        return build_memo(rep(window.current), path)
    if kind == "word":
        from thermowell_sizer.reports.word import build_word

        return build_word(rep(window.current), path)
    reps = [rep(i) for i in range(len(project.tags))]
    if kind == "excel":
        from thermowell_sizer.reports.excel import build_excel

        return build_excel(reps, path)
    if kind == "bom":
        from thermowell_sizer.reports.excel import build_excel

        return build_excel(reps, path, bom_only=True)
    from thermowell_sizer.reports.summary import build_summary

    return build_summary(reps, path)


def run(window: MainWindow, kind: str) -> None:
    """Pide el archivo de destino, genera el reporte y lo abre."""
    if window.current < 0:
        return
    window._flush_editor()
    suffix, filt, all_tags = SPECS[kind]
    base = (window.project.info.document_number or window.project.info.name) if all_tags \
        else window.project.tags[window.current].input.identification.tag
    ext = ".xlsx" if "xlsx" in filt else ".docx" if "docx" in filt else ".pdf"
    default = Path(window._last_dir()) / f"{base}_{suffix}{ext}".replace(" ", "_")
    name, _ = QFileDialog.getSaveFileName(window, t(f"act.{kind}"), str(default), filt)
    if not name:
        return
    path = Path(name)
    if path.suffix.lower() != ext:
        path = path.with_suffix(ext)
    QApplication.setOverrideCursor(window.cursor())
    try:
        generate(window, kind, path)
    except (OSError, ValueError) as exc:
        QMessageBox.warning(window, t(f"act.{kind}"), str(exc))
        return
    finally:
        QApplication.restoreOverrideCursor()
    window.statusBar().showMessage(str(path), 5000)
    QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
