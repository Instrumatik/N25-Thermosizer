"""Controles reutilizables: campo con unidades, combos de enumeraciones y semáforos."""

from __future__ import annotations

import math
from collections.abc import Iterable
from enum import StrEnum

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPaintEvent
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QLineEdit, QWidget

from thermowell_sizer.core.models import CheckStatus
from thermowell_sizer.core.units import QuantityKind, from_display, to_display
from thermowell_sizer.i18n import format_number, parse_number
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.text import enum_text, t

STATUS_COLORS: dict[CheckStatus | None, str] = {
    CheckStatus.PASS: "#2e9e44",
    CheckStatus.WARNING: "#e0a100",
    CheckStatus.FAIL: "#d0342c",
    CheckStatus.NOT_APPLICABLE: "#8a8f98",
    None: "#8a8f98",
}
SIGNIFICANT_DIGITS = 5


def smart_decimals(value: float) -> int:
    """Decimales para mostrar ``value`` con unas cinco cifras significativas."""
    if value == 0 or not math.isfinite(value):
        return 2
    magnitude = math.floor(math.log10(abs(value)))
    return max(0, min(6, SIGNIFICANT_DIGITS - 1 - magnitude))


def fmt(value: float, decimals: int | None = None) -> str:
    """Número con el separador decimal del idioma vigente.

    Sin ``decimals`` muestra unas cinco cifras significativas y quita los ceros finales.
    """
    if not math.isfinite(value):
        return "∞" if value > 0 else "—"
    if decimals is not None:
        return format_number(value, decimals, STATE.language)
    text = format_number(value, smart_decimals(value), STATE.language)
    sep = "," if STATE.language.value == "es" else "."
    if sep in text:
        text = text.rstrip("0").rstrip(sep)
    return text


def fmt_quantity(value_si: float, kind: QuantityKind, *, gauge: bool = False) -> str:
    """Valor SI convertido a las unidades vigentes, con su símbolo."""
    value, symbol = to_display(value_si, kind, STATE.units, gauge=gauge,
                               barometric_pa=STATE.barometric)
    return f"{fmt(value)} {symbol}".strip()


class QuantityEdit(QWidget):
    """Campo numérico que guarda el valor en SI y lo muestra en las unidades vigentes.

    Emite :attr:`changed` cuando el usuario termina de editar un valor válido. Si el
    texto no es un número, el campo se marca en rojo y ``value()`` devuelve ``None``.
    """

    changed = Signal()

    def __init__(
        self,
        kind: QuantityKind,
        *,
        gauge_capable: bool = False,
        optional: bool = False,
        minimum: float | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.kind = kind
        self.gauge_capable = gauge_capable
        self.optional = optional
        self.minimum = minimum
        self._si: float | None = None
        self.edit = QLineEdit()
        self.edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit.setMinimumWidth(90)
        self.unit = QLabel()
        self.unit.setMinimumWidth(44)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.edit, 1)
        layout.addWidget(self.unit)
        self.edit.editingFinished.connect(self._commit)
        self.edit.textEdited.connect(self._live_check)
        self.refresh_units()

    @property
    def gauge(self) -> bool:
        """Si se muestran presiones manométricas."""
        return self.gauge_capable and STATE.gauge

    def value(self) -> float | None:
        """Valor en SI, o ``None`` si está vacío o es inválido."""
        return self._si

    def set_value(self, value_si: float | None) -> None:
        """Muestra un valor SI sin emitir :attr:`changed`."""
        self._si = value_si
        self._render()

    def set_error(self, message: str | None) -> None:
        """Marca el campo con un error de validación (o lo limpia)."""
        self.edit.setProperty("invalid", bool(message))
        self.edit.setToolTip(message or "")
        self.edit.style().unpolish(self.edit)
        self.edit.style().polish(self.edit)

    def refresh_units(self) -> None:
        """Vuelve a mostrar el valor tras un cambio de unidades o idioma."""
        _, symbol = to_display(0.0, self.kind, STATE.units, gauge=self.gauge,
                               barometric_pa=STATE.barometric)
        self.unit.setText(symbol)
        self._render()

    def _render(self) -> None:
        if self._si is None:
            self.edit.setText("")
            return
        value, _ = to_display(self._si, self.kind, STATE.units, gauge=self.gauge,
                              barometric_pa=STATE.barometric)
        self.edit.setText(fmt(value))

    def _parse(self, text: str) -> float | None:
        value = parse_number(text, STATE.language)
        si = from_display(value, self.kind, STATE.units, gauge=self.gauge,
                          barometric_pa=STATE.barometric)
        if self.minimum is not None and si < self.minimum:
            raise ValueError
        return si

    def _live_check(self, text: str) -> None:
        if not text.strip():
            self.set_error(None if self.optional else t("status.invalid"))
            return
        try:
            self._parse(text)
            self.set_error(None)
        except ValueError:
            self.set_error(t("status.invalid"))

    def _commit(self) -> None:
        text = self.edit.text()
        if not text.strip():
            new: float | None = None
        else:
            try:
                new = self._parse(text)
            except ValueError:
                return
        if new != self._si:
            self._si = new
            self._render()
            self.changed.emit()


class EnumCombo(QComboBox):
    """Combo con los valores de una enumeración y sus nombres traducidos."""

    def __init__(self, values: Iterable[StrEnum], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._values = list(values)
        self.retranslate()

    def retranslate(self) -> None:
        """Actualiza los textos sin cambiar la selección."""
        current = self.currentIndex()
        self.blockSignals(True)
        self.clear()
        for v in self._values:
            self.addItem(enum_text(v.value), v)
        self.setCurrentIndex(max(current, 0))
        self.blockSignals(False)

    def value(self) -> StrEnum:
        """Valor seleccionado."""
        return self._values[max(self.currentIndex(), 0)]

    def set_value(self, value: StrEnum) -> None:
        """Selecciona ``value`` sin emitir señales."""
        self.blockSignals(True)
        self.setCurrentIndex(self._values.index(value))
        self.blockSignals(False)


class StatusLight(QWidget):
    """Semáforo circular con texto (CUMPLE / REVISAR / NO CUMPLE)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.status: CheckStatus | None = None
        self.setMinimumSize(180, 44)

    def set_status(self, status: CheckStatus | None) -> None:
        """Cambia el estado mostrado."""
        self.status = status
        self.setAccessibleName(self.label())
        self.update()

    def label(self) -> str:
        """Texto del estado."""
        if self.status is None:
            return t("res.not_calculated")
        return t(f"status.{self.status.value}")

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802 - API de Qt
        """Dibuja el círculo y el texto."""
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        h = self.height() - 8
        p.setBrush(QColor(STATUS_COLORS[self.status]))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(4, 4, h, h)
        font = p.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSizeF() * 1.3)
        p.setFont(font)
        p.setPen(self.palette().windowText().color())
        p.drawText(h + 14, 0, self.width() - h - 14, self.height(),
                   Qt.AlignmentFlag.AlignVCenter, self.label())
        p.end()
