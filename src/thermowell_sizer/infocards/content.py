"""Contenido de las fichas «ⓘ» (español e inglés).

Cada ficha explica un dato del programa: qué es, qué hace en el cálculo, qué resultados
afecta, sus umbrales, contra qué se compara, cómo interpretarlo, qué hacer y en qué parte de
la norma se apoya. Las referencias citan solo el número de párrafo o ecuación; no se
reproduce el texto de ninguna norma.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from thermowell_sizer.infocards.guides import (
    CONNECTION_NOTE,
    CONNECTION_ROWS,
    CONNECTION_TABLE,
    PROFILE_AUTO,
    PROFILE_COST_NOTE,
    PROFILE_ROWS,
    PROFILE_TABLE,
)

Bi = tuple[str, str]
_NO: Final[Bi] = ("", "")

SECTIONS: Final = ("what", "role", "affects", "limits", "compare", "interpret", "actions",
                   "reference", "units")
SECTION_TITLES: Final[dict[str, Bi]] = {
    "what": ("Qué es", "What it is"),
    "role": ("Qué hace en el programa", "What it does in the program"),
    "affects": ("Resultados que afecta", "Results it affects"),
    "limits": ("Umbrales y límites", "Thresholds and limits"),
    "compare": ("Contra qué se compara", "What it is compared against"),
    "interpret": ("Cómo interpretarlo", "How to read it"),
    "actions": ("Qué hacer", "What to do"),
    "reference": ("Referencia (resumida)", "Reference (summarized)"),
    "units": ("Unidades", "Units"),
    "formulas": ("Fórmulas", "Formulas"),
    "diagram": ("Diagrama", "Diagram"),
    "curves": ("Curvas con los datos del tag", "Curves with the tag data"),
    "example": ("Ejemplo resuelto", "Worked example"),
    "table": ("Guía de selección", "Selection guide"),
}


@dataclass(frozen=True, slots=True)
class Card:
    """Una ficha de ayuda."""

    id: str
    title: Bi
    what: Bi
    role: Bi
    affects: Bi = _NO
    limits: Bi = _NO
    compare: Bi = _NO
    interpret: Bi = _NO
    actions: Bi = _NO
    reference: Bi = _NO
    units: Bi = _NO
    formulas: tuple[str, ...] = ()
    diagram: str = ""
    """``tw:<cota>``, ``mount``, ``orientation`` o ``connection``."""
    curves: tuple[str, ...] = ()
    symbols: tuple[str, ...] = ()
    """Símbolos de la traza que se muestran en el ejemplo resuelto."""
    table: tuple[tuple[Bi, ...], ...] = ()
    """Tabla de guía: primera fila encabezados, cada celda (es, en)."""
    highlight: int = 0
    """Fila de la tabla resaltada (la opción de la ficha); 0 = ninguna."""
    table_note: Bi = _NO

    def text(self, section: str, es: bool) -> str:
        """Texto de una sección en el idioma pedido."""
        pair: Bi = getattr(self, section)
        return pair[0 if es else 1]


CARDS: dict[str, Card] = {}


def _c(cid: str, title: Bi, what: Bi, role: Bi, **kw: object) -> None:
    CARDS[cid] = Card(cid, title, what, role, **kw)  # type: ignore[arg-type]


# Fragmentos repetidos
_ID_ROLE = ("Solo identifica el tag en pantalla, en la lista de tags y en el rótulo de los "
            "reportes. No interviene en ningún cálculo.",
            "Only identifies the tag on screen, in the tag list and in the report title block. "
            "It does not enter any calculation.")
_ID_AFFECTS = ("Ningún resultado; aparece en la hoja de datos, la memoria y el resumen.",
               "No result; it appears in the datasheet, the memo and the summary.")
_GEOM_REF = ("ASME PTC 19.3 TW-2016, sección 4 (geometría y rangos de aplicación) y sección 6 "
             "(cálculo).", "ASME PTC 19.3 TW-2016, section 4 (geometry and scope) and section "
             "6 (calculation).")
_LEN = ("mm o in, según el sistema de unidades elegido.",
        "mm or in, depending on the chosen unit system.")
_PRESS = ("bar, kPa, MPa o psi; manométrica o absoluta según la opción del proyecto. Internamente "
          "se usa Pa absoluto.", "bar, kPa, MPa or psi; gauge or absolute depending on the "
          "project option. Internally Pa absolute is used.")
_TEMP = ("°C o °F (internamente K).", "°C or °F (internally K).")

# --- Identificación y proyecto -------------------------------------------------------------
for _id, _t, _w in (
    ("f.tag", ("Tag", "Tag"), ("Código único del termopozo en el proyecto (por ejemplo TW-101).",
                               "Unique code of the thermowell in the project (e.g. TW-101).")),
    ("f.service", ("Servicio", "Service"), ("Descripción breve del servicio o del punto de "
                                            "medición.", "Short description of the service or "
                                            "measuring point.")),
    ("f.line", ("Línea / equipo", "Line / equipment"),
     ("Número de línea o equipo donde se instala.", "Line or equipment number where it is "
                                                    "installed.")),
    ("f.pid", ("P&ID", "P&ID"), ("Plano P&ID donde figura el instrumento.",
                                 "P&ID drawing where the instrument appears.")),
    ("f.location", ("Ubicación", "Location"), ("Área o ubicación física en la planta.",
                                               "Area or physical location in the plant.")),
    ("dlg.project_name", ("Nombre del proyecto", "Project name"),
     ("Nombre del proyecto que agrupa los tags.", "Name of the project that groups the tags.")),
    ("dlg.client", ("Cliente", "Client"), ("Cliente o usuario final.", "Client or end user.")),
    ("dlg.plant", ("Planta", "Plant"), ("Planta o instalación.", "Plant or facility.")),
    ("dlg.doc_number", ("Número de documento", "Document number"),
     ("Código del documento en el rótulo de los reportes.",
      "Document code shown in the report title block.")),
):
    _c(_id, _t, _w, _ID_ROLE, affects=_ID_AFFECTS,
       actions=("Use la codificación del proyecto para que los reportes se puedan rastrear.",
                "Use the project numbering so the reports are traceable."))

_c("dlg.barometric", ("Presión barométrica", "Barometric pressure"),
   ("Presión atmosférica del sitio, en valor absoluto.",
    "Site atmospheric pressure, absolute."),
   ("Convierte las presiones manométricas que se cargan a absolutas para CoolProp y resta de "
    "nuevo para los esfuerzos por presión (que usan la diferencia con el exterior).",
    "Converts the gauge pressures entered to absolute for CoolProp and subtracts it again for "
    "pressure stresses (which use the difference with the outside)."),
   affects=("Densidad y viscosidad de gases, esfuerzos radiales, tangenciales y axiales, y la "
            "comparación con el rating de presión.", "Gas density and viscosity, radial, "
            "tangential and axial stresses, and the pressure-rating comparison."),
   limits=("Al nivel del mar 101,325 kPa; a 1000 m, unos 90 kPa.",
           "At sea level 101.325 kPa; at 1000 m, about 90 kPa."),
   interpret=("Solo cambia los resultados en gases a baja presión o en sitios de altura.",
              "It only changes results for low-pressure gases or high-altitude sites."),
   units=_PRESS)
_c("dlg.gauge", ("Presiones manométricas", "Gauge pressures"),
   ("Indica si las presiones se cargan y se muestran como manométricas (barg, psig).",
    "Whether pressures are entered and shown as gauge (barg, psig)."),
   ("Solo cambia la forma de mostrar y leer los valores; el cálculo usa siempre Pa absoluto.",
    "Only changes how values are shown and read; the calculation always uses Pa absolute."),
   affects=("Ningún resultado numérico.", "No numeric result."))

# --- Proceso ---------------------------------------------------------------------------------
_c("f.fluid_type", ("Tipo de fluido", "Fluid type"),
   ("Familia del fluido: líquidos, gases, vapores, vapor de agua (steam) o bifásico.",
    "Fluid family: liquids, gases, vapours, steam or two-phase."),
   ("Filtra la lista «Fluido» para que solo muestre los fluidos de ese tipo y fija la fase que "
    "se usa en el cálculo. Con propiedades automáticas el programa verifica con P y T que el "
    "fluido esté realmente en ese estado y avisa si no lo está.",
    "Filters the «Fluid» list so it only shows fluids of that type and sets the phase used in "
    "the calculation. With automatic properties the program checks with P and T that the fluid "
    "really is in that state and warns otherwise."),
   affects=("Densidad, viscosidad, Reynolds, Strouhal, criterio de Scruton (los gases de baja "
            "densidad pueden usar un límite de frecuencia más alto) y avisos de fase.",
            "Density, viscosity, Reynolds, Strouhal, Scruton criterion (low-density gases may "
            "use a higher frequency limit) and phase warnings."),
   compare=("Fase calculada por CoolProp a la presión y temperatura de operación.",
            "Phase computed by CoolProp at the operating pressure and temperature."),
   interpret=("Si aparece el aviso «el fluido está como …», el tipo elegido no coincide con "
              "las condiciones: revise el tipo, la presión o la temperatura.",
              "If the «the fluid is …» warning appears, the chosen type does not match the "
              "conditions: check the type, pressure or temperature."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-8 (los criterios de frecuencia distinguen "
              "líquidos y gases por la densidad y el número de Scruton).",
              "ASME PTC 19.3 TW-2016, para. 6-8 (frequency criteria distinguish liquids and "
              "gases by density and Scruton number)."))
_c("f.fluid", ("Fluido", "Fluid"),
   ("Sustancia que circula por la tubería. «(Estado Líquido)» o «(Estado Vapor)» indican el "
    "estado de un fluido que puede estar en más de una fase.",
    "Substance flowing in the pipe. «(Liquid state)» or «(Vapour state)» mark the state of a "
    "fluid that can be in more than one phase."),
   ("Con propiedades automáticas, CoolProp calcula ρ y μ a P y T de operación. Sin CoolProp se "
    "usan los datos de la biblioteca o los que cargue a mano.",
    "With automatic properties, CoolProp computes ρ and μ at operating P and T. Without "
    "CoolProp the library data or hand-entered values are used."),
   affects=("Velocidad (si el caudal es másico o estándar), Reynolds, Strouhal, frecuencia de "
            "estela, presiones dinámicas y todos los esfuerzos por flujo.",
            "Velocity (for mass or standard flow), Reynolds, Strouhal, wake frequency, "
            "dynamic pressures and all flow stresses."),
   actions=("Si el fluido no está en la lista, elija uno parecido y cargue ρ y μ a mano.",
            "If the fluid is not listed, pick a similar one and enter ρ and μ by hand."))
_c("f.phase_calc", ("Fase usada en el cálculo", "Phase used in the calculation"),
   ("Fase del fluido que usa el cálculo. Se deduce del tipo de fluido; con propiedades "
    "automáticas se muestra la fase que calcula CoolProp.",
    "Fluid phase used by the calculation. It follows from the fluid type; with automatic "
    "properties the phase computed by CoolProp is shown."),
   ("Decide si se aplican los criterios para gases de baja densidad y qué propiedades se "
    "toman.", "Decides whether the low-density gas criteria apply and which properties are "
    "used."),
   affects=("Límite de frecuencia y avisos.", "Frequency limit and warnings."),
   interpret=("Es un dato de solo lectura; para cambiarlo, cambie el tipo de fluido.",
              "Read-only; change the fluid type to change it."))
_c("f.p_op", ("Presión de operación", "Operating pressure"),
   ("Presión normal del proceso en el punto de instalación.",
    "Normal process pressure at the installation point."),
   ("Se usa para las propiedades del fluido (gases) y para los esfuerzos por presión que se "
    "suman a los esfuerzos de arrastre (von Mises).",
    "Used for fluid properties (gases) and for the pressure stresses added to the drag "
    "stresses (von Mises)."),
   affects=("ρ, μ, velocidad real con caudal estándar, S_r, S_t, S_a y el esfuerzo de von Mises.",
            "ρ, μ, actual velocity for standard flow, S_r, S_t, S_a and the von Mises stress."),
   limits=("No hay límite propio; la presión de diseño es la que se compara con el rating.",
           "No own limit; the design pressure is the one compared with the rating."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-11 y 6-12.", "ASME PTC 19.3 TW-2016, paras. 6-11 "
              "and 6-12."), units=_PRESS,
   formulas=(r"S_r = P", r"S_t = P\frac{1+(d/D)^2}{1-(d/D)^2}", r"S_a = \frac{P}{1-(d/D)^2}"),
   symbols=("S_r", "S_t", "S_a"))
_c("f.p_design", ("Presión de diseño", "Design pressure"),
   ("Presión máxima para la que se diseña la línea.", "Maximum pressure the line is "
                                                     "designed for."),
   ("Se compara con la presión admisible del vástago y de la punta, y con el rating de la "
    "brida a la temperatura de diseño.", "Compared with the allowable pressure of the shank "
    "and tip, and with the flange rating at design temperature."),
   affects=("Criterio «Presión admisible» y «Rating de brida».",
            "«Pressure rating» and «Flange rating» criteria."),
   limits=("Debe ser menor o igual que P_c (vástago), P_t (punta) y P_f (brida).",
           "Must be at most P_c (shank), P_t (tip) and P_f (flange)."),
   compare=("Mínimo entre P_c, P_t y P_f.", "Minimum of P_c, P_t and P_f."),
   actions=("Si no cumple: aumente la clase de brida, el espesor de punta t o la diferencia "
            "B − d, o elija un material más resistente.",
            "If it fails: raise the flange class, tip thickness t or B − d, or choose a "
            "stronger material."),
   reference=("ASME PTC 19.3 TW-2016, sección 7 (presión) y ASME B16.5 (rating de bridas).",
              "ASME PTC 19.3 TW-2016, section 7 (pressure) and ASME B16.5 (flange ratings)."),
   units=_PRESS, formulas=(r"P_c = 0.66\,S\,\left[\frac{2.167}{1+d/B}-0.0833\right]",
                           r"P_t = \frac{S}{0.13}\left(\frac{t}{d}\right)^2"),
   symbols=("P_c", "P_t", "P_r"))
_c("f.t_op", ("Temperatura de operación", "Operating temperature"),
   ("Temperatura normal del proceso.", "Normal process temperature."),
   ("Fija las propiedades del fluido y las del material (E y S a esa temperatura).",
    "Sets the fluid properties and the material properties (E and S at that temperature)."),
   affects=("ρ, μ, E, S, factor F_T, frecuencia natural y límites de fatiga.",
            "ρ, μ, E, S, F_T factor, natural frequency and fatigue limits."),
   limits=("Debe estar dentro del rango de la tabla del material; fuera de él el programa "
           "avisa.", "Must be within the material table range; outside it the program warns."),
   units=_TEMP, symbols=("F_T",))
_c("f.t_design", ("Temperatura de diseño", "Design temperature"),
   ("Temperatura máxima de diseño de la línea.", "Maximum design temperature of the line."),
   ("Se usa para S a temperatura de diseño (presión admisible) y para el rating de la brida.",
    "Used for S at design temperature (pressure rating) and the flange rating."),
   affects=("Presión admisible, rating de brida y criterio «Temperatura del material».",
            "Pressure rating, flange rating and «Material temperature» criterion."),
   limits=("No debe superar la temperatura máxima del material ni del recubrimiento.",
           "Must not exceed the maximum temperature of the material or coating."),
   units=_TEMP)
_c("f.auto_props", ("Propiedades automáticas", "Automatic properties"),
   ("Calcula densidad y viscosidad con CoolProp (o con la biblioteca) a P y T de operación.",
    "Computes density and viscosity with CoolProp (or the library) at operating P and T."),
   ("Si está marcado, ρ y μ se recalculan en cada cambio y se detecta la fase real; si no, se "
    "usan los valores que cargue.", "When checked, ρ and μ are recomputed on every change and "
    "the actual phase is detected; otherwise your values are used."),
   affects=("Todos los resultados de flujo.", "All flow results."),
   actions=("Desmárquelo solo si tiene datos de proceso más confiables (hoja de datos del "
            "proceso, mezcla especial).", "Uncheck it only if you have more reliable process "
            "data (process datasheet, special mixture)."))
_c("f.density", ("Densidad del fluido ρ", "Fluid density ρ"),
   ("Masa por unidad de volumen del fluido a las condiciones de operación.",
    "Mass per unit volume of the fluid at operating conditions."),
   ("Entra en el Reynolds, en las presiones dinámicas (arrastre y sustentación), en la masa "
    "agregada que baja la frecuencia natural, en el número de Scruton y en la velocidad "
    "erosional.", "Enters the Reynolds number, the dynamic pressures (drag and lift), the added "
    "mass that lowers the natural frequency, the Scruton number and the erosional velocity."),
   affects=("Re, N_S, P_D, P_d, P_l, H_a,f, f_n,c, N_Sc, V_e y todos los esfuerzos.",
            "Re, N_S, P_D, P_d, P_l, H_a,f, f_n,c, N_Sc, V_e and all stresses."),
   limits=("Gases con ρ bajo y N_Sc ≥ 2,5 pueden usar r < 0,8 en lugar de 0,4.",
           "Gases with low ρ and N_Sc ≥ 2.5 may use r < 0.8 instead of 0.4."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-3, 6-5 y 6-8.",
              "ASME PTC 19.3 TW-2016, paras. 6-3, 6-5 and 6-8."),
   units=("kg/m³ o lb/ft³.", "kg/m³ or lb/ft³."),
   formulas=(r"Re = \frac{\rho V B}{\mu}", r"P_D = \tfrac12 \rho C_D V^2",
             r"V_e = \frac{C}{\sqrt{\rho}}"),
   curves=("ve_rho",), symbols=("Re", "P_D", "H_af"))
_c("f.viscosity", ("Viscosidad dinámica μ", "Dynamic viscosity μ"),
   ("Resistencia del fluido a fluir, a las condiciones de operación.",
    "Fluid resistance to flow at operating conditions."),
   ("Solo entra en el número de Reynolds, que a su vez fija el Strouhal.",
    "Only enters the Reynolds number, which in turn sets the Strouhal number."),
   affects=("Re, N_S y la frecuencia de estela f_s.", "Re, N_S and the wake frequency f_s."),
   interpret=("Un error de μ cambia poco el resultado salvo cerca de los cambios de régimen del "
              "Strouhal.", "An error in μ changes little except near the Strouhal regime "
              "changes."),
   units=("cP, mPa·s o Pa·s.", "cP, mPa·s or Pa·s."),
   formulas=(r"Re = \frac{\rho V B}{\mu}",), curves=("st_re",), symbols=("Re",))
_c("f.std_density", ("Densidad estándar", "Standard density"),
   ("Densidad del gas a 15 °C y 101,325 kPa.", "Gas density at 15 °C and 101.325 kPa."),
   ("Convierte un caudal estándar (Sm³/h, MMSCFD) a caudal másico y luego a velocidad real.",
    "Converts a standard flow (Sm³/h, MMSCFD) to mass flow and then to actual velocity."),
   affects=("Velocidad de los casos dados como caudal estándar.",
            "Velocity of cases given as standard flow."),
   formulas=(r"\dot m = \rho_{std} Q_{std}", r"V = \frac{\dot m}{\rho A}"),
   units=("kg/m³ o lb/ft³.", "kg/m³ or lb/ft³."))
_c("f.prop_source", ("Fuente de las propiedades", "Property source"),
   ("De dónde salen ρ y μ: CoolProp, biblioteca o carga manual.",
    "Where ρ and μ come from: CoolProp, library or manual entry."),
   ("Se informa en la memoria para la trazabilidad.", "Reported in the memo for traceability."))
_c("f.flow_cases", ("Casos de flujo", "Flow cases"),
   ("Condiciones de caudal a verificar (mínimo, normal, máximo u otras).",
    "Flow conditions to check (minimum, normal, maximum or others)."),
   ("Cada caso se verifica por separado; el estado global es el del peor caso.",
    "Each case is checked separately; the overall status is that of the worst case."),
   affects=("Todos los resultados por caso.", "All per-case results."),
   actions=("Incluya siempre el caudal máximo; el arranque y la parada se evalúan con la opción "
            "de paso por resonancia.", "Always include the maximum flow; start-up and shutdown "
            "are evaluated with the resonance-passage option."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-1.", "ASME PTC 19.3 TW-2016, para. 6-1."))
_c("f.basis", ("Dato del caso", "Case input"),
   ("Cómo se da el caudal: velocidad, caudal másico, volumétrico real o estándar.",
    "How the flow is given: velocity, mass flow, actual or standard volume flow."),
   ("Se convierte a velocidad media en la tubería con el diámetro interno.",
    "It is converted to mean pipe velocity with the inside diameter."),
   formulas=(r"V = \frac{\dot m}{\rho\,\pi D^2/4}", r"V = \frac{Q}{\pi D^2/4}"),
   symbols=("V",))
_c("f.case", ("Caso", "Case"), ("Nombre del caso de flujo.", "Flow case name."),
   ("Identifica el caso en las tablas y gráficas.", "Identifies the case in tables and charts."))
_c("f.value", ("Valor del caso", "Case value"), ("Valor del caudal o velocidad del caso.",
                                                 "Flow or velocity value of the case."),
   ("Define la velocidad V de ese caso.", "Defines the velocity V of that case."),
   symbols=("V",))
_c("f.h2s", ("Presión parcial de H₂S", "H₂S partial pressure"),
   ("Presión parcial de sulfuro de hidrógeno en el fluido.",
    "Hydrogen sulfide partial pressure in the fluid."),
   ("Activa las recomendaciones de servicio ácido (NACE MR0175/ISO 15156) en el asistente de "
    "materiales.", "Triggers the sour-service recommendations (NACE MR0175/ISO 15156) in the "
    "material assistant."),
   affects=("Solo recomendaciones; no entra en el cálculo ASME.",
            "Recommendations only; not in the ASME calculation."),
   limits=("Por encima de 0,3 kPa (0,05 psia) se considera servicio ácido.",
           "Above 0.3 kPa (0.05 psia) the service is considered sour."), units=_PRESS)
_c("f.chlorides", ("Cloruros", "Chlorides"), ("Contenido de cloruros en ppm.",
                                              "Chloride content in ppm."),
   ("Orienta la elección de material (corrosión bajo tensión de los austeníticos).",
    "Guides material choice (stress-corrosion cracking of austenitic steels)."),
   affects=("Solo recomendaciones.", "Recommendations only."),
   limits=("Con cloruros y más de unos 60 °C, los 304/316 pueden fisurar.",
           "With chlorides above about 60 °C, 304/316 may crack."))
_c("f.ph", ("pH", "pH"), ("Acidez del fluido.", "Fluid acidity."),
   ("Orienta la elección de material.", "Guides material choice."),
   affects=("Solo recomendaciones.", "Recommendations only."))
_c("f.nace", ("Servicio ácido (NACE)", "Sour service (NACE)"),
   ("Marca el servicio como ácido según NACE MR0175/ISO 15156.",
    "Marks the service as sour per NACE MR0175/ISO 15156."),
   ("Agrega requisitos de dureza y materiales en las recomendaciones.",
    "Adds hardness and material requirements to the recommendations."),
   affects=("Solo recomendaciones.", "Recommendations only."))
_c("f.erosive", ("Sólidos o servicio erosivo", "Solids or erosive service"),
   ("Indica que el fluido arrastra sólidos o es erosivo.",
    "Indicates that the fluid carries solids or is erosive."),
   ("Agrega avisos de erosión y recomienda recubrimientos o mayor sobreespesor.",
    "Adds erosion warnings and recommends coatings or a larger allowance."),
   affects=("Avisos y estado de erosión.", "Warnings and erosion status."))

# --- Tubería ---------------------------------------------------------------------------------
_c("f.nps", ("Tamaño nominal NPS", "Nominal pipe size NPS"),
   ("Diámetro nominal de la tubería (ASME B36.10M / B36.19M).",
    "Nominal pipe diameter (ASME B36.10M / B36.19M)."),
   ("Con el schedule fija el diámetro externo, el espesor y el diámetro interno. También sugiere "
    "el tamaño de la conexión y el largo de inserción.",
    "With the schedule it sets the outside diameter, wall and inside diameter. It also "
    "suggests the connection size and insertion length."),
   affects=("Velocidad (con caudal), inserción recomendada, aviso de punta contra la pared.",
            "Velocity (from flow), recommended insertion, tip-to-wall warning."),
   actions=("Elija «Otro» para cargar OD y espesor a mano.", "Choose «Other» to enter OD and "
                                                          "wall by hand."),
   diagram="mount")
_c("f.schedule", ("Schedule", "Schedule"), ("Espesor normalizado de la tubería.",
                                            "Standardized pipe wall thickness."),
   ("Fija el espesor de pared y con él el diámetro interno. La lista se ordena de menor a "
    "mayor espesor.", "Sets the wall thickness and hence the inside diameter. The list is "
    "ordered from thinner to thicker."),
   affects=("Diámetro interno, velocidad y desglose Hs + pared + inmersión.",
            "Inside diameter, velocity and the Hs + wall + immersion breakdown."),
   reference=("ASME B36.10M (acero al carbono) y B36.19M (inoxidable, sufijo S).",
              "ASME B36.10M (carbon steel) and B36.19M (stainless, S suffix)."))
_c("f.pipe_od", ("Diámetro externo", "Outside diameter"),
   ("Diámetro exterior de la tubería.", "Pipe outside diameter."),
   ("Con NPS de tabla es de solo lectura; con «Otro» se carga y se calcula ID = OD − 2·pared.",
    "Read-only with a table NPS; with «Other» you enter it and ID = OD − 2·wall is computed."),
   formulas=(r"D_i = D_o - 2e",), units=_LEN)
_c("f.wall", ("Espesor de pared", "Wall thickness"), ("Espesor de la pared de la tubería.",
                                                      "Pipe wall thickness."),
   ("Se suma a Hs para ubicar la pared interna: U = Hs + pared + inmersión.",
    "Added to Hs to locate the inner wall: U = Hs + wall + immersion."),
   affects=("Inmersión real dentro del flujo y aviso de zona protegida.",
            "Actual immersion in the flow and shielded-zone warning."),
   formulas=(r"U = H_s + e + \text{inmersión}",), diagram="mount", units=_LEN)
_c("f.pipe_id", ("Diámetro interno", "Inside diameter"),
   ("Diámetro interior de la tubería.", "Pipe inside diameter."),
   ("Convierte caudal en velocidad y define cuánto puede entrar el termopozo sin tocar la "
    "pared opuesta.", "Converts flow to velocity and defines how far the thermowell can go "
    "without touching the opposite wall."),
   affects=("V, Re, f_s, esfuerzos, caudal volumétrico real y avisos de inserción.",
            "V, Re, f_s, stresses, actual volume flow and insertion warnings."),
   formulas=(r"V = \frac{Q}{\pi D_i^2/4}",), symbols=("V",), units=_LEN)
_c("f.orientation", ("Orientación", "Orientation"),
   ("Cómo se instala el termopozo: perpendicular a la tubería, inclinado (con su ángulo), en "
    "codo o en recipiente (sin flujo).",
    "How the thermowell is installed: perpendicular to the pipe, angled (with its angle), in "
    "an elbow or in a vessel (no flow)."),
   ("En codo con la punta hacia el flujo, la carga transversal es menor; el programa lo informa "
    "y mantiene el cálculo conservador.", "In an elbow facing the flow the transverse load is "
    "lower; the program reports it and keeps the calculation conservative."),
   affects=("Avisos e inserción recomendada.", "Warnings and recommended insertion."),
   interpret=("En recipiente la velocidad es 0: la frecuencia de estela no aplica y TS verifica "
              "presión, temperatura y esfuerzo estático. No pide NPS ni schedule, solo Hs, "
              "pared, diámetro y profundidad útil de líquido. Si hay agitador, agregue un caso "
              "con la velocidad estimada del líquido.",
              "In a vessel the velocity is 0: wake frequency does not apply and TS checks "
              "pressure, temperature and steady stress. It asks for no NPS or schedule, only "
              "Hs, wall, diameter and usable liquid depth. With an agitator, add a case with "
              "the estimated liquid velocity."),
   diagram="orientation")
_c("f.insulation", ("Espesor de aislación", "Insulation thickness"),
   ("Espesor del aislamiento térmico de la línea.", "Line thermal insulation thickness."),
   ("Sugiere el largo de lag T para que el cabezal quede fuera de la aislación.",
    "Suggests the lag length T so the head stays outside the insulation."),
   affects=("Recomendaciones de lag.", "Lag recommendations."), units=_LEN)
_c("f.mount", ("Hs, altura de la brida de montaje", "Hs, mounting flange height"),
   ("Distancia desde la superficie externa de la tubería hasta la cara de la brida de montaje "
    "(niple o conexión soldada a la línea más su brida).",
    "Distance from the pipe outer surface to the mounting flange face (nipple or connection "
    "welded to the line plus its flange)."),
   ("El programa suma el espesor de pared del schedule para obtener la distancia de la cara "
    "de la brida a la pared interna. La parte de U dentro de Hs + pared no recibe flujo.",
    "The program adds the schedule wall thickness to get the distance from the flange face "
    "to the inner wall. The part of U inside Hs + wall receives no flow."),
   affects=("Desglose de U, inmersión real, aviso de zona protegida L0 y sugerencia de L0 al "
            "aplicar un diseño.", "U breakdown, actual immersion, shielded-zone L0 warning and "
            "L0 suggestion when applying a design."),
   compare=("La planilla de referencia usa L = Hs + inserción; el programa usa U = L desde la "
            "cara de la brida. Es la misma longitud.", "The reference spreadsheet uses L = Hs "
            "+ insertion; the program uses U = L from the flange face. It is the same length."),
   interpret=("Si Hs es grande, gran parte del vástago queda sin flujo: conviene declararla "
              "como L0 para no sobreestimar la carga.", "If Hs is large, much of the shank "
              "has no flow: declare it as L0 so the load is not overestimated."),
   formulas=(r"U = H_s + e + \text{inmersión}", r"L = H_s + \text{inserción (planilla)}"),
   diagram="mount", units=_LEN)
_c("f.nozzle_id", ("Diámetro interno de la conexión de montaje",
                   "Mounting connection inside diameter"),
   ("Diámetro interno del niple o de la conexión de montaje.",
    "Inside diameter of the nipple or mounting connection."),
   ("Verifica que el termopozo (Ø A) entre con holgura.", "Checks that the thermowell (Ø A) "
                                                          "fits with clearance."),
   affects=("Solo avisos («no entra» o «holgura escasa»).", "Warnings only («does not fit» "
                                                          "or «tight clearance»)."),
   limits=("Holgura recomendada de al menos 1,5 mm por lado.",
           "Recommended clearance of at least 1.5 mm per side."), units=_LEN)

# --- Termopozo -------------------------------------------------------------------------------
_c("f.profile", ("Perfil del vástago", "Shank profile"),
   ("Forma del vástago: recto, cónico o escalonado.", "Shank shape: straight, tapered or "
                                                      "stepped."),
   ("Elige las fórmulas de frecuencia natural, de diámetro medio y del factor G de esfuerzos.",
    "Selects the natural frequency, mean diameter and stress G-factor formulas."),
   affects=("f_n, f_n,c, todos los esfuerzos y el criterio de alcance.",
            "f_n, f_n,c, all stresses and the scope criterion."),
   limits=("Rangos de aplicación de las tablas 4-1-1 (recto/cónico) y 4-2-1 (escalonado).",
           "Applicability ranges of tables 4-1-1 (straight/tapered) and 4-2-1 (stepped)."),
   interpret=PROFILE_AUTO, reference=_GEOM_REF, diagram="tw:A", table=PROFILE_TABLE,
   table_note=PROFILE_COST_NOTE)
_c("f.connection", ("Tipo de conexión", "Connection type"),
   ("Cómo se fija el termopozo al proceso: roscada, bridada, para soldar, socket weld, Van Stone "
    "o sanitaria.", "How the thermowell attaches to the process: threaded, flanged, weld-in, "
    "socket weld, Van Stone or sanitary."),
   ("Fija la rigidez del apoyo (H_c), el factor de concentración K_t y si corresponde rating "
    "de brida.", "Sets the support stiffness (H_c), the stress concentration factor K_t and "
    "whether a flange rating applies."),
   affects=("f_n,c, esfuerzo dinámico y rating de presión.", "f_n,c, dynamic stress and "
                                                             "pressure rating."),
   interpret=("Las roscadas son más flexibles (H_c menor) y tienen K_t mayor; evítelas con "
              "velocidades altas.", "Threaded ones are more flexible (lower H_c) and have a "
              "higher K_t; avoid them at high velocity."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-6 y 6-12.", "ASME PTC 19.3 TW-2016, paras. 6-6 "
                                                          "and 6-12."),
   diagram="connection", symbols=("H_c", "K_t"), table=CONNECTION_TABLE,
   table_note=CONNECTION_NOTE)
_c("f.conn_size", ("Tamaño de conexión", "Connection size"),
   ("Tamaño nominal de la rosca o brida del termopozo.", "Nominal size of the thermowell "
                                                         "thread or flange."),
   ("Se sugiere según el NPS de la línea (tabla editable). Limita el Ø A máximo posible.",
    "Suggested from the line NPS (editable table). It limits the maximum possible Ø A."),
   affects=("Hoja de datos y plano; avisos de diseño.", "Datasheet and drawing; design "
                                                        "warnings."),
   actions=("Puede cambiar la tabla de sugerencias en la carpeta de datos del usuario "
            "(tamanos_conexion.json).", "You can change the suggestion table in the user data "
            "folder (tamanos_conexion.json)."))
_c("f.rating", ("Clase ASME B16.5", "ASME B16.5 class"),
   ("Clase de presión de la brida (150 a 2500).", "Flange pressure class (150 to 2500)."),
   ("Con el grupo del material y la temperatura de diseño da la presión admisible P_f.",
    "With the material group and design temperature it gives the allowable pressure P_f."),
   affects=("Criterio «Rating de brida».", "«Flange rating» criterion."),
   compare=("Presión de diseño.", "Design pressure."),
   actions=("Si no cumple, suba la clase.", "If it fails, raise the class."),
   reference=("ASME B16.5, tablas de presión-temperatura.", "ASME B16.5 pressure-temperature "
                                                            "tables."), symbols=("P_f",))
_c("f.face", ("Cara de la brida", "Flange face"), ("RF, FF o RTJ.", "RF, FF or RTJ."),
   ("Solo para la hoja de datos.", "Datasheet only."),
   affects=("Ningún resultado numérico.", "No numeric result."))
_c("f.material", ("Material", "Material"), ("Material del termopozo.", "Thermowell material."),
   ("De la biblioteca salen ρ_m, E, S, la clase de fatiga y el grupo B16.5, interpolados a "
    "la temperatura.", "The library gives ρ_m, E, S, fatigue class and B16.5 group, "
    "interpolated to temperature."),
   affects=("f_n, límites de esfuerzo, presión admisible y rating de brida.",
            "f_n, stress limits, pressure rating and flange rating."),
   actions=("Si su material no está, use E y S manuales o agréguelo en la biblioteca.",
            "If your material is missing, use manual E and S or add it to the library."),
   reference=("ASME PTC 19.3 TW-2016, sección 7-4 y tabla 6-12.3-1 (fatiga); valores de S "
              "según ASME B31.3 / BPVC sección II-D.", "ASME PTC 19.3 TW-2016, 7-4 and table "
              "6-12.3-1 (fatigue); S values per ASME B31.3 / BPVC section II-D."),
   symbols=("S_f_adm",))
_c("f.coating", ("Recubrimiento", "Coating"), ("Recubrimiento duro de la superficie.",
                                               "Hard surface coating."),
   ("Avisa si la temperatura supera la del recubrimiento. No cambia la rigidez del cálculo.",
    "Warns if the temperature exceeds the coating limit. It does not change the calculation "
    "stiffness."),
   affects=("Avisos.", "Warnings."))
_c("f.E_manual", ("Módulo de elasticidad E (manual)", "Elastic modulus E (manual)"),
   ("Módulo de Young del material a la temperatura de operación, cargado a mano.",
    "Material Young's modulus at operating temperature, entered by hand."),
   ("Si lo carga, reemplaza el valor de la biblioteca en este tag y se anota en la memoria.",
    "If entered, it replaces the library value for this tag and is noted in the memo."),
   affects=("f_n y f_n,c (proporcional a √E), F_T y el límite de fatiga corregido.",
            "f_n and f_n,c (proportional to √E), F_T and the corrected fatigue limit."),
   limits=("Aceros: unos 190 a 210 GPa a temperatura ambiente.",
           "Steels: about 190 to 210 GPa at room temperature."),
   formulas=(r"f_a = \frac{1.875^2}{2\pi}\sqrt{\frac{EI}{m}}\,\frac{1}{L^2}",),
   units=("GPa o psi.", "GPa or psi."), symbols=("f_a", "F_T"))
_c("f.S_manual", ("Esfuerzo admisible S (manual)", "Allowable stress S (manual)"),
   ("Esfuerzo admisible del material, cargado a mano.", "Material allowable stress, entered "
                                                        "by hand."),
   ("Reemplaza S de la biblioteca a la temperatura de operación y de diseño.",
    "Replaces the library S at operating and design temperature."),
   affects=("Límite de von Mises (1,5·S), P_c y P_t.", "Von Mises limit (1.5·S), P_c and P_t."),
   formulas=(r"S_{vm} \le 1.5\,S",), units=("MPa o psi.", "MPa or psi."))

_GEOM: dict[str, tuple[Bi, Bi, Bi, tuple[str, ...], tuple[str, ...]]] = {
    "L": (("Largo no soportado L", "Unsupported length L"),
          ("Distancia del plano de apoyo a la punta: la parte del vástago que vibra como "
           "voladizo.", "Distance from the support plane to the tip: the part of the shank that "
           "vibrates as a cantilever."),
          ("Es el dato que más pesa: f_n baja con 1/L² y el momento de arrastre sube con L².",
           "The most influential input: f_n drops with 1/L² and the drag moment rises with L²."),
          (r"f_a = \frac{1.875^2}{2\pi}\sqrt{\frac{EI}{m}}\,\frac{1}{L^2}",), ("f_a", "f_n", "G")),
    "U": (("Largo de inserción U", "Insertion length U"),
          ("Largo desde la cara de la brida (o del asiento de la rosca) hasta la punta.",
           "Length from the flange face (or thread seat) to the tip."),
          ("En el programa U = L desde la cara de la brida. Se desglosa en Hs + pared + "
           "inmersión.", "In the program U = L from the flange face. It is broken down into Hs "
           "+ wall + immersion."), (r"U = H_s + e + \text{inmersión}",), ()),
    "A": (("Diámetro de raíz A", "Root diameter A"),
          ("Diámetro exterior del vástago en el apoyo.", "Shank outside diameter at the "
                                                         "support."),
          ("Aumenta la rigidez (f_n) y baja el esfuerzo en la raíz.", "Raises stiffness (f_n) "
                                                                      "and lowers root stress."),
          (r"D_a = \frac{A+B}{2}", r"I = \frac{\pi}{64}(D_a^4 - d^4)"), ("D_a", "I", "G")),
    "B": (("Diámetro de punta B", "Tip diameter B"),
          ("Diámetro exterior en la punta.", "Outside diameter at the tip."),
          ("Fija la frecuencia de estela (f_s = N_S·V/B) y el Reynolds.",
           "Sets the wake frequency (f_s = N_S·V/B) and the Reynolds number."),
          (r"f_s = \frac{N_S V}{B}", r"Re = \frac{\rho V B}{\mu}"), ("f_s", "Re")),
    "d": (("Diámetro del agujero d", "Bore diameter d"),
          ("Diámetro del agujero para el sensor.", "Bore diameter for the sensor."),
          ("Reduce la rigidez y la resistencia a la presión.", "Reduces stiffness and pressure "
                                                               "resistance."),
          (r"I = \frac{\pi}{64}(D_a^4 - d^4)", r"P_t = \frac{S}{0.13}\left(\frac{t}{d}\right)^2"),
          ("I", "P_t")),
    "t": (("Espesor de punta t", "Tip thickness t"),
          ("Espesor del fondo en la punta.", "Bottom thickness at the tip."),
          ("Entra en la presión admisible de la punta P_t.", "Enters the tip pressure rating "
                                                              "P_t."),
          (r"P_t = \frac{S}{0.13}\left(\frac{t}{d}\right)^2",), ("P_t",)),
    "b": (("Radio de acuerdo b", "Root fillet radius b"),
          ("Radio de acuerdo en la raíz del vástago.", "Fillet radius at the shank root."),
          ("Reduce la concentración de esfuerzos K_t y aumenta la rigidez del apoyo.",
           "Lowers stress concentration K_t and raises support stiffness."),
          (r"K_t = 1.1 + 0.033\,\frac{A}{b}",), ("K_t", "H_c")),
    "Ls": (("Largo del escalón Ls", "Step length Ls"),
           ("Largo de la sección de menor diámetro en un vástago escalonado.",
            "Length of the reduced section on a stepped shank."),
           ("Cambia la frecuencia natural y agrega una sección a verificar en el escalón.",
            "Changes the natural frequency and adds a section to check at the step."), (),
           ("H_f",)),
    "bs": (("Radio del escalón bs", "Step fillet bs"),
           ("Radio de acuerdo en el escalón.", "Fillet radius at the step."),
           ("Fija K_t en la sección del escalón.", "Sets K_t at the step section."), (), ()),
    "T_lag": (("Largo de lag T", "Lag length T"),
              ("Prolongación entre la brida y el cabezal, fuera del proceso.",
               "Extension between the flange and the head, outside the process."),
              ("No entra en el cálculo ASME; aleja el cabezal del calor y de la aislación.",
               "Not in the ASME calculation; keeps the head away from heat and insulation."),
              (), ()),
    "L0": (("Zona protegida L0", "Shielded length L0"),
           ("Parte del vástago, desde el apoyo, que no recibe flujo (dentro de la brida de "
            "montaje o del niple).", "Part of the shank, from the support, that receives no "
            "flow (inside the mounting flange or nipple)."),
           ("Reduce la carga de arrastre en el factor G. No cambia la frecuencia natural.",
            "Reduces the drag load in the G factor. It does not change the natural frequency."),
           (), ("G",)),
    "ca": (("Sobreespesor de corrosión", "Corrosion allowance"),
           ("Material que se espera perder por corrosión o erosión durante la vida útil.",
            "Material expected to be lost to corrosion or erosion over the service life."),
           ("Si la opción está activa, se verifica también la geometría corroída (A y B "
            "menores, d mayor).", "If the option is on, the corroded geometry is also checked "
            "(smaller A and B, larger d)."), (), ()),
}
for _k, (_title, _what, _role, _forms, _syms) in _GEOM.items():
    _c(f"f.{_k}", _title, _what, _role,
       affects=("Frecuencia natural, esfuerzos y criterio de alcance (rangos de la tabla 4-1-1 "
                "o 4-2-1).", "Natural frequency, stresses and scope criterion (ranges of table "
                             "4-1-1 or 4-2-1)."),
       reference=_GEOM_REF, units=_LEN, formulas=_forms, diagram=f"tw:{_k}",
       curves=("fn_L",) if _k == "L" else (), symbols=_syms)

# --- Sensor ----------------------------------------------------------------------------------
_c("f.sensor_type", ("Tipo de sensor", "Sensor type"),
   ("Termocupla, RTD o bimetálico.", "Thermocouple, RTD or bimetallic."),
   ("Orienta los ensayos y la tabla de colores/clases de la biblioteca.",
    "Guides the tests and the library colour/class tables."),
   affects=("Hoja de datos y plan de inspección.", "Datasheet and inspection plan."))
_c("f.sheath", ("Diámetro de vaina", "Sheath diameter"),
   ("Diámetro del sensor que entra en el agujero.", "Diameter of the sensor that goes into the "
                                                    "bore."),
   ("Se verifica la holgura con d y se estima el tiempo de respuesta.",
    "The clearance with d is checked and the response time is estimated."),
   affects=("Avisos de holgura y tiempo de respuesta.", "Clearance warnings and response "
                                                        "time."), units=_LEN)
_c("f.spring", ("Con resorte", "Spring loaded"), ("El sensor se apoya en el fondo con resorte.",
                                                  "The sensor bottoms with a spring."),
   ("Mejora el contacto térmico; solo informativo.", "Improves thermal contact; informative "
                                                     "only."))
_c("f.sensor_mass", ("Masa del sensor", "Sensor mass"), ("Masa del sensor dentro del vástago.",
                                                         "Sensor mass inside the shank."),
   ("Agrega masa y baja la frecuencia natural (factor H_a,s).",
    "Adds mass and lowers the natural frequency (H_a,s factor)."),
   affects=("f_n.", "f_n."), symbols=("H_as",), units=("kg o lb.", "kg or lb."))

# --- Opciones del cálculo --------------------------------------------------------------------
_c("opt.damping", ("Amortiguamiento ζ", "Damping ζ"),
   ("Fracción de amortiguamiento estructural del termopozo.",
    "Structural damping ratio of the thermowell."),
   ("Entra en el número de Scruton y en el factor de amplificación cerca de la resonancia.",
    "Enters the Scruton number and the magnification factor near resonance."),
   affects=("N_Sc, F_M y el límite de frecuencia aplicable.", "N_Sc, F_M and the applicable "
                                                              "frequency limit."),
   limits=("Por defecto 0,0005 (conservador). Valores mayores requieren justificación.",
           "Default 0.0005 (conservative). Higher values need justification."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-8.", "ASME PTC 19.3 TW-2016, para. 6-8."),
   formulas=(r"N_{Sc} = \frac{\pi^2}{2}\,\zeta\,\frac{\rho_m}{\rho}\left[1-\left(\frac{d}{B}"
             r"\right)^2\right]",), curves=("fm_r",), symbols=("N_Sc", "F_M"))
_c("opt.strouhal", ("Método de Strouhal", "Strouhal method"),
   ("Cómo se obtiene el número de Strouhal: correlación con Reynolds o valor fijo 0,22.",
    "How the Strouhal number is obtained: Reynolds correlation or fixed 0.22."),
   ("Fija N_S y con él la frecuencia de estela.", "Sets N_S and with it the wake frequency."),
   affects=("f_s y la relación de frecuencias.", "f_s and the frequency ratio."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-5.", "ASME PTC 19.3 TW-2016, para. 6-5."),
   curves=("st_re",), symbols=("N_S",))
_c("opt.fe", ("Factor ambiental F_E", "Environmental factor F_E"),
   ("Reducción del límite de fatiga por el ambiente (corrosión, temperatura alta).",
    "Fatigue-limit reduction for the environment (corrosion, high temperature)."),
   ("Multiplica el esfuerzo dinámico admisible.", "Multiplies the allowable dynamic stress."),
   affects=("Límite del esfuerzo dinámico.", "Dynamic stress limit."),
   limits=("Entre 0 y 1; 1 = sin reducción.", "Between 0 and 1; 1 = no reduction."),
   formulas=(r"S_{f,adm} = F_T\,F_E\,S_f",), symbols=("S_f_adm",))
_c("opt.metal_state", ("Estado del metal", "Metal condition"),
   ("Si la raíz es soldada o no soldada, para elegir el límite de fatiga.",
    "Whether the root is welded or not, to pick the fatigue limit."),
   ("Elige S_f de la tabla de fatiga; «automático» lo deduce de la conexión.",
    "Picks S_f from the fatigue table; «automatic» infers it from the connection."),
   affects=("Esfuerzo dinámico admisible.", "Allowable dynamic stress."),
   reference=("ASME PTC 19.3 TW-2016, tabla 6-12.3-1.", "ASME PTC 19.3 TW-2016, table "
                                                        "6-12.3-1."))
_c("opt.amber", ("Margen amarillo", "Amber margin"),
   ("Margen porcentual debajo del límite a partir del cual el estado pasa a amarillo.",
    "Percent margin below the limit from which the status turns amber."),
   ("Solo cambia el color; un amarillo sigue cumpliendo.", "Only changes the colour; an amber "
                                                           "result still passes."),
   limits=("Por defecto 10 %.", "Default 10 %."))
_c("opt.flange_manual", ("Rating de brida manual", "Manual flange rating"),
   ("Presión admisible de la brida cargada a mano.", "Flange allowable pressure entered by "
                                                     "hand."),
   ("Reemplaza el valor de la tabla B16.5 de la biblioteca.", "Replaces the library B16.5 "
                                                              "value."),
   affects=("Criterio «Rating de brida».", "«Flange rating» criterion."), units=_PRESS)
_c("opt.inline", ("Paso por resonancia en línea", "In-line resonance passage"),
   ("Permite que el arranque o la parada pasen por la resonancia en línea (solo gases).",
    "Allows start-up or shutdown to pass through in-line resonance (gases only)."),
   ("Aplica el criterio de permanencia en la banda de resonancia en lugar de prohibirla.",
    "Applies the lock-in dwell criterion instead of forbidding the band."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-8.5.", "ASME PTC 19.3 TW-2016, para. 6-8.5."),
   symbols=("V_IR",))
_c("opt.corrosion_cases", ("Casos con corrosión", "Corrosion cases"),
   ("Evalúa también la geometría con el sobreespesor consumido.",
    "Also evaluates the geometry with the allowance consumed."),
   ("Agrega casos con A y B menores y d mayor.", "Adds cases with smaller A and B and larger "
                                                 "d."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-2.", "ASME PTC 19.3 TW-2016, para. 6-2."))
_c("opt.supplier", ("Rating de proveedor", "Supplier rating"),
   ("Calcula sin la masa agregada del fluido (H_a,f = 1), como un rating genérico.",
    "Calculates without fluid added mass (H_a,f = 1), as a generic rating."),
   ("Útil para catálogos; para un servicio real déjelo desmarcado.",
    "Useful for catalogues; leave unchecked for a real service."),
   reference=("ASME PTC 19.3 TW-2016, sección 9.", "ASME PTC 19.3 TW-2016, section 9."))

# --- Resultados calculados -------------------------------------------------------------------
_RES_REF = ("ASME PTC 19.3 TW-2016, sección 6.", "ASME PTC 19.3 TW-2016, section 6.")
_c("r.q_actual", ("Caudal volumétrico real", "Actual volumetric flow"),
   ("Caudal a las condiciones de operación (no estándar).", "Flow at operating conditions (not "
                                                            "standard)."),
   ("Se calcula con la velocidad del caso y el área interna de la tubería.",
    "Computed from the case velocity and the pipe inside area."),
   compare=("La planilla lo obtiene corrigiendo SCFM por P y T; el programa usa la densidad real.",
            "The spreadsheet corrects SCFM for P and T; the program uses the actual density."),
   formulas=(r"Q = V\,\frac{\pi D_i^2}{4}",), units=("m³/h o ft³/min (ACFM).",
                                                     "m³/h or ft³/min (ACFM)."))
_c("r.velocity", ("Velocidad del fluido V", "Fluid velocity V"),
   ("Velocidad media del fluido en la tubería.", "Mean fluid velocity in the pipe."),
   ("Es la entrada principal de la verificación: fija Re, f_s y las presiones dinámicas.",
    "The main input of the check: it sets Re, f_s and the dynamic pressures."),
   affects=("Todo el cálculo de flujo.", "The whole flow calculation."),
   interpret=("Con la curva f_s vs. V se ve qué velocidad lleva al límite.",
              "The f_s vs V curve shows which velocity reaches the limit."),
   reference=_RES_REF, formulas=(r"V = \frac{\dot m}{\rho\,\pi D_i^2/4}",),
   curves=("fs_v",), symbols=("V",), units=("m/s o ft/s.", "m/s or ft/s."))
_c("r.ve", ("Velocidad erosional V_e", "Erosional velocity V_e"),
   ("Velocidad a partir de la cual el flujo puede erosionar el metal (criterio orientativo de "
    "API RP 14E).", "Velocity above which the flow may erode metal (guidance criterion from API "
    "RP 14E)."),
   ("Se compara con V para el estado de erosión; no es parte de PTC 19.3.",
    "Compared with V for the erosion status; not part of PTC 19.3."),
   limits=("C = 100 (servicio continuo sin sólidos).", "C = 100 (continuous service without "
                                                       "solids)."),
   formulas=(r"V_e = \frac{C}{\sqrt{\rho}}\quad(\rho\ \mathrm{en\ lb/ft^3},\ V_e\ \mathrm{en"
             r"\ ft/s})",),
   reference=("API RP 14E, §2.5 (resumen).", "API RP 14E, §2.5 (summary)."),
   curves=("ve_rho",), units=("m/s o ft/s.", "m/s or ft/s."))
_c("r.v_ve", ("Relación V/V_e", "Velocity ratio V/V_e"),
   ("Cociente entre la velocidad y la velocidad erosional.", "Ratio of velocity to erosional "
                                                             "velocity."),
   ("Da el estado de erosión: no erosivo, vigilar o erosivo.", "Gives the erosion status: "
                                                               "non-erosive, monitor or erosive."),
   limits=("< 0,7 no erosivo; 0,7 a 1 vigilar; ≥ 1 erosivo.", "< 0.7 non-erosive; 0.7 to 1 "
                                                              "monitor; ≥ 1 erosive."),
   actions=("Si es erosivo: reduzca la velocidad, use un material más duro o un recubrimiento "
            "(Stellite) y programe inspecciones.", "If erosive: reduce velocity, use a harder "
            "material or a coating (Stellite) and schedule inspections."),
   curves=("ve_rho",))
_c("r.reynolds", ("Número de Reynolds Re", "Reynolds number Re"),
   ("Relación entre fuerzas de inercia y viscosas, con B como longitud.",
    "Ratio of inertial to viscous forces, with B as length."),
   ("Fija el número de Strouhal por la correlación.", "Sets the Strouhal number through the "
                                                      "correlation."),
   limits=("Por debajo de Re = 22 no hay desprendimiento de vórtices.",
           "Below Re = 22 there is no vortex shedding."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-3 y 6-5.", "ASME PTC 19.3 TW-2016, paras. 6-3 "
                                                         "and 6-5."),
   formulas=(r"Re = \frac{\rho V B}{\mu}",), curves=("st_re",), symbols=("Re",),
   units=("Adimensional.", "Dimensionless."))
_c("r.strouhal", ("Número de Strouhal N_S", "Strouhal number N_S"),
   ("Frecuencia adimensional de desprendimiento de vórtices.", "Dimensionless vortex shedding "
                                                               "frequency."),
   ("Multiplica V/B para dar la frecuencia de estela.", "Multiplies V/B to give the wake "
                                                        "frequency."),
   limits=("Entre 0,17 y 0,22 en el rango usual.", "Between 0.17 and 0.22 in the usual range."),
   compare=("La planilla usa 0,22 fijo hasta Re = 5·10⁵; el programa usa la correlación completa.",
            "The spreadsheet uses a fixed 0.22 up to Re = 5·10⁵; the program uses the full "
            "correlation."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-5.", "ASME PTC 19.3 TW-2016, para. 6-5."),
   curves=("st_re",), symbols=("N_S",), units=("Adimensional.", "Dimensionless."))
_c("r.fs", ("Frecuencia de estela f_s", "Wake frequency f_s"),
   ("Frecuencia con que se desprenden los vórtices detrás del termopozo.",
    "Frequency at which vortices shed behind the thermowell."),
   ("Se compara con la frecuencia natural instalada.", "Compared with the installed natural "
                                                       "frequency."),
   limits=("f_s < 0,8·f_n,c (o < 0,4·f_n,c si no se cumplen las condiciones de Scruton).",
           "f_s < 0.8·f_n,c (or < 0.4·f_n,c if the Scruton conditions are not met)."),
   compare=("f_n,c.", "f_n,c."),
   actions=("Si no cumple: acorte L, aumente A o B, o cambie a escalonado.",
            "If it fails: shorten L, increase A or B, or switch to stepped."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-5 y 6-8.", "ASME PTC 19.3 TW-2016, paras. 6-5 "
                                                         "and 6-8."),
   formulas=(r"f_s = \frac{N_S V}{B}",), curves=("fs_v",), symbols=("f_s",),
   units=("Hz.", "Hz."))
_c("r.fn", ("Frecuencia natural f_n", "Natural frequency f_n"),
   ("Primera frecuencia propia del termopozo con apoyo ideal.", "First natural frequency of "
                                                                "the thermowell on an ideal "
                                                                "support."),
   ("Se corrige por masa del fluido y del sensor; luego por la flexibilidad del apoyo.",
    "Corrected for fluid and sensor mass; then for support flexibility."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-6.", "ASME PTC 19.3 TW-2016, para. 6-6."),
   formulas=(r"f_n = H_f\,H_{a,f}\,H_{a,s}\,f_a",), curves=("fn_L",), symbols=("f_a", "f_n"),
   units=("Hz.", "Hz."))
_c("r.hc", ("Factor de apoyo H_c", "Support factor H_c"),
   ("Corrección de la frecuencia por la flexibilidad del apoyo.", "Frequency correction for "
                                                                  "support flexibility."),
   ("Multiplica f_n para dar f_n,c.", "Multiplies f_n to give f_n,c."),
   limits=("Menor que 1; las roscadas usan 0,9 o menos.", "Below 1; threaded ones use 0.9 or "
                                                          "less."),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-7.", "ASME PTC 19.3 TW-2016, para. 6-7."),
   symbols=("H_c",))
_c("r.fnc", ("Frecuencia natural instalada f_n,c", "Installed natural frequency f_n,c"),
   ("Frecuencia propia del termopozo ya montado, con la flexibilidad del apoyo.",
    "Natural frequency of the mounted thermowell, including support flexibility."),
   ("Es la referencia del límite de frecuencia.", "The reference for the frequency limit."),
   compare=("La planilla usa 500/L² (aproximación); el programa aplica la sección 6-6 y 6-7 "
            "completas.", "The spreadsheet uses 500/L² (approximation); the program applies "
            "sections 6-6 and 6-7 in full."),
   formulas=(r"f_{n,c} = H_c\,f_n",), curves=("fn_L", "fs_v"), symbols=("f_nc",),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-7.", "ASME PTC 19.3 TW-2016, para. 6-7."),
   units=("Hz.", "Hz."))
_c("r.scruton", ("Número de Scruton N_Sc", "Scruton number N_Sc"),
   ("Mide cuánto amortiguamiento y masa tiene el termopozo frente al fluido.",
    "Measures how much damping and mass the thermowell has relative to the fluid."),
   ("Decide si se puede usar el límite 0,8 (N_Sc ≥ 2,5) y si se suprimen las vibraciones "
    "(N_Sc > 64).", "Decides whether the 0.8 limit applies (N_Sc ≥ 2.5) and whether vibration "
    "is suppressed (N_Sc > 64)."),
   limits=("2,5 y 64.", "2.5 and 64."),
   formulas=(r"N_{Sc} = \frac{\pi^2}{2}\,\zeta\,\frac{\rho_m}{\rho}\left[1-\left(\frac{d}{B}"
             r"\right)^2\right]",), symbols=("N_Sc",),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-8.", "ASME PTC 19.3 TW-2016, para. 6-8."))
_c("r.ratio", ("Relación de frecuencias r", "Frequency ratio r"),
   ("Cociente f_s/f_n,c.", "Ratio f_s/f_n,c."),
   ("Es el criterio de frecuencia de estela del estado ASME.", "It is the wake-frequency "
                                                                "criterion of the ASME status."),
   limits=("r < 0,8 con N_Sc ≥ 2,5 y condiciones de esfuerzo en línea; si no, r < 0,4.",
           "r < 0.8 with N_Sc ≥ 2.5 and in-line stress conditions; otherwise r < 0.4."),
   interpret=("Cerca de 1 hay resonancia transversal; cerca de 0,5 resonancia en línea.",
              "Near 1 there is transverse resonance; near 0.5 in-line resonance."),
   actions=("Si hay riesgo de resonancia: acorte L, aumente A o B, o use un collar de apoyo.",
            "If there is resonance risk: shorten L, increase A or B, or use a support collar."),
   formulas=(r"r = \frac{f_s}{f_{n,c}}", r"F_M = \frac{1}{1-r^2}"), curves=("fm_r", "fs_v"),
   symbols=("r", "F_M"), reference=("ASME PTC 19.3 TW-2016, párr. 6-8 y 6-9.",
                                    "ASME PTC 19.3 TW-2016, paras. 6-8 and 6-9."))
_c("r.steady", ("Esfuerzo estacionario S_max", "Steady stress S_max"),
   ("Suma del esfuerzo de flexión por arrastre y el axial por presión en la raíz.",
    "Sum of drag bending stress and axial pressure stress at the root."),
   ("Entra en el esfuerzo de von Mises.", "Enters the von Mises stress."),
   formulas=(r"S_D = G\,P_D", r"S_{max} = S_D + S_a"), curves=("steady_v",),
   symbols=("S_D", "S_max"), reference=("ASME PTC 19.3 TW-2016, párr. 6-10 y 6-12.",
                                        "ASME PTC 19.3 TW-2016, paras. 6-10 and 6-12."),
   units=("MPa o psi.", "MPa or psi."))
_c("r.dynamic", ("Esfuerzo dinámico S_o", "Dynamic stress S_o"),
   ("Pico de esfuerzo oscilante en la raíz por arrastre y sustentación oscilantes, con "
    "amplificación y concentración de esfuerzos.", "Peak oscillating stress at the root from "
    "oscillating drag and lift, with magnification and stress concentration."),
   ("Se compara con el límite de fatiga corregido.", "Compared with the corrected fatigue "
                                                     "limit."),
   limits=("S_o ≤ F_T·F_E·S_f.", "S_o ≤ F_T·F_E·S_f."),
   actions=("Si no cumple: baje r (más rigidez), aumente el radio b o elija un material con "
            "mayor límite de fatiga.", "If it fails: lower r (more stiffness), increase the "
            "fillet b or choose a material with a higher fatigue limit."),
   formulas=(r"S_{o} = K_t\sqrt{S_d^2 + S_L^2}", r"S_L = G\,F_M\,P_l"),
   curves=("stress_v",), symbols=("S_o", "S_d", "S_L", "S_f_adm"),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-10 y 6-12.", "ASME PTC 19.3 TW-2016, paras. 6-10 "
                                                           "and 6-12."),
   units=("MPa o psi.", "MPa or psi."))
_c("r.von_mises", ("Esfuerzo de von Mises S_vm", "Von Mises stress S_vm"),
   ("Esfuerzo equivalente que combina S_max con los esfuerzos radial y tangencial de presión.",
    "Equivalent stress combining S_max with the radial and tangential pressure stresses."),
   ("Se compara con 1,5 veces el esfuerzo admisible S.", "Compared with 1.5 times the "
                                                         "allowable stress S."),
   limits=("S_vm ≤ 1,5·S.", "S_vm ≤ 1.5·S."),
   compare=("La planilla combina estacionario y dinámico en una sola raíz; el programa los "
            "verifica por separado como pide la norma.", "The spreadsheet combines steady and "
            "dynamic in one root; the program checks them separately as the standard requires."),
   formulas=(r"S_{vm} = \sqrt{\tfrac12[(S_{max}-S_r)^2+(S_{max}-S_t)^2+(S_t-S_r)^2]}",),
   curves=("steady_v",), symbols=("S_vm",),
   reference=("ASME PTC 19.3 TW-2016, párr. 6-12.", "ASME PTC 19.3 TW-2016, para. 6-12."),
   units=("MPa o psi.", "MPa or psi."))
_c("r.v_ir", ("Velocidad de resonancia en línea V_IR", "In-line resonance velocity V_IR"),
   ("Velocidad a la que la frecuencia de estela vale la mitad de f_n,c.",
    "Velocity at which the wake frequency equals half of f_n,c."),
   ("Se usa para el criterio de paso por resonancia en línea.", "Used for the in-line "
                                                                 "resonance passage criterion."),
   formulas=(r"V_{IR} = \frac{B f_{n,c}}{2 N_S}",), symbols=("V_IR",), units=("m/s.", "m/s."))

# --- Selección automática por bloque ----------------------------------------------------------
_AUTO_ROLE = ("En «Automático» el programa completa el bloque al calcular, a partir de la "
              "biblioteca y de los resultados, y deja la justificación en pantalla («Resumen "
              "ASME»), en la hoja de datos y en la memoria («Selección automática y "
              "justificación»). En «Manual» se usan los datos que usted cargue.",
              "In «Automatic» the program fills the block on calculation from the library and "
              "the results, and records the rationale on screen («ASME summary»), in the "
              "datasheet and in the memo («Automatic selection and rationale»). In «Manual» your "
              "own data are used.")
_AUTO_ACT = ("Las recomendaciones son orientativas y deben ser revisadas por un ingeniero "
             "calificado. Para fijar un valor, vuelva el bloque a «Manual»: el editor conserva lo "
             "último calculado.", "Recommendations are guidance and must be reviewed by a "
             "qualified engineer. To fix a value, switch the block back to «Manual»: the editor "
             "keeps the last computed values.")
_AUTO_IN = ("Siempre los carga usted: condiciones de proceso (P y T de operación y diseño), "
            "tipo de fluido y fluido, casos de flujo, H₂S, cloruros, pH y sólidos si aplican, "
            "NPS, schedule, Hs y diámetro interno de la conexión de montaje.",
            "You always enter: process conditions (operating and design P and T), fluid type "
            "and fluid, flow cases, H₂S, chlorides, pH and solids if they apply, NPS, schedule, "
            "Hs and mounting connection inside diameter.")
_c("f.mode_material", ("Modo: material y protecciones", "Mode: material and protections"),
   ("Elige si el material, el recubrimiento y el sobreespesor de corrosión los carga usted o los "
    "recomienda el programa.", "Chooses whether material, coating and corrosion allowance are "
    "entered by you or recommended by the program."), _AUTO_ROLE,
   affects=("Material (ρ_m, E, S, fatiga, grupo B16.5), recubrimiento y ca; por lo tanto f_n, "
            "esfuerzos admisibles y rating.", "Material (ρ_m, E, S, fatigue, B16.5 group), "
            "coating and ca; hence f_n, allowable stresses and rating."),
   compare=("Material: matriz de selección de la biblioteca a la temperatura de diseño con H₂S, "
            "cloruros, pH y sólidos; entre aptos se prefiere 316/316L y se listan alternativas. "
            "Recubrimiento: recargue duro si hay sólidos o V/V_e ≥ 0,7. Sobreespesor: 1 mm en "
            "servicio agresivo.", "Material: library selection matrix at design temperature "
            "with H₂S, chlorides, pH and solids; among suitable ones 316/316L is preferred and "
            "alternatives are listed. Coating: hard-facing with solids or V/V_e ≥ 0.7. "
            "Allowance: 1 mm in aggressive service."),
   limits=_AUTO_IN, actions=_AUTO_ACT,
   reference=("Criterios de práctica (NACE MR0175/ISO 15156 para H₂S, API RP 14E para erosión) "
              "resumidos en la biblioteca.", "Practice criteria (NACE MR0175/ISO 15156 for H₂S, "
              "API RP 14E for erosion) summarised in the library."))
_c("f.mode_connection", ("Modo: conexión", "Mode: connection"),
   ("Elige si el tipo, el tamaño, la clase y la cara de la conexión los carga usted o los "
    "recomienda el programa.", "Chooses whether connection type, size, class and face are "
    "entered by you or recommended by the program."), _AUTO_ROLE,
   affects=("Rating de brida, diseño típico disponible y hoja de datos.",
            "Flange rating, available typical designs and datasheet."),
   compare=("Roscada solo en utilidades no peligrosas (agua, aire, nitrógeno) ≤ 20 barg y "
            "≤ 200 °C; soldada desde clase 1500; en el resto, bridada. Clase: la menor de "
            "ASME B16.5 que admite la presión de diseño a la temperatura de diseño para el "
            "grupo del material. Cara: RF hasta clase 600 y RTJ desde 900. Tamaño: tabla de "
            "tamaños sugeridos por NPS (editable).", "Threaded only for non-hazardous utilities "
            "(water, air, nitrogen) ≤ 20 barg and ≤ 200 °C; weld-in from class 1500; otherwise "
            "flanged. Class: the smallest ASME B16.5 class that holds the design pressure at "
            "design temperature for the material group. Face: RF up to class 600 and RTJ from "
            "900. Size: suggested-size table by NPS (editable)."),
   limits=_AUTO_IN, actions=_AUTO_ACT,
   reference=("ASME B16.5 (rating por grupo de material); práctica habitual de especificaciones "
              "de cañería.", "ASME B16.5 (rating by material group); common piping-spec "
              "practice."))
_c("f.mode_geometry", ("Modo: geometría", "Mode: geometry"),
   ("Elige si el perfil y las cotas U, A, B, d, L0 los carga usted o los busca el programa "
    "iterando con la verificación ASME.", "Chooses whether profile and dimensions U, A, B, d, "
    "L0 are entered by you or searched by the program iterating with the ASME check."),
   _AUTO_ROLE,
   affects=("Todos los resultados de frecuencia y esfuerzos.",
            "All frequency and stress results."),
   compare=("Se parte del U normalizado que deja la punta al menos 1/3 del diámetro (o 100 mm) "
            "dentro del flujo; se prueban diseños típicos cónicos, luego escalonados y rectos, "
            "con agujero 0,260\" o 0,385\", que entren en la conexión de montaje; si ninguno "
            "cumple se prueban largos más cortos. Se elige el primero que cumple; si ninguno, "
            "el de mejor margen y se avisa.", "Starting from the standard U that puts the tip "
            "at least 1/3 of the diameter (or 100 mm) into the flow, tapered typical designs "
            "are tried, then stepped and straight, with 0.260\" or 0.385\" bore, that fit the "
            "mounting connection; if none passes shorter lengths are tried. The first passing "
            "one is chosen; if none, the best-margin one with a warning."),
   limits=_AUTO_IN, actions=_AUTO_ACT, reference=_GEOM_REF, diagram="tw:U")
_c("f.mode_sensor", ("Modo: vaina del sensor", "Mode: sensor sheath"),
   ("Elige si el diámetro de vaina lo carga usted o lo elige el programa según el agujero.",
    "Chooses whether the sheath diameter is entered by you or chosen by the program from the "
    "bore."), _AUTO_ROLE,
   affects=("Solo la hoja de datos y el huelgo sensor–agujero.",
            "Only the datasheet and the sensor–bore clearance."),
   compare=("La vaina normalizada más gruesa (3, 4,5, 6 mm, 1/4\", 8 mm o 3/8\") que deja un "
            "huelgo de 0,25 a 1,5 mm: 6,35 mm (1/4\") para 0,260\" y 9,5 mm (3/8\") para "
            "0,385\", con sensor a resorte.", "The thickest standard sheath (3, 4.5, 6 mm, 1/4\", "
            "8 mm or 3/8\") leaving 0.25 to 1.5 mm clearance: 6.35 mm (1/4\") for 0.260\" and "
            "9.5 mm (3/8\") for 0.385\", spring-loaded."), actions=_AUTO_ACT)
_c("topic.auto", ("Selección automática y justificación", "Automatic selection and rationale"),
   ("Lista de los valores que completó el programa en los bloques en «Automático», con su "
    "justificación y alternativas.", "List of the values the program filled in the blocks set "
    "to «Automatic», with rationale and alternatives."), _AUTO_ROLE, actions=_AUTO_ACT)

# --- Estado ASME por tema y criterios --------------------------------------------------------
_c("topic.erosion", ("Evaluación de erosión", "Erosion evaluation"),
   ("Veredicto de erosión con la relación V/V_e del peor caso.", "Erosion verdict with the "
                                                                 "worst-case V/V_e ratio."),
   ("No erosivo, vigilar o erosivo. Es orientativo (API RP 14E), fuera de PTC 19.3; un "
    "resultado erosivo pide revisión de ingeniería.", "Non-erosive, monitor or erosive. "
    "Guidance only (API RP 14E), outside PTC 19.3; an erosive result calls for engineering "
    "review."), limits=("0,7 y 1,0.", "0.7 and 1.0."), curves=("ve_rho",))
_c("topic.frequency", ("Frecuencia de estela", "Wake frequency"),
   ("Veredicto del límite de frecuencia y del paso por resonancia.",
    "Verdict of the frequency limit and resonance passage."),
   ("Cumple o riesgo de resonancia.", "Pass or resonance risk."), curves=("fs_v",))
_c("topic.stress", ("Esfuerzos", "Stresses"),
   ("Veredicto de los esfuerzos estacionario (von Mises) y dinámico (fatiga).",
    "Verdict of steady (von Mises) and dynamic (fatigue) stresses."),
   ("Cumple, cumple con margen bajo o no cumple.", "Pass, pass with low margin or fail."),
   curves=("stress_v", "steady_v"))
_c("topic.pressure", ("Presión y rating", "Pressure and rating"),
   ("Veredicto de la presión admisible, el rating de brida y la temperatura del material.",
    "Verdict of pressure rating, flange rating and material temperature."),
   ("Cumple o no cumple.", "Pass or fail."))
_c("topic.overall", ("Estado ASME global", "Overall ASME status"),
   ("Resumen de todos los temas.", "Summary of all topics."),
   ("Cumple si todo cumple; requiere revisión de ingeniería si hay márgenes bajos, erosión o "
    "avisos críticos; no cumple si falla algún criterio de la norma.",
    "Pass if everything passes; requires engineering review with low margins, erosion or "
    "critical warnings; fail if any criterion of the standard fails."))
_CRIT = {
    "scope": (("Alcance de la norma", "Scope of the standard"),
              ("Verifica que la geometría esté dentro de los rangos de la norma.",
               "Checks that the geometry is within the standard's ranges.")),
    "material_temperature": (("Temperatura del material", "Material temperature"),
                             ("Verifica que la temperatura de diseño esté dentro del rango del "
                              "material.", "Checks that the design temperature is within the "
                                           "material range.")),
    "pressure_rating": (("Presión admisible", "Pressure rating"),
                        ("Compara la presión de diseño con P_c y P_t.", "Compares design "
                                                                        "pressure with P_c and "
                                                                        "P_t.")),
    "flange_rating": (("Rating de brida", "Flange rating"),
                      ("Compara la presión de diseño con la de la brida B16.5.",
                       "Compares design pressure with the B16.5 flange pressure.")),
    "steady_stress": (("Esfuerzo estacionario", "Steady stress"),
                      ("Compara S_vm con 1,5·S.", "Compares S_vm with 1.5·S.")),
    "dynamic_stress": (("Esfuerzo dinámico", "Dynamic stress"),
                       ("Compara S_o con el límite de fatiga corregido.",
                        "Compares S_o with the corrected fatigue limit.")),
    "frequency_limit": (("Límite de frecuencia", "Frequency limit"),
                        ("Compara f_s con 0,4 u 0,8 veces f_n,c.", "Compares f_s with 0.4 or "
                                                                   "0.8 times f_n,c.")),
    "inline_lockin_dwell": (("Paso por resonancia en línea", "In-line resonance passage"),
                            ("Verifica el esfuerzo durante el paso por la banda de resonancia "
                             "en línea.", "Checks the stress while passing through the in-line "
                                          "resonance band.")),
    "fatigue_data": (("Datos de fatiga", "Fatigue data"),
                     ("Indica si el material tiene datos de fatiga en la norma.",
                      "Indicates whether the material has fatigue data in the standard.")),
}
_CRIT_LINK = {"steady_stress": "r.von_mises", "dynamic_stress": "r.dynamic",
              "frequency_limit": "r.ratio", "pressure_rating": "f.p_design",
              "flange_rating": "f.rating"}
for _k, (_title, _what) in _CRIT.items():
    base = CARDS.get(_CRIT_LINK.get(_k, ""))
    _c(f"crit.{_k}", _title, _what,
       ("Es uno de los criterios de la tabla de resultados; el estado global es el del peor "
        "criterio.", "One of the criteria in the results table; the overall status is that of "
                     "the worst criterion."),
       limits=base.limits if base else _NO, actions=base.actions if base else _NO,
       reference=base.reference if base else _RES_REF,
       formulas=base.formulas if base else (), curves=base.curves if base else (),
       symbols=base.symbols if base else ())

# --- Guías por tipo de conexión y perfil (biblioteca) ---------------------------------------
_CONN_WHAT: Final[dict[str, Bi]] = {
    "threaded": ("Termopozo con rosca macho (NPT cónica o G cilíndrica ISO 228) que se enrosca "
                 "en una cupla o niple de la línea.",
                 "Thermowell with a male thread (tapered NPT or parallel G ISO 228) screwed into "
                 "a coupling or nipple on the line."),
    "flanged": ("Termopozo soldado o maquinado con una brida que se abulona a la brida de "
                "montaje de la línea.",
                "Thermowell welded or machined with a flange bolted to the line mounting "
                "flange."),
    "socket_weld": ("Termopozo que se inserta en un socket y se suelda con un filete exterior.",
                    "Thermowell inserted into a socket and welded with an outside fillet."),
    "weld_in": ("Termopozo soldado directamente a la tubería o a un sockolet, sin brida.",
                "Thermowell welded directly to the pipe or to a sockolet, without a flange."),
    "van_stone": ("Termopozo de una sola pieza con un collar solapado que queda apretado por una "
                  "brida loca.",
                  "One-piece thermowell with a lapped collar clamped by a loose flange."),
    "sanitary": ("Termopozo con conexión tipo clamp (abrazadera y junta) y superficies pulidas.",
                 "Thermowell with a clamp connection (clamp and gasket) and polished surfaces."),
}
for _key, _row in CONNECTION_ROWS.items():
    _r = CONNECTION_TABLE[_row]
    _c(f"conn.{_key}", (f"Conexión: {_r[0][0]}", f"Connection: {_r[0][1]}"), _CONN_WHAT[_key],
       ("Define la rigidez del apoyo, el K_t de esfuerzos y si aplica rating de brida; la tabla "
        "resume dónde conviene y dónde no.", "It defines support stiffness, the stress K_t and "
        "whether a flange rating applies; the table summarizes where it fits and where not."),
       limits=(_r[2][0], _r[2][1]), interpret=(_r[1][0], _r[1][1]),
       table=CONNECTION_TABLE, highlight=_row, table_note=CONNECTION_NOTE, diagram="connection")

_PROFILE_WHAT: Final[dict[str, Bi]] = {
    "tapered": ("Vástago que se afina linealmente desde la raíz A hasta la punta B.",
                "Shank that tapers linearly from the root A to the tip B."),
    "stepped": ("Vástago con dos diámetros: A en la raíz y B en la punta, unidos por un escalón.",
                "Shank with two diameters: A at the root and B at the tip, joined by a step."),
    "straight": ("Vástago de diámetro constante (A = B).",
                 "Constant-diameter shank (A = B)."),
}
for _key, _row in PROFILE_ROWS.items():
    _r = PROFILE_TABLE[_row]
    _c(f"profile.{_key}", (f"Perfil: {_r[0][0]}", f"Profile: {_r[0][1]}"), _PROFILE_WHAT[_key],
       ("Elige las fórmulas de frecuencia natural, diámetro medio y factor G de esfuerzos.",
        "Selects the natural frequency, mean diameter and stress G-factor formulas."),
       interpret=(_r[1][0], _r[1][1]), limits=(_r[2][0], _r[2][1]),
       compare=(f"Costo relativo {_r[3][0]} (recto = 1,0). {_r[4][0]}",
                f"Relative cost {_r[3][1]} (straight = 1.0). {_r[4][1]}"),
       actions=PROFILE_AUTO, reference=_GEOM_REF, table=PROFILE_TABLE, highlight=_row,
       table_note=PROFILE_COST_NOTE, diagram="tw:A")

# --- Montaje en recipiente, ángulo y rosca ----------------------------------------------------
_c("f.mount_angle", ("Ángulo de montaje", "Mounting angle"),
   ("Ángulo entre el termopozo y el eje de la tubería cuando el montaje es inclinado (90° = "
    "perpendicular, 45° = típico a contraflujo).",
    "Angle between the thermowell and the pipe axis for an angled mounting (90° = "
    "perpendicular, 45° = typical against the flow)."),
   ("Proyecta la parte expuesta sobre el radio de la tubería: la profundidad real es "
    "inmersión × sen(ángulo). Con eso TS verifica que la punta no toque la pared opuesta y "
    "elige U en automático.",
    "Projects the exposed length onto the pipe radius: the actual depth is immersion × "
    "sin(angle). TS uses it to check the tip does not touch the opposite wall and to choose "
    "U in automatic mode."),
   affects=("Aviso de posición de la punta, largo U automático y hoja de datos («Inclinado "
            "45°»).", "Tip position warning, automatic U length and datasheet (\"Angled "
            "45°\")."),
   limits=("Entre 5° y 90°. El cálculo ASME se hace con la velocidad normal al vástago, que "
           "es conservador.", "Between 5° and 90°. The ASME check uses the velocity normal "
           "to the shank, which is conservative."))
_c("f.liquid_depth", ("Profundidad útil de líquido", "Usable liquid depth"),
   ("En un recipiente o tanque, profundidad mínima de líquido por debajo de la conexión que "
    "el termopozo puede aprovechar (nivel mínimo de operación).",
    "In a vessel or tank, minimum liquid depth below the connection that the thermowell can "
    "use (minimum operating level)."),
   ("Limita la posición de la punta junto con el diámetro del recipiente: TS toma el menor de "
    "los dos como recorrido disponible.",
    "Limits the tip position together with the vessel diameter: TS takes the smaller of the "
    "two as the available travel."),
   affects=("Aviso de posición de la punta y largo U automático.",
            "Tip position warning and automatic U length."),
   interpret=("Para medir bien, la punta debe quedar sumergida aun con nivel bajo; TS busca "
              "una inmersión de al menos 450 mm en recipientes, como sugiere la tabla de "
              "instalación de la biblioteca.",
              "For a good reading the tip must stay submerged even at low level; TS looks for "
              "an immersion of at least 450 mm in vessels, as the library installation table "
              "suggests."), units=_LEN)
_c("f.thread", ("Tipo de rosca", "Thread type"),
   ("Rosca de la conexión roscada: NPT (cónica, ASME B1.20.1, sella en el filete) o G "
    "(BSPP cilíndrica, ISO 228, sella con junta o arandela).",
    "Thread of a threaded connection: NPT (tapered, ASME B1.20.1, seals on the thread) or G "
    "(BSPP parallel, ISO 228, seals with a gasket or washer)."),
   ("Cambia la designación del tamaño («1 NPT» o «G 1»), el código de la hoja de datos (R o G) "
    "y el rótulo del plano. El cálculo ASME trata ambas como conexión roscada.",
    "Changes the size designation (\"1 NPT\" or \"G 1\"), the datasheet code (R or G) "
    "and the drawing label. The ASME check treats both as a threaded connection."),
   affects=("Hoja de datos, plano y aviso informativo para rosca G.",
            "Datasheet, drawing and informative warning for G threads."),
   interpret=("La G necesita una cara de asiento y junta; verifique que la cupla de la línea "
              "tenga la misma rosca.", "G needs a seating face and gasket; check that the "
              "line coupling has the same thread."))

ALIASES: Final[dict[str, str]] = {
    # columnas de la tabla por caso y filas de «Resultados calculados»
    "V": "r.velocity", "Re": "r.reynolds", "N_S": "r.strouhal", "f_s": "r.fs", "f_n": "r.fn",
    "H_c": "r.hc", "f_n,c": "r.fnc", "N_Sc": "r.scruton", "f_s / f_n,c": "r.ratio",
    "V_IR": "r.v_ir", "q_actual": "r.q_actual", "velocity": "r.velocity", "ve": "r.ve",
    "v_ve": "r.v_ve", "reynolds": "r.reynolds", "strouhal": "r.strouhal", "fs": "r.fs",
    "fnc": "r.fnc", "ratio": "r.ratio", "steady": "r.steady", "dynamic": "r.dynamic",
    "von_mises": "r.von_mises",
    # opciones con otra clave de texto
    "opt.flange_manual": "opt.flange_manual", "f.nozzle": "f.mount",
    "f.auto_select": "topic.auto", "res.auto_title": "topic.auto",
    "f.mode_process": "f.auto_props", "f.mode_pipe": "f.schedule",
}


def card_for(key: str) -> Card | None:
    """Ficha de una clave de texto, columna o criterio (``steady_stress_support`` incluido)."""
    if key in CARDS:
        return CARDS[key]
    if key in ALIASES:
        return CARDS.get(ALIASES[key])
    for prefix in ("steady_stress", "dynamic_stress"):
        if key.startswith(prefix):
            return CARDS[f"crit.{prefix}"]
    return CARDS.get(f"crit.{key}")
