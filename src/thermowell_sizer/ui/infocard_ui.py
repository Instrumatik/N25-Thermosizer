"""Ventana de fichas de ayuda (se abren desde «Buscar en la biblioteca» y los resultados)."""

from __future__ import annotations

import re
from collections.abc import Callable
from functools import lru_cache

from PySide6.QtCore import QUrl
from PySide6.QtGui import QImage, QTextDocument
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.infocards.content import CARDS, Card, card_for
from thermowell_sizer.infocards.render import render_card
from thermowell_sizer.services import Evaluation
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.text import UI
from thermowell_sizer.ui.widgets import fmt_quantity

Provider = Callable[[], tuple[Evaluation | None, str]]
_provider: list[Provider] = []
_reference: list[Callable[[], Evaluation | None]] = []
_SUFFIX = re.compile(r"\s*(\*|\(g\)|\(abs\)|\(mV\)|\(Ω\))\s*$")


def set_context(current: Provider, reference: Callable[[], Evaluation | None]) -> None:
    """Fija de dónde salen el tag actual y el caso de referencia para los ejemplos."""
    _provider[:] = [current]
    _reference[:] = [reference]


@lru_cache(maxsize=1)
def _text_to_key() -> dict[str, str]:
    """Texto visible (en ambos idiomas) → clave de texto, solo para claves con ficha."""
    out: dict[str, str] = {}
    for key, pair in UI.items():
        if card_for(key) is None:
            continue
        for text in pair:
            out.setdefault(text.strip().lower(), key)
    return out


def key_for_label(text: str) -> str | None:
    """Clave de la ficha para el texto de una etiqueta («Tag *» → «f.tag»)."""
    clean = _SUFFIX.sub("", text).strip().lower()
    return _text_to_key().get(clean)


def _qfmt(value: float, kind: QuantityKind) -> str:
    return fmt_quantity(value, kind, gauge=kind is QuantityKind.PRESSURE and STATE.gauge)


class CardDialog(QDialog):
    """Ventana con una ficha."""

    def __init__(self, card: Card, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        es = STATE.language.value == "es"
        self.setWindowTitle(("Ficha: " if es else "Card: ") + card.title[0 if es else 1])
        self.resize(720, 760)
        self.view = QTextBrowser()
        self.view.setOpenLinks(False)
        ev, tag = _provider[0]() if _provider else (None, "")
        ref = _reference[0]() if _reference else None
        rendered = render_card(card, ev, ref, es=es, qfmt=_qfmt, tag=tag)
        doc = self.view.document()
        for name, png in rendered.images.items():
            img = QImage.fromData(png)
            doc.addResource(QTextDocument.ResourceType.ImageResource, QUrl(f"img:{name}"), img)
        self.view.setHtml(rendered.html)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        close = buttons.button(QDialogButtonBox.StandardButton.Close)
        if close is not None:
            close.setText("Cerrar" if es else "Close")
        lay = QVBoxLayout(self)
        lay.addWidget(self.view)
        lay.addWidget(buttons)


def show_card(key: str, parent: QWidget | None = None) -> bool:
    """Abre la ficha de una clave; devuelve ``False`` si no hay ficha."""
    card = card_for(key)
    if card is None:
        return False
    CardDialog(card, parent).exec()
    return True


def all_card_ids() -> list[str]:
    """Identificadores de todas las fichas (para la búsqueda)."""
    return list(CARDS)
