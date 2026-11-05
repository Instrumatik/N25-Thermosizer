# Cambios

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
