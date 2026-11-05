"""Temas claro y oscuro (paleta Qt + hoja de estilos)."""

from __future__ import annotations

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

LIGHT = {"window": "#f4f5f7", "base": "#ffffff", "text": "#20242a", "alt": "#eef0f3",
         "button": "#e9ecf0", "highlight": "#2a6fdb", "mid": "#c9ced6",
         "disabled": "#8a9099"}
DARK = {"window": "#1b1e24", "base": "#23272f", "text": "#e6e8eb", "alt": "#2a2f38",
        "button": "#2d323b", "highlight": "#4a8cf0", "mid": "#3b414c",
        "disabled": "#8a9099"}

QSS = """
QLineEdit[invalid="true"] {{ border: 2px solid #d0342c; border-radius: 3px; }}
QLabel#errorLabel {{ color: #d0342c; padding: 4px; }}
QLabel#errorLabel[ok="true"] {{ color: {text}; }}
QLabel#warningLabel {{ color: #b06000; }}
QGroupBox {{ font-weight: bold; border: 1px solid {mid}; border-radius: 6px;
             margin-top: 12px; padding-top: 8px; }}
QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 4px; }}
QListWidget::item:selected {{ background: {highlight}; color: white; }}
QToolBar {{ spacing: 4px; }}
"""


def apply_theme(app: QApplication, dark: bool) -> None:
    """Aplica el tema elegido a toda la aplicación."""
    c = DARK if dark else LIGHT
    app.setStyle("Fusion")
    pal = QPalette()
    roles = {
        QPalette.ColorRole.Window: c["window"], QPalette.ColorRole.WindowText: c["text"],
        QPalette.ColorRole.Base: c["base"], QPalette.ColorRole.AlternateBase: c["alt"],
        QPalette.ColorRole.Text: c["text"], QPalette.ColorRole.Button: c["button"],
        QPalette.ColorRole.ButtonText: c["text"], QPalette.ColorRole.Highlight: c["highlight"],
        QPalette.ColorRole.HighlightedText: "#ffffff", QPalette.ColorRole.ToolTipBase:
        c["base"], QPalette.ColorRole.ToolTipText: c["text"], QPalette.ColorRole.Mid: c["mid"],
    }
    for role, color in roles.items():
        pal.setColor(role, QColor(color))
    for role in (QPalette.ColorRole.Text, QPalette.ColorRole.ButtonText,
                 QPalette.ColorRole.WindowText):
        pal.setColor(QPalette.ColorGroup.Disabled, role, QColor(c["disabled"]))
    app.setPalette(pal)
    app.setStyleSheet(QSS.format(**c))
