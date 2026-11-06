"""Piezas comunes de los reportes: formato de números y unidades, textos y datos."""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from datetime import date
from typing import Final

from thermowell_sizer import DISCLAIMER_EN, DISCLAIMER_ES, __version__
from thermowell_sizer.core.advisories import Advisory, AdvisoryLevel, inspection_plan
from thermowell_sizer.core.models import CheckStatus
from thermowell_sizer.core.units import QuantityKind, UnitSystem, to_display
from thermowell_sizer.data.database import Library
from thermowell_sizer.i18n import Language, format_number, tr
from thermowell_sizer.project import Project, TagRecord
from thermowell_sizer.services import Evaluation, evaluate, render_advisory

SIGNIFICANT: Final = 5
SCI_LOW: Final = 1e-3
SCI_HIGH: Final = 1e9
"""Fuera de este rango los números se muestran en notación científica."""
STATUS_RGB: Final = {CheckStatus.PASS: (0.18, 0.62, 0.27), CheckStatus.WARNING: (0.88, 0.63, 0.0),
                     CheckStatus.FAIL: (0.82, 0.2, 0.17),
                     CheckStatus.NOT_APPLICABLE: (0.54, 0.56, 0.6)}

CRITERION_NAMES: Final[dict[str, tuple[str, str]]] = {
    "scope": ("Alcance de la norma", "Scope of the standard"),
    "material_temperature": ("Temperatura del material", "Material temperature"),
    "fatigue_data": ("Datos de fatiga", "Fatigue data"),
    "pressure_rating": ("Presión externa", "External pressure"),
    "pressure_high_service": ("Servicio de alta presión", "High-pressure service"),
    "flange_rating": ("Rating de brida", "Flange rating"),
    "low_velocity": ("Exención por baja velocidad", "Low-velocity exemption"),
    "steady_stress_support": ("Esfuerzo estacionario (soporte)", "Steady stress (support)"),
    "steady_stress_step": ("Esfuerzo estacionario (escalón)", "Steady stress (step)"),
    "dynamic_stress_support": ("Esfuerzo dinámico (soporte)", "Dynamic stress (support)"),
    "dynamic_stress_step": ("Esfuerzo dinámico (escalón)", "Dynamic stress (step)"),
    "frequency_limit": ("Límite de frecuencia", "Frequency limit"),
    "inline_lockin_dwell": ("Captura en línea", "In-line lock-in"),
}
SCOPE_NAMES: Final[dict[str, tuple[str, str]]] = {
    "min": ("Mín.", "Min"), "normal": ("Normal", "Normal"), "max": ("Máx.", "Max"),
    "root_corrosion": ("corr. raíz", "root corr."), "tip_corrosion": ("corr. punta", "tip corr."),
}

