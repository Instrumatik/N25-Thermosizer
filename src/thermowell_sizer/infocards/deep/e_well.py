"""Segunda pasada: fichas de geometría, conexión y sensor llevadas al nivel del modelo."""

from __future__ import annotations

from typing import Any

DEEP: dict[str, dict[str, Any]] = {
    "f.A": {
        "essence": (
            "Diámetro de la raíz, la sección donde la vaina se une a la conexión. En una viga "
            "en voladizo el momento flector es máximo justo ahí: toda la carga del flujo "
            "repartida a lo largo del vástago «cuelga» de esa sección.\n\n"
            "La geometría trabaja a favor: la rigidez a flexión de un tubo depende del momento "
            "de inercia I = π·(A⁴ − d⁴)/64, que crece con la cuarta potencia del diámetro, y la "
            "resistencia (módulo resistente I/(A/2)) crece con el cubo. El agujero d resta muy "
            "poco porque está cerca del eje, donde el metal aporta poca rigidez. Por eso unos "
            "pocos milímetros más de raíz cambian mucho el resultado.",
            "Root diameter, the section where the well joins the connection. In a cantilever "
            "the bending moment is maximum right there: all the flow load distributed along "
            "the shank «hangs» from that section.\n\n"
            "Geometry helps: a tube's bending stiffness depends on the moment of inertia "
            "I = π·(A⁴ − d⁴)/64, which grows with the fourth power of diameter, and strength "
            "(section modulus I/(A/2)) grows with the cube. Bore d subtracts very little "
            "because it sits near the axis, where metal adds little stiffness. That is why a "
            "few extra millimetres at the root change the result a lot."),
        "why": (
            "Engrosar la raíz sube la frecuencia natural y baja el esfuerzo de raíz a la vez, "
            "sin tocar la punta, que es la que manda en la estela (f_s ∝ 1/B) y en la "
            "respuesta térmica. Es la palanca preferida cuando no se puede acortar. El límite "
            "práctico lo pone la conexión: la raíz tiene que entrar en la brida o rosca y en el "
            "niple de montaje.",
            "Thickening the root raises natural frequency and lowers root stress at once, "
            "without touching the tip, which governs the wake (f_s ∝ 1/B) and thermal "
            "response. It is the preferred lever when the well cannot be shortened. The "
            "practical limit is the connection: the root must fit the flange or thread and the "
            "mounting nozzle."),
        "worked": (
            "Agujero d = 6,6 mm.\n\n"
            "1. A = 22,2 mm: I = π(22,2⁴ − 6,6⁴)/64 = 11 830 mm⁴; módulo = 1066 mm³.\n"
            "2. A = 26,7 mm: I = π(26,7⁴ − 6,6⁴)/64 = 24 860 mm⁴; módulo = 1862 mm³.\n\n"
            "Un 20 % más de diámetro da 2,1 veces la rigidez y 1,75 veces la resistencia: el "
            "esfuerzo en la raíz baja un 43 % con la misma carga.",
            "Bore d = 6.6 mm.\n\n"
            "1. A = 22.2 mm: I = π(22.2⁴ − 6.6⁴)/64 = 11,830 mm⁴; modulus = 1066 mm³.\n"
            "2. A = 26.7 mm: I = π(26.7⁴ − 6.6⁴)/64 = 24,860 mm⁴; modulus = 1862 mm³.\n\n"
            "20 % more diameter gives 2.1 times the stiffness and 1.75 times the strength: "
            "root stress drops 43 % under the same load."),
        "mistakes": (
            "- Pedir una raíz que no entra en el niple (revisar el Di de la conexión de "
            "montaje).\n"
            "- Engrosar la raíz y olvidar que en una roscada el diámetro lo limita la rosca.\n"
            "- Confundir A con el diámetro de la brida o del hexágono.",
            "- Asking for a root that does not fit the nozzle (check the mounting connection "
            "ID).\n"
            "- Thickening the root and forgetting that on a threaded well the thread limits "
            "it.\n"
            "- Confusing A with the flange or hex diameter."),
    },
    "f.B": {
        "essence": (
            "Diámetro de la punta, la parte de la vaina que está en el centro del flujo. "
            "Influye por tres caminos distintos:\n\n"
            "- Estela: f_s = N_S·V/B. Una punta más fina suelta remolinos más seguido.\n"
            "- Fuerza: la fuerza del flujo por unidad de largo es ½·ρ·V²·C·B; una punta más "
            "fina recibe menos fuerza.\n"
            "- Respuesta térmica: el calor tiene que atravesar la pared y calentar la masa de "
            "la punta; menos diámetro es menos masa y menos pared, y la medición responde "
            "antes.",
            "Tip diameter, the part of the well in the middle of the flow. It acts through "
            "three different paths:\n\n"
            "- Wake: f_s = N_S·V/B. A thinner tip sheds eddies more often.\n"
            "- Force: flow force per unit length is ½·ρ·V²·C·B; a thinner tip receives less "
            "force.\n"
            "- Thermal response: heat must cross the wall and warm the tip mass; smaller "
            "diameter means less mass and less wall, and the reading responds sooner."),
        "why": (
            "Es un compromiso entre medición y mecánica. Engrosar la punta baja la frecuencia "
            "de estela, pero aumenta la fuerza y la masa en el lugar que más baja la frecuencia "
            "natural, y vuelve lenta la medición. Por eso la norma y los diseños típicos "
            "prefieren puntas finas con raíces gruesas (perfiles cónicos o escalonados).",
            "It is a trade-off between measurement and mechanics. Thickening the tip lowers "
            "wake frequency, but increases force and mass where they lower natural frequency "
            "most, and slows the reading. That is why the standard and typical designs prefer "
            "thin tips with thick roots (tapered or stepped profiles)."),
        "worked": (
            "Gas a 20 m/s, N_S = 0,22:\n\n"
            "- B = 15,9 mm: f_s = 0,22 × 20 / 0,0159 = 277 Hz.\n"
            "- B = 19,05 mm: f_s = 231 Hz (−17 %).\n\n"
            "La fuerza sube un 20 % y la constante de tiempo, aproximadamente un 25 a 35 %.",
            "Gas at 20 m/s, N_S = 0.22:\n\n"
            "- B = 15.9 mm: f_s = 0.22 × 20 / 0.0159 = 277 Hz.\n"
            "- B = 19.05 mm: f_s = 231 Hz (−17 %).\n\n"
            "Force rises 20 % and the time constant roughly 25 to 35 %."),
        "mistakes": (
            "- Engrosar la punta como primera solución a la vibración.\n"
            "- Pedir una punta tan fina que la pared alrededor del agujero quede por debajo "
            "de unos 3 mm.\n"
            "- Olvidar sumar el sobreespesor de corrosión en la punta.",
            "- Thickening the tip as the first fix for vibration.\n"
            "- Asking for a tip so thin the wall around the bore drops below about 3 mm.\n"
            "- Forgetting to add corrosion allowance at the tip."),
    },
    "f.U": {
        "essence": (
            "Largo de inserción: desde la cara de la brida (o el plano de la rosca) hasta la "
            "punta. Es la cota con la que se compra la vaina. Se reparte en tres tramos con "
            "papeles distintos:\n\n"
            "- Dentro del montaje (Hs): sin flujo, solo agrega largo de viga.\n"
            "- Dentro de la pared: tampoco recibe flujo.\n"
            "- En el fluido (inmersión): recibe el calor y la carga.\n\n"
            "Para medir bien hace falta inmersión: la vaina conduce calor hacia la conexión "
            "y, si está poco sumergida, la punta queda a una temperatura intermedia. Para la "
            "mecánica conviene lo contrario: menos largo, más frecuencia (∝ 1/L²) y menos "
            "momento (∝ L²).",
            "Insertion length: from the flange face (or thread plane) to the tip. It is the "
            "dimension the well is bought by. It splits into three stretches with different "
            "roles:\n\n"
            "- Inside the mount (Hs): no flow, only adds beam length.\n"
            "- Inside the wall: no flow either.\n"
            "- In the fluid (immersion): receives heat and load.\n\n"
            "A good reading needs immersion: the well conducts heat towards the connection "
            "and, if barely immersed, the tip settles at an intermediate temperature. "
            "Mechanics want the opposite: less length, more frequency (∝ 1/L²) and less "
            "moment (∝ L²)."),
        "why": (
            "Es la decisión de diseño más importante: elegir U es elegir entre buena medición "
            "y margen de vibración. TS busca el largo normalizado más corto que deja la punta "
            "bien inmersa (un tercio a la mitad del diámetro interno, o 450 mm en recipientes) "
            "y, si no cumple, prueba largos más cortos.",
            "It is the most important design decision: choosing U is choosing between a good "
            "reading and vibration margin. TS looks for the shortest standard length that "
            "leaves the tip well immersed (a third to a half of the inside diameter, or 450 mm "
            "in vessels) and, if it fails, tries shorter lengths."),
        "worked": (
            "Línea 6\" Sch 40 (Di 154,1 mm, pared 7,1 mm), Hs = 150 mm.\n\n"
            "1. Inmersión objetivo ≈ 154,1/3 = 51 mm.\n"
            "2. U mínimo = 150 + 7,1 + 51 = 208 mm.\n"
            "3. Largos normalizados: 190,5 mm (7½\") se queda corto; 266,7 mm (10½\") da "
            "109,6 mm de inmersión (71 % del Di).\n"
            "4. Si 10½\" no cumple vibración, TS prueba un largo no normalizado de 210 mm.",
            "Line 6\" Sch 40 (ID 154.1 mm, wall 7.1 mm), Hs = 150 mm.\n\n"
            "1. Target immersion ≈ 154.1/3 = 51 mm.\n"
            "2. Minimum U = 150 + 7.1 + 51 = 208 mm.\n"
            "3. Standard lengths: 190.5 mm (7½\") falls short; 266.7 mm (10½\") gives "
            "109.6 mm immersion (71 % of ID).\n"
            "4. If 10½\" fails vibration, TS tries a non-standard 210 mm."),
        "mistakes": (
            "- Pedir U largo «por las dudas»: la frecuencia cae con el cuadrado.\n"
            "- Olvidar sumar Hs y la pared al pasar de inmersión a U.\n"
            "- Llevar la punta más allá del 90 % del diámetro: toca la pared en dilatación.",
            "- Ordering a long U «just in case»: frequency falls with the square.\n"
            "- Forgetting to add Hs and wall when going from immersion to U.\n"
            "- Taking the tip beyond 90 % of the diameter: it touches the wall under thermal "
            "growth."),
    },
    "f.L": {
        "essence": (
            "Largo no soportado: la parte de la vaina que vibra libremente, desde el plano "
            "donde queda empotrada (cara de la brida, asiento de la rosca o soldadura) hasta "
            "la punta. Es la «palanca» de la viga.\n\n"
            "En un voladizo, la rigidez cae con L³ (una regla el doble de larga se dobla ocho "
            "veces más con la misma fuerza en la punta) y la masa crece con L. La frecuencia "
            "natural, que es √(rigidez/masa), cae entonces con L². El momento en la raíz por "
            "una carga repartida crece con L².",
            "Unsupported length: the part of the well vibrating freely, from the plane where "
            "it is fixed (flange face, thread seat or weld) to the tip. It is the beam's "
            "«lever».\n\n"
            "In a cantilever, stiffness falls with L³ (a ruler twice as long bends eight times "
            "more under the same tip force) and mass grows with L. Natural frequency, "
            "√(stiffness/mass), therefore falls with L². Root moment from a distributed load "
            "grows with L²."),
        "why": (
            "Es la variable geométrica más influyente. Un 10 % más de largo quita un 17 % de "
            "frecuencia y agrega un 21 % de momento. Medirlo desde el plano equivocado arruina "
            "el cálculo.",
            "It is the most influential geometric variable. 10 % more length removes 17 % of "
            "frequency and adds 21 % of moment. Measuring it from the wrong plane ruins the "
            "calculation."),
        "worked": (
            "Vaina de f_n = 600 Hz con L = 200 mm:\n\n"
            "- L = 250 mm: 600 × (200/250)² = 384 Hz; momento × 1,56.\n"
            "- L = 300 mm: 267 Hz; momento × 2,25.",
            "Well with f_n = 600 Hz at L = 200 mm:\n\n"
            "- L = 250 mm: 600 × (200/250)² = 384 Hz; moment × 1.56.\n"
            "- L = 300 mm: 267 Hz; moment × 2.25."),
        "mistakes": (
            "- Medir desde la superficie de la cañería.\n"
            "- En roscadas, medir desde el extremo de la rosca y no desde el asiento.\n"
            "- Ignorar un niple largo y flexible, que corre el empotramiento hacia atrás.",
            "- Measuring from the pipe surface.\n"
            "- On threaded wells, measuring from the thread end instead of the seat.\n"
            "- Ignoring a long flexible nozzle, which moves the fixed point back."),
    },
    "f.d": {
        "essence": (
            "Agujero central donde se aloja el sensor. Se mecaniza con broca larga (perforado "
            "profundo), que es la operación más difícil y cara de la fabricación: la broca "
            "tiende a desviarse y la pared puede quedar despareja.\n\n"
            "Medidas habituales: 0,260\" (6,6 mm) para sensores de 6 mm o ¼\", y 0,385\" "
            "(9,8 mm) para 3/8\" o 8 mm. El agujero quita metal cerca del eje, donde aporta "
            "poca rigidez, pero adelgaza la pared alrededor, que es la que resiste la presión.",
            "Central bore housing the sensor. It is gun-drilled (deep drilling), the hardest "
            "and most expensive manufacturing step: the drill tends to wander and the wall may "
            "end up uneven.\n\n"
            "Usual sizes: 0.260\" (6.6 mm) for 6 mm or ¼\" sensors, and 0.385\" (9.8 mm) for "
            "3/8\" or 8 mm. The bore removes metal near the axis, where it adds little "
            "stiffness, but thins the surrounding wall, which carries pressure."),
        "why": (
            "Define qué sensores entran y cuánto metal queda. El huelgo entre sensor y agujero "
            "es aire, un aislante: cada décima de milímetro de más retrasa la medición.",
            "It defines which sensors fit and how much metal remains. The gap between sensor "
            "and bore is air, an insulator: every extra tenth of a millimetre delays the "
            "reading."),
        "worked": (
            "Sensor de 6,35 mm (¼\"):\n\n"
            "- En 6,6 mm: huelgo diametral 0,25 mm → buen contacto.\n"
            "- En 9,8 mm: huelgo 3,45 mm → la constante de tiempo puede duplicarse.\n\n"
            "Punta B = 15,9 mm con agujero 9,8 mm: pared de solo 3,05 mm.",
            "6.35 mm (¼\") sensor:\n\n"
            "- In 6.6 mm: 0.25 mm diametral gap → good contact.\n"
            "- In 9.8 mm: 3.45 mm gap → time constant may double.\n\n"
            "Tip B = 15.9 mm with 9.8 mm bore: wall of only 3.05 mm."),
        "mistakes": (
            "- Pedir agujero grande «por si cambia el sensor».\n"
            "- No verificar la pared mínima en la punta.",
            "- Ordering a large bore «in case the sensor changes».\n"
            "- Not checking minimum wall at the tip."),
    },
    "f.t": {
        "essence": (
            "Espesor del fondo cerrado de la vaina. Es una pequeña tapa que soporta la "
            "presión del proceso de frente y separa el sensor del fluido. También es la zona "
            "que más impacto recibe en flujos con partículas y donde suele empezar la "
            "erosión.\n\n"
            "Térmicamente es la primera barrera: el sensor suele apoyar su extremo sensible "
            "contra este fondo, así que un fondo grueso agrega masa y retraso.",
            "Thickness of the well's closed bottom. It is a small cap carrying process "
            "pressure head-on and separating sensor from fluid. It is also the zone taking "
            "most impact in particle-laden flows, where erosion usually starts.\n\n"
            "Thermally it is the first barrier: the sensor usually rests its sensitive end "
            "against this bottom, so a thick bottom adds mass and lag."),
        "why": (
            "Si es delgado, la presión externa puede abollarlo o, con erosión, perforarlo; si "
            "es grueso, la medición se retrasa. TS verifica la presión admisible de la punta.",
            "If thin, external pressure can dent it or, with erosion, perforate it; if thick, "
            "the reading lags. TS checks tip allowable pressure."),
        "worked": (
            "Fondo de ¼\" (6,35 mm) en 316: admite cientos de bar. Con erosión de 0,5 mm/año, "
            "en 6 años queda en 3,35 mm: hay que verificar la vaina corroída.",
            "¼\" (6.35 mm) bottom in 316: holds hundreds of bar. With 0.5 mm/year erosion, in "
            "6 years it is down to 3.35 mm: check the corroded well."),
        "mistakes": (
            "- Reducir t para ganar respuesta en un servicio erosivo.\n"
            "- Olvidar la punta en el plan de inspección.",
            "- Reducing t for response in an erosive service.\n"
            "- Leaving the tip out of the inspection plan."),
    },
    "f.b": {
        "essence": (
            "Radio de acuerdo en la raíz: la curva que une el vástago con la brida o el "
            "cuerpo. Las tensiones dentro del metal fluyen como el agua en un canal: en un "
            "cambio brusco de sección se amontonan, y en una esquina viva el esfuerzo local "
            "puede ser varias veces el nominal. Un radio amplio guía las tensiones suavemente "
            "y baja el factor K_t.",
            "Fillet radius at the root: the curve joining shank and flange or body. Stresses "
            "inside metal flow like water in a channel: at an abrupt section change they pile "
            "up, and at a sharp corner local stress can be several times nominal. A generous "
            "radius guides stresses smoothly and lowers K_t."),
        "why": (
            "La raíz es donde nacen las fisuras de fatiga. Un radio bien hecho puede ser la "
            "diferencia entre una vaina que dura décadas y una que se corta en semanas. TS usa "
            "1/8\" (3,2 mm) si no se indica otro.",
            "The root is where fatigue cracks start. A well-made radius can be the difference "
            "between a well lasting decades and one snapping in weeks. TS uses 1/8\" (3.2 mm) "
            "unless another is given."),
        "worked": (
            "Esfuerzo dinámico nominal 14 MPa:\n\n"
            "- Radio 3,2 mm, K_t ≈ 1,2: 16,8 MPa → cumple contra 21 MPa.\n"
            "- Arista viva, K_t ≈ 2: 28 MPa → no cumple.",
            "Nominal dynamic stress 14 MPa:\n\n"
            "- 3.2 mm radius, K_t ≈ 1.2: 16.8 MPa → passes against 21 MPa.\n"
            "- Sharp corner, K_t ≈ 2: 28 MPa → fails."),
        "mistakes": (
            "- No acotar el radio en el plano: el taller hace arista viva.\n"
            "- Grabar el tag o marcas de punzón cerca de la raíz (crean entallas).",
            "- Not dimensioning the radius on the drawing: the shop makes a sharp corner.\n"
            "- Engraving the tag or stamping near the root (it creates notches)."),
    },
    "f.Ls": {
        "essence": (
            "En un perfil escalonado, Ls es el largo del tramo fino de la punta, medido desde "
            "la punta hasta el escalón. El resto del vástago tiene el diámetro grueso de la "
            "raíz. La idea es tener la rigidez del tramo grueso en la zona de mayor momento y "
            "una punta fina, liviana y de respuesta rápida donde está el sensor.",
            "In a stepped profile, Ls is the length of the thin tip section, measured from "
            "the tip to the step. The rest of the shank has the thick root diameter. The idea "
            "is to have the stiffness of the thick section where moment is highest and a "
            "thin, light, fast-responding tip where the sensor is."),
        "why": (
            "Un Ls largo hace la vaina más flexible (más largo fino); uno corto la acerca a un "
            "recto grueso. Además el escalón es un segundo punto de concentración de "
            "esfuerzos que TS también verifica.",
            "A long Ls makes the well more flexible (more thin length); a short one brings it "
            "closer to a thick straight well. The step is also a second stress concentration "
            "point that TS checks."),
        "worked": (
            "U 250 mm, A 22,2, B 12,7, Ls 64 mm: el 74 % del largo tiene 22,2 mm. Con "
            "Ls 125 mm, solo el 50 %: la frecuencia baja aproximadamente un 20 %.",
            "U 250 mm, A 22.2, B 12.7, Ls 64 mm: 74 % of the length has 22.2 mm. With "
            "Ls 125 mm, only 50 %: frequency drops roughly 20 %."),
        "mistakes": (
            "- Ubicar el escalón dentro del niple, donde no aporta nada.\n"
            "- Pedir Ls mayor que el largo sensible del sensor sin necesidad.",
            "- Placing the step inside the nozzle, where it adds nothing.\n"
            "- Asking for Ls longer than the sensor's sensitive length without need."),
    },
    "f.bs": {
        "essence": (
            "Radio de acuerdo en el escalón de un perfil escalonado, donde el diámetro pasa de "
            "A a B. Cumple la misma función que el radio de raíz: suavizar el cambio de "
            "sección para que las tensiones no se concentren en una esquina.",
            "Fillet radius at the step of a stepped profile, where diameter changes from A to "
            "B. It plays the same role as the root fillet: smoothing the section change so "
            "stresses do not concentrate at a corner."),
        "why": (
            "El escalón soporta menos momento que la raíz, pero su sección es más chica, así "
            "que el esfuerzo puede ser comparable. Sin radio, el escalón puede ser el punto de "
            "falla.",
            "The step carries less moment than the root, but its section is smaller, so "
            "stress can be comparable. Without a radius the step can be the failure point."),
        "worked": (
            "A 22,2 → B 12,7 mm con bs = 3,2 mm: K_t moderado. Con bs = 0,5 mm el K_t puede "
            "duplicarse y el escalón pasa a mandar sobre la raíz.",
            "A 22.2 → B 12.7 mm with bs = 3.2 mm: moderate K_t. With bs = 0.5 mm K_t can "
            "double and the step governs over the root."),
        "mistakes": ("- No acotarlo en el plano.\n- Pulir el escalón dejando marcas "
                     "circunferenciales.",
                     "- Not dimensioning it on the drawing.\n- Polishing the step leaving "
                     "circumferential marks."),
    },
    "f.T_lag": {
        "essence": (
            "Extensión (lag) entre la conexión de proceso y el cabezal. Cumple tres funciones: "
            "aleja el cabezal y la electrónica del calor (o del frío) del proceso, deja lugar "
            "para el aislamiento térmico de la cañería y da espacio para llaves y "
            "herramientas al montar y desmontar.\n\n"
            "El lag actúa como una aleta de enfriamiento: a lo largo de ese tramo el calor se "
            "disipa al ambiente y la temperatura en el cabezal baja.",
            "Extension (lag) between the process connection and the head. It does three "
            "things: moves the head and electronics away from process heat (or cold), leaves "
            "room for pipe insulation and gives space for wrenches and tools when installing "
            "and removing.\n\n"
            "The lag acts as a cooling fin: along it heat dissipates to ambient and head "
            "temperature drops."),
        "why": (
            "No entra en la verificación de vibración del vástago, pero sí en la vida del "
            "instrumento: un transmisor montado en cabezal suele admitir 85 °C. Un lag corto "
            "en una línea a 300 °C lo daña.",
            "It does not enter the shank vibration check, but it matters for instrument life: "
            "a head-mounted transmitter usually allows 85 °C. A short lag on a 300 °C line "
            "damages it."),
        "worked": (
            "Aislamiento 75 mm → lag ≈ 75 + 25 = 100 mm, para que el cabezal quede 25 mm "
            "fuera del aislamiento. En servicio criogénico, el lag evita que el cabezal se "
            "congele.",
            "75 mm insulation → lag ≈ 75 + 25 = 100 mm, so the head sits 25 mm outside the "
            "insulation. In cryogenic service the lag keeps the head from freezing."),
        "mistakes": (
            "- Confundir lag con largo de inserción U.\n"
            "- Pedir lag cero en líneas aisladas.",
            "- Confusing lag with insertion length U.\n"
            "- Ordering zero lag on insulated lines."),
    },
    "f.L0": {
        "essence": (
            "Zona protegida: la parte del vástago que queda dentro del niple o la cupla de "
            "montaje. Ahí el fluido casi no circula (es un «bolsillo» lateral de la cañería), "
            "así que no hay arrastre ni desprendimiento de vórtices. La carga del flujo solo "
            "actúa sobre el largo expuesto, U − L0.",
            "Shielded length: the part of the shank inside the mounting nozzle or coupling. "
            "There the fluid barely moves (it is a side «pocket» of the pipe), so there is no "
            "drag or vortex shedding. Flow load only acts on the exposed length, U − L0."),
        "why": (
            "Declararla evita sobrestimar la carga. Como el momento en la raíz depende del "
            "brazo de palanca, sacar la carga del tramo cercano a la raíz baja poco el "
            "momento, pero sacar un tramo largo cambia mucho el resultado en vainas de "
            "montajes altos.",
            "Declaring it avoids overestimating load. Since root moment depends on lever arm, "
            "removing load near the root lowers moment slightly, but removing a long stretch "
            "changes results a lot for wells on tall mounts."),
        "worked": (
            "U = 300 mm, Hs = 200 mm → L0 ≈ 200 mm. Solo 100 mm reciben flujo: la fuerza total "
            "cae a un tercio y TS calcula el momento con la carga solo en ese tramo.",
            "U = 300 mm, Hs = 200 mm → L0 ≈ 200 mm. Only 100 mm receive flow: total force "
            "drops to a third and TS computes moment with load only on that stretch."),
        "mistakes": (
            "- Declarar L0 mayor que el niple real.\n"
            "- Declararla en un niple de diámetro grande donde sí entra flujo.",
            "- Declaring L0 larger than the real nozzle.\n"
            "- Declaring it in a large-bore nozzle where flow does enter."),
    },
    "f.ca": {
        "essence": (
            "Sobreespesor de corrosión: metal extra que se agrega sabiendo que se va a perder "
            "durante la vida útil por corrosión o erosión. La vaina se diseña para que, al "
            "final de esa vida, con el sobreespesor consumido, siga cumpliendo.\n\n"
            "La corrosión uniforme avanza a una velocidad más o menos constante (mm/año) que "
            "depende del par material-fluido: se estima con datos de la biblioteca, "
            "experiencia de planta o cupones de ensayo.",
            "Corrosion allowance: extra metal added knowing it will be lost over the service "
            "life to corrosion or erosion. The well is designed so that, at end of life, with "
            "the allowance consumed, it still passes.\n\n"
            "Uniform corrosion advances at a roughly constant rate (mm/year) depending on the "
            "material-fluid pair: it is estimated from library data, plant experience or test "
            "coupons."),
        "why": (
            "Una vaina corroída es más delgada: menos rígida (menos frecuencia) y más débil. "
            "TS verifica ambos estados, nueva y corroída, y manda el peor.",
            "A corroded well is thinner: less stiff (lower frequency) and weaker. TS checks "
            "both states, new and corroded, and the worse governs."),
        "worked": (
            "Velocidad 0,1 mm/año × vida 20 años = 2 mm. Una punta B = 19,05 mm queda en "
            "15,05 mm al final (2 mm por lado): f_s sube 27 % y la frecuencia natural baja.",
            "Rate 0.1 mm/year × 20-year life = 2 mm. A B = 19.05 mm tip ends at 15.05 mm "
            "(2 mm per side): f_s rises 27 % and natural frequency falls."),
        "mistakes": (
            "- Copiar el sobreespesor de la cañería sin pensar en la punta, que se erosiona "
            "más.\n"
            "- Agregar sobreespesor y no verificar la vaina corroída.",
            "- Copying the pipe allowance without thinking of the tip, which erodes more.\n"
            "- Adding allowance and not checking the corroded well."),
    },
    "f.thread": {
        "essence": (
            "Dos sistemas de rosca incompatibles:\n\n"
            "- NPT (ASME B1.20.1): cónica, con pendiente 1:16. Al apretar, los filetes macho y "
            "hembra se acuñan y sellan, ayudados por un sellador o cinta. Típica en América.\n"
            "- G o BSPP (ISO 228): cilíndrica. Los filetes no sellan; el sello lo hace una "
            "junta o arandela contra una cara de asiento. Típica en Europa.\n\n"
            "Además de no sellar, los perfiles son distintos (NPT a 60°, BSP a 55°) y el paso "
            "difiere en varios tamaños.",
            "Two incompatible thread systems:\n\n"
            "- NPT (ASME B1.20.1): tapered, 1:16 slope. When tightened male and female threads "
            "wedge and seal, helped by sealant or tape. Typical in the Americas.\n"
            "- G or BSPP (ISO 228): parallel. Threads do not seal; a gasket or washer against "
            "a seating face does. Typical in Europe.\n\n"
            "Besides not sealing, profiles differ (NPT at 60°, BSP at 55°) and pitch differs "
            "in several sizes."),
        "why": (
            "Una NPT en una cupla G entra unas vueltas y luego se traba o filtra. En una "
            "vaina, una fuga por la rosca es una fuga de proceso. TS lo informa en la hoja de "
            "datos (código R o G) y en el plano.",
            "An NPT in a G coupling enters a few turns and then binds or leaks. On a well, a "
            "thread leak is a process leak. TS reports it on the datasheet (code R or G) and "
            "the drawing."),
        "worked": (
            "1\" NPT: 11,5 hilos por pulgada, diámetro ≈ 33,4 mm. G 1: 11 hilos por pulgada, "
            "≈ 33,25 mm. Parecen iguales a simple vista y no lo son.",
            "1\" NPT: 11.5 threads per inch, diameter ≈ 33.4 mm. G 1: 11 threads per inch, "
            "≈ 33.25 mm. They look the same and are not."),
        "mistakes": (
            "- Pedir NPT para un equipo europeo con cuplas G.\n"
            "- Usar sellador en una G en lugar de junta.",
            "- Ordering NPT for European equipment with G couplings.\n"
            "- Using sealant on a G thread instead of a gasket."),
    },
    "f.sensor_type": {
        "essence": (
            "Hay dos tecnologías principales:\n\n"
            "- RTD (Pt100): la resistencia eléctrica del platino sube con la temperatura "
            "porque los átomos vibran más y dispersan a los electrones. Es precisa (décimas "
            "de grado) y estable, hasta unos 600 °C.\n"
            "- Termopar: dos metales distintos unidos generan un voltaje proporcional a la "
            "diferencia de temperatura entre la unión y los extremos (efecto Seebeck). Cubre "
            "hasta 1200 a 1700 °C, es robusto, pero menos preciso (grados).",
            "There are two main technologies:\n\n"
            "- RTD (Pt100): platinum's electrical resistance rises with temperature because "
            "atoms vibrate more and scatter electrons. It is accurate (tenths of a degree) and "
            "stable, up to about 600 °C.\n"
            "- Thermocouple: two dissimilar metals joined produce a voltage proportional to "
            "the temperature difference between junction and ends (Seebeck effect). Covers up "
            "to 1200 to 1700 °C, rugged, but less accurate (degrees)."),
        "why": (
            "Define el rango, la precisión y el diámetro de vaina del sensor, y con él el "
            "agujero de la termovaina.",
            "It defines range, accuracy and sensor sheath diameter, and with it the "
            "thermowell bore."),
        "worked": (
            "Pt100 clase A a 100 °C: ±0,35 °C. Termopar K clase 1 a 100 °C: ±1,5 °C. Para "
            "transferencia de custodia se prefiere Pt100; para un horno a 900 °C, termopar.",
            "Class A Pt100 at 100 °C: ±0.35 °C. Class 1 type K at 100 °C: ±1.5 °C. Custody "
            "transfer prefers Pt100; a 900 °C furnace, a thermocouple."),
        "mistakes": (
            "- Usar Pt100 por encima de su rango.\n"
            "- Usar termopar donde se necesita precisión fina.",
            "- Using Pt100 above its range.\n"
            "- Using a thermocouple where fine accuracy is needed."),
    },
    "f.sheath": {
        "essence": (
            "Diámetro exterior del sensor (su vaina metálica, normalmente con aislamiento "
            "mineral compactado). Debe entrar en el agujero de la termovaina con el menor "
            "huelgo posible: el aire en el huelgo conduce el calor unas 500 veces peor que el "
            "acero y es la principal causa de respuesta lenta.",
            "Outside diameter of the sensor (its metal sheath, usually with compacted mineral "
            "insulation). It must fit the thermowell bore with the smallest possible gap: air "
            "in the gap conducts heat about 500 times worse than steel and is the main cause "
            "of slow response."),
        "why": (
            "Fija el agujero de la vaina y la velocidad de respuesta. TS elige 0,260\" para "
            "vainas de hasta 6,35 mm y 0,385\" para mayores.",
            "It sets the well bore and response speed. TS picks 0.260\" for sheaths up to "
            "6.35 mm and 0.385\" for larger ones."),
        "worked": (
            "Sensor de 6 mm en agujero de 6,6 mm: huelgo 0,3 mm. El mismo en 9,8 mm: huelgo "
            "3,8 mm y una constante de tiempo que puede duplicarse.",
            "6 mm sensor in a 6.6 mm bore: 0.3 mm gap. The same in 9.8 mm: 3.8 mm gap and a "
            "time constant that can double."),
        "mistakes": (
            "- Comprar sensores de 8 mm para vainas de 0,260\".\n"
            "- No usar pasta térmica cuando el huelgo es grande.",
            "- Buying 8 mm sensors for 0.260\" wells.\n"
            "- Not using thermal paste when the gap is large."),
    },
    "f.spring": {
        "essence": (
            "Un resorte en el cabezal empuja el sensor contra el fondo de la vaina. Así el "
            "extremo sensible queda en contacto metálico con el fondo, que es la parte más "
            "cercana al fluido, en lugar de quedar flotando en aire.",
            "A spring in the head pushes the sensor against the well bottom. That way the "
            "sensitive end stays in metal contact with the bottom, the part closest to the "
            "fluid, instead of floating in air."),
        "why": (
            "Mejora la respuesta y la exactitud, y evita que el sensor vibre suelto dentro de "
            "la vaina (lo que daña el elemento de una Pt100).",
            "It improves response and accuracy, and keeps the sensor from vibrating loose in "
            "the well (which damages a Pt100 element)."),
        "worked": (
            "Mismo sensor y vaina: sin resorte τ ≈ 60 s; con resorte y contacto al fondo "
            "τ ≈ 30 s.",
            "Same sensor and well: without spring τ ≈ 60 s; with spring and bottom contact "
            "τ ≈ 30 s."),
        "mistakes": (
            "- Cortar el sensor sin dejar recorrido para el resorte.\n"
            "- Usar sensor con resorte en una vaina más larga de lo previsto.",
            "- Cutting the sensor without spring travel.\n"
            "- Using a spring-loaded sensor in a well longer than planned."),
    },
    "f.sensor_mass": {
        "essence": (
            "Masa del sensor dentro de la vaina. Si el sensor se apoya en el fondo, se mueve "
            "con la punta cuando la vaina vibra y suma inercia justo donde más influye: en un "
            "voladizo, la masa en el extremo baja la frecuencia natural mucho más que la misma "
            "masa cerca de la raíz.",
            "Mass of the sensor inside the well. If the sensor rests on the bottom it moves "
            "with the tip when the well vibrates and adds inertia exactly where it matters "
            "most: in a cantilever, mass at the end lowers natural frequency far more than the "
            "same mass near the root."),
        "why": (
            "Para sensores livianos el efecto es chico; para bulbos de termómetros o "
            "sensores múltiples puede ser de varios puntos porcentuales.",
            "For light sensors the effect is small; for thermometer bulbs or multipoint "
            "sensors it can be several percent."),
        "worked": (
            "Sensor de 6 mm × 300 mm ≈ 50 g: f_n baja 1 a 2 %. Un bimetálico de 300 g en una "
            "vaina liviana puede bajarla 5 % o más.",
            "6 mm × 300 mm sensor ≈ 50 g: f_n drops 1 to 2 %. A 300 g bimetallic in a light "
            "well can lower it 5 % or more."),
        "mistakes": ("- Ignorarla en multipuntos o bimetálicos.",
                     "- Ignoring it for multipoints or bimetallics."),
    },
    "f.E_manual": {
        "essence": (
            "El módulo de elasticidad (E) mide cuánto se estira el metal por cada unidad de "
            "esfuerzo mientras se comporta como un resorte. Viene de la rigidez de los enlaces "
            "entre átomos: casi no cambia con el tratamiento térmico o la dureza, pero sí con "
            "la familia de aleación (aceros ≈ 200 GPa, titanio ≈ 110, aluminio ≈ 70) y baja con "
            "la temperatura porque los átomos vibran más y los enlaces se aflojan.",
            "The elastic modulus (E) measures how much metal stretches per unit stress while "
            "it behaves like a spring. It comes from the stiffness of atomic bonds: it hardly "
            "changes with heat treatment or hardness, but does with alloy family (steels ≈ "
            "200 GPa, titanium ≈ 110, aluminium ≈ 70) and falls with temperature because atoms "
            "vibrate more and bonds loosen."),
        "why": (
            "La frecuencia natural es proporcional a √E. TS toma E de la biblioteca a la "
            "temperatura de operación; cargarlo a mano solo tiene sentido con un dato "
            "certificado para una aleación especial.",
            "Natural frequency is proportional to √E. TS takes E from the library at "
            "operating temperature; entering it by hand only makes sense with a certified "
            "value for a special alloy."),
        "worked": (
            "Cambiar 316 (195 GPa) por titanio grado 2 (107 GPa) con la misma geometría: f_n "
            "× √(107/195) = 0,74 → 26 % menos de frecuencia.",
            "Replacing 316 (195 GPa) with titanium grade 2 (107 GPa) at the same geometry: "
            "f_n × √(107/195) = 0.74 → 26 % less frequency."),
        "mistakes": (
            "- Cargar el valor a 20 °C para un servicio caliente.\n"
            "- Mezclar unidades (psi, ksi, MPa, GPa).",
            "- Entering the 20 °C value for a hot service.\n"
            "- Mixing units (psi, ksi, MPa, GPa)."),
    },
    "f.S_manual": {
        "essence": (
            "El esfuerzo admisible (S) es la tensión máxima que el código permite usar en el "
            "diseño. Sale de las propiedades del material divididas por factores de "
            "seguridad: por ejemplo, el menor entre la resistencia a la tracción sobre 3,5 y "
            "la fluencia sobre 1,5, evaluadas a la temperatura de servicio. A alta "
            "temperatura también se considera la fluencia lenta (creep).",
            "Allowable stress (S) is the maximum stress the code allows in design. It comes "
            "from material properties divided by safety factors: for example the lower of "
            "tensile strength over 3.5 and yield over 1.5, evaluated at service temperature. "
            "At high temperature creep is also considered."),
        "why": (
            "Fija la presión admisible del vástago y la punta, y el límite del esfuerzo "
            "estacionario (1,5·S). Un valor demasiado alto aprueba una vaina que puede "
            "deformarse.",
            "It sets shank and tip allowable pressure and the steady-stress limit (1.5·S). A "
            "value too high passes a well that may deform."),
        "worked": (
            "316 a 38 °C: S ≈ 138 MPa; a 400 °C: ≈ 103 MPa. A 400 °C la presión admisible "
            "cae un 25 %.",
            "316 at 38 °C: S ≈ 138 MPa; at 400 °C: ≈ 103 MPa. At 400 °C allowable pressure "
            "drops 25 %."),
        "mistakes": (
            "- Usar la fluencia directamente como admisible.\n"
            "- Usar el valor de otro código sin revisar su base.",
            "- Using yield directly as allowable.\n"
            "- Using another code's value without checking its basis."),
    },
    "f.conn_size": {
        "essence": (
            "Tamaño nominal de la rosca o la brida de la termovaina (1\" NPT, brida 1½\", 2\"). "
            "Es independiente del tamaño de la línea: una cañería de 12\" puede llevar una "
            "vaina con brida de 1½\".\n\n"
            "El tamaño de conexión limita el diámetro de raíz A: la raíz tiene que caber en la "
            "brida o en la rosca. Por eso subir un tamaño de conexión es a menudo la forma más "
            "barata de engrosar la raíz y rigidizar la vaina.",
            "Nominal size of the thermowell thread or flange (1\" NPT, 1½\" flange, 2\"). It is "
            "independent of line size: a 12\" pipe may take a well with a 1½\" flange.\n\n"
            "Connection size limits root diameter A: the root must fit the flange or thread. "
            "That is why going up one connection size is often the cheapest way to thicken "
            "the root and stiffen the well."),
        "why": (
            "También define el niple o la cupla en la cañería, que hay que prever en el "
            "diseño de la línea. Cambiarlo después implica modificar la cañería.",
            "It also defines the nozzle or coupling on the pipe, which must be provided in the "
            "line design. Changing it later means modifying the piping."),
        "worked": (
            "Brida 1\": A máx ≈ 25 mm. Brida 1½\": A hasta ≈ 35 mm. De A = 25 a 32 mm, la "
            "rigidez a flexión (∝ A⁴) crece 2,7 veces.",
            "1\" flange: max A ≈ 25 mm. 1½\" flange: A up to ≈ 35 mm. From A = 25 to 32 mm, "
            "bending stiffness (∝ A⁴) grows 2.7 times."),
        "mistakes": (
            "- Confundir el tamaño de la conexión con el de la línea.\n"
            "- Definir la cupla de la cañería sin consultar instrumentos.",
            "- Confusing connection size with line size.\n"
            "- Defining the pipe coupling without consulting instrumentation."),
    },
    "f.face": {
        "essence": (
            "La cara de la brida es la superficie donde se asienta la junta:\n\n"
            "- RF (raised face): un resalto anular concentra la carga de los bulones sobre la "
            "junta (espirometálica o plana). La más común hasta clase 600.\n"
            "- RTJ (ring type joint): un anillo metálico se aloja en una ranura de ambas "
            "bridas y sella por deformación plástica del metal. Para alta presión y "
            "temperatura.\n"
            "- FF (flat face): cara plana completa, para bridas frágiles (fundición) donde un "
            "resalto podría romperlas al apretar.",
            "The flange face is the surface where the gasket seats:\n\n"
            "- RF (raised face): an annular step concentrates bolt load on the gasket "
            "(spiral-wound or flat). The most common up to class 600.\n"
            "- RTJ (ring type joint): a metal ring sits in a groove in both flanges and seals "
            "by plastic deformation of the metal. For high pressure and temperature.\n"
            "- FF (flat face): full flat face, for brittle flanges (cast iron) where a raised "
            "face could break them when tightened."),
        "why": ("Debe coincidir con la brida de la línea: una RF contra una RTJ no sella.",
                "It must match the line flange: RF against RTJ does not seal."),
        "worked": (
            "Clase 300 típica: RF con junta espirometálica. Clase 1500: RTJ con anillo R-24 "
            "(según tamaño).",
            "Typical class 300: RF with spiral-wound gasket. Class 1500: RTJ with an R-24 "
            "ring (depending on size)."),
        "mistakes": ("- Pedir RF para una línea RTJ.\n- Usar FF contra RF.",
                     "- Ordering RF for an RTJ line.\n- Using FF against RF."),
    },
    "f.coating": {
        "essence": (
            "Un recubrimiento cambia la superficie sin cambiar el material base:\n\n"
            "- Stellite (cobalto-cromo-tungsteno, soldado en la punta): muy duro, resiste "
            "erosión y desgaste a alta temperatura.\n"
            "- Carburo de tungsteno (proyección térmica): resistencia extrema a la abrasión.\n"
            "- PTFE o PFA (fluoropolímeros): inertes frente a casi todos los ácidos, pero "
            "blandos y limitados a unos 200 a 260 °C.\n\n"
            "Cada uno resuelve un problema distinto y agrega una limitación.",
            "A coating changes the surface without changing the base material:\n\n"
            "- Stellite (cobalt-chromium-tungsten, welded on the tip): very hard, resists "
            "erosion and wear at high temperature.\n"
            "- Tungsten carbide (thermal spray): extreme abrasion resistance.\n"
            "- PTFE or PFA (fluoropolymers): inert to almost all acids, but soft and limited "
            "to about 200 to 260 °C.\n\n"
            "Each solves a different problem and adds a limitation."),
        "why": (
            "Puede llevar la vida de una vaina erosionada de meses a años, o permitir un "
            "material base común en un ácido. TS avisa si la temperatura supera el límite del "
            "recubrimiento.",
            "It can take an eroded well's life from months to years, or allow a common base "
            "material in an acid. TS warns if temperature exceeds the coating limit."),
        "worked": (
            "Gas con arena, V/V_e = 0,9: Stellite 6 en la punta. Ácido clorhídrico a 60 °C: "
            "acero al carbono con PFA, más barato que una vaina maciza de Hastelloy.",
            "Gas with sand, V/V_e = 0.9: Stellite 6 on the tip. Hydrochloric acid at 60 °C: "
            "carbon steel with PFA, cheaper than a solid Hastelloy well."),
        "mistakes": (
            "- Usar PTFE por encima de su temperatura.\n"
            "- Esperar respuesta rápida con un recubrimiento plástico grueso (aísla).",
            "- Using PTFE above its temperature.\n"
            "- Expecting fast response with a thick plastic coating (it insulates)."),
    },
    "f.rating": {
        "essence": (
            "La clase de presión ASME B16.5 (150, 300, 600, 900, 1500, 2500) es un nombre, no "
            "una presión. Para cada clase, la norma tabula cuánta presión soporta la brida a "
            "cada temperatura según el grupo de material (por ejemplo 1.1 acero al carbono, "
            "2.2 inoxidable 316). Al subir la temperatura el metal pierde resistencia y la "
            "presión admisible baja.",
            "ASME B16.5 pressure class (150, 300, 600, 900, 1500, 2500) is a name, not a "
            "pressure. For each class the standard tabulates how much pressure the flange "
            "holds at each temperature by material group (for example 1.1 carbon steel, 2.2 "
            "stainless 316). As temperature rises the metal weakens and allowable pressure "
            "falls."),
        "why": (
            "La brida de la vaina es parte de la frontera de presión: debe tener al menos la "
            "clase de la línea y admitir la presión de diseño a la temperatura de diseño.",
            "The well flange is part of the pressure boundary: it must have at least the line "
            "class and hold design pressure at design temperature."),
        "worked": (
            "316 (grupo 2.2) clase 300: ≈ 49,6 bar a 38 °C, ≈ 37 bar a 300 °C. Con 45 bar de "
            "diseño a 300 °C no alcanza: hace falta clase 600 (≈ 74 bar a 300 °C).",
            "316 (group 2.2) class 300: ≈ 49.6 bar at 38 °C, ≈ 37 bar at 300 °C. With 45 bar "
            "design at 300 °C it falls short: class 600 is needed (≈ 74 bar at 300 °C)."),
        "mistakes": (
            "- Leer «clase 300» como 300 psi.\n"
            "- Usar la tabla de otro grupo de material.",
            "- Reading «class 300» as 300 psi.\n"
            "- Using another material group's table."),
    },
    "f.pipe_od": {
        "essence": (
            "Diámetro exterior real de la cañería. En tamaños normalizados es fijo para cada "
            "NPS (por eso los accesorios encajan aunque cambie el espesor). Con «Otro» se "
            "carga a mano: tubos de instrumentación, ductos, cañerías de normas no ASME.",
            "Actual outside diameter of the pipe. For standard sizes it is fixed per NPS "
            "(which is why fittings fit even when thickness changes). With «Other» it is "
            "entered by hand: instrument tubing, ducts, non-ASME piping."),
        "why": (
            "Con el espesor da el diámetro interno: Di = OD − 2 × pared, que fija la velocidad.",
            "With wall thickness it gives inside diameter: ID = OD − 2 × wall, which sets "
            "velocity."),
        "worked": (
            "Tubo de 219,1 mm × 8,18 mm → Di = 202,7 mm (igual a NPS 8 Sch 40). Si por error "
            "se carga 200 mm como OD, el Di sale 183,6 mm y la velocidad 22 % mayor.",
            "Tube 219.1 mm × 8.18 mm → ID = 202.7 mm (same as NPS 8 Sch 40). If 200 mm is "
            "entered as OD by mistake, ID comes out 183.6 mm and velocity 22 % higher."),
        "mistakes": ("- Cargar el diámetro interno en el campo de OD.",
                     "- Entering inside diameter in the OD field."),
    },
}
