# ThermoWell Sizer 1.0: manual de usuario

ThermoWell Sizer dimensiona, verifica y ayuda a seleccionar termopozos (termovainas)
según **ASME PTC 19.3 TW-2016**, y emite la hoja de datos, la memoria de cálculo y los
listados del proyecto.

> **Aviso de responsabilidad.** Los resultados deben ser revisados por un ingeniero
> calificado y no sustituyen la consulta de la edición vigente de las normas. El programa
> resume y cita las normas, pero no reproduce su texto: ante cualquier duda, manda la norma.

## 1. Instalación

1. Ejecute `ThermoWellSizer-1.0.0-setup.exe`. Puede instalar solo para su usuario (no
   pide permisos de administrador) o para todos los usuarios del equipo.
2. Opcionalmente, cree el acceso directo en el escritorio y asocie los archivos `.tws`
   para abrir los proyectos con doble clic.
3. La primera vez que se abre el programa se muestra el aviso de responsabilidad, que
   hay que aceptar.

El instalador copia también tres proyectos de ejemplo en la carpeta `ejemplos` del
programa (accesible desde el menú Inicio).

Los datos del usuario (biblioteca con sus materiales y fluidos propios, licencia,
preferencias) se guardan en `%APPDATA%\InstruMatik\ThermoWellSizer`. Desinstalar el
programa no borra esa carpeta.

## 2. Licencia

Sin licencia, el programa funciona completo en **modo evaluación**: todos los cálculos y
reportes están disponibles, pero los PDF llevan la marca de agua «VERSIÓN DE
EVALUACIÓN» y los pies de página lo indican.

Para activar una licencia:

1. Abra **Ayuda › Licencia…**.
2. Si la licencia es para un equipo determinado, copie la **huella del equipo** con el
   botón *Copiar huella* y envíela a InstruMatik.
3. Pegue el código recibido (empieza con `TWS1.`) y pulse **Instalar licencia**.

La licencia se verifica sin conexión a Internet. Si el código fue alterado, venció o
corresponde a otro equipo, el programa lo informa y no lo instala. Con licencia, el pie
de cada reporte muestra «Licenciado a …».

## 3. La ventana principal

| Zona | Para qué sirve |
|---|---|
| Menús y barra de herramientas | Archivo, Editar, Proyecto, Cálculo, Biblioteca, Herramientas, Reportes y Ayuda. |
| Panel de tags (izquierda) | Lista de tags con su semáforo; clic derecho para nuevo, duplicar, renombrar, eliminar, copiar y pegar. |
| Editor del tag (centro) | Asistente de 5 pasos, o modo experto (Ctrl+E) con todo en una página. |
| Vista 2D (arriba a la derecha) | Esquema acotado del termopozo, se actualiza al escribir. |
| Resultados (abajo a la derecha) | Semáforo, criterios, resumen por caso, notas, traza, alternativas y gráficas. |

**Semáforo**: verde = cumple todos los criterios; amarillo = cumple con advertencias
(por ejemplo, datos a verificar o margen chico); rojo = no cumple o hay datos inválidos.

## 4. Flujo de trabajo

1. **Archivo › Nuevo proyecto** y luego **Proyecto › Datos del proyecto…**: nombre,
   cliente, planta, número de documento y revisiones. Estos datos van al rótulo de los
   reportes.
2. **Proyecto › Nuevo tag** (Ctrl+T). Complete los cinco pasos:
   1. *Identificación*: tag, servicio, línea o equipo, P&ID, ubicación.
   2. *Proceso*: fluido, presiones y temperaturas de operación y diseño, y uno o más
      casos de flujo (mínimo, normal, máximo) por velocidad, caudal másico o
      volumétrico. La densidad, la viscosidad y la fase se calculan solas (CoolProp o
      tablas de la biblioteca); desmarque la casilla para cargarlas a mano.
   3. *Tubería*: NPS y schedule (el diámetro interno sale de ASME B36.10M/B36.19M) u
      otro diámetro cargado a mano, y orientación.
   4. *Termopozo*: perfil (recto, cónico, escalonado), dimensiones L, A, B, d, t, b, U,
      material, conexión a proceso y recubrimiento.
   5. *Sensor*: tipo (RTD o termopar) y diámetro de vaina.
3. El cálculo corre solo medio segundo después de cada cambio; **F5** lo fuerza y
   **Shift+F5** calcula todos los tags.
4. Revise los resultados. Cada criterio muestra valor, límite, margen y la referencia a
   la subsección de la norma. La pestaña *Traza* lista cada paso del cálculo con su
   ecuación y sus valores.
5. Si el tag no cumple, **Cálculo › Proponer alternativas** (Ctrl+Shift+O) busca
   geometrías que cumplan cambiando longitud, diámetros o perfil (nunca propone
   collares de soporte). Seleccione una alternativa en la pestaña *Alternativas* y pulse
   *Aplicar al tag* (se puede deshacer con Ctrl+Z).
