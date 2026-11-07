"""Segunda pasada: opciones de cálculo, modos de selección y casos de flujo."""

from __future__ import annotations

from typing import Any

_MODE_LIMITS = (
    "En «Automático» TS justifica cada valor en la pestaña de selección automática. En "
    "«Manual», el valor cargado manda aunque no sea el óptimo, y las verificaciones lo "
    "aceptan o lo rechazan.",
    "In «Automatic» TS justifies each value on the automatic selection tab. In «Manual» the "
    "entered value rules even if not optimal, and the checks accept or reject it.")

DEEP: dict[str, dict[str, Any]] = {
    "opt.damping": {
        "essence": (
            "El amortiguamiento ζ es la fracción de energía de vibración que se pierde en cada "
            "ciclo. En una termovaina viene de tres fuentes:\n\n"
            "- Fricción interna del metal: al deformarse, los granos y las dislocaciones se "
            "mueven un poco y disipan calor. En el acero es muy baja.\n"
            "- Microdeslizamiento en el apoyo: la brida y la junta, o los filetes de la rosca, "
            "rozan levemente con cada ciclo.\n"
            "- El fluido: la vaina empuja fluido al moverse y pierde energía en él.\n\n"
            "Un ζ de 0,0005 significa que, si se golpea la vaina, la vibración tarda unos 220 "
            "ciclos en caer a la mitad: suena como una campana.",
            "Damping ζ is the fraction of vibration energy lost each cycle. In a thermowell it "
            "comes from three sources:\n\n"
            "- Internal metal friction: when deforming, grains and dislocations move slightly "
            "and dissipate heat. In steel it is very low.\n"
            "- Micro-slip at the support: flange and gasket, or thread flanks, rub slightly "
            "each cycle.\n"
            "- The fluid: the well pushes fluid as it moves and loses energy into it.\n\n"
            "A ζ of 0.0005 means that if the well is struck, vibration takes about 220 cycles "
            "to halve: it rings like a bell."),
        "why": (
            "Entra en el número de Scruton, que decide si se aplica el límite 0,4 o el 0,8. "
            "Con poco amortiguamiento, la vaina no puede frenar la resonancia en línea. El "
            "valor por defecto de la norma es deliberadamente conservador.",
            "It enters the Scruton number, which decides whether the 0.4 or 0.8 limit "
            "applies. With little damping the well cannot curb in-line resonance. The "
            "standard's default value is deliberately conservative."),
        "worked": (
            "Gas a 40 kg/m³, vaina de 316: con ζ = 0,0005 → N_Sc ≈ 0,43 (límite 0,4). Con "
            "ζ = 0,003 → N_Sc ≈ 2,6 (pasa el umbral de 2,5 y el límite sube a 0,8). Cambiar ζ "
            "puede duplicar la velocidad admitida.",
            "Gas at 40 kg/m³, 316 well: with ζ = 0.0005 → N_Sc ≈ 0.43 (0.4 limit). With "
            "ζ = 0.003 → N_Sc ≈ 2.6 (crosses the 2.5 threshold and the limit rises to 0.8). "
            "Changing ζ can double the allowed velocity."),
        "mistakes": (
            "- Subirlo sin un ensayo de golpe (ring-down) que lo respalde.\n"
            "- Usar valores de estructuras soldadas o atornilladas grandes, que amortiguan "
            "mucho más que una vaina maciza.",
            "- Raising it without a ring-down test to back it.\n"
            "- Using values from large welded or bolted structures, which damp far more than "
            "a solid well."),
    },
    "opt.strouhal": {
        "essence": (
            "El número de Strouhal N_S dice cuántos remolinos suelta un cilindro por cada "
            "diámetro que avanza el flujo: f_s = N_S·V/B. No es una constante: depende del "
            "número de Reynolds, que mide si el flujo es dominado por la viscosidad o por la "
            "inercia. En el rango subcrítico ronda 0,2 a 0,22; cerca de la transición de la "
            "capa límite a turbulenta (Re ≈ 2·10⁵ a 5·10⁵) los remolinos se desorganizan y "
            "N_S puede subir bastante.\n\n"
            "Esta opción elige entre la correlación de la norma en función de Re y un valor "
            "fijo de 0,22, que usan algunas planillas antiguas.",
            "The Strouhal number N_S says how many eddies a cylinder sheds per diameter of "
            "flow travel: f_s = N_S·V/B. It is not constant: it depends on Reynolds number, "
            "which measures whether flow is dominated by viscosity or inertia. In the "
            "subcritical range it is about 0.2 to 0.22; near the boundary layer transition to "
            "turbulent (Re ≈ 2·10⁵ to 5·10⁵) eddies become disorganised and N_S can rise "
            "noticeably.\n\n"
            "This option chooses between the standard's Re-dependent correlation and a fixed "
            "0.22, used by some older spreadsheets."),
        "why": (
            "Un N_S mayor da una f_s mayor y menos margen. La correlación es la de la norma y "
            "la que se emite; el valor fijo sirve solo para comparar con cálculos viejos.",
            "A higher N_S gives a higher f_s and less margin. The correlation is the "
            "standard's and the one to issue; the fixed value only serves to compare with old "
            "calculations."),
        "worked": (
            "Gas, V = 20 m/s, B = 19,05 mm. Con 0,22: f_s = 231 Hz. Si la correlación da "
            "0,26 en la zona de transición: f_s = 273 Hz, un 18 % más. Con f_n,c = 620 Hz, r "
            "pasa de 0,37 a 0,44 y deja de cumplir el límite 0,4.",
            "Gas, V = 20 m/s, B = 19.05 mm. With 0.22: f_s = 231 Hz. If the correlation gives "
            "0.26 in the transition zone: f_s = 273 Hz, 18 % more. With f_n,c = 620 Hz, r goes "
            "from 0.37 to 0.44 and fails the 0.4 limit."),
        "mistakes": ("- Emitir un cálculo con el valor fijo.",
                     "- Issuing a calculation with the fixed value."),
    },
    "opt.fe": {
        "essence": (
            "El factor ambiental F_E multiplica el límite de fatiga para descontar el efecto "
            "del medio. Un ambiente corrosivo ataca la fatiga por dos caminos:\n\n"
            "- Crea picaduras que actúan como entallas y concentran esfuerzos.\n"
            "- En la punta de una fisura, el metal recién expuesto en cada ciclo se corroe "
            "antes de repasivarse, y la fisura avanza más rápido (fatiga-corrosión). En este "
            "caso puede no existir un límite de vida infinita.",
            "The environmental factor F_E multiplies the fatigue limit to discount the "
            "effect of the medium. A corrosive environment attacks fatigue in two ways:\n\n"
            "- It creates pits acting as notches that concentrate stress.\n"
            "- At a crack tip, metal freshly exposed each cycle corrodes before repassivating, "
            "and the crack advances faster (corrosion fatigue). In that case an "
            "infinite-life limit may not exist."),
        "why": (
            "Sin descuento, una vaina en agua de mar o en un ácido puede fatigarse mucho antes "
            "de lo previsto, aunque la corrosión uniforme sea baja.",
            "Without the discount, a well in seawater or acid may fatigue much sooner than "
            "expected, even if uniform corrosion is low."),
        "worked": (
            "316 soldado, límite 21 MPa. Aire o hidrocarburo seco: F_E = 1. Agua de mar: "
            "F_E ≈ 0,5 → 10,5 MPa. Una vaina con S_o = 14 MPa pasa de cumplir con margen a "
            "no cumplir.",
            "Welded 316, limit 21 MPa. Air or dry hydrocarbon: F_E = 1. Seawater: F_E ≈ 0.5 "
            "→ 10.5 MPa. A well with S_o = 14 MPa goes from passing with margin to failing."),
        "mistakes": ("- Dejar 1 en servicios ácidos o con cloruros.\n- Usar F_E para «compensar» "
                     "un material inadecuado.",
                     "- Leaving 1 in acidic or chloride services.\n- Using F_E to "
                     "«compensate» an unsuitable material."),
    },
    "opt.metal_state": {
        "essence": (
            "Una raíz mecanizada de barra tiene la microestructura del laminado, homogénea y "
            "sin defectos. Una raíz soldada tiene tres desventajas frente a la fatiga:\n\n"
            "- Defectos microscópicos (poros, inclusiones, falta de fusión) que ya son "
            "fisuras pequeñas.\n"
            "- Tensiones residuales de tracción por la contracción del cordón al enfriarse.\n"
            "- Una zona afectada por el calor con granos más gruesos.\n\n"
            "Por eso las normas dan límites de fatiga distintos para cada estado.",
            "A root machined from bar has the rolled microstructure, homogeneous and "
            "defect-free. A welded root has three drawbacks for fatigue:\n\n"
            "- Microscopic defects (pores, inclusions, lack of fusion) that are already small "
            "cracks.\n"
            "- Tensile residual stresses from the weld shrinking as it cools.\n"
            "- A heat-affected zone with coarser grains.\n\n"
            "That is why standards give different fatigue limits for each state."),
        "why": ("Puede cambiar el límite de fatiga a más del doble. Elegir mal el estado "
                "es aprobar una vaina que no cumple.",
                "It can change the fatigue limit by more than a factor of two. Choosing the "
                "wrong state means passing a well that fails."),
        "worked": (
            "316 mecanizado ≈ 48 MPa; soldado ≈ 21 MPa. Una vaina bridada de una pieza "
            "mecanizada usa 48; una con la brida soldada al vástago, 21.",
            "Machined 316 ≈ 48 MPa; welded ≈ 21 MPa. A one-piece machined flanged well uses "
            "48; one with the flange welded to the shank, 21."),
        "mistakes": ("- Elegir «no soldado» para una vaina con brida soldada.",
                     "- Choosing «not welded» for a well with a welded flange."),
    },
    "opt.amber": {
        "essence": (
            "Define desde qué cercanía al límite el estado pasa a amarillo. Una verificación "
            "que está al 95 % del límite cumple en el papel, pero cualquier incertidumbre la "
            "puede dejar afuera: el caudal real suele diferir del de diseño en un 10 a 20 %, "
            "las propiedades del fluido tienen errores y la geometría tiene tolerancias de "
            "fabricación.\n\n"
            "El margen no cambia el cálculo: solo marca las verificaciones que piden una "
            "segunda mirada.",
            "It defines how close to the limit the status turns amber. A check at 95 % of "
            "the limit passes on paper, but any uncertainty can push it out: actual flow "
            "usually differs from design by 10 to 20 %, fluid properties have errors and "
            "geometry has manufacturing tolerances.\n\n"
            "The margin does not change the calculation: it only flags the checks that need "
            "a second look."),
        "why": ("Evita emitir diseños al filo sin una decisión consciente.",
                "It avoids issuing knife-edge designs without a conscious decision."),
        "worked": (
            "Margen 10 %, límite 0,4: un r = 0,37 queda amarillo (más del 90 % del límite). "
            "Como f_s ∝ V, un 8 % más de velocidad lo lleva a 0,40.",
            "10 % margin, limit 0.4: r = 0.37 is amber (above 90 % of the limit). Since "
            "f_s ∝ V, 8 % more velocity takes it to 0.40."),
        "mistakes": ("- Ponerlo en 0 para que todo salga verde.",
                     "- Setting it to 0 so everything turns green."),
    },
    "opt.flange_manual": {
        "essence": (
            "Reemplaza la presión admisible de la tabla B16.5 por un valor cargado a mano. Se "
            "usa cuando la brida no es B16.5: bridas de otra norma (EN 1092, API 6A), "
            "bridas especiales de proveedor o materiales sin grupo en la tabla. El valor debe "
            "ser la presión admisible a la temperatura de diseño, no a temperatura ambiente.",
            "It replaces the B16.5 table allowable pressure with a hand-entered value. It is "
            "used when the flange is not B16.5: flanges of another standard (EN 1092, API 6A), "
            "special supplier flanges or materials without a group in the table. The value "
            "must be the allowable pressure at design temperature, not at ambient."),
        "why": ("El cálculo lo acepta sin verificarlo: debe tener respaldo documental en el "
                "informe.",
                "The calculation accepts it unchecked: it must be documented in the report."),
        "worked": (
            "Brida EN PN 40 en acero 1.4404 a 200 °C: el fabricante declara ≈ 32 bar (menos "
            "que los 40 nominales). Se carga 32, no 40.",
            "EN PN 40 flange in 1.4404 steel at 200 °C: the manufacturer declares ≈ 32 bar "
            "(less than the nominal 40). Enter 32, not 40."),
        "mistakes": ("- Cargar la presión nominal o la de prueba.",
                     "- Entering nominal or test pressure."),
    },
    "opt.inline": {
        "essence": (
            "Con Scruton alto, la norma permite que la vaina opere por encima de la "
            "resonancia en línea (f_s entre 0,4 y 0,8 de f_n,c), siempre que solo la atraviese "
            "durante arranques y paradas. Esta opción habilita ese criterio y activa la "
            "verificación del esfuerzo durante el paso.\n\n"
            "Funciona porque en un gas liviano el fluido entrega poca energía y la vaina "
            "disipa lo suficiente para que la resonancia en línea no crezca mucho.",
            "With high Scruton, the standard allows the well to run above in-line resonance "
            "(f_s between 0.4 and 0.8 of f_n,c), provided it only crosses it during start-ups "
            "and shutdowns. This option enables that criterion and turns on the passage "
            "stress check.\n\n"
            "It works because in a light gas the fluid supplies little energy and the well "
            "dissipates enough so in-line resonance does not grow much."),
        "why": ("Habilita diseños más largos en gases, pero pide un proceso que no opere "
                "mucho tiempo en la zona de resonancia.",
                "It enables longer designs in gases, but needs a process that does not run "
                "long in the resonance zone."),
        "worked": (
            "Compresor que arranca en 30 s y luego opera estable a f_s = 0,6·f_n,c: paso "
            "breve, aceptable si el esfuerzo en resonancia cumple. Un gasoducto que opera días "
            "a caudal reducido justo en la banda de resonancia no lo es.",
            "Compressor starting in 30 s and then running steadily at f_s = 0.6·f_n,c: brief "
            "passage, acceptable if resonant stress passes. A pipeline running for days at "
            "reduced flow right in the resonance band is not."),
        "mistakes": ("- Activarlo en líquidos.\n- No cargar el caso de caudal mínimo.",
                     "- Enabling it for liquids.\n- Not entering the minimum-flow case."),
    },
    "opt.corrosion_cases": {
        "essence": (
            "Evalúa cada caso dos veces: con la vaina nueva y con el sobreespesor consumido "
            "(fin de vida). Al corroerse, la vaina pierde diámetro exterior y gana agujero, "
            "así que todo cambia a la vez: menos rigidez y menos masa (la frecuencia baja, "
            "porque la rigidez cae más rápido), una punta más fina (la estela sube) y menos "
            "pared (menos presión admisible).",
            "It evaluates each case twice: with the new well and with the allowance consumed "
            "(end of life). As it corrodes the well loses outside diameter and gains bore, so "
            "everything changes at once: less stiffness and less mass (frequency falls, "
            "because stiffness drops faster), a thinner tip (the wake rises) and less wall "
            "(less allowable pressure)."),
        "why": ("La vaina tiene que cumplir el último día de su vida, no solo el primero.",
                "The well must pass on the last day of its life, not just the first."),
        "worked": (
            "Sobreespesor 1,5 mm. Nueva: B = 19,05 mm, r = 0,36. Corroída: B = 16,05 mm, f_s "
            "sube 19 %, f_n,c baja ≈ 4 %, r = 0,45 → manda la corroída y no cumple el "
            "límite 0,4.",
            "Allowance 1.5 mm. New: B = 19.05 mm, r = 0.36. Corroded: B = 16.05 mm, f_s rises "
            "19 %, f_n,c falls ≈ 4 %, r = 0.45 → corroded governs and fails the 0.4 limit."),
        "mistakes": ("- Desactivarlo con sobreespesor cargado.",
                     "- Turning it off with an allowance entered."),
    },
    "opt.supplier": {
        "essence": (
            "Calcula como los ratings genéricos de catálogo: sin la masa añadida del fluido "
            "ni la del sensor. Esos ratings suelen publicarse para agua o aire con supuestos "
            "simplificados, y la frecuencia natural resulta algo mayor que la de la norma.",
            "It calculates like generic catalogue ratings: without fluid added mass or sensor "
            "mass. Those ratings are usually published for water or air with simplified "
            "assumptions, and natural frequency comes out somewhat higher than the "
            "standard's."),
        "why": ("Sirve para entender por qué un proveedor aprueba una vaina que TS rechaza; "
                "no para el diseño final en líquidos.",
                "It helps understand why a supplier passes a well TS rejects; not for final "
                "design in liquids."),
        "worked": (
            "En agua, la masa añadida baja f_n unos 5 a 7 % en una vaina típica. Una vaina "
            "con r = 0,38 según el proveedor puede dar r = 0,41 con la norma.",
            "In water, added mass lowers f_n about 5 to 7 % for a typical well. A well with "
            "r = 0.38 per the supplier may give r = 0.41 with the standard."),
        "mistakes": ("- Emitir el cálculo con esta opción.",
                     "- Issuing the calculation with this option."),
    },
    "f.mode_material": {
        "essence": (
            "En automático, TS elige el material en este orden:\n\n"
            "1. Compatibilidad química con el fluido según la matriz de la biblioteca.\n"
            "2. Rango de temperatura del material.\n"
            "3. Servicio ácido: si la presión parcial de H₂S supera 0,345 kPa (0,05 psia), "
            "exige un material "
            "aceptado por NACE con límite de dureza.\n"
            "4. Cloruros: por encima de unos 50 ppm y 60 °C descarta austeníticos y pasa a "
            "dúplex o aleaciones de níquel, por el riesgo de corrosión bajo tensión.\n"
            "5. Erosión: con V/V_e alta agrega Stellite en la punta y sobreespesor.",
            "In automatic, TS chooses material in this order:\n\n"
            "1. Chemical compatibility with the fluid per the library matrix.\n"
            "2. Material temperature range.\n"
            "3. Sour service: if H₂S partial pressure exceeds 0.345 kPa (0.05 psia), it requires a "
            "NACE-accepted material with a hardness limit.\n"
            "4. Chlorides: above about 50 ppm and 60 °C it discards austenitics and moves to "
            "duplex or nickel alloys, because of stress corrosion cracking risk.\n"
            "5. Erosion: with high V/V_e it adds a Stellite tip and allowance."),
        "why": _MODE_LIMITS,
        "worked": (
            "Agua a 120 °C sin agentes: 316/316L sin recubrimiento. La misma agua con 200 ppm "
            "de cloruros: dúplex 2205, con la justificación «riesgo de corrosión bajo tensión "
            "en austeníticos».",
            "Water at 120 °C with no agents: 316/316L, no coating. The same water with "
            "200 ppm chlorides: duplex 2205, justified as «stress corrosion cracking risk in "
            "austenitics»."),
        "mistakes": ("- Dejar automático cuando la especificación del cliente fija el material.\n"
                     "- No cargar cloruros ni H₂S y confiar en la selección.",
                     "- Leaving automatic when the client spec fixes the material.\n"
                     "- Not entering chlorides or H₂S and trusting the selection."),
    },
    "f.mode_connection": {
        "essence": (
            "En automático, TS elige el tipo de conexión según el servicio (roscada para "
            "utilidades de baja exigencia, bridada para hidrocarburos y servicios peligrosos, "
            "sanitaria para alimentos), la clase de brida según la presión de diseño a la "
            "temperatura de diseño con la tabla B16.5, y la cara según la clase (RF hasta "
            "valores medios, RTJ en alta presión).",
            "In automatic, TS chooses connection type by service (threaded for low-demand "
            "utilities, flanged for hydrocarbons and hazardous services, sanitary for food), "
            "flange class by design pressure at design temperature with the B16.5 table, and "
            "face by class (RF up to medium values, RTJ at high pressure)."),
        "why": _MODE_LIMITS,
        "worked": (
            "Gas a 60 bar y 300 °C: la clase 300 admite ≈ 37 bar a esa temperatura, la 600 "
            "≈ 74 bar → bridada 1½\" clase 600 RF.",
            "Gas at 60 bar and 300 °C: class 300 holds ≈ 37 bar at that temperature, class "
            "600 ≈ 74 bar → flanged 1½\" class 600 RF."),
        "mistakes": ("- No revisar la clase frente a la especificación de cañería, que puede "
                     "exigir una mayor.",
                     "- Not checking the class against the piping spec, which may require a "
                     "higher one."),
    },
    "f.mode_geometry": {
        "essence": (
            "En automático, TS busca la vaina más simple que cumpla todo:\n\n"
            "1. Calcula la inmersión objetivo (un tercio a la mitad del diámetro, o 450 mm en "
            "recipientes).\n"
            "2. Elige el largo U normalizado más corto que la alcanza.\n"
            "3. Prueba perfiles en orden de preferencia (cónico, escalonado, recto) con "
            "diámetros típicos para la conexión.\n"
            "4. Si nada cumple, prueba largos más cortos, aceptando menos inmersión, y lo "
            "informa.",
            "In automatic, TS looks for the simplest well that passes everything:\n\n"
            "1. Computes target immersion (a third to a half of the diameter, or 450 mm in "
            "vessels).\n"
            "2. Picks the shortest standard U length that reaches it.\n"
            "3. Tries profiles in order of preference (tapered, stepped, straight) with "
            "typical diameters for the connection.\n"
            "4. If nothing passes, it tries shorter lengths, accepting less immersion, and "
            "reports it."),
        "why": _MODE_LIMITS,
        "worked": (
            "6\" en gas a 22 m/s: cónico 10½\" no cumple (r = 0,47), 7½\" tampoco por "
            "inmersión, largo especial de 210 mm cumple con r = 0,38.",
            "6\" in gas at 22 m/s: tapered 10½\" fails (r = 0.47), 7½\" fails on immersion, "
            "special 210 mm length passes with r = 0.38."),
        "mistakes": ("- Fijar U a mano y dejar el resto en automático esperando que cumpla.",
                     "- Fixing U by hand and leaving the rest automatic expecting a pass."),
    },
    "f.mode_sensor": {
        "essence": (
            "En automático, TS elige el diámetro de vaina del sensor que mejor ajusta en el "
            "agujero: 6,35 mm (¼\") o 6 mm para agujero 0,260\" (6,6 mm), y 9,5 mm (3/8\") u "
            "8 mm para 0,385\" (9,8 mm). El objetivo es el menor huelgo posible, porque el "
            "aire es el peor conductor en el camino del calor.",
            "In automatic, TS chooses the sensor sheath diameter that best fits the bore: "
            "6.35 mm (¼\") or 6 mm for a 0.260\" (6.6 mm) bore, and 9.5 mm (3/8\") or 8 mm for "
            "0.385\" (9.8 mm). The goal is the smallest gap possible, because air is the worst "
            "conductor in the heat path."),
        "why": _MODE_LIMITS,
        "worked": ("Agujero 6,6 mm → vaina de 6,35 mm (¼\"), huelgo 0,25 mm.",
                   "6.6 mm bore → 6.35 mm (¼\") sheath, 0.25 mm gap."),
        "mistakes": ("- Comprar el sensor antes de cerrar el agujero.",
                     "- Buying the sensor before fixing the bore."),
    },
    "f.value": {
        "essence": (
            "Es el número del caudal o la velocidad de cada caso, en la base elegida. TS lo "
            "convierte a velocidad media en la cañería:\n\n"
            "- Velocidad: se usa directa.\n"
            "- Másico: V = ṁ / (ρ·A).\n"
            "- Volumétrico real: V = Q / A.\n"
            "- Estándar: primero se pasa a másico con la densidad estándar y luego a "
            "velocidad con la densidad real.\n\n"
            "La velocidad media es una simplificación: en flujo turbulento el centro de la "
            "cañería va un 15 a 25 % más rápido que la media, y la punta de la vaina está "
            "cerca del centro.",
            "It is the flow or velocity number of each case, in the chosen basis. TS converts "
            "it to mean pipe velocity:\n\n"
            "- Velocity: used directly.\n"
            "- Mass: V = ṁ / (ρ·A).\n"
            "- Actual volumetric: V = Q / A.\n"
            "- Standard: first converted to mass with standard density, then to velocity "
            "with actual density.\n\n"
            "Mean velocity is a simplification: in turbulent flow the pipe centre runs 15 to "
            "25 % faster than the mean, and the well tip is near the centre."),
        "why": (
            "Es el dato que más influye en la estela (f_s ∝ V) y en la fuerza (∝ V²). Un "
            "error de unidad acá arruina todo el cálculo.",
            "It is the datum with the most influence on the wake (f_s ∝ V) and force (∝ V²). "
            "A unit error here ruins the whole calculation."),
        "worked": (
            "Base másica, 12 t/h de agua (ρ = 990 kg/m³) en 3\" Sch 40 (Di 77,9 mm, A = "
            "0,00477 m²): V = 12 000 / 3600 / 990 / 0,00477 = 0,71 m/s. Si se carga 12 kg/s por "
            "error (43,2 t/h), V sale 2,54 m/s: 3,6 veces más, y la fuerza 13 veces más.",
            "Mass basis, 12 t/h water (ρ = 990 kg/m³) in 3\" Sch 40 (ID 77.9 mm, A = "
            "0.00477 m²): V = 12,000 / 3600 / 990 / 0.00477 = 0.71 m/s. Entering 12 kg/s by "
            "mistake (43.2 t/h) gives 2.54 m/s: 3.6 times more, and 13 times the force."),
        "mistakes": (
            "- Cargar caudal estándar como real.\n"
            "- Confundir t/h con kg/h o kg/s.\n"
            "- Usar el caudal de diseño de la bomba y no el del punto de la vaina.",
            "- Entering standard flow as actual.\n"
            "- Confusing t/h with kg/h or kg/s.\n"
            "- Using pump design flow rather than flow at the well location."),
    },
    "f.case": {
        "essence": (
            "Es el nombre de cada condición de flujo. No entra en el cálculo, pero es lo que "
            "conecta cada fila del resultado con una situación real de operación. El informe "
            "dice «manda el caso X»: si X se llama «Caso 4», nadie sabe qué significa en la "
            "planta; si se llama «Máximo con by-pass abierto», el operador sabe qué evitar.",
            "It is the name of each flow condition. It does not enter the calculation, but it "
            "connects each result row with a real operating situation. The report says «case "
            "X governs»: if X is «Case 4», nobody in the plant knows what that means; if it is "
            "«Maximum with by-pass open», the operator knows what to avoid."),
        "why": (
            "Hace legible el resultado y deja trazabilidad con el balance de masa y energía "
            "del que salieron los datos.",
            "It makes the result readable and keeps traceability to the heat and mass "
            "balance the data came from."),
        "worked": (
            "«Mínimo (turndown 30 %)», «Normal (HMB rev. C)», «Máximo (110 % diseño)», "
            "«Arranque con N₂». Si manda el arranque con nitrógeno, la solución puede ser un "
            "procedimiento y no una vaina nueva.",
            "«Minimum (30 % turndown)», «Normal (HMB rev. C)», «Maximum (110 % design)», "
            "«Start-up with N₂». If the nitrogen start-up governs, the fix may be a procedure "
            "rather than a new well."),
        "mistakes": ("- Usar nombres genéricos sin referencia al documento de origen.",
                     "- Using generic names without reference to the source document."),
    },
    "f.basis": {
        "mistakes": (
            "- Elegir «volumétrico real» y cargar Sm³/h del balance de masa: en gas a 50 bar "
            "la velocidad sale unas 50 veces mayor.\n"
            "- Elegir «másico» y cargar kg/s en un campo que espera kg/h.\n"
            "- En vapor húmedo o mezclas, usar la densidad del líquido con un caudal de "
            "vapor.",
            "- Choosing «actual volumetric» and entering Sm³/h from the heat and mass "
            "balance: in gas at 50 bar velocity comes out about 50 times too high.\n"
            "- Choosing «mass» and entering kg/s in a field expecting kg/h.\n"
            "- In wet steam or mixtures, using liquid density with a vapour flow."),
    },
    "f.wall": {
        "worked": (
            "Hs = 150 mm, pared 18 mm, U = 250 mm → inmersión = 250 − 150 − 18 = 82 mm.\n\n"
            "Misma vaina en un recipiente con pared de 60 mm: inmersión = 40 mm, menos de la "
            "mitad. Además, en 6\" Sch 40 (7,1 mm) y Sch 160 (18,3 mm) el Di pasa de 154 a "
            "131,8 mm: a igual caudal la velocidad sube un 37 %.",
            "Hs = 150 mm, wall 18 mm, U = 250 mm → immersion = 250 − 150 − 18 = 82 mm.\n\n"
            "The same well on a vessel with a 60 mm wall: immersion = 40 mm, less than half. "
            "Also, in 6\" Sch 40 (7.1 mm) and Sch 160 (18.3 mm) ID goes from 154 to 131.8 mm: "
            "at equal flow velocity rises 37 %."),
        "mistakes": (
            "- Olvidar la pared de un recipiente (puede tener 30 a 80 mm).\n"
            "- Usar el espesor nominal de un schedule distinto del real de la línea.\n"
            "- No restar el sobreespesor de corrosión de la cañería al evaluar fin de vida.",
            "- Forgetting a vessel wall (it may be 30 to 80 mm).\n"
            "- Using the nominal thickness of a schedule different from the actual line.\n"
            "- Not accounting for pipe corrosion allowance when evaluating end of life."),
    },
    "f.insulation": {
        "mistakes": (
            "- Pedir lag cero en líneas calientes aisladas.\n"
            "- Olvidar el aislamiento en líneas frías: el cabezal se escarcha, entra humedad y "
            "la medición deriva.\n"
            "- Cargar el espesor sin el revestimiento metálico exterior (unos 5 a 10 mm "
            "más).",
            "- Asking for zero lag on hot insulated lines.\n"
            "- Forgetting insulation on cold lines: the head frosts, moisture gets in and the "
            "reading drifts.\n"
            "- Entering thickness without the outer metal jacketing (about 5 to 10 mm "
            "more)."),
    },
}