TEXT: Final[dict[str, tuple[str, str]]] = {
    "ov.inputs_title": ("Datos de entrada principales", "Main input data"),
    "ov.inputs_text": (
        "Los 15 datos de la planilla de referencia, con su valor en este tag, de dónde sale "
        "(cargado por el usuario o calculado por el programa) y si interviene en la "
        "verificación ASME PTC 19.3 TW o solo en las recomendaciones.",
        "The 15 inputs of the reference spreadsheet, with their value for this tag, where "
        "they come from (entered by the user or calculated by the program) and whether they "
        "enter the ASME PTC 19.3 TW verification or only the recommendations."),
    "ov.title": ("2. Resumen de la verificación", "2. Verification summary"),
    "ov.input": ("Dato", "Input"),
    "ov.origin": ("Origen", "Source"),
    "ov.asme_use": ("Cálculo ASME", "ASME calculation"),
    "ds.title": ("HOJA DE DATOS — TERMOPOZO", "THERMOWELL DATASHEET"),
    "memo.title": ("MEMORIA DE CÁLCULO — TERMOPOZO", "THERMOWELL CALCULATION REPORT"),
    "summary.title": ("RESUMEN DEL PROYECTO — TERMOPOZOS", "PROJECT SUMMARY — THERMOWELLS"),
    "bom.title": ("LISTA DE MATERIALES", "BILL OF MATERIALS"),
    "project": ("Proyecto", "Project"), "client": ("Cliente", "Client"),
    "plant": ("Planta", "Plant"), "doc": ("Documento", "Document"), "rev": ("Rev.", "Rev."),
    "date": ("Fecha", "Date"), "sheet": ("Hoja", "Sheet"), "of": ("de", "of"),
    "prepared": ("Elaboró", "Prepared"), "checked": ("Revisó", "Checked"),
    "approved": ("Aprobó", "Approved"), "description": ("Descripción", "Description"),
    "sec.general": ("GENERAL", "GENERAL"),
    "sec.process": ("CONDICIONES DE PROCESO", "PROCESS CONDITIONS"),
    "sec.pipe": ("TUBERÍA / INSTALACIÓN", "PIPE / INSTALLATION"),
    "sec.thermowell": ("TERMOPOZO", "THERMOWELL"),
    "sec.sensor": ("SENSOR", "SENSOR"),
    "sec.calc": ("CÁLCULO ASME PTC 19.3 TW-2016", "ASME PTC 19.3 TW-2016 CALCULATION"),
    "sec.notes": ("NOTAS", "NOTES"),
    "tag": ("Tag", "Tag"), "service": ("Servicio", "Service"),
    "line": ("Línea / equipo", "Line / equipment"), "pid": ("P&ID", "P&ID"),
    "location": ("Ubicación", "Location"), "fluid": ("Fluido", "Fluid"),
    "phase": ("Fase", "Phase"), "p_op": ("Presión de operación", "Operating pressure"),
    "p_design": ("Presión de diseño", "Design pressure"),
    "t_op": ("Temperatura de operación", "Operating temperature"),
    "t_design": ("Temperatura de diseño", "Design temperature"),
    "density": ("Densidad", "Density"), "viscosity": ("Viscosidad", "Viscosity"),
    "props_source": ("Fuente de propiedades", "Property source"),
    "velocity": ("Velocidad", "Velocity"), "case": ("Caso", "Case"),
    "pipe_size": ("Tamaño / schedule", "Size / schedule"),
    "pipe_id": ("Diámetro interno", "Inner diameter"),
    "orientation": ("Orientación", "Orientation"),
    "nozzle": ("Hs, altura de la brida de montaje", "Hs, mounting flange height"),
    "wall": ("Espesor de pared", "Wall thickness"),
    "u_breakdown": ("U = Hs + pared + inmersión", "U = Hs + wall + immersion"),
    "u_breakdown_value": ("{hs} + {wall} + {imm}", "{hs} + {wall} + {imm}"),
    "construction": ("Construcción", "Construction"),
    "bar_stock": ("Barra maciza", "Bar stock"), "profile": ("Perfil", "Profile"),
    "material": ("Material", "Material"), "coating": ("Recubrimiento", "Coating"),
    "connection": ("Conexión", "Connection"), "rating": ("Clase / cara", "Class / face"),
    "U": ("Inserción U", "Insertion U"), "L": ("Longitud no soportada L", "Unsupported L"),
    "A": ("Diámetro de raíz A", "Root diameter A"), "B": ("Diámetro de punta B", "Tip B"),
    "d": ("Agujero d", "Bore d"), "t": ("Espesor de punta t", "Tip thickness t"),
    "b": ("Radio de acuerdo b", "Fillet b"), "lag": ("Lag T", "Lag T"),
    "ca": ("Sobreespesor de corrosión", "Corrosion allowance"),
    "sensor_type": ("Tipo", "Type"), "sheath": ("Diámetro de vaina", "Sheath diameter"),
    "fs": ("Frecuencia de estela f_s", "Wake frequency f_s"),
    "fnc": ("Frecuencia natural instalada f_n,c", "Installed natural frequency f_n,c"),
    "ratio": ("Relación f_s / f_n,c (límite)", "Ratio f_s / f_n,c (limit)"),
    "scruton": ("Número de Scruton", "Scruton number"),
    "dyn": ("Esfuerzo dinámico / admisible", "Dynamic stress / allowable"),
    "steady": ("Esfuerzo estacionario / admisible", "Steady stress / allowable"),
    "pr": ("Presión de diseño / admisible", "Design / allowable pressure"),
    "vmax": ("Velocidad máxima admisible", "Maximum allowable velocity"),
    "result": ("RESULTADO", "RESULT"), "tau": ("Constante de tiempo τ / t90",
                                              "Time constant τ / t90"),
    "status.pass": ("CUMPLE", "PASS"), "status.warning": ("REVISAR", "REVIEW"),
    "status.fail": ("NO CUMPLE", "FAIL"), "status.n/a": ("N/A", "N/A"),
    "not_calculated": ("Sin calcular", "Not calculated"),
    "toc": ("Índice", "Contents"),
    "m.scope": ("1. Objeto y alcance", "1. Purpose and scope"),
    "m.scope_text": (
        "Esta memoria verifica el termopozo identificado según ASME PTC 19.3 TW-2016: frecuencia "
        "de desprendimiento de vórtices frente a la frecuencia natural instalada, esfuerzos "
        "estacionarios y dinámicos con su límite de fatiga, y presión externa. Se citan los "
        "números de ecuación y párrafo de la norma; el texto de la norma no se reproduce. "
        "Se evalúan todos los casos de flujo y, si corresponde, las variantes con el sobreespesor "
        "de corrosión consumido en raíz y en punta (párr. 6-2).",
        "This report checks the identified thermowell per ASME PTC 19.3 TW-2016: vortex "
        "shedding frequency versus installed natural frequency, steady and dynamic stresses "
        "against the fatigue limit, and external pressure. Equation and paragraph numbers are "
        "cited; the text of the standard is not reproduced. All flow cases are evaluated and, "
        "when applicable, the variants with corrosion allowance consumed at root and tip "
        "(para. 6-2)."),
    "m.inputs": ("3. Datos de entrada", "3. Input data"),
    "ds.corr_cases": ("Los casos con sobreespesor de corrosión consumido (raíz y punta) se "
                      "detallan en la memoria de cálculo.", "Cases with the corrosion allowance "
                      "consumed (root and tip) are detailed in the calculation memo."),
    "m.auto": ("4. Selección automática y justificación", "4. Automatic selection and rationale"),
    "m.auto_text": ("Valores que completó el programa en los bloques en modo «Automático», con "
                   "la justificación de cada elección y sus alternativas. El resto de los datos "
                   "fue cargado por el usuario.", "Values filled by the program in the blocks set "
                   "to «Automatic», with the rationale for each choice and its alternatives. "
                   "All other data were entered by the user."),
    "m.auto_none": ("Todos los bloques en modo «Manual»: los datos de material, conexión, "
                   "geometría y sensor fueron cargados por el usuario.", "All blocks in "
                   "«Manual» mode: material, connection, geometry and sensor data were entered "
                   "by the user."),
    "m.material": ("5. Propiedades del material", "5. Material properties"),
    "m.options": ("6. Opciones de cálculo", "6. Calculation options"),
    "m.summary": ("7. Resumen de verificaciones", "7. Check summary"),
    "m.cases": ("8. Resumen por caso", "8. Case summary"),
    "m.trace": ("9. Desarrollo del cálculo", "9. Detailed calculation"),
    "m.charts": ("10. Sensibilidad", "10. Sensitivity"),
    "m.extra": ("11. Criterios adicionales", "11. Additional criteria"),
    "m.notes": ("12. Notas y advertencias", "12. Notes and warnings"),
    "m.common": ("Valores comunes", "Common values"),
    "criterion": ("Criterio", "Criterion"), "value": ("Valor", "Value"),
    "limit": ("Límite", "Limit"), "margin": ("Margen", "Margin"),
    "reference": ("Referencia", "Reference"), "status": ("Estado", "Status"),
    "symbol": ("Símbolo", "Symbol"), "expression": ("Expresión", "Expression"),
    "substitution": ("Datos", "Inputs"),
    "E": ("Módulo elástico E (operación)", "Elastic modulus E (operating)"),
    "E_ref": ("E de referencia", "Reference E"),
    "S": ("Esfuerzo admisible S (operación)", "Allowable stress S (operating)"),
    "S_design": ("Esfuerzo admisible S (diseño)", "Allowable stress S (design)"),
    "fatigue_class": ("Clase de fatiga", "Fatigue class"),
    "rho_m": ("Densidad del material", "Material density"),
    "source": ("Fuente", "Source"),
    "damping": ("Amortiguamiento ζ", "Damping ζ"), "strouhal": ("Strouhal", "Strouhal"),
    "fe": ("Factor ambiental F_E", "Environmental factor F_E"),
    "metal_state": ("Estado del metal", "Metal condition"),
    "flange_pf": ("Rating de brida P_f", "Flange rating P_f"),
    "inline": ("Paso por resonancia en línea", "In-line resonance passage"),
    "yes": ("Sí", "Yes"), "no": ("No", "No"), "auto": ("Automático", "Automatic"),
    "extra_text": (
        "Estimaciones fuera del alcance de PTC 19.3 TW, para orientar la selección.",
        "Estimates outside the scope of PTC 19.3 TW, to guide the selection."),
    "h": ("Coeficiente de película h", "Film coefficient h"),
    "imm_err": ("Error por conducción (base a 20 °C)", "Conduction error (base at 20 °C)"),
    "imm_min": ("Inmersión mínima para error < 0,1 K", "Minimum immersion for error < 0.1 K"),
    "qty": ("Cant.", "Qty"), "item": ("Ítem", "Item"),
    "generated": ("Generado con ThermoWell Sizer", "Generated with ThermoWell Sizer"),
    "units_note": ("Unidades", "Units"),
    "licensed_to": ("Licenciado a", "Licensed to"),
    "evaluation": ("VERSIÓN DE EVALUACIÓN", "EVALUATION VERSION"),
}


