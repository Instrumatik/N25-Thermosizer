"""Fichas completas para los términos del glosario que no tienen campo propio."""

from __future__ import annotations

from typing import Any


def _g(title: tuple[str, str], what: tuple[str, str], role: tuple[str, str],
       essence: tuple[str, str], why: tuple[str, str], worked: tuple[str, str],
       mistakes: tuple[str, str], **kw: Any) -> dict[str, Any]:
    return {"title": title, "what": what, "role": role, "essence": essence, "why": why,
            "worked": worked, "mistakes": mistakes, **kw}


NEW: dict[str, dict[str, Any]] = {
    "g.lock_in": _g(
        ("Captura (lock-in)", "Lock-in"),
        ("Fenómeno por el cual, cerca de la resonancia, el desprendimiento de vórtices se "
         "sincroniza con la vibración de la vaina.",
         "Phenomenon by which, near resonance, vortex shedding synchronizes with the well's "
         "vibration."),
        ("Explica por qué TS exige margen respecto de la resonancia y no solo evitar el punto "
         "exacto.",
         "It explains why TS requires margin from resonance and not just avoiding the exact "
         "point."),
        ("Lejos de la resonancia, la estela marca su propio ritmo (f_s = N_S·V/B) y la vaina "
         "apenas se mueve. Cuando f_s se acerca a la frecuencia natural, la vaina empieza a "
         "oscilar y su movimiento lateral «ordena» la separación de la capa límite: los "
         "remolinos se sueltan cuando la vaina llega al extremo de su recorrido. A partir de "
         "ahí la estela sigue a la vaina y no a la velocidad: aunque el caudal cambie un poco, "
         "la frecuencia de desprendimiento queda «capturada» en la natural.\n\n"
         "Es un mecanismo de realimentación: más amplitud ordena más la estela, y una estela "
         "más ordenada empuja con más fuerza y en fase.",
         "Far from resonance the wake sets its own rate (f_s = N_S·V/B) and the well barely "
         "moves. When f_s approaches the natural frequency the well starts oscillating and "
         "its sideways motion «organizes» boundary-layer separation: eddies are shed when the "
         "well reaches the end of its stroke. From then on the wake follows the well, not the "
         "velocity: even if flow changes slightly, the shedding frequency stays «captured» at "
         "the natural one.\n\n"
         "It is a feedback mechanism: more amplitude organizes the wake more, and a more "
         "organized wake pushes harder and in phase."),
        ("Convierte la resonancia en una banda, no en un punto. Una vaina calculada con "
         "r = 0,95 «porque no es exactamente 1» puede pasar mucho tiempo capturada y "
         "romperse.",
         "It turns resonance into a band, not a point. A well calculated at r = 0.95 "
         "«because it is not exactly 1» may spend a long time locked in and break."),
        ("Con f_n,c = 400 Hz, la captura puede abarcar aproximadamente de 0,8 a 1,2 veces la "
         "velocidad de resonancia: si V_res = 30 m/s, todo el rango 24 a 36 m/s es "
         "peligroso.",
         "With f_n,c = 400 Hz, lock-in can span roughly 0.8 to 1.2 times the resonance "
         "velocity: if V_res = 30 m/s, the whole 24 to 36 m/s range is dangerous."),
        ("- Calcular justo debajo de la resonancia sin margen.\n"
         "- Suponer que una variación de caudal «saca» a la vaina de la resonancia.",
         "- Designing just below resonance with no margin.\n"
         "- Assuming a flow change will «pull» the well out of resonance.")),
    "g.standard_flow": _g(
        ("Caudal estándar (Sm³, Nm³, SCF)", "Standard flow (Sm³, Nm³, SCF)"),
        ("Caudal de gas expresado como el volumen que ocuparía en condiciones de referencia.",
         "Gas flow expressed as the volume it would take at reference conditions."),
        ("TS lo convierte a caudal másico con la densidad estándar y a velocidad real con la "
         "densidad de operación.",
         "TS converts it to mass flow with standard density and to actual velocity with "
         "operating density."),
        ("Como el volumen de un gas cambia con P y T, para comparar cantidades se las lleva "
         "a una condición fija. Sm³ (estándar): 15 °C y 101,325 kPa. Nm³ (normal): 0 °C y "
         "101,325 kPa. SCF: pie cúbico a 60 °F y 14,696 psia. Un caudal estándar es en "
         "realidad un caudal de moles (o de masa para composición fija).",
         "Since gas volume changes with P and T, quantities are compared at a fixed "
         "condition. Sm³ (standard): 15 °C and 101.325 kPa. Nm³ (normal): 0 °C and "
         "101.325 kPa. SCF: cubic foot at 60 °F and 14.696 psia. A standard flow is really a "
         "molar flow (or mass flow for fixed composition)."),
        ("Es la forma más común de especificar caudales de gas y la fuente del error más "
         "grave: confundirlo con caudal real.",
         "It is the most common way to specify gas flows and the source of the worst error: "
         "mistaking it for actual flow."),
        ("1 MMSCFD = 1 000 000 SCF/día = 28 317 Sm³/día aprox. ≈ 1180 Sm³/h. A 50 bar y "
         "30 °C, eso son unos 23 m³/h reales.",
         "1 MMSCFD = 1,000,000 SCF/day ≈ 28,317 Sm³/day ≈ 1180 Sm³/h. At 50 bar and 30 °C "
         "that is about 23 actual m³/h."),
        ("- Mezclar Nm³ y Sm³ (5 % de diferencia).\n- Usar Sm³/h como m³/h real.",
         "- Mixing Nm³ and Sm³ (5 % difference).\n- Using Sm³/h as actual m³/h.")),
    "g.velocity_collar": _g(
        ("Collar de soporte", "Velocity collar"),
        ("Anillo en el vástago, cerca de la raíz, que se apoya contra el niple para acortar "
         "el largo que vibra libremente.",
         "Ring on the shank near the root that bears against the nozzle to shorten the "
         "freely vibrating length."),
        ("TS lo menciona como última opción cuando acortar o rigidizar no alcanza.",
         "TS mentions it as a last option when shortening or stiffening is not enough."),
        ("Si el collar queda ajustado dentro del niple, la vaina pasa a apoyarse en dos "
         "puntos y el largo efectivo se reduce: la frecuencia sube con el cuadrado. El "
         "problema es que el ajuste es difícil de garantizar: el niple tiene tolerancias, "
         "se ovaliza y la dilatación cambia la holgura. Un collar flojo golpea y se desgasta "
         "(fretting).",
         "If the collar fits tightly in the nozzle the well rests on two points and the "
         "effective length shrinks: frequency rises with the square. The problem is that the "
         "fit is hard to guarantee: the nozzle has tolerances, goes oval and thermal growth "
         "changes clearance. A loose collar knocks and wears (fretting)."),
        ("La edición 2016 de la norma desaconseja depender de collares porque su efecto "
         "real es incierto.",
         "The 2016 edition of the standard discourages relying on collars because their real "
         "effect is uncertain."),
        ("Vaina con L = 300 mm y collar a 100 mm de la brida: largo libre 200 mm → "
         "frecuencia × 2,25, si el ajuste es perfecto.",
         "Well with L = 300 mm and collar 100 mm from the flange: free length 200 mm → "
         "frequency × 2.25, if the fit is perfect."),
        ("- Usar el collar como solución estándar en vez de rediseñar.\n"
         "- Mecanizar el collar sin medir el niple real.",
         "- Using the collar as a standard fix instead of redesigning.\n"
         "- Machining the collar without measuring the actual nozzle.")),
    "g.time_constant": _g(
        ("Constante de tiempo (τ)", "Time constant (τ)"),
        ("Tiempo que tarda la medición en recorrer el 63,2 % de un cambio brusco de "
         "temperatura.",
         "Time for the reading to cover 63.2 % of a step temperature change."),
        ("Ayuda a elegir entre una vaina rápida (fina) y una robusta (gruesa).",
         "It helps choose between a fast (thin) and a robust (thick) well."),
        ("La vaina y el sensor forman una cadena de resistencias térmicas (película de "
         "fluido, pared metálica, aire del huelgo, vaina del sensor) y de capacidades "
         "(masa que hay que calentar). La respuesta sigue aproximadamente una exponencial: "
         "63 % en τ, 95 % en 3τ, 99 % en 5τ. Un fluido más rápido y más conductor (líquido) "
         "transmite el calor mejor que un gas lento.",
         "Well and sensor form a chain of thermal resistances (fluid film, metal wall, gap "
         "air, sensor sheath) and capacities (mass to be heated). Response roughly follows an "
         "exponential: 63 % at τ, 95 % at 3τ, 99 % at 5τ. A faster, more conductive fluid "
         "(liquid) transfers heat better than a slow gas."),
        ("Un lazo de control con una medición lenta oscila o reacciona tarde. En reactores "
         "exotérmicos puede ser un tema de seguridad.",
         "A control loop with slow measurement oscillates or reacts late. In exothermic "
         "reactors it may be a safety issue."),
        ("τ = 20 s en agua: tras un salto de 50 a 80 °C, a los 20 s marca 69 °C, a los "
         "60 s 78,5 °C. En gas lento la misma vaina puede tener τ = 120 s.",
         "τ = 20 s in water: after a step from 50 to 80 °C, at 20 s it reads 69 °C, at 60 s "
         "78.5 °C. In slow gas the same well may have τ = 120 s."),
        ("- Engrosar la punta para la mecánica sin evaluar la respuesta.\n"
         "- No usar pasta térmica ni resorte en lazos rápidos.",
         "- Thickening the tip for mechanics without assessing response.\n"
         "- Using neither thermal paste nor spring in fast loops.")),
    "g.immersion_error": _g(
        ("Error por conducción (inmersión)", "Conduction (immersion) error"),
        ("Diferencia entre la temperatura del fluido y la que mide el sensor por el calor que "
         "se escapa a lo largo de la vaina hacia la conexión.",
         "Difference between fluid temperature and the sensor reading due to heat escaping "
         "along the well towards the connection."),
        ("Justifica la inmersión mínima que TS recomienda.",
         "It justifies the minimum immersion TS recommends."),
        ("La vaina es una aleta: recibe calor del fluido en la punta y lo conduce hacia la "
         "brida y el cabezal, que están más fríos (o calientes). La punta queda a una "
         "temperatura intermedia. Cuanto más larga la parte sumergida respecto del "
         "diámetro, y cuanto mejor el coeficiente de transferencia del fluido, más se acerca "
         "la punta a la temperatura del fluido. La regla práctica es sumergir de 10 a 15 "
         "diámetros más el largo sensible del sensor.",
         "The well is a fin: it receives heat from the fluid at the tip and conducts it "
         "towards the flange and head, which are colder (or hotter). The tip settles at an "
         "intermediate temperature. The longer the immersed part relative to diameter, and "
         "the better the fluid's heat transfer, the closer the tip gets to fluid temperature. "
         "The rule of thumb is to immerse 10 to 15 diameters plus the sensor's sensitive "
         "length."),
        ("El error puede ser de varios grados en gases lentos con líneas sin aislar: una "
         "medición que «parece» bien está sistemáticamente corrida.",
         "The error can be several degrees in slow gases with uninsulated lines: a reading "
         "that «looks fine» is systematically off."),
        ("Gas a 200 °C, ambiente 20 °C, inmersión 40 mm con B = 19 mm (2 diámetros): error "
         "de varios °C. Con 120 mm (6 diámetros) cae por debajo de 0,5 °C.",
         "Gas at 200 °C, ambient 20 °C, 40 mm immersion with B = 19 mm (2 diameters): error "
         "of several °C. With 120 mm (6 diameters) it drops below 0.5 °C."),
        ("- Acortar la vaina por vibración sin evaluar el error.\n"
         "- No aislar la conexión en líneas calientes.",
         "- Shortening the well for vibration without assessing the error.\n"
         "- Not insulating the connection on hot lines.")),
    "g.stress_concentration": _g(
        ("Factor de concentración de esfuerzos (K_t)", "Stress concentration factor (K_t)"),
        ("Cuánto aumenta el esfuerzo local en un cambio de forma (radio, rosca, escalón) "
         "respecto del esfuerzo nominal.",
         "How much local stress rises at a shape change (fillet, thread, step) relative to "
         "nominal stress."),
        ("Multiplica el esfuerzo dinámico de la raíz.", "It multiplies root dynamic stress."),
        ("Las líneas de fuerza dentro del metal son como el agua en un canal: en un cambio "
         "brusco de sección se aprietan y la intensidad local sube. Un radio amplio las "
         "guía suavemente; una arista viva las amontona en un punto. Por eso las fisuras de "
         "fatiga nacen en la raíz, en el escalón o en el primer filete de la rosca.",
         "Lines of force in metal are like water in a channel: at an abrupt section change "
         "they bunch up and local intensity rises. A generous radius guides them smoothly; a "
         "sharp corner piles them at a point. That is why fatigue cracks start at the root, "
         "the step or the first thread."),
        ("En fatiga, un K_t de 2 equivale a duplicar la carga.",
         "In fatigue, a K_t of 2 is like doubling the load."),
        ("Raíz con radio de 3,2 mm: K_t ≈ 1,1 a 1,3. Rosca NPT: K_t de 2 o más.",
         "Root with 3.2 mm fillet: K_t ≈ 1.1 to 1.3. NPT thread: K_t of 2 or more."),
        ("- Omitir el radio en el plano.\n- Marcar con punzón cerca de la raíz.",
         "- Omitting the fillet on the drawing.\n- Stamping near the root.")),
    "g.magnification": _g(
        ("Factor de magnificación", "Magnification factor"),
        ("Cuánto se amplifica la respuesta dinámica por la cercanía a la resonancia: "
         "F_M = 1/(1 − r²).",
         "How much dynamic response is amplified by proximity to resonance: "
         "F_M = 1/(1 − r²)."),
        ("Multiplica las fuerzas oscilantes en el esfuerzo dinámico.",
         "It multiplies oscillating forces in dynamic stress."),
        ("Si empujás un columpio a un ritmo lento, se mueve lo mismo que si lo empujaras "
         "despacio y lo soltaras. Si lo empujás al ritmo justo, cada empujón suma: la "
         "amplitud crece mucho más que la fuerza. F_M mide ese crecimiento para una "
         "estructura sin amortiguamiento.",
         "If you push a swing at a slow rate it moves as much as if pushed slowly and "
         "released. If you push at the right rate each push adds up: amplitude grows much "
         "more than force. F_M measures that growth for an undamped structure."),
        ("Explica por qué una vaina cerca de la resonancia falla con fuerzas modestas.",
         "It explains why a well near resonance fails under modest forces."),
        ("r = 0,4 → 1,19; r = 0,6 → 1,56; r = 0,8 → 2,78; r = 0,9 → 5,26.",
         "r = 0.4 → 1.19; r = 0.6 → 1.56; r = 0.8 → 2.78; r = 0.9 → 5.26."),
        ("- Creer que el esfuerzo crece linealmente con r.",
         "- Believing stress grows linearly with r.")),
    "g.fatigue_limit": _g(
        ("Límite de fatiga (S_f)", "Fatigue limit (S_f)"),
        ("Amplitud de esfuerzo por debajo de la cual el material soporta un número "
         "prácticamente ilimitado de ciclos.",
         "Stress amplitude below which the material withstands a practically unlimited "
         "number of cycles."),
        ("Es el límite del esfuerzo dinámico.", "It is the dynamic stress limit."),
        ("En cada ciclo de carga, los granos más desfavorablemente orientados se deslizan "
         "levemente y forman bandas de deslizamiento en la superficie. Si la amplitud es alta, "
         "esas bandas se vuelven microfisuras que crecen un poco con cada ciclo, hasta que la "
         "sección restante rompe de golpe. Por debajo del límite, los deslizamientos son "
         "reversibles y la fisura no progresa. La rugosidad, la soldadura y la corrosión "
         "bajan el límite porque ofrecen sitios de inicio.",
         "In each load cycle the worst-oriented grains slip slightly and form slip bands at "
         "the surface. If amplitude is high those bands become microcracks that grow a little "
         "each cycle, until the remaining section breaks suddenly. Below the limit slip is "
         "reversible and the crack does not progress. Roughness, welding and corrosion lower "
         "the limit because they offer initiation sites."),
        ("A cientos de hertz, la vaina acumula ciclos tan rápido que cualquier amplitud "
         "sobre el límite termina en rotura.",
         "At hundreds of hertz the well accumulates cycles so fast that any amplitude above "
         "the limit ends in fracture."),
        ("316 mecanizado ≈ 48 MPa; soldado ≈ 21 MPa (valores típicos).",
         "Machined 316 ≈ 48 MPa; welded ≈ 21 MPa (typical values)."),
        ("- Usar la resistencia a la tracción en vez del límite de fatiga.",
         "- Using tensile strength instead of the fatigue limit.")),
    "g.added_mass": _g(
        ("Masa añadida", "Added mass"),
        ("Masa del fluido que la vaina arrastra consigo al vibrar.",
         "Mass of fluid the well carries with it when vibrating."),
        ("Baja la frecuencia natural en fluidos densos.",
         "It lowers natural frequency in dense fluids."),
        ("Para moverse de un lado a otro, la vaina tiene que acelerar también el fluido que "
         "la rodea. Ese fluido se comporta como si fuera masa extra pegada a ella: para un "
         "cilindro, aproximadamente la masa de fluido del volumen del propio cilindro.",
         "To move back and forth the well must also accelerate the surrounding fluid. That "
         "fluid acts as extra mass attached to it: for a cylinder, roughly the fluid mass in "
         "the cylinder's own volume."),
        ("En agua puede bajar la frecuencia 3 a 6 %; en gas es despreciable.",
         "In water it can lower frequency 3 to 6 %; in gas it is negligible."),
        ("Acero 8000 kg/m³ en agua 1000 kg/m³: f baja ≈ 1/√(1 + 1000/8000 × factor) → "
         "unos puntos porcentuales.",
         "Steel 8000 kg/m³ in water 1000 kg/m³: f drops ≈ 1/√(1 + 1000/8000 × factor) → a "
         "few percent."),
        ("- Usar ratings de proveedor (sin masa añadida) para líquidos.",
         "- Using supplier ratings (no added mass) for liquids.")),
    "g.pmi": _g(
        ("PMI (identificación positiva de material)", "PMI (positive material "
                                                     "identification)"),
        ("Ensayo no destructivo que verifica la composición química de la pieza.",
         "Non-destructive test that verifies the part's chemical composition."),
        ("Se pide en la hoja de datos para asegurar que el material es el especificado.",
         "It is requested on the datasheet to ensure the material is as specified."),
        ("Un equipo portátil de fluorescencia de rayos X (XRF) excita los átomos de la "
         "superficie y mide la energía característica que emite cada elemento: así detecta "
         "cromo, níquel, molibdeno. Los equipos de chispa (OES) además miden carbono.",
         "A portable X-ray fluorescence (XRF) unit excites surface atoms and measures the "
         "characteristic energy each element emits: it detects chromium, nickel, "
         "molybdenum. Spark (OES) units also measure carbon."),
        ("Un 304 entregado como 316 se ve igual pero no resiste cloruros. El PMI lo "
         "detecta en segundos.",
         "A 304 delivered as 316 looks the same but does not resist chlorides. PMI detects "
         "it in seconds."),
        ("316 debe mostrar ≈ 2 a 3 % de Mo; un 304 da ≈ 0 %.",
         "316 should show ≈ 2 to 3 % Mo; a 304 gives ≈ 0 %."),
        ("- Confiar solo en el certificado del proveedor.\n"
         "- Pedir XRF para distinguir 316 de 316L (hace falta OES por el carbono).",
         "- Relying only on the supplier certificate.\n"
         "- Asking for XRF to distinguish 316 from 316L (OES is needed for carbon).")),
    "g.support_plane": _g(
        ("Plano de soporte", "Support plane"),
        ("Plano donde la vaina queda empotrada: desde ahí se mide el largo que vibra.",
         "Plane where the well is fixed: the vibrating length is measured from there."),
        ("Define L para el cálculo.", "It defines L for the calculation."),
        ("En una bridada es la cara de la brida; en una roscada, el punto donde la rosca "
         "ajusta; en una soldada, la soldadura. Si el niple es largo o flexible, el apoyo "
         "real está más atrás de lo que parece.",
         "On a flanged well it is the flange face; on a threaded one, where the thread "
         "seats; on a welded one, the weld. If the nozzle is long or flexible, the real "
         "support is further back than it seems."),
        ("Medir L desde un plano equivocado cambia la frecuencia con el cuadrado.",
         "Measuring L from the wrong plane changes frequency with the square."),
        ("Error de 25 mm en L = 250 mm: frecuencia ±20 %.",
         "A 25 mm error in L = 250 mm: frequency ±20 %."),
        ("- Medir desde la superficie de la cañería.",
         "- Measuring from the pipe surface.")),
    "g.hydro_test": _g(
        ("Prueba hidrostática", "Hydrostatic test"),
        ("Ensayo con agua a presión superior a la de diseño para verificar resistencia y "
         "estanqueidad.",
         "Water test at pressure above design to verify strength and tightness."),
        ("TS la recomienda en la hoja de datos.", "TS recommends it on the datasheet."),
        ("Se usa agua porque es casi incompresible: almacena poca energía y, si algo falla, "
         "no explota como un gas. La presión de prueba (típicamente 1,5 veces la de diseño) "
         "revela poros, soldaduras defectuosas o paredes delgadas.",
         "Water is used because it is almost incompressible: it stores little energy and, if "
         "something fails, it does not explode like a gas. Test pressure (typically 1.5 "
         "times design) reveals pores, defective welds or thin walls."),
        ("Una vaina con poro filtra proceso al cabezal; la prueba lo descubre antes.",
         "A porous well leaks process into the head; the test finds it first."),
        ("Diseño 40 barg → prueba 60 barg durante el tiempo que fije la especificación.",
         "Design 40 barg → test at 60 barg for the time the specification sets."),
        ("- Probar inoxidables con agua con cloruros altos.",
         "- Testing stainless with high-chloride water.")),
    "g.pt100": _g(
        ("Pt100", "Pt100"),
        ("Sensor de resistencia de platino que vale 100 Ω a 0 °C.",
         "Platinum resistance sensor worth 100 Ω at 0 °C."),
        ("Es el sensor más común en procesos hasta unos 600 °C.",
         "It is the most common process sensor up to about 600 °C."),
        ("La resistencia eléctrica de un metal sube con la temperatura porque los átomos "
         "vibran más y dispersan a los electrones. En el platino esa relación es muy estable "
         "y casi lineal: unos 0,385 Ω por °C. El transmisor mide la resistencia y la "
         "convierte a temperatura.",
         "A metal's electrical resistance rises with temperature because atoms vibrate more "
         "and scatter electrons. In platinum this relation is very stable and nearly linear: "
         "about 0.385 Ω per °C. The transmitter measures resistance and converts it to "
         "temperature."),
        ("Es preciso y estable, pero su elemento es frágil a vibración y choque.",
         "It is accurate and stable, but its element is fragile to vibration and shock."),
        ("A 100 °C vale 138,5 Ω. Un cable de 2 hilos de 1 Ω agrega ≈ 2,6 °C de error; con "
         "3 o 4 hilos se compensa.",
         "At 100 °C it is 138.5 Ω. A 2-wire cable of 1 Ω adds ≈ 2.6 °C error; 3 or 4 wires "
         "compensate."),
        ("- Usar 2 hilos en distancias largas.", "- Using 2 wires over long distances.")),
    "g.inline_resonance": _g(
        ("Resonancia en línea", "In-line resonance"),
        ("Vibración en la dirección del flujo cuando 2·f_s coincide con la frecuencia natural.",
         "Vibration along the flow when 2·f_s matches the natural frequency."),
        ("Define el límite r < 0,4 cuando el Scruton es bajo.",
         "It defines the r < 0.4 limit when Scruton is low."),
        ("Cada remolino, sea de un lado o del otro, produce un pequeño pulso de arrastre "
         "hacia atrás: dos pulsos por ciclo de estela. Si ese ritmo doble coincide con la "
         "frecuencia natural, la vaina vibra a lo largo del flujo. La fuerza es chica, pero "
         "en fluidos densos el amortiguamiento no alcanza para frenarla.",
         "Each eddy, from either side, produces a small backward drag pulse: two pulses per "
         "wake cycle. If that double rate matches the natural frequency, the well vibrates "
         "along the flow. The force is small, but in dense fluids damping is not enough to "
         "stop it."),
        ("Fue la causa de la falla del reactor Monju en 1995 y la razón principal de la "
         "edición 2016 de la norma.",
         "It caused the Monju reactor failure in 1995 and is the main reason for the 2016 "
         "edition of the standard."),
        ("f_n,c = 420 Hz → resonancia en línea a f_s = 210 Hz.",
         "f_n,c = 420 Hz → in-line resonance at f_s = 210 Hz."),
        ("- Evaluar solo la resonancia transversal.",
         "- Assessing only transverse resonance.")),
    "g.transverse_resonance": _g(
        ("Resonancia transversal", "Transverse resonance"),
        ("Vibración perpendicular al flujo cuando f_s coincide con la frecuencia natural.",
         "Vibration across the flow when f_s matches the natural frequency."),
        ("Define el límite r < 0,8.", "It defines the r < 0.8 limit."),
        ("La fuerza de sustentación alterna de lado con cada remolino; si su ritmo coincide "
         "con la frecuencia natural, la amplitud crece hasta valores destructivos. Es la "
         "fuerza más grande de la estela.",
         "The lift force alternates sides with each eddy; if its rate matches the natural "
         "frequency, amplitude grows to destructive values. It is the largest wake force."),
        ("Ningún amortiguamiento razonable la hace aceptable: hay que evitarla siempre.",
         "No reasonable damping makes it acceptable: it must always be avoided."),
        ("f_n,c = 420 Hz → resonancia transversal a f_s = 420 Hz; límite 336 Hz.",
         "f_n,c = 420 Hz → transverse resonance at f_s = 420 Hz; limit 336 Hz."),
        ("- Operar entre 0,8 y 1,2 confiando en el amortiguamiento.",
         "- Operating between 0.8 and 1.2 relying on damping.")),
    "g.thermocouple": _g(
        ("Termopar", "Thermocouple"),
        ("Sensor formado por dos alambres de metales distintos unidos en un punto.",
         "Sensor made of two wires of different metals joined at a point."),
        ("Se usa en altas temperaturas o donde se necesita robustez.",
         "It is used at high temperature or where robustness is needed."),
        ("En un metal con un extremo caliente y otro frío, los electrones del extremo "
         "caliente tienen más energía y se difunden hacia el frío, creando un voltaje. Cada "
         "metal lo hace con distinta intensidad; uniendo dos metales distintos aparece una "
         "diferencia neta medible (efecto Seebeck), del orden de 40 µV/°C en un tipo K.",
         "In a metal with a hot and a cold end, electrons at the hot end have more energy "
         "and diffuse to the cold end, creating a voltage. Each metal does it with a "
         "different intensity; joining two different metals gives a net measurable "
         "difference (Seebeck effect), around 40 µV/°C for type K."),
        ("Mide hasta 1200 °C (K) o 1700 °C (S, R, B), pero es menos preciso que una Pt100 "
         "y necesita compensación de junta fría.",
         "It measures up to 1200 °C (K) or 1700 °C (S, R, B), but is less accurate than a "
         "Pt100 and needs cold-junction compensation."),
        ("Tipo K a 500 °C: ≈ 20,6 mV.", "Type K at 500 °C: ≈ 20.6 mV."),
        ("- Extender con cable de cobre en vez de cable compensado.",
         "- Extending with copper wire instead of compensating cable.")),
    "g.skin_point": _g(
        ("Termopar de piel (skin point)", "Skin-point thermocouple"),
        ("Termopar soldado a la superficie exterior de un tubo de horno o equipo, sin vaina.",
         "Thermocouple welded to the outer surface of a furnace tube or equipment, without a "
         "well."),
        ("Es una alternativa sin intrusión cuando no se puede poner vaina.",
         "It is a non-intrusive alternative when no well can be installed."),
        ("Mide la temperatura del metal, no la del fluido. En tubos de horno se usa para "
         "controlar que el metal no pase su límite (coquificación, creep).",
         "It measures metal temperature, not fluid temperature. In furnace tubes it is used "
         "to keep metal below its limit (coking, creep)."),
        ("Evita el riesgo de vibración por completo, pero la medición tiene otra "
         "interpretación.",
         "It avoids vibration risk entirely, but the reading has a different meaning."),
        ("Tubo de horno con fluido a 400 °C y metal a 520 °C: el skin point marca 520.",
         "Furnace tube with fluid at 400 °C and metal at 520 °C: the skin point reads 520."),
        ("- Usarlo como medición de proceso.", "- Using it as a process measurement.")),
    "g.thermowell": _g(
        ("Termopozo (termovaina)", "Thermowell"),
        ("Tubo cerrado en un extremo que se inserta en el proceso para alojar un sensor de "
         "temperatura.",
         "Tube closed at one end, inserted into the process to house a temperature sensor."),
        ("Es la pieza que TS calcula.", "It is the part TS calculates."),
        ("Separa el sensor del fluido: lo protege de la presión, la corrosión y la "
         "velocidad, y permite cambiar el sensor sin abrir la línea. A cambio, agrega masa "
         "térmica (respuesta más lenta) y es una viga en voladizo expuesta al flujo, con "
         "riesgo de vibración.",
         "It separates the sensor from the fluid: it protects it from pressure, corrosion "
         "and velocity, and allows changing the sensor without opening the line. In exchange "
         "it adds thermal mass (slower response) and is a cantilever exposed to flow, with "
         "vibration risk."),
        ("Una vaina que falla puede liberar el fluido del proceso y dañar equipos aguas "
         "abajo.",
         "A failing well can release process fluid and damage downstream equipment."),
        ("Bridada 1½\" clase 300, cónica, 316, U 250 mm: la configuración más común en "
         "refinería.",
         "Flanged 1½\" class 300, tapered, 316, U 250 mm: the most common refinery setup."),
        ("- Comprarla por catálogo sin cálculo.", "- Buying it from a catalogue without "
                                                  "calculation.")),
    "g.bimetallic": _g(
        ("Termómetro bimetálico", "Bimetallic thermometer"),
        ("Termómetro de esfera con un espiral de dos metales soldados.",
         "Dial thermometer with a coil of two bonded metals."),
        ("Es indicación local; se monta en la misma vaina.",
         "It is local indication; mounted in the same well."),
        ("Dos metales con distinta dilatación térmica, unidos, se curvan al calentarse "
         "porque uno se alarga más que el otro. Enrollados en espiral, esa curvatura se "
         "convierte en giro de la aguja.",
         "Two metals with different thermal expansion, bonded, bend when heated because one "
         "grows more than the other. Wound in a coil, that bending becomes needle "
         "rotation."),
        ("No necesita energía, pero su bulbo es largo: la vaina debe tener inmersión "
         "suficiente para todo el elemento.",
         "It needs no power, but its stem is long: the well must immerse the whole "
         "element."),
        ("Rango 0 a 200 °C, precisión típica ±1 % de escala = ±2 °C.",
         "Range 0 to 200 °C, typical accuracy ±1 % of span = ±2 °C."),
        ("- Elegir un rango donde la operación quede en el extremo de la escala.",
         "- Choosing a range where operation sits at the end of the scale.")),
    "g.ceramic_sheath": _g(
        ("Vaina cerámica", "Ceramic sheath"),
        ("Tubo de alúmina u otra cerámica para termopares en hornos a muy alta temperatura.",
         "Alumina or other ceramic tube for thermocouples in very high-temperature "
         "furnaces."),
        ("Fuera del alcance del cálculo ASME (no es metálica).",
         "Outside the scope of the ASME calculation (not metallic)."),
        ("Las cerámicas resisten temperaturas donde los metales se oxidan o funden, y son "
         "químicamente inertes, pero son frágiles: no toleran golpes térmicos ni flexión.",
         "Ceramics withstand temperatures where metals oxidize or melt, and are chemically "
         "inert, but they are brittle: they do not tolerate thermal shock or bending."),
        ("Se usan en hornos, no en cañerías con flujo.",
         "They are used in furnaces, not in flowing pipes."),
        ("Alúmina 99,7 %: hasta 1700 °C.", "99.7 % alumina: up to 1700 °C."),
        ("- Introducirla rápido en un horno caliente (se fisura).",
         "- Inserting it quickly into a hot furnace (it cracks).")),
}
