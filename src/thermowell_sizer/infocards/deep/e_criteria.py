"""Segunda pasada: criterios de aceptación y temas del veredicto."""

from __future__ import annotations

from typing import Any

DEEP: dict[str, dict[str, Any]] = {
    "topic.frequency": {
        "essence": (
            "Este tema responde una sola pregunta: ¿puede el flujo hacer vibrar la vaina en "
            "su propia frecuencia? Junta dos verificaciones:\n\n"
            "- Límite de frecuencia: la frecuencia de estela f_s (cuántos remolinos por "
            "segundo suelta el flujo detrás de la vaina) tiene que quedar bien por debajo de "
            "la frecuencia natural instalada f_n,c. Si se acercan, cada remolino empuja la "
            "vaina justo cuando ya se está moviendo en ese sentido, como empujar una hamaca "
            "en el momento justo, y la amplitud crece ciclo a ciclo.\n"
            "- Paso por resonancia en línea: si la vaina opera por encima de la resonancia "
            "en línea (a la mitad de la frecuencia natural), se verifica que el esfuerzo al "
            "atravesarla durante arranques o paradas sea aceptable.",
            "This topic answers a single question: can the flow make the well vibrate at its "
            "own frequency? It combines two checks:\n\n"
            "- Frequency limit: the wake frequency f_s (how many eddies per second the flow "
            "sheds behind the well) must stay well below installed natural frequency f_n,c. "
            "If they approach, each eddy pushes the well just when it is already moving that "
            "way, like pushing a swing at the right moment, and amplitude grows cycle after "
            "cycle.\n"
            "- In-line resonance passage: if the well runs above in-line resonance (at half "
            "the natural frequency), the stress while crossing it during start-ups or "
            "shutdowns is checked."),
        "why": (
            "Es la causa de casi todas las roturas de termovainas en servicio: la fatiga por "
            "vibración inducida por vórtices puede cortar una vaina de acero en horas. Un "
            "rojo acá no se compensa con ningún otro verde.",
            "It is the cause of almost every thermowell failure in service: "
            "vortex-induced-vibration fatigue can snap a steel well in hours. A red here is "
            "not offset by any other green."),
        "worked": (
            "f_n,c = 620 Hz, peor caso f_s = 210 Hz:\n\n"
            "1. r = 210 / 620 = 0,34.\n"
            "2. Con Scruton bajo (gas, poco amortiguamiento) el límite es 0,4: 0,34 < 0,4 → "
            "cumple, con un 15 % de margen.\n"
            "3. Si la velocidad sube un 20 % en un caso futuro, f_s = 252 Hz, r = 0,41 → no "
            "cumple. Por eso conviene cargar el caso de máximo caudal.",
            "f_n,c = 620 Hz, worst case f_s = 210 Hz:\n\n"
            "1. r = 210 / 620 = 0.34.\n"
            "2. With low Scruton (gas, little damping) the limit is 0.4: 0.34 < 0.4 → passes, "
            "with 15 % margin.\n"
            "3. If velocity rises 20 % in a future case, f_s = 252 Hz, r = 0.41 → fails. "
            "That is why the maximum-flow case should be entered."),
        "mistakes": (
            "- Evaluar solo el caudal normal y no el máximo.\n"
            "- Aceptar un amarillo sin revisar qué tan inciertos son los datos de caudal.\n"
            "- Creer que un collar de velocidad «arregla» la frecuencia sin verificar el "
            "contacto real con el niple.",
            "- Evaluating only normal flow, not maximum.\n"
            "- Accepting an amber without checking how uncertain the flow data are.\n"
            "- Believing a velocity collar «fixes» frequency without checking actual contact "
            "with the nozzle."),
    },
    "topic.erosion": {
        "essence": (
            "Compara la velocidad del fluido con la velocidad erosiva V_e, la velocidad a "
            "partir de la cual el flujo empieza a arrancar material de la superficie. El "
            "mecanismo depende del fluido:\n\n"
            "- Gas con partículas (arena, polvo de catalizador): cada grano golpea como un "
            "proyectil; la pérdida de metal crece aproximadamente con la velocidad elevada a "
            "2 o 3.\n"
            "- Líquido con burbujas o gotas a alta velocidad: impacto de gotas y cavitación, "
            "que arrancan la capa protectora de óxido.\n"
            "- Corrosión-erosión: el flujo barre la película pasiva que protege al metal y lo "
            "deja corroerse sin freno.\n\n"
            "TS informa la relación V/V_e del peor caso.",
            "It compares fluid velocity with erosional velocity V_e, the speed above which "
            "the flow starts removing material from the surface. The mechanism depends on the "
            "fluid:\n\n"
            "- Gas with particles (sand, catalyst dust): each grain strikes like a "
            "projectile; metal loss grows roughly with velocity to the power 2 or 3.\n"
            "- Liquid with bubbles or droplets at high speed: droplet impact and cavitation, "
            "which strip the protective oxide layer.\n"
            "- Erosion-corrosion: the flow sweeps away the passive film protecting the metal "
            "and lets it corrode unchecked.\n\n"
            "TS reports the V/V_e ratio of the worst case."),
        "why": (
            "La erosión no rompe la vaina de golpe: la adelgaza. Una punta más fina vibra a "
            "otra frecuencia, soporta menos presión y, al final, se perfora y deja salir el "
            "proceso por el agujero del sensor.",
            "Erosion does not break the well at once: it thins it. A thinner tip vibrates at "
            "another frequency, holds less pressure and, eventually, perforates and lets "
            "process out through the sensor bore."),
        "worked": (
            "Gas húmedo, V = 18 m/s, V_e = 20 m/s → V/V_e = 0,9 → amarillo.\n\n"
            "Si la erosión crece con V³, pasar de 18 a 22 m/s multiplica el desgaste por "
            "(22/18)³ = 1,8. Opciones: punta con Stellite, más sobreespesor o una ubicación "
            "aguas abajo de un tramo recto donde el flujo sea más uniforme.",
            "Wet gas, V = 18 m/s, V_e = 20 m/s → V/V_e = 0.9 → amber.\n\n"
            "If erosion grows with V³, going from 18 to 22 m/s multiplies wear by "
            "(22/18)³ = 1.8. Options: Stellite tip, more allowance or a location downstream "
            "of a straight run where the flow is more uniform."),
        "mistakes": (
            "- Marcar el servicio como no erosivo cuando hay arena o catalizador.\n"
            "- Instalar la vaina justo después de un codo o una válvula reductora, donde la "
            "velocidad local es mayor que la media.",
            "- Marking the service non-erosive when there is sand or catalyst.\n"
            "- Installing the well right after an elbow or a reducing valve, where local "
            "velocity exceeds the mean."),
    },
    "topic.pressure": {
        "essence": (
            "La vaina es parte de la frontera de presión: si falla, el proceso sale por el "
            "agujero del sensor. Este tema junta tres verificaciones de esa frontera:\n\n"
            "- Presión admisible del vástago y de la punta: la presión externa intenta "
            "aplastar el tubo y abollar el fondo; se compara con lo que admite la geometría "
            "con el esfuerzo admisible del material.\n"
            "- Rating de brida: la brida debe admitir la presión de diseño a la temperatura "
            "de diseño.\n"
            "- Temperatura del material: el material debe estar dentro del rango donde sus "
            "propiedades son válidas.",
            "The well is part of the pressure boundary: if it fails, process escapes through "
            "the sensor bore. This topic combines three checks of that boundary:\n\n"
            "- Shank and tip allowable pressure: external pressure tries to crush the tube "
            "and dent the bottom; it is compared with what the geometry allows at the "
            "material's allowable stress.\n"
            "- Flange rating: the flange must hold design pressure at design temperature.\n"
            "- Material temperature: the material must be within the range where its "
            "properties are valid."),
        "why": (
            "En vainas de proceso típicas este tema casi siempre sobra, porque el vástago es "
            "grueso. Se vuelve crítico en alta presión, alta temperatura, puntas finas o "
            "vainas muy corroídas, y un error acá es una fuga, no una vibración.",
            "For typical process wells this topic almost always has margin, because the "
            "shank is thick. It becomes critical at high pressure, high temperature, thin "
            "tips or heavily corroded wells, and an error here is a leak, not a vibration."),
        "worked": (
            "Diseño 95 bar a 350 °C, vaina 316 brida clase 600:\n\n"
            "- Vástago: P_c ≈ 700 bar → sobra.\n"
            "- Brida 600 grupo 2.2 a 350 °C ≈ 72 bar < 95 bar → no cumple. Hay que subir a "
            "clase 900.",
            "Design 95 bar at 350 °C, 316 well, class 600 flange:\n\n"
            "- Shank: P_c ≈ 700 bar → ample.\n"
            "- Class 600 group 2.2 flange at 350 °C ≈ 72 bar < 95 bar → fails. Class 900 is "
            "needed."),
        "mistakes": (
            "- Cargar la presión de operación en lugar de la de diseño.\n"
            "- Mirar solo el vástago y olvidar la brida.",
            "- Entering operating pressure instead of design.\n"
            "- Looking only at the shank and forgetting the flange."),
    },
    "topic.stress": {
        "essence": (
            "Dos formas distintas de romper la vaina por esfuerzo:\n\n"
            "- Esfuerzo estacionario: la suma de la presión que comprime el vástago y el "
            "arrastre constante del flujo que lo dobla. Se combinan con el criterio de von "
            "Mises, que convierte un estado de esfuerzos en varias direcciones en un único "
            "valor comparable con el material. Si se pasa, la vaina se deforma de forma "
            "permanente (fluencia).\n"
            "- Esfuerzo dinámico: la parte que oscila con la estela, millones de veces por "
            "día. Aunque sea pequeño, cada ciclo puede hacer avanzar una fisura microscópica. "
            "Se compara con el límite de fatiga: el nivel por debajo del cual el metal "
            "aguanta ciclos indefinidamente.",
            "Two different ways stress breaks the well:\n\n"
            "- Steady stress: the sum of pressure compressing the shank and constant flow "
            "drag bending it. They are combined with the von Mises criterion, which turns a "
            "multi-directional stress state into a single value comparable with the material. "
            "If exceeded, the well deforms permanently (yield).\n"
            "- Dynamic stress: the part oscillating with the wake, millions of times a day. "
            "Even if small, each cycle can advance a microscopic crack. It is compared with "
            "the fatigue limit: the level below which metal survives cycles indefinitely."),
        "why": (
            "El esfuerzo dinámico suele ser el que manda: el límite de fatiga de un acero "
            "soldado es del orden de 20 MPa, diez veces menos que su fluencia. Una vaina que "
            "aguanta perfectamente la carga estática puede fatigarse.",
            "Dynamic stress usually governs: a welded steel's fatigue limit is around 20 MPa, "
            "ten times less than its yield. A well that holds static load perfectly may still "
            "fatigue."),
        "worked": (
            "Vaina 316 soldada, S = 138 MPa, límite de fatiga 21 MPa:\n\n"
            "- S_vm = 60 MPa < 1,5 × 138 = 207 MPa → estacionario cumple con amplio margen.\n"
            "- S_o = 24 MPa > 21 MPa → dinámico no cumple. La solución es mecánica (más rigidez "
            "o menos largo), no un material más resistente: el límite de fatiga de los "
            "aceros cambia poco con la resistencia.",
            "Welded 316 well, S = 138 MPa, fatigue limit 21 MPa:\n\n"
            "- S_vm = 60 MPa < 1.5 × 138 = 207 MPa → steady passes with ample margin.\n"
            "- S_o = 24 MPa > 21 MPa → dynamic fails. The fix is mechanical (more stiffness or "
            "less length), not a stronger material: steels' fatigue limit changes little with "
            "strength."),
        "mistakes": (
            "- Pensar que un material más «fuerte» resuelve la fatiga.\n"
            "- Ignorar el factor de concentración en la raíz (radio de acuerdo).",
            "- Thinking a «stronger» material solves fatigue.\n"
            "- Ignoring the root stress concentration factor (fillet radius)."),
    },
    "topic.overall": {
        "essence": (
            "El estado global es el peor de todos los temas, evaluado en todos los casos de "
            "flujo y en los estados nueva y corroída. No es un promedio: una sola "
            "verificación roja vuelve rojo el diseño entero, igual que una cadena se corta por "
            "el eslabón más débil.\n\n"
            "- Verde: todas las verificaciones cumplen con margen.\n"
            "- Amarillo: todo cumple, pero alguna está dentro del margen de advertencia.\n"
            "- Rojo: al menos una no cumple.",
            "Overall status is the worst of all topics, evaluated over every flow case and "
            "the new and corroded states. It is not an average: a single red check turns the "
            "whole design red, just as a chain breaks at its weakest link.\n\n"
            "- Green: every check passes with margin.\n"
            "- Amber: everything passes, but some check is within the warning margin.\n"
            "- Red: at least one fails."),
        "why": (
            "Es lo que se lee primero y lo que va a la hoja de datos. Antes de emitir hay que "
            "abrir el tema que manda y entender por qué.",
            "It is what is read first and what goes on the datasheet. Before issuing, open "
            "the governing topic and understand why."),
        "worked": (
            "Frecuencia verde (r = 0,30), erosión amarilla (V/V_e = 0,93), presión y esfuerzos "
            "verdes → global amarillo. La acción es sobre erosión, no sobre la geometría.",
            "Frequency green (r = 0.30), erosion amber (V/V_e = 0.93), pressure and stress "
            "green → overall amber. The action is on erosion, not geometry."),
        "mistakes": (
            "- Emitir un amarillo sin decir en el informe qué tema lo causa.\n"
            "- Cambiar la geometría cuando el problema es de material o de rating.",
            "- Issuing an amber without stating in the report which topic causes it.\n"
            "- Changing geometry when the problem is material or rating."),
    },
    "topic.auto": {
        "essence": (
            "Cuando un bloque está en «Automático», TS elige el valor y deja escrito por qué: "
            "la regla que aplicó, el dato de proceso que la disparó y qué alternativas "
            "descartó. Es la memoria de cálculo de las decisiones, no solo de los números.\n\n"
            "Por ejemplo: «316/316L: compatible con el fluido, sin H₂S, cloruros por debajo "
            "del umbral; alternativa Duplex si los cloruros superan 50 ppm a más de 60 °C».",
            "When a block is in «Automatic», TS chooses the value and writes down why: the "
            "rule applied, the process datum that triggered it and the alternatives "
            "discarded. It is the calculation record of the decisions, not only the "
            "numbers.\n\n"
            "For example: «316/316L: compatible with the fluid, no H₂S, chlorides below the "
            "threshold; alternative Duplex if chlorides exceed 50 ppm above 60 °C»."),
        "why": (
            "Un revisor tiene que poder reconstruir cada decisión. Si el dato de entrada "
            "estaba mal (por ejemplo, cloruros omitidos), la justificación lo deja en "
            "evidencia.",
            "A reviewer must be able to reconstruct every decision. If an input was wrong "
            "(for example, chlorides omitted), the justification makes it visible."),
        "worked": (
            "Gas a 60 bar y 300 °C: «Bridada clase 600 RF: la clase 300 admite ≈ 37 bar a "
            "300 °C, menos que el diseño». Si el cliente exige clase 900, se pasa el bloque a "
            "manual y se carga.",
            "Gas at 60 bar and 300 °C: «Flanged class 600 RF: class 300 holds ≈ 37 bar at "
            "300 °C, less than design». If the client requires class 900, switch the block to "
            "manual and enter it."),
        "mistakes": (
            "- Aceptar la selección sin leer la justificación.\n"
            "- Usar una selección automática como sustituto de la especificación del cliente.",
            "- Accepting the selection without reading the justification.\n"
            "- Using an automatic selection as a substitute for the client specification."),
    },
    "crit.fatigue_data": {
        "essence": (
            "Para verificar el esfuerzo dinámico hace falta saber cuánto aguanta el material "
            "a la fatiga. La norma tabula ese límite para grupos de materiales comunes "
            "(aceros al carbono, inoxidables austeníticos, algunas aleaciones de níquel), "
            "obtenido de ensayos con millones de ciclos. Para materiales fuera de esas tablas "
            "no hay un valor reconocido.\n\n"
            "El límite de fatiga no se deduce de la resistencia a la tracción con "
            "confianza: depende de la microestructura, las inclusiones, la superficie y el "
            "ambiente.",
            "To check dynamic stress you need to know how much the material withstands in "
            "fatigue. The standard tabulates that limit for common material groups (carbon "
            "steels, austenitic stainless, some nickel alloys), obtained from tests with "
            "millions of cycles. For materials outside those tables there is no recognised "
            "value.\n\n"
            "The fatigue limit cannot be confidently deduced from tensile strength: it "
            "depends on microstructure, inclusions, surface and environment."),
        "why": (
            "Sin datos, TS no puede aprobar la verificación dinámica: la marca como no "
            "evaluable. Hace falta un dato documentado del proveedor del material o elegir un "
            "material con datos.",
            "Without data TS cannot pass the dynamic check: it marks it as not evaluable. A "
            "documented value from the material supplier is needed, or a material with data "
            "must be chosen."),
        "worked": (
            "316 y acero al carbono: con datos. Tantalio o circonio: sin datos en la norma; "
            "se puede usar un valor del fabricante con su referencia, cargado como "
            "propiedad manual.",
            "316 and carbon steel: with data. Tantalum or zirconium: no data in the "
            "standard; a manufacturer value with its reference can be used, entered as a "
            "manual property."),
        "mistakes": (
            "- Usar el límite de un acero para una aleación exótica.\n"
            "- Tomar la resistencia a la tracción dividida por 2 como límite de fatiga.",
            "- Using a steel's limit for an exotic alloy.\n"
            "- Taking tensile strength divided by 2 as the fatigue limit."),
    },
    "crit.flange_rating": {
        "essence": (
            "Compara la presión de diseño con la presión admisible de la brida de la vaina "
            "según ASME B16.5, para su clase, su grupo de material y la temperatura de "
            "diseño. Las tablas de la norma ya incluyen la pérdida de resistencia del metal "
            "con la temperatura: por eso una misma brida admite menos presión en caliente.",
            "It compares design pressure with the thermowell flange allowable pressure per "
            "ASME B16.5, for its class, material group and design temperature. The standard's "
            "tables already include metal strength loss with temperature: that is why the "
            "same flange holds less pressure when hot."),
        "why": (
            "La brida es la unión con la cañería: si no alcanza, la junta pierde o la brida "
            "se deforma. También debe coincidir con la clase de la línea para que el "
            "conjunto sea consistente.",
            "The flange is the joint with the piping: if short, the gasket leaks or the "
            "flange deforms. It must also match the line class for a consistent assembly."),
        "worked": (
            "Acero al carbono (grupo 1.1) clase 150: ≈ 19,6 bar a 38 °C, ≈ 13,8 bar a "
            "200 °C. Diseño 15 bar a 200 °C → no cumple; clase 300 (≈ 43,8 bar) sí.",
            "Carbon steel (group 1.1) class 150: ≈ 19.6 bar at 38 °C, ≈ 13.8 bar at 200 °C. "
            "Design 15 bar at 200 °C → fails; class 300 (≈ 43.8 bar) passes."),
        "mistakes": (
            "- Usar el valor a temperatura ambiente.\n"
            "- Elegir el grupo de material de la cañería y no el de la vaina.",
            "- Using the ambient-temperature value.\n"
            "- Choosing the pipe's material group instead of the well's."),
    },
    "crit.steady_stress": {
        "essence": (
            "Verifica que el esfuerzo constante en la raíz no deforme la vaina. En la raíz se "
            "suman tres efectos: la flexión por el arrastre medio del flujo, la compresión "
            "axial y la compresión radial por la presión externa. El criterio de von Mises "
            "los combina en un esfuerzo equivalente S_vm, que se compara con 1,5 veces el "
            "esfuerzo admisible S. El factor 1,5 refleja que la flexión es un esfuerzo "
            "secundario local: la sección no colapsa cuando la fibra exterior empieza a "
            "fluir, porque el centro sigue elástico.",
            "It checks that constant root stress does not deform the well. At the root three "
            "effects add up: bending from mean flow drag, axial compression and radial "
            "compression from external pressure. The von Mises criterion combines them into "
            "an equivalent stress S_vm, compared with 1.5 times allowable stress S. The 1.5 "
            "factor reflects that bending is a local secondary stress: the section does not "
            "collapse when the outer fibre starts to yield, because the core remains "
            "elastic."),
        "why": (
            "Rara vez manda, pero en líquidos densos a alta velocidad o vainas largas el "
            "arrastre puede ser grande y doblar la vaina de forma permanente.",
            "It rarely governs, but in dense liquids at high velocity or long wells drag can "
            "be large and permanently bend the well."),
        "worked": (
            "S = 138 MPa → límite 207 MPa. Agua a 4 m/s, U = 400 mm: S_vm ≈ 85 MPa → cumple. "
            "Mismo caso con U = 600 mm: el momento crece (600/400)² = 2,25 veces → S_vm "
            "≈ 180 MPa, cerca del límite.",
            "S = 138 MPa → limit 207 MPa. Water at 4 m/s, U = 400 mm: S_vm ≈ 85 MPa → passes. "
            "Same case with U = 600 mm: moment grows (600/400)² = 2.25 times → S_vm "
            "≈ 180 MPa, near the limit."),
        "mistakes": ("- Usar S a temperatura ambiente para un servicio caliente.",
                     "- Using ambient S for a hot service."),
    },
    "crit.dynamic_stress": {
        "essence": (
            "Verifica que el esfuerzo oscilante en la raíz quede debajo del límite de fatiga "
            "corregido. El esfuerzo oscilante S_o es la parte que va y viene con la estela "
            "(arrastre oscilante en línea y sustentación transversal). Si la vaina está cerca "
            "de una resonancia, la respuesta se amplifica.\n\n"
            "El límite de fatiga se corrige por la concentración de esfuerzos de la raíz, "
            "el estado del metal (soldado o mecanizado) y el ambiente. Una fisura de fatiga "
            "nace en la superficie, en el punto de mayor esfuerzo, y avanza un poco con cada "
            "ciclo hasta que la sección restante no aguanta.",
            "It checks that oscillating root stress stays below the corrected fatigue limit. "
            "Oscillating stress S_o is the part going back and forth with the wake (in-line "
            "oscillating drag and transverse lift). If the well is near a resonance, response "
            "is amplified.\n\n"
            "The fatigue limit is corrected for root stress concentration, metal state "
            "(welded or machined) and environment. A fatigue crack starts at the surface at "
            "the highest-stress point and advances a little each cycle until the remaining "
            "section cannot hold."),
        "why": (
            "A 200 Hz, la vaina acumula 17 millones de ciclos por día: cualquier esfuerzo "
            "por encima del límite termina rompiéndola en poco tiempo.",
            "At 200 Hz the well accumulates 17 million cycles a day: any stress above the "
            "limit ends up breaking it quickly."),
        "worked": (
            "Límite 316 soldado ≈ 21 MPa, F_E = 1. S_o = 12 MPa → cumple (57 %). Con F_E = 0,5 "
            "en agua de mar, el límite pasa a 10,5 MPa → no cumple.",
            "Welded 316 limit ≈ 21 MPa, F_E = 1. S_o = 12 MPa → passes (57 %). With F_E = 0.5 "
            "in seawater the limit becomes 10.5 MPa → fails."),
        "mistakes": (
            "- Declarar «no soldado» para una vaina con brida soldada.\n"
            "- Dejar F_E = 1 en un ambiente corrosivo.",
            "- Declaring «not welded» for a well with a welded flange.\n"
            "- Leaving F_E = 1 in a corrosive environment."),
    },
    "crit.pressure_rating": {
        "essence": (
            "Compara la presión de diseño con dos presiones admisibles de la propia vaina:\n\n"
            "- P_c, del vástago: la presión externa intenta reducir el diámetro del tubo. "
            "Resiste la pared entre el agujero y el exterior; cuanto más gruesa en relación "
            "con el diámetro, más presión aguanta.\n"
            "- P_t, de la punta: el fondo cerrado actúa como una pequeña tapa empujada desde "
            "afuera.\n\n"
            "Ambas se calculan con el esfuerzo admisible a la temperatura de diseño.",
            "It compares design pressure with two allowable pressures of the well itself:\n\n"
            "- P_c, shank: external pressure tries to reduce the tube diameter. The wall "
            "between bore and outside resists it; the thicker relative to diameter, the more "
            "pressure it holds.\n"
            "- P_t, tip: the closed bottom acts like a small cap pushed from outside.\n\n"
            "Both use allowable stress at design temperature."),
        "why": (
            "Es la frontera de presión del instrumento: si falla, el proceso sale al "
            "ambiente por el cabezal.",
            "It is the instrument's pressure boundary: if it fails, process escapes through "
            "the head."),
        "worked": (
            "Punta 15,9 mm con agujero 6,6 mm: pared 4,65 mm, admite cientos de bar. Con "
            "agujero 9,8 mm la pared queda en 3,05 mm y la admisible cae aproximadamente un "
            "35 %.",
            "15.9 mm tip with a 6.6 mm bore: 4.65 mm wall, holds hundreds of bar. With a "
            "9.8 mm bore the wall is 3.05 mm and allowable falls roughly 35 %."),
        "mistakes": ("- Verificar solo la vaina nueva y no la corroída.",
                     "- Checking only the new well and not the corroded one."),
    },
    "crit.inline_lockin_dwell": {
        "essence": (
            "La estela empuja la vaina en dos direcciones: de costado (transversal), a la "
            "frecuencia f_s, y en la dirección del flujo (en línea), al doble, 2·f_s, porque "
            "cada remolino, sea de arriba o de abajo, tira hacia atrás. Por eso existe una "
            "resonancia en línea cuando f_s está cerca de la mitad de la frecuencia natural.\n\n"
            "Si se acepta operar por encima de ella, la vaina la atraviesa en cada arranque y "
            "parada. Este criterio verifica que el esfuerzo durante ese paso, amplificado por "
            "la resonancia, sea aceptable.",
            "The wake pushes the well in two directions: sideways (transverse), at f_s, and "
            "along the flow (in-line), at twice that, 2·f_s, because each eddy, whether top "
            "or bottom, pulls backwards. That is why there is an in-line resonance when f_s "
            "is near half the natural frequency.\n\n"
            "If running above it is accepted, the well crosses it at every start-up and "
            "shutdown. This criterion checks that stress during that passage, amplified by "
            "resonance, is acceptable."),
        "why": (
            "Permite diseños más largos en gases, pero solo si el paso es breve y el esfuerzo "
            "en resonancia no inicia fisuras.",
            "It allows longer designs in gases, but only if the passage is brief and "
            "resonant stress does not start cracks."),
        "worked": (
            "f_n,c = 500 Hz → resonancia en línea en f_s ≈ 250 Hz. Operación a f_s = 300 Hz: "
            "al arrancar, la vaina pasa por 250 Hz. Si el esfuerzo amplificado es 15 MPa con "
            "límite 21 MPa, se acepta.",
            "f_n,c = 500 Hz → in-line resonance at f_s ≈ 250 Hz. Operation at f_s = 300 Hz: "
            "on start-up the well passes through 250 Hz. If amplified stress is 15 MPa with a "
            "21 MPa limit, it is accepted."),
        "mistakes": ("- Aceptarlo en líquidos, donde el lock-in en línea es más severo.",
                     "- Accepting it in liquids, where in-line lock-in is more severe."),
    },
    "crit.frequency_limit": {
        "essence": (
            "Fija cuánto puede acercarse la frecuencia de estela a la frecuencia natural. El "
            "límite depende del número de Scruton, que mide cuánta energía puede disipar la "
            "vaina frente a la que le entrega el fluido:\n\n"
            "- Scruton bajo (gases densos y líquidos, poco amortiguamiento): la vaina no puede "
            "frenar la resonancia en línea, así que hay que quedarse por debajo de ella: "
            "f_s < 0,4·f_n,c.\n"
            "- Scruton alto (gases livianos): la resonancia en línea casi no crece y se "
            "admite f_s < 0,8·f_n,c, siempre que se verifique el paso.",
            "It sets how close wake frequency may get to natural frequency. The limit depends "
            "on the Scruton number, which measures how much energy the well can dissipate "
            "relative to what the fluid supplies:\n\n"
            "- Low Scruton (dense gases and liquids, little damping): the well cannot curb "
            "in-line resonance, so it must stay below it: f_s < 0.4·f_n,c.\n"
            "- High Scruton (light gases): in-line resonance barely grows and f_s < "
            "0.8·f_n,c is allowed, provided the passage is checked."),
        "why": (
            "Es la verificación que más rechaza diseños. Entender qué límite aplica explica "
            "por qué una misma vaina cumple en aire y no en agua.",
            "It is the check that rejects most designs. Understanding which limit applies "
            "explains why the same well passes in air and fails in water."),
        "worked": (
            "f_n,c = 600 Hz: en agua el límite es 240 Hz; en gas liviano con Scruton alto, "
            "480 Hz. Una f_s de 300 Hz cumple en el segundo caso y no en el primero.",
            "f_n,c = 600 Hz: in water the limit is 240 Hz; in light gas with high Scruton, "
            "480 Hz. An f_s of 300 Hz passes the second and fails the first."),
        "mistakes": ("- Inflar el amortiguamiento para que el Scruton suba.",
                     "- Inflating damping so Scruton rises."),
    },
    "crit.material_temperature": {
        "essence": (
            "Cada material tiene un rango de temperatura donde sus propiedades tabuladas son "
            "válidas. Por arriba, el metal empieza a fluir lentamente bajo carga (creep), se "
            "oxida o cambia de microestructura (por ejemplo, la sensibilización de los "
            "inoxidables entre 450 y 850 °C, que los vuelve vulnerables a la corrosión "
            "intergranular). Por abajo, algunos aceros se vuelven frágiles y pueden romperse "
            "como vidrio ante un golpe.",
            "Each material has a temperature range where its tabulated properties are valid. "
            "Above it, metal starts to flow slowly under load (creep), oxidises or changes "
            "microstructure (for example sensitisation of stainless steels between 450 and "
            "850 °C, which makes them vulnerable to intergranular corrosion). Below it, some "
            "steels turn brittle and can shatter like glass under impact."),
        "why": (
            "Fuera de rango, el esfuerzo admisible y el módulo usados en el cálculo no "
            "representan al material real.",
            "Outside the range, the allowable stress and modulus used in the calculation do "
            "not represent the real material."),
        "worked": (
            "Acero al carbono A105 en servicio a −50 °C: por debajo de su rango sin ensayo de "
            "impacto → elegir A350 LF2 o inoxidable. 304 a 650 °C continuos: preferir 321 o "
            "347, estabilizados.",
            "A105 carbon steel at −50 °C: below its range without impact testing → choose "
            "A350 LF2 or stainless. 304 continuously at 650 °C: prefer 321 or 347, "
            "stabilised."),
        "mistakes": ("- Olvidar la temperatura mínima de diseño en servicios fríos o de "
                     "despresurización.",
                     "- Forgetting minimum design temperature in cold or depressurisation "
                     "services."),
    },
    "crit.scope": {
        "essence": (
            "Las fórmulas de la norma se validaron para un rango de geometrías: relaciones "
            "entre largo y diámetro, conicidad, radio de raíz y espesor mínimo de pared. "
            "Fuera de ese rango las fórmulas siguen dando números, pero ya no representan bien "
            "la física: por ejemplo, una vaina muy corta y gruesa se comporta más como un "
            "bloque que como una viga, y una muy delgada puede pandear.",
            "The standard's formulas were validated for a range of geometries: length to "
            "diameter ratios, taper, root radius and minimum wall thickness. Outside that "
            "range the formulas still produce numbers, but no longer represent the physics "
            "well: for example a very short thick well behaves more like a block than a beam, "
            "and a very thin one may buckle."),
        "why": (
            "Un resultado verde fuera de alcance no tiene respaldo de la norma. TS lo marca "
            "para que el ingeniero decida si hace falta un análisis por elementos finitos o "
            "un ensayo.",
            "A green result out of scope has no backing from the standard. TS flags it so the "
            "engineer decides whether finite-element analysis or a test is needed."),
        "worked": (
            "Pared en la punta de 2,5 mm cuando la norma pide un mínimo de unos 3 mm → fuera "
            "de alcance. Solución: agujero menor o punta mayor.",
            "Tip wall of 2.5 mm when the standard asks for a minimum of about 3 mm → out of "
            "scope. Fix: smaller bore or larger tip."),
        "mistakes": ("- Ignorar la advertencia porque el resto está verde.",
                     "- Ignoring the warning because the rest is green."),
    },
}
