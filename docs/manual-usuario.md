# ThermoWell Sizer 1.3: manual de usuario

ThermoWell Sizer dimensiona, verifica y ayuda a seleccionar termopozos (termovainas)
según **ASME PTC 19.3 TW-2016**, y emite la hoja de datos, la memoria de cálculo y los
listados del proyecto.

> **Aviso de responsabilidad.** Los resultados deben ser revisados por un ingeniero
> calificado y no sustituyen la consulta de la edición vigente de las normas. El programa
> resume y cita las normas, pero no reproduce su texto: ante cualquier duda, manda la norma.

## 1. Instalación

1. Ejecute `ThermoWellSizer-1.3.0-setup.exe`. Puede instalar solo para su usuario (no
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
   2. *Proceso*: primero el **tipo de fluido** (líquidos, gases, vapores, vapor de agua
      (steam) o bifásico) y después el **fluido**, que muestra solo los de ese tipo; los
      gases licuables aparecen en líquidos como «(Estado Líquido)». Con propiedades
      automáticas el programa avisa si con P y T el fluido no está en el estado elegido.
      Luego presiones y temperaturas de operación y diseño, y uno o más
      casos de flujo (mínimo, normal, máximo) por velocidad, caudal másico,
      volumétrico o **caudal estándar de gas** (Sm³/h a 15 °C y 101,325 kPa). La
      densidad, la viscosidad, la fase y la densidad en condiciones estándar se calculan
      solas (CoolProp o tablas de la biblioteca); desmarque la casilla para cargarlas a
      mano.
   3. *Tubería*: NPS (1/8" a 48") y schedule (todos los de ASME B36.10M y B36.19M,
      ordenados por espesor); con **Otro** se cargan OD y espesor a mano. Orientación,
      **Hs, altura de la brida de montaje** medida desde la superficie externa de la
      tubería hasta la cara de la brida (el programa suma el espesor de pared y muestra
      el desglose Hs + pared + inmersión = U) y, opcionalmente, el diámetro interno de la
      conexión de montaje (para verificar que el vástago pase).
   4. *Termopozo*: perfil (recto, cónico, escalonado), dimensiones L, A, B, d, t, b, U,
      material, conexión a proceso (el **tamaño** se elige de una lista según el tipo,
      con el sugerido para el NPS de la línea; clase y cara solo para bridadas y Van
      Stone), recubrimiento y, si hace falta, **E y S cargados a mano** para ese tag. El botón **Diseño típico /
      especificación…** completa las cotas solo (ver sección 4.1).
   5. *Sensor*: tipo (RTD o termopar) y diámetro de vaina.
3. El cálculo corre solo medio segundo después de cada cambio; **F5** lo fuerza y
   **Shift+F5** calcula todos los tags.
4. Revise los resultados. La pestaña **Resumen ASME** muestra el estado por tema
   (erosión, frecuencia de estela, esfuerzos, presión y rating, y global), los
   **resultados calculados** de cada caso con su límite (caudal real, V, V_e, V/V_e,
   Re, Strouhal, f_s, f_n,c, relación de frecuencias, esfuerzos estacionario, dinámico
   y de von Mises) y la equivalencia entre la convención de la planilla (Hs + inserción)
   y la del programa (U = L desde la cara de la brida). Cada criterio muestra valor, límite, margen y la referencia a
   la subsección de la norma. La pestaña *Traza* lista cada paso del cálculo con su
   ecuación y sus valores.
5. Si el tag no cumple, **Cálculo › Proponer alternativas** (Ctrl+Shift+O) busca
   geometrías que cumplan cambiando longitud, diámetros o perfil (nunca propone
   collares de soporte). Seleccione una alternativa en la pestaña *Alternativas* y pulse
   *Aplicar al tag* (se puede deshacer con Ctrl+Z).
6. Emita los reportes desde el menú **Reportes**.

Los campos fuera del alcance de la norma se marcan en rojo con el motivo. F1 abre la
ayuda del paso visible.

**Fichas de ayuda.** Cada dato, opción y resultado tiene una ficha que se abre desde
**Buscar en la biblioteca** (Ctrl+K: escriba el nombre del dato) o, en los resultados, con
doble clic en un criterio o clic en el encabezado de la tabla por caso. La
ficha explica qué es, qué hace en el programa, qué resultados afecta, sus umbrales,
contra qué se compara, cómo interpretarlo, qué hacer, la referencia resumida a la norma
y las unidades, con fórmulas, diagrama del termopozo con la cota resaltada, esquemas de
instalación, curvas trazadas con los datos del tag y un ejemplo resuelto con el tag
actual y con un caso de referencia.

### 4.1 Diseños típicos y especificaciones de cliente

En el paso *Termopozo*, **Diseño típico / especificación…** abre un diálogo con dos
orígenes:

- **Catálogo genérico**: ejecuciones habituales de la industria (roscadas recta, cónica
  y escalonada; bridadas recta, cónica y escalonada; socket weld; para soldar; Van
  Stone), agujero de 0,260" (6,6 mm) o 0,385" (9,8 mm), punta de 1/4" y largos U
  normalizados de 2½" a 22½". El programa **recomienda el largo U** según el diámetro
  interno y la altura Hs: el más corto que deja la punta al menos a 1/3 del diámetro (y unos
  100 mm dentro del flujo si la línea lo permite) sin acercarse a la pared opuesta.
- **Perfiles de cliente**: archivos JSON con los modelos normalizados de una
  especificación de empresa. El programa elige el modelo según el tipo de conexión, el
  NPS de la línea, el rating y el montaje (en codo o a 90°), y avisa si la línea es
  chica o si el montaje no está permitido. Con **Importar perfil…** se copia el archivo
  a la carpeta de datos del usuario; el formato está en `docs/perfiles-cliente.md` y
  hay una plantilla en `ejemplos\perfil_ejemplo.json`.

Al aplicar se cargan perfil, conexión, U = L, A, B, d, t, Ls y el tramo protegido L0
(brida de montaje). Son valores típicos: confirme las cotas con el plano del fabricante.

### 4.2 Recomendaciones automáticas

La pestaña **Recomendaciones** de los resultados complementa la verificación ASME con
avisos de buena práctica, ordenados por gravedad:

- velocidad erosiva (API RP 14E) y fluidos con sólidos;
- inmersión insuficiente (largo sensible más 4 a 6 diámetros de punta), punta que toca o
  queda cerca de la pared opuesta, brida de montaje sin L0 cargado, vástago que no pasa por la
  conexión de montaje;
- huelgo entre sensor y agujero, sensor sin resorte, rango de temperatura del sensor,
  vaina cerámica a muy alta temperatura, escala sugerida del termómetro bimetálico;
- recubrimiento por encima de su temperatura, conexión roscada en servicio peligroso o
  de alta presión, y presión de prueba hidráulica de referencia.

Las mismas recomendaciones y una lista de **ensayos y documentación** (prueba
hidrostática, END de soldaduras, PMI, certificados 3.1, NACE, control dimensional,
marcado) salen en la hoja de datos y en la memoria de cálculo.

### 4.3 Selección automática por bloque (manual / automático)

Cada bloque de datos empieza con su selector **Modo: Manual / Automático** (en negrita):
*Proceso* (propiedades del fluido), *Tubería*, y en el paso *Termopozo* los bloques
*Conexión a proceso*, *Material y protecciones* y *Geometría del termopozo*; el paso
*Sensor* tiene el suyo para la vaina:

| Bloque | En automático el programa elige | Criterio resumido |
|---|---|---|
| Propiedades del fluido | ρ, μ y fase | CoolProp o biblioteca a P y T de operación (casilla «Calcular ρ y μ»). |
| Tubería | DI y espesor de pared | Tabla ASME B36.10M / B36.19M según NPS y schedule. |
| Material y protecciones | material, alternativas, recubrimiento y sobreespesor de corrosión | Matriz de selección de la biblioteca a la temperatura de diseño con H₂S, cloruros, pH y sólidos; se prefiere 316/316L entre los aptos. Recargue duro si hay sólidos o V/V_e ≥ 0,7; 1 mm de sobreespesor en servicio agresivo. |
| Conexión | tipo, tamaño, clase y cara | Roscada solo en utilidades (agua, aire, nitrógeno) ≤ 20 barg y ≤ 200 °C; soldada desde clase 1500; bridada en el resto. Clase B16.5 mínima para la presión de diseño y el grupo del material; RF hasta 600, RTJ desde 900. |
| Geometría | perfil, U, A, B, d, L0 | Se prueban diseños típicos (cónico, escalonado, recto) y largos normalizados con la verificación ASME hasta que cumple, cuidando la inmersión de la parte sensible y que el vástago entre en la conexión de montaje. Si nada cumple, se muestra el de mejor margen con un aviso. |
| Sensor | diámetro de vaina | 6 mm para agujero 0,260" y 8 mm para 0,385", con resorte. |

Siempre los carga usted: condiciones de proceso (P y T de operación y de diseño), tipo de
fluido y fluido, casos de flujo, H₂S, cloruros, pH y sólidos si aplican, NPS, schedule, Hs y
el diámetro interno de la conexión de montaje.

Los campos de un bloque automático quedan en gris y se completan al calcular. Cada valor
elegido aparece con su justificación en la pestaña **Resumen ASME**, en la página 2 de la
hoja de datos y en la sección **4. Selección automática y justificación** de la memoria; en
la tabla de datos de entrada su origen figura como «Automático». La elección se guarda en el
proyecto. Para fijar un valor a mano, vuelva el bloque a «Manual»: el editor conserva lo
último calculado. Las recomendaciones son orientativas y deben ser revisadas por un
ingeniero calificado.

## 5. Unidades, idioma y presentación

- **Herramientas › Unidades SI / imperiales** (Ctrl+U). Internamente todo se guarda en
  SI, de modo que cambiar de sistema no altera el proyecto.
- Presiones manométricas o absolutas y presión barométrica del sitio: **Proyecto ›
  Datos del proyecto…**.
- Idioma de la interfaz y de los reportes (**Herramientas › Español / Inglés**). En
  español se usa coma decimal.
- Tema claro u oscuro y modo experto, también en **Herramientas**.

## 6. Biblioteca

El menú **Biblioteca** abre materiales, fluidos, bridas y tuberías, glosario, fichas de
normas y **Referencias**: tipos de termopozo y cuándo usar cada uno, diseños típicos,
buenas prácticas de instalación, guía de materiales por servicio, códigos de color de
termopares (ANSI e IEC), tolerancias de termopares, clases y cableado de Pt100 y escalas
de termómetros bimetálicos. **Ctrl+K** busca en toda la biblioteca, sin distinguir acentos y tolerando
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

- **Conversor de unidades**: 12 magnitudes, incluida presión absoluta/manométrica y
  caudal de gas en condiciones estándar (Sm³/h, Nm³/h, SCFM, MSCFD, MMSCFD).
- **Calculadoras**: velocidad en tubería, Reynolds y coeficiente de película, error por
  inmersión, constante de tiempo, RTD (IEC 60751), termopares (ITS-90), sobreespesor
  por corrosión y vida remanente.

Las estimaciones térmicas (error por inmersión, tiempo de respuesta) son modelos
simplificados de ingeniería y no forman parte de ASME PTC 19.3 TW; los resultados lo
aclaran.

## 8. Reportes

| Reporte | Formato | Contenido |
|---|---|---|
| Hoja de datos | PDF A4 | Formato tipo ISA-TR20 con rótulo, plano acotado (U, L, A, B, d, t, rosca o brida, largo total), resultado, recomendaciones y ensayos. |
| Memoria de cálculo | PDF A4 / Word | Índice, resumen de la verificación, datos, selección automática y justificación, ecuaciones, traza paso a paso, gráficas, conclusiones. |
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
| `ejemplo_3_gas_no_cumple.tws` | Gas natural 50 barg / 30 °C a 30 m/s; vástago largo y delgado (L = 400 mm, brida de montaje Hs = 140 mm) en línea de 12". | No cumple por frecuencia (resonancia). Use *Proponer alternativas* para ver geometrías que cumplen. |

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
