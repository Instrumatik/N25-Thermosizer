"""Tablas de guía de la biblioteca: tipos de conexión y perfiles del vástago.

Práctica habitual de ingeniería resumida con redacción propia (no se copia texto de
normas). Los costos son relativos y orientativos, no precios de proveedor.
"""

from __future__ import annotations

from typing import Final

Bi = tuple[str, str]
Table = tuple[tuple[Bi, ...], ...]
"""Primera fila = encabezados; cada celda es (es, en)."""

CONNECTION_TABLE: Final[Table] = (
    (("Conexión", "Connection"), ("Dónde se usa", "Where it is used"),
     ("Dónde no conviene", "Where it should not be used")),
    (("Roscado (NPT)", "Threaded (NPT)"),
     ("Servicios auxiliares de baja exigencia: agua de refrigeración, aire, aceite de "
      "lubricación, hasta unos 20 barg y 200 °C. Barato y rápido de montar.",
      "Low-demand utility services: cooling water, air, lube oil, up to about 20 barg and "
      "200 °C. Cheap and quick to install."),
     ("Fluidos peligrosos o inflamables, H₂S, vapor, alta presión o temperatura, vibración o "
      "ciclos térmicos: la rosca es un camino de fuga y concentra esfuerzos en la raíz.",
      "Hazardous or flammable fluids, H₂S, steam, high pressure or temperature, vibration or "
      "thermal cycling: the thread is a leak path and concentrates stress at the root.")),
    (("Bridado", "Flanged"),
     ("La opción estándar en refinerías, petroquímica, oil & gas y vapor. Se desmonta para "
      "inspeccionar y la clase B16.5 cubre casi cualquier presión.",
      "The standard choice in refineries, petrochemicals, oil & gas and steam. It can be "
      "removed for inspection and the B16.5 class covers almost any pressure."),
     ("Espacios muy reducidos o costo mínimo en líneas chicas. Pide clase y material de brida "
      "compatibles con la especificación de cañería.",
      "Very tight spaces or minimum cost on small lines. It needs a flange class and material "
      "compatible with the piping specification.")),
    (("Socket weld", "Socket weld"),
     ("Líneas chicas de alta presión o temperatura (vapor, hidrocarburos) donde se quiere "
      "estanqueidad total sin brida.",
      "Small high-pressure or high-temperature lines (steam, hydrocarbons) where full "
      "tightness without a flange is wanted."),
     ("Servicios con corrosión en rendijas o con inspección frecuente: queda una rendija en el "
      "socket y no se retira sin cortar.",
      "Services with crevice corrosion or frequent inspection: a crevice remains in the socket "
      "and it cannot be removed without cutting.")),
    (("Soldado (weld-in)", "Weld-in"),
     ("Muy alta presión y temperatura: vapor principal, calderas, turbinas. Es la conexión más "
      "resistente.",
      "Very high pressure and temperature: main steam, boilers, turbines. It is the strongest "
      "connection."),
     ("Cuando hay que desmontar o reemplazar la vaina en servicio. Exige soldador calificado y "
      "tratamiento térmico según el material.",
      "When the thermowell must be removed or replaced in service. It needs a qualified welder "
      "and heat treatment depending on the material.")),
    (("Van Stone", "Van Stone"),
     ("Servicios corrosivos: el cuerpo de la vaina es de una sola pieza en aleación "
      "(Hastelloy, titanio, etc.) y se sujeta con una brida loca de acero común, más barata.",
      "Corrosive services: the thermowell body is one piece of alloy (Hastelloy, titanium, "
      "etc.) clamped by a cheaper loose carbon-steel flange."),
     ("Alta presión o temperatura, donde la brida loca no da la misma rigidez. Poco común "
      "fuera de química.",
      "High pressure or temperature, where the loose flange is not as stiff. Uncommon outside "
      "chemicals.")),
    (("Sanitario (clamp)", "Sanitary (clamp)"),
     ("Alimentos, bebidas, farmacia y biotecnología: superficies pulidas, sin rendijas y "
      "desarme rápido para limpieza CIP/SIP.",
      "Food, beverages, pharma and biotech: polished surfaces, no crevices and quick "
      "disassembly for CIP/SIP cleaning."),
     ("Procesos industriales a presión, hidrocarburos o vapor de alta: su presión admisible es "
      "baja.",
      "Pressurized industrial processes, hydrocarbons or high-pressure steam: its allowable "
      "pressure is low.")),
)
CONNECTION_ROWS: Final[dict[str, int]] = {
    "threaded": 1, "flanged": 2, "socket_weld": 3, "weld_in": 4, "van_stone": 5,
    "sanitary": 6,
}
CONNECTION_NOTE: Final[Bi] = (
    "En el cálculo ASME las conexiones roscadas tienen un factor de concentración de esfuerzos "
    "mayor y un límite a la fatiga menor que las bridadas o soldadas, y TS avisa si hay una "
    "rosca en un servicio exigente. La elección final sigue la especificación de cañería del "
    "proyecto.",
    "In the ASME calculation threaded connections have a higher stress concentration factor "
    "and a lower fatigue limit than flanged or welded ones, and TS warns about a thread in a "
    "demanding service. The final choice follows the project piping specification.")

