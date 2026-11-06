# Cambios

## 1.3.0 (2026-11-06)

Revisión del usuario sobre la versión 1.2.0.

- **Selección automática por bloque**: selector Manual / Automático para material y
  protecciones, conexión, geometría y vaina del sensor (las propiedades del fluido y la
  tubería ya se calculaban). Con los datos de proceso, fluido, casos de flujo, servicio
  corrosivo, NPS, schedule, Hs y DI de la conexión de montaje, el programa recomienda
  material (con alternativas), recubrimiento, sobreespesor, tipo, tamaño, clase y cara de
  la conexión, perfil y cotas (iterando con la verificación ASME hasta que cumple) y la
  vaina del sensor. La elección por bloque se guarda en el proyecto.
- **Justificación** de cada valor automático en la pestaña Resumen ASME, en la página 2
  de la hoja de datos y en la nueva sección «4. Selección automática y justificación» de
  la memoria PDF y Word (las secciones siguientes pasan a 5–12). En la tabla de datos de
  entrada el origen puede ser cargado, calculado o automático.
- Fichas ⓘ de los selectores nuevos y de la sección de justificación.
- Diseño típico bridado escalonado corregido a punta de 7/8" (la correlación de la norma
  solo admite 1/2" y 7/8").
- Resultados calculados en tablas de hasta tres casos; la hoja de datos muestra los casos
  base y remite a la memoria para las variantes con sobreespesor consumido.
- **Logo THWS** (termopozo negro como «T» y «HWS» en azul) en reportes, ventana, barra
  de tareas, Acerca de, Licencia, instalador y archivos .tws; el .ico usa solo el
  termopozo de 16 a 48 px. `tools/make_icons.py` regenera todo desde el logo maestro.

## 1.2.0 (2026-11-06)

Revisión del usuario sobre la versión 1.1.0.

- **Resumen ASME** (pestaña nueva, página 2 de la hoja de datos y comienzo de la
  memoria PDF y Word): estado por tema (erosión: no erosivo / vigilar / erosivo;
  frecuencia de estela: cumple / riesgo de resonancia; esfuerzos; presión y rating;
  global: cumple / requiere revisión de ingeniería / no cumple) y **resultados
  calculados** por caso con su límite: caudal volumétrico real, V, V_e (API RP 14E),
  V/V_e, Re, Strouhal, f_s, f_n,c, relación de frecuencias, esfuerzo estacionario,
  dinámico y de von Mises.
- **Datos de entrada** al inicio de la memoria: los 15 datos de la planilla con su
  valor, si son cargados o calculados y si entran en el cálculo ASME.
- **Convención de largos**: equivalencia entre la planilla (L = Hs + inserción) y el
  programa (U = L desde la cara de la brida), en pantalla y en la memoria.
- **Fichas ⓘ** en cada dato, opción y resultado (105 fichas en español e inglés) con
  explicación, umbrales, fórmulas, diagramas, esquemas de instalación, curvas con los
  datos del tag y ejemplo resuelto; búsqueda con Ctrl+K y prueba automática de que
  ningún campo quede sin ficha.
- **Brida de montaje** en lugar de «tobera»: Hs se mide desde la superficie externa
  de la tubería y el programa suma el espesor de pared; desglose Hs + pared +
  inmersión = U en pantalla y en la hoja de datos. Esquema de montaje en la ayuda.
- **Tuberías**: todos los NPS de 1/8" a 48" y todos los schedules de ASME B36.10M y
  B36.19M, ordenados por espesor; opción «Otro» con OD y espesor a mano. Los archivos
  viejos completan el espesor desde la tabla.
- **Fluido** en dos listas encadenadas (tipo y fluido), con «(Estado Líquido)» y
  «(Estado Vapor)», y aviso si la fase calculada no coincide.
- **Tamaño de conexión** en lista según el tipo, con el sugerido para el NPS de la
  línea (tabla editable en `tamanos_conexion.json`); clase y cara solo para bridadas
  y Van Stone.
- **E y S manuales** por tag, anotados en la memoria.
- **Plano** sin valores numéricos ni signos igual en las cotas; etiquetas «Cabezal»,
  «Brida del termopozo» y «Rosca NPT». Números 100 a 108 centrados en la tabla ASME.
