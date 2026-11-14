"""Profundidad de las fichas del termopozo: geometría, material, conexión y sensor."""

from __future__ import annotations

from typing import Any

DEEP: dict[str, dict[str, Any]] = {
    "f.profile": {
        "essence": (
            "La vaina es una viga en voladizo: empotrada en la conexión y libre en la punta. "
            "En una viga así el momento flector es máximo en la raíz y cero en la punta, y la "
            "masa que más «pesa» para la vibración es la de la punta, que es la que más se "
            "mueve. El perfil ideal pone metal donde hace falta resistencia (raíz) y lo saca de "
            "donde solo agrega masa (punta). Eso hace el cónico; el escalonado lo aproxima con "
            "dos diámetros; el recto es el más simple pero desaprovecha material.",
            "A thermowell is a cantilever beam: fixed at the connection and free at the tip. "
            "In such a beam bending moment is maximum at the root and zero at the tip, and the "
            "mass that «weighs» most for vibration is at the tip, which moves the most. The "
            "ideal profile puts metal where strength is needed (root) and removes it where it "
            "only adds mass (tip). The tapered profile does that; the stepped one approximates "
            "it with two diameters; the straight one is simplest but wastes material."),
        "why": (
            "Con la misma punta y el mismo largo, un cónico puede tener 30 a 50 % más "
            "frecuencia natural que un recto, y menor esfuerzo en la raíz. Es la diferencia "
            "entre cumplir y no cumplir en servicios de gas.",
            "With the same tip and length, a tapered well can have 30 to 50 % higher natural "
            "frequency than a straight one, and lower root stress. It is the difference "
            "between passing and failing in gas services."),
        "worked": (
            "U = 250 mm, punta 19 mm, agujero 6,6 mm: recto (A = B = 19 mm) f_n ≈ 330 Hz; "
            "cónico (A = 26,7 mm) f_n ≈ 460 Hz. Con f_s = 170 Hz, el recto da r = 0,52 y el "
            "cónico r = 0,37.",
            "U = 250 mm, tip 19 mm, bore 6.6 mm: straight (A = B = 19 mm) f_n ≈ 330 Hz; "
            "tapered (A = 26.7 mm) f_n ≈ 460 Hz. With f_s = 170 Hz, straight gives r = 0.52 "
            "and tapered r = 0.37."),
        "mistakes": (
            "- Elegir recto por costo en un servicio de gas rápido.\n"
            "- Usar un escalonado fuera del rango B/A de la norma.",
            "- Choosing straight for cost in a fast gas service.\n"
            "- Using a stepped well outside the standard's B/A range."),
    },
    "f.connection": {
        "essence": (
            "La conexión es el apoyo de la viga y la frontera de presión. Su rigidez define "
            "cuánto «empotrada» está la vaina (más rígida, más frecuencia) y su forma define "
            "cuánto se concentra el esfuerzo en la transición (una rosca tiene filetes que "
            "actúan como entallas y multiplican el esfuerzo local).",
            "The connection is the beam's support and the pressure boundary. Its stiffness "
            "sets how «fixed» the well is (stiffer, higher frequency) and its shape sets how "
            "much stress concentrates at the transition (a thread has roots acting as notches "
            "that multiply local stress)."),
        "why": (
            "Afecta la frecuencia instalada (H_c), el esfuerzo dinámico (K_t), la presión "
            "admisible (rating de brida) y el mantenimiento (si se puede retirar).",
            "It affects installed frequency (H_c), dynamic stress (K_t), allowable pressure "
            "(flange rating) and maintenance (whether it can be removed)."),
        "worked": (
            "Misma vaina, misma condición: bridada S_o = 14 MPa; roscada S_o ≈ 20 MPa por K_t "
            "mayor, frente a un límite de fatiga de unos 21 MPa: la roscada queda al límite.",
            "Same well, same condition: flanged S_o = 14 MPa; threaded S_o ≈ 20 MPa due to "
            "higher K_t, against a fatigue limit of about 21 MPa: the threaded one is at the "
            "limit."),
        "mistakes": (
            "- Elegir roscada en servicios peligrosos o con vibración.\n"
            "- Soldar una vaina que habrá que inspeccionar.",
            "- Choosing threaded in hazardous or vibrating services.\n"
            "- Welding a well that will need inspection."),
    },
    "f.conn_size": {
        "essence": (
            "Es el tamaño nominal de la rosca o la brida del termopozo (por ejemplo 1\" NPT o "
            "brida 1½\"). Limita el diámetro de raíz A: una brida más grande permite una raíz "
            "más gruesa y por lo tanto una vaina más rígida.",
            "It is the nominal size of the well's thread or flange (for example 1\" NPT or 1½\" "
            "flange). It limits root diameter A: a larger flange allows a thicker root and "
            "therefore a stiffer well."),
        "why": (
            "Si la vaina no cumple, subir un tamaño de conexión suele ser la forma más barata "
            "de engrosar la raíz.",
            "If the well fails, going up one connection size is often the cheapest way to "
            "thicken the root."),
        "worked": (
            "Brida 1\": A máx ≈ 25 mm. Brida 1½\": A hasta ≈ 35 mm. Con A de 25 a 32 mm, la "
            "rigidez a flexión (∝ A⁴) crece 2,7 veces.",
            "1\" flange: max A ≈ 25 mm. 1½\" flange: A up to ≈ 35 mm. With A from 25 to 32 mm, "
            "bending stiffness (∝ A⁴) grows 2.7 times."),
        "mistakes": ("- Confundir el tamaño de la conexión con el de la línea.",
                     "- Confusing connection size with line size."),
    },
    "f.rating": {
        "essence": (
            "La clase ASME B16.5 (150, 300, 600, 900, 1500, 2500) define la presión que una "
            "brida soporta a cada temperatura, para cada grupo de materiales. No es una "
            "presión en psi: una brida clase 300 de acero al carbono admite unos 51 bar a 38 °C "
            "y bastante menos en caliente, porque el metal pierde resistencia.",
            "ASME B16.5 class (150, 300, 600, 900, 1500, 2500) defines the pressure a flange "
            "holds at each temperature, for each material group. It is not a pressure in psi: "
            "a carbon steel class 300 flange allows about 51 bar at 38 °C and quite a bit less "
            "when hot, because the metal loses strength."),
        "why": (
            "La brida de la vaina debe tener al menos la clase de la brida de la línea y "
            "admitir la presión de diseño a la temperatura de diseño.",
            "The well flange must have at least the line flange class and hold design pressure "
            "at design temperature."),
        "worked": (
            "316 (grupo 2.2) clase 300: ≈ 49,6 bar a 38 °C; ≈ 37 bar a 300 °C. Con 45 bar de "
            "diseño a 300 °C hace falta clase 600.",
            "316 (group 2.2) class 300: ≈ 49.6 bar at 38 °C; ≈ 37 bar at 300 °C. With 45 bar "
            "design at 300 °C class 600 is needed."),
        "mistakes": (
            "- Leer la clase como presión.\n"
            "- Usar la tabla de otro grupo de material.",
            "- Reading the class as a pressure.\n"
            "- Using another material group's table."),
    },
    "f.face": {
        "essence": (
            "La cara de la brida es la superficie donde apoya la junta. RF (raised face, cara "
            "levantada) concentra la presión de apriete en un anillo y sella con juntas "
            "espirometálicas o planas; RTJ (ring type joint) usa un anillo metálico en una "
            "ranura y sella por deformación del metal, para alta presión; FF (cara plana) se "
            "usa con bridas de fundición frágil.",
            "The flange face is where the gasket seats. RF (raised face) concentrates bolt load "
            "on a ring and seals with spiral-wound or flat gaskets; RTJ (ring type joint) uses "
            "a metal ring in a groove and seals by metal deformation, for high pressure; FF "
            "(flat face) is used with brittle cast-iron flanges."),
        "why": ("Debe coincidir con la brida de la línea: RF con RTJ no sella.",
                "It must match the line flange: RF against RTJ does not seal."),
        "worked": ("Clase 300 típica: RF. Clase 900 en adelante: suele ser RTJ.",
                   "Typical class 300: RF. Class 900 and above: usually RTJ."),
        "mistakes": ("- Pedir RF para una línea RTJ.", "- Ordering RF for an RTJ line."),
    },
    "f.material": {
        "essence": (
            "El material define tres propiedades que el cálculo usa: el módulo elástico E "
            "(rigidez, fija la frecuencia natural), el esfuerzo admisible S (resistencia "
            "estática) y el límite de fatiga (resistencia a millones de ciclos). Además debe "
            "resistir química y térmicamente el fluido.\n\n"
            "Los inoxidables austeníticos (304, 316) deben su resistencia a la corrosión al "
            "cromo, que forma una capa de óxido de pocos nanómetros que se regenera sola; el "
            "molibdeno del 316 la refuerza frente a cloruros. Las aleaciones de níquel "
            "resisten mejor ácidos y altas temperaturas; los dúplex combinan resistencia "
            "mecánica y a cloruros.",
            "Material defines three properties the calculation uses: elastic modulus E "
            "(stiffness, sets natural frequency), allowable stress S (static strength) and "
            "fatigue limit (strength over millions of cycles). It must also resist the fluid "
            "chemically and thermally.\n\n"
            "Austenitic stainless steels (304, 316) owe their corrosion resistance to "
            "chromium, which forms a self-healing oxide film a few nanometres thick; "
            "molybdenum in 316 strengthens it against chlorides. Nickel alloys resist acids and "
            "high temperatures better; duplex grades combine mechanical and chloride "
            "resistance."),
        "why": (
            "Un material incompatible falla por corrosión aunque el cálculo mecánico sea "
            "perfecto. Un material más rígido o resistente puede hacer cumplir una vaina "
            "larga.",
            "An incompatible material fails by corrosion even if the mechanical calculation is "
            "perfect. A stiffer or stronger material can make a long well pass."),
        "worked": (
            "316 a 200 °C: S ≈ 115 MPa. Inconel 625: S ≈ 240 MPa. Dúplex 2205: S ≈ 200 MPa. "
            "Con el mismo diseño, el dúplex admite casi el doble de presión.",
            "316 at 200 °C: S ≈ 115 MPa. Inconel 625: S ≈ 240 MPa. Duplex 2205: S ≈ 200 MPa. "
            "With the same design, duplex allows almost twice the pressure."),
        "mistakes": (
            "- Elegir un material distinto del de la cañería sin evaluar par galvánico.\n"
            "- Suponer que «inoxidable» resiste cualquier cosa.",
            "- Choosing a material different from the pipe without assessing galvanic "
            "coupling.\n"
            "- Assuming «stainless» resists anything."),
    },
    "f.coating": {
        "essence": (
            "Un recubrimiento protege la superficie sin cambiar el material base: Stellite "
            "(aleación de cobalto-cromo soldada en la punta) da dureza contra erosión; PTFE o "
            "PFA dan inercia química contra ácidos; carburo de tungsteno resiste abrasión "
            "severa.",
            "A coating protects the surface without changing base material: Stellite "
            "(cobalt-chromium alloy welded on the tip) gives hardness against erosion; PTFE or "
            "PFA give chemical inertness against acids; tungsten carbide resists severe "
            "abrasion."),
        "why": (
            "Puede extender la vida de una vaina erosionada de meses a años, pero cada "
            "recubrimiento tiene un límite de temperatura y algunos cambian la respuesta "
            "térmica.",
            "It can extend an eroded well's life from months to years, but each coating has a "
            "temperature limit and some change thermal response."),
        "worked": (
            "PTFE: hasta unos 260 °C. Stellite 6: hasta unos 800 °C. Una vaina con PTFE en una "
            "línea a 300 °C pierde el recubrimiento.",
            "PTFE: up to about 260 °C. Stellite 6: up to about 800 °C. A PTFE-lined well in a "
            "300 °C line loses its coating."),
        "mistakes": ("- Recubrir con PTFE y esperar respuesta térmica rápida.",
                     "- Coating with PTFE and expecting fast thermal response."),
    },
    "f.E_manual": {
        "essence": (
            "El módulo de elasticidad mide cuánto se estira el metal por unidad de esfuerzo "
            "en la zona elástica. Viene de la rigidez de los enlaces entre átomos: casi no "
            "depende del tratamiento térmico, pero sí del tipo de aleación y de la temperatura.",
            "The elastic modulus measures how much metal stretches per unit stress in the "
            "elastic range. It comes from the stiffness of atomic bonds: it barely depends on "
            "heat treatment, but it does depend on alloy type and temperature."),
        "why": (
            "La frecuencia natural es proporcional a √E. Cargarlo a mano solo tiene sentido "
            "con un dato certificado distinto del de la biblioteca.",
            "Natural frequency is proportional to √E. Entering it by hand only makes sense "
            "with a certified value different from the library's."),
        "worked": ("Acero al carbono 203 GPa; 316 195 GPa; titanio grado 2 107 GPa (f_n −27 %).",
                   "Carbon steel 203 GPa; 316 195 GPa; titanium grade 2 107 GPa (f_n −27 %)."),
        "mistakes": ("- Cargar en psi o ksi sin convertir.",
                     "- Entering psi or ksi without converting."),
    },
    "f.S_manual": {
        "essence": (
            "El esfuerzo admisible es la tensión máxima que el código permite usar en diseño. "
            "Se obtiene de la resistencia del material dividida por factores de seguridad: "
            "por ejemplo el menor entre la tracción última sobre 3,5 y la fluencia sobre 1,5, "
            "evaluados a la temperatura de servicio.",
            "Allowable stress is the maximum stress the code allows in design. It comes from "
            "material strength divided by safety factors: for example the lower of ultimate "
            "tensile over 3.5 and yield over 1.5, evaluated at service temperature."),
        "why": (
            "Fija la presión admisible y el límite del esfuerzo estacionario. Cargarlo mal "
            "puede aprobar una vaina que se deforma.",
            "It sets allowable pressure and the steady-stress limit. Entering it wrongly can "
            "pass a well that deforms."),
        "worked": ("316 a 38 °C: 138 MPa; a 400 °C: ≈ 103 MPa.",
                   "316 at 38 °C: 138 MPa; at 400 °C: ≈ 103 MPa."),
        "mistakes": ("- Usar la fluencia como admisible.",
                     "- Using yield as allowable."),
    },
    "f.L": {
        "essence": (
            "Es el largo que vibra libremente: desde el punto de apoyo (cara de la brida, "
            "fondo de la rosca o soldadura) hasta la punta. Es la «palanca» de la viga.",
            "It is the length that vibrates freely: from the support point (flange face, "
            "thread bottom or weld) to the tip. It is the beam's «lever»."),
        "why": (
            "La frecuencia natural cae con 1/L² y el momento en la raíz crece con L². Es la "
            "variable geométrica más influyente.",
            "Natural frequency falls with 1/L² and root moment grows with L². It is the most "
            "influential geometric variable."),
        "worked": (
            "L de 300 a 250 mm: frecuencia × 1,44; momento estático × 0,69.",
            "L from 300 to 250 mm: frequency × 1.44; static moment × 0.69."),
        "mistakes": ("- Medir desde la cara de la brida de la línea en lugar del apoyo real.",
                     "- Measuring from the line flange face instead of the real support."),
    },
    "f.U": {
        "essence": (
            "Largo de inserción: desde la cara de la brida (o la rosca) hasta la punta. Es la "
            "cota de compra. Se reparte en tres tramos: dentro del montaje (Hs), dentro de la "
            "pared y en el fluido (inmersión).",
            "Insertion length: from flange face (or thread) to tip. It is the purchase "
            "dimension. It splits into three stretches: inside the mount (Hs), inside the wall "
            "and in the fluid (immersion)."),
        "why": (
            "Debe ser suficiente para medir bien (la punta lejos de la pared y de la conexión, "
            "que conducen calor) y lo más corto posible para la mecánica.",
            "It must be enough for a good reading (tip away from the wall and connection, "
            "which conduct heat) and as short as possible for the mechanics."),
        "worked": (
            "Hs 150 + pared 7 + inmersión 1/3 de 154 mm (51 mm) = 208 mm → se redondea al "
            "normalizado de 7½\" (190,5 mm) o 10½\" (266,7 mm) según el criterio.",
            "Hs 150 + wall 7 + immersion 1/3 of 154 mm (51 mm) = 208 mm → rounded to the "
            "standard 7½\" (190.5 mm) or 10½\" (266.7 mm) depending on the criterion."),
        "mistakes": (
            "- Pedir U largo «por las dudas».\n"
            "- Olvidar sumar Hs y la pared.",
            "- Ordering a long U «just in case».\n"
            "- Forgetting to add Hs and wall."),
    },
    "f.A": {
        "essence": (
            "Diámetro de la raíz, donde el momento flector es máximo. La rigidez a flexión de "
            "un tubo crece con la cuarta potencia del diámetro (momento de inercia ∝ A⁴ − d⁴) "
            "y la resistencia con el cubo.",
            "Root diameter, where bending moment is maximum. A tube's bending stiffness grows "
            "with the fourth power of diameter (moment of inertia ∝ A⁴ − d⁴) and its strength "
            "with the cube."),
        "why": (
            "Engrosar la raíz es una de las formas más eficaces de subir la frecuencia y bajar "
            "el esfuerzo, sin tocar la punta (que manda en la respuesta térmica).",
            "Thickening the root is one of the most effective ways to raise frequency and "
            "lower stress, without touching the tip (which governs thermal response)."),
        "worked": ("A de 22 a 26,7 mm (+21 %): módulo resistente × 1,8 aprox.",
                   "A from 22 to 26.7 mm (+21 %): section modulus × 1.8 approx."),
        "mistakes": ("- Pedir una A que no entra en el niple o la brida.",
                     "- Asking for an A that does not fit the nozzle or flange."),
    },
    "f.B": {
        "essence": (
            "Diámetro de la punta. Manda en la frecuencia de estela (f_s ∝ 1/B), en la fuerza "
            "del flujo (∝ B) y en la respuesta térmica: una punta fina tiene menos masa que "
            "calentar y responde más rápido.",
            "Tip diameter. It governs wake frequency (f_s ∝ 1/B), flow force (∝ B) and thermal "
            "response: a thin tip has less mass to heat and responds faster."),
        "why": (
            "Es un compromiso: más fina mide mejor pero vibra a más frecuencia; más gruesa "
            "baja f_s pero tarda más en medir.",
            "It is a trade-off: thinner reads better but vibrates at higher frequency; "
            "thicker lowers f_s but is slower to read."),
        "worked": ("B de 15,9 a 19,05 mm: f_s −17 %; constante de tiempo +30 % aprox.",
                   "B from 15.9 to 19.05 mm: f_s −17 %; time constant +30 % approx."),
        "mistakes": ("- Engrosar la punta como primera solución a la vibración.",
                     "- Thickening the tip as the first fix for vibration."),
    },
    "f.d": {
        "essence": (
            "Agujero donde va el sensor. Se elige según la vaina del sensor (0,260\" para "
            "sensores de 6 mm o ¼\", 0,385\" para 3/8\"). Quita metal de la sección, sobre todo "
            "cerca del eje, donde aporta poca rigidez.",
            "Bore where the sensor goes. It is chosen for the sensor sheath (0.260\" for 6 mm "
            "or ¼\" sensors, 0.385\" for 3/8\"). It removes metal from the section, mostly near "
            "the axis, where it adds little stiffness."),
        "why": (
            "Un agujero muy justo dificulta insertar el sensor; muy holgado deja aire que aísla "
            "y hace la medición lenta.",
            "A very tight bore makes the sensor hard to insert; a loose one leaves air that "
            "insulates and slows the reading."),
        "worked": ("Agujero 6,6 mm con sensor de 6,35 mm: huelgo 0,25 mm, adecuado.",
                   "Bore 6.6 mm with a 6.35 mm sensor: 0.25 mm clearance, adequate."),
        "mistakes": ("- Pedir agujero de 0,385\" para un sensor de 6 mm.",
                     "- Ordering a 0.385\" bore for a 6 mm sensor."),
    },
    "f.t": {
        "essence": (
            "Espesor del fondo de la punta. Es la pared que separa el sensor del fluido en el "
            "extremo, y la que soporta la presión de frente.",
            "Thickness of the tip bottom. It is the wall separating the sensor from the fluid "
            "at the end, and the one carrying pressure head-on."),
        "why": ("Si es delgada, la presión externa puede abollarla; si es gruesa, retrasa la "
                "medición.",
                "If thin, external pressure can dent it; if thick, it delays the reading."),
        "worked": ("Típico ¼\" (6,35 mm). Con 3 mm de sobreespesor, hay que sumarlos.",
                   "Typical ¼\" (6.35 mm). With 3 mm allowance, add it."),
        "mistakes": ("- Olvidar la erosión de la punta al fijar t.",
                     "- Forgetting tip erosion when setting t."),
    },
    "f.b": {
        "essence": (
            "Radio de acuerdo en la raíz, donde el vástago se une a la brida o al cuerpo. Una "
            "arista viva concentra el esfuerzo como una grieta incipiente; un radio suaviza el "
            "flujo de tensiones.",
            "Fillet radius at the root, where the shank meets the flange or body. A sharp "
            "corner concentrates stress like an incipient crack; a radius smooths the stress "
            "flow."),
        "why": ("Baja K_t y aumenta la vida a fatiga.", "It lowers K_t and increases fatigue "
                                                         "life."),
        "worked": ("TS usa 1/8\" (3,2 mm) por defecto. Con b = 0 el K_t de la raíz sube.",
                   "TS uses 1/8\" (3.2 mm) by default. With b = 0 root K_t rises."),
        "mistakes": ("- No indicar el radio en el plano: el taller hace arista viva.",
                     "- Not showing the radius on the drawing: the shop makes a sharp "
                     "corner."),
    },
    "f.Ls": {
        "essence": ("Largo del tramo de punta fina en un escalonado.",
                    "Length of the thin tip section in a stepped well."),
        "why": (
            "Define dónde está el escalón y cuánto de la viga es fina: más largo, más flexible.",
            "It defines where the step is and how much of the beam is thin: longer, more "
            "flexible."),
        "worked": ("U 250 mm con Ls 64 mm: el 74 % del largo tiene la raíz gruesa.",
                   "U 250 mm with Ls 64 mm: 74 % of the length has the thick root."),
        "mistakes": ("- Escalón dentro de la zona de flujo máxima sin verificarlo.",
                     "- Step inside the peak flow zone without checking it."),
    },
    "f.bs": {
        "essence": ("Radio del escalón: la misma idea que b pero en el cambio de diámetro.",
                    "Step fillet: the same idea as b but at the diameter change."),
        "why": ("El escalón es un segundo punto de concentración de esfuerzos.",
                "The step is a second stress concentration point."),
        "worked": ("1/8\" por defecto.", "1/8\" by default."),
        "mistakes": ("- Escalón sin radio.", "- Step without radius."),
    },
    "f.T_lag": {
        "essence": (
            "Extensión entre la conexión y el cabezal. Aleja el cabezal y la electrónica del "
            "calor del proceso y deja espacio para el aislamiento y las herramientas.",
            "Extension between connection and head. It moves the head and electronics away "
            "from process heat and leaves room for insulation and tools."),
        "why": ("No entra en el cálculo de vibración, pero sí en la integridad del "
                "instrumento.",
                "It does not enter the vibration calculation, but it matters for instrument "
                "integrity."),
        "worked": ("Aislamiento 50 mm → lag 75 mm.", "Insulation 50 mm → lag 75 mm."),
        "mistakes": ("- Confundir lag con largo de inserción.",
                     "- Confusing lag with insertion length."),
    },
    "f.L0": {
        "essence": (
            "Parte del vástago que queda dentro del niple o la cupla, protegida del flujo. "
            "Ahí el fluido está casi quieto y no genera arrastre ni vórtices.",
            "Part of the shank inside the nozzle or coupling, shielded from flow. There the "
            "fluid is almost still and creates no drag or vortices."),
        "why": (
            "Declararla evita sobrestimar la carga: la fuerza solo actúa sobre el largo "
            "expuesto, y el momento en la raíz se reduce.",
            "Declaring it avoids overestimating load: force only acts on the exposed length, "
            "and root moment drops."),
        "worked": ("U = 250, L0 = 150: solo 100 mm reciben flujo; el momento cae fuerte.",
                   "U = 250, L0 = 150: only 100 mm receive flow; moment drops sharply."),
        "mistakes": ("- Declarar L0 mayor que el niple real.",
                     "- Declaring L0 larger than the real nozzle."),
    },
    "f.ca": {
        "essence": (
            "Espesor extra que se agrega previendo pérdida por corrosión o erosión durante la "
            "vida útil. Al final de la vida, la vaina debe seguir cumpliendo con ese espesor "
            "consumido.",
            "Extra thickness added for expected corrosion or erosion loss over the service "
            "life. At end of life the well must still pass with that thickness consumed."),
        "why": (
            "TS verifica la vaina nueva y la corroída: una vaina más delgada es menos rígida y "
            "más débil.",
            "TS checks the new and the corroded well: a thinner well is less stiff and "
            "weaker."),
        "worked": ("Corrosión 0,1 mm/año × 20 años = 2 mm de sobreespesor.",
                   "Corrosion 0.1 mm/year × 20 years = 2 mm allowance."),
        "mistakes": ("- Copiar el sobreespesor de la cañería sin evaluar la punta.",
                     "- Copying the pipe allowance without assessing the tip."),
    },
    "f.sensor_type": {
        "essence": (
            "RTD (Pt100): resistencia de platino que aumenta con la temperatura, muy precisa "
            "y estable hasta unos 600 °C. Termopar: dos metales distintos unidos generan un "
            "voltaje que depende de la temperatura (efecto Seebeck); cubre hasta 1700 °C, "
            "menos preciso.",
            "RTD (Pt100): platinum resistance that rises with temperature, very accurate and "
            "stable up to about 600 °C. Thermocouple: two dissimilar metals joined produce a "
            "temperature-dependent voltage (Seebeck effect); covers up to 1700 °C, less "
            "accurate."),
        "why": ("Define el rango, la precisión y el diámetro de vaina habitual.",
                "It defines range, accuracy and usual sheath diameter."),
        "worked": ("Pt100 clase A a 100 °C: ±0,35 °C. Termopar K clase 1: ±1,5 °C.",
                   "Pt100 class A at 100 °C: ±0.35 °C. Type K class 1 thermocouple: ±1.5 °C."),
        "mistakes": ("- Elegir Pt100 para 800 °C.", "- Choosing Pt100 for 800 °C."),
    },
    "f.sheath": {
        "essence": (
            "Diámetro exterior del sensor que va dentro de la vaina. Debe entrar en el agujero "
            "con un huelgo chico: el aire entre ambos aísla y retrasa la medición.",
            "Outside diameter of the sensor inside the well. It must fit the bore with small "
            "clearance: air between them insulates and delays the reading."),
        "why": ("Define el agujero d y por lo tanto el diseño de la vaina.",
                "It defines bore d and therefore the well design."),
        "worked": ("Sensor 6 mm en agujero 6,6 mm: huelgo 0,3 mm, bien.",
                   "6 mm sensor in a 6.6 mm bore: 0.3 mm clearance, fine."),
        "mistakes": ("- Sensor de 6 mm en agujero de 9,8 mm: respuesta lenta.",
                     "- 6 mm sensor in a 9.8 mm bore: slow response."),
    },
    "f.spring": {
        "essence": (
            "Un resorte en el cabezal empuja el sensor contra el fondo de la vaina. El contacto "
            "metal con metal transfiere calor mucho mejor que el aire.",
            "A spring in the head pushes the sensor against the well bottom. Metal-to-metal "
            "contact transfers heat much better than air."),
        "why": ("Mejora la respuesta y evita que el sensor vibre suelto.",
                "It improves response and keeps the sensor from vibrating loose."),
        "worked": ("Constante de tiempo típica sin resorte 60 s; con resorte 30 s.",
                   "Typical time constant without spring 60 s; with spring 30 s."),
        "mistakes": ("- Cortar el sensor justo sin dejar recorrido para el resorte.",
                     "- Cutting the sensor exactly without spring travel."),
    },
    "f.sensor_mass": {
        "essence": (
            "Masa del sensor dentro de la vaina. Si está apoyado en la punta, suma masa donde "
            "más baja la frecuencia natural.",
            "Mass of the sensor inside the well. If resting on the tip, it adds mass where it "
            "lowers natural frequency most."),
        "why": ("TS la usa para corregir f_n.", "TS uses it to correct f_n."),
        "worked": ("Sensor de 6 mm × 300 mm ≈ 50 g: baja f_n un 1 a 2 %.",
                   "6 mm × 300 mm sensor ≈ 50 g: lowers f_n 1 to 2 %."),
        "mistakes": ("- Ignorarla en bulbos de termómetro pesados.",
                     "- Ignoring it with heavy thermometer bulbs."),
    },
    "f.thread": {
        "essence": (
            "NPT es una rosca cónica (1:16): al apretar, los filetes se encajan y sellan con "
            "ayuda de sellador. G (BSPP, ISO 228) es cilíndrica: no sella en el filete, necesita "
            "una junta o arandela contra una cara de asiento.",
            "NPT is a tapered thread (1:16): when tightened the threads wedge and seal with "
            "sealant. G (BSPP, ISO 228) is parallel: it does not seal on the thread and needs a "
            "gasket or washer against a seating face."),
        "why": ("No son intercambiables: una NPT en una cupla G filtra.",
                "They are not interchangeable: an NPT in a G coupling leaks."),
        "worked": ("1\" NPT ≈ 33,4 mm; G 1 ≈ 33,25 mm: casi iguales, pero no compatibles.",
                   "1\" NPT ≈ 33.4 mm; G 1 ≈ 33.25 mm: almost equal, but not compatible."),
        "mistakes": ("- Pedir NPT para un equipo europeo con cuplas G.",
                     "- Ordering NPT for European equipment with G couplings."),
    },
}

