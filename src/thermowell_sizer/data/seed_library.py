"""Glosario bilingüe y fichas de normas. Redacción propia: no se copia texto de normas."""

from __future__ import annotations

from typing import Final

# (id, término ES, término EN, definición ES, definición EN, fórmula LaTeX, diagrama)
GLOSSARY: Final[tuple[tuple[str, str, str, str, str, str, str], ...]] = (
    ("thermowell", "Termopozo (termovaina)", "Thermowell",
     "Tubo cerrado en un extremo que se inserta en el proceso y aloja al sensor de "
     "temperatura, separándolo del fluido y de la presión.",
     "Closed-end tube inserted in the process that houses the temperature sensor and "
     "isolates it from the fluid and pressure.", "", "geometry"),
    ("insertion", "Longitud de inserción (U)", "Insertion length (U)",
     "Distancia desde la cara de la conexión hasta la punta del termopozo.",
     "Distance from the connection face to the thermowell tip.", "", "geometry"),
    ("unsupported_length", "Longitud no soportada (L)", "Unsupported length (L)",
     "Distancia desde la punta hasta el plano de soporte; es la longitud que vibra.",
     "Distance from the tip to the support plane; the length that vibrates.", "", "geometry"),
    ("lag", "Longitud de extensión (lag, T)", "Lag length (T)",
     "Tramo adicional entre la conexión y la cabeza para atravesar aislamiento o alejar "
     "la electrónica del calor.",
     "Extra length between the connection and the head to clear insulation.", "",
     "geometry"),
    ("bore", "Agujero (bore, d)", "Bore (d)",
     "Diámetro interior donde se aloja el sensor.", "Inner diameter that houses the sensor.",
     "", "geometry"),
    ("root_diameter", "Diámetro de raíz (A)", "Root diameter (A)",
     "Diámetro exterior del vástago en el plano de soporte.",
     "Outside shank diameter at the support plane.", "", "geometry"),
    ("tip_diameter", "Diámetro de punta (B)", "Tip diameter (B)",
     "Diámetro exterior del vástago en la punta.", "Outside shank diameter at the tip.", "",
     "geometry"),
    ("support_plane", "Plano de soporte", "Support plane",
     "Sección donde el termopozo queda empotrado: cara de la brida, inicio de la rosca o "
     "punto medio del collar soldado.",
     "Section where the thermowell is clamped: flange face, thread start or weld collar "
     "midpoint.", "", "geometry"),
    ("fillet", "Radio de acuerdo (b)", "Fillet radius (b)",
     "Radio de la transición entre el vástago y la base; reduce la concentración de "
     "esfuerzos y la flexibilidad del soporte.",
     "Radius of the shank-to-base transition; lowers stress concentration.", "", "geometry"),
    ("vortex_shedding", "Desprendimiento de vórtices", "Vortex shedding",
     "Formación alternada de remolinos detrás de un cuerpo en un flujo, que genera fuerzas "
     "periódicas sobre él.",
     "Alternating formation of eddies behind a body in a flow, which creates periodic "
     "forces.", "", ""),
    ("wake_frequency", "Frecuencia de estela (fs)", "Wake frequency (fs)",
     "Frecuencia con que se desprenden los vórtices; crece con la velocidad.",
     "Frequency at which vortices are shed; grows with velocity.", r"f_s = N_S V / B", ""),
    ("strouhal", "Número de Strouhal (N_S)", "Strouhal number (N_S)",
     "Relación adimensional entre la frecuencia de desprendimiento, el diámetro y la "
     "velocidad; vale cerca de 0,22 para cilindros.",
     "Dimensionless ratio of shedding frequency, diameter and velocity; about 0.22 for "
     "cylinders.", r"N_S = f_s B / V", ""),
    ("reynolds", "Número de Reynolds (Re)", "Reynolds number (Re)",
     "Relación entre fuerzas de inercia y viscosas; define el régimen del flujo.",
     "Ratio of inertial to viscous forces; defines the flow regime.", r"Re = V B \rho/\mu",
     ""),
    ("scruton", "Número de Scruton (N_Sc)", "Scruton number (N_Sc)",
     "Parámetro de masa y amortiguamiento; si es alto, el fluido no logra excitar la "
     "vibración.",
     "Mass-damping parameter; when high, the fluid cannot excite vibration.",
     r"N_{Sc} = \pi^2 \zeta (\rho_m/\rho)[1-(d/B)^2]", ""),
    ("natural_frequency", "Frecuencia natural (fn)", "Natural frequency (fn)",
     "Frecuencia a la que el termopozo vibra libremente; depende de la geometría, el "
     "material y el soporte.",
     "Frequency at which the thermowell vibrates freely.", "", ""),
    ("installed_frequency", "Frecuencia natural instalada (f_n^c)",
     "Installed natural frequency (f_n^c)",
     "Frecuencia natural corregida por la flexibilidad real del soporte.",
     "Natural frequency corrected for real support compliance.", r"f_n^c = H_c f_n", ""),
    ("inline_resonance", "Resonancia en línea", "In-line resonance",
     "Vibración en la dirección del flujo cuando el doble de fs coincide con la frecuencia "
     "natural.", "Vibration along the flow when twice fs matches the natural frequency.",
     r"2 f_s \approx f_n^c", ""),
    ("transverse_resonance", "Resonancia transversal", "Transverse resonance",
     "Vibración perpendicular al flujo cuando fs coincide con la frecuencia natural; debe "
     "evitarse siempre.", "Vibration across the flow when fs matches the natural frequency.",
     r"f_s \approx f_n^c", ""),
    ("lock_in", "Captura (lock-in)", "Lock-in",
     "Fenómeno por el cual el desprendimiento de vórtices se sincroniza con la vibración "
     "del termopozo en un rango de velocidades.",
     "Synchronization of vortex shedding with the thermowell vibration over a velocity "
     "range.", "", ""),
    ("magnification", "Factor de magnificación", "Magnification factor",
     "Amplificación dinámica de la respuesta respecto de la carga estática.",
     "Dynamic amplification relative to the static response.", r"F_M = 1/(1-r^2)", ""),
    ("damping", "Amortiguamiento (ζ)", "Damping (ζ)",
     "Disipación de energía de la vibración; en termopozos es muy baja (≈0,0005).",
     "Vibration energy dissipation; very low in thermowells (≈0.0005).", "", ""),
    ("stress_concentration", "Factor de concentración de esfuerzos (Kt)",
     "Stress concentration factor (Kt)",
     "Multiplicador del esfuerzo nominal en cambios de sección o roscas.",
     "Multiplier of nominal stress at section changes or threads.", "", ""),
    ("fatigue_limit", "Límite de fatiga (Sf)", "Fatigue limit (Sf)",
     "Amplitud de esfuerzo que el material soporta un número muy alto de ciclos sin romper.",
     "Stress amplitude the material withstands for a very high number of cycles.", "", ""),
    ("von_mises", "Esfuerzo de von Mises", "Von Mises stress",
     "Esfuerzo equivalente que combina los esfuerzos principales para compararlos con el "
     "admisible.", "Equivalent stress combining principal stresses.", "", ""),
    ("allowable_stress", "Esfuerzo admisible (S)", "Allowable stress (S)",
     "Esfuerzo máximo permitido por el código de diseño a una temperatura.",
     "Maximum stress allowed by the design code at a temperature.", "", ""),
    ("compliance", "Flexibilidad del soporte (Hc)", "Support compliance (Hc)",
     "Factor que reduce la frecuencia natural porque el soporte no es perfectamente rígido.",
     "Factor that lowers natural frequency because the support is not perfectly rigid.",
     "", ""),
    ("added_mass", "Masa añadida", "Added mass",
     "Masa de fluido que se mueve con el termopozo y baja su frecuencia natural.",
     "Fluid mass moving with the thermowell that lowers its natural frequency.",
     r"H_{a,f} = 1 - \rho/(2\rho_m)", ""),
    ("tapered", "Perfil cónico", "Tapered shank",
     "Vástago cuyo diámetro disminuye de la raíz a la punta: más rígido que uno recto.",
     "Shank whose diameter decreases from root to tip; stiffer than a straight one.", "",
     "geometry"),
    ("stepped", "Perfil escalonado", "Stepped shank",
     "Vástago con un tramo final de diámetro reducido para mejorar la respuesta térmica.",
     "Shank with a reduced-diameter end section for faster thermal response.", "",
     "geometry"),
    ("velocity_collar", "Collar de soporte", "Velocity collar",
     "Anillo que apoya el vástago en la tobera. La norma vigente lo deja fuera de su "
     "alcance y desaconseja su uso.",
     "Ring that supports the shank in the nozzle; outside the current standard's scope.",
     "", ""),
    ("immersion_error", "Error por conducción (inmersión)", "Conduction (immersion) error",
     "Diferencia entre la temperatura del fluido y la del sensor por el calor que fluye a "
     "lo largo del termopozo hacia el exterior.",
     "Difference between fluid and sensor temperature due to heat conducted along the "
     "thermowell.", r"\Delta T = (T_f - T_w)/\cosh(mL)", ""),
    ("time_constant", "Constante de tiempo (τ)", "Time constant (τ)",
     "Tiempo que tarda la medición en alcanzar el 63,2 % de un cambio en escalón.",
     "Time for the reading to reach 63.2 % of a step change.", r"\tau = \rho c V/(hA)", ""),
    ("corrosion_allowance", "Sobreespesor de corrosión (c)", "Corrosion allowance (c)",
     "Material adicional que se prevé perder por corrosión o erosión durante la vida útil.",
     "Extra material expected to be lost to corrosion or erosion.", "", ""),
    ("nace", "Servicio NACE (ácido)", "NACE (sour) service",
     "Servicio con H₂S húmedo que exige materiales calificados según NACE MR0175 / "
     "ISO 15156.", "Wet H₂S service requiring materials qualified per NACE MR0175.", "",
     ""),
    ("rating", "Rating presión-temperatura", "Pressure-temperature rating",
     "Presión máxima admisible de una brida en función de su clase, material y temperatura.",
     "Maximum allowable flange pressure for its class, material and temperature.", "", ""),
    ("pt100", "Pt100", "Pt100",
     "Termorresistencia de platino de 100 Ω a 0 °C según IEC 60751.",
     "Platinum resistance thermometer of 100 Ω at 0 °C per IEC 60751.",
     r"R(T) = R_0(1 + AT + BT^2)", ""),
    ("thermocouple", "Termopar", "Thermocouple",
     "Sensor formado por dos metales distintos que genera una tensión según la diferencia "
     "de temperatura (IEC 60584).",
     "Sensor of two dissimilar metals generating a voltage with temperature difference.",
     "", ""),
)

