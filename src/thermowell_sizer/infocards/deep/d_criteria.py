"""Profundidad de las fichas de criterios ASME y temas del estado."""

from __future__ import annotations

from typing import Any

DEEP: dict[str, dict[str, Any]] = {
    "crit.scope": {
        "essence": (
            "Las fórmulas de la norma salen de modelos y ensayos sobre vainas de proporciones "
            "habituales: punta no demasiado fina respecto de la raíz, largo razonable respecto "
            "del diámetro, agujero centrado. Fuera de esos rangos el modelo de viga deja de "
            "representar bien a la pieza (por ejemplo, una vaina muy corta y gruesa se comporta "
            "más como un bloque que como una viga).",
            "The standard's formulas come from models and tests on wells of usual proportions: "
            "tip not too thin relative to root, reasonable length relative to diameter, "
            "centred bore. Outside those ranges the beam model no longer represents the part "
            "well (for example, a very short thick well behaves more like a block than a "
            "beam)."),
        "why": (
            "Si la geometría está fuera de alcance, el resultado numérico puede no ser válido "
            "aunque «cumpla». Hace falta análisis especial (elementos finitos) o cambiar la "
            "geometría.",
            "If geometry is out of scope, the numerical result may be invalid even if it "
            "«passes». Special analysis (finite elements) or a geometry change is needed."),
        "worked": (
            "Escalonado con B/A = 0,5: fuera del rango del escalonado (≈ 0,58 a 0,88). "
            "Subiendo B a 12,7 mm con A = 22,2 mm, B/A = 0,57: todavía fuera; con A = 19,05, "
            "B/A = 0,67: dentro.",
            "Stepped with B/A = 0.5: outside the stepped range (≈ 0.58 to 0.88). Raising B to "
            "12.7 mm with A = 22.2 mm, B/A = 0.57: still outside; with A = 19.05, B/A = 0.67: "
            "inside."),
        "mistakes": ("- Ignorar el aviso de alcance porque el resto da verde.",
                     "- Ignoring the scope warning because the rest is green."),
    },
    "crit.material_temperature": {
        "essence": (
            "Cada material tiene un rango donde sus propiedades están tabuladas y son "
            "confiables. Por arriba aparecen fluencia lenta, oxidación o cambios de "
            "microestructura (por ejemplo, el 304 «sensibilizado» entre 425 y 815 °C, cuando "
            "precipitan carburos de cromo en los bordes de grano y pierde resistencia a la "
            "corrosión). Por abajo, algunos aceros se vuelven frágiles.",
            "Each material has a range where its properties are tabulated and reliable. Above "
            "it, creep, oxidation or microstructural changes appear (for example 304 "
            "«sensitized» between 425 and 815 °C, when chromium carbides precipitate at grain "
            "boundaries and corrosion resistance drops). Below it, some steels become "
            "brittle."),
        "why": ("Fuera de rango, E y S no son conocidos y el cálculo no tiene base.",
                "Out of range, E and S are unknown and the calculation has no basis."),
        "worked": (
            "Acero al carbono A105 a −50 °C: por debajo de su rango habitual (−29 °C) → usar "
            "A350 LF2 con ensayo de impacto.",
            "A105 carbon steel at −50 °C: below its usual range (−29 °C) → use A350 LF2 with "
            "impact testing."),
        "mistakes": ("- Olvidar la temperatura mínima (arranques en invierno, despresurización).",
                     "- Forgetting minimum temperature (winter start-ups, "
                     "depressurization)."),
    },
    "crit.pressure_rating": {
        "essence": (
            "Verifica que el vástago (P_c) y la punta (P_t) aguanten la presión externa del "
            "proceso. Un tubo bajo presión externa puede colapsar (aplastarse) o pandear; la "
            "punta, que es una tapa plana o semiesférica, puede abollarse.",
            "It checks that shank (P_c) and tip (P_t) withstand the external process "
            "pressure. A tube under external pressure can collapse (crush) or buckle; the tip, "
            "a flat or hemispherical cap, can dent."),
        "why": ("Una vaina colapsada deja de alojar el sensor y puede filtrar.",
                "A collapsed well no longer houses the sensor and may leak."),
        "worked": (
            "Vaina de 316 con A 26,7 y d 6,6 mm: P_c del orden de cientos de bar; rara vez "
            "manda salvo en paredes delgadas o alta temperatura.",
            "316 well with A 26.7 and d 6.6 mm: P_c in the order of hundreds of bar; it "
            "rarely governs except with thin walls or high temperature."),
        "mistakes": ("- No sumar el sobreespesor consumido.",
                     "- Not accounting for consumed allowance."),
    },
    "crit.flange_rating": {
        "essence": (
            "Compara la presión de diseño con la presión admisible de la brida según su clase, "
            "grupo de material y temperatura. Los ratings salen de tablas que contemplan la "
            "resistencia de la brida, los bulones y la junta.",
            "It compares design pressure with the flange's allowable pressure for its class, "
            "material group and temperature. Ratings come from tables covering flange, bolt "
            "and gasket strength."),
        "why": ("La brida es frontera de presión: si no alcanza, hay riesgo de fuga.",
                "The flange is a pressure boundary: if insufficient, there is leak risk."),
        "worked": ("Diseño 40 bar a 250 °C, 316 clase 300: ≈ 40,6 bar → cumple justo.",
                   "Design 40 bar at 250 °C, 316 class 300: ≈ 40.6 bar → passes just."),
        "mistakes": ("- Usar la tabla del grupo del acero al carbono para un inoxidable.",
                     "- Using the carbon steel group table for stainless."),
    },
    "crit.steady_stress": {
        "essence": (
            "Verifica que el esfuerzo combinado constante (flexión por arrastre más presión) "
            "no haga fluir el metal. El factor 1,5 sobre S refleja que la flexión tiene "
            "reserva plástica: la sección no falla cuando la fibra externa fluye, sino cuando "
            "toda la sección se plastifica.",
            "It checks that the constant combined stress (drag bending plus pressure) does not "
            "make the metal yield. The 1.5 factor on S reflects that bending has plastic "
            "reserve: the section does not fail when the outer fibre yields, but when the "
            "whole section plasticizes."),
        "why": ("Evita que la vaina se doble de forma permanente.",
                "It prevents the well from bending permanently."),
        "worked": ("S_vm = 60 MPa, S = 115 MPa → límite 172 MPa → 35 % del límite.",
                   "S_vm = 60 MPa, S = 115 MPa → limit 172 MPa → 35 % of limit."),
        "mistakes": ("- Confundirlo con el criterio de fatiga.",
                     "- Confusing it with the fatigue criterion."),
    },
    "crit.dynamic_stress": {
        "essence": (
            "Verifica que la amplitud del esfuerzo oscilante quede por debajo del límite de "
            "fatiga, corregido por temperatura (F_T) y ambiente (F_E). La fatiga no depende "
            "de un esfuerzo máximo sino de la cantidad de ciclos: por debajo del límite, el "
            "acero soporta ciclos indefinidamente.",
            "It checks that the oscillating stress amplitude stays below the fatigue limit, "
            "corrected for temperature (F_T) and environment (F_E). Fatigue does not depend on "
            "a peak stress but on the number of cycles: below the limit, steel takes cycles "
            "indefinitely."),
        "why": ("Es el criterio que previene la rotura en la raíz.",
                "It is the criterion that prevents root fracture."),
        "worked": ("S_o = 15 MPa, F_T·F_E·S_f = 0,95 × 1 × 21 = 20 MPa → 75 %.",
                   "S_o = 15 MPa, F_T·F_E·S_f = 0.95 × 1 × 21 = 20 MPa → 75 %."),
        "mistakes": ("- Dejar F_E = 1 en servicios corrosivos.",
                     "- Leaving F_E = 1 in corrosive services."),
    },
    "crit.frequency_limit": {
        "essence": (
            "Verifica que la frecuencia de estela no se acerque a la natural instalada. Hay dos "
            "resonancias: la transversal (r = 1, fuerza grande) y la en línea (r = 0,5, fuerza "
            "chica pero frecuente en gases densos y líquidos). Con poco amortiguamiento "
            "(Scruton bajo) hay que quedar debajo de ambas (r < 0,4); con suficiente, la en "
            "línea se suprime y basta r < 0,8.",
            "It checks that wake frequency does not approach the installed natural frequency. "
            "There are two resonances: transverse (r = 1, large force) and in-line (r = 0.5, "
            "small force but common in dense gases and liquids). With little damping (low "
            "Scruton) the well must stay below both (r < 0.4); with enough, in-line is "
            "suppressed and r < 0.8 suffices."),
        "why": ("Es el criterio que más vainas rechaza en servicios de gas.",
                "It is the criterion that rejects the most wells in gas services."),
        "worked": ("r = 0,45 con N_Sc = 0,4 → no cumple; con N_Sc = 3 → cumple.",
                   "r = 0.45 with N_Sc = 0.4 → fail; with N_Sc = 3 → pass."),
        "mistakes": ("- Suponer que 0,8 aplica siempre.",
                     "- Assuming 0.8 always applies."),
    },
    "crit.inline_lockin_dwell": {
        "essence": (
            "Cuando la vaina opera por encima de la resonancia en línea, en cada arranque o "
            "cambio de caudal la atraviesa. Durante ese paso la amplitud crece; si el paso es "
            "breve y el esfuerzo en la banda es aceptable, se admite.",
            "When the well runs above in-line resonance, it crosses it at each start-up or "
            "flow change. During that passage amplitude grows; if the passage is brief and "
            "stress in the band is acceptable, it is allowed."),
        "why": ("Permite vainas que operan cómodas a alta velocidad sin quedarse en "
                "resonancia.",
                "It allows wells that run comfortably at high velocity without dwelling in "
                "resonance."),
        "worked": (
            "V_IR = 18 m/s, operación a 25 m/s, rampa de 2 minutos: el paso dura segundos; TS "
            "verifica el esfuerzo en la banda.",
            "V_IR = 18 m/s, operation at 25 m/s, 2-minute ramp: the passage lasts seconds; TS "
            "checks stress in the band."),
        "mistakes": ("- Habilitarlo en procesos que pueden quedarse a caudal intermedio.",
                     "- Enabling it in processes that may stay at intermediate flow."),
    },
    "crit.fatigue_data": {
        "essence": (
            "La norma tabula límites de fatiga para familias de materiales. Si el material "
            "elegido no está, el límite se estima y el resultado es menos confiable.",
            "The standard tabulates fatigue limits for material families. If the chosen "
            "material is not there, the limit is estimated and the result is less reliable."),
        "why": ("El revisor debe saber si el límite de fatiga tiene respaldo de la norma.",
                "The reviewer must know whether the fatigue limit is backed by the standard."),
        "worked": ("Titanio grado 2: sin dato tabulado → TS lo informa.",
                   "Titanium grade 2: no tabulated value → TS reports it."),
        "mistakes": ("- Ignorar el aviso.", "- Ignoring the warning."),
    },
    "topic.auto": {
        "essence": (
            "Resume lo que TS eligió por vos en los bloques automáticos y por qué: material, "
            "conexión, perfil y cotas, y vaina del sensor. Cada decisión cita el dato de "
            "proceso que la motivó y las alternativas.",
            "It summarizes what TS chose for you in automatic blocks and why: material, "
            "connection, profile and dimensions, and sensor sheath. Each decision cites the "
            "process datum behind it and the alternatives."),
        "why": ("Un cálculo automático sin justificación no es auditable.",
                "An automatic calculation without justification is not auditable."),
        "worked": ("«Roscada: agua ≤ 20 barg y ≤ 200 °C» explica por qué no se eligió brida.",
                   "«Threaded: water ≤ 20 barg and ≤ 200 °C» explains why no flange was "
                   "chosen."),
        "mistakes": ("- Aceptar la elección sin leer la justificación.",
                     "- Accepting the choice without reading the justification."),
    },
    "topic.erosion": {
        "essence": ("Semáforo de erosión con la peor relación V/V_e.",
                    "Erosion traffic light with the worst V/V_e ratio."),
        "why": ("La erosión no está en la norma de vainas pero es causa real de falla.",
                "Erosion is not in the thermowell standard but is a real failure cause."),
        "worked": ("V/V_e = 0,76 → amarillo: evaluar sobreespesor o Stellite.",
                   "V/V_e = 0.76 → amber: consider allowance or Stellite."),
        "mistakes": ("- Ignorarlo porque «no es ASME».", "- Ignoring it because «it is not "
                                                          "ASME»."),
    },
    "topic.frequency": {
        "essence": ("Veredicto del riesgo de resonancia en todos los casos.",
                    "Verdict on resonance risk across all cases."),
        "why": ("Es la causa principal de rotura de vainas.",
                "It is the main cause of thermowell fracture."),
        "worked": ("Rojo en el caso máximo, verde en el normal → manda el rojo.",
                   "Red in the maximum case, green in normal → red governs."),
        "mistakes": ("- Mirar solo el caso normal.", "- Looking only at normal."),
    },
    "topic.stress": {
        "essence": ("Veredicto de esfuerzos estáticos (fluencia) y dinámicos (fatiga).",
                    "Verdict on static (yield) and dynamic (fatigue) stresses."),
        "why": ("Una vaina puede cumplir frecuencia y fallar por fatiga.",
                "A well can pass frequency and fail by fatigue."),
        "worked": ("r = 0,35 pero S_o al 110 % → no cumple.",
                   "r = 0.35 but S_o at 110 % → fail."),
        "mistakes": ("- Creer que verde en frecuencia implica verde en esfuerzos.",
                     "- Believing green on frequency implies green on stress."),
    },
    "topic.pressure": {
        "essence": ("Veredicto de presión admisible, rating de brida y temperatura del "
                    "material.",
                    "Verdict on allowable pressure, flange rating and material temperature."),
        "why": ("La vaina es parte de la envolvente de presión de la línea.",
                "The well is part of the line's pressure boundary."),
        "worked": ("Brida clase 150 con 25 bar de diseño → rojo.",
                   "Class 150 flange with 25 bar design → red."),
        "mistakes": ("- Usar presión de operación.", "- Using operating pressure."),
    },
    "topic.overall": {
        "essence": (
            "Estado global: el peor de todos los temas y casos. Verde = cumple; amarillo = "
            "cumple con poco margen o requiere revisión; rojo = no cumple.",
            "Overall status: the worst of all topics and cases. Green = passes; amber = "
            "passes with little margin or needs review; red = fails."),
        "why": ("Es lo que mira primero quien aprueba el diseño.",
                "It is what the approver looks at first."),
        "worked": ("Todo verde salvo erosión amarilla → global amarillo.",
                   "All green except amber erosion → overall amber."),
        "mistakes": ("- Aprobar en amarillo sin leer la causa.",
                     "- Approving amber without reading the cause."),
    },
}