_CONN = {
    "threaded": (
        ("La rosca transmite la carga por los flancos de los filetes; la raíz de cada filete "
         "es una entalla que concentra esfuerzos, y el primer filete cargado se lleva la mayor "
         "parte. Además, la rosca tiene juego y el apoyo es menos rígido.",
         "The thread transmits load through the flanks; each thread root is a notch that "
         "concentrates stress, and the first engaged thread carries most of it. The thread "
         "also has play and the support is less stiff."),
        ("1\" NPT en agua a 3 m/s: cumple con margen. La misma vaina en gas a 20 m/s: K_t "
         "mayor y H_c menor la dejan fuera.",
         "1\" NPT in water at 3 m/s: passes with margin. The same well in gas at 20 m/s: "
         "higher K_t and lower H_c put it out."),
        ("- Usar roscadas en hidrocarburos o vapor.\n- No usar sellador compatible.",
         "- Using threaded wells in hydrocarbons or steam.\n- Not using compatible "
         "sealant.")),
    "flanged": (
        ("La vaina se suelda o mecaniza a una brida que se abulona a la de la línea. La "
         "brida da un apoyo rígido y permite retirar la vaina para inspección.",
         "The well is welded or machined to a flange bolted to the line flange. The flange "
         "gives a stiff support and allows removing the well for inspection."),
        ("Brida 1½\" clase 300, cónica, U 250: la opción estándar de refinería.",
         "1½\" class 300 flange, tapered, U 250: the standard refinery choice."),
        ("- Clase de brida menor que la de la línea.", "- Flange class lower than the "
                                                       "line's.")),
    "socket_weld": (
        ("La vaina entra en un socket y se suelda con un filete exterior. Es estanca y "
         "barata, pero deja una pequeña rendija entre la vaina y el fondo del socket.",
         "The well goes into a socket and is fillet-welded outside. It is tight and cheap, "
         "but leaves a small crevice between the well and the socket bottom."),
        ("Línea de 1\" de vapor a 40 bar: socket weld es habitual.",
         "1\" steam line at 40 bar: socket weld is common."),
        ("- No dejar el huelgo de 1,6 mm en el fondo del socket (fisura por dilatación).",
         "- Not leaving the 1.6 mm gap at the socket bottom (expansion cracking).")),
    "weld_in": (
        ("La vaina se suelda directamente a la cañería: sin juntas ni roscas, es la conexión "
         "más resistente.",
         "The well is welded directly to the pipe: with no gaskets or threads, it is the "
         "strongest connection."),
        ("Vapor principal a 160 bar y 540 °C: soldada.",
         "Main steam at 160 bar and 540 °C: welded."),
        ("- Usarla donde hace falta retirar la vaina.",
         "- Using it where the well must be removed.")),
    "van_stone": (
        ("La vaina tiene un collar solapado que queda apretado entre la brida loca y la de "
         "la línea: solo el collar toca el fluido, así que la brida puede ser de acero común.",
         "The well has a lapped collar clamped between the loose flange and the line flange: "
         "only the collar touches the fluid, so the flange can be ordinary steel."),
        ("Ácido clorhídrico: vaina de tantalio o Hastelloy con brida loca de acero al "
         "carbono.",
         "Hydrochloric acid: tantalum or Hastelloy well with a loose carbon steel flange."),
        ("- Usarla con alta vibración: el apoyo es menos rígido.",
         "- Using it with high vibration: the support is less stiff.")),
    "sanitary": (
        ("Conexión con abrazadera y junta sobre superficies pulidas, sin rendijas donde "
         "crezcan bacterias.",
         "Clamp and gasket connection on polished surfaces, with no crevices where bacteria "
         "can grow."),
        ("Leche pasteurizada, 3 bar, 80 °C: tri-clamp de 1½\".",
         "Pasteurized milk, 3 bar, 80 °C: 1½\" tri-clamp."),
        ("- Usarla a presiones industriales altas.",
         "- Using it at high industrial pressures.")),
}
for _key, (_ess, _ex, _mis) in _CONN.items():
    DEEP[f"conn.{_key}"] = {
        "essence": _ess,
        "why": ("Define la rigidez del apoyo, la concentración de esfuerzos y el mantenimiento: "
                "elegir mal la conexión puede hacer fallar una vaina bien calculada.",
                "It defines support stiffness, stress concentration and maintenance: the "
                "wrong connection can make a well-calculated thermowell fail."),
        "worked": _ex, "mistakes": _mis}