- **Logo nuevo** TWS · Thermosizer by INSTRUMATIK S.A.S en los reportes, la ventana,
  la barra de tareas, Acerca de, Licencia, el instalador y los archivos .tws (ícono
  .ico de 16 a 256 px, con la «T» sola en los tamaños chicos).
- Ejemplos regenerados con espesor de pared, fase correcta y Hs en el ejemplo 3.

## 1.1.0 (2026-11-06)

Mejoras a partir de la planilla de cálculo, una especificación de operadora y un
catálogo de fabricante aportados por el usuario.

- **Plano acotado estilo catálogo** en la vista 2D, la hoja de datos y la memoria: U,
  L, largo total, largo del agujero, t, T (lag), largo de rosca I o espesor de brida E,
  Ls, L0, Ø A, Ø B, Ø d, cabezal 1/2" NPT y conexión, con tablas de rosca, hexágono,
  brida (B16.5) y socket.
- **Diseños típicos**: catálogo genérico de nueve ejecuciones con agujeros de 0,260" y
  0,385" y largos U normalizados; recomienda el largo U según la línea y completa la
  geometría.
- **Perfiles de especificación de cliente** (JSON): modelos normalizados y tabla de
  selección por NPS, rating y montaje; plantilla en `examples/perfil_ejemplo.json`.
- **Caudal estándar de gas** (Sm³/h, Nm³/h, SCFM, MSCFD, MMSCFD) como base de los
  casos de flujo, con densidad estándar automática; nueva magnitud en el conversor.
- **Recomendaciones automáticas**: erosión (API RP 14E), inmersión, punta contra la
  pared, tobera, sensor, rango del sensor, bimetálicos, recubrimientos, conexión
  roscada y prueba hidráulica; pestaña nueva en resultados y sección en los reportes.
- **Ensayos y documentación** sugeridos en la hoja de datos, la memoria PDF y Word.
- **Biblioteca › Referencias**: tipos de termopozo, diseños típicos, instalación, guía
  de materiales, colores y tolerancias de termopares, clases y cableado de Pt100,
  escalas de bimetálicos. Glosario ampliado y recubrimientos nuevos (Stellite 1,
  carburo de cromo, PFA, PVDF, tantalio, cerámico).
- Diámetro interno de tobera opcional en el paso Tubería.
- El ejemplo 3 incluye la tobera, de modo que falla solo por frecuencia.

## 1.0.0 (2026-11-05)

Primera versión completa.

- **Motor** ASME PTC 19.3 TW-2016: frecuencias natural y de Strouhal, criterios de
  frecuencia (subcrítico y supercrítico, lock-in en línea), esfuerzos estacionarios y
  dinámicos, presión externa, rating de brida, alcance de la norma; traza de cálculo
  completa y validación contra los ejemplos de la norma.
- **Biblioteca** de 16 materiales con recubrimientos, compatibilidad química, fluidos
  (CoolProp y tablas propias), bridas ASME B16.5, tuberías B36.10M/B36.19M, sensores,
  glosario y fichas de normas; asistente de selección de material.
- **Interfaz** PySide6: asistente de 5 pasos o modo experto, vista 2D, semáforo,
  alternativas que cumplen, gráficas de sensibilidad, deshacer/rehacer, autoguardado,
  importación CSV/Excel, español e inglés, SI e imperial, tema oscuro.
- **Herramientas**: conversor de 11 magnitudes y 8 calculadoras (velocidad, película,
  inmersión, constante de tiempo, RTD, termopares, corrosión, vida remanente).
- **Reportes**: hoja de datos tipo ISA-TR20, memoria de cálculo (PDF y Word),
  resultados y lista de materiales en Excel, resumen del proyecto.
- **Licencias** firmadas con Ed25519, verificación sin conexión, modo evaluación con
  marca de agua.
- **Distribución**: ejecutable PyInstaller, instalador Inno Setup con asociación de
  archivos `.tws`, flujo de GitHub Actions para generarlo; manual de usuario y tres
  ejemplos resueltos.
