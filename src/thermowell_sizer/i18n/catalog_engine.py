"""Textos del motor: criterios, notas, alternativas y pasos de la memoria (redacción propia)."""

from __future__ import annotations

from typing import Final

ENGINE_ES: Final[dict[str, str]] = {
    # Criterios
    "check.scope_ok": "La geometría está dentro del alcance de la norma.",
    "check.scope_fail": (
        "La geometría está fuera del alcance de la norma: revise los avisos de validación."
    ),
    "check.material_temperature": (
        "La temperatura de diseño supera la máxima de uso del material. Elija otro material."
    ),
    "check.pressure_rating": "Presión de diseño frente a la presión externa admisible P_r.",
    "check.pressure_high_service": (
        "Presión admisible mayor que 103 MPa: verifique con ASME BPVC VIII-3 o B31.3 cap. IX."
    ),
    "check.flange_rating": "Presión de diseño frente al rating de la brida (ASME B16.5).",
    "check.flange_rating_missing": (
        "Falta el rating de la brida a la temperatura de diseño (ASME B16.5)."
    ),
    "check.flange_derated": (
        "La brida tiene más capacidad que el vástago o la punta: su rating se limita a P_r."
    ),
    "check.steady_stress": "Esfuerzo estacionario de von Mises frente a 1,5·S.",
    "check.dynamic_stress": "Amplitud del esfuerzo oscilante frente al límite de fatiga.",
    "check.low_velocity_exempt": (
        "Velocidad menor que 0,64 m/s: no se requieren los cálculos de vibración."
    ),
    "check.no_vortex_shedding": "Re < 22: no hay desprendimiento de vórtices.",
    "check.frequency_scruton_all": (
        "Re < 10⁵ y N_Sc > 64: ambas resonancias suprimidas; por encima de 0,8·f_n^c "
        "deben analizarse modos superiores."
    ),
    "check.frequency_scruton_inline": (
        "Re < 10⁵ y N_Sc > 2,5: resonancia en línea suprimida; se exige fs < 0,8·f_n^c."
    ),
    "check.frequency_inline_ok": (
        "El termopozo resiste la resonancia en línea: se exige fs < 0,8·f_n^c."
    ),
    "check.frequency_inline_limited": (
        "El termopozo no resiste la resonancia en línea: se exige fs < 0,4·f_n^c."
    ),
    "check.frequency_inline_passage": (
        "Paso transitorio por la resonancia en línea aceptado con condiciones (gas, solo "
        "en arranque y parada)."
    ),
    "check.frequency_supercritical": (
        "fs supera la frecuencia natural: operación supercrítica, fuera del alcance."
    ),
    "check.lockin_dwell": (
        "En régimen permanente fs cae en la banda de captura en línea (0,4 a 0,6·f_n^c)."
    ),
    "check.lockin_clear": "En régimen permanente fs queda fuera de la banda de captura.",
    "check.fatigue_data_missing": (
        "El material no figura en la tabla de límites de fatiga: se usa el valor de su "
        "clase como referencia; la norma exige determinarlo por ensayo."
    ),
    # Notas
    "note.two_phase": (
        "Flujo bifásico: las correlaciones son para una sola fase; use la condición más "
        "desfavorable y juicio de ingeniería."
    ),
    "note.elbow_downstream": (
        "Montaje en codo con la punta aguas abajo: se calcula como si el flujo fuera "
        "normal a todo el vástago."
    ),
    "note.elbow_upstream": (
        "Montaje en codo con la punta aguas arriba: se evalúa como montaje perpendicular "
        "(conservador)."
    ),
    "note.angled": "Montaje inclinado: se evalúa como perpendicular (conservador).",
    "note.vessel": (
        "Montaje en recipiente: sin flujo (velocidad 0) no hay desprendimiento de vórtices y "
        "la verificación de frecuencia no aplica; se verifican presión, temperatura del "
        "material y esfuerzo estático. Si hay agitación, cargue un caso con su velocidad."
    ),
    "note.sanitary_compliance": (
        "Conexión sanitaria: la norma no cubre su flexibilidad; se usa H_c de conexión "
        "roscada como aproximación."
    ),
    "note.high_temperature_fe": (
        "Temperatura mayor que 427 °C: considere un factor ambiental F_E < 1."
    ),
    "note.supplier_rating": "Rating de proveedor: H_a,f = 1 según el párr. 9-2.",
    "note.higher_modes": "Por encima de 0,8·f_n^c deben analizarse modos superiores.",
    "note.inline_passage_conditions": (
        "Verifique todas las condiciones del párr. 6-8.5: fluido gaseoso, sin permanencia "
        "en resonancia, menos de 10¹¹ ciclos, sin efectos metalúrgicos y consecuencias "
        "de falla aceptables."
    ),
    "note.no_velocity_collars": (
        "No se proponen collares de soporte: la norma vigente los deja fuera de su "
        "alcance y desaconseja su uso."
    ),
    # Alternativas
    "opt.reason.reduce_length": (
        "Reducir L sube la frecuencia natural (∝ 1/L²) y baja el momento flector (∝ L²)."
    ),
    "opt.reason.increase_root": (
        "Una raíz más gruesa aumenta la rigidez y el módulo resistente donde el esfuerzo "
        "es máximo."
    ),
    "opt.reason.tapered_profile": (
        "El perfil cónico concentra material en la raíz: más frecuencia natural sin "
        "cambiar la punta ni la respuesta térmica."
    ),
    "opt.reason.change_material": (
        "Un material con mayor módulo o mayor límite de fatiga mejora frecuencia y esfuerzos."
    ),
    "opt.reason.change_connection": (
        "Una conexión bridada es más rígida que una roscada y tiene menor concentración "
        "de esfuerzos."
    ),
    # Pasos de la memoria
    "trace.v": "Velocidad del fluido",
    "trace.re": "Número de Reynolds sobre el diámetro de punta",
    "trace.ns": "Número de Strouhal",
    "trace.fs": "Frecuencia de desprendimiento de vórtices",
    "trace.da": "Diámetro medio del vástago",
    "trace.i": "Momento de inercia de la sección",
    "trace.m": "Masa por unidad de longitud",
    "trace.fa": "Frecuencia natural aproximada del voladizo",
    "trace.hf": "Factor de corrección de forma H_f",
    "trace.haf": "Factor de masa añadida del fluido",
    "trace.has": "Factor de masa del sensor",
    "trace.fn": "Frecuencia natural con soporte ideal",
    "trace.hc": "Factor de flexibilidad del soporte",
    "trace.fnc": "Frecuencia natural instalada",
    "trace.nsc": "Número de Scruton",
    "trace.ft": "Factor de temperatura del límite de fatiga",
    "trace.sf_allow": "Amplitud de esfuerzo admisible",
    "trace.gsp": "Parámetro geométrico G en el soporte",
    "trace.grd": "Parámetro geométrico G en la base del tramo reducido",
    "trace.kt": "Factor de concentración de esfuerzos",
    "trace.pd_steady": "Presión de arrastre estacionario",
    "trace.sr": "Esfuerzo radial por presión",
    "trace.st": "Esfuerzo tangencial por presión",
    "trace.sa": "Esfuerzo axial por presión",
    "trace.sd_steady": "Esfuerzo por arrastre estacionario",
    "trace.smax": "Esfuerzo longitudinal máximo",
    "trace.vm": "Esfuerzo equivalente de von Mises",
    "trace.r": "Relación de frecuencias transversal",
    "trace.r_prime": "Relación de frecuencias en línea",
    "trace.fm": "Factor de magnificación transversal",
    "trace.fm_prime": "Factor de magnificación en línea",
    "trace.pd_osc": "Presión de arrastre oscilante",
    "trace.pl_osc": "Presión de sustentación oscilante",
    "trace.sd_osc": "Esfuerzo oscilante en línea",
    "trace.sl_osc": "Esfuerzo oscilante transversal",
    "trace.so": "Amplitud pico combinada",
    "trace.vir": "Velocidad de resonancia en línea",
    "trace.pd_ir": "Presión de arrastre oscilante en resonancia en línea",
    "trace.sd_ir": "Esfuerzo oscilante en resonancia en línea",
    "trace.so_ir": "Amplitud pico en resonancia en línea",
    "trace.pc": "Presión externa admisible del vástago",
    "trace.pt": "Presión externa admisible de la punta",
    "trace.pr": "Presión externa nominal del termopozo",
}

