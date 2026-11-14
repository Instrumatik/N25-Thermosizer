"""Profundidad de las fichas de resultados (r.*)."""

from __future__ import annotations

from typing import Any

DEEP: dict[str, dict[str, Any]] = {
    "r.q_actual": {
        "essence": (
            "Un gas se comprime: el mismo kilogramo ocupa menos volumen a más presión y más "
            "volumen a más temperatura. Por eso un caudal «estándar» (a 15 °C y 1 atm) no dice "
            "qué volumen pasa de verdad por la cañería. El caudal real es el volumen que circula "
            "en las condiciones de operación, y es el que fija la velocidad que golpea la vaina."
            "\n\n"
            "Para líquidos casi no hay diferencia, porque su densidad apenas cambia con la "
            "presión; para gases la diferencia puede ser de 10 a 100 veces.",
            "A gas compresses: the same kilogram takes less volume at higher pressure and more "
            "volume at higher temperature. That is why a «standard» flow (at 15 °C and 1 atm) "
            "does not tell what volume really flows in the pipe. The actual flow is the volume "
            "moving at operating conditions, and it is what sets the velocity hitting the well."
            "\n\n"
            "For liquids there is hardly any difference, because their density barely changes "
            "with pressure; for gases the difference can be 10 to 100 times."),
        "why": (
            "Toda la verificación de vibración depende de la velocidad, y la velocidad sale del "
            "caudal real dividido por el área. Confundir caudal estándar con real en un gas a "
            "40 bar subestima la velocidad unas 40 veces y aprueba una vaina que se rompería.",
            "The whole vibration check depends on velocity, and velocity is actual flow divided "
            "by area. Mixing up standard and actual flow in a gas at 40 bar underestimates "
            "velocity about 40 times and passes a thermowell that would break."),
        "worked": (
            "Gas natural, 50 000 Sm³/h, a 41 bar abs y 30 °C, en cañería de 6\" Sch 40 "
            "(Di = 154,1 mm, área 0,01865 m²).\n\n"
            "1. Densidad estándar ≈ 0,68 kg/m³; densidad real ≈ 30 kg/m³ (TS la calcula con "
            "CoolProp).\n"
            "2. Caudal másico = 50 000 × 0,68 / 3600 = 9,44 kg/s.\n"
            "3. Caudal real = 9,44 / 30 = 0,315 m³/s = 1133 m³/h.\n"
            "4. Velocidad = 0,315 / 0,01865 = 16,9 m/s.\n\n"
            "Si se hubiera usado el caudal estándar como real: 13,9 m³/s y 745 m/s, un valor "
            "absurdo que muestra el tamaño del error.",
            "Natural gas, 50,000 Sm³/h, at 41 bar abs and 30 °C, in a 6\" Sch 40 pipe "
            "(ID = 154.1 mm, area 0.01865 m²).\n\n"
            "1. Standard density ≈ 0.68 kg/m³; actual density ≈ 30 kg/m³ (TS computes it with "
            "CoolProp).\n"
            "2. Mass flow = 50,000 × 0.68 / 3600 = 9.44 kg/s.\n"
            "3. Actual flow = 9.44 / 30 = 0.315 m³/s = 1133 m³/h.\n"
            "4. Velocity = 0.315 / 0.01865 = 16.9 m/s.\n\n"
            "Had the standard flow been used as actual: 13.9 m³/s and 745 m/s, an absurd value "
            "that shows the size of the error."),
        "mistakes": (
            "- Cargar Sm³/h o SCFM como caudal volumétrico real.\n"
            "- Confundir Nm³ (0 °C) con Sm³ (15 °C): un 5 % de diferencia.\n"
            "- Usar presión manométrica en vez de absoluta al corregir a mano.\n"
            "- Tomar el caudal de diseño del instrumento de caudal en vez del máximo de proceso.",
            "- Entering Sm³/h or SCFM as actual volume flow.\n"
            "- Confusing Nm³ (0 °C) with Sm³ (15 °C): a 5 % difference.\n"
            "- Using gauge instead of absolute pressure when correcting by hand.\n"
            "- Taking the flowmeter design flow instead of the process maximum."),
    },
    "r.velocity": {
        "essence": (
            "Es la velocidad promedio del fluido en la sección de la cañería: caudal real "
            "dividido por el área interna. El perfil real no es plano: en flujo turbulento el "
            "centro va cerca de un 20 % más rápido que el promedio y la pared está casi quieta. "
            "La vaina, que entra hacia el centro, ve la zona más rápida, y por eso la norma usa "
            "la velocidad media sin descuentos.\n\n"
            "El fluido que choca con el vástago transfiere su cantidad de movimiento: la "
            "presión dinámica ½·ρ·V² es la «fuerza por área» del viento sobre la vaina.",
            "It is the average fluid velocity over the pipe section: actual flow divided by "
            "inside area. The real profile is not flat: in turbulent flow the centre runs about "
            "20 % faster than the average and the wall is almost still. The thermowell, reaching "
            "towards the centre, sees the fastest zone, which is why the standard uses the mean "
            "velocity without discounts.\n\n"
            "Fluid striking the shank transfers its momentum: the dynamic pressure ½·ρ·V² is the "
            "«force per area» of the wind on the well."),
        "why": (
            "La velocidad aparece dos veces: la frecuencia de estela crece en proporción a V y "
            "las fuerzas crecen con V². Duplicar la velocidad duplica la frecuencia y cuadruplica "
            "el esfuerzo. Es el dato de proceso que más decide si la vaina cumple.",
            "Velocity appears twice: wake frequency grows in proportion to V and forces grow "
            "with V². Doubling velocity doubles frequency and quadruples stress. It is the "
            "process datum that most decides whether the well passes."),
        "worked": (
            "Agua a 80 °C (ρ = 972 kg/m³), 120 m³/h en 4\" Sch 40 (Di = 102,3 mm).\n\n"
            "1. Área = π × 0,1023² / 4 = 0,00822 m².\n"
            "2. V = (120 / 3600) / 0,00822 = 4,06 m/s.\n"
            "3. Presión dinámica = ½ × 972 × 4,06² = 8010 Pa.\n\n"
            "Si el caudal sube a 180 m³/h, V = 6,1 m/s y la presión dinámica pasa a 18 000 Pa: "
            "un 50 % más de caudal da un 125 % más de carga.",
            "Water at 80 °C (ρ = 972 kg/m³), 120 m³/h in 4\" Sch 40 (ID = 102.3 mm).\n\n"
            "1. Area = π × 0.1023² / 4 = 0.00822 m².\n"
            "2. V = (120 / 3600) / 0.00822 = 4.06 m/s.\n"
            "3. Dynamic pressure = ½ × 972 × 4.06² = 8010 Pa.\n\n"
            "If flow rises to 180 m³/h, V = 6.1 m/s and the dynamic pressure becomes 18,000 Pa: "
            "50 % more flow gives 125 % more load."),
        "mistakes": (
            "- Verificar solo el caso normal: el máximo o un arranque con válvula abierta suele "
            "mandar.\n"
            "- Usar el diámetro nominal en vez del interno (en 2\" Sch 160 la diferencia de "
            "área es del 40 %).\n"
            "- Olvidar que en un codo o reducción la velocidad local puede ser mayor.\n"
            "- En gases, calcular V con densidad estándar.",
            "- Checking only the normal case: the maximum or a start-up with an open valve "
            "usually governs.\n"
            "- Using nominal instead of inside diameter (in 2\" Sch 160 the area differs by "
            "40 %).\n"
            "- Forgetting that local velocity may be higher in an elbow or reducer.\n"
            "- In gases, computing V with standard density."),
    },
    "r.ve": {
        "essence": (
            "La erosión es desgaste mecánico: el fluido arranca material de la superficie, "
            "sobre todo cuando arrastra gotas, burbujas que colapsan o partículas sólidas. "
            "En metales que se protegen con una capa de óxido (inoxidables, aceros al carbono "
            "en agua) el flujo rápido barre esa capa y el metal queda expuesto a corroerse otra "
            "vez: es la erosión-corrosión, que avanza mucho más rápido que cada fenómeno solo."
            "\n\n"
            "La fórmula empírica de API RP 14E (V_e = C/√ρ) dice que un fluido más denso tolera "
            "menos velocidad, porque su impacto lleva más energía por unidad de volumen.",
            "Erosion is mechanical wear: the fluid tears material from the surface, especially "
            "when it carries droplets, collapsing bubbles or solid particles. In metals "
            "protected by an oxide film (stainless, carbon steel in water) fast flow sweeps that "
            "film away and the bare metal corrodes again: this is erosion-corrosion, much faster "
            "than either mechanism alone.\n\n"
            "The empirical API RP 14E formula (V_e = C/√ρ) says a denser fluid tolerates less "
            "velocity, because its impact carries more energy per unit volume."),
        "why": (
            "La vaina es la pieza que más recibe el impacto del flujo, y su punta es delgada. "
            "Una pérdida de 1 mm en la pared de la punta puede llevar a una perforación: el "
            "fluido entra al sensor y la medición se pierde, o peor, hay fuga a la atmósfera "
            "por el cabezal. Además, una punta adelgazada cambia la frecuencia natural.",
            "The thermowell is the part that takes the most flow impact, and its tip is thin. "
            "Losing 1 mm of tip wall can lead to a perforation: fluid reaches the sensor and "
            "the reading is lost, or worse, there is a leak to atmosphere through the head. A "
            "thinned tip also changes the natural frequency."),
        "worked": (
            "Gas húmedo a 30 kg/m³ (1,87 lb/ft³), sin sólidos, C = 100.\n\n"
            "1. V_e = 100 / √1,87 = 73 ft/s = 22,3 m/s.\n"
            "2. Con V = 16,9 m/s, V/V_e = 0,76: zona «vigilar».\n\n"
            "Agua a 972 kg/m³ (60,7 lb/ft³): V_e = 100 / √60,7 = 12,8 ft/s = 3,9 m/s. Con "
            "4,06 m/s, V/V_e = 1,04: «erosivo». En agua limpia el criterio es conservador; con "
            "arena o cavitación es real.",
            "Wet gas at 30 kg/m³ (1.87 lb/ft³), no solids, C = 100.\n\n"
            "1. V_e = 100 / √1.87 = 73 ft/s = 22.3 m/s.\n"
            "2. With V = 16.9 m/s, V/V_e = 0.76: «watch» zone.\n\n"
            "Water at 972 kg/m³ (60.7 lb/ft³): V_e = 100 / √60.7 = 12.8 ft/s = 3.9 m/s. With "
            "4.06 m/s, V/V_e = 1.04: «erosive». In clean water the criterion is conservative; "
            "with sand or cavitation it is real."),
        "mistakes": (
            "- Tomar V_e como límite de la norma de termopozos: es una guía de API para "
            "cañerías, orientativa.\n"
            "- Usar C = 100 con sólidos: con arena el valor práctico es mucho menor.\n"
            "- Ignorar la erosión porque la vaina «cumple ASME»: son verificaciones "
            "independientes.\n"
            "- No sumar sobreespesor de corrosión cuando la relación está cerca de 1.",
            "- Taking V_e as a thermowell standard limit: it is an API piping guide, "
            "indicative.\n"
            "- Using C = 100 with solids: with sand the practical value is much lower.\n"
            "- Ignoring erosion because the well «passes ASME»: they are independent checks.\n"
            "- Not adding a corrosion allowance when the ratio is close to 1."),
    },
    "r.v_ve": {
        "essence": (
            "Es la velocidad real expresada como fracción de la velocidad erosional. Funciona "
            "como un semáforo: por debajo de 0,7 hay margen, entre 0,7 y 1 el desgaste puede "
            "aparecer con el tiempo y por encima de 1 se espera desgaste activo.",
            "It is the actual velocity expressed as a fraction of the erosional velocity. It "
            "works like a traffic light: below 0.7 there is margin, between 0.7 and 1 wear may "
            "appear over time and above 1 active wear is expected."),
        "why": (
            "Resume en un número si hace falta proteger la vaina: material más duro, "
            "recubrimiento de Stellite en la punta, sobreespesor o inspecciones periódicas. "
            "Decidirlo en el diseño cuesta poco; descubrirlo con una fuga cuesta una parada.",
            "It sums up in one number whether the well needs protection: harder material, "
            "Stellite tip overlay, allowance or periodic inspections. Deciding it at design "
            "costs little; finding out through a leak costs a shutdown."),
        "worked": (
            "V = 16,9 m/s y V_e = 22,3 m/s → V/V_e = 0,76 (vigilar).\n\n"
            "Opciones: aceptar con inspección anual de la punta, o agregar 1,5 mm de "
            "sobreespesor. TS recalcula la vaina con el sobreespesor consumido para verificar "
            "que siga cumpliendo al final de su vida.",
            "V = 16.9 m/s and V_e = 22.3 m/s → V/V_e = 0.76 (watch).\n\n"
            "Options: accept with yearly tip inspection, or add a 1.5 mm allowance. TS "
            "re-checks the well with the allowance consumed to verify it still passes at the "
            "end of its life."),
        "mistakes": (
            "- Mirar solo el caso normal: la erosión acumula durante todo el tiempo a alta "
            "velocidad.\n"
            "- Suponer que el inoxidable no se erosiona: resiste la corrosión, no el impacto.\n"
            "- Poner Stellite sin verificar compatibilidad con el fluido y la temperatura.",
            "- Looking only at the normal case: erosion accumulates over all the time at high "
            "velocity.\n"
            "- Assuming stainless does not erode: it resists corrosion, not impact.\n"
            "- Applying Stellite without checking compatibility with fluid and temperature."),
    },
    "r.reynolds": {
        "essence": (
            "Compara dos tendencias del fluido: la inercia, que lo hace seguir de largo y "
            "formar remolinos (ρ·V·B), y la viscosidad, que lo frena y lo mantiene ordenado (μ). "
            "Con Re bajo dominan las fuerzas viscosas y el flujo rodea el cilindro sin "
            "despegarse; al crecer Re aparecen los remolinos alternados, y a Re muy alto la capa "
            "límite se vuelve turbulenta, se despega más atrás y la estela se angosta (la "
            "«crisis de arrastre», entre 2·10⁵ y 3·10⁶ aproximadamente).\n\n"
            "A nivel molecular, la viscosidad es la transferencia de cantidad de movimiento "
            "entre capas de fluido por choques entre moléculas; por eso en gases aumenta con la "
            "temperatura y en líquidos disminuye.",
            "It compares two tendencies of the fluid: inertia, which makes it carry on and form "
            "eddies (ρ·V·B), and viscosity, which slows it and keeps it orderly (μ). At low Re "
            "viscous forces dominate and the flow goes round the cylinder without separating; "
            "as Re grows alternating eddies appear, and at very high Re the boundary layer turns "
            "turbulent, separates further back and the wake narrows (the «drag crisis», roughly "
            "between 2·10⁵ and 3·10⁶).\n\n"
            "At molecular level viscosity is the transfer of momentum between fluid layers by "
            "molecular collisions; that is why it rises with temperature in gases and falls in "
            "liquids."),
        "why": (
            "El número de Strouhal, y con él la frecuencia de estela, depende del régimen de "
            "Reynolds. Además define si hay desprendimiento de vórtices: con Re muy bajo "
            "(fluidos muy viscosos y lentos) no hay vibración por estela.",
            "The Strouhal number, and with it the wake frequency, depends on the Reynolds "
            "regime. It also defines whether there is vortex shedding: at very low Re (very "
            "viscous, slow fluids) there is no wake vibration."),
        "worked": (
            "Agua a 80 °C: ρ = 972 kg/m³, μ = 0,355 mPa·s, V = 4,06 m/s, B = 19,05 mm.\n\n"
            "Re = 972 × 4,06 × 0,01905 / 0,000355 = 2,1·10⁵: en el borde de la crisis de "
            "arrastre.\n\n"
            "Aceite pesado a 40 °C: ρ = 900, μ = 0,2 Pa·s, V = 1 m/s → Re = 86: hay vórtices, "
            "pero débiles y de baja frecuencia.",
            "Water at 80 °C: ρ = 972 kg/m³, μ = 0.355 mPa·s, V = 4.06 m/s, B = 19.05 mm.\n\n"
            "Re = 972 × 4.06 × 0.01905 / 0.000355 = 2.1·10⁵: at the edge of the drag "
            "crisis.\n\n"
            "Heavy oil at 40 °C: ρ = 900, μ = 0.2 Pa·s, V = 1 m/s → Re = 86: there are "
            "vortices, but weak and low in frequency."),
        "mistakes": (
            "- Usar el diámetro de la cañería como longitud: para la vaina se usa B.\n"
            "- Confundir viscosidad dinámica (Pa·s) con cinemática (m²/s o cSt).\n"
            "- Usar la viscosidad a 20 °C para un fluido a 200 °C: puede cambiar 10 veces.",
            "- Using the pipe diameter as length: for the well B is used.\n"
            "- Confusing dynamic viscosity (Pa·s) with kinematic (m²/s or cSt).\n"
            "- Using viscosity at 20 °C for a fluid at 200 °C: it can change tenfold."),
    },
    "r.strouhal": {
        "essence": (
            "Es la «cadencia» de la estela: cuántos remolinos se sueltan mientras el fluido "
            "avanza un diámetro. Con N_S = 0,2, cada remolino se desprende cada 5 diámetros "
            "recorridos. Es casi constante en un rango enorme de Reynolds porque la geometría de "
            "la estela (separación entre filas de remolinos) se mantiene parecida; cambia cuando "
            "la capa límite pasa de laminar a turbulenta y la estela se angosta.",
            "It is the «cadence» of the wake: how many eddies are shed while the fluid moves "
            "one diameter. With N_S = 0.2, one eddy is shed every 5 diameters travelled. It is "
            "nearly constant over a huge Reynolds range because the wake geometry (spacing "
            "between eddy rows) stays similar; it changes when the boundary layer turns from "
            "laminar to turbulent and the wake narrows."),
        "why": (
            "Un error del 10 % en N_S es un error del 10 % en la frecuencia de estela, que "
            "puede mover la relación r de 0,75 a 0,83 y pasar de cumplir a no cumplir. Por eso "
            "TS usa la correlación de la norma en función de Re y no un valor fijo.",
            "A 10 % error in N_S is a 10 % error in wake frequency, which can move the ratio r "
            "from 0.75 to 0.83 and turn a pass into a fail. That is why TS uses the standard's "
            "Re correlation instead of a fixed value."),
        "worked": (
            "Re = 2,1·10⁵ → N_S ≈ 0,21 (correlación). Con V = 4,06 m/s y B = 19,05 mm:\n\n"
            "f_s = 0,21 × 4,06 / 0,01905 = 44,8 Hz.\n\n"
            "Con 0,22 fijo daría 46,9 Hz: casi 5 % más, del lado seguro.",
            "Re = 2.1·10⁵ → N_S ≈ 0.21 (correlation). With V = 4.06 m/s and B = 19.05 mm:\n\n"
            "f_s = 0.21 × 4.06 / 0.01905 = 44.8 Hz.\n\n"
            "With a fixed 0.22 it would be 46.9 Hz: almost 5 % more, on the safe side."),
        "mistakes": (
            "- Suponer 0,22 siempre: en la crisis de arrastre puede ser mayor.\n"
            "- Confundir el Strouhal de un cilindro con el de otras formas (placas, perfiles).\n"
            "- Creer que la superficie rugosa no influye: adelanta la transición turbulenta.",
            "- Assuming 0.22 always: in the drag crisis it can be higher.\n"
            "- Confusing a cylinder's Strouhal with that of other shapes (plates, profiles).\n"
            "- Believing surface roughness does not matter: it brings the turbulent transition "
            "forward."),
    },
    "r.fs": {
        "essence": (
            "Cuando un fluido rodea un cilindro, se acelera por los costados y la presión baja; "
            "detrás tiene que frenarse contra una presión que sube. La capa pegada a la pared "
            "(capa límite) no tiene energía para remontar esa subida y se despega. Las dos "
            "láminas despegadas se enrollan y forman remolinos.\n\n"
            "Los remolinos se sueltan alternados, uno de cada lado, en una fila en zigzag (la "
            "calle de vórtices de von Kármán). Cada vez que se suelta uno, la circulación "
            "alrededor del cilindro cambia de signo y aparece una fuerza lateral que alterna de "
            "lado, la misma física que da sustentación a un ala:\n\n"
            "- Fuerza transversal (lift): perpendicular al flujo, a la frecuencia f_s. Es la "
            "más grande.\n"
            "- Fuerza en línea (drag oscilante): en la dirección del flujo, a 2·f_s, porque "
            "cada remolino, sea de arriba o de abajo, tira hacia atrás. Es unas diez veces más "
            "chica, pero excita la vaina a una frecuencia más alta.\n\n"
            "Es el mismo fenómeno que hace «cantar» los cables con viento.",
            "When a fluid flows round a cylinder it speeds up along the sides and pressure "
            "drops; behind it must slow down against rising pressure. The layer stuck to the "
            "wall (boundary layer) lacks the energy to climb that rise and separates. The two "
            "separated sheets roll up into eddies.\n\n"
            "The eddies are shed alternately, one from each side, in a zigzag row (the von "
            "Kármán vortex street). Each time one is shed the circulation around the cylinder "
            "changes sign and a side force appears that alternates, the same physics that lifts "
            "a wing:\n\n"
            "- Transverse force (lift): perpendicular to the flow, at frequency f_s. It is the "
            "largest.\n"
            "- In-line force (oscillating drag): along the flow, at 2·f_s, because each eddy, "
            "top or bottom, pulls backwards. It is about ten times smaller, but excites the "
            "well at a higher frequency.\n\n"
            "It is the same phenomenon that makes wires «sing» in the wind."),
        "why": (
            "La vaina es un voladizo con su propia frecuencia natural. Si la estela la empuja "
            "a un ritmo cercano, entra en resonancia: cada empujón llega en el momento justo y "
            "la amplitud crece hasta que el material se fatiga y la vaina se corta en la raíz, "
            "en horas o días. A 300 Hz la raíz soporta 26 millones de ciclos por día. El trozo "
            "suelto viaja hacia bombas, válvulas o turbinas y el fluido sale por la conexión."
            "\n\n"
            "Un caso conocido es la fuga de sodio del reactor Monju (Japón, 1995): una "
            "termovaina se rompió por vibración en línea, un modo que la versión anterior de la "
            "norma no evaluaba. La edición 2016 incorpora esa verificación.\n\n"
            "Lock-in: cerca de la resonancia, el movimiento de la vaina ordena el "
            "desprendimiento y lo engancha a su frecuencia natural en un rango de velocidades. "
            "Por eso no alcanza con quedar apenas por debajo: hace falta margen.",
            "The thermowell is a cantilever with its own natural frequency. If the wake pushes "
            "it at a nearby rate it resonates: each push arrives at the right moment and the "
            "amplitude grows until the material fatigues and the well snaps at the root, in "
            "hours or days. At 300 Hz the root takes 26 million cycles a day. The loose piece "
            "travels to pumps, valves or turbines and the fluid escapes through the "
            "connection.\n\n"
            "A well-known case is the sodium leak at the Monju reactor (Japan, 1995): a "
            "thermowell broke from in-line vibration, a mode the previous edition of the "
            "standard did not assess. The 2016 edition adds that check.\n\n"
            "Lock-in: near resonance the well's own motion organizes the shedding and locks it "
            "to the natural frequency over a velocity range. That is why being just below is "
            "not enough: margin is needed."),
        "worked": (
            "Gas natural a 25 m/s y 40 kg/m³, punta B = 19,05 mm, agujero d = 6,6 mm, "
            "f_n,c = 420 Hz, ζ = 0,0005, acero 8000 kg/m³.\n\n"
            "1. f_s = 0,22 × 25 / 0,01905 = 289 Hz.\n"
            "2. r = 289 / 420 = 0,69: zona condicional.\n"
            "3. N_Sc = (π²/2) × 0,0005 × (8000/40) × [1 − (6,6/19,05)²] = 0,43 < 2,5: el gas es "
            "demasiado liviano para amortiguar la vibración en línea.\n"
            "4. Rige r < 0,4: no cumple.\n"
            "5. f_s máx = 0,4 × 420 = 168 Hz → V máx = 168 × 0,01905 / 0,22 ≈ 14,5 m/s. Con "
            "25 m/s hay que acortar o rigidizar la vaina.",
            "Natural gas at 25 m/s and 40 kg/m³, tip B = 19.05 mm, bore d = 6.6 mm, "
            "f_n,c = 420 Hz, ζ = 0.0005, steel 8000 kg/m³.\n\n"
            "1. f_s = 0.22 × 25 / 0.01905 = 289 Hz.\n"
            "2. r = 289 / 420 = 0.69: conditional zone.\n"
            "3. N_Sc = (π²/2) × 0.0005 × (8000/40) × [1 − (6.6/19.05)²] = 0.43 < 2.5: the gas "
            "is too light to damp in-line vibration.\n"
            "4. r < 0.4 governs: fail.\n"
            "5. Max f_s = 0.4 × 420 = 168 Hz → max V = 168 × 0.01905 / 0.22 ≈ 14.5 m/s. At "
            "25 m/s the well must be shortened or stiffened."),
        "mistakes": (
            "- Verificar solo el caudal normal: el máximo o un arranque que pasa por la "
            "resonancia suele mandar.\n"
            "- Usar la frecuencia empotrada f_n en vez de la montada f_n,c.\n"
            "- Suponer que un líquido lento es seguro: es más denso y empuja más fuerte.\n"
            "- Creer que basta con quedar un poco por debajo de la resonancia: el lock-in "
            "amplía la zona peligrosa.\n"
            "- Olvidar la zona protegida L0 dentro del niple: sin declararla se sobrestima la "
            "carga.",
            "- Checking only normal flow: the maximum or a start-up passing through resonance "
            "usually governs.\n"
            "- Using the fixed-base f_n instead of the installed f_n,c.\n"
            "- Assuming a slow liquid is safe: it is denser and pushes harder.\n"
            "- Believing being slightly below resonance is enough: lock-in widens the danger "
            "zone.\n"
            "- Forgetting the shielded length L0 inside the nozzle: undeclared, the load is "
            "overestimated."),
        "interpret": (
            "Mirá siempre r = f_s/f_n,c, no f_s sola: 300 Hz puede ser seguro en una vaina "
            "corta y gruesa (f_n,c de 1500 Hz) y destructivo en una larga y fina.",
            "Always look at r = f_s/f_n,c, not f_s alone: 300 Hz may be safe in a short thick "
            "well (f_n,c of 1500 Hz) and destructive in a long thin one."),
        "actions": (
            "Si no cumple, de más a menos efectivo:\n\n"
            "1. Acortar U: la frecuencia natural crece con 1/L², un 20 % menos de largo la sube "
            "cerca de un 55 %.\n"
            "2. Engrosar la raíz A o pasar a cónico o escalonado.\n"
            "3. Agrandar B: baja f_s, pero empeora la respuesta térmica.\n"
            "4. Collar de apoyo en la conexión.",
            "If it fails, from most to least effective:\n\n"
            "1. Shorten U: natural frequency grows with 1/L², 20 % shorter raises it about "
            "55 %.\n"
            "2. Thicken the root A or go tapered or stepped.\n"
            "3. Enlarge B: lowers f_s, but worsens thermal response.\n"
            "4. Support collar at the connection."),
    },
    "r.fn": {
        "essence": (
            "Toda estructura elástica tiene frecuencias a las que «prefiere» vibrar, igual "
            "que una regla apretada en el borde de una mesa: si la golpeás, oscila siempre al "
            "mismo ritmo. Ese ritmo sale del equilibrio entre rigidez (que la devuelve a su "
            "lugar) y masa (que por inercia la hace pasarse). Más rigidez, frecuencia más alta; "
            "más masa, más baja.\n\n"
            "Para un voladizo, la rigidez cae con el cubo del largo y la masa crece con el "
            "largo, así que la frecuencia cae con el cuadrado del largo: f_n ∝ (1/L²)·√(E·I/m). "
            "TS corrige además por la masa del fluido que la vaina arrastra al moverse (masa "
            "añadida) y por la masa del sensor.",
            "Every elastic structure has frequencies at which it «prefers» to vibrate, like a "
            "ruler pressed at the edge of a table: strike it and it always oscillates at the "
            "same rate. That rate comes from the balance between stiffness (which pulls it back) "
            "and mass (whose inertia makes it overshoot). More stiffness, higher frequency; more "
            "mass, lower.\n\n"
            "For a cantilever stiffness falls with the cube of length and mass grows with "
            "length, so frequency falls with the square of length: f_n ∝ (1/L²)·√(E·I/m). TS "
            "also corrects for the fluid mass the well drags when moving (added mass) and for "
            "the sensor mass."),
        "why": (
            "Es la mitad de la comparación de resonancia. Una vaina con frecuencia natural "
            "alta deja margen frente a la estela; una baja queda expuesta. El largo es la "
            "palanca más fuerte: cambia con el cuadrado.",
            "It is half of the resonance comparison. A well with high natural frequency leaves "
            "margin against the wake; a low one is exposed. Length is the strongest lever: it "
            "acts squared."),
        "worked": (
            "Vaina cónica de 316, L = 250 mm, f_n = 520 Hz.\n\n"
            "- Con L = 200 mm: f_n ≈ 520 × (250/200)² = 812 Hz.\n"
            "- Con L = 300 mm: f_n ≈ 520 × (250/300)² = 361 Hz.\n\n"
            "Un cambio de ±20 % en el largo mueve la frecuencia entre −31 % y +56 %.",
            "Tapered 316 well, L = 250 mm, f_n = 520 Hz.\n\n"
            "- With L = 200 mm: f_n ≈ 520 × (250/200)² = 812 Hz.\n"
            "- With L = 300 mm: f_n ≈ 520 × (250/300)² = 361 Hz.\n\n"
            "A ±20 % change in length moves frequency between −31 % and +56 %."),
        "mistakes": (
            "- Comparar la estela con f_n en vez de f_n,c (la montada es más baja).\n"
            "- Olvidar la masa añadida en líquidos densos: baja la frecuencia unos puntos.\n"
            "- Usar E a temperatura ambiente para una vaina a 400 °C: E cae y f_n también.",
            "- Comparing the wake with f_n instead of f_n,c (the installed one is lower).\n"
            "- Forgetting added mass in dense liquids: it lowers frequency a few points.\n"
            "- Using room-temperature E for a well at 400 °C: E drops and so does f_n."),
    },
    "r.hc": {
        "essence": (
            "Las fórmulas de frecuencia suponen una vaina empotrada en una pared infinitamente "
            "rígida. En la realidad la base se deforma un poco: la brida flexiona, la rosca "
            "tiene juego, la pared de la cañería cede. Ese apoyo «blando» actúa como un resorte "
            "en serie y baja la frecuencia. H_c es el factor que descuenta ese efecto.",
            "Frequency formulas assume a well clamped in an infinitely rigid wall. In reality "
            "the base deforms slightly: the flange bends, the thread has play, the pipe wall "
            "yields. That «soft» support acts as a series spring and lowers the frequency. H_c "
            "is the factor that discounts this effect."),
        "why": (
            "Ignorar la flexibilidad del apoyo da una frecuencia optimista y puede aprobar una "
            "vaina que en campo resuena. Las roscadas son las más afectadas, por eso tienen un "
            "factor menor.",
            "Ignoring support flexibility gives an optimistic frequency and may pass a well "
            "that resonates in the field. Threaded wells are the most affected, which is why "
            "they get a lower factor."),
        "worked": (
            "f_n = 520 Hz, bridada: H_c ≈ 0,93 → f_n,c = 484 Hz.\n\n"
            "La misma vaina roscada: H_c ≈ 0,85 → f_n,c = 442 Hz. La rosca sola quita un 9 % de "
            "frecuencia.",
            "f_n = 520 Hz, flanged: H_c ≈ 0.93 → f_n,c = 484 Hz.\n\n"
            "The same well threaded: H_c ≈ 0.85 → f_n,c = 442 Hz. The thread alone removes 9 % "
            "of frequency."),
        "mistakes": (
            "- Tomar H_c = 1 «porque la brida es rígida».\n"
            "- Suponer que una cupla soldada larga se comporta como una brida: agrega "
            "flexibilidad.",
            "- Taking H_c = 1 «because the flange is rigid».\n"
            "- Assuming a long welded coupling behaves like a flange: it adds flexibility."),
    },
    "r.fnc": {
        "essence": (
            "Es la frecuencia natural real de la vaina instalada: la teórica corregida por la "
            "masa del fluido, la del sensor y la flexibilidad del apoyo. Es el «tono» al que "
            "vibraría si se la golpeara ya montada en la línea.",
            "It is the real natural frequency of the installed well: the theoretical one "
            "corrected for fluid mass, sensor mass and support flexibility. It is the «tone» it "
            "would ring at if struck once mounted in the line."),
        "why": (
            "Es la referencia contra la que se compara la estela. Si la estela se acerca a "
            "f_n,c hay resonancia transversal; si se acerca a la mitad, resonancia en línea.",
            "It is the reference against which the wake is compared. If the wake approaches "
            "f_n,c there is transverse resonance; if it approaches half of it, in-line "
            "resonance."),
        "worked": (
            "f_n = 520 Hz y H_c = 0,93 → f_n,c = 484 Hz.\n\n"
            "- Resonancia transversal a f_s = 484 Hz.\n"
            "- Resonancia en línea a f_s = 242 Hz.\n"
            "- Con N_Sc < 2,5 la estela debe quedar por debajo de 0,4 × 484 = 194 Hz.",
            "f_n = 520 Hz and H_c = 0.93 → f_n,c = 484 Hz.\n\n"
            "- Transverse resonance at f_s = 484 Hz.\n"
            "- In-line resonance at f_s = 242 Hz.\n"
            "- With N_Sc < 2.5 the wake must stay below 0.4 × 484 = 194 Hz."),
        "mistakes": (
            "- Usar fórmulas aproximadas tipo 500/L² de planillas antiguas.\n"
            "- No actualizar la frecuencia cuando cambia el material o la temperatura.",
            "- Using approximate formulas like 500/L² from old spreadsheets.\n"
            "- Not updating frequency when material or temperature changes."),
    },
    "r.scruton": {
        "essence": (
            "Mide cuánto le cuesta al fluido sostener una vibración. Combina dos cosas: el "
            "amortiguamiento propio del metal y del apoyo (ζ, cuánta energía se pierde por "
            "ciclo como calor) y la relación entre la masa de la vaina y la del fluido que la "
            "rodea. Una vaina pesada y bien amortiguada en un gas liviano tiene Scruton alto; el "
            "fluido no logra «organizar» la vibración. Una vaina en un líquido denso tiene "
            "Scruton bajo: el fluido pesa casi tanto como ella y la puede arrastrar.",
            "It measures how hard it is for the fluid to sustain a vibration. It combines two "
            "things: the metal and support damping (ζ, how much energy is lost per cycle as "
            "heat) and the ratio between the well's mass and that of the surrounding fluid. A "
            "heavy, well-damped well in a light gas has a high Scruton number; the fluid cannot "
            "«organize» the vibration. A well in a dense liquid has a low Scruton: the fluid "
            "weighs almost as much as the well and can carry it along."),
        "why": (
            "Decide qué límite de frecuencia se aplica. Con N_Sc ≥ 2,5 la vibración en línea se "
            "considera suprimida y se puede trabajar hasta r < 0,8; con menos, la vaina debe "
            "quedar por debajo de la resonancia en línea (r < 0,4). Con N_Sc > 64 prácticamente "
            "no hay vibración por estela.",
            "It decides which frequency limit applies. With N_Sc ≥ 2.5 in-line vibration is "
            "considered suppressed and r < 0.8 is allowed; below that the well must stay under "
            "in-line resonance (r < 0.4). With N_Sc > 64 there is practically no wake "
            "vibration."),
        "worked": (
            "Acero 8000 kg/m³, ζ = 0,0005, B = 19,05 mm, d = 6,6 mm → factor geométrico 0,88.\n"
            "\n"
            "- Gas a 40 kg/m³: N_Sc = 4,93 × 0,0005 × 200 × 0,88 = 0,43.\n"
            "- Gas a 5 kg/m³: N_Sc = 4,93 × 0,0005 × 1600 × 0,88 = 3,5 ≥ 2,5.\n"
            "- Agua a 1000 kg/m³: N_Sc = 0,017.\n\n"
            "Contraintuitivo: el gas a baja presión es el que permite el límite 0,8.",
            "Steel 8000 kg/m³, ζ = 0.0005, B = 19.05 mm, d = 6.6 mm → geometric factor 0.88.\n\n"
            "- Gas at 40 kg/m³: N_Sc = 4.93 × 0.0005 × 200 × 0.88 = 0.43.\n"
            "- Gas at 5 kg/m³: N_Sc = 4.93 × 0.0005 × 1600 × 0.88 = 3.5 ≥ 2.5.\n"
            "- Water at 1000 kg/m³: N_Sc = 0.017.\n\n"
            "Counter-intuitive: low-pressure gas is the one that allows the 0.8 limit."),
        "mistakes": (
            "- Subir ζ por encima de 0,0005 sin datos medidos para que «cumpla».\n"
            "- Creer que un líquido amortigua más: su densidad baja el Scruton.\n"
            "- Usar la densidad del gas en condiciones estándar.",
            "- Raising ζ above 0.0005 without measured data so it «passes».\n"
            "- Believing a liquid damps more: its density lowers the Scruton number.\n"
            "- Using gas density at standard conditions."),
    },
    "r.ratio": {
        "essence": (
            "Dice a qué fracción de su frecuencia natural está siendo sacudida la vaina. r = 1 "
            "es el peor caso: la fuerza transversal llega justo al ritmo propio. r = 0,5 es "
            "resonancia en línea, porque la fuerza en línea va al doble de la estela. Por debajo "
            "de 0,4 la vaina está por debajo de ambas.\n\n"
            "El factor de amplificación F_M = 1/(1 − r²) muestra cuánto se agranda el esfuerzo "
            "dinámico: 1,19 en r = 0,4; 1,33 en r = 0,5; 2,78 en r = 0,8; infinito en r = 1 (en "
            "la realidad lo limita el amortiguamiento).",
            "It tells at what fraction of its natural frequency the well is being shaken. r = 1 "
            "is the worst case: the transverse force arrives exactly at the natural rate. "
            "r = 0.5 is in-line resonance, because the in-line force runs at twice the wake. "
            "Below 0.4 the well is below both.\n\n"
            "The magnification factor F_M = 1/(1 − r²) shows how much dynamic stress grows: "
            "1.19 at r = 0.4; 1.33 at r = 0.5; 2.78 at r = 0.8; infinite at r = 1 (in reality "
            "damping limits it)."),
        "why": (
            "Es el criterio de frecuencia del estado ASME. Un r bajo protege contra los dos "
            "modos de resonancia y también reduce el esfuerzo dinámico.",
            "It is the frequency criterion of the ASME status. A low r protects against both "
            "resonance modes and also reduces dynamic stress."),
        "worked": (
            "f_s = 289 Hz, f_n,c = 420 Hz → r = 0,69 → F_M = 1/(1 − 0,476) = 1,91: el esfuerzo "
            "transversal casi se duplica respecto del estático.",
            "f_s = 289 Hz, f_n,c = 420 Hz → r = 0.69 → F_M = 1/(1 − 0.476) = 1.91: transverse "
            "stress nearly doubles compared with static."),
        "mistakes": (
            "- Pensar que r = 0,7 es «cómodo»: puede estar atravesando la resonancia en línea.\n"
            "- Mirar r solo en el caso normal, no en el máximo.",
            "- Thinking r = 0.7 is «comfortable»: it may be crossing in-line resonance.\n"
            "- Looking at r only in the normal case, not at the maximum."),
    },
    "r.steady": {
        "essence": (
            "Es el esfuerzo constante en la raíz. Tiene dos partes: la flexión que produce el "
            "arrastre promedio del fluido (la vaina se comporta como una viga en voladizo con "
            "carga distribuida, y el momento máximo está en la raíz) y la compresión axial que "
            "produce la presión del proceso sobre la punta. La flexión crece con el cuadrado "
            "del largo y con V²; la axial con la presión.",
            "It is the constant stress at the root. It has two parts: bending from the mean "
            "fluid drag (the well behaves as a cantilever beam under distributed load, with "
            "the maximum moment at the root) and axial compression from process pressure on "
            "the tip. Bending grows with the square of length and with V²; axial with "
            "pressure."),
        "why": (
            "Si es alto, la vaina puede deformarse permanentemente (doblarse) aunque no "
            "vibre. Además entra en el esfuerzo combinado de von Mises y reduce el margen para "
            "la parte dinámica.",
            "If high, the well can deform permanently (bend) even without vibrating. It also "
            "enters the combined von Mises stress and reduces the margin for the dynamic "
            "part."),
        "worked": (
            "Agua, presión dinámica 8010 Pa, vaina de 250 mm. Si el arrastre da 5 MPa de "
            "flexión y la presión 2 MPa axial, S_max = 7 MPa, muy lejos de un admisible de "
            "115 MPa. Con gas a 25 m/s y 40 kg/m³ (12 500 Pa) y 400 mm de largo, la flexión "
            "puede pasar de 20 MPa.",
            "Water, dynamic pressure 8010 Pa, 250 mm well. If drag gives 5 MPa bending and "
            "pressure 2 MPa axial, S_max = 7 MPa, far from an allowable of 115 MPa. With gas at "
            "25 m/s and 40 kg/m³ (12,500 Pa) and 400 mm length, bending can exceed 20 MPa."),
        "mistakes": (
            "- Olvidar que el momento crece con L²: un largo extra «por las dudas» sale caro.\n"
            "- Usar la presión manométrica donde corresponde la absoluta o viceversa.",
            "- Forgetting the moment grows with L²: extra length «just in case» is costly.\n"
            "- Using gauge pressure where absolute applies or vice versa."),
    },
    "r.dynamic": {
        "essence": (
            "Es la amplitud del esfuerzo que oscila en la raíz con cada remolino. Combina la "
            "fuerza en línea y la transversal, cada una amplificada por la cercanía a la "
            "resonancia, y multiplicada por K_t, que representa cómo el radio de acuerdo de la "
            "raíz concentra el esfuerzo.\n\n"
            "La fatiga es acumulativa: cada ciclo crea o hace crecer microfisuras en la "
            "superficie. Por debajo del límite de fatiga el acero puede soportar ciclos casi "
            "indefinidamente; por encima, la fisura crece hasta que la sección restante no "
            "aguanta.",
            "It is the amplitude of the stress oscillating at the root with each eddy. It "
            "combines the in-line and transverse forces, each magnified by proximity to "
            "resonance, and multiplied by K_t, which represents how the root fillet "
            "concentrates stress.\n\n"
            "Fatigue is cumulative: each cycle creates or grows microcracks at the surface. "
            "Below the fatigue limit steel can take cycles almost indefinitely; above it, the "
            "crack grows until the remaining section cannot carry the load."),
        "why": (
            "Es el modo de falla real de las termovainas: rotura por fatiga en la raíz. A "
            "cientos de hertz se acumulan mil millones de ciclos en pocos meses, así que el "
            "esfuerzo debe quedar por debajo del límite de fatiga corregido, no solo del "
            "admisible estático.",
            "It is the real failure mode of thermowells: fatigue fracture at the root. At "
            "hundreds of hertz a billion cycles build up in a few months, so stress must stay "
            "below the corrected fatigue limit, not just the static allowable."),
        "worked": (
            "Límite de fatiga de un 316 soldado ≈ 21 MPa (amplitud, valor típico). Si S_o = "
            "15 MPa → cumple con 29 % de margen. Si el radio de raíz b se reduce de 3,2 a "
            "1 mm, K_t sube y S_o puede pasar a 22 MPa: no cumple con la misma geometría.",
            "Fatigue limit of welded 316 ≈ 21 MPa (amplitude, typical). If S_o = 15 MPa → "
            "passes with 29 % margin. If the root fillet b drops from 3.2 to 1 mm, K_t rises "
            "and S_o can reach 22 MPa: fail with the same geometry."),
        "mistakes": (
            "- Comparar con el admisible estático S en vez del límite de fatiga.\n"
            "- Fabricar sin el radio de raíz especificado (aristas vivas).\n"
            "- Ignorar el estado del metal: soldado o roscado tiene menos resistencia a fatiga.",
            "- Comparing with the static allowable S instead of the fatigue limit.\n"
            "- Manufacturing without the specified root fillet (sharp corners).\n"
            "- Ignoring metal condition: welded or threaded has lower fatigue strength."),
    },
    "r.von_mises": {
        "essence": (
            "Un punto del metal puede estar comprimido en una dirección, estirado en otra y "
            "cortado en otra a la vez. El criterio de von Mises resume ese estado en un único "
            "número comparable con un ensayo de tracción simple: mide la energía que deforma el "
            "material cambiando su forma (no su volumen), que es la que lo hace fluir "
            "plásticamente.",
            "A point in the metal may be compressed in one direction, stretched in another and "
            "sheared in a third at once. The von Mises criterion sums that state into a single "
            "number comparable with a simple tensile test: it measures the energy that deforms "
            "the material by changing its shape (not its volume), which is what makes it yield."),
        "why": (
            "Verifica que la combinación de flexión, presión y esfuerzos de pared no haga "
            "fluir la raíz. Un fluencia local cambia la geometría y deja tensiones residuales "
            "que aceleran la fatiga.",
            "It checks that the combination of bending, pressure and wall stresses does not "
            "make the root yield. Local yielding changes geometry and leaves residual stresses "
            "that accelerate fatigue."),
        "worked": (
            "S_max = 30 MPa, S_r = −4 MPa, S_t = 10 MPa → S_vm ≈ 30 MPa. Con S = 115 MPa, el "
            "límite 1,5·S = 172 MPa: amplio margen.",
            "S_max = 30 MPa, S_r = −4 MPa, S_t = 10 MPa → S_vm ≈ 30 MPa. With S = 115 MPa, the "
            "1.5·S limit = 172 MPa: wide margin."),
        "mistakes": (
            "- Sumar estacionario y dinámico en una sola raíz cuadrada, como hacen algunas "
            "planillas: la norma los verifica por separado.\n"
            "- Usar S a temperatura ambiente cuando la vaina opera caliente.",
            "- Adding steady and dynamic under a single square root, as some spreadsheets do: "
            "the standard checks them separately.\n"
            "- Using room-temperature S when the well runs hot."),
    },
    "r.v_ir": {
        "essence": (
            "Es la velocidad del fluido a la que la frecuencia de estela llega a la mitad de "
            "la natural, es decir, la velocidad a la que empieza la resonancia en línea. Por "
            "encima de V_IR la vaina ya la atravesó; por debajo todavía no llegó.",
            "It is the fluid velocity at which the wake frequency reaches half the natural "
            "one, that is, the velocity at which in-line resonance begins. Above V_IR the well "
            "has already crossed it; below, it has not yet arrived."),
        "why": (
            "Permite saber si el proceso, al arrancar o variar el caudal, pasa por la "
            "resonancia en línea y cuánto tiempo puede quedarse ahí. Es clave en servicios "
            "con muchas maniobras.",
            "It tells whether the process, at start-up or with flow changes, passes through "
            "in-line resonance and how long it may dwell there. It is key in services with "
            "frequent operations."),
        "worked": (
            "B = 19,05 mm, f_n,c = 420 Hz, N_S = 0,22 → V_IR = 0,01905 × 420 / (2 × 0,22) = "
            "18,2 m/s. Un gas que opera a 25 m/s atraviesa la resonancia en línea en cada "
            "arranque.",
            "B = 19.05 mm, f_n,c = 420 Hz, N_S = 0.22 → V_IR = 0.01905 × 420 / (2 × 0.22) = "
            "18.2 m/s. A gas running at 25 m/s crosses in-line resonance at every start-up."),
        "mistakes": (
            "- Ignorar los transitorios: la vaina puede fallar en la rampa, no en operación "
            "normal.",
            "- Ignoring transients: the well may fail during the ramp, not in normal "
            "operation."),
    },
}
