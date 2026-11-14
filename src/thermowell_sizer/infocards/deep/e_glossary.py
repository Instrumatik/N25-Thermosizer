"""Segunda pasada: términos del glosario llevados al nivel del modelo."""

from __future__ import annotations

from typing import Any

DEEP: dict[str, dict[str, Any]] = {
    "g.ceramic_sheath": {
        "essence": (
            "Por encima de unos 1100 a 1200 °C los metales de vaina se oxidan rápido, pierden "
            "resistencia y, peor aún, liberan átomos que contaminan los alambres del termopar "
            "y corren su calibración. Las cerámicas, como la alúmina (Al₂O₃) o el carburo de "
            "silicio, tienen enlaces iónicos y covalentes muy fuertes: no se oxidan porque ya "
            "son óxidos, y no se ablandan hasta temperaturas muy altas.\n\n"
            "A cambio son frágiles: no se deforman antes de romperse. Un choque térmico "
            "(meterla fría en un horno caliente) produce una diferencia de dilatación entre "
            "la superficie y el centro que la fisura.",
            "Above about 1100 to 1200 °C metal sheaths oxidise fast, lose strength and, worse, "
            "release atoms that contaminate thermocouple wires and shift their calibration. "
            "Ceramics such as alumina (Al₂O₃) or silicon carbide have very strong ionic and "
            "covalent bonds: they do not oxidise because they already are oxides, and they do "
            "not soften until very high temperatures.\n\n"
            "In exchange they are brittle: they do not deform before breaking. A thermal shock "
            "(inserting it cold into a hot furnace) produces a difference in expansion between "
            "surface and core that cracks it."),
        "why": (
            "Es la única opción para hornos, fundiciones y combustión a muy alta temperatura. "
            "No es una termovaina de proceso a presión: no se calcula con la norma de "
            "termovainas y no debe usarse donde haya presión o flujo que la cargue.",
            "It is the only option for furnaces, foundries and very high temperature "
            "combustion. It is not a pressure process thermowell: it is not calculated with "
            "the thermowell standard and must not be used where pressure or flow loads it."),
        "worked": (
            "Horno a 1450 °C con termopar tipo B: vaina de alúmina 99,7 % (admite hasta "
            "≈ 1700 °C). Se inserta a unos 50 a 100 mm por minuto para que la temperatura del "
            "tubo se iguale sin fisurarse. Una vaina de Inconel 600 a esa temperatura se "
            "oxidaría en semanas.",
            "Furnace at 1450 °C with a type B thermocouple: 99.7 % alumina sheath (good to "
            "≈ 1700 °C). It is inserted at about 50 to 100 mm per minute so the tube "
            "temperature equalises without cracking. An Inconel 600 sheath at that temperature "
            "would oxidise within weeks."),
        "mistakes": (
            "- Insertarla de golpe en un horno caliente.\n"
            "- Montarla horizontal y larga sin apoyo: se dobla por su propio peso a alta "
            "temperatura.\n"
            "- Usarla en un fluido a presión.",
            "- Inserting it suddenly into a hot furnace.\n"
            "- Mounting it long and horizontal without support: it sags under its own weight "
            "at high temperature.\n"
            "- Using it in a pressurised fluid."),
    },
    "g.skin_point": {
        "essence": (
            "En un horno, el fluido va por dentro de los tubos y la llama calienta el exterior. "
            "El calor tiene que atravesar la pared del tubo, y para eso la superficie exterior "
            "tiene que estar más caliente que el fluido: la diferencia es proporcional al "
            "flujo de calor y al espesor de la pared, y crece si por dentro se forma coque o "
            "depósitos, que aíslan.\n\n"
            "El skin point mide esa temperatura de metal directamente, con un termopar soldado "
            "o fijado a la pared. No mide el proceso: mide cuánto sufre el tubo.",
            "In a heater, fluid flows inside the tubes and the flame heats the outside. Heat "
            "must cross the tube wall, and for that the outer surface must be hotter than the "
            "fluid: the difference is proportional to heat flux and wall thickness, and grows "
            "if coke or deposits form inside, which insulate.\n\n"
            "The skin point measures that metal temperature directly, with a thermocouple "
            "welded or clamped to the wall. It does not measure the process: it measures how "
            "much the tube suffers."),
        "why": (
            "La vida de un tubo de horno depende de la temperatura de metal por la fluencia "
            "lenta (creep): unos 15 a 20 °C de más pueden reducir su vida a la mitad. El skin "
            "point es la alarma de coquización y de llama mal distribuida.",
            "Heater tube life depends on metal temperature through creep: some 15 to 20 °C too "
            "much can halve it. The skin point is the alarm for coking and poorly distributed "
            "flame."),
        "worked": (
            "Fluido a 400 °C, metal limpio a 480 °C. Tras meses, el skin point marca 520 °C con "
            "la misma carga: el coque interno agregó 40 °C de resistencia térmica. Si el límite "
            "del tubo es 550 °C, queda poco margen y hay que planificar el decoquizado.",
            "Fluid at 400 °C, clean metal at 480 °C. After months, the skin point reads 520 °C "
            "at the same load: internal coke added 40 °C of thermal resistance. If the tube "
            "limit is 550 °C there is little margin and decoking must be planned."),
        "mistakes": (
            "- Usarlo como medición del proceso.\n"
            "- Ubicarlo del lado expuesto a la llama directa sin escudo: marca de más.\n"
            "- Calcularlo con la norma de termovainas: no tiene vaina.",
            "- Using it as a process measurement.\n"
            "- Placing it on the side exposed to direct flame without a shield: it reads "
            "high.\n"
            "- Calculating it with the thermowell standard: it has no well."),
    },
    "g.support_plane": {
        "essence": (
            "Una viga en voladizo vibra desde el punto donde está empotrada. El plano de "
            "soporte es ese punto: donde la vaina deja de poder moverse. En una bridada es la "
            "cara de la brida; en una roscada, el asiento de la rosca; en una soldada, el "
            "cordón.\n\n"
            "La realidad no es un empotramiento perfecto: la brida, el niple y la propia "
            "cañería ceden un poco. Ese ceder equivale a correr el plano de soporte hacia "
            "atrás, y es lo que la norma corrige con el factor de flexibilidad del soporte "
            "(H_c), que baja la frecuencia natural «ideal» a la instalada.",
            "A cantilever vibrates from the point where it is fixed. The support plane is "
            "that point: where the well can no longer move. On a flanged well it is the "
            "flange face; on a threaded well, the thread seat; on a welded well, the weld.\n\n"
            "Reality is not a perfect fixed end: flange, nozzle and the pipe itself give a "
            "little. That give is equivalent to moving the support plane back, and it is what "
            "the standard corrects with the support compliance factor (H_c), lowering the "
            "«ideal» natural frequency to the installed one."),
        "why": (
            "Toda la frecuencia natural se calcula desde este plano: como f ∝ 1/L², medir "
            "desde el lugar equivocado cambia mucho el resultado.",
            "All natural frequency is calculated from this plane: since f ∝ 1/L², measuring "
            "from the wrong place changes the result a lot."),
        "worked": (
            "L = 250 mm medido bien. Si se mide desde la superficie del caño y no desde la "
            "brida (25 mm más corto): f calculada × (250/225)² = 1,23 → 23 % optimista. Al "
            "revés, 25 mm de más da 17 % pesimista.",
            "L = 250 mm measured correctly. If measured from the pipe surface instead of the "
            "flange (25 mm shorter): computed f × (250/225)² = 1.23 → 23 % optimistic. The "
            "other way round, 25 mm too long gives 17 % pessimistic."),
        "mistakes": (
            "- Medir desde la pared de la cañería.\n"
            "- Ignorar un niple largo y delgado, que flexa y corre el empotramiento.",
            "- Measuring from the pipe wall.\n"
            "- Ignoring a long thin nozzle, which flexes and moves the fixed point."),
    },
    "g.transverse_resonance": {
        "essence": (
            "Detrás de la vaina, los remolinos se desprenden alternadamente de arriba y de "
            "abajo (calle de vórtices de von Kármán). Cada desprendimiento deja una zona de "
            "baja presión de un lado, y la vaina recibe un empujón lateral que cambia de "
            "sentido con cada remolino: una fuerza de sustentación que oscila a la frecuencia "
            "de estela f_s, perpendicular al flujo.\n\n"
            "Cuando f_s coincide con la frecuencia natural, la vaina entra en resonancia "
            "transversal. Además, el propio movimiento de la vaina ordena el desprendimiento y "
            "lo «engancha» (lock-in), así que la resonancia se mantiene en un rango de "
            "velocidades y no solo en un punto.",
            "Behind the well, eddies shed alternately from top and bottom (von Kármán vortex "
            "street). Each shedding leaves a low-pressure zone on one side, and the well gets "
            "a sideways push that reverses with each eddy: a lift force oscillating at wake "
            "frequency f_s, perpendicular to the flow.\n\n"
            "When f_s matches natural frequency, the well enters transverse resonance. "
            "Moreover the well's own motion organises shedding and «locks it in», so "
            "resonance holds over a range of velocities, not just at one point."),
        "why": (
            "La fuerza transversal es la mayor de la estela: en resonancia la amplitud puede "
            "ser decenas de veces la estática. Ninguna termovaina debe operar ahí.",
            "Transverse force is the largest of the wake: at resonance amplitude can be tens "
            "of times the static one. No thermowell may run there."),
        "worked": (
            "f_n,c = 420 Hz, B = 15,9 mm, N_S = 0,22. La resonancia transversal ocurre en "
            "V = 420 × 0,0159 / 0,22 = 30 m/s. Con límite 0,8, la velocidad máxima es "
            "24 m/s; con límite 0,4 (resonancia en línea), 12 m/s.",
            "f_n,c = 420 Hz, B = 15.9 mm, N_S = 0.22. Transverse resonance occurs at "
            "V = 420 × 0.0159 / 0.22 = 30 m/s. With the 0.8 limit maximum velocity is 24 m/s; "
            "with the 0.4 limit (in-line resonance), 12 m/s."),
        "mistakes": ("- Pensar que solo existe la resonancia transversal y olvidar la en línea.",
                     "- Thinking only transverse resonance exists and forgetting in-line."),
    },
    "g.hydro_test": {
        "essence": (
            "Se llena la pieza (o la línea con la vaina instalada) con agua y se presuriza por "
            "encima de la presión de diseño, típicamente 1,5 veces, durante un tiempo fijado. "
            "Se usa agua porque es casi incompresible: almacena muy poca energía, así que si "
            "algo falla la presión cae de inmediato y no hay explosión, a diferencia de una "
            "prueba con gas.\n\n"
            "Verifica dos cosas: que no haya fugas (soldaduras, poros, rosca) y que la pieza "
            "no se deforme de forma permanente.",
            "The part (or the line with the well installed) is filled with water and "
            "pressurised above design pressure, typically 1.5 times, for a set time. Water is "
            "used because it is nearly incompressible: it stores very little energy, so if "
            "something fails pressure drops at once and there is no explosion, unlike a gas "
            "test.\n\n"
            "It checks two things: no leaks (welds, pores, thread) and no permanent "
            "deformation."),
        "why": (
            "Es la evidencia documental de que la frontera de presión es estanca. En vainas "
            "soldadas a partir de varias piezas detecta poros que el cálculo no ve.",
            "It is the documented evidence that the pressure boundary is tight. In wells "
            "welded from several pieces it detects pores the calculation cannot see."),
        "worked": (
            "Diseño 40 barg → prueba 60 barg. La vaina debe admitir esa presión con margen: "
            "si P_c es 300 bar, sobra. Para inoxidables, el agua debe tener pocos cloruros "
            "(por ejemplo, menos de 50 ppm) y secarse después, para no dejar sales que "
            "causen picaduras.",
            "Design 40 barg → test 60 barg. The well must hold that pressure with margin: if "
            "P_c is 300 bar, there is plenty. For stainless steels the water must be low in "
            "chlorides (for example under 50 ppm) and dried afterwards, so no salts remain to "
            "cause pitting."),
        "mistakes": (
            "- Usar agua de red con cloruros en inoxidables y dejarla adentro.\n"
            "- Hacer la prueba neumática por comodidad sin las precauciones necesarias.",
            "- Using chloride-rich mains water on stainless steel and leaving it inside.\n"
            "- Doing a pneumatic test for convenience without the necessary precautions."),
    },
    "g.bimetallic": {
        "essence": (
            "Dos tiras de metales con distinto coeficiente de dilatación (por ejemplo, un "
            "acero y una aleación de níquel con muy poca dilatación) se sueldan a lo largo. "
            "Al calentarse, una se estira más que la otra; como están unidas, la tira se "
            "curva. Enrollada en espiral o hélice, esa curvatura se convierte en un giro que "
            "mueve directamente la aguja, sin electricidad.",
            "Two strips of metals with different expansion coefficients (for example a steel "
            "and a very low expansion nickel alloy) are bonded along their length. When "
            "heated, one stretches more than the other; since they are joined, the strip "
            "bends. Wound into a spiral or helix, that bending turns into rotation that moves "
            "the pointer directly, with no electricity."),
        "why": (
            "Es la indicación local más común en planta: barata, sin energía y fácil de leer. "
            "Para la termovaina importa porque su bulbo es largo y pesado: requiere inmersión "
            "suficiente en todo el largo sensible y su masa baja la frecuencia natural.",
            "It is the most common local indication in plants: cheap, unpowered and easy to "
            "read. For the thermowell it matters because its stem is long and heavy: it needs "
            "enough immersion over its whole sensitive length and its mass lowers natural "
            "frequency."),
        "worked": (
            "Esfera de 0 a 200 °C, precisión ±1 % de escala = ±2 °C. Su elemento sensible "
            "mide unos 50 mm: con una inmersión de 40 mm, la lectura queda por debajo de la "
            "real porque parte del espiral está fuera del fluido.",
            "0 to 200 °C dial, accuracy ±1 % of span = ±2 °C. Its sensitive element is about "
            "50 mm long: with 40 mm immersion the reading stays below actual because part of "
            "the coil is out of the fluid."),
        "mistakes": (
            "- Usarlo para control o custodia.\n"
            "- Montarlo en una línea que vibra: la aguja oscila y el mecanismo se gasta.",
            "- Using it for control or custody.\n"
            "- Mounting it on a vibrating line: the pointer swings and the mechanism wears."),
    },
    "g.magnification": {
        "essence": (
            "Cuando una fuerza oscilante empuja un resorte con masa, la respuesta no depende "
            "solo del tamaño de la fuerza, sino de qué tan cerca está su frecuencia de la "
            "frecuencia natural. Lejos (r = f/f_n pequeño), la vaina se dobla como si la "
            "fuerza fuera estática. Al acercarse, la inercia y la rigidez se van "
            "compensando, cada empuje suma energía y la amplitud crece. Sin amortiguamiento, "
            "F_M = 1/(1 − r²) tiende a infinito en r = 1.",
            "When an oscillating force pushes a spring with mass, the response depends not "
            "only on force size but on how close its frequency is to natural frequency. Far "
            "away (small r = f/f_n), the well bends as if the force were static. Getting "
            "closer, inertia and stiffness offset each other, each push adds energy and "
            "amplitude grows. Without damping, F_M = 1/(1 − r²) goes to infinity at r = 1."),
        "why": (
            "Multiplica el esfuerzo dinámico. Explica por qué una vaina que cumple fatiga con "
            "r = 0,4 puede fallar con r = 0,8 aunque la fuerza haya cambiado poco.",
            "It multiplies dynamic stress. It explains why a well passing fatigue at r = 0.4 "
            "may fail at r = 0.8 even though force has changed little."),
        "worked": (
            "r = 0,4 → 1,19; r = 0,6 → 1,56; r = 0,8 → 2,78; r = 0,9 → 5,26. Un esfuerzo "
            "estático de 5 MPa queda en 6 MPa a r = 0,4, pero en 26 MPa a r = 0,9: por "
            "encima del límite de fatiga de un 316 soldado.",
            "r = 0.4 → 1.19; r = 0.6 → 1.56; r = 0.8 → 2.78; r = 0.9 → 5.26. A static stress "
            "of 5 MPa becomes 6 MPa at r = 0.4, but 26 MPa at r = 0.9: above a welded 316's "
            "fatigue limit."),
        "mistakes": ("- Calcular el esfuerzo dinámico sin magnificación.",
                     "- Computing dynamic stress without magnification."),
    },
    "g.thermowell": {
        "essence": (
            "Una termovaina es un tubo cerrado en un extremo, de pared gruesa y mecanizado de "
            "barra, que entra en la cañería o el recipiente y deja al sensor afuera del "
            "fluido. Separa dos cosas que el sensor solo no puede resolver:\n\n"
            "- Mecánica: soporta la presión, el flujo, la corrosión y la erosión.\n"
            "- Mantenimiento: el sensor se puede sacar y calibrar sin abrir el proceso.\n\n"
            "A cambio, introduce dos problemas: retrasa la medición (el calor atraviesa más "
            "metal y aire) y es un objeto metido en el flujo, que puede vibrar.",
            "A thermowell is a tube closed at one end, thick-walled and machined from bar, "
            "that enters the pipe or vessel and keeps the sensor out of the fluid. It "
            "separates two things the sensor alone cannot handle:\n\n"
            "- Mechanics: it withstands pressure, flow, corrosion and erosion.\n"
            "- Maintenance: the sensor can be removed and calibrated without opening the "
            "process.\n\n"
            "In exchange it introduces two problems: it delays the reading (heat crosses more "
            "metal and air) and it is an object in the flow that can vibrate."),
        "why": (
            "Es la pieza que TS dimensiona. Su falla no es un mal dato: es una fuga de proceso "
            "o un trozo de metal viajando por la línea hacia una bomba o un compresor.",
            "It is the part TS sizes. Its failure is not bad data: it is a process leak or a "
            "piece of metal travelling down the line towards a pump or compressor."),
        "worked": (
            "Bridada 1½\" clase 300, cónica, 316, U 250 mm, agujero 6,6 mm: la configuración "
            "más común en refinería. En gas a 25 m/s puede no cumplir y hay que acortarla a "
            "190 mm o pasar a una raíz más gruesa.",
            "Flanged 1½\" class 300, tapered, 316, U 250 mm, 6.6 mm bore: the most common "
            "refinery configuration. In gas at 25 m/s it may fail and must be shortened to "
            "190 mm or given a thicker root."),
        "mistakes": (
            "- Elegirla por catálogo sin cálculo de vibración.\n"
            "- Pensar que más larga es siempre mejor medición.",
            "- Picking it from a catalogue without a vibration calculation.\n"
            "- Thinking longer always means better measurement."),
    },
    "g.added_mass": {
        "essence": (
            "Cuando la vaina se mueve, no se mueve sola: tiene que empujar el fluido que la "
            "rodea para hacerse lugar, y ese fluido acelera con ella. Para la vibración es "
            "como si la vaina pesara más. Para un cilindro, la masa añadida por unidad de "
            "largo es aproximadamente la masa del fluido que desplaza: ρ_fluido × π·B²/4.\n\n"
            "La rigidez no cambia, la masa sube, y la frecuencia natural (√(rigidez/masa)) "
            "baja. El efecto depende de la relación de densidades: grande en líquidos, "
            "despreciable en gases a baja presión.",
            "When the well moves it does not move alone: it must push the surrounding fluid "
            "out of the way, and that fluid accelerates with it. For vibration it is as if "
            "the well were heavier. For a cylinder, added mass per unit length is roughly the "
            "mass of fluid it displaces: ρ_fluid × π·B²/4.\n\n"
            "Stiffness does not change, mass rises, and natural frequency (√(stiffness/mass)) "
            "falls. The effect depends on the density ratio: large in liquids, negligible in "
            "low-pressure gases."),
        "why": (
            "Ignorarla da una frecuencia natural optimista en líquidos. Es una de las "
            "diferencias entre el cálculo de la norma y los ratings genéricos de catálogo.",
            "Ignoring it gives an optimistic natural frequency in liquids. It is one of the "
            "differences between the standard's calculation and generic catalogue ratings."),
        "worked": (
            "Punta B = 19,05 mm, agujero 6,6 mm, acero 8000 kg/m³, en agua (1000 kg/m³):\n\n"
            "1. Masa de metal por metro ∝ 8000 × (19,05² − 6,6²) = 2,56·10⁶.\n"
            "2. Masa añadida ∝ 1000 × 19,05² = 0,36·10⁶ (14 % más).\n"
            "3. f baja × 1/√1,14 = 0,94 → unos 6 % menos.\n\n"
            "En gas a 50 bar (≈ 40 kg/m³) baja apenas un 0,3 %.",
            "Tip B = 19.05 mm, 6.6 mm bore, steel 8000 kg/m³, in water (1000 kg/m³):\n\n"
            "1. Metal mass per metre ∝ 8000 × (19.05² − 6.6²) = 2.56·10⁶.\n"
            "2. Added mass ∝ 1000 × 19.05² = 0.36·10⁶ (14 % more).\n"
            "3. f drops × 1/√1.14 = 0.94 → about 6 % less.\n\n"
            "In gas at 50 bar (≈ 40 kg/m³) it drops barely 0.3 %."),
        "mistakes": ("- Usar ratings de catálogo sin masa añadida para servicio en líquido.",
                     "- Using catalogue ratings without added mass for liquid service."),
    },
    "g.pt100": {
        "essence": (
            "Un alambre o película de platino cuya resistencia sube con la temperatura: al "
            "calentarse, los átomos de la red cristalina vibran con más amplitud y los "
            "electrones que transportan la corriente chocan más seguido con ellos. Se usa "
            "platino porque esa relación es muy estable, casi lineal, reproducible y el metal "
            "no se oxida. Vale 100 Ω a 0 °C y sube unos 0,385 Ω por °C.",
            "A platinum wire or film whose resistance rises with temperature: as it heats, "
            "the crystal lattice atoms vibrate with more amplitude and current-carrying "
            "electrons collide with them more often. Platinum is used because the "
            "relationship is very stable, nearly linear, reproducible and the metal does not "
            "oxidise. It is 100 Ω at 0 °C and rises about 0.385 Ω per °C."),
        "why": (
            "Es el sensor de referencia en procesos hasta unos 600 °C por su precisión. Su "
            "elemento es delicado: la vibración de la vaina puede fisurar la película o "
            "cortar los alambres, por eso la sujeción con resorte importa.",
            "It is the reference process sensor up to about 600 °C for its accuracy. Its "
            "element is delicate: well vibration can crack the film or break the wires, so "
            "spring loading matters."),
        "worked": (
            "A 100 °C vale 138,5 Ω. Un cable de 2 hilos con 0,5 Ω por hilo suma 1 Ω, que el "
            "instrumento lee como 1/0,385 ≈ 2,6 °C de más. Con 3 hilos el error se compensa; "
            "con 4 desaparece.",
            "At 100 °C it reads 138.5 Ω. A 2-wire cable with 0.5 Ω per conductor adds 1 Ω, "
            "which the instrument reads as 1/0.385 ≈ 2.6 °C too high. With 3 wires the error "
            "is compensated; with 4 it disappears."),
        "mistakes": (
            "- Conectar a 2 hilos en tendidos largos.\n"
            "- Usarla por encima de su rango de temperatura.",
            "- Wiring 2-wire on long runs.\n"
            "- Using it above its temperature range."),
    },
    "g.pmi": {
        "essence": (
            "Identifica la composición química de la pieza sin dañarla. El método más común "
            "es fluorescencia de rayos X (XRF): se ilumina la superficie con rayos X, los "
            "átomos se excitan y al relajarse emiten rayos X con una energía característica de "
            "cada elemento, como una huella digital. Midiendo esas energías y su intensidad "
            "se obtiene el porcentaje de cromo, níquel, molibdeno, etc. Para el carbono, que "
            "XRF no ve, se usa espectrometría de emisión óptica (chispa).",
            "It identifies the part's chemical composition without damaging it. The most "
            "common method is X-ray fluorescence (XRF): the surface is irradiated with X-rays, "
            "atoms get excited and on relaxing emit X-rays with an energy characteristic of "
            "each element, like a fingerprint. Measuring those energies and their intensity "
            "gives the percentage of chromium, nickel, molybdenum, etc. For carbon, which XRF "
            "cannot see, optical emission spectrometry (spark) is used."),
        "why": (
            "Las mezclas de material son una causa real de fallas: un 304 entregado como 316 "
            "se pica en servicio con cloruros, y un acero al carbono en lugar de un inoxidable "
            "se corroe en meses. Ambos se ven idénticos.",
            "Material mix-ups are a real failure cause: a 304 delivered as 316 pits in "
            "chloride service, and carbon steel instead of stainless corrodes in months. Both "
            "look identical."),
        "worked": (
            "316 debe mostrar ≈ 16 a 18 % Cr, 10 a 14 % Ni y 2 a 3 % Mo. Un 304 da Mo ≈ 0 %. "
            "Para 316L el carbono (≤ 0,03 %) solo se confirma con chispa.",
            "316 must show ≈ 16 to 18 % Cr, 10 to 14 % Ni and 2 to 3 % Mo. A 304 shows "
            "Mo ≈ 0 %. For 316L carbon (≤ 0.03 %) can only be confirmed by spark."),
        "mistakes": ("- Aceptar 316L solo con XRF.\n- Hacer PMI en la brida y no en el "
                     "vástago soldado.",
                     "- Accepting 316L with XRF alone.\n- Doing PMI on the flange and not on "
                     "the welded shank."),
    },
    "g.inline_resonance": {
        "essence": (
            "Además del empujón lateral, cada remolino que se desprende tira la vaina hacia "
            "atrás, en la dirección del flujo. Como los remolinos salen alternadamente de "
            "arriba y de abajo, hay dos tirones hacia atrás por cada ciclo lateral: la fuerza "
            "en línea oscila al doble, 2·f_s. Es más chica que la transversal, pero entra en "
            "resonancia antes: cuando f_s llega a la mitad de la frecuencia natural.",
            "Besides the sideways push, each shed eddy pulls the well backwards, along the "
            "flow. Since eddies leave alternately from top and bottom, there are two backward "
            "pulls per sideways cycle: in-line force oscillates at twice the frequency, 2·f_s. "
            "It is smaller than the transverse force, but resonates sooner: when f_s reaches "
            "half the natural frequency."),
        "why": (
            "Es la razón del límite 0,4: con poco amortiguamiento (Scruton bajo), la "
            "resonancia en línea puede fatigar la vaina, y muchas roturas históricas fueron "
            "por esta resonancia, no por la transversal.",
            "It is the reason for the 0.4 limit: with little damping (low Scruton), in-line "
            "resonance can fatigue the well, and many historical failures were due to this "
            "resonance, not the transverse one."),
        "worked": (
            "f_n,c = 420 Hz → resonancia en línea a f_s = 210 Hz. Con B = 15,9 mm y N_S = 0,22 "
            "eso es V = 210 × 0,0159 / 0,22 = 15 m/s: un gas a 20 m/s ya pasó por ella.",
            "f_n,c = 420 Hz → in-line resonance at f_s = 210 Hz. With B = 15.9 mm and "
            "N_S = 0.22 that is V = 210 × 0.0159 / 0.22 = 15 m/s: a gas at 20 m/s has already "
            "passed through it."),
        "mistakes": ("- Creer que basta con estar debajo de la resonancia transversal.",
                     "- Believing it is enough to be below transverse resonance."),
    },
    "g.stress_concentration": {
        "essence": (
            "Las líneas de fuerza dentro de una pieza cargada se comportan como el agua en un "
            "río: en una sección uniforme van parejas, pero en un cambio brusco (una esquina, "
            "el fondo de una rosca, una marca) tienen que rodear el obstáculo y se amontonan. "
            "Ahí el esfuerzo local es K_t veces el nominal. Cuanto más aguda la entalla (radio "
            "pequeño frente al tamaño de la pieza), mayor K_t.",
            "Lines of force in a loaded part behave like water in a river: in a uniform "
            "section they run evenly, but at an abrupt change (a corner, a thread root, a "
            "mark) they must go around the obstacle and crowd together. There local stress is "
            "K_t times nominal. The sharper the notch (small radius relative to part size), "
            "the higher K_t."),
        "why": (
            "La fatiga empieza siempre en el punto de mayor esfuerzo local. Por eso las vainas "
            "roscadas, con el fondo de rosca justo en la raíz, aguantan mucho menos vibración "
            "que las bridadas con radio generoso.",
            "Fatigue always starts at the point of highest local stress. That is why threaded "
            "wells, with the thread root right at the fixed end, withstand much less "
            "vibration than flanged ones with a generous radius."),
        "worked": (
            "Esfuerzo nominal 10 MPa, límite de fatiga 21 MPa:\n\n"
            "- Radio de 3,2 mm, K_t ≈ 1,2: 12 MPa → cumple.\n"
            "- Rosca NPT, K_t ≈ 2,3: 23 MPa → no cumple.",
            "Nominal stress 10 MPa, fatigue limit 21 MPa:\n\n"
            "- 3.2 mm radius, K_t ≈ 1.2: 12 MPa → passes.\n"
            "- NPT thread, K_t ≈ 2.3: 23 MPa → fails."),
        "mistakes": ("- Punzonar o grabar marcas cerca de la raíz.",
                     "- Stamping or engraving marks near the root."),
    },
    "g.thermocouple": {
        "essence": (
            "En un metal, los electrones libres se mueven más en la zona caliente y tienden a "
            "difundirse hacia la fría, generando un pequeño voltaje a lo largo del alambre "
            "(efecto Seebeck). Cada metal lo hace en distinta medida. Si se unen dos metales "
            "distintos en un extremo (la junta caliente) y se mide entre los otros dos (la "
            "junta fría), el voltaje neto depende de la diferencia de temperatura entre ambas "
            "juntas.\n\n"
            "Por eso el instrumento necesita medir la temperatura de la junta fría "
            "(compensación) y por eso el cable de extensión debe ser del mismo par de "
            "metales.",
            "In a metal, free electrons move more in the hot zone and tend to diffuse towards "
            "the cold one, producing a small voltage along the wire (Seebeck effect). Each "
            "metal does it to a different degree. If two dissimilar metals are joined at one "
            "end (hot junction) and measured across the other two (cold junction), the net "
            "voltage depends on the temperature difference between the junctions.\n\n"
            "That is why the instrument must measure cold-junction temperature "
            "(compensation) and why extension cable must be the same metal pair."),
        "why": (
            "Cubre temperaturas que una Pt100 no alcanza y es robusto frente a la vibración, "
            "pero es menos preciso y su señal (milivoltios) es sensible al ruido.",
            "It covers temperatures a Pt100 cannot reach and is rugged against vibration, but "
            "it is less accurate and its signal (millivolts) is noise-sensitive."),
        "worked": (
            "Tipo K a 500 °C con junta fría a 0 °C: ≈ 20,6 mV, unos 41 µV por °C. Si se usa "
            "cable de cobre en un tramo con 30 °C de diferencia, el error es del orden de "
            "30 °C.",
            "Type K at 500 °C with cold junction at 0 °C: ≈ 20.6 mV, about 41 µV per °C. If "
            "copper wire is used on a stretch with a 30 °C difference, the error is of the "
            "order of 30 °C."),
        "mistakes": ("- Empalmar con cable de cobre.\n- Mezclar tipos de termopar y cable.",
                     "- Splicing with copper wire.\n- Mixing thermocouple and cable types."),
    },
    "g.standard_flow": {
        "essence": (
            "Un gas se comprime: la misma masa ocupa mucho menos volumen a alta presión. Para "
            "poder comparar caudales, se expresa el volumen que ocuparía en condiciones de "
            "referencia (por ejemplo 15 °C y 1,01325 bar para Sm³, 0 °C para Nm³, 60 °F y "
            "14,696 psia para SCF). Es en realidad una medida de masa disfrazada de volumen.\n\n"
            "Para la vaina importa el caudal real a la presión y temperatura de la línea, que "
            "es el que da la velocidad. TS convierte usando la densidad real y la de "
            "referencia.",
            "Gas compresses: the same mass occupies much less volume at high pressure. To "
            "compare flows, the volume it would occupy at reference conditions is given (for "
            "example 15 °C and 1.01325 bar for Sm³, 0 °C for Nm³, 60 °F and 14.696 psia for "
            "SCF). It is really a mass measure disguised as volume.\n\n"
            "For the well what matters is actual flow at line pressure and temperature, which "
            "gives velocity. TS converts using actual and reference density."),
        "why": (
            "Confundir caudal estándar con real es uno de los errores más grandes posibles: "
            "puede dar velocidades 50 o 100 veces mayores que las reales.",
            "Confusing standard with actual flow is one of the largest possible errors: it "
            "can give velocities 50 or 100 times higher than real."),
        "worked": (
            "1 MMSCFD ≈ 28 317 Sm³/día ≈ 1180 Sm³/h. A 50 bar y 30 °C, con Z ≈ 0,9, el "
            "volumen real es ≈ 1180 × (1,013/50) × (303/288) × 0,9 ≈ 23 m³/h. Si se cargan "
            "1180 m³/h como reales, la velocidad sale 51 veces mayor.",
            "1 MMSCFD ≈ 28,317 Sm³/day ≈ 1180 Sm³/h. At 50 bar and 30 °C, with Z ≈ 0.9, "
            "actual volume is ≈ 1180 × (1.013/50) × (303/288) × 0.9 ≈ 23 m³/h. If 1180 m³/h is "
            "entered as actual, velocity comes out 51 times too high."),
        "mistakes": ("- Mezclar Nm³ y Sm³ (difieren ≈ 5 %).\n- Cargar Sm³/h como m³/h reales.",
                     "- Mixing Nm³ and Sm³ (≈ 5 % apart).\n- Entering Sm³/h as actual m³/h."),
    },
    "g.velocity_collar": {
        "essence": (
            "Un collar es un anillo mecanizado en el vástago, cerca de la raíz, con un diámetro "
            "apenas menor que el interior del niple. Al montar, el collar queda dentro del "
            "niple; si ajusta bien, la vaina se apoya en él y el largo que vibra se acorta. "
            "Como f ∝ 1/L², acortar el largo libre sube mucho la frecuencia.\n\n"
            "El problema es que el apoyo depende de un ajuste fino entre dos piezas hechas por "
            "distintos fabricantes, con tolerancias, dilatación y desgaste.",
            "A collar is a ring machined on the shank, near the root, with a diameter just "
            "below the nozzle bore. When installed the collar sits inside the nozzle; if it "
            "fits well, the well bears on it and the vibrating length shortens. Since "
            "f ∝ 1/L², shortening free length raises frequency a lot.\n\n"
            "The problem is that support depends on a fine fit between two parts made by "
            "different manufacturers, with tolerances, expansion and wear."),
        "why": (
            "La norma actual no le da crédito: si el ajuste es flojo, el collar no apoya y la "
            "vaina vibra como si no lo tuviera; si golpea, puede generar desgaste y "
            "fisuras. Se prefiere rediseñar la vaina para que cumpla sin collar.",
            "The current standard gives it no credit: if the fit is loose the collar does not "
            "support and the well vibrates as if it had none; if it hammers it can cause wear "
            "and cracks. Redesigning the well to pass without a collar is preferred."),
        "worked": (
            "L = 300 mm, collar a 100 mm de la brida → largo libre 200 mm: f × (300/200)² = "
            "2,25 solo si el ajuste es perfecto. Con 0,5 mm de juego, el beneficio puede ser "
            "nulo.",
            "L = 300 mm, collar 100 mm from the flange → free length 200 mm: f × "
            "(300/200)² = 2.25 only with a perfect fit. With 0.5 mm clearance the benefit may "
            "be nil."),
        "mistakes": ("- Contar con el collar en el cálculo de aceptación.",
                     "- Counting on the collar in the acceptance calculation."),
    },
    "g.fatigue_limit": {
        "essence": (
            "Bajo cargas que van y vienen, un metal puede romperse con esfuerzos muy "
            "inferiores a su resistencia. El mecanismo: en cada ciclo, en los granos mejor "
            "orientados, planos de átomos se deslizan un poco hacia un lado y vuelven; ese "
            "ir y venir forma escalones microscópicos en la superficie donde nace una fisura, "
            "que luego avanza una fracción de micrómetro por ciclo.\n\n"
            "Por debajo de cierta amplitud, el deslizamiento no alcanza a formar fisuras: es "
            "el límite de fatiga. Los aceros lo muestran claramente cerca de 10⁷ ciclos.",
            "Under loads that go back and forth, metal can break at stresses far below its "
            "strength. The mechanism: each cycle, in the best-oriented grains, planes of atoms "
            "slip slightly one way and back; that back-and-forth forms microscopic steps on "
            "the surface where a crack starts, which then advances a fraction of a micrometre "
            "per cycle.\n\n"
            "Below a certain amplitude, slip cannot form cracks: that is the fatigue limit. "
            "Steels show it clearly around 10⁷ cycles."),
        "why": (
            "Una vaina a 300 Hz acumula 10⁷ ciclos en 9 horas: toda su vida transcurre en la "
            "zona de vida infinita. El límite de fatiga, no la resistencia, decide.",
            "A well at 300 Hz accumulates 10⁷ cycles in 9 hours: its whole life is in the "
            "infinite-life region. The fatigue limit, not strength, decides."),
        "worked": (
            "316 mecanizado ≈ 48 MPa; soldado ≈ 21 MPa (la soldadura agrega defectos y "
            "tensiones residuales). En agua de mar, con F_E = 0,5, el soldado queda en ≈ 10 MPa.",
            "Machined 316 ≈ 48 MPa; welded ≈ 21 MPa (welding adds defects and residual "
            "stresses). In seawater, with F_E = 0.5, the welded one drops to ≈ 10 MPa."),
        "mistakes": ("- Esperar que un acero más resistente tenga mucho más límite de fatiga.",
                     "- Expecting a stronger steel to have a much higher fatigue limit."),
    },
    "g.time_constant": {
        "essence": (
            "La temperatura del sensor no salta cuando cambia la del fluido: el calor tiene "
            "que pasar del fluido a la superficie de la vaina (convección), atravesar el metal "
            "(conducción), cruzar el huelgo de aire y calentar la masa del sensor. Cada paso "
            "es una resistencia, y cada masa es una capacidad que hay que llenar, como un "
            "tanque que se llena a través de una cañería angosta.\n\n"
            "La respuesta resultante se acerca exponencialmente al valor final. τ es el tiempo "
            "en recorrer el 63,2 % del salto; a 3τ se llega al 95 % y a 5τ al 99 %.",
            "Sensor temperature does not jump when fluid temperature changes: heat must pass "
            "from the fluid to the well surface (convection), cross the metal (conduction), "
            "cross the air gap and warm the sensor mass. Each step is a resistance, and each "
            "mass a capacity to fill, like a tank filling through a narrow pipe.\n\n"
            "The resulting response approaches the final value exponentially. τ is the time "
            "to cover 63.2 % of the step; at 3τ it reaches 95 % and at 5τ 99 %."),
        "why": (
            "Un lazo de control con una medición lenta oscila o reacciona tarde, y una alarma "
            "de alta temperatura llega tarde. La vaina suele ser la mayor parte del retraso.",
            "A control loop with a slow reading oscillates or reacts late, and a high "
            "temperature alarm arrives late. The well is usually most of the lag."),
        "worked": (
            "τ = 20 s en agua: tras un salto de 50 a 80 °C, a los 20 s marca 69 °C y a los "
            "60 s 78,5 °C. En gas lento la misma vaina puede tener τ = 120 s, porque la "
            "convección en gas transfiere mucho menos calor.",
            "τ = 20 s in water: after a step from 50 to 80 °C it reads 69 °C at 20 s and "
            "78.5 °C at 60 s. In slow gas the same well may have τ = 120 s, because gas "
            "convection transfers far less heat."),
        "mistakes": ("- Dar τ del sensor desnudo como τ del conjunto.",
                     "- Quoting bare-sensor τ as the assembly τ."),
    },
}
