"""Profundidad de las fichas de identificación, proyecto, proceso y fluido."""

from __future__ import annotations

from typing import Any

Bi = tuple[str, str]

_ID_WHY = (
    "La identificación es lo que une el cálculo con el objeto físico. En una planta hay "
    "cientos de termovainas parecidas; si el reporte no permite saber sin dudas a cuál "
    "corresponde, el cálculo pierde valor de auditoría y puede terminar aplicado a otra "
    "línea con otras condiciones.",
    "Identification is what links the calculation to the physical object. A plant has "
    "hundreds of similar thermowells; if the report does not tell unambiguously which one "
    "it belongs to, the calculation loses audit value and may end up applied to another "
    "line with other conditions.")


def _ident(essence: Bi, worked: Bi, mistakes: Bi) -> dict[str, Any]:
    return {"essence": essence, "why": _ID_WHY, "worked": worked, "mistakes": mistakes}


DEEP: dict[str, dict[str, Any]] = {
    "f.tag": _ident(
        ("El tag es la «cédula» del instrumento: un código único que lo identifica en el P&ID, "
         "en la lista de instrumentos, en el pedido de compra, en el almacén y en la placa del "
         "equipo. Suele seguir la norma ISA 5.1: letras de función (TW = termovaina, TE = "
         "elemento, TT = transmisor) más un número de lazo que comparten todos los elementos "
         "del mismo punto.",
         "The tag is the instrument's «ID card»: a unique code that identifies it on the P&ID, "
         "in the instrument list, in the purchase order, in the warehouse and on the nameplate. "
         "It usually follows ISA 5.1: function letters (TW = thermowell, TE = element, TT = "
         "transmitter) plus a loop number shared by all elements at the same point."),
        ("Lazo 101 de temperatura: TW-101 (vaina), TE-101 (sensor), TT-101 (transmisor), "
         "TI-101 (indicación). Si el mismo punto tiene un indicador local y uno remoto, se "
         "agregan sufijos: TW-101A y TW-101B.",
         "Temperature loop 101: TW-101 (well), TE-101 (sensor), TT-101 (transmitter), TI-101 "
         "(indication). If the same point has a local and a remote indicator, suffixes are "
         "added: TW-101A and TW-101B."),
        ("- Usar el tag del sensor (TE) para la vaina.\n"
         "- Repetir tags entre proyectos o unidades sin prefijo de área.\n"
         "- Cambiar el tag en el P&ID y no en el cálculo.",
         "- Using the sensor tag (TE) for the well.\n"
         "- Repeating tags across projects or units without an area prefix.\n"
         "- Changing the tag on the P&ID but not in the calculation.")),
    "f.service": _ident(
        ("Describe qué mide el punto en palabras del proceso: «Salida de gas del separador "
         "V-201» dice más que un número. Es lo que lee el operador y el inspector para "
         "entender la importancia del punto.",
         "It describes what the point measures in process words: «Gas outlet of separator "
         "V-201» says more than a number. It is what operators and inspectors read to "
         "understand the point's importance."),
        ("«Temperatura de descarga compresor K-301 etapa 2» permite inferir que hay pulsación "
         "y temperatura alta, y alertar sobre vibración.",
         "«Discharge temperature compressor K-301 stage 2» lets one infer pulsation and high "
         "temperature, and flag vibration concerns."),
        ("- Escribir solo «temperatura».\n- Copiar el servicio de otro tag sin revisarlo.",
         "- Writing just «temperature».\n- Copying another tag's service without "
         "checking it.")),
    "f.line": _ident(
        ("Es el número de línea de cañería (o el equipo) donde va la vaina. La línea define "
         "la especificación de cañería (material, clase de brida, sobreespesor de corrosión), "
         "que la vaina debe respetar.",
         "It is the piping line number (or equipment) where the well goes. The line defines "
         "the piping specification (material, flange class, corrosion allowance) that the "
         "well must follow."),
        ("6\"-PG-1203-A1B: 6 pulgadas, gas de proceso, línea 1203, especificación A1B (por "
         "ejemplo acero al carbono clase 300 con 3 mm de corrosión). Esa clase y ese "
         "sobreespesor son los que conviene usar en la vaina.",
         "6\"-PG-1203-A1B: 6 inch, process gas, line 1203, spec A1B (for example carbon "
         "steel class 300 with 3 mm corrosion). That class and allowance are the ones to use "
         "on the well."),
        ("- No consultar la especificación de la línea al elegir brida y material.",
         "- Not checking the line spec when choosing flange and material.")),
    "f.pid": _ident(
        ("Número del diagrama de cañerías e instrumentos donde aparece el punto. Es la "
         "fuente oficial de la ubicación lógica del instrumento.",
         "Number of the piping and instrumentation diagram where the point appears. It is "
         "the official source of the instrument's logical location."),
        ("P&ID 100-PID-0012 hoja 3: con ese dato cualquier persona encuentra el punto en "
         "segundos.",
         "P&ID 100-PID-0012 sheet 3: with it anyone finds the point in seconds."),
        ("- Omitir la hoja o la revisión del plano.",
         "- Omitting the sheet or drawing revision.")),
    "f.location": _ident(
        ("Ubicación física: área, nivel, coordenada o plataforma. Ayuda a montaje y "
         "mantenimiento a encontrar la vaina en campo.",
         "Physical location: area, level, coordinate or platform. It helps construction and "
         "maintenance find the well in the field."),
        ("«Área 200, rack principal, nivel +6,5 m, junto a FV-210».",
         "«Area 200, main rack, level +6.5 m, next to FV-210»."),
        ("- Dejarlo vacío en proyectos grandes.", "- Leaving it empty in large projects.")),
    "dlg.project_name": _ident(
        ("Nombre del proyecto que agrupa todos los tags calculados juntos. Aparece en el "
         "rótulo de cada reporte.",
         "Name of the project grouping all tags calculated together. It appears in every "
         "report title block."),
        ("«Ampliación planta de gas, fase 2».", "«Gas plant expansion, phase 2»."),
        ("- Usar nombres genéricos que se repiten entre proyectos.",
         "- Using generic names repeated across projects.")),
    "dlg.client": _ident(
        ("Cliente o usuario final. Determina qué especificaciones propias de cliente pueden "
         "aplicar (por ejemplo, un perfil de cliente con diseños y materiales preferidos).",
         "Client or end user. It determines which client specifications may apply (for "
         "example a client profile with preferred designs and materials)."),
        ("Un cliente puede exigir 316L como mínimo y bridas RF clase 300: conviene cargar "
         "ese perfil antes de calcular.",
         "A client may require 316L as a minimum and RF class 300 flanges: load that profile "
         "before calculating."),
        ("- Calcular con preferencias genéricas cuando el cliente tiene especificación "
         "propia.",
         "- Calculating with generic preferences when the client has its own spec.")),
    "dlg.plant": _ident(
        ("Planta o instalación donde se monta. Junto con la ubicación, define la altitud "
         "(presión barométrica) y las condiciones ambientales.",
         "Plant or facility where it is installed. Together with location it sets altitude "
         "(barometric pressure) and ambient conditions."),
        ("Una planta a 2500 m de altitud tiene una presión barométrica de unos 75 kPa, no "
         "101 kPa.",
         "A plant at 2500 m altitude has a barometric pressure of about 75 kPa, not "
         "101 kPa."),
        ("- No revisar la presión barométrica al cambiar de planta.",
         "- Not reviewing barometric pressure when changing plant.")),
    "dlg.doc_number": _ident(
        ("Número de documento del cálculo según el sistema documental del proyecto. "
         "Permite controlar revisiones y aprobaciones.",
         "Calculation document number per the project's document system. It allows "
         "revision and approval control."),
        ("XYZ-100-CAL-IN-0045 rev. B.", "XYZ-100-CAL-IN-0045 rev. B."),
        ("- Emitir revisiones nuevas sin cambiar la letra de revisión.",
         "- Issuing new revisions without changing the revision letter.")),
    "dlg.barometric": {
        "essence": (
            "Un manómetro mide la diferencia entre la presión del proceso y la atmósfera que lo "
            "rodea; la física del fluido (densidad de un gas, punto de ebullición) depende de "
            "la presión absoluta, medida desde el vacío. La presión barométrica es el puente: "
            "absoluta = manométrica + barométrica. Cae con la altitud, cerca de 1,2 kPa cada "
            "100 m, porque hay menos aire encima.",
            "A pressure gauge measures the difference between process pressure and the "
            "surrounding atmosphere; fluid physics (gas density, boiling point) depends on "
            "absolute pressure, measured from vacuum. Barometric pressure is the bridge: "
            "absolute = gauge + barometric. It falls with altitude, about 1.2 kPa per 100 m, "
            "because there is less air above."),
        "why": (
            "En gases a baja presión el error es grande: 2 barg a nivel del mar son 3,01 bar "
            "abs, y en una planta a 3000 m son 2,70 bar abs. Esa diferencia del 10 % pasa "
            "directo a la densidad y a la velocidad calculada.",
            "In low-pressure gases the error is large: 2 barg at sea level is 3.01 bar abs, and "
            "at a 3000 m plant it is 2.70 bar abs. That 10 % difference goes straight into "
            "density and computed velocity."),
        "worked": (
            "Planta a 1500 m: presión ≈ 101,3 × (1 − 2,26·10⁻⁵ × 1500)^5,26 ≈ 84,6 kPa. Un gas "
            "a 0,5 barg está a 134,6 kPa abs, no a 151,3: un 11 % menos de densidad.",
            "Plant at 1500 m: pressure ≈ 101.3 × (1 − 2.26·10⁻⁵ × 1500)^5.26 ≈ 84.6 kPa. A gas "
            "at 0.5 barg is at 134.6 kPa abs, not 151.3: 11 % less density."),
        "mistakes": (
            "- Dejar 101,325 kPa en plantas de altura.\n"
            "- Cargar presiones absolutas con la opción manométrica activa (se suma dos veces "
            "la atmósfera).",
            "- Leaving 101.325 kPa at high-altitude plants.\n"
            "- Entering absolute pressures with the gauge option on (atmosphere added "
            "twice)."),
    },
    "dlg.gauge": {
        "essence": (
            "Define cómo leés y escribís las presiones: manométricas (barg, psig, relativas a "
            "la atmósfera) o absolutas (bar a, psia, relativas al vacío). En planta casi todo "
            "se especifica en manométrica; las propiedades físicas se calculan en absoluta. TS "
            "convierte internamente y siempre calcula en Pa absoluto.",
            "It defines how you read and enter pressures: gauge (barg, psig, relative to "
            "atmosphere) or absolute (bar a, psia, relative to vacuum). In plants almost "
            "everything is specified in gauge; physical properties are computed in absolute. TS "
            "converts internally and always calculates in absolute Pa."),
        "why": (
            "Un error de convención es un error de 1 bar. En una línea de 1 barg eso duplica "
            "la densidad del gas.",
            "A convention error is a 1 bar error. In a 1 barg line that doubles gas density."),
        "worked": (
            "Hoja de datos: 10 barg. Con la opción manométrica activa se carga 10; con la "
            "absoluta se carga 11,01 (a nivel del mar).",
            "Datasheet: 10 barg. With the gauge option on, enter 10; with absolute, enter "
            "11.01 (at sea level)."),
        "mistakes": (
            "- Copiar valores de una hoja de datos sin mirar si dice «g» o «a».\n"
            "- Usar manométrica para vacío: un recipiente a −0,5 barg está a 0,51 bar abs.",
            "- Copying datasheet values without checking whether they say «g» or «a».\n"
            "- Using gauge for vacuum: a vessel at −0.5 barg is at 0.51 bar abs."),
    },
    "f.fluid_type": {
        "essence": (
            "Separa los fluidos por cómo se comportan:\n\n"
            "- Líquido: casi incompresible, denso (500 a 1500 kg/m³). Empuja fuerte a "
            "velocidades bajas.\n"
            "- Gas: compresible, liviano (0,5 a 200 kg/m³). Velocidades altas, frecuencias "
            "altas.\n"
            "- Vapor: gas cerca de su punto de condensación; puede formar gotas que erosionan.\n"
            "- Vapor de agua (steam): saturado o sobrecalentado, con propiedades propias.\n"
            "- Bifásico: mezcla de líquido y gas; flujo irregular con golpes (slugs) que la "
            "norma no cubre.",
            "Separates fluids by how they behave:\n\n"
            "- Liquid: almost incompressible, dense (500 to 1500 kg/m³). Pushes hard at low "
            "velocities.\n"
            "- Gas: compressible, light (0.5 to 200 kg/m³). High velocities, high "
            "frequencies.\n"
            "- Vapour: gas near its condensation point; may form eroding droplets.\n"
            "- Steam: saturated or superheated water, with its own properties.\n"
            "- Two-phase: liquid and gas mixture; irregular flow with slugs the standard does "
            "not cover."),
        "why": (
            "La fase decide la densidad (orden de magnitud), qué criterio de Scruton aplica y "
            "si el cálculo es válido. Un bifásico calculado como gas subestima mucho la carga "
            "por los tapones de líquido.",
            "Phase sets density (order of magnitude), which Scruton criterion applies and "
            "whether the calculation is valid. Two-phase computed as gas greatly underestimates "
            "load from liquid slugs."),
        "worked": (
            "Propano a 15 bar y 40 °C es líquido (presión de vapor ≈ 13,7 bar). A 10 bar y "
            "40 °C es gas. Mismo fluido, densidades de 480 y 20 kg/m³: TS avisa si el tipo "
            "elegido no coincide con lo que da CoolProp.",
            "Propane at 15 bar and 40 °C is liquid (vapour pressure ≈ 13.7 bar). At 10 bar and "
            "40 °C it is gas. Same fluid, densities of 480 and 20 kg/m³: TS warns if the chosen "
            "type does not match CoolProp."),
        "mistakes": (
            "- Elegir «gas» para vapor saturado con condensado.\n"
            "- Calcular un bifásico sin margen extra.",
            "- Choosing «gas» for saturated steam with condensate.\n"
            "- Calculating two-phase flow without extra margin."),
    },
    "f.fluid": {
        "essence": (
            "Identifica la sustancia para calcular sus propiedades. CoolProp resuelve "
            "ecuaciones de estado de referencia (modelos termodinámicos ajustados a miles de "
            "mediciones) que dan densidad y viscosidad a cualquier presión y temperatura, "
            "incluso cerca del punto crítico, donde las propiedades cambian bruscamente.",
            "It identifies the substance to compute its properties. CoolProp solves reference "
            "equations of state (thermodynamic models fitted to thousands of measurements) "
            "that give density and viscosity at any pressure and temperature, even near the "
            "critical point, where properties change sharply."),
        "why": (
            "La densidad y la viscosidad entran en todo el cálculo de flujo. Elegir «aire» "
            "para un gas natural rico subestima la densidad un 30 % o más.",
            "Density and viscosity enter the whole flow calculation. Choosing «air» for a rich "
            "natural gas underestimates density by 30 % or more."),
        "worked": (
            "CO₂ a 80 bar: a 25 °C es líquido denso (≈ 750 kg/m³); a 40 °C es supercrítico "
            "(≈ 280 kg/m³). Una diferencia de 15 °C cambia la densidad 2,7 veces.",
            "CO₂ at 80 bar: at 25 °C it is a dense liquid (≈ 750 kg/m³); at 40 °C it is "
            "supercritical (≈ 280 kg/m³). A 15 °C difference changes density 2.7 times."),
        "mistakes": (
            "- Usar un componente puro para una mezcla (gas natural, crudos): cargue "
            "propiedades a mano del simulador de procesos.\n"
            "- No revisar el estado («Líquido» o «Vapor») cerca de la saturación.",
            "- Using a pure component for a mixture (natural gas, crudes): enter properties "
            "from the process simulator.\n"
            "- Not checking the state («Liquid» or «Vapour») near saturation."),
    },
    "f.phase_calc": {
        "essence": (
            "Es la fase que el cálculo usa de verdad. Con propiedades automáticas, TS compara "
            "presión y temperatura con la curva de saturación del fluido: por encima de la "
            "presión de vapor es líquido; por debajo, gas.",
            "It is the phase the calculation actually uses. With automatic properties, TS "
            "compares pressure and temperature with the fluid's saturation curve: above vapour "
            "pressure it is liquid; below, gas."),
        "why": (
            "Si la fase calculada no coincide con la elegida, probablemente hay un error de "
            "datos (presión manométrica por absoluta, unidades de temperatura) o el punto está "
            "en flasheo.",
            "If the computed phase does not match the chosen one, there is probably a data "
            "error (gauge for absolute, temperature units) or the point is flashing."),
        "worked": (
            "Agua a 1 barg y 110 °C: presión de vapor a 110 °C = 1,43 bar abs; presión real "
            "= 2,01 bar abs → líquido. A 0,2 barg sería vapor.",
            "Water at 1 barg and 110 °C: vapour pressure at 110 °C = 1.43 bar abs; actual "
            "pressure = 2.01 bar abs → liquid. At 0.2 barg it would be steam."),
        "mistakes": (
            "- Ignorar el aviso de fase distinta.",
            "- Ignoring the phase-mismatch warning."),
    },
    "f.p_op": {
        "essence": (
            "Es la presión normal del fluido en el punto de la vaina. Actúa de dos formas: "
            "comprime el gas (más presión, más densidad, más fuerza del flujo a igual "
            "velocidad) y empuja sobre la superficie de la vaina, generando un esfuerzo axial "
            "y esfuerzos de pared que se suman a la flexión.",
            "It is the normal fluid pressure at the well location. It acts in two ways: it "
            "compresses the gas (more pressure, more density, more flow force at equal "
            "velocity) and pushes on the well surface, creating axial and wall stresses that "
            "add to bending."),
        "why": (
            "En gases define la densidad, que entra al cuadrado en nada pero linealmente en "
            "todas las fuerzas y en el Scruton. Duplicar la presión de un gas duplica la carga "
            "dinámica a igual velocidad y reduce a la mitad el Scruton.",
            "In gases it sets density, which enters linearly in all forces and in the Scruton "
            "number. Doubling a gas's pressure doubles dynamic load at equal velocity and "
            "halves the Scruton number."),
        "worked": (
            "Gas natural a 30 °C: a 20 bar abs ρ ≈ 15 kg/m³; a 70 bar abs ρ ≈ 58 kg/m³. A 20 m/s, "
            "la presión dinámica pasa de 3000 a 11 600 Pa.",
            "Natural gas at 30 °C: at 20 bar abs ρ ≈ 15 kg/m³; at 70 bar abs ρ ≈ 58 kg/m³. At "
            "20 m/s, dynamic pressure goes from 3000 to 11,600 Pa."),
        "mistakes": (
            "- Cargar la presión de diseño como de operación: sobreestima la densidad.\n"
            "- Tomar la presión de otro punto de la línea (antes de una válvula reductora).",
            "- Entering design pressure as operating: overestimates density.\n"
            "- Taking pressure from another point of the line (upstream of a reducing "
            "valve)."),
    },
    "f.p_design": {
        "essence": (
            "Es la presión máxima que la línea puede ver en una condición anormal pero "
            "creíble (bloqueo, falla de control) y para la que se calibran las válvulas de "
            "seguridad. La vaina, como parte de la envolvente de presión, debe aguantarla sin "
            "colapsar ni filtrar.\n\n"
            "Una vaina es un tubo cerrado sometido a presión externa: el riesgo no es que "
            "«explote» sino que se aplaste o pandee hacia adentro, sobre todo en la punta.",
            "It is the maximum pressure the line can see in an abnormal but credible condition "
            "(blocked outlet, control failure), the one safety valves are set for. The well, "
            "as part of the pressure boundary, must withstand it without collapsing or "
            "leaking.\n\n"
            "A thermowell is a closed tube under external pressure: the risk is not that it "
            "«bursts» but that it crushes or buckles inwards, especially at the tip."),
        "why": (
            "Si la presión admisible del vástago, de la punta o de la brida es menor que la de "
            "diseño, la vaina es el punto débil de la línea.",
            "If the allowable pressure of shank, tip or flange is below design pressure, the "
            "well is the weak point of the line."),
        "worked": (
            "Línea clase 300 en acero al carbono a 200 °C: la brida admite unos 43 bar. Con "
            "presión de diseño de 50 barg, hay que subir a clase 600 aunque el vástago aguante.",
            "Class 300 carbon steel line at 200 °C: the flange allows about 43 bar. With a "
            "50 barg design pressure, go up to class 600 even if the shank holds."),
        "mistakes": (
            "- Usar la presión de operación.\n"
            "- Olvidar la prueba hidrostática, que suele ser 1,5 veces la de diseño.",
            "- Using operating pressure.\n"
            "- Forgetting the hydrostatic test, usually 1.5 times design."),
    },
    "f.t_op": {
        "essence": (
            "La temperatura cambia el fluido y el metal. En el fluido: un gas caliente es "
            "menos denso, un líquido caliente es menos viscoso. En el metal: los átomos vibran "
            "más, los enlaces se aflojan y el módulo elástico baja (un 316 pierde cerca de un "
            "8 % de rigidez a 300 °C). Menos rigidez significa menos frecuencia natural.",
            "Temperature changes both fluid and metal. In the fluid: a hot gas is less dense, "
            "a hot liquid less viscous. In the metal: atoms vibrate more, bonds loosen and the "
            "elastic modulus falls (316 loses about 8 % of stiffness at 300 °C). Less "
            "stiffness means lower natural frequency."),
        "why": (
            "Afecta la densidad, el Reynolds, la frecuencia natural y la resistencia a la "
            "fatiga. Además define el sensor y la conexión adecuados.",
            "It affects density, Reynolds, natural frequency and fatigue strength. It also "
            "defines the suitable sensor and connection."),
        "worked": (
            "316 a 20 °C: E = 195 GPa; a 400 °C: E ≈ 170 GPa. La frecuencia cae √(170/195) = "
            "0,93: un 7 % menos de margen de resonancia.",
            "316 at 20 °C: E = 195 GPa; at 400 °C: E ≈ 170 GPa. Frequency drops √(170/195) = "
            "0.93: 7 % less resonance margin."),
        "mistakes": (
            "- Usar la temperatura ambiente para un servicio caliente.\n"
            "- Confundir °C y °F al importar datos.",
            "- Using ambient temperature for a hot service.\n"
            "- Mixing °C and °F when importing data."),
    },
    "f.t_design": {
        "essence": (
            "Es la temperatura máxima para la que se diseña la línea. A más temperatura, el "
            "metal resiste menos (el esfuerzo admisible baja) y las bridas admiten menos "
            "presión. Por encima de unos 425 °C en aceros al carbono y 540 °C en inoxidables "
            "aparece la fluencia lenta (creep): el metal se deforma con el tiempo aun con carga "
            "constante.",
            "It is the maximum temperature the line is designed for. Hotter metal is weaker "
            "(allowable stress falls) and flanges allow less pressure. Above about 425 °C in "
            "carbon steels and 540 °C in stainless, creep appears: the metal deforms over time "
            "even under constant load."),
        "why": (
            "Fija el esfuerzo admisible y el rating de la brida para la verificación de "
            "presión. Si supera el límite del material o del recubrimiento, la vaina no es "
            "apta.",
            "It sets allowable stress and flange rating for the pressure check. If it exceeds "
            "the material or coating limit, the well is unfit."),
        "worked": (
            "Brida clase 150 en acero al carbono: unos 19,6 bar a 38 °C y unos 13,8 bar a "
            "200 °C. La misma brida pierde un 30 % de capacidad.",
            "Class 150 carbon steel flange: about 19.6 bar at 38 °C and about 13.8 bar at "
            "200 °C. The same flange loses 30 % of capacity."),
        "mistakes": (
            "- Usar la temperatura de operación para el rating.\n"
            "- Olvidar el límite del recubrimiento (PTFE, Stellite).",
            "- Using operating temperature for the rating.\n"
            "- Forgetting the coating limit (PTFE, Stellite)."),
    },
    "f.auto_props": {
        "essence": (
            "Activa el cálculo automático de densidad y viscosidad con ecuaciones de estado "
            "(CoolProp) a la presión y temperatura del tag, en lugar de usar valores fijos. "
            "Cada vez que cambiás P o T, las propiedades se recalculan y la fase se verifica.",
            "It turns on automatic density and viscosity calculation with equations of state "
            "(CoolProp) at the tag's pressure and temperature, instead of fixed values. Each "
            "time P or T change, properties are recomputed and phase is checked."),
        "why": (
            "Evita el error más común: cambiar la presión y dejar la densidad vieja. También "
            "detecta cambios de fase que a mano pasarían desapercibidos.",
            "It avoids the most common error: changing pressure and keeping the old density. "
            "It also detects phase changes that would go unnoticed by hand."),
        "worked": (
            "Nitrógeno: de 10 a 30 bar abs a 20 °C la densidad pasa de 11,5 a 34,6 kg/m³. Con "
            "automático se actualiza sola; a mano habría que recalcularla.",
            "Nitrogen: from 10 to 30 bar abs at 20 °C density goes from 11.5 to 34.6 kg/m³. "
            "With automatic it updates itself; by hand it must be recalculated."),
        "mistakes": (
            "- Desactivarlo para mezclas sin cargar después las propiedades correctas.",
            "- Turning it off for mixtures without then entering correct properties."),
    },
    "f.density": {
        "essence": (
            "Es cuánta masa hay en cada metro cúbico de fluido. A nivel molecular, depende de "
            "cuán juntas están las moléculas: en un líquido casi se tocan y la densidad cambia "
            "poco; en un gas están muy separadas y la densidad sigue casi a la ley de gases "
            "(proporcional a la presión e inversa a la temperatura absoluta), corregida por el "
            "factor de compresibilidad Z.\n\n"
            "Para la vaina, la densidad es «cuánto pesa el viento»: a igual velocidad, un fluido "
            "más denso empuja más.",
            "It is how much mass there is in each cubic metre of fluid. At molecular level it "
            "depends on how close molecules are: in a liquid they almost touch and density "
            "changes little; in a gas they are far apart and density nearly follows the gas law "
            "(proportional to pressure, inverse to absolute temperature), corrected by the "
            "compressibility factor Z.\n\n"
            "For the well, density is «how heavy the wind is»: at equal velocity, a denser "
            "fluid pushes harder."),
        "why": (
            "Entra en las fuerzas (lineal), en el Reynolds, en la masa añadida que baja la "
            "frecuencia natural, en el Scruton (inversa) y en la velocidad erosional. Es, junto "
            "con la velocidad, el dato de proceso que más pesa.",
            "It enters forces (linearly), Reynolds, the added mass that lowers natural "
            "frequency, Scruton (inversely) and erosional velocity. With velocity, it is the "
            "process datum that weighs most."),
        "worked": (
            "Metano a 50 bar abs y 25 °C: ρ = P·M/(Z·R·T) = 5·10⁶ × 0,01604 / (0,92 × 8,314 × "
            "298) = 35,2 kg/m³. Sin el factor Z (Z = 1) daría 32,4: un 8 % menos.",
            "Methane at 50 bar abs and 25 °C: ρ = P·M/(Z·R·T) = 5·10⁶ × 0.01604 / (0.92 × "
            "8.314 × 298) = 35.2 kg/m³. Without Z (Z = 1) it would be 32.4: 8 % less."),
        "mistakes": (
            "- Usar densidad estándar para un gas a presión.\n"
            "- Usar la gravedad específica (adimensional) como si fuera kg/m³.",
            "- Using standard density for a gas under pressure.\n"
            "- Using specific gravity (dimensionless) as if it were kg/m³."),
    },
    "f.viscosity": {
        "essence": (
            "Es la resistencia interna del fluido a deslizar sobre sí mismo. En líquidos viene "
            "de las fuerzas de atracción entre moléculas vecinas: al calentar, las moléculas se "
            "mueven más y se «sueltan», y la viscosidad cae mucho (el agua pierde 70 % de "
            "viscosidad de 20 a 100 °C). En gases viene de los choques entre moléculas que "
            "pasan de una capa a otra: al calentar chocan más y la viscosidad sube.",
            "It is the fluid's internal resistance to sliding over itself. In liquids it comes "
            "from attraction between neighbouring molecules: heating makes them move more and "
            "«let go», and viscosity drops sharply (water loses 70 % of its viscosity from 20 "
            "to 100 °C). In gases it comes from molecules crossing between layers and "
            "colliding: heating increases collisions and viscosity rises."),
        "why": (
            "Solo entra en el Reynolds, que define el régimen de la estela y el Strouhal. Su "
            "influencia es menor que la de la densidad, salvo en fluidos muy viscosos, donde "
            "puede suprimir el desprendimiento de vórtices.",
            "It only enters Reynolds, which sets the wake regime and Strouhal. Its influence is "
            "smaller than density's, except in very viscous fluids, where it can suppress "
            "vortex shedding."),
        "worked": (
            "Agua: 1,0 mPa·s a 20 °C, 0,35 a 80 °C. Aire: 0,018 mPa·s a 20 °C, 0,025 a 200 °C. "
            "Crudo pesado: 500 mPa·s a 20 °C, 30 a 80 °C.",
            "Water: 1.0 mPa·s at 20 °C, 0.35 at 80 °C. Air: 0.018 mPa·s at 20 °C, 0.025 at "
            "200 °C. Heavy crude: 500 mPa·s at 20 °C, 30 at 80 °C."),
        "mistakes": (
            "- Cargar centistokes (cinemática) como centipoise (dinámica): hay que multiplicar "
            "por la densidad.",
            "- Entering centistokes (kinematic) as centipoise (dynamic): multiply by "
            "density."),
    },
    "f.std_density": {
        "essence": (
            "Es la densidad del gas en condiciones de referencia (15 °C y 101,325 kPa en TS). "
            "Sirve para convertir caudales «estándar», que en realidad son caudales de masa "
            "disfrazados de volumen: 1 Sm³ siempre contiene la misma masa de un gas dado.",
            "It is the gas density at reference conditions (15 °C and 101.325 kPa in TS). It "
            "converts «standard» flows, which are really mass flows disguised as volume: 1 Sm³ "
            "always contains the same mass of a given gas."),
        "why": (
            "Sin ella no se puede pasar de Sm³/h o MMSCFD a velocidad real.",
            "Without it you cannot go from Sm³/h or MMSCFD to actual velocity."),
        "worked": (
            "Gas natural de peso molecular 18,5: ρ_std = 101 325 × 0,0185 / (8,314 × 288,15) = "
            "0,78 kg/m³.",
            "Natural gas with molecular weight 18.5: ρ_std = 101,325 × 0.0185 / (8.314 × "
            "288.15) = 0.78 kg/m³."),
        "mistakes": (
            "- Usar condiciones normales (0 °C) con caudales estándar (15 °C) o al revés.\n"
            "- En EE. UU. el estándar suele ser 60 °F y 14,696 psia.",
            "- Using normal conditions (0 °C) with standard flows (15 °C) or the reverse.\n"
            "- In the US the standard is usually 60 °F and 14.696 psia."),
    },
    "f.prop_source": {
        "essence": (
            "Registra el origen de la densidad y la viscosidad: calculadas con CoolProp, "
            "tomadas de la biblioteca o cargadas a mano (por ejemplo del simulador de "
            "procesos). Es trazabilidad: quien revise el cálculo sabe de dónde salió cada "
            "número.",
            "It records the origin of density and viscosity: computed by CoolProp, taken from "
            "the library or entered by hand (for example from the process simulator). It is "
            "traceability: whoever reviews the calculation knows where each number came from."),
        "why": (
            "Un revisor puede aceptar o cuestionar un dato según su fuente. En mezclas, la "
            "fuente correcta suele ser el balance de masa y energía del proceso.",
            "A reviewer can accept or question a value depending on its source. For mixtures "
            "the right source is usually the process heat and mass balance."),
        "worked": (
            "«Manual: HMB rev. C, corriente 23» deja claro qué documento respalda los datos.",
            "«Manual: HMB rev. C, stream 23» makes clear which document backs the data."),
        "mistakes": (
            "- Dejar la nota vacía cuando las propiedades son manuales.",
            "- Leaving the note empty when properties are manual."),
    },
    "f.flow_cases": {
        "essence": (
            "Un proceso no opera a un solo caudal: arranca, opera normal, sube al máximo, "
            "baja al mínimo. Cada condición produce una velocidad distinta y la vaina debe "
            "sobrevivir a todas. TS verifica cada caso por separado y el estado global es el "
            "del peor.",
            "A process does not run at a single flow: it starts up, runs normal, rises to "
            "maximum, drops to minimum. Each condition gives a different velocity and the well "
            "must survive them all. TS checks each case separately and the overall status is "
            "the worst one."),
        "why": (
            "El caso que manda depende del criterio: el máximo da los esfuerzos más altos, "
            "pero un caso intermedio puede caer justo en la resonancia en línea.",
            "The governing case depends on the criterion: the maximum gives the highest "
            "stresses, but an intermediate case may fall right on in-line resonance."),
        "worked": (
            "Mínimo 8 m/s (r = 0,22), normal 15 m/s (r = 0,41), máximo 20 m/s (r = 0,55). Con "
            "N_Sc < 2,5, el normal ya pasa de 0,4: el caso que manda no es el máximo sino el "
            "normal, porque es donde la vaina pasa más tiempo.",
            "Minimum 8 m/s (r = 0.22), normal 15 m/s (r = 0.41), maximum 20 m/s (r = 0.55). "
            "With N_Sc < 2.5, normal already exceeds 0.4: the governing case is normal, not "
            "maximum, because that is where the well spends most time."),
        "mistakes": (
            "- Cargar solo el normal.\n"
            "- Olvidar casos de arranque, purga o by-pass con caudales fuera de rango.",
            "- Entering only normal.\n"
            "- Forgetting start-up, purge or bypass cases with out-of-range flows."),
    },
    "f.basis": {
        "essence": (
            "Indica en qué forma tenés el caudal: velocidad directa, caudal másico (kg/h), "
            "volumétrico real (m³/h a condiciones de operación) o estándar (Sm³/h). Todos se "
            "convierten a velocidad media con el diámetro interno y la densidad.",
            "It states the form of your flow data: direct velocity, mass flow (kg/h), actual "
            "volume flow (m³/h at operating conditions) or standard (Sm³/h). All are converted "
            "to mean velocity with inside diameter and density."),
        "why": (
            "Elegir la base equivocada es un error de factor 10 o más en gases.",
            "Choosing the wrong basis is an error of a factor of 10 or more in gases."),
        "worked": (
            "10 000 kg/h de vapor a 10 bar abs y 250 °C (ρ = 4,3 kg/m³) en 6\" Sch 40: Q = "
            "10 000 / 3600 / 4,3 = 0,646 m³/s; V = 0,646 / 0,01865 = 34,6 m/s.",
            "10,000 kg/h of steam at 10 bar abs and 250 °C (ρ = 4.3 kg/m³) in 6\" Sch 40: Q = "
            "10,000 / 3600 / 4.3 = 0.646 m³/s; V = 0.646 / 0.01865 = 34.6 m/s."),
        "mistakes": (
            "- Elegir «volumétrico» para un dato en Sm³/h.",
            "- Choosing «volumetric» for data in Sm³/h."),
    },
    "f.case": {
        "essence": (
            "Es el nombre de cada condición de flujo (mínimo, normal, máximo, arranque…). Solo "
            "identifica el caso en tablas y gráficos.",
            "It is the name of each flow condition (minimum, normal, maximum, start-up…). It "
            "only identifies the case in tables and charts."),
        "why": (
            "Un nombre claro permite al revisor saber qué condición manda y por qué.",
            "A clear name lets the reviewer know which condition governs and why."),
        "worked": ("«Máx. con by-pass abierto» es mejor que «Caso 4».",
                   "«Max. with bypass open» is better than «Case 4»."),
        "mistakes": ("- Nombres genéricos que no dicen la condición.",
                     "- Generic names that do not state the condition."),
    },
    "f.value": {
        "essence": (
            "Es el número del caudal o la velocidad de cada caso, en las unidades de la base "
            "elegida.",
            "It is the flow or velocity number of each case, in the units of the chosen "
            "basis."),
        "why": (
            "Define la velocidad del caso, que manda en frecuencia y esfuerzos.",
            "It defines the case velocity, which governs frequency and stresses."),
        "worked": (
            "Base másica, 12 t/h → 12 000 kg/h → con ρ y Di da la velocidad.",
            "Mass basis, 12 t/h → 12,000 kg/h → with ρ and ID gives velocity."),
        "mistakes": ("- Confundir t/h con kg/h, o MMSCFD con MSCFD.",
                     "- Confusing t/h with kg/h, or MMSCFD with MSCFD."),
    },
    "f.h2s": {
        "essence": (
            "La presión parcial de H₂S mide cuánta fuerza tiene el H₂S para disolverse en el "
            "agua y atacar el metal. En una mezcla de gases, cada componente aporta una parte "
            "de la presión total proporcional a su fracción molar:\n\n"
            "p H₂S = presión absoluta total × fracción molar de H₂S\n\n"
            "Si hay agua, el H₂S disuelto reacciona con el hierro y libera hidrógeno atómico "
            "(H, no H₂) en la superficie. Ese átomo es tan pequeño que se mete en la red "
            "cristalina del acero; el sulfuro impide que se recombine en H₂ y escape. Dentro "
            "del metal se acumula en zonas tensionadas o duras (soldaduras, zonas afectadas por "
            "calor, martensita) y fragiliza el material: aparecen fisuras que avanzan sin "
            "deformación previa. Es la fisuración bajo tensión por sulfuros (SSC).",
            "H₂S partial pressure measures how strongly H₂S can dissolve in water and attack "
            "the metal. In a gas mixture each component contributes a share of total pressure "
            "proportional to its mole fraction:\n\n"
            "p H₂S = total absolute pressure × H₂S mole fraction\n\n"
            "If water is present, dissolved H₂S reacts with iron and releases atomic hydrogen "
            "(H, not H₂) at the surface. That atom is so small it enters the steel's crystal "
            "lattice; sulfide prevents it from recombining into H₂ and escaping. Inside the "
            "metal it gathers in stressed or hard zones (welds, heat-affected zones, "
            "martensite) and embrittles the material: cracks appear and grow without prior "
            "deformation. This is sulfide stress cracking (SSC)."),
        "why": (
            "Lo que importa no es solo cuánto H₂S hay, sino a qué presión: cuanto más alta la "
            "presión parcial, más H₂S se disuelve y mayor el riesgo. El mismo gas con 100 ppm "
            "es inofensivo a 2 bar y peligroso a 50 bar. En la vaina, la zona de riesgo es la "
            "de mayor esfuerzo: la raíz y la soldadura de la brida. Una fisura ahí libera un "
            "gas tóxico (letal por encima de unos cientos de ppm en aire).",
            "What matters is not only how much H₂S there is, but at what pressure: the higher "
            "the partial pressure, the more H₂S dissolves and the higher the risk. The same "
            "gas with 100 ppm is harmless at 2 bar and dangerous at 50 bar. On the well, the "
            "risk zone is the highest-stress one: the root and flange weld. A crack there "
            "releases a toxic gas (lethal above a few hundred ppm in air)."),
        "limits": (
            "Desde unos 0,3 kPa (0,05 psia), NACE MR0175 / ISO 15156 considera el servicio "
            "ácido (sour). Desde ahí los materiales deben estar aceptados para ese servicio, "
            "con dureza controlada (por ejemplo ≤ 22 HRC en acero al carbono). El riesgo crece "
            "con pH bajo y con la presión parcial; los límites detallados por material están "
            "en la norma.",
            "From about 0.3 kPa (0.05 psia), NACE MR0175 / ISO 15156 considers the service "
            "sour. From there materials must be accepted for that service, with controlled "
            "hardness (for example ≤ 22 HRC for carbon steel). Risk grows with low pH and with "
            "partial pressure; detailed limits per material are in the standard."),
        "worked": (
            "100 ppm de H₂S (fracción 0,0001):\n\n"
            "- A 50 bar abs: 50 × 0,0001 = 0,005 bar = 0,5 kPa → servicio ácido.\n"
            "- A 2 bar abs: 2 × 0,0001 = 0,0002 bar = 0,02 kPa → no ácido.\n\n"
            "TS bloquea los materiales no aptos para servicio ácido desde 345 Pa (0,05 psia) o "
            "si marcás servicio NACE.",
            "100 ppm H₂S (fraction 0.0001):\n\n"
            "- At 50 bar abs: 50 × 0.0001 = 0.005 bar = 0.5 kPa → sour service.\n"
            "- At 2 bar abs: 2 × 0.0001 = 0.0002 bar = 0.02 kPa → not sour.\n\n"
            "TS blocks materials not fit for sour service from 345 Pa (0.05 psia) or if you "
            "tick NACE service."),
        "mistakes": (
            "- Cargar los ppm como si fueran la presión parcial.\n"
            "- Usar presión manométrica en vez de absoluta.\n"
            "- Suponer que sin agua libre no hay riesgo: basta con condensación en paradas.\n"
            "- Aceptar un material «compatible» sin control de dureza en soldaduras.",
            "- Entering ppm as if it were partial pressure.\n"
            "- Using gauge instead of absolute pressure.\n"
            "- Assuming no free water means no risk: condensation during shutdowns is "
            "enough.\n"
            "- Accepting a «compatible» material without hardness control on welds."),
    },
    "f.chlorides": {
        "essence": (
            "Los cloruros (Cl⁻, de sal, agua de mar, agua de pozo) atacan la capa pasiva de "
            "óxido de cromo que protege a los inoxidables. El ion cloruro es pequeño y muy "
            "móvil: rompe la capa en puntos débiles y forma picaduras. Si además hay esfuerzo de "
            "tracción y temperatura (por encima de unos 60 °C), desde esas picaduras nacen "
            "fisuras ramificadas que atraviesan el grano: la corrosión bajo tensión por "
            "cloruros (Cl-SCC). Los austeníticos comunes (304, 316) son especialmente "
            "sensibles.",
            "Chlorides (Cl⁻, from salt, seawater, produced water) attack the passive chromium "
            "oxide film that protects stainless steels. The chloride ion is small and very "
            "mobile: it breaks the film at weak spots and forms pits. If there is also tensile "
            "stress and temperature (above about 60 °C), branched cracks grow from those pits "
            "through the grains: chloride stress corrosion cracking (Cl-SCC). Common "
            "austenitics (304, 316) are especially susceptible."),
        "why": (
            "La raíz de la vaina tiene tensión residual de mecanizado y soldadura: es el lugar "
            "típico de Cl-SCC. Una fisura así no se ve desde afuera hasta que filtra.",
            "The well root has residual stress from machining and welding: the typical place "
            "for Cl-SCC. Such a crack is not visible from outside until it leaks."),
        "worked": (
            "Agua producida con 20 000 ppm de cloruros a 90 °C: 316 descartado; opciones "
            "dúplex 2205 o super dúplex, aleaciones de níquel (Inconel 625, Hastelloy C-276) o "
            "titanio. TS penaliza los materiales sensibles desde 50 ppm y 60 °C.",
            "Produced water with 20,000 ppm chlorides at 90 °C: 316 ruled out; options duplex "
            "2205 or super duplex, nickel alloys (Inconel 625, Hastelloy C-276) or titanium. TS "
            "penalizes susceptible materials from 50 ppm and 60 °C."),
        "mistakes": (
            "- Elegir 316 «porque es inoxidable».\n"
            "- Olvidar los cloruros del agua de lavado o del aislamiento húmedo exterior.",
            "- Choosing 316 «because it is stainless».\n"
            "- Forgetting chlorides from wash water or wet external insulation."),
    },
    "f.ph": {
        "essence": (
            "El pH mide la concentración de iones hidrógeno (H⁺): pH 7 es neutro, menor es "
            "ácido, mayor es alcalino, en escala logarítmica (pH 4 es diez veces más ácido que "
            "pH 5). Los H⁺ disuelven las capas protectoras de óxido y aceleran la corrosión; "
            "en servicio con H₂S, un pH bajo aumenta mucho la entrada de hidrógeno al acero.",
            "pH measures the concentration of hydrogen ions (H⁺): pH 7 is neutral, lower is "
            "acidic, higher alkaline, on a log scale (pH 4 is ten times more acidic than pH 5). "
            "H⁺ ions dissolve protective oxide films and speed up corrosion; in H₂S service, "
            "low pH greatly increases hydrogen uptake by steel."),
        "why": (
            "Orienta la elección de material junto con cloruros y H₂S. El acero al carbono "
            "aguanta bien entre pH 9 y 11 y se corroe rápido por debajo de 5.",
            "It guides material choice together with chlorides and H₂S. Carbon steel copes "
            "well between pH 9 and 11 and corrodes fast below 5."),
        "worked": (
            "Agua ácida pH 4 con CO₂: acero al carbono con corrosión de varios mm/año; 316 "
            "resiste si no hay cloruros altos.",
            "Sour water pH 4 with CO₂: carbon steel corrodes several mm/year; 316 resists if "
            "chlorides are not high."),
        "mistakes": ("- Medir el pH a temperatura ambiente: cambia con la temperatura.",
                     "- Measuring pH at room temperature: it changes with temperature."),
    },
    "f.nace": {
        "essence": (
            "Marca que el servicio es ácido según NACE MR0175 / ISO 15156 (H₂S con agua). La "
            "norma no prohíbe metales sino que fija condiciones para que no fisuren por "
            "hidrógeno: dureza máxima, tratamiento térmico y composición, porque una "
            "microestructura dura atrapa más hidrógeno y fisura con menos esfuerzo.",
            "It flags the service as sour per NACE MR0175 / ISO 15156 (H₂S with water). The "
            "standard does not ban metals but sets conditions so they do not crack from "
            "hydrogen: maximum hardness, heat treatment and composition, because a hard "
            "microstructure traps more hydrogen and cracks at lower stress."),
        "why": (
            "Activa el filtrado de materiales y los requisitos de dureza en la hoja de datos. "
            "El proveedor debe certificar el cumplimiento (por ejemplo con ensayos de dureza en "
            "el certificado de material).",
            "It enables material filtering and hardness requirements on the datasheet. The "
            "supplier must certify compliance (for example with hardness tests on the material "
            "certificate)."),
        "worked": (
            "316 recocido: aceptado con dureza ≤ 22 HRC. Acero al carbono: ≤ 22 HRC (≈ 250 HV) "
            "también en soldadura y zona afectada.",
            "Annealed 316: accepted with hardness ≤ 22 HRC. Carbon steel: ≤ 22 HRC (≈ 250 HV) "
            "also in weld and heat-affected zone."),
        "mistakes": (
            "- Marcarlo sin pedir certificado de dureza.\n"
            "- Olvidar el Stellite: algunas aleaciones de recubrimiento tienen requisitos "
            "propios.",
            "- Ticking it without requesting a hardness certificate.\n"
            "- Forgetting Stellite: some overlay alloys have their own requirements."),
    },
    "f.erosive": {
        "essence": (
            "Indica que el fluido arrastra partículas (arena, catalizador, óxido) o gotas a "
            "alta velocidad. Cada partícula que impacta arranca microvirutas o deforma la "
            "superficie; con millones de impactos por segundo, la punta pierde material. La "
            "pérdida crece aproximadamente con el cubo de la velocidad.",
            "It states that the fluid carries particles (sand, catalyst, rust) or droplets at "
            "high velocity. Each impacting particle tears micro-chips or deforms the surface; "
            "with millions of impacts per second the tip loses material. Loss grows roughly "
            "with the cube of velocity."),
        "why": (
            "Con sólidos, la vida de la vaina puede ser de meses. TS recomienda recubrimientos "
            "duros (Stellite, carburo de tungsteno), materiales más duros o más sobreespesor.",
            "With solids the well life may be months. TS recommends hard coatings (Stellite, "
            "tungsten carbide), harder materials or more allowance."),
        "worked": (
            "Si a 10 m/s la punta pierde 0,2 mm/año, a 15 m/s pierde unos 0,2 × 1,5³ = "
            "0,68 mm/año.",
            "If at 10 m/s the tip loses 0.2 mm/year, at 15 m/s it loses about 0.2 × 1.5³ = "
            "0.68 mm/year."),
        "mistakes": (
            "- No marcarlo en pozos de gas con arena.\n"
            "- Usar C = 100 para la velocidad erosional con sólidos.",
            "- Not ticking it in sandy gas wells.\n"
            "- Using C = 100 for erosional velocity with solids."),
    },
}