_PROF = {
    "tapered": (
        ("El diámetro baja linealmente de A a B: la masa se concentra en la raíz y la punta "
         "es liviana. Es la forma que mejor aprovecha el metal en una viga en voladizo.",
         "Diameter falls linearly from A to B: mass concentrates at the root and the tip is "
         "light. It is the shape that best uses metal in a cantilever."),
        ("A 26,7, B 19,05, U 250 mm: f_n ≈ 460 Hz, contra 330 Hz del recto equivalente.",
         "A 26.7, B 19.05, U 250 mm: f_n ≈ 460 Hz, against 330 Hz for the equivalent "
         "straight.")),
    "stepped": (
        ("Dos cilindros: uno grueso en la raíz y uno fino en la punta, unidos por un "
         "escalón. Aproxima al cónico con mecanizado más simple; el escalón agrega una "
         "concentración de esfuerzos.",
         "Two cylinders: a thick one at the root and a thin one at the tip, joined by a "
         "step. It approximates the tapered shape with simpler machining; the step adds a "
         "stress concentration."),
        ("A 22,2, B 12,7, Ls 64 mm: punta fina para respuesta rápida, raíz gruesa.",
         "A 22.2, B 12.7, Ls 64 mm: thin tip for fast response, thick root.")),
    "straight": (
        ("Diámetro constante. El más simple, pero la punta pesa tanto como la raíz y la "
         "frecuencia es la más baja para un mismo largo.",
         "Constant diameter. The simplest, but the tip weighs as much as the root and "
         "frequency is the lowest for a given length."),
        ("A = B = 19 mm, U 150 mm en agua a 1 m/s: cumple holgado y es la opción barata.",
         "A = B = 19 mm, U 150 mm in water at 1 m/s: passes easily and is the cheap "
         "option.")),
}
for _key, (_ess, _ex) in _PROF.items():
    DEEP[f"profile.{_key}"] = {
        "essence": _ess,
        "why": ("El perfil decide cuánta frecuencia y resistencia se obtiene por cada gramo "
                "de metal y por cada peso de mecanizado.",
                "The profile decides how much frequency and strength you get per gram of "
                "metal and per unit of machining cost."),
        "worked": _ex,
        "mistakes": ("- Elegir solo por costo sin verificar la frecuencia.\n"
                     "- Cambiar el perfil en compras sin recalcular.",
                     "- Choosing on cost alone without checking frequency.\n"
                     "- Changing profile at purchasing without recalculating.")}
