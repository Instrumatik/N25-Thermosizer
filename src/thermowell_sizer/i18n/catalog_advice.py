"""Textos de las advertencias y recomendaciones complementarias (``core.advisories``)."""

from __future__ import annotations

from typing import Final

ADVICE_ES: Final[dict[str, str]] = {
    "adv.erosion": (
        "Servicio erosivo: V = {v} supera la velocidad erosiva Ve = {ve} (V/Ve = {ratio}). "
        "Reduzca la velocidad o use recubrimiento duro (Stellite 6, carburo de tungsteno), un "
        "perfil cónico y un material más resistente; prevea inspecciones periódicas."
    ),
    "adv.erosion_watch": (
        "Posible erosión: V/Ve = {ratio} (V = {v}, Ve = {ve}). Considere recubrimiento duro "
        "o un sobreespesor de corrosión/erosión."
    ),
    "adv.solids": (
        "Fluido con sólidos o abrasivo: la velocidad erosiva real es menor que la de "
        "referencia. Recomendado recubrimiento duro en el vástago y la punta."
    ),
    "adv.immersion_short": (
        "Inmersión expuesta {exposed} menor que la recomendada {needed} (largo sensible + "
        "{factor} veces el diámetro de punta). Puede haber error por conducción: alargue la "
        "inserción si la verificación mecánica lo permite."
    ),
    "adv.tip_hits_wall": (
        "La parte expuesta ({exposed}) es igual o mayor que el diámetro interno ({id}): la "
        "punta toca la pared opuesta. Acorte el termopozo o use montaje en codo o inclinado."
    ),
    "adv.tip_near_wall": (
        "La punta queda muy cerca de la pared opuesta ({exposed} de {id}). Verifique "
        "tolerancias, dilatación y el espesor real de la tubería."
    ),
    "adv.shielded_length": (
        "La brida de montaje está a {nozzle} de la pared interna pero L0 = 0. Si el vástago "
        "dentro de la conexión de montaje queda "
        "protegido del flujo, cargue L0 para un cálculo menos conservador."
    ),
    "adv.nozzle_blocked": (
        "El vástago (A = {a}) no pasa por la conexión de montaje (diámetro interno "
        "{nozzle_id}). Elija "
        "otra conexión o un termopozo más delgado en la raíz."
    ),
    "adv.nozzle_tight": (
        "Huelgo muy chico entre el vástago (A = {a}) y la conexión de montaje "
        "({nozzle_id}): dificulta el "
        "montaje y puede dañar el termopozo."
    ),
    "adv.sensor_no_fit": (
        "El sensor ({sensor}) no entra en el agujero ({d}). Cambie el diámetro del sensor o "
        "del agujero."
    ),
    "adv.sensor_tight": (
        "Huelgo agujero-sensor muy justo ({d} para un sensor de {sensor}): riesgo de "
        "trabamiento por dilatación o suciedad."
    ),
    "adv.sensor_loose": (
        "Huelgo agujero-sensor grande ({d} para un sensor de {sensor}): la respuesta será "
        "lenta. Use un sensor más grueso, resorte de empuje o pasta conductora."
    ),
    "adv.spring": (
        "Sensor sin resorte de empuje: se recomienda para asegurar el contacto con el fondo "
        "del termopozo."
    ),
    "adv.sensor_range": (
        "La temperatura de servicio queda fuera del rango habitual del sensor elegido "
        "({low} a {high}). Para alta temperatura use termopar tipo K o N; para servicio "
        "criogénico, RTD o termopar tipo T."
    ),
    "adv.ceramic": (
        "Temperatura muy alta: evalúe funda cerámica o termopozo especial (llama directa, "
        "atmósferas reductoras, termopares de platino)."
    ),
    "adv.dial_range": (
        "Escala recomendada para el termómetro: {low} a {high} (la operación queda en el "
        "tercio central y el diseño dentro de la escala)."
    ),
    "adv.dial_none": (
        "Ninguna escala normalizada deja la operación en el tercio central: especifique una "
        "escala especial o use un transmisor con indicador."
    ),
    "adv.coating_temperature": (
        "La temperatura de diseño supera la máxima del recubrimiento ({limit})."
    ),
    "adv.threaded_service": (
        "Conexión roscada en servicio inflamable, tóxico o de presión elevada: se recomienda "
        "conexión bridada o soldada."
    ),
    "adv.angle_missing": (
        "Montaje inclinado sin ángulo cargado: la posición de la punta se evalúa como "
        "perpendicular. Indique el ángulo entre el termopozo y el eje de la tubería."
    ),
    "adv.vessel_immersion": (
        "Recipiente: la punta entra {exposed} en el fluido, menos que la inmersión habitual "
        "de {min}. En un fluido quieto la transferencia de calor es baja y puede haber "
        "estratificación: alargue la inserción o verifique el error por conducción."
    ),
    "adv.thread_g": (
        "Rosca G (ISO 228-1, BSPP, paralela): no sella en la rosca, sino con una junta o un "
        "anillo en la cara de apoyo. Especifique la junta y confirme el rating con el "
        "fabricante; en plantas con especificación ASME suele pedirse NPT."
    ),
    "adv.hydro_test": (
        "Prueba hidráulica de referencia: {p} (1,5 × presión de diseño). Confirme la presión "
        "interna y externa con la especificación del proyecto."
    ),
    "insp.title": "Ensayos y documentación",
    "insp.hydro": (
        "Prueba hidrostática a {p} (1,5 × presión de diseño): externa sobre el vástago y, en "
        "bridados, también de la unión brida-vástago."
    ),
    "insp.weld_flange": (
        "Soldadura brida-vástago a penetración completa, con tintas penetrantes y radiografía "
        "o ultrasonido."
    ),
    "insp.weld_field": (
        "Soldadura a la línea según ASME B31.3 (o B31.1), con procedimiento y soldador "
        "calificados y tintas penetrantes."
    ),
    "insp.pmi": "Identificación positiva de material (PMI) del termopozo y de la brida.",
    "insp.certificates": (
        "Certificados de material EN 10204 3.1 con número de colada del termopozo y de la "
        "brida."
    ),
    "insp.nace": (
        "Certificado de cumplimiento NACE MR0175 / ISO 15156 (dureza y tratamiento térmico)."
    ),
    "insp.dimensional": (
        "Control dimensional: agujero concéntrico, fondo con apoyo para el sensor y vástago "
        "pulido (Ra ≤ 0,8 µm)."
    ),
    "insp.marking": (
        "Marcado indeleble: tag {tag}, material, tamaño de conexión, rating y números de colada."
    ),
    "insp.calc_report": "Memoria de cálculo ASME PTC 19.3 TW firmada, incluida en la entrega.",
    "insp.hydro_short": "Prueba hidrostática {p}",
    "insp.weld_flange_short": "Soldadura a penetración completa + PT y RT/UT",
    "insp.weld_field_short": "Soldadura a línea B31.3 + PT",
    "insp.pmi_short": "PMI",
    "insp.certificates_short": "Certificados EN 10204 3.1",
    "insp.nace_short": "Certificado NACE MR0175",
    "insp.dimensional_short": "Control dimensional, Ra ≤ 0,8 µm",
    "insp.marking_short": "Marcado: tag, material, conexión, rating, colada",
    "insp.calc_report_short": "Memoria ASME PTC 19.3 TW",
    "adv.phase_is_liquid": (
        "Con la presión y la temperatura de operación el fluido está LÍQUIDO, no en el estado "
        "del tipo elegido. Revise el tipo de fluido o las condiciones; el cálculo usa la fase "
        "real."
    ),
    "adv.phase_is_gas": (
        "Con la presión y la temperatura de operación el fluido es GAS o VAPOR, no líquido. "
        "Revise el tipo de fluido o las condiciones; el cálculo usa la fase real."
    ),
    "adv.phase_is_steam": (
        "Con la presión y la temperatura de operación el agua está como VAPOR (steam), no "
        "líquida. Revise el tipo de fluido o las condiciones; el cálculo usa la fase real."
    ),
    "adv.phase_is_two_phase": (
        "Con la presión y la temperatura de operación el fluido está en saturación (bifásico). "
        "Revise el tipo de fluido o las condiciones."
    ),
    "adv.title": "Advertencias y recomendaciones",
    "adv.level.critical": "Crítico",
    "adv.level.warning": "Advertencia",
    "adv.level.info": "Recomendación",
}

