"""Profundidad de las fichas de tubería e instalación."""

from __future__ import annotations

from typing import Any

DEEP: dict[str, dict[str, Any]] = {
    "f.nps": {
        "essence": (
            "El tamaño nominal (NPS, Nominal Pipe Size) es un nombre, no una medida. Desde "
            "NPS 14 en adelante coincide con el diámetro exterior en pulgadas; de NPS 1/8 a 12 "
            "el diámetro exterior es mayor que el número (un NPS 2 tiene 60,3 mm de OD, no "
            "50,8). El OD es fijo para cada NPS, y lo que cambia con el schedule es el espesor y "
            "por lo tanto el diámetro interno. Su equivalente métrico es el DN (DN 50 = NPS 2).\n"
            "\n"
            "La opción «Recipiente» es para vainas montadas en un recipiente o tanque, donde no "
            "hay cañería: se cargan el diámetro del recipiente y la profundidad de líquido.",
            "Nominal Pipe Size is a name, not a measurement. From NPS 14 up it matches the "
            "outside diameter in inches; from NPS 1/8 to 12 the OD is larger than the number "
            "(an NPS 2 has a 60.3 mm OD, not 50.8). OD is fixed per NPS, and the schedule "
            "changes wall thickness and therefore inside diameter. The metric equivalent is DN "
            "(DN 50 = NPS 2).\n\n"
            "The «Vessel» option is for wells mounted on a vessel or tank, where there is no "
            "pipe: enter vessel diameter and liquid depth."),
        "why": (
            "El NPS fija el área de paso (y con ella la velocidad) y el espacio disponible para "
            "la inserción. En líneas chicas (≤ 2\") la vaina ocupa una parte importante de la "
            "sección y la regla habitual es instalar en un codo o en un ensanche.",
            "NPS sets the flow area (and therefore velocity) and the space available for "
            "insertion. In small lines (≤ 2\") the well takes up a significant part of the "
            "section and common practice is to install in an elbow or an enlarged section."),
        "worked": (
            "NPS 6 Sch 40: OD 168,3 mm, pared 7,11 mm, Di 154,1 mm.\n"
            "NPS 6 Sch 160: misma OD, pared 18,26 mm, Di 131,8 mm. El área cae 27 % y la "
            "velocidad sube 37 % con el mismo caudal.",
            "NPS 6 Sch 40: OD 168.3 mm, wall 7.11 mm, ID 154.1 mm.\n"
            "NPS 6 Sch 160: same OD, wall 18.26 mm, ID 131.8 mm. Area drops 27 % and velocity "
            "rises 37 % at the same flow."),
        "mistakes": (
            "- Calcular el área con el número del NPS como si fuera el diámetro.\n"
            "- Confundir NPS con DN en hojas de datos mixtas.\n"
            "- Instalar una vaina de 3/4\" en una línea de 1\" sin revisar el bloqueo de flujo.",
            "- Computing area with the NPS number as if it were the diameter.\n"
            "- Mixing NPS and DN on mixed datasheets.\n"
            "- Installing a 3/4\" well in a 1\" line without checking flow blockage."),
    },
    "f.schedule": {
        "essence": (
            "El schedule es una designación del espesor de pared. Históricamente salía de una "
            "fórmula aproximada (Sch ≈ 1000 × P/S): más schedule, más presión admisible. Hoy es "
            "una tabla: Sch 10, 40, 80, 160, XS, XXS (B36.10M, acero al carbono) y 5S, 10S, 40S, "
            "80S (B36.19M, inoxidable). El mismo schedule tiene espesores distintos según el "
            "NPS.",
            "Schedule designates wall thickness. Historically it came from an approximate "
            "formula (Sch ≈ 1000 × P/S): higher schedule, higher allowable pressure. Today it is "
            "a table: Sch 10, 40, 80, 160, XS, XXS (B36.10M, carbon steel) and 5S, 10S, 40S, "
            "80S (B36.19M, stainless). The same schedule has different thicknesses per NPS."),
        "why": (
            "Define el diámetro interno (velocidad) y el espesor de pared que se suma a Hs para "
            "llegar al interior de la cañería. En líneas de alta presión la pared puede tener "
            "más de 20 mm: parte del largo U queda dentro del metal.",
            "It defines inside diameter (velocity) and the wall thickness added to Hs to reach "
            "the pipe interior. In high-pressure lines the wall may exceed 20 mm: part of U "
            "length sits inside the metal."),
        "worked": (
            "NPS 4: Sch 40 = 6,02 mm; Sch 80 = 8,56 mm; Sch 160 = 13,49 mm. Pasar de 40 a 160 "
            "reduce el Di de 102,3 a 87,3 mm.",
            "NPS 4: Sch 40 = 6.02 mm; Sch 80 = 8.56 mm; Sch 160 = 13.49 mm. Going from 40 to "
            "160 reduces ID from 102.3 to 87.3 mm."),
        "mistakes": (
            "- Suponer que Sch 40 y STD son iguales en todos los tamaños (difieren desde "
            "NPS 12).\n"
            "- Usar el schedule de la línea principal en un ramal reducido.",
            "- Assuming Sch 40 and STD are equal at all sizes (they differ from NPS 12).\n"
            "- Using the main line schedule for a reduced branch."),
    },
    "f.pipe_od": {
        "essence": (
            "Diámetro exterior real de la cañería. En tamaños normalizados sale de la tabla; "
            "con «Otro» lo cargás a mano (cañerías especiales, tubos de instrumentación, "
            "ductos).",
            "Actual outside diameter of the pipe. For standard sizes it comes from the table; "
            "with «Other» you enter it by hand (special pipes, tubing, ducts)."),
        "why": (
            "Junto con el espesor da el diámetro interno: Di = OD − 2 × pared.",
            "With wall thickness it gives inside diameter: ID = OD − 2 × wall."),
        "worked": ("Tubo de 219,1 mm × 8,18 mm → Di = 202,7 mm (equivale a NPS 8 Sch 40).",
                   "Tube 219.1 mm × 8.18 mm → ID = 202.7 mm (equivalent to NPS 8 Sch 40)."),
        "mistakes": ("- Cargar el diámetro interno en el campo de OD.",
                     "- Entering inside diameter in the OD field."),
    },
    "f.wall": {
        "essence": (
            "Espesor de la pared de la cañería o del recipiente. Para la vaina importa por dos "
            "motivos: resta área de paso y es parte del recorrido que la vaina atraviesa sin "
            "flujo, desde la cara de la brida hasta la superficie interna.",
            "Thickness of the pipe or vessel wall. It matters to the well for two reasons: it "
            "reduces flow area and it is part of the path the well crosses without flow, from "
            "flange face to inner surface."),
        "why": (
            "Un error de espesor cambia la inmersión real: en una línea de pared gruesa la "
            "punta puede quedar menos sumergida de lo previsto y medir mal.",
            "A thickness error changes real immersion: in a thick-wall line the tip may be less "
            "immersed than expected and read wrongly."),
        "worked": ("Hs = 150 mm, pared 18 mm, U = 250 mm → inmersión = 250 − 150 − 18 = 82 mm.",
                   "Hs = 150 mm, wall 18 mm, U = 250 mm → immersion = 250 − 150 − 18 = 82 mm."),
        "mistakes": ("- Olvidar la pared de un recipiente (puede tener 30 a 80 mm).",
                     "- Forgetting a vessel wall (it may be 30 to 80 mm)."),
    },
    "f.pipe_id": {
        "essence": (
            "Es el diámetro libre por donde pasa el fluido. Con él se calcula el área (π·Di²/4) "
            "que convierte caudal en velocidad, y es también el límite físico de la inserción: "
            "la punta no puede tocar la pared opuesta.",
            "It is the free diameter the fluid flows through. It gives the area (π·ID²/4) that "
            "converts flow into velocity, and it is also the physical insertion limit: the tip "
            "must not touch the opposite wall."),
        "why": (
            "La velocidad depende de 1/Di²: un error del 5 % en el diámetro es un error del "
            "10 % en la velocidad y del 21 % en las fuerzas.",
            "Velocity depends on 1/ID²: a 5 % diameter error is a 10 % velocity error and a "
            "21 % force error."),
        "worked": (
            "Caudal 0,1 m³/s: con Di = 154 mm, V = 5,37 m/s; con Di = 146 mm, V = 5,97 m/s "
            "(+11 %).\n\n"
            "Para una buena medición la punta suele quedar entre 1/3 y 1/2 del diámetro: en "
            "Di = 154 mm, entre 51 y 77 mm de inmersión.",
            "Flow 0.1 m³/s: with ID = 154 mm, V = 5.37 m/s; with ID = 146 mm, V = 5.97 m/s "
            "(+11 %).\n\n"
            "For a good reading the tip usually sits between 1/3 and 1/2 of the diameter: at "
            "ID = 154 mm, 51 to 77 mm immersion."),
        "mistakes": ("- Usar el diámetro nominal.\n- Olvidar revestimientos internos.",
                     "- Using nominal diameter.\n- Forgetting internal linings."),
    },
    "f.orientation": {
        "essence": (
            "Describe la posición de la vaina respecto del flujo:\n\n"
            "- Perpendicular: el flujo golpea el vástago de costado; es el caso de la norma.\n"
            "- Inclinado: la vaina entra en ángulo, típicamente 45° contra el flujo, para ganar "
            "inmersión en líneas chicas.\n"
            "- En codo: la vaina queda alineada con el eje de la cañería y la punta enfrenta el "
            "flujo; la carga transversal es mucho menor.\n"
            "- En recipiente: sin flujo apreciable; la vaina solo soporta presión, temperatura "
            "y su peso.",
            "Describes the well position relative to flow:\n\n"
            "- Perpendicular: flow hits the shank sideways; the standard's case.\n"
            "- Angled: the well enters at an angle, typically 45° against the flow, to gain "
            "immersion in small lines.\n"
            "- Elbow: the well is aligned with the pipe axis and the tip faces the flow; "
            "transverse load is much smaller.\n"
            "- Vessel: no significant flow; the well only carries pressure, temperature and "
            "its own weight."),
        "why": (
            "Cambia la inmersión útil, la carga del flujo y qué verificaciones aplican. El codo "
            "es la mejor solución para líneas chicas y velocidades altas.",
            "It changes useful immersion, flow load and which checks apply. The elbow is the "
            "best solution for small lines and high velocities."),
        "worked": (
            "Línea de 2\" (Di 52,5 mm): perpendicular, la inserción máxima razonable es unos "
            "26 mm; inclinada a 45°, el mismo recorrido radial permite 37 mm de vástago; en "
            "codo, la inserción puede ser de 100 mm o más.",
            "2\" line (ID 52.5 mm): perpendicular, the reasonable max insertion is about "
            "26 mm; angled at 45°, the same radial travel allows 37 mm of shank; in an elbow "
            "insertion can be 100 mm or more."),
        "mistakes": (
            "- Instalar en codo con la punta a favor del flujo (aguas abajo): queda en la "
            "estela y mide mal.\n"
            "- Usar «En recipiente» para un tanque con agitador sin agregar un caso con "
            "velocidad.",
            "- Installing in an elbow with the tip pointing downstream: it sits in the wake "
            "and reads poorly.\n"
            "- Using «Vessel» for an agitated tank without adding a velocity case."),
    },
    "f.insulation": {
        "essence": (
            "Espesor del aislamiento térmico de la cañería. La conexión y el cabezal de la "
            "vaina deben quedar fuera del aislamiento para que el sensor y su electrónica no "
            "se calienten y para poder desmontarla. El largo de lag (extensión) sale de este "
            "espesor.",
            "Thickness of the pipe's thermal insulation. The well's connection and head must "
            "stay outside the insulation so the sensor and electronics do not overheat and the "
            "well can be removed. The lag (extension) length comes from this thickness."),
        "why": (
            "Un cabezal enterrado en el aislamiento recibe el calor del proceso: un "
            "transmisor que admite 85 °C puede fallar en una línea de vapor a 250 °C.",
            "A head buried in insulation receives process heat: a transmitter rated for 85 °C "
            "may fail on a 250 °C steam line."),
        "worked": ("Aislamiento 75 mm → lag recomendado ≈ 75 + 25 = 100 mm.",
                   "Insulation 75 mm → recommended lag ≈ 75 + 25 = 100 mm."),
        "mistakes": ("- Pedir lag cero en líneas calientes aisladas.",
                     "- Asking for zero lag on hot insulated lines."),
    },
    "f.mount": {
        "essence": (
            "Es la altura del montaje: desde la superficie externa de la cañería hasta la cara "
            "de la brida (o la boca de la cupla) donde se fija la vaina. Ese tramo es un tubo "
            "por donde la vaina pasa sin recibir flujo: el fluido dentro del niple está casi "
            "quieto.",
            "It is the mounting height: from the pipe outer surface to the flange face (or "
            "coupling mouth) where the well is fixed. That stretch is a tube the well crosses "
            "without receiving flow: the fluid inside the nozzle is nearly still."),
        "why": (
            "Define cuánto del largo U queda realmente en el flujo y, por lo tanto, la "
            "inmersión y la carga. También determina la zona protegida L0, que reduce la carga "
            "calculada si se declara.",
            "It defines how much of U is really in the flow, and therefore immersion and load. "
            "It also sets the shielded length L0, which reduces the computed load if "
            "declared."),
        "mistakes": (
            "- Medir Hs desde el eje de la cañería en vez de la superficie externa.\n"
            "- Olvidar que Hs incluye la brida de la línea y la junta.",
            "- Measuring Hs from the pipe axis instead of the outer surface.\n"
            "- Forgetting that Hs includes the line flange and gasket."),
        "worked": (
            "Cupla de 1\" con brida de 1½\" clase 300: Hs = 150 mm, pared Sch 40 en 6\" = "
            "7,1 mm. Con U = 250 mm la inmersión es 250 − 157,1 = 92,9 mm (60 % del Di de "
            "154 mm).",
            "1\" coupling with 1½\" class 300 flange: Hs = 150 mm, Sch 40 wall in 6\" = "
            "7.1 mm. With U = 250 mm immersion is 250 − 157.1 = 92.9 mm (60 % of the 154 mm "
            "ID)."),
    },
    "f.nozzle_id": {
        "essence": (
            "Diámetro interno del niple o conexión por donde pasa la vaina. La raíz A tiene "
            "que entrar con holgura: si el niple es justo, la vaina roza y no se puede montar, "
            "o queda apoyada en un punto que cambia su comportamiento vibratorio.",
            "Inside diameter of the nozzle the well passes through. Root A must fit with "
            "clearance: if the nozzle is tight, the well rubs and cannot be installed, or it "
            "rests on a point that changes its vibration behaviour."),
        "why": (
            "Evita descubrir en el montaje que la vaina no entra. Las soldaduras internas del "
            "niple también reducen el paso real.",
            "It avoids finding out at installation that the well does not fit. Internal "
            "nozzle welds also reduce the real bore."),
        "worked": (
            "Niple de 1½\" Sch 80: Di = 38,1 mm. Vaina con A = 34,9 mm (1⅜\"): holgura "
            "(38,1 − 34,9)/2 = 1,6 mm por lado → justo. Con Sch 160 (Di 33,98 mm) no entra.",
            "1½\" Sch 80 nozzle: ID = 38.1 mm. Well with A = 34.9 mm (1⅜\"): clearance "
            "(38.1 − 34.9)/2 = 1.6 mm per side → tight. With Sch 160 (ID 33.98 mm) it does "
            "not fit."),
        "mistakes": ("- No dejar margen para el cordón interno de soldadura.",
                     "- Leaving no margin for the internal weld bead."),
    },
    "f.mount_angle": {
        "essence": (
            "Con la vaina inclinada, el largo expuesto se reparte entre una componente hacia el "
            "centro de la cañería (radial) y otra a lo largo del eje. La profundidad radial es "
            "inmersión × sen(ángulo): a 45°, 100 mm de vástago avanzan 71 mm hacia el centro. "
            "Por eso inclinar permite más vástago en líneas chicas sin tocar la pared "
            "opuesta.\n\n"
            "Además, el flujo ya no golpea de costado: la componente normal al vástago es "
            "V·sen(ángulo), menor que V. TS usa V completa, del lado seguro.",
            "With an angled well, the exposed length splits into a component towards the pipe "
            "centre (radial) and one along the axis. Radial depth is immersion × sin(angle): "
            "at 45°, 100 mm of shank advances 71 mm towards the centre. That is why angling "
            "allows more shank in small lines without touching the opposite wall.\n\n"
            "Also, flow no longer hits sideways: the component normal to the shank is "
            "V·sin(angle), smaller than V. TS uses the full V, on the safe side."),
        "why": (
            "Sin el ángulo, el aviso de pared opuesta y el largo automático suponen montaje "
            "perpendicular y pueden recortar de más la inserción.",
            "Without the angle, the opposite-wall warning and automatic length assume "
            "perpendicular mounting and may cut insertion too much."),
        "worked": (
            "Di = 77,9 mm (3\" Sch 40), ángulo 45°, inmersión 80 mm → profundidad radial "
            "= 80 × 0,707 = 57 mm = 73 % del Di: queda lejos de la pared opuesta.",
            "ID = 77.9 mm (3\" Sch 40), angle 45°, immersion 80 mm → radial depth = 80 × "
            "0.707 = 57 mm = 73 % of ID: well clear of the opposite wall."),
        "mistakes": (
            "- Medir el ángulo respecto de la vertical en vez del eje de la cañería.\n"
            "- Inclinar a favor del flujo: la punta queda en la estela.",
            "- Measuring the angle from vertical instead of the pipe axis.\n"
            "- Angling with the flow: the tip sits in the wake."),
    },
    "f.liquid_depth": {
        "essence": (
            "En un recipiente, la vaina mide bien solo si la punta está sumergida en el "
            "líquido. Con el nivel bajo, la punta puede quedar en el vapor o el gas de arriba, "
            "que tiene otra temperatura y transfiere mucho menos calor. La profundidad útil es "
            "lo que la vaina puede aprovechar del líquido con el nivel mínimo de operación.",
            "In a vessel the well reads correctly only if the tip is submerged in liquid. At "
            "low level the tip may sit in the vapour or gas above, which has a different "
            "temperature and transfers much less heat. Usable depth is what the well can use "
            "of the liquid at minimum operating level."),
        "why": (
            "Limita la inmersión junto con el diámetro del recipiente. TS busca 450 mm de "
            "inmersión, sin pasar del 80 % de esta profundidad.",
            "It limits immersion together with vessel diameter. TS looks for 450 mm "
            "immersion, without exceeding 80 % of this depth."),
        "worked": (
            "Tanque con nivel mínimo 600 mm sobre la conexión inferior: inmersión objetivo = "
            "mín(450, 0,8 × 600) = 450 mm. Con nivel mínimo 300 mm: 240 mm.",
            "Tank with minimum level 600 mm above the lower nozzle: target immersion = "
            "min(450, 0.8 × 600) = 450 mm. With minimum level 300 mm: 240 mm."),
        "mistakes": (
            "- Usar el nivel normal en vez del mínimo.\n"
            "- Montar en la parte superior de un tanque con nivel variable.",
            "- Using normal level instead of minimum.\n"
            "- Mounting on the top of a tank with variable level."),
    },
}