# (id, título, edición, resumen ES, resumen EN)
STANDARDS: Final[tuple[tuple[str, str, str, str, str], ...]] = (
    ("ASME-PTC-19.3-TW", "ASME PTC 19.3 TW", "2016",
     "Diseño mecánico de termopozos de barra maciza: frecuencia natural, desprendimiento "
     "de vórtices, esfuerzos estáticos y dinámicos, fatiga y presión externa.",
     "Mechanical design of bar-stock thermowells: natural frequency, vortex shedding, "
     "static and dynamic stresses, fatigue and external pressure."),
    ("ASME-B16.5", "ASME B16.5", "2020",
     "Bridas y accesorios bridados de NPS ½ a 24: dimensiones, materiales y ratings "
     "presión-temperatura por clase.",
     "Pipe flanges NPS ½ to 24: dimensions, materials and pressure-temperature ratings."),
    ("ASME-B40.9", "ASME B40.200 (B40.9)", "2018",
     "Termopozos para termómetros y sensores: selección, fabricación e instalación, con "
     "diseños estándar.",
     "Thermowells for thermometers and sensors: selection, fabrication and installation."),
    ("DIN-43772", "DIN 43772", "2016",
     "Formas y dimensiones normalizadas de termopozos (formas 1 a 4) usadas en Europa.",
     "Standardized thermowell forms and dimensions (forms 1 to 4) used in Europe."),
    ("ISA-TR20", "ISA-TR20.00.01", "2007",
     "Formatos de hojas de datos para la especificación de instrumentos, incluidos "
     "termopozos.", "Instrument specification datasheet formats, including thermowells."),
    ("NACE-MR0175", "NACE MR0175 / ISO 15156", "2020",
     "Materiales para servicio con H₂S en producción de petróleo y gas: límites de dureza, "
     "temperatura, cloruros y presión parcial.",
     "Materials for H₂S service in oil and gas production."),
    ("IEC-60751", "IEC 60751", "2022",
     "Termorresistencias de platino: relación resistencia-temperatura (Callendar-Van "
     "Dusen) y clases de tolerancia.",
     "Platinum RTDs: resistance-temperature relation and tolerance classes."),
    ("IEC-60584", "IEC 60584-1", "2013",
     "Termopares: tablas de fem de referencia y tolerancias para los tipos normalizados.",
     "Thermocouples: reference EMF tables and tolerances."),
)
