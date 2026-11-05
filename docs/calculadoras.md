# Calculadoras y conversor (Fase 5)

Se abren desde **Herramientas** como ventanas flotantes no modales, de modo que pueden quedar abiertas mientras
se edita un tag. La lógica vive en `core/tools/` (sin Qt) y está probada.

## Conversor de unidades (Ctrl+Shift+U)

Un valor se muestra a la vez en todas las unidades de la categoría: temperatura, presión (absoluta y
manométrica, con presión barométrica editable), longitud, caudal másico y volumétrico, densidad, viscosidad
dinámica y cinemática, velocidad, esfuerzo y frecuencia. Los factores son exactos por definición cuando
existen (pulgada, libra, psi, galón US, atmósfera, gravedad normal).

## Calculadoras

| Pestaña | Qué calcula | Modelo |
|---|---|---|
| Velocidad y Re | Velocidad en tubería desde caudal másico o volumétrico; Re de tubería y del termopozo | V = ṁ/(ρA), Re = ρVD/μ |
| Densidad de gas | ρ, μ, Z, fase y temperatura de saturación de cualquier fluido de la biblioteca | CoolProp (ecuaciones de referencia) |
| Bridas P-T | Presión admisible por grupo de material, clase y temperatura | Tablas de la biblioteca, interpoladas (a verificar) |
| Error de inmersión | Error por conducción en la punta e inmersión mínima para un error admisible | Aleta anular con punta adiabática: ΔT = θ/cosh(mL) |
| Constante de tiempo | τ y t90 del conjunto termopozo + sensor | Resistencias de película y de huelgo por unidad de longitud |
| Corrosión | Sobreespesor para la vida de diseño y vida remanente | c = tasa × años |
| Pt100 | R(T), T(R) y tolerancias de clase AA, A, B y C para Pt100, Pt500 y Pt1000 | Callendar-Van Dusen, IEC 60751 |
| Termopares | FEM(T) y T(FEM) con compensación de unión fría y tabla completa, tipos B, E, J, K, N, R, S y T | Funciones de referencia NIST ITS-90 |

Los coeficientes NIST ITS-90 son de dominio público (NIST SRD 60) y se tomaron de la compilación
`thermocouples_reference` 0.20, también de dominio público. Las pruebas comparan contra valores de tabla NIST
con tolerancia de 1,5 µV.

## Criterios adicionales en los resultados

Cada cálculo de tag agrega ahora, como estimación fuera de PTC 19.3 TW:

- coeficiente de película h con la correlación de Churchill-Bernstein (propiedades k y cp de CoolProp, o
  valores típicos de la fase si el fluido no tiene modelo);
- error por conducción con la base del termopozo a 20 °C y la inmersión expuesta mínima para un error menor
  que 0,1 K;
- constante de tiempo y t90 con huelgo de aire entre sensor y agujero.

Aparecen en el resumen del panel de resultados y se detallan en la pestaña de notas.
