"""Tablas de consulta para el ingeniero (biblioteca › Referencias).

Datos técnicos de dominio público resumidos con redacción propia: no se reproduce texto
de normas. Los valores son orientativos y deben contrastarse con la edición vigente de
cada norma o con el catálogo del fabricante.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from thermowell_sizer.core.advisories import DIAL_RANGES_C
from thermowell_sizer.core.designs import DESIGN_NAMES, STANDARD_U, TYPICAL_DESIGNS
from thermowell_sizer.infocards.guides import (
    CONNECTION_NOTE,
    CONNECTION_TABLE,
    PROFILE_COST_NOTE,
    PROFILE_TABLE,
)

Bi = tuple[str, str]
"""Texto bilingüe (es, en)."""


@dataclass(frozen=True)
class RefTable:
    """Tabla de referencia con título, nota y filas de texto."""

    id: str
    title: Bi
    note: Bi
    headers: tuple[Bi, ...]
    rows: tuple[tuple[str | Bi, ...], ...]


def _b(es: str, en: str | None = None) -> Bi:
    return es, en if en is not None else es


THERMOCOUPLE_COLORS = RefTable(
    "tc_colors",
    _b("Termopares: códigos de color", "Thermocouples: colour codes"),
    _b("ANSI MC96.1 (EE. UU.): el negativo es siempre rojo. IEC 60584-3: el negativo es "
       "siempre blanco y la cubierta tiene el color del positivo. Verifique el código que "
       "pide la especificación del proyecto antes de cablear.",
       "ANSI MC96.1 (USA): negative is always red. IEC 60584-3: negative is always white "
       "and the jacket matches the positive colour. Check the code required by the project "
       "specification before wiring."),
    (_b("Tipo", "Type"), _b("Aleación (+ / −)", "Alloy (+ / −)"),
     _b("ANSI: + / − / cubierta", "ANSI: + / − / jacket"),
     _b("IEC: + / − / cubierta", "IEC: + / − / jacket")),
    (
        ("K", "Chromel / Alumel",
         _b("amarillo / rojo / amarillo", "yellow / red / yellow"),
         _b("verde / blanco / verde", "green / white / green")),
        ("J", _b("Hierro / Constantán", "Iron / Constantan"),
         _b("blanco / rojo / negro", "white / red / black"),
         _b("negro / blanco / negro", "black / white / black")),
        ("T", _b("Cobre / Constantán", "Copper / Constantan"),
         _b("azul / rojo / azul", "blue / red / blue"),
         _b("marrón / blanco / marrón", "brown / white / brown")),
        ("E", "Chromel / Constantán",
         _b("violeta / rojo / violeta", "purple / red / purple"),
         _b("violeta / blanco / violeta", "violet / white / violet")),
        ("N", "Nicrosil / Nisil",
         _b("naranja / rojo / naranja", "orange / red / orange"),
         _b("rosa / blanco / rosa", "pink / white / pink")),
        ("R, S", "Pt-Rh / Pt",
         _b("negro / rojo / verde (compensación)", "black / red / green (compensating)"),
         _b("naranja / blanco / naranja", "orange / white / orange")),
        ("B", "Pt-30Rh / Pt-6Rh",
         _b("gris / rojo / gris", "grey / red / grey"),
         _b("gris / blanco / gris", "grey / white / grey")),
    ),
)

THERMOCOUPLE_TOLERANCES = RefTable(
    "tc_tolerances",
    _b("Termopares: rangos y tolerancias", "Thermocouples: ranges and tolerances"),
    _b("Tolerancia = el mayor de los dos valores; |t| en °C. Rangos de uso continuo "
       "orientativos con vaina adecuada. Fuente: IEC 60584-1 y ASTM E230 (ANSI).",
       "Tolerance = the larger of the two values; |t| in °C. Indicative continuous-use "
       "ranges with a suitable sheath. Source: IEC 60584-1 and ASTM E230 (ANSI)."),
    (_b("Tipo", "Type"), _b("Rango de uso", "Use range"), _b("IEC clase 1", "IEC class 1"),
     _b("IEC clase 2", "IEC class 2"), _b("ASTM estándar", "ASTM standard"),
     _b("ASTM especial", "ASTM special")),
    (
        ("K", "−200 … 1260 °C", "±1,5 °C / 0,004·|t|", "±2,5 °C / 0,0075·|t|",
         "±2,2 °C / 0,75 %", "±1,1 °C / 0,4 %"),
        ("J", "−40 … 750 °C", "±1,5 °C / 0,004·|t|", "±2,5 °C / 0,0075·|t|",
         "±2,2 °C / 0,75 %", "±1,1 °C / 0,4 %"),
        ("T", "−200 … 370 °C", "±0,5 °C / 0,004·|t|", "±1,0 °C / 0,0075·|t|",
         "±1,0 °C / 0,75 %", "±0,5 °C / 0,4 %"),
        ("E", "−200 … 870 °C", "±1,5 °C / 0,004·|t|", "±2,5 °C / 0,0075·|t|",
         "±1,7 °C / 0,5 %", "±1,0 °C / 0,4 %"),
        ("N", "−200 … 1260 °C", "±1,5 °C / 0,004·|t|", "±2,5 °C / 0,0075·|t|",
         "±2,2 °C / 0,75 %", "±1,1 °C / 0,4 %"),
        ("R, S", "0 … 1480 °C", "±1,0 °C (≤ 1100 °C)", "±1,5 °C / 0,0025·|t|",
         "±1,5 °C / 0,25 %", "±0,6 °C / 0,1 %"),
        ("B", "870 … 1700 °C", "—", "0,0025·|t| (≥ 600 °C)", "±0,5 % (> 870 °C)",
         "±0,25 %"),
    ),
)

RTD_CLASSES = RefTable(
    "rtd_classes",
    _b("Pt100: clases de tolerancia IEC 60751", "Pt100: IEC 60751 tolerance classes"),
    _b("Tolerancia en °C con |t| en °C. El rango válido depende de la construcción "
       "(bobinado o película). Para medición de proceso suele pedirse clase A o B con "
       "conexión a 3 o 4 hilos.",
       "Tolerance in °C with |t| in °C. The valid range depends on construction (wire-wound "
       "or thin film). Process measurement usually calls for class A or B with 3 or 4 wires."),
    (_b("Clase", "Class"), _b("Tolerancia", "Tolerance"),
     _b("Bobinado", "Wire-wound"), _b("Película", "Thin film"), _b("A 100 °C", "At 100 °C")),
    (
        ("AA (1/3 DIN)", "±(0,1 + 0,0017·|t|)", "−50 … 250 °C", "0 … 150 °C", "±0,27 °C"),
        ("A", "±(0,15 + 0,002·|t|)", "−100 … 450 °C", "−30 … 300 °C", "±0,35 °C"),
        ("B", "±(0,3 + 0,005·|t|)", "−196 … 600 °C", "−50 … 500 °C", "±0,80 °C"),
        ("C", "±(0,6 + 0,01·|t|)", "−196 … 600 °C", "−50 … 600 °C", "±1,60 °C"),
    ),
)

RTD_WIRING = RefTable(
    "rtd_wiring",
    _b("RTD: conexión y colores de cables", "RTD: wiring and wire colours"),
    _b("IEC 60751: los conductores de un mismo extremo del elemento llevan el mismo color "
       "(rojo en un extremo, blanco en el otro). La práctica norteamericana usa a menudo "
       "rojo/blanco o rojo/negro: confirme con el fabricante.",
       "IEC 60751: leads from the same end of the element share a colour (red at one end, "
       "white at the other). North American practice often uses red/white or red/black: "
       "confirm with the manufacturer."),
    (_b("Conexión", "Connection"), _b("Colores IEC", "IEC colours"),
     _b("Compensa cables", "Lead compensation"), _b("Uso típico", "Typical use")),
    (
        (_b("2 hilos", "2 wires"), _b("rojo / blanco", "red / white"),
         _b("No", "No"), _b("Distancias cortas, indicación local", "Short runs, local display")),
        (_b("3 hilos", "3 wires"), _b("rojo / rojo / blanco", "red / red / white"),
         _b("Sí (cables iguales)", "Yes (equal leads)"),
         _b("Estándar en procesos industriales", "Industrial process standard")),
        (_b("4 hilos", "4 wires"), _b("rojo / rojo / blanco / blanco",
                                       "red / red / white / white"),
         _b("Sí, total", "Yes, full"), _b("Laboratorio, custodia, alta exactitud",
                                          "Laboratory, custody transfer, high accuracy")),
    ),
)

DIAL_SCALES = RefTable(
    "dial_scales",
    _b("Termómetros bimetálicos: escalas normalizadas",
       "Bimetallic thermometers: standard scales"),
    _b("Elegir la escala que deja la operación normal en el tercio central y la temperatura "
       "de diseño dentro de la escala. Diales habituales de 100 y 125 mm; clase 1 (±1 % del "
       "span). El programa propone la escala solo cuando el sensor es bimetálico.",
       "Pick the scale that puts normal operation in the middle third and the design "
       "temperature within the scale. Usual dials are 100 and 125 mm; class 1 (±1 % of span). "
       "The program proposes the scale when the sensor is bimetallic."),
    (_b("Escala", "Scale"), _b("Tercio central (operación)", "Middle third (operation)")),
    tuple((f"{lo:g} … {hi:g} °C",
           f"{lo + (hi - lo) / 3:.0f} … {lo + 2 * (hi - lo) / 3:.0f} °C")
          for lo, hi in DIAL_RANGES_C),
)

THERMOWELL_TYPES = RefTable(
    "tw_types",
    _b("Tipos de termopozo: cuándo usar cada uno", "Thermowell types: when to use each"),
    _b("Resumen de práctica habitual. La especificación del cliente y el servicio "
       "(presión, fluido, peligrosidad) definen la elección final.",
       "Summary of common practice. The client specification and the service (pressure, "
       "fluid, hazard) set the final choice."),
    (_b("Tipo", "Type"), _b("Ventajas", "Advantages"), _b("Limitaciones", "Limitations"),
     _b("Aplicación típica", "Typical application")),
    (
        (_b("Roscado (NPT)", "Threaded (NPT)"),
         _b("Económico, se desmonta fácil", "Low cost, easy removal"),
         _b("Camino de fuga por la rosca; limitado en presión y en servicio peligroso",
            "Thread leak path; limited in pressure and hazardous service"),
         _b("Líneas chicas, servicios auxiliares (agua, aire)",
            "Small lines, utilities (water, air)")),
        (_b("Bridado", "Flanged"),
         _b("Desmontable, cualquier rating, el más usado en proceso",
            "Removable, any rating, most common in process"),
         _b("Más caro; requiere brida de montaje en la línea",
            "More costly; needs a flanged mounting nozzle"),
         _b("Hidrocarburos, servicios peligrosos, recipientes",
            "Hydrocarbons, hazardous service, vessels")),
        ("Socket weld",
         _b("Sin camino de fuga, alta presión", "No leak path, high pressure"),
         _b("Permanente; reemplazo con corte", "Permanent; replacement needs cutting"),
         _b("Vapor y alta presión en líneas chicas", "Steam and high pressure in small lines")),
        (_b("Para soldar (weld-in)", "Weld-in"),
         _b("Máxima resistencia mecánica", "Highest mechanical strength"),
         _b("Permanente; soldadura en campo", "Permanent; field welding"),
         _b("Alta velocidad y presión: vapor, gas de alta", "High velocity and pressure: "
            "steam, high-pressure gas")),
        ("Van Stone",
         _b("Solo el termopozo es de aleación (brida loca de acero al carbono)",
            "Only the thermowell is alloy (carbon-steel lap-joint flange)"),
         _b("Requiere brida loca y junta en el collar", "Needs lap-joint flange and gasket "
            "on the collar"),
         _b("Servicios corrosivos con aleaciones caras", "Corrosive service with costly "
            "alloys")),
        (_b("Sanitario (clamp)", "Sanitary (clamp)"),
         _b("Limpieza CIP, sin intersticios", "CIP cleaning, crevice-free"),
         _b("Baja presión", "Low pressure"),
         _b("Alimentos, farmacia", "Food, pharma")),
    ),
)

CORROSION_GUIDE = RefTable(
    "corrosion",
    _b("Guía de materiales por servicio", "Material guide by service"),
    _b("Orientativa y «a verificar»: la selección final depende de la concentración, la "
       "temperatura, las impurezas y la experiencia de planta. Use el asistente de "
       "material para un ranking con sus condiciones.",
       "Indicative and 'to be verified': the final choice depends on concentration, "
       "temperature, impurities and plant experience. Use the material assistant for a "
       "ranking with your conditions."),
    (_b("Servicio", "Service"), _b("Material habitual", "Usual material"),
     _b("Alternativas / notas", "Alternatives / notes")),
    (
        (_b("Agua, aire, aceite, gas dulce", "Water, air, oil, sweet gas"), "AISI 316/316L",
         _b("304 en servicios no críticos", "304 for non-critical service")),
        (_b("Vapor hasta 425 °C", "Steam up to 425 °C"), "A105 / 316",
         _b("Igual material que la cañería", "Same material as the piping")),
        (_b("Vapor y alta temperatura 425 … 595 °C", "Steam and high temperature "
            "425 … 595 °C"), "F11 / F22 (Cr-Mo)", _b("F91 para alta presión y temperatura",
                                                        "F91 for high P and T")),
        (_b("Gas o crudo agrio (H₂S)", "Sour gas or crude (H₂S)"),
         _b("316L según NACE MR0175 (≤ 22 HRC)", "316L per NACE MR0175 (≤ 22 HRC)"),
         _b("Inconel 625, Incoloy 825 con cloruros altos", "Inconel 625, Incoloy 825 with "
            "high chlorides")),
        (_b("Agua de mar, salmuera, cloruros", "Seawater, brine, chlorides"),
         _b("Dúplex 2205, Monel 400", "Duplex 2205, Monel 400"),
         _b("Superdúplex, Hastelloy C-276, titanio", "Super duplex, Hastelloy C-276, titanium")),
        (_b("Ácido sulfúrico", "Sulfuric acid"), _b("Alloy 20, Hastelloy C-276",
                                                     "Alloy 20, Hastelloy C-276"),
         _b("Tantalio o recubrimiento PTFE/PFA", "Tantalum or PTFE/PFA lining")),
        (_b("Ácido clorhídrico", "Hydrochloric acid"), _b("Hastelloy B-3 / C-276",
                                                           "Hastelloy B-3 / C-276"),
         _b("Tantalio, PFA", "Tantalum, PFA")),
        (_b("Soda cáustica caliente", "Hot caustic soda"), _b("Níquel 200, Monel 400",
                                                               "Nickel 200, Monel 400"),
         _b("Evitar inoxidables austeníticos (fisuración)", "Avoid austenitic stainless "
            "(cracking)")),
        (_b("Gases de combustión con azufre", "Flue gas with sulfur"), "AISI 446",
         _b("Inconel 600 en atmósferas oxidantes", "Inconel 600 in oxidizing atmospheres")),
        (_b("Más de 800 °C, hornos", "Above 800 °C, furnaces"), _b("Inconel 600, 446",
                                                                     "Inconel 600, 446"),
         _b("Vaina cerámica por encima de 1100 °C", "Ceramic sheath above 1100 °C")),
        (_b("Hidrógeno a alta temperatura", "High-temperature hydrogen"),
         _b("Cr-Mo según curvas de Nelson (API 941)", "Cr-Mo per Nelson curves (API 941)"),
         _b("Verificar con el licenciante del proceso", "Check with the process licensor")),
        (_b("Sólidos, erosión", "Solids, erosion"), _b("316 + Stellite 6", "316 + Stellite 6"),
         _b("Carburo de tungsteno HVOF; perfil cónico", "HVOF tungsten carbide; tapered "
            "profile")),
    ),
)


def _designs_table() -> RefTable:
    rows: list[tuple[str | Bi, ...]] = []
    for d in TYPICAL_DESIGNS:
        for bore, (a, b) in d.diameters.items():
            rows.append((DESIGN_NAMES[d.id], ", ".join(d.sizes), f"{bore * 1000:.1f}",
                         f"{a * 1000:.2f}", f"{b * 1000:.2f}"))
    return RefTable(
        "designs",
        _b("Diseños típicos (catálogo genérico)", "Typical designs (generic catalog)"),
        _b("Dimensiones típicas en mm, t = 6,35 mm (1/4\"). Largos U normalizados: "
           + ", ".join(f"{u * 1000:.1f}" for u in STANDARD_U) + " mm. Confirme con el plano "
           "del fabricante. Se cargan desde Termopozo › Diseño típico.",
           "Typical dimensions in mm, t = 6.35 mm (1/4\"). Standard U lengths: "
           + ", ".join(f"{u * 1000:.1f}" for u in STANDARD_U) + " mm. Confirm with the "
           "manufacturer's drawing. Load them from Thermowell › Typical design."),
        (_b("Ejecución", "Design"), _b("Conexión", "Connection"), _b("d", "d"),
         _b("A (raíz)", "A (root)"), _b("B (punta)", "B (tip)")),
        tuple(rows),
    )


INSTALLATION = RefTable(
    "installation",
    _b("Buenas prácticas de instalación", "Installation good practice"),
    _b("Resumen de práctica habitual en especificaciones de operadoras y catálogos.",
       "Summary of common practice in operator specifications and catalogs."),
    (_b("Tema", "Topic"), _b("Recomendación", "Recommendation")),
    (
        (_b("Inmersión", "Immersion"),
         _b("Punta entre 1/3 y 1/2 del diámetro interno; al menos el largo sensible más 4 a 6 "
            "diámetros de punta expuestos al flujo.",
            "Tip between 1/3 and 1/2 of the inside diameter; at least the sensitive length "
            "plus 4 to 6 tip diameters exposed to the flow.")),
        (_b("Líneas chicas", "Small lines"),
         _b("En líneas menores de 3\" a 4\", montar en codo (punta hacia aguas arriba) o "
            "ampliar la línea en el punto de medición.",
            "On lines below 3\" to 4\", mount in an elbow (tip facing upstream) or enlarge "
            "the line at the measuring point.")),
        (_b("Orientación", "Orientation"),
         _b("En líneas horizontales, conexión en el cuadrante superior; evitar el fondo "
            "(sedimentos) en líquidos sucios.",
            "On horizontal lines, connection in the upper quadrant; avoid the bottom "
            "(sediment) in dirty liquids.")),
        (_b("Brida de montaje (Hs)", "Mounting flange (Hs)"),
         _b("Altura habitual de 150 mm hasta 600# y 200 mm desde 900#; considerar el "
            "tramo protegido L0 en el cálculo.",
            "Usual projection 150 mm up to 600# and 200 mm from 900#; account for the "
            "shielded length L0 in the calculation.")),
        (_b("Agujero y sensor", "Bore and sensor"),
         _b("Agujero de 6,6 a 7 mm para sensores de 6 mm; resorte de empuje para asegurar "
            "el contacto con el fondo.",
            "6.6 to 7 mm bore for 6 mm sensors; spring loading to keep contact with the "
            "bottom.")),
        (_b("Recipientes y tanques", "Vessels and tanks"),
         _b("Inmersión de 450 mm (recipientes) a 1500 mm (tanques); por encima de 1000 mm "
            "estudiar soportes.",
            "Immersion from 450 mm (vessels) to 1500 mm (tanks); above 1000 mm study "
            "supports.")),
        (_b("Termopozo sin sensor", "Thermowell without sensor"),
         _b("Tapón hexagonal de 1/2\" NPT de inoxidable con cadena.",
            "1/2\" NPT stainless hex plug with chain.")),
    ),
)

CONNECTION_USE: Final = RefTable(
    "connection_use", _b("Tipos de conexión: dónde se usan y dónde no",
                         "Connection types: where to use them and where not"),
    CONNECTION_NOTE, CONNECTION_TABLE[0], CONNECTION_TABLE[1:])
PROFILE_GUIDE: Final = RefTable(
    "profile_guide", _b("Perfiles del vástago: uso, límites y costo relativo",
                        "Shank profiles: use, limits and relative cost"),
    PROFILE_COST_NOTE, PROFILE_TABLE[0], PROFILE_TABLE[1:])

REFERENCE_TABLES: Final[tuple[RefTable, ...]] = (
    THERMOWELL_TYPES, CONNECTION_USE, PROFILE_GUIDE, _designs_table(), INSTALLATION,
    CORROSION_GUIDE, THERMOCOUPLE_COLORS,
    THERMOCOUPLE_TOLERANCES, RTD_CLASSES, RTD_WIRING, DIAL_SCALES,
)


def text(value: str | Bi, es: bool) -> str:
    """Texto en el idioma pedido."""
    if isinstance(value, str):
        return value
    return value[0] if es else value[1]
