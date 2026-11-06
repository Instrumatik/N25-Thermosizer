# Cambios

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
