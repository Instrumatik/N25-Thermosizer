# Reportes (Fase 6)

Todos los reportes salen del menú **Reportes**, en el idioma y el sistema de unidades activos en la interfaz.
Cada uno lleva el aviso de responsabilidad en todas las páginas.

| Reporte | Formato | Contenido |
|---|---|---|
| Hoja de datos | PDF A4 | Rótulo tipo ISA-TR20 con logo, documento, revisión, fecha y hoja; 35 líneas numeradas (general, proceso, tubería, termopozo, sensor); plano esquemático acotado; resultados del cálculo (fs, fn,c, relación y límite, Scruton, esfuerzos, presión, velocidad máxima admisible, τ); recuadro de resultado; notas; tabla de revisiones y firmas |
| Memoria de cálculo | PDF A4 | Portada con plano y resultado, índice, objeto y alcance, datos de entrada, propiedades del material, opciones, resumen de verificaciones con márgenes y estado, resumen por caso, desarrollo completo del cálculo por caso (símbolo, descripción, ecuación renderizada, datos sustituidos, resultado y referencia a la norma), gráficas de sensibilidad, criterios adicionales y notas |
| Memoria en Word | DOCX | Igual contenido que la memoria PDF, editable |
| Resultados | Excel | Hoja de resumen con semáforo, lista de materiales y una hoja por tag con datos, criterios (valores SI) y traza completa |
| Resumen del proyecto | PDF A4 | Tabla de todos los tags con material, conexión, dimensiones, relación de frecuencias, margen del esfuerzo dinámico y estado; lista de materiales |
| Lista de materiales | Excel | Termopozos agrupados por especificación idéntica con cantidades y tags |

## Detalles

- Las ecuaciones de la traza se dibujan con mathtext de matplotlib a partir de la expresión LaTeX de cada paso;
  si alguna no puede dibujarse, se muestra en texto plano.
- Se usa la fuente DejaVu Sans (incluida con matplotlib) para que se vean bien ρ, μ, ζ, τ y subíndices.
- La memoria cita números de ecuación y párrafo de ASME PTC 19.3 TW-2016; no reproduce texto de la norma.
- La revisión y la fecha del rótulo salen de la última revisión cargada en los datos del proyecto.
