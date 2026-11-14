"""Segunda pasada: normas, tipos de conexión y perfiles."""

from __future__ import annotations

from typing import Any

DEEP: dict[str, dict[str, Any]] = {
    "std.iec60584": {
        "essence": (
            "Define, para cada tipo de termopar (K, J, N, T, E, R, S, B), la relación entre "
            "temperatura y voltaje como tablas y polinomios de referencia, y las clases de "
            "tolerancia. Así un termopar tipo K de cualquier fabricante da el mismo voltaje "
            "a la misma temperatura, dentro de su clase.\n\n"
            "Cada tipo es un par de aleaciones elegido por un compromiso distinto: K "
            "(níquel-cromo / níquel-aluminio) es el todoterreno hasta ≈ 1200 °C; N mejora la "
            "estabilidad a alta temperatura; J (hierro / constantán) se oxida pero es barato; "
            "R, S y B (platino-rodio) llegan a 1600 a 1800 °C con mayor costo.",
            "It defines, for each thermocouple type (K, J, N, T, E, R, S, B), the "
            "temperature-voltage relationship as reference tables and polynomials, and "
            "tolerance classes. That way a type K thermocouple from any manufacturer gives the "
            "same voltage at the same temperature, within its class.\n\n"
            "Each type is an alloy pair chosen for a different compromise: K "
            "(nickel-chromium / nickel-aluminium) is the all-rounder up to ≈ 1200 °C; N "
            "improves high-temperature stability; J (iron / constantan) oxidises but is cheap; "
            "R, S and B (platinum-rhodium) reach 1600 to 1800 °C at higher cost."),
        "why": (
            "Es la referencia para especificar tipo y clase en la hoja de datos y para saber "
            "qué error esperar del sensor, que se suma al error por inmersión y retraso de la "
            "vaina.",
            "It is the reference to specify type and class on the datasheet and to know what "
            "error to expect from the sensor, which adds to the well's immersion and lag "
            "error."),
        "worked": (
            "Tipo K clase 1: ±1,5 °C o ±0,004·|t|, el mayor. A 800 °C: ±3,2 °C. Clase 2 a "
            "800 °C: ±6 °C. Para un horno con control a ±5 °C, la clase 2 ya consume todo el "
            "margen.",
            "Type K class 1: ±1.5 °C or ±0.004·|t|, whichever is greater. At 800 °C: "
            "±3.2 °C. Class 2 at 800 °C: ±6 °C. For a furnace controlled to ±5 °C, class 2 "
            "already uses the whole margin."),
        "mistakes": (
            "- Especificar «termopar» sin tipo ni clase.\n"
            "- Usar un tipo K entre 250 y 600 °C con ciclos largos sin considerar su deriva "
            "(orden de corto alcance).",
            "- Specifying «thermocouple» without type or class.\n"
            "- Using type K between 250 and 600 °C for long periods without considering its "
            "drift (short-range ordering)."),
    },
    "std.iec60751": {
        "essence": (
            "Define la curva resistencia-temperatura del platino industrial (la ecuación de "
            "Callendar-Van Dusen con sus coeficientes) y las clases de tolerancia AA, A, B y "
            "C. Gracias a ella, una Pt100 de cualquier marca vale 100 Ω a 0 °C y 138,51 Ω a "
            "100 °C, dentro de su clase, y los transmisores pueden convertir sin calibración "
            "individual.",
            "It defines the resistance-temperature curve of industrial platinum (the "
            "Callendar-Van Dusen equation with its coefficients) and tolerance classes AA, A, "
            "B and C. Thanks to it, a Pt100 of any brand is 100 Ω at 0 °C and 138.51 Ω at "
            "100 °C, within its class, and transmitters can convert without individual "
            "calibration."),
        "why": (
            "Permite especificar la precisión del sensor en la hoja de datos. En custodia o "
            "balance de masa, la diferencia entre clase A y B puede ser significativa.",
            "It lets you specify sensor accuracy on the datasheet. In custody transfer or "
            "mass balance, the difference between class A and B can be significant."),
        "worked": (
            "Clase A: ±(0,15 + 0,002·|t|) °C → a 100 °C, ±0,35 °C. Clase B: ±(0,3 + 0,005·|t|) "
            "→ a 100 °C, ±0,8 °C. En un tanque de 10 000 m³ de crudo, 0,45 °C de diferencia "
            "son unos 4 m³ de volumen corregido.",
            "Class A: ±(0.15 + 0.002·|t|) °C → at 100 °C, ±0.35 °C. Class B: ±(0.3 + "
            "0.005·|t|) → at 100 °C, ±0.8 °C. In a 10,000 m³ crude tank, a 0.45 °C difference "
            "is about 4 m³ of corrected volume."),
        "mistakes": ("- Pedir clase A y conectar a 2 hilos.",
                     "- Ordering class A and wiring 2-wire."),
    },
    "std.isatr20": {
        "essence": (
            "Es un informe técnico de ISA que propone hojas de datos normalizadas para "
            "especificar instrumentos, incluidos termómetros, sensores y termovainas. No "
            "calcula nada: organiza qué datos hay que dar (proceso, material, conexión, "
            "dimensiones, ensayos) para que el comprador y el fabricante hablen el mismo "
            "idioma.",
            "It is an ISA technical report proposing standardised datasheets to specify "
            "instruments, including thermometers, sensors and thermowells. It calculates "
            "nothing: it organises which data must be given (process, material, connection, "
            "dimensions, tests) so buyer and manufacturer speak the same language."),
        "why": (
            "La hoja de datos de TS sigue esa organización, así que se puede adjuntar a una "
            "requisición sin rehacerla.",
            "The TS datasheet follows that organisation, so it can be attached to a "
            "requisition without redoing it."),
        "worked": (
            "Campos típicos: tag, servicio, presión y temperatura de operación y diseño, "
            "material, conexión, U, agujero, ensayos (PMI, hidrostática, dimensional) y "
            "referencia al cálculo de vibración.",
            "Typical fields: tag, service, operating and design pressure and temperature, "
            "material, connection, U, bore, tests (PMI, hydrostatic, dimensional) and a "
            "reference to the vibration calculation."),
        "mistakes": ("- Enviar la hoja sin el cálculo de vibración adjunto.",
                     "- Sending the sheet without the vibration calculation attached."),
    },
    "std.din43772": {
        "essence": (
            "Norma alemana que define formas normalizadas de vainas de protección (por "
            "ejemplo, la forma 2 y 3 roscadas, la forma 4 cónica mecanizada de barra, para "
            "soldar o roscar) con sus diámetros, largos y conexiones típicas. Es el "
            "equivalente europeo de las tablas dimensionales de ASME B40.\n\n"
            "Define dimensiones, no la verificación de vibración: una forma DIN también debe "
            "calcularse con la norma de termovainas.",
            "German standard defining standard protective well forms (for example forms 2 "
            "and 3 threaded, form 4 tapered machined from bar, for welding or threading) with "
            "their diameters, lengths and typical connections. It is the European equivalent "
            "of the ASME B40 dimensional tables.\n\n"
            "It defines dimensions, not the vibration check: a DIN form must also be "
            "calculated with the thermowell standard."),
        "why": ("En equipos europeos las cuplas y repuestos siguen DIN; pedir una vaina ASME "
                "puede no encajar.",
                "In European equipment couplings and spares follow DIN; ordering an ASME "
                "well may not fit."),
        "worked": (
            "Forma 4 con rosca G 1, punta 12,5 mm, U 140 mm. Si se reemplaza por una vaina "
            "ASME 1\" NPT, la rosca no entra en la cupla G.",
            "Form 4 with G 1 thread, 12.5 mm tip, U 140 mm. If replaced by an ASME 1\" NPT "
            "well, the thread does not enter the G coupling."),
        "mistakes": ("- Asumir que una forma DIN está verificada a vibración.",
                     "- Assuming a DIN form is vibration-checked."),
    },
    "std.b40": {
        "essence": (
            "Norma de termómetros bimetálicos y de las termovainas que los alojan: tipos de "
            "conexión, largos U normalizados, diámetros de agujero y la forma de designar una "
            "vaina. Por eso los largos U «raros» en pulgadas (2½\", 4½\", 7½\"…) aparecen en "
            "todos los catálogos: vienen de acá, más un margen para la rosca del cabezal.",
            "Standard for bimetallic thermometers and the thermowells housing them: "
            "connection types, standard U lengths, bore diameters and how to designate a "
            "well. That is why the «odd» U lengths in inches (2½\", 4½\", 7½\"…) appear in "
            "every catalogue: they come from here, plus an allowance for the head thread."),
        "why": (
            "TS usa estos largos como primera opción porque son los que el mercado fabrica "
            "en serie: más baratos y con mejores plazos.",
            "TS uses these lengths as first choice because they are what the market "
            "manufactures in series: cheaper and with better lead times."),
        "worked": (
            "Largos U típicos: 2½\", 4½\", 7½\", 10½\", 13½\", 16½\", 22½\". Si el cálculo pide "
            "210 mm, la opción comercial es 7½\" (190,5 mm) si alcanza la inmersión, o un "
            "largo especial.",
            "Typical U lengths: 2½\", 4½\", 7½\", 10½\", 13½\", 16½\", 22½\". If the calculation "
            "asks for 210 mm, the commercial option is 7½\" (190.5 mm) if immersion is "
            "enough, or a special length."),
        "mistakes": ("- Tomar sus dimensiones como aprobación de vibración.",
                     "- Taking its dimensions as vibration approval."),
    },
    "std.b165": {
        "essence": (
            "Norma de bridas y accesorios bridados de cañería de NPS ½ a 24: dimensiones "
            "(diámetros, cantidad y tamaño de bulones, caras), clases de presión y, sobre "
            "todo, las tablas de presión-temperatura por grupo de material. Esas tablas "
            "reflejan que el metal pierde resistencia al calentarse: la presión admisible de "
            "una misma brida baja con la temperatura.",
            "Standard for pipe flanges and flanged fittings NPS ½ to 24: dimensions "
            "(diameters, number and size of bolts, faces), pressure classes and, above all, "
            "pressure-temperature tables by material group. Those tables reflect that metal "
            "loses strength when heated: the same flange's allowable pressure falls with "
            "temperature."),
        "why": (
            "Gobierna la verificación de rating de la brida de la vaina y garantiza que se "
            "pueda abulonar a la brida de la línea.",
            "It governs the well flange rating check and guarantees it can be bolted to the "
            "line flange."),
        "worked": (
            "316 (grupo 2.2) clase 300: ≈ 49,6 bar a 38 °C y ≈ 37 bar a 300 °C, un 25 % menos. "
            "Acero al carbono (1.1) clase 300 a 300 °C: ≈ 39,8 bar.",
            "316 (group 2.2) class 300: ≈ 49.6 bar at 38 °C and ≈ 37 bar at 300 °C, 25 % "
            "less. Carbon steel (1.1) class 300 at 300 °C: ≈ 39.8 bar."),
        "mistakes": ("- Leer la clase como la presión en psi.",
                     "- Reading the class as the pressure in psi."),
    },
    "conn.weld_in": {
        "essence": (
            "La vaina se suelda directamente a la cañería o a un accesorio (sockolet, "
            "weldolet) con soldadura de penetración. No hay junta ni rosca: el metal de la "
            "vaina y el de la línea quedan unidos de forma continua. Es la frontera de "
            "presión más confiable, pero la vaina ya no se puede sacar sin cortar.",
            "The well is welded directly to the pipe or a fitting (sockolet, weldolet) with "
            "a penetration weld. There is no gasket or thread: well and line metal are "
            "joined continuously. It is the most reliable pressure boundary, but the well can "
            "no longer be removed without cutting."),
        "why": (
            "Se usa en alta presión y alta temperatura, servicios letales o donde una fuga de "
            "junta no se tolera (vapor de alta, hidrógeno). Para la mecánica, la raíz soldada "
            "tiene menor límite de fatiga que una mecanizada.",
            "It is used at high pressure and temperature, lethal services or where a gasket "
            "leak is not tolerated (high-pressure steam, hydrogen). Mechanically, the welded "
            "root has a lower fatigue limit than a machined one."),
        "worked": (
            "Vapor a 100 bar y 540 °C, material F22: vaina soldada a un weldolet. Requiere "
            "precalentamiento, tratamiento térmico posterior y radiografía o ultrasonido de "
            "la soldadura, y la vaina se verifica con el estado «soldado».",
            "Steam at 100 bar and 540 °C, F22 material: well welded to a weldolet. It needs "
            "preheat, post-weld heat treatment and radiography or ultrasound of the weld, and "
            "the well is checked in the «welded» state."),
        "mistakes": (
            "- Soldar materiales distintos sin procedimiento calificado.\n"
            "- Declararla «no soldada» en el cálculo.",
            "- Welding dissimilar materials without a qualified procedure.\n"
            "- Declaring it «not welded» in the calculation."),
    },
    "conn.sanitary": {
        "essence": (
            "Conexión tipo clamp (tri-clamp): dos férulas con ranura se enfrentan con una "
            "junta elastomérica en el medio y se aprietan con una abrazadera. Las superficies "
            "en contacto con el producto son pulidas (rugosidad baja, por ejemplo "
            "Ra ≤ 0,8 µm) y sin rendijas, porque en una rendija las bacterias encuentran "
            "refugio y la limpieza en sitio (CIP) no llega.",
            "Clamp connection (tri-clamp): two grooved ferrules face each other with an "
            "elastomer gasket between them and are tightened with a clamp. Product-contact "
            "surfaces are polished (low roughness, for example Ra ≤ 0.8 µm) and crevice-free, "
            "because bacteria find shelter in a crevice and clean-in-place (CIP) cannot reach "
            "it."),
        "why": (
            "Es el estándar en alimentos, bebidas y farmacia. Se desarma rápido, pero la "
            "junta limita la presión y la temperatura (típicamente decenas de bar y unos "
            "150 °C).",
            "It is the standard in food, beverage and pharma. It disassembles quickly, but "
            "the gasket limits pressure and temperature (typically tens of bar and about "
            "150 °C)."),
        "worked": (
            "Leche a 4 bar y 85 °C, CIP con soda caliente: vaina 316L, clamp 1½\", junta "
            "EPDM, Ra ≤ 0,8 µm. En vapor de esterilización a 135 °C hace falta una junta de "
            "silicona o PTFE.",
            "Milk at 4 bar and 85 °C, CIP with hot caustic: 316L well, 1½\" clamp, EPDM "
            "gasket, Ra ≤ 0.8 µm. In sterilisation steam at 135 °C a silicone or PTFE gasket "
            "is needed."),
        "mistakes": ("- Usarla en servicios de hidrocarburos o alta presión.",
                     "- Using it in hydrocarbon or high-pressure services."),
    },
    "conn.flanged": {
        "essence": (
            "La vaina se mecaniza de barra y se suelda (o se mecaniza en una pieza) a una "
            "brida que se abulona a la brida del niple de la línea, con una junta entre "
            "ambas. Separa la frontera de presión en dos partes desmontables: la vaina se "
            "puede retirar para inspección o reemplazo sin cortar la cañería.\n\n"
            "Mecánicamente, la brida da un empotramiento rígido y permite raíces gruesas.",
            "The well is machined from bar and welded (or machined in one piece) to a flange "
            "bolted to the line nozzle flange, with a gasket between them. It splits the "
            "pressure boundary into two removable parts: the well can be taken out for "
            "inspection or replacement without cutting the pipe.\n\n"
            "Mechanically, the flange gives a stiff fixed end and allows thick roots."),
        "why": (
            "Es la opción estándar en refinerías y petroquímica. Hay que verificar el rating "
            "de la brida y el estado del metal en la raíz (soldada o mecanizada de una pieza).",
            "It is the standard option in refineries and petrochemicals. Flange rating and "
            "metal state at the root (welded or one-piece machined) must be checked."),
        "worked": (
            "Brida 1½\" clase 300 RF, cónica, 316, U 250 mm. Si la brida está soldada al "
            "vástago, el límite de fatiga baja a ≈ 21 MPa; si es una pieza mecanizada, "
            "≈ 48 MPa.",
            "1½\" class 300 RF flange, tapered, 316, U 250 mm. If the flange is welded to "
            "the shank, the fatigue limit drops to ≈ 21 MPa; if one-piece machined, "
            "≈ 48 MPa."),
        "mistakes": ("- Elegir una clase menor que la de la línea.",
                     "- Choosing a lower class than the line."),
    },
    "conn.socket_weld": {
        "essence": (
            "El extremo de la vaina entra en un encaje (socket) de la cañería o de un "
            "sockolet y se suelda con un cordón de filete exterior. Queda un pequeño espacio "
            "entre el fondo del encaje y la vaina (se dejan unos 1,5 mm para que la "
            "dilatación no fisure el cordón), y ese espacio es una rendija donde puede haber "
            "corrosión.",
            "The well end enters a socket in the pipe or a sockolet and is welded with an "
            "external fillet weld. A small gap remains between the socket bottom and the well "
            "(about 1.5 mm is left so expansion does not crack the weld), and that gap is a "
            "crevice where corrosion can occur."),
        "why": (
            "Es común en líneas chicas de vapor y servicios de alta presión. La soldadura de "
            "filete tiene una concentración de esfuerzos alta: no es la mejor raíz para "
            "vibración.",
            "It is common on small steam lines and high-pressure services. The fillet weld "
            "has a high stress concentration: it is not the best root for vibration."),
        "worked": (
            "Línea de 1\" de vapor a 40 bar: socket weld habitual. Sin el espacio de 1,5 mm, "
            "la dilatación puede fisurar el cordón en los primeros arranques.",
            "1\" steam line at 40 bar: socket weld is usual. Without the 1.5 mm gap, "
            "expansion can crack the weld in the first start-ups."),
        "mistakes": ("- Usarla en servicios con corrosión en rendijas.",
                     "- Using it in crevice-corrosion services."),
    },
    "conn.van_stone": {
        "essence": (
            "La vaina tiene un collar solapado (lap) en una sola pieza con el vástago, y una "
            "brida loca la aprieta contra la brida de la línea. Solo la vaina toca el fluido; "
            "la brida loca queda afuera y puede ser de un material más barato. Además la brida "
            "gira libre, lo que facilita alinear los agujeros de los bulones.",
            "The well has a lapped collar in one piece with the shank, and a loose flange "
            "presses it against the line flange. Only the well touches the fluid; the loose "
            "flange stays outside and can be a cheaper material. The flange also rotates "
            "freely, making bolt-hole alignment easy."),
        "why": (
            "Es la solución para materiales caros (tantalio, Hastelloy, titanio): se usa el "
            "material noble solo donde hace falta, y la vaina de una pieza no tiene "
            "soldaduras en la raíz.",
            "It is the solution for expensive materials (tantalum, Hastelloy, titanium): the "
            "noble material is used only where needed, and the one-piece well has no welds at "
            "the root."),
        "worked": (
            "Ácido clorhídrico: vaina de Hastelloy C-276 con brida loca de acero al carbono "
            "clase 150. Una brida maciza de Hastelloy costaría varias veces más.",
            "Hydrochloric acid: Hastelloy C-276 well with a class 150 carbon steel loose "
            "flange. A solid Hastelloy flange would cost several times more."),
        "mistakes": ("- Verificar el rating con el material de la vaina y no con el de la "
                     "brida loca.",
                     "- Checking rating with the well material instead of the loose flange "
                     "material."),
    },
    "conn.threaded": {
        "essence": (
            "La vaina tiene una rosca macho que se enrosca en una cupla o un thredolet de la "
            "línea. Es barata y simple, pero mecánicamente es la conexión más débil frente a "
            "la vibración: el fondo de cada filete es una entalla que concentra esfuerzos, y "
            "está justo en la raíz, donde el momento es máximo. Además la rosca no es un "
            "empotramiento perfecto, lo que baja la frecuencia instalada.",
            "The well has a male thread screwed into a coupling or thredolet on the line. It "
            "is cheap and simple, but mechanically the weakest connection against vibration: "
            "each thread root is a notch concentrating stress, and it sits right at the fixed "
            "end, where moment is maximum. The thread is also not a perfect fixed end, which "
            "lowers installed frequency."),
        "why": (
            "Sirve para servicios de baja velocidad, utilidades y líneas chicas. En gas rápido "
            "o con H₂S suele quedar fuera.",
            "It suits low-velocity services, utilities and small lines. In fast gas or with "
            "H₂S it usually falls out."),
        "worked": (
            "1\" NPT en agua a 3 m/s: cumple con margen. La misma vaina en gas a 20 m/s: K_t "
            "≈ 2,3 en la rosca y menor rigidez del apoyo la dejan fuera. Pasar a bridada "
            "1½\" la resuelve.",
            "1\" NPT in water at 3 m/s: passes with margin. The same well in gas at 20 m/s: "
            "K_t ≈ 2.3 at the thread and lower support stiffness take it out. Switching to a "
            "1½\" flanged well solves it."),
        "mistakes": ("- Sellar con soldadura una rosca sin procedimiento (seal weld).",
                     "- Seal-welding a thread without a procedure."),
    },
    "profile.straight": {
        "essence": (
            "Vástago de diámetro constante, A = B. Es la forma más simple de mecanizar, pero "
            "no aprovecha el material: el momento flector es máximo en la raíz y nulo en la "
            "punta, y sin embargo el recto tiene el mismo diámetro en ambos lados. Hay mucho "
            "metal en la punta, donde agrega masa sin aportar resistencia, y poco en la raíz, "
            "donde haría falta.",
            "Shank of constant diameter, A = B. It is the simplest to machine, but does not "
            "use material well: bending moment is maximum at the root and zero at the tip, yet "
            "the straight well has the same diameter on both. There is a lot of metal at the "
            "tip, adding mass without strength, and little at the root, where it would be "
            "needed."),
        "why": (
            "Es la opción barata para servicios suaves (agua lenta, utilidades). En flujos "
            "rápidos suele quedar corto frente al cónico.",
            "It is the cheap option for mild services (slow water, utilities). In fast flows "
            "it usually falls short of the tapered profile."),
        "worked": (
            "A = B = 19 mm, U 150 mm en agua a 1 m/s: cumple con amplio margen. Con U 250 mm "
            "en gas a 25 m/s, un cónico 26,7 → 19 mm da unos 40 % más de frecuencia.",
            "A = B = 19 mm, U 150 mm in water at 1 m/s: passes with ample margin. With "
            "U 250 mm in gas at 25 m/s, a tapered 26.7 → 19 mm gives about 40 % more "
            "frequency."),
        "mistakes": ("- Usarlo por costumbre en gas rápido.",
                     "- Using it out of habit in fast gas."),
    },
    "profile.tapered": {
        "essence": (
            "El diámetro baja linealmente de A en la raíz a B en la punta. Sigue la forma del "
            "momento flector: mucho metal donde la carga es mayor y poco donde casi no hay "
            "momento. Así sube la rigidez donde importa y baja la masa donde más pesa en la "
            "frecuencia natural (en el extremo). Es la forma que una viga «elegiría» si "
            "pudiera optimizarse sola.",
            "Diameter falls linearly from A at the root to B at the tip. It follows the "
            "bending moment: lots of metal where load is highest and little where there is "
            "almost no moment. Stiffness rises where it matters and mass drops where it "
            "weighs most on natural frequency (at the end). It is the shape a beam would "
            "«choose» if it could optimise itself."),
        "why": (
            "Es el perfil más usado en refinería: mejor relación entre frecuencia, esfuerzo y "
            "respuesta térmica, sin escalones que concentren esfuerzos.",
            "It is the most used refinery profile: best balance between frequency, stress and "
            "thermal response, with no steps concentrating stress."),
        "worked": (
            "A 26,7, B 19,05, U 250 mm: f_n ≈ 460 Hz, contra unos 330 Hz de un recto de "
            "19,05 mm con el mismo largo: un 40 % más, con la misma punta y la misma estela.",
            "A 26.7, B 19.05, U 250 mm: f_n ≈ 460 Hz, against about 330 Hz for a 19.05 mm "
            "straight well of the same length: 40 % more, with the same tip and wake."),
        "mistakes": ("- Pedir una conicidad mayor que la que admite la norma.",
                     "- Asking for more taper than the standard allows."),
    },
    "profile.stepped": {
        "essence": (
            "Dos tramos rectos: uno grueso (A) desde la raíz y uno fino (B) en la punta, "
            "unidos por un escalón con radio. La punta fina responde rápido y suelta la estela "
            "a mayor frecuencia; la raíz gruesa da rigidez. Es un compromiso entre el recto y "
            "el cónico, y es típico de vainas para sensores de respuesta rápida.",
            "Two straight sections: a thick one (A) from the root and a thin one (B) at the "
            "tip, joined by a step with a radius. The thin tip responds fast and sheds the "
            "wake at higher frequency; the thick root gives stiffness. It is a compromise "
            "between straight and tapered, typical of wells for fast-response sensors."),
        "why": (
            "El escalón es un segundo punto crítico de fatiga y la punta fina recibe flujo "
            "con poca rigidez: hay que verificar ambas zonas.",
            "The step is a second fatigue-critical point and the thin tip takes flow with "
            "little stiffness: both zones must be checked."),
        "worked": (
            "A 22,2, B 12,7, Ls 64 mm: la punta de 12,7 mm da una constante de tiempo cerca de "
            "la mitad que una de 19 mm, pero su f_s es un 50 % mayor a la misma velocidad.",
            "A 22.2, B 12.7, Ls 64 mm: the 12.7 mm tip gives a time constant near half that "
            "of a 19 mm tip, but its f_s is 50 % higher at the same velocity."),
        "mistakes": ("- No acotar el radio del escalón.",
                     "- Not dimensioning the step radius."),
    },
}
