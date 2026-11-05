# Biblioteca de datos (Fase 3)

La biblioteca vive en un archivo SQLite por usuario (en Windows, `%APPDATA%\ThermoWellSizer\biblioteca.sqlite`).
Se crea con `data/schema.sql` y se completa con los módulos `seed_materials.py`, `seed_tables.py` y
`seed_library.py`. Cuando una versión nueva del programa cambia `SEED_VERSION`, se reescriben solo las
filas de fábrica: los materiales y fluidos que agregó el usuario (`user_defined = 1`) se conservan.

## Contenido

| Bloque | Contenido | Estado de los datos |
|---|---|---|
| Materiales | A105, F11, F22, F91, 304/304L, 316/316L, 321, 347, 2205, 2507, Inconel 600 y 625, Hastelloy C276, Monel 400, titanio gr. 2, tantalio | **A verificar**: E(T) y S(T) aproximados de fuentes públicas |
| Recubrimientos | Estelita 6, carburo de tungsteno HVOF, PTFE | Orientativo |
| Bridas B16.5 | Grupos 1.1, 2.1 y 2.2, clases 150 a 2500 (600+ escaladas desde la 300) | **A verificar** contra la edición vigente |
| Tuberías B36.10M | NPS ½ a 24, schedules 40, 80, 160, STD, XS | Dimensiones nominales |
| Fluidos | 28 fluidos de CoolProp (incluye gas natural típico) y 3 tabulados (crudo API 30, gasoil, agua-glicol 50 %) | CoolProp: ecuaciones de referencia; tablas: aproximadas |
| Sensores | Pt100 y termopares K, J, T, E, N, S, R en diámetros típicos | Orientativo |
| Compatibilidad química | 11 agentes × 16 materiales, escala A/B/C | Orientativa |
| Glosario y normas | ~37 términos bilingües y 8 fichas de normas, redacción propia | No reproduce texto de normas |

Todas las magnitudes se guardan en SI (K, Pa, m, kg/m³, Pa·s). Las propiedades de materiales se interpolan
linealmente en temperatura; fuera del rango tabulado se toma el extremo y la verificación de temperatura
máxima del motor lo señala. La viscosidad de los fluidos tabulados se interpola en escala logarítmica.

Cada material informa en la memoria de cálculo la nota "Valores de biblioteca, a verificar". Antes de usar
el programa en un proyecto real, conviene contrastar E(T), S(T) y los ratings de bridas con ASME BPVC II-D,
B31.1/B31.3 y B16.5, y marcar la fuente como verificada.

## Materiales fuera de la tabla de fatiga

Titanio y tantalio no figuran en la tabla de límites de fatiga de PTC 19.3 TW. El motor emite un aviso
(`fatigue_data`) y usa el límite de la clase A salvo que el usuario cargue un valor justificado.

## Selección de material

`data/selection.py` puntúa cada material frente a: temperatura de diseño y mínima, servicio ácido
(NACE MR0175/ISO 15156, a partir de 0,05 psia de H₂S o si se marca el servicio), cloruros (corrosión bajo
tensión en austeníticos sobre 60 °C y 50 ppm), agentes químicos y erosión (propone recubrimientos aptos para
la temperatura). Devuelve "recomendado", "aceptable" o "no recomendado" con sus motivos. Es una ayuda: la
decisión final la toma el especialista en materiales.

## Propiedades de fluidos

`properties/fluids.py` calcula ρ, μ, Z, fase y temperatura de saturación con CoolProp. Si el fluido no tiene
modelo, usa la tabla de la biblioteca. La fuente queda anotada en `FluidProperties.source_note` y aparece en
la memoria.
