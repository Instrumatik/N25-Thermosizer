# Interfaz de escritorio (Fase 4)

La interfaz está hecha con PySide6 (Qt 6). Arranca con `thermowell-sizer` o
`python -m thermowell_sizer.ui.app [proyecto.tws]`.

## Organización de la ventana

- **Barra de menús**: Archivo, Editar, Proyecto, Cálculo, Biblioteca, Herramientas, Reportes y Ayuda.
- **Barra de herramientas** con las acciones frecuentes (nuevo, abrir, guardar, deshacer, nuevo tag, calcular,
  alternativas, reportes, buscador y conversor).
- **Panel lateral de tags** con el semáforo de cada uno y menú contextual (nuevo, duplicar, renombrar,
  eliminar, copiar, pegar).
- **Editor del tag**: asistente de cinco pasos (Identificación, Proceso, Tubería, Termopozo, Sensor) o modo
  experto con todas las secciones en una sola página (Ctrl+E). La validación es en tiempo real: los campos
  fuera del alcance de la norma se marcan en rojo con el motivo y la referencia.
- **Vista previa 2D** del termopozo con cotas, que se actualiza al escribir.
- **Panel de resultados**: semáforo global, criterios ordenados por gravedad con valor, límite y margen,
  resumen por caso (V, Re, Strouhal, fs, fn, Hc, fnc, Scruton, relación de frecuencias, V_IR), notas, traza
  de cálculo completa, alternativas que cumplen (nunca collares) y gráficas de sensibilidad (frecuencias y
  esfuerzo dinámico en función de la velocidad, frecuencias en función de L) con la velocidad máxima
  admisible.
- **Barra de estado**: estado del tag, sistema de unidades y archivo.

## Comportamiento

- Las propiedades del fluido (ρ, μ y fase) se recalculan con CoolProp o con las tablas de la biblioteca al
  cambiar presión o temperatura; se pueden cargar a mano desactivando la casilla.
- El diámetro interno sale de NPS y schedule (ASME B36.10M) o se carga a mano.
- El rating de brida se toma de la biblioteca según el grupo B16.5 del material, la clase y la temperatura de
  diseño; si no hay dato, se avisa y puede cargarse en Opciones de cálculo.
- El cálculo se dispara solo medio segundo después de la última edición; F5 lo fuerza.
- Deshacer y rehacer (Ctrl+Z, Ctrl+Y) guardan instantáneas del proyecto completo; las ediciones seguidas de
  un mismo tag se agrupan en un solo paso.
- Autoguardado cada 3 minutos en `proyecto.tws.autosave`; al abrir, si hay uno más reciente, se ofrece
  recuperarlo.
- Idioma (español/inglés), unidades (SI/imperial, Ctrl+U), presiones manométricas o absolutas y tema
  claro/oscuro se recuerdan entre sesiones. En pantalla se usa coma decimal en español.
- F1 abre la ayuda del paso visible. Ctrl+K abre el buscador global de la biblioteca.
- Importación de tags desde CSV o Excel con plantilla descargable, y exportación a JSON del tag o del
  proyecto con sus resultados.

## Atajos de teclado

| Atajo | Acción |
|---|---|
| Ctrl+N / Ctrl+O / Ctrl+S | Nuevo, abrir, guardar |
| Ctrl+Z / Ctrl+Y | Deshacer, rehacer |
| Ctrl+T / Ctrl+D / F2 / Supr | Nuevo tag, duplicar, renombrar, eliminar |
| F5 / Shift+F5 | Calcular tag, calcular todos |
| Ctrl+Shift+O | Proponer alternativas |
| Ctrl+K | Buscar en la biblioteca |
| Ctrl+E | Modo experto |
| Ctrl+U | Cambiar unidades |
| Ctrl+Re Pág / Ctrl+Av Pág | Paso anterior / siguiente |
| F1 | Ayuda contextual |

## Arquitectura

La lógica que no depende de Qt vive en `services.py` (evaluar un tag, propiedades, rating de brida,
importación) y se prueba sin ventanas. `ui/` solo arma pantallas: `tag_editor.py`, `results.py`,
`preview.py`, `charts.py`, `library_ui.py`, `dialogs.py`, `help.py` y `main_window.py`. Los textos de la
interfaz están en `ui/text.py` como pares español/inglés.
