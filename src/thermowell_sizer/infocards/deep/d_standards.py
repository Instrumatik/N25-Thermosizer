"""Fichas completas de las normas de la biblioteca (resumen propio, sin texto de la norma)."""

from __future__ import annotations

from typing import Any


def _s(title: tuple[str, str], what: tuple[str, str], role: tuple[str, str],
       essence: tuple[str, str], why: tuple[str, str], worked: tuple[str, str],
       mistakes: tuple[str, str], reference: tuple[str, str]) -> dict[str, Any]:
    return {"title": title, "what": what, "role": role, "essence": essence, "why": why,
            "worked": worked, "mistakes": mistakes, "reference": reference}


_NOTE = ("Resumen propio con fines de orientación. Consulte la edición vigente de la norma.",
         "Own summary for guidance. Consult the current edition of the standard.")

NEW: dict[str, dict[str, Any]] = {
    "std.ptc193": _s(
        ("ASME PTC 19.3 TW", "ASME PTC 19.3 TW"),
        ("Norma de ASME para el diseño mecánico de termopozos de barra maciza perforada.",
         "ASME standard for the mechanical design of drilled bar-stock thermowells."),
        ("Es la base de toda la verificación de TS.", "It is the basis of all TS checks."),
        ("Trata la vaina como una viga en voladizo expuesta a flujo cruzado y verifica:\n\n"
         "- Frecuencia: que la estela no excite la frecuencia natural instalada (transversal "
         "y en línea), con criterios según el amortiguamiento (Scruton).\n"
         "- Esfuerzos estacionarios: flexión por arrastre más presión, contra el admisible.\n"
         "- Esfuerzos dinámicos: amplitud oscilante contra el límite de fatiga.\n"
         "- Presión: colapso del vástago y de la punta, y rating de la brida.\n\n"
         "La edición 2016 reemplazó al método anterior (PTC 19.3-1974), que solo evaluaba la "
         "resonancia transversal con un límite simple de frecuencia.",
         "It treats the well as a cantilever beam in cross-flow and checks:\n\n"
         "- Frequency: that the wake does not excite the installed natural frequency "
         "(transverse and in-line), with criteria depending on damping (Scruton).\n"
         "- Steady stresses: drag bending plus pressure, against the allowable.\n"
         "- Dynamic stresses: oscillating amplitude against the fatigue limit.\n"
         "- Pressure: shank and tip collapse, and flange rating.\n\n"
         "The 2016 edition replaced the earlier method (PTC 19.3-1974), which only assessed "
         "transverse resonance with a simple frequency limit."),
        ("Es la referencia aceptada por la industria y por los clientes para aprobar "
         "termovainas en servicios con flujo.",
         "It is the reference accepted by industry and clients to approve thermowells in "
         "flowing services."),
        ("Una vaina que cumplía con el método 1974 (f_s < 0,8 f_n) puede no cumplir con 2016 "
         "si el fluido es denso y la relación cae entre 0,4 y 0,8.",
         "A well that passed under the 1974 method (f_s < 0.8 f_n) may fail under 2016 if the "
         "fluid is dense and the ratio falls between 0.4 and 0.8."),
        ("- Usar planillas basadas en 1974.\n"
         "- Aplicarla a vainas fabricadas (tubo soldado) o cerámicas, fuera de su alcance.",
         "- Using spreadsheets based on 1974.\n"
         "- Applying it to fabricated (welded tube) or ceramic wells, outside its scope."),
        _NOTE),
    "std.b165": _s(
        ("ASME B16.5", "ASME B16.5"),
        ("Norma de bridas y accesorios bridados de cañería de NPS ½ a 24.",
         "Standard for pipe flanges and flanged fittings from NPS ½ to 24."),
        ("Define el rating de la brida de la vaina.", "It defines the well flange rating."),
        ("Agrupa los materiales por comportamiento (grupos 1.1, 2.2, etc.) y, para cada "
         "clase, tabula la presión admisible en función de la temperatura. También fija "
         "dimensiones, caras (RF, RTJ, FF), bulones y tolerancias, para que bridas de "
         "distintos fabricantes sean intercambiables.",
         "It groups materials by behaviour (groups 1.1, 2.2, etc.) and, for each class, "
         "tabulates allowable pressure versus temperature. It also sets dimensions, faces "
         "(RF, RTJ, FF), bolting and tolerances so flanges from different makers are "
         "interchangeable."),
        ("La brida de la vaina debe calzar con la de la línea y soportar la presión de "
         "diseño a la temperatura de diseño.",
         "The well flange must mate with the line flange and withstand design pressure at "
         "design temperature."),
        ("316 (grupo 2.2) clase 300: ≈ 49,6 bar a 38 °C y ≈ 37 bar a 300 °C.",
         "316 (group 2.2) class 300: ≈ 49.6 bar at 38 °C and ≈ 37 bar at 300 °C."),
        ("- Usar la clase como presión en psi.", "- Using the class as a pressure in psi."),
        _NOTE),
    "std.b40": _s(
        ("ASME B40.200 (B40.9)", "ASME B40.200 (B40.9)"),
        ("Norma de termómetros y termovainas: tipos, dimensiones y designaciones.",
         "Standard for thermometers and thermowells: types, dimensions and designations."),
        ("Orienta dimensiones típicas (agujeros, largos U normalizados, conexiones).",
         "It guides typical dimensions (bores, standard U lengths, connections)."),
        ("Normaliza las formas constructivas (roscadas, bridadas, para soldar), los "
         "agujeros habituales (0,260\" y 0,385\") y la forma de designar largos, para que un "
         "sensor de un fabricante entre en la vaina de otro.",
         "It standardizes constructions (threaded, flanged, weld-in), common bores (0.260\" "
         "and 0.385\") and length designation so one maker's sensor fits another's well."),
        ("Permite comprar vainas y sensores intercambiables. No reemplaza la verificación "
         "mecánica de PTC 19.3 TW.",
         "It allows buying interchangeable wells and sensors. It does not replace the PTC "
         "19.3 TW mechanical check."),
        ("Largos U típicos: 2½\", 4½\", 7½\", 10½\", 13½\", 16½\", 22½\".",
         "Typical U lengths: 2½\", 4½\", 7½\", 10½\", 13½\", 16½\", 22½\"."),
        ("- Suponer que una vaina dimensionalmente estándar es mecánicamente apta.",
         "- Assuming a dimensionally standard well is mechanically fit."),
        _NOTE),
    "std.din43772": _s(
        ("DIN 43772", "DIN 43772"),
        ("Norma alemana de vainas de protección para termómetros (formas 1 a 4).",
         "German standard for thermometer protection wells (forms 1 to 4)."),
        ("Referencia para equipos de origen europeo.", "Reference for European equipment."),
        ("Define formas constructivas (tubo, barra perforada cónica, con rosca G o brida), "
         "dimensiones métricas y materiales habituales. Las formas 4 son de barra perforada "
         "y comparables a las de ASME.",
         "It defines constructions (tube, tapered drilled bar, with G thread or flange), "
         "metric dimensions and usual materials. Form 4 wells are drilled bar stock and "
         "comparable to ASME ones."),
        ("En plantas con equipos europeos aparecen roscas G y cotas métricas; hay que "
         "verificarlas igual con PTC 19.3 TW.",
         "Plants with European equipment show G threads and metric dimensions; they must "
         "still be checked with PTC 19.3 TW."),
        ("Forma 4 con rosca G 1, punta 12,5 mm, U 140 mm.",
         "Form 4 with G 1 thread, 12.5 mm tip, U 140 mm."),
        ("- Mezclar roscas G y NPT.", "- Mixing G and NPT threads."),
        _NOTE),
    "std.isatr20": _s(
        ("ISA-TR20.00.01", "ISA-TR20.00.01"),
        ("Informe técnico de ISA con hojas de datos de especificación de instrumentos.",
         "ISA technical report with instrument specification datasheets."),
        ("Modelo para la hoja de datos de TS.", "Model for the TS datasheet."),
        ("Propone formularios estándar con los campos que un proveedor necesita para "
         "cotizar y fabricar: proceso, conexión, material, dimensiones, ensayos.",
         "It proposes standard forms with the fields a supplier needs to quote and "
         "manufacture: process, connection, material, dimensions, tests."),
        ("Una hoja de datos completa evita consultas y errores de compra.",
         "A complete datasheet avoids queries and purchasing errors."),
        ("Campos típicos: tag, servicio, P y T, material, conexión, U, ensayos (PMI, "
         "hidrostática).",
         "Typical fields: tag, service, P and T, material, connection, U, tests (PMI, "
         "hydrostatic)."),
        ("- Emitir hojas sin datos de proceso: el proveedor no puede verificar.",
         "- Issuing sheets without process data: the supplier cannot verify."),
        _NOTE),
    "std.nace": _s(
        ("NACE MR0175 / ISO 15156", "NACE MR0175 / ISO 15156"),
        ("Norma de materiales para equipos en servicio con H₂S en producción de petróleo y "
         "gas.",
         "Standard for materials in H₂S-containing service in oil and gas production."),
        ("Activa el filtrado de materiales para servicio ácido.",
         "It enables material filtering for sour service."),
        ("Define cuándo un servicio es ácido (por presión parcial de H₂S, con agua) y qué "
         "materiales, durezas y tratamientos térmicos resisten la fisuración por hidrógeno. "
         "Está dividida en principios generales, aceros al carbono y de baja aleación, y "
         "aleaciones resistentes a la corrosión, con límites por material de pH, cloruros, "
         "temperatura y presión parcial.",
         "It defines when a service is sour (by H₂S partial pressure, with water) and which "
         "materials, hardnesses and heat treatments resist hydrogen cracking. It is split "
         "into general principles, carbon and low-alloy steels, and corrosion-resistant "
         "alloys, with per-material limits on pH, chlorides, temperature and partial "
         "pressure."),
        ("Una falla por H₂S libera un gas tóxico; el cumplimiento suele ser obligatorio por "
         "contrato y por regulación.",
         "An H₂S failure releases a toxic gas; compliance is usually mandatory by contract "
         "and regulation."),
        ("Gas a 70 bar con 50 ppm de H₂S: p = 70 × 0,00005 = 0,0035 bar = 0,35 kPa → ácido.",
         "Gas at 70 bar with 50 ppm H₂S: p = 70 × 0.00005 = 0.0035 bar = 0.35 kPa → sour."),
        ("- Confundir con NACE MR0103 (refinación), que tiene otros criterios.",
         "- Confusing it with NACE MR0103 (refining), which has other criteria."),
        _NOTE),
    "std.iec60751": _s(
        ("IEC 60751", "IEC 60751"),
        ("Norma de termorresistencias de platino industriales (Pt100, Pt1000).",
         "Standard for industrial platinum resistance thermometers (Pt100, Pt1000)."),
        ("Define la curva y las tolerancias de los sensores RTD.",
         "It defines the curve and tolerances of RTD sensors."),
        ("Fija la relación resistencia-temperatura del platino (ecuación de Callendar-Van "
         "Dusen) y las clases de tolerancia (AA, A, B, C): cuánto puede apartarse un sensor "
         "nuevo de la curva.",
         "It sets platinum's resistance-temperature relation (Callendar-Van Dusen equation) "
         "and tolerance classes (AA, A, B, C): how far a new sensor may deviate from the "
         "curve."),
        ("Garantiza que cualquier transmisor lea bien cualquier Pt100 de la misma norma.",
         "It ensures any transmitter reads any Pt100 of the same standard correctly."),
        ("Clase A: ±(0,15 + 0,002·|t|) °C → a 100 °C, ±0,35 °C.",
         "Class A: ±(0.15 + 0.002·|t|) °C → at 100 °C, ±0.35 °C."),
        ("- Pedir clase AA para un servicio que no la necesita.",
         "- Ordering class AA for a service that does not need it."),
        _NOTE),
    "std.iec60584": _s(
        ("IEC 60584-1", "IEC 60584-1"),
        ("Norma de termopares: tablas de voltaje-temperatura y tolerancias.",
         "Thermocouple standard: voltage-temperature tables and tolerances."),
        ("Define los tipos (K, J, N, T, E, R, S, B) y sus clases.",
         "It defines the types (K, J, N, T, E, R, S, B) and their classes."),
        ("Cada par de metales tiene una tabla de fuerza electromotriz en función de la "
         "temperatura. La norma las fija junto con las tolerancias de clase 1, 2 y 3.",
         "Each metal pair has an emf-versus-temperature table. The standard fixes them along "
         "with class 1, 2 and 3 tolerances."),
        ("Permite elegir el tipo según rango y atmósfera, y saber la precisión esperada.",
         "It allows choosing the type by range and atmosphere, and knowing expected "
         "accuracy."),
        ("Tipo K clase 1: ±1,5 °C o ±0,004·|t|, el mayor. A 800 °C: ±3,2 °C.",
         "Type K class 1: ±1.5 °C or ±0.004·|t|, whichever is greater. At 800 °C: ±3.2 °C."),
        ("- Mezclar códigos de color ANSI e IEC.", "- Mixing ANSI and IEC colour codes."),
        _NOTE),
}