@dataclass(frozen=True, slots=True)
class Fmt:
    """Formato de números y magnitudes según idioma y sistema de unidades."""

    lang: Language = Language.ES
    units: UnitSystem = UnitSystem.SI
    barometric: float = 101_325.0
    gauge: bool = True
    licensee: str | None = None
    """Titular de la licencia; ``None`` = versión de evaluación (marca de agua)."""

    def t(self, key: str, **params: object) -> str:
        """Texto del reporte (o del catálogo general)."""
        pair = TEXT.get(key)
        if pair is None:
            text = tr(key, self.lang, **params)
            if text != key:
                return text
            from thermowell_sizer.ui.text import UI  # textos compartidos con la interfaz

            pair = UI.get(key)
            if pair is None:
                return key
        text = pair[0] if self.lang is Language.ES else pair[1]
        return text.format(**params) if params else text

    def num(self, value: float | None, decimals: int | None = None) -> str:
        """Número con ~5 cifras significativas y separador del idioma."""
        if value is None:
            return "—"
        if not math.isfinite(value):
            return "∞" if value > 0 else "—"
        if decimals is None and value and not SCI_LOW <= abs(value) < SCI_HIGH:
            mant = f"{value:.4e}"
            return mant.replace(".", ",") if self.lang is Language.ES else mant
        if decimals is None:
            mag = math.floor(math.log10(abs(value))) if value else 0
            decimals = max(0, min(6, SIGNIFICANT - 1 - mag))
            text = format_number(value, decimals, self.lang)
            sep = "," if self.lang is Language.ES else "."
            return text.rstrip("0").rstrip(sep) if sep in text else text
        return format_number(value, decimals, self.lang)

    def q(self, value_si: float | None, kind: QuantityKind, *, gauge: bool = False,
          decimals: int | None = None) -> str:
        """Magnitud SI en las unidades del reporte, con símbolo."""
        if value_si is None:
            return "—"
        value, sym = to_display(value_si, kind, self.units, gauge=gauge and self.gauge,
                                barometric_pa=self.barometric)
        return f"{self.num(value, decimals)} {sym}".strip()

    def pressure(self, value_abs: float) -> str:
        """Presión absoluta mostrada como manométrica si así se configuró."""
        return self.q(value_abs, QuantityKind.PRESSURE, gauge=True)

    def criterion(self, cid: str) -> str:
        """Nombre del criterio."""
        pair = CRITERION_NAMES.get(cid, (cid, cid))
        return pair[0] if self.lang is Language.ES else pair[1]

    def scope(self, scope: str) -> str:
        """Etiqueta de caso, con variante de corrosión."""
        if not scope:
            return "—"
        base, _, variant = scope.partition("|")
        idx = 0 if self.lang is Language.ES else 1
        text = SCOPE_NAMES.get(base, (base, base))[idx]
        if variant:
            text += " · " + SCOPE_NAMES.get(variant, (variant, variant))[idx]
        return text

    def status(self, status: CheckStatus | None) -> str:
        """Texto del estado."""
        return self.t("not_calculated") if status is None else self.t(f"status.{status.value}")

    @property
    def disclaimer(self) -> str:
        """Aviso de responsabilidad obligatorio."""
        return DISCLAIMER_ES if self.lang is Language.ES else DISCLAIMER_EN

    def footer(self) -> str:
        """Pie con versión, fecha y titular de la licencia."""
        lic = (f"{self.t('licensed_to')} {self.licensee}" if self.licensee
               else self.t("evaluation"))
        return f"{self.t('generated')} {__version__} · {date.today().isoformat()} · {lic}"


