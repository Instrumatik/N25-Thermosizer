"""Ayuda contextual (F1). Redacción propia; las referencias citan la norma por párrafo."""

from __future__ import annotations

from typing import Final

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QSplitter, QTextBrowser, QVBoxLayout, QWidget

from thermowell_sizer import DISCLAIMER_EN, DISCLAIMER_ES
from thermowell_sizer.i18n import Language
from thermowell_sizer.ui.state import STATE
from thermowell_sizer.ui.text import t

TOPICS: Final[tuple[tuple[str, str, str, str, str], ...]] = (
    # (id, título ES, título EN, cuerpo ES, cuerpo EN)
    ("start", "Primeros pasos", "Getting started",
     "<p>Un proyecto agrupa los tags (puntos de medición). Cree un tag con <b>Ctrl+T</b>, "
     "complete los cinco pasos del asistente y presione <b>F5</b> para calcular. El panel "
     "de resultados muestra el semáforo global y cada criterio con su margen.</p>"
     "<p>El <b>modo experto</b> (Ctrl+E) muestra todas las secciones en una sola página. "
     "Los cambios se autoguardan cada pocos minutos y pueden deshacerse con Ctrl+Z.</p>",
     "<p>A project groups tags (measuring points). Create a tag with <b>Ctrl+T</b>, fill "
     "in the five wizard steps and press <b>F5</b> to calculate. The results panel shows "
     "the overall traffic light and each criterion with its margin.</p>"
     "<p><b>Expert mode</b> (Ctrl+E) shows every section on one page. Changes are "
     "autosaved every few minutes and can be undone with Ctrl+Z.</p>"),
    ("identification", "1. Identificación", "1. Identification",
     "<p>El tag es obligatorio y debe ser único en el proyecto. Servicio, línea, P&amp;ID y "
     "ubicación aparecen en la hoja de datos.</p>",
     "<p>The tag is required and must be unique in the project. Service, line, P&amp;ID "
     "and location are printed on the datasheet.</p>"),
    ("process", "2. Proceso", "2. Process",
     "<p>Ingrese presiones (manométricas por defecto, se cambia en Preferencias) y "
     "temperaturas de operación y diseño. Con la casilla de propiedades automáticas, la "
     "densidad y la viscosidad se calculan con CoolProp o con las tablas de la biblioteca "
     "a las condiciones de operación, y la fase se detecta sola.</p>"
     "<p>Cargue al menos un caso de flujo (mínimo, normal, máximo) como velocidad, caudal "
     "másico o volumétrico. La velocidad se calcula con el diámetro interno de la tubería "
     "(párr. 7-3). Evalúe siempre el caso de mayor velocidad.</p>",
     "<p>Enter pressures (gauge by default, changeable in Preferences) and operating and "
     "design temperatures. With automatic properties enabled, density and viscosity are "
     "computed with CoolProp or library tables at operating conditions and the phase is "
     "detected automatically.</p><p>Enter at least one flow case (min, normal, max) as "
     "velocity, mass or volume flow. Velocity uses the pipe inner diameter (para. 7-3). "
     "Always evaluate the highest-velocity case.</p>"),
    ("pipe", "3. Tubería", "3. Pipe",
     "<p>Elija NPS y schedule para obtener el diámetro interno de ASME B36.10M, o "
     "seleccione “—” para cargarlo a mano. La longitud de tobera define cuánto del vástago "
     "queda protegido del flujo (L0).</p>",
     "<p>Choose NPS and schedule to get the ASME B36.10M inner diameter, or pick “—” to "
     "enter it manually. Nozzle length defines how much of the shank is shielded (L0).</p>"),
    ("thermowell", "4. Termopozo", "4. Thermowell",
     "<p>L es la longitud no soportada, desde la punta hasta el plano de soporte (cara de "
     "brida, inicio de rosca o soldadura). A es el diámetro en el soporte y B en la punta. "
     "Los límites dimensionales de la norma (tablas 4-1-1 y 4-2-1) se verifican mientras "
     "escribe: un campo en rojo indica un valor fuera de alcance.</p>"
     "<p>El programa nunca propone collares de velocidad: si la geometría no cumple, use "
     "el botón de alternativas (acortar, engrosar, perfil cónico, otro material).</p>",
     "<p>L is the unsupported length, from the tip to the support plane (flange face, "
     "thread start or weld). A is the diameter at the support and B at the tip. The "
     "standard's dimensional limits (tables 4-1-1 and 4-2-1) are checked as you type: a "
     "red field means the value is out of scope.</p><p>The program never proposes "
     "velocity collars: if the geometry fails, use the alternatives button (shorten, "
     "thicken, tapered profile, other material).</p>"),
    ("sensor", "5. Sensor", "5. Sensor",
     "<p>El diámetro de vaina y la masa del sensor intervienen en la corrección de "
     "frecuencia por masa añadida (H<sub>a,s</sub>). Si deja la masa vacía se estima.</p>",
     "<p>Sheath diameter and sensor mass enter the added-mass frequency correction "
     "(H<sub>a,s</sub>). Leave the mass blank to estimate it.</p>"),
    ("results", "Resultados", "Results",
     "<p>Verde: cumple con margen. Ámbar: cumple con margen menor al configurado (10 % por "
     "defecto) o requiere juicio de ingeniería. Rojo: no cumple. El margen es "
     "(límite − valor)/límite.</p><p>Se evalúan los casos sin corrosión y con el "
     "sobreespesor consumido en raíz y en punta (párr. 6-2). La pestaña de traza muestra "
     "cada paso con su ecuación de referencia; la memoria de cálculo la imprime "
     "completa.</p>",
     "<p>Green: passes with margin. Amber: passes with less than the configured margin "
     "(10 % by default) or requires engineering judgment. Red: fails. Margin is "
     "(limit − value)/limit.</p><p>Nominal and corroded cases (root and tip, para. 6-2) "
     "are evaluated. The trace tab lists every step with its reference equation; the "
     "calculation report prints it in full.</p>"),
    ("library", "Biblioteca", "Library",
     "<p>Materiales, bridas, tuberías, fluidos, glosario y fichas de normas. Ctrl+K abre el "
     "buscador, que tolera errores de escritura y acentos. Los valores de materiales y "
     "bridas son aproximados y deben verificarse contra la edición vigente de los códigos "
     "antes de un uso contractual.</p>",
     "<p>Materials, flanges, pipes, fluids, glossary and standard summaries. Ctrl+K opens "
     "the search, tolerant of typos and accents. Material and flange values are "
     "approximate and must be checked against the current code editions before "
     "contractual use.</p>"),
    ("disclaimer", "Aviso de responsabilidad", "Disclaimer", f"<p>{DISCLAIMER_ES}</p>",
     f"<p>{DISCLAIMER_EN}</p>"),
)
STEP_TOPICS: Final = ("identification", "process", "pipe", "thermowell", "sensor")


class HelpWindow(QWidget):
    """Ventana de ayuda no modal con índice de temas."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle(t("help.title"))
        self.resize(820, 540)
        self.index = QListWidget()
        self.view = QTextBrowser()
        es = STATE.language is Language.ES
        for topic in TOPICS:
            self.index.addItem(topic[1] if es else topic[2])
        self.index.currentRowChanged.connect(self._show)
        split = QSplitter()
        split.addWidget(self.index)
        split.addWidget(self.view)
        split.setSizes([220, 600])
        QVBoxLayout(self).addWidget(split)
        self.index.setCurrentRow(0)

    def _show(self, row: int) -> None:
        if 0 <= row < len(TOPICS):
            topic = TOPICS[row]
            es = STATE.language is Language.ES
            self.view.setHtml(f"<h2>{topic[1] if es else topic[2]}</h2>"
                              + (topic[3] if es else topic[4]))

    def show_topic(self, topic_id: str) -> None:
        """Abre el tema indicado."""
        for i, topic in enumerate(TOPICS):
            if topic[0] == topic_id:
                self.index.setCurrentRow(i)
        self.show()
        self.raise_()
        self.activateWindow()