PROFILE_TABLE: Final[Table] = (
    (("Perfil", "Profile"), ("Cuándo conviene", "When to use it"),
     ("Limitaciones", "Limitations"), ("Costo relativo", "Relative cost"),
     ("Por qué", "Why")),
    (("Cónico", "Tapered"),
     ("La opción por defecto en la mayoría de los servicios, sobre todo gases y vapor a "
      "velocidad media o alta. A igual punta es el más rígido: la raíz gruesa sube la "
      "frecuencia natural y baja el esfuerzo donde más carga hay.",
      "The default in most services, especially gases and steam at medium or high velocity. "
      "For the same tip it is the stiffest: the thick root raises the natural frequency and "
      "lowers the stress where the load is highest."),
     ("Algo más caro de mecanizar que el recto.", "Somewhat more costly to machine than "
                                                  "straight."),
     ("1,10 a 1,25", "1.10 to 1.25"),
     ("Torneado de perfil (CNC o copiador) y más tiempo; arranca de una barra más gruesa para "
      "lograr la raíz A.",
      "Profile turning (CNC or copy lathe) and more time; it starts from a thicker bar to get "
      "the root A.")),
    (("Escalonado", "Stepped"),
     ("Velocidades altas donde hace falta punta fina (respuesta térmica) y raíz gruesa "
      "(rigidez). También cuando la brida de montaje limita el diámetro de raíz A.",
      "High velocities that need a thin tip (thermal response) and a thick root (stiffness). "
      "Also when the mounting flange limits the root diameter A."),
     ("El escalón concentra esfuerzos, así que TS también verifica esa sección. ASME acota la "
      "relación B/A (aprox. 0,58 a 0,88).",
      "The step concentrates stress, so TS also checks that section. ASME limits the B/A "
      "ratio (about 0.58 to 0.88)."),
     ("1,05 a 1,15", "1.05 to 1.15"),
     ("Dos diámetros y un radio en el escalón: una operación más, pero sigue siendo torneado "
      "simple.",
      "Two diameters and a radius at the step: one more operation, still simple turning.")),
    (("Recto", "Straight"),
     ("Servicios suaves: líquidos a baja velocidad, largos cortos, roscadas chicas. Es el más "
      "simple y barato.",
      "Mild services: liquids at low velocity, short lengths, small threaded wells. The "
      "simplest and cheapest."),
     ("Es el menos rígido: con largos grandes o gases rápidos entra en resonancia.",
      "The least stiff: with long lengths or fast gases it goes into resonance."),
     ("1,0 (base)", "1.0 (base)"),
     ("Torneado cilíndrico simple: menos material desbastado y menos tiempo de máquina.",
      "Simple cylindrical turning: less material removed and less machine time.")),
)
PROFILE_ROWS: Final[dict[str, int]] = {"tapered": 1, "stepped": 2, "straight": 3}
PROFILE_COST_NOTE: Final[Bi] = (
    "Costos relativos orientativos para una vaina de barra perforada en inoxidable 316 de "
    "largo similar (no son precios de proveedor). El perfil pesa menos que el material "
    "(aleaciones como Inconel, Hastelloy o titanio multiplican el costo 3 a 10 veces), la "
    "conexión y su clase, el largo y el diámetro de barra (la perforación profunda es la "
    "operación más cara) y los extras (stellite, PMI, radiografía, prueba hidrostática, "
    "certificados). Un cónico que cumple con un U más corto suele salir más barato en total "
    "que un recto largo.",
    "Indicative relative costs for a 316 stainless drilled bar-stock thermowell of similar "
    "length (not supplier prices). The profile weighs less than the material (alloys such as "
    "Inconel, Hastelloy or titanium multiply the cost 3 to 10 times), the connection and its "
    "class, the length and bar diameter (deep drilling is the most expensive operation) and "
    "extras (stellite, PMI, radiography, hydrostatic test, certificates). A tapered well that "
    "passes with a shorter U is usually cheaper overall than a long straight one.")
PROFILE_AUTO: Final[Bi] = (
    "En automático TS arma candidatos con los diseños típicos para la conexión y el agujero "
    "del sensor (0,260\" o 0,385\"), descarta los que no entran en la brida de montaje, prueba "
    "primero cónicos, después escalonados y por último rectos, recorriendo los largos U desde "
    "el de buena inmersión. Corre la verificación ASME completa en todos los casos de flujo, "
    "se queda con el primero que cumple (mejor margen en el peor caso) y, si ninguno cumple, "
    "informa el mejor y avisa.",
    "In automatic mode TS builds candidates from the typical designs for the connection and "
    "the sensor bore (0.260\" or 0.385\"), drops those that do not fit the mounting flange, "
    "tries tapered first, then stepped and finally straight, going through the U lengths from "
    "the one with good immersion. It runs the full ASME check for every flow case, keeps the "
    "first one that passes (best worst-case margin) and, if none passes, reports the best one "
    "and warns.")