ENGINE_EN: Final[dict[str, str]] = {
    "check.scope_ok": "Geometry is within the scope of the standard.",
    "check.scope_fail": "Geometry is outside the scope of the standard: review the warnings.",
    "check.material_temperature": (
        "Design temperature exceeds the material's maximum. Choose another material."
    ),
    "check.pressure_rating": "Design pressure versus external pressure rating P_r.",
    "check.pressure_high_service": (
        "Rating above 103 MPa: verify with ASME BPVC VIII-3 or B31.3 Chapter IX."
    ),
    "check.flange_rating": "Design pressure versus flange rating (ASME B16.5).",
    "check.flange_rating_missing": "Flange rating at design temperature (ASME B16.5) missing.",
    "check.flange_derated": (
        "The flange is stronger than the shank or tip: its rating is limited to P_r."
    ),
    "check.steady_stress": "Steady-state von Mises stress versus 1.5·S.",
    "check.dynamic_stress": "Oscillating stress amplitude versus fatigue limit.",
    "check.low_velocity_exempt": "Velocity below 0.64 m/s: vibration checks not required.",
    "check.no_vortex_shedding": "Re < 22: no vortex shedding.",
    "check.frequency_scruton_all": (
        "Re < 10⁵ and N_Sc > 64: both resonances suppressed; above 0.8·f_n^c higher modes "
        "must be analysed."
    ),
    "check.frequency_scruton_inline": (
        "Re < 10⁵ and N_Sc > 2.5: in-line resonance suppressed; fs < 0.8·f_n^c required."
    ),
    "check.frequency_inline_ok": (
        "The thermowell withstands in-line resonance: fs < 0.8·f_n^c required."
    ),
    "check.frequency_inline_limited": (
        "The thermowell does not withstand in-line resonance: fs < 0.4·f_n^c required."
    ),
    "check.frequency_inline_passage": (
        "Transient passage through in-line resonance accepted with conditions (gas, "
        "start-up and shutdown only)."
    ),
    "check.frequency_supercritical": (
        "fs exceeds the natural frequency: supercritical operation, outside the scope."
    ),
    "check.lockin_dwell": "At steady state fs lies in the in-line lock-in band (0.4-0.6·f_n^c).",
    "check.lockin_clear": "At steady state fs lies outside the lock-in band.",
    "check.fatigue_data_missing": (
        "Material not in the fatigue-limit table: its class value is used as reference; "
        "the standard requires test data."
    ),
    "note.two_phase": (
        "Two-phase flow: correlations are single-phase; use the worst condition and "
        "engineering judgement."
    ),
    "note.elbow_downstream": (
        "Elbow mounting, tip downstream: computed as if flow were normal to the whole shank."
    ),
    "note.elbow_upstream": (
        "Elbow mounting, tip upstream: evaluated as perpendicular (conservative)."
    ),
    "note.angled": "Angled mounting: evaluated as perpendicular (conservative).",
    "note.vessel": (
        "Vessel mounting: with no flow (velocity 0) there is no vortex shedding and the "
        "frequency check does not apply; pressure, material temperature and steady stress "
        "are checked. If there is agitation, enter a case with its velocity."
    ),
    "note.sanitary_compliance": (
        "Sanitary connection: its compliance is not covered; the threaded H_c is used."
    ),
    "note.high_temperature_fe": "Temperature above 427 °C: consider F_E < 1.",
    "note.supplier_rating": "Supplier rating: H_a,f = 1 per para. 9-2.",
    "note.higher_modes": "Above 0.8·f_n^c higher modes must be analysed.",
    "note.inline_passage_conditions": (
        "Check every condition of para. 6-8.5: gas, no dwelling at resonance, fewer than "
        "10¹¹ cycles, no metallurgical effects and acceptable failure consequences."
    ),
    "note.no_velocity_collars": (
        "Support collars are not proposed: the current standard leaves them outside its "
        "scope and discourages their use."
    ),
    "opt.reason.reduce_length": (
        "Shorter L raises the natural frequency (∝ 1/L²) and lowers bending (∝ L²)."
    ),
    "opt.reason.increase_root": (
        "A thicker root increases stiffness and section modulus where stress peaks."
    ),
    "opt.reason.tapered_profile": (
        "A tapered shank puts material at the root: higher natural frequency with the "
        "same tip and thermal response."
    ),
    "opt.reason.change_material": (
        "Higher modulus or fatigue limit improves frequency and stress margins."
    ),
    "opt.reason.change_connection": (
        "A flanged connection is stiffer than a threaded one and has lower stress "
        "concentration."
    ),
    "trace.v": "Fluid velocity",
    "trace.re": "Reynolds number on tip diameter",
    "trace.ns": "Strouhal number",
    "trace.fs": "Vortex shedding frequency",
    "trace.da": "Average shank diameter",
    "trace.i": "Second moment of area",
    "trace.m": "Mass per unit length",
    "trace.fa": "Approximate cantilever natural frequency",
    "trace.hf": "Shape correction factor H_f",
    "trace.haf": "Fluid added-mass factor",
    "trace.has": "Sensor mass factor",
    "trace.fn": "Natural frequency, ideal support",
    "trace.hc": "Support compliance factor",
    "trace.fnc": "Installed natural frequency",
    "trace.nsc": "Scruton number",
    "trace.ft": "Fatigue temperature factor",
    "trace.sf_allow": "Allowable stress amplitude",
    "trace.gsp": "Geometric parameter G at support",
    "trace.grd": "Geometric parameter G at reduced-diameter base",
    "trace.kt": "Stress concentration factor",
    "trace.pd_steady": "Steady drag pressure",
    "trace.sr": "Radial pressure stress",
    "trace.st": "Tangential pressure stress",
    "trace.sa": "Axial pressure stress",
    "trace.sd_steady": "Steady drag stress",
    "trace.smax": "Maximum longitudinal stress",
    "trace.vm": "Von Mises equivalent stress",
    "trace.r": "Transverse frequency ratio",
    "trace.r_prime": "In-line frequency ratio",
    "trace.fm": "Transverse magnification factor",
    "trace.fm_prime": "In-line magnification factor",
    "trace.pd_osc": "Oscillating drag pressure",
    "trace.pl_osc": "Oscillating lift pressure",
    "trace.sd_osc": "In-line oscillating stress",
    "trace.sl_osc": "Transverse oscillating stress",
    "trace.so": "Combined peak amplitude",
    "trace.vir": "In-line resonance velocity",
    "trace.pd_ir": "Oscillating drag pressure at in-line resonance",
    "trace.sd_ir": "Oscillating stress at in-line resonance",
    "trace.so_ir": "Peak amplitude at in-line resonance",
    "trace.pc": "Shank external pressure rating",
    "trace.pt": "Tip external pressure rating",
    "trace.pr": "Thermowell external pressure rating",
}