ADVICE_EN: Final[dict[str, str]] = {
    "adv.erosion": (
        "Erosive service: V = {v} exceeds the erosional velocity Ve = {ve} (V/Ve = {ratio}). "
        "Reduce velocity or use a hard coating (Stellite 6, tungsten carbide), a tapered "
        "shank and a more resistant material; plan periodic inspections."
    ),
    "adv.erosion_watch": (
        "Possible erosion: V/Ve = {ratio} (V = {v}, Ve = {ve}). Consider a hard coating or "
        "a corrosion/erosion allowance."
    ),
    "adv.solids": (
        "Fluid with solids or abrasive: the actual erosional velocity is lower than the "
        "reference. A hard coating on shank and tip is recommended."
    ),
    "adv.immersion_short": (
        "Exposed immersion {exposed} below the recommended {needed} (sensitive length + "
        "{factor} tip diameters). Conduction error may occur: lengthen the insertion if the "
        "mechanical check allows it."
    ),
    "adv.tip_hits_wall": (
        "The exposed length ({exposed}) is equal to or larger than the inside diameter "
        "({id}): the tip touches the opposite wall. Shorten the thermowell or use an elbow "
        "or angled installation."
    ),
    "adv.tip_near_wall": (
        "The tip is very close to the opposite wall ({exposed} of {id}). Check tolerances, "
        "expansion and the actual pipe wall."
    ),
    "adv.shielded_length": (
        "There is a {nozzle} nozzle but L0 = 0. If the shank inside the nozzle is shielded "
        "from the flow, enter L0 for a less conservative calculation."
    ),
    "adv.nozzle_blocked": (
        "The shank (A = {a}) does not fit through the nozzle (inside diameter {nozzle_id}). "
        "Choose another connection or a thinner root."
    ),
    "adv.nozzle_tight": (
        "Very small clearance between the shank (A = {a}) and the nozzle ({nozzle_id}): "
        "installation is difficult and the thermowell may be damaged."
    ),
    "adv.sensor_no_fit": (
        "The sensor ({sensor}) does not fit in the bore ({d}). Change the sensor or bore "
        "diameter."
    ),
    "adv.sensor_tight": (
        "Very tight bore-sensor clearance ({d} for a {sensor} sensor): risk of seizing due to "
        "expansion or dirt."
    ),
    "adv.sensor_loose": (
        "Large bore-sensor clearance ({d} for a {sensor} sensor): response will be slow. Use "
        "a thicker sensor, a spring or conductive paste."
    ),
    "adv.spring": (
        "Sensor without spring: recommended to ensure contact with the bottom of the "
        "thermowell."
    ),
    "adv.sensor_range": (
        "The service temperature is outside the usual range of the selected sensor ({low} to "
        "{high}). For high temperature use a type K or N thermocouple; for cryogenic service, "
        "an RTD or type T thermocouple."
    ),
    "adv.ceramic": (
        "Very high temperature: consider a ceramic sheath or special thermowell (direct "
        "flame, reducing atmospheres, platinum thermocouples)."
    ),
    "adv.dial_range": (
        "Recommended thermometer scale: {low} to {high} (operation in the middle third, "
        "design within the scale)."
    ),
    "adv.dial_none": (
        "No standard scale places operation in the middle third: specify a special scale or "
        "use a transmitter with indicator."
    ),
    "adv.coating_temperature": "The design temperature exceeds the coating limit ({limit}).",
    "adv.threaded_service": (
        "Threaded connection in flammable, toxic or high-pressure service: a flanged or "
        "welded connection is recommended."
    ),
    "adv.angle_missing": (
        "Angled mounting without an angle: the tip position is evaluated as perpendicular. "
        "Enter the angle between the thermowell and the pipe axis."
    ),
    "adv.vessel_immersion": (
        "Vessel: the tip goes {exposed} into the fluid, less than the usual immersion of "
        "{min}. In a still fluid heat transfer is low and stratification may occur: lengthen "
        "the insertion or check the conduction error."
    ),
    "adv.thread_g": (
        "G thread (ISO 228-1, BSPP, parallel): it does not seal on the thread but with a "
        "gasket or ring on the seating face. Specify the gasket and confirm the rating with "
        "the manufacturer; plants with ASME specifications usually require NPT."
    ),
    "adv.hydro_test": (
        "Reference hydrostatic test: {p} (1.5 × design pressure). Confirm internal and "
        "external test pressures with the project specification."
    ),
    "insp.title": "Testing and documentation",
    "insp.hydro": (
        "Hydrostatic test at {p} (1.5 × design pressure): external on the shank and, on "
        "flanged wells, also of the flange-to-shank joint."
    ),
    "insp.weld_flange": (
        "Full-penetration flange-to-shank weld, with dye penetrant and radiographic or "
        "ultrasonic examination."
    ),
    "insp.weld_field": (
        "Weld to the line per ASME B31.3 (or B31.1), with qualified procedure and welder and "
        "dye penetrant examination."
    ),
    "insp.pmi": "Positive material identification (PMI) of the thermowell and the flange.",
    "insp.certificates": (
        "EN 10204 3.1 material certificates with heat numbers of thermowell and flange."
    ),
    "insp.nace": "NACE MR0175 / ISO 15156 compliance certificate (hardness and heat treatment).",
    "insp.dimensional": (
        "Dimensional check: concentric bore, bottom seat for the sensor and polished shank "
        "(Ra ≤ 0.8 µm)."
    ),
    "insp.marking": (
        "Permanent marking: tag {tag}, material, connection size, rating and heat numbers."
    ),
    "insp.calc_report": "Signed ASME PTC 19.3 TW calculation report included in the delivery.",
    "insp.hydro_short": "Hydrostatic test {p}",
    "insp.weld_flange_short": "Full-penetration weld + PT and RT/UT",
    "insp.weld_field_short": "Line weld per B31.3 + PT",
    "insp.pmi_short": "PMI",
    "insp.certificates_short": "EN 10204 3.1 certificates",
    "insp.nace_short": "NACE MR0175 certificate",
    "insp.dimensional_short": "Dimensional check, Ra ≤ 0.8 µm",
    "insp.marking_short": "Marking: tag, material, connection, rating, heat",
    "insp.calc_report_short": "ASME PTC 19.3 TW calculation report",
    "adv.phase_is_liquid": (
        "At the operating pressure and temperature the fluid is LIQUID, not the chosen type. "
        "Check the fluid type or the conditions; the calculation uses the actual phase."
    ),
    "adv.phase_is_gas": (
        "At the operating pressure and temperature the fluid is GAS or VAPOR, not liquid. "
        "Check the fluid type or the conditions; the calculation uses the actual phase."
    ),
    "adv.phase_is_steam": (
        "At the operating pressure and temperature the water is STEAM, not liquid. Check the "
        "fluid type or the conditions; the calculation uses the actual phase."
    ),
    "adv.phase_is_two_phase": (
        "At the operating pressure and temperature the fluid is saturated (two-phase). Check "
        "the fluid type or the conditions."
    ),
    "adv.title": "Warnings and recommendations",
    "adv.level.critical": "Critical",
    "adv.level.warning": "Warning",
    "adv.level.info": "Recommendation",
}