@dataclass(slots=True)
class TagReport:
    """Datos de un tag listos para reportar."""

    project: Project
    index: int
    record: TagRecord
    evaluation: Evaluation
    library: Library
    fmt: Fmt = field(default_factory=Fmt)

    @property
    def tag(self) -> str:
        """Nombre del tag."""
        return self.record.input.identification.tag


def make_fmt(project: Project, lang: Language | None = None,
             units: UnitSystem | None = None, licensee: str | None = None) -> Fmt:
    """Formato según las preferencias del proyecto (o las indicadas)."""
    s = project.settings
    return Fmt(lang or s.language, units or s.unit_system, s.barometric_pressure,
               s.pressure_as_gauge, licensee)


def tag_report(project: Project, index: int, library: Library, fmt: Fmt | None = None,
               evaluation: Evaluation | None = None) -> TagReport:
    """Arma el :class:`TagReport` evaluando el tag si hace falta."""
    rec = project.tags[index]
    ev = evaluation or evaluate(rec, library, project.settings)
    return TagReport(project, index, rec, ev, library, fmt or make_fmt(project))


def short_ref(reference: str) -> str:
    """Referencia abreviada."""
    return reference.replace("ASME PTC 19.3 TW-2016, ", "PTC 19.3 TW ")


def current_revision(project: Project) -> tuple[str, str]:
    """(revisión, fecha) vigentes."""
    if project.info.revisions:
        last = project.info.revisions[-1]
        return last.rev, last.date.isoformat()
    return "0", date.today().isoformat()


def _render(rep: TagReport, adv: Advisory) -> str:
    f = rep.fmt

    def qfmt(value: float, kind: QuantityKind) -> str:
        return f.pressure(value) if kind is QuantityKind.PRESSURE else f.q(value, kind)

    return render_advisory(adv, f.lang, qfmt, f.num)


def advisory_lines(rep: TagReport) -> list[tuple[AdvisoryLevel, str]]:
    """Advertencias y recomendaciones traducidas (la prueba hidráulica va en ensayos)."""
    return [(a.level, _render(rep, a)) for a in rep.evaluation.advisories
            if a.key != "adv.hydro_test"]


def inspection_lines(rep: TagReport, *, short: bool = False) -> list[str]:
    """Ensayos y documentación sugeridos, ya traducidos (``short``: versión resumida)."""
    plan = inspection_plan(rep.evaluation.input)
    if short:
        plan = [replace(a, key=f"{a.key}_short") for a in plan]
    return [_render(rep, a) for a in plan]