6. Emita los reportes desde el menú **Reportes**.

Los campos fuera del alcance de la norma se marcan en rojo con el motivo. F1 abre la
ayuda del paso visible.

## 5. Unidades, idioma y presentación

- **Herramientas › Unidades SI / imperiales** (Ctrl+U). Internamente todo se guarda en
  SI, de modo que cambiar de sistema no altera el proyecto.
- Presiones manométricas o absolutas y presión barométrica del sitio: **Proyecto ›
  Datos del proyecto…**.
- Idioma de la interfaz y de los reportes (**Herramientas › Español / Inglés**). En
  español se usa coma decimal.
- Tema claro u oscuro y modo experto, también en **Herramientas**.

## 6. Biblioteca

El menú **Biblioteca** abre materiales, fluidos, bridas y tuberías, glosario y fichas de
normas. **Ctrl+K** busca en toda la biblioteca, sin distinguir acentos y tolerando
errores de tipeo.

- **Asistente de material**: a partir de las condiciones del servicio (temperatura,
  cloruros, H₂S, agentes químicos, erosión) ordena los materiales en recomendados,
  aceptables y no recomendados, con el motivo de cada uno.
- Se pueden agregar materiales y fluidos propios; se conservan al actualizar el
  programa.

**Importante:** los esfuerzos admisibles, módulos elásticos y ratings de brida de la
biblioteca provienen de fuentes públicas y están marcados **«a verificar»**. Contrástelos
con ASME BPVC Sección II-D y ASME B16.5 vigentes antes de emitir un documento para
construcción. La memoria de cálculo lo indica junto a cada valor.

## 7. Herramientas

- **Conversor de unidades**: 11 magnitudes, incluida presión absoluta/manométrica.
- **Calculadoras**: velocidad en tubería, Reynolds y coeficiente de película, error por
  inmersión, constante de tiempo, RTD (IEC 60751), termopares (ITS-90), sobreespesor
  por corrosión y vida remanente.

Las estimaciones térmicas (error por inmersión, tiempo de respuesta) son modelos
simplificados de ingeniería y no forman parte de ASME PTC 19.3 TW; los resultados lo
aclaran.

## 8. Reportes

| Reporte | Formato | Contenido |
|---|---|---|
| Hoja de datos | PDF A4 | Formato tipo ISA-TR20 con rótulo, plano acotado y resultado. |
| Memoria de cálculo | PDF A4 / Word | Índice, datos, ecuaciones, traza paso a paso, gráficas, conclusiones. |
| Resultados | Excel | Una fila por tag con los resultados principales. |
| Resumen del proyecto | PDF A4 | Tabla de todos los tags con su estado. |
| Lista de materiales | Excel | Cantidades por material, perfil y conexión. |

Todos los reportes llevan el aviso de responsabilidad y la versión del programa.

## 9. Importar y exportar

- **Archivo › Importar › Guardar plantilla CSV…** genera una planilla con las columnas
  esperadas. Complétela en Excel y cárguela con **Tags desde CSV/Excel…**. Las filas con
  errores se informan por número de fila y no se importan.
- **Archivo › Exportar** guarda un tag o todo el proyecto en JSON, con sus resultados.
- Los proyectos se guardan como `.tws` (JSON legible). Cada 3 minutos se hace un
  autoguardado `.tws.autosave`; al abrir, si es más reciente, se ofrece recuperarlo.

## 10. Ejemplos resueltos

| Archivo | Caso | Resultado esperado |
|---|---|---|
| `ejemplo_1_agua.tws` | Agua de refrigeración, 10 barg / 80 °C, 2 m/s; cónico 316, bridado 1½" 300# RF en línea de 6". | Cumple. |
| `ejemplo_2_vapor.tws` | Vapor sobrecalentado 40 barg / 400 °C, 25 y 35 m/s; cónico corto F22, 600#, línea de 8" sch 80. | Cumple, con aviso de que el rating de la brida F22 (grupo 1.10) no está en la biblioteca y debe verificarse aparte. |
| `ejemplo_3_gas_no_cumple.tws` | Gas natural 50 barg / 30 °C a 30 m/s; vástago largo y delgado (L = 400 mm) en línea de 12". | No cumple por frecuencia (resonancia). Use *Proponer alternativas* para ver geometrías que cumplen. |

## 11. Atajos de teclado

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

## 12. Problemas frecuentes

- **«Rating de brida no disponible»**: el grupo B16.5 del material no está tabulado.
  Cargue el valor en **Cálculo › Opciones de cálculo…**.
- **«Sin datos del fluido»**: el fluido no está en CoolProp ni en las tablas. Cargue ρ y
  μ a mano o agregue el fluido en la biblioteca.
- **El reporte sale con marca de agua**: no hay licencia instalada (ver sección 2).
