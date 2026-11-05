# Validación del motor de cálculo

Comparación entre el motor y los resultados intermedios publicados en los ejemplos
resueltos de ASME PTC 19.3 TW-2016 (sección 8). Criterio de aceptación: desviación
menor al 1 % en **cada** valor. Este archivo se generó ejecutando el motor; las mismas
comparaciones están en `tests/test_reference_examples.py` y corren en cada cambio.

Además, `tests/test_cross_cases.py` compara tres casos adicionales (gas a baja presión
con perfil recto bridado, aceite viscoso con Re < 1300 en termopozo roscado y agua con
tramo protegido L0) contra un recálculo independiente escrito aparte, que obtiene el
parámetro G por integración numérica. Todos quedan por debajo del 1 %.

Erratas detectadas en los ejemplos de la norma (el motor sigue la ecuación, no la errata):

- 8-1.2, paso 3: imprime H_a,f = 0,9922; el valor correcto, usado en el paso 5, es 0,9995.
- 8-1.8 y 8-2.1.1: imprimen 0,833 y 0,248 donde las ecuaciones (6-13-1) y (6-4-2) dicen
  0,0833 y 0,0248; los resultados publicados corresponden a estas últimas.
- 8-2.1.3 indica E = 1,93·10¹¹ Pa, pero los cálculos usan 1,91·10¹¹ Pa.
- 8-2.5.2, paso 2: imprime 124 200 Pa; el resultado corresponde a 12 420 Pa.


## Ejemplo 8-1: termopozo cónico soldado, vapor (unidades US)

| Símbolo | Norma (SI) | Motor (SI) | Desviación |
|---|---:|---:|---:|
| `Re` | 1.068e+06 | 1.0676e+06 | 0.040 % |
| `N_S` | 0.22 | 0.22 | 0.000 % |
| `f_a` | 2095 | 2094.9 | 0.004 % |
| `H_f` | 1.352 | 1.3519 | 0.010 % |
| `H_af` | 0.9995 | 0.99949 | 0.001 % |
| `H_as` | 0.9922 | 0.99221 | 0.001 % |
| `f_n` | 2809 | 2808.6 | 0.016 % |
| `H_c` | 0.7746 | 0.77463 | 0.004 % |
| `f_nc` | 2176 | 2175.6 | 0.018 % |
| `N_Sc` | 4.525 | 4.5252 | 0.003 % |
| `f_s` | 778.8 | 778.8 | 0.000 % |
| `V_IR` | 125.58 | 125.59 | 0.011 % |
| `G_SP` | 29.05 | 29.046 | 0.014 % |
| `S_o_IR_support` | 4.0286e+08 | 4.0283e+08 | 0.008 % |
| `F_T` | 0.9386 | 0.93857 | 0.004 % |
| `S_f_adm` | 1.9416e+07 | 1.9428e+07 | 0.065 % |
| `S_t_support` | 1.7209e+06 | 1.7206e+06 | 0.017 % |
| `S_a_support` | 1.6706e+06 | 1.6705e+06 | 0.009 % |
| `P_D` | 45237 | 45237 | 0.001 % |
| `S_D_support` | 1.3141e+06 | 1.314e+06 | 0.014 % |
| `S_max_support` | 2.9847e+06 | 2.9844e+06 | 0.011 % |
| `S_vm_support` | 1.3169e+06 | 1.3168e+06 | 0.005 % |
| `r` | 0.358 | 0.35797 | 0.008 % |
| `F_M` | 1.147 | 1.147 | 0.002 % |
| `r_prime` | 0.7159 | 0.71594 | 0.006 % |
| `F_M_prime` | 2.052 | 2.0516 | 0.020 % |
| `P_d` | 3230.9 | 3231.2 | 0.010 % |
| `S_d_support` | 1.9257e+05 | 1.9255e+05 | 0.011 % |
| `S_L_support` | 1.0763e+06 | 1.0765e+06 | 0.020 % |
| `S_o_support` | 2.4056e+06 | 2.4059e+06 | 0.011 % |
| `P_c` | 6.4735e+07 | 6.4736e+07 | 0.002 % |
| `P_t` | 5.4903e+08 | 5.4905e+08 | 0.003 % |

Desviación máxima: **0.065 %**. Estado global del motor: `pass`.

## Ejemplo 8-2: termopozo escalonado roscado, agua caliente (SI)

| Símbolo | Norma (SI) | Motor (SI) | Desviación |
|---|---:|---:|---:|
| `Re` | 3.69e+05 | 3.6904e+05 | 0.011 % |
| `N_S` | 0.204 | 0.204 | 0.001 % |
| `f_a` | 438.5 | 438.5 | 0.000 % |
| `H_f` | 1.503 | 1.5031 | 0.005 % |
| `H_af` | 0.9395 | 0.93945 | 0.005 % |
| `H_as` | 0.9836 | 0.98364 | 0.004 % |
| `f_n` | 609.1 | 609.06 | 0.006 % |
| `H_c` | 0.8948 | 0.89484 | 0.005 % |
| `f_nc` | 545 | 545.01 | 0.002 % |
| `N_Sc` | 0.02974 | 0.029744 | 0.015 % |
| `f_s` | 160.6 | 160.63 | 0.019 % |
| `V_IR` | 16.01 | 16.013 | 0.022 % |
| `G_SP` | 286.4 | 286.42 | 0.005 % |
| `P_d_IR` | 12420 | 12422 | 0.012 % |
| `S_d_IR_support` | 3.558e+09 | 3.5577e+09 | 0.008 % |
| `K_t_SP` | 2.3 | 2.3 | 0.000 % |
| `S_o_IR_support` | 8.183e+09 | 8.1828e+09 | 0.003 % |
| `F_T` | 0.9795 | 0.97949 | 0.001 % |
| `S_f_adm` | 3.644e+07 | 3.6437e+07 | 0.008 % |
| `G_RD` | 137.3 | 137.34 | 0.030 % |
| `S_d_IR_step` | 1.706e+09 | 1.706e+09 | 0.000 % |
| `K_t_RD` | 1.231 | 1.231 | 0.003 % |
| `S_o_IR_step` | 2.1e+09 | 2.1e+09 | 0.001 % |
| `S_t_support` | 4.776e+05 | 4.7756e+05 | 0.008 % |
| `S_a_support` | 4.388e+05 | 4.3878e+05 | 0.004 % |
| `P_D` | 67820 | 67816 | 0.006 % |
| `S_D_support` | 1.942e+07 | 1.9424e+07 | 0.018 % |
| `S_max_support` | 1.986e+07 | 1.9862e+07 | 0.012 % |
| `S_vm_support` | 1.942e+07 | 1.9424e+07 | 0.019 % |
| `S_t_step` | 6.96e+05 | 6.96e+05 | 0.000 % |
| `S_a_step` | 5.48e+05 | 5.48e+05 | 0.000 % |
| `S_D_step` | 9.31e+06 | 9.314e+06 | 0.042 % |
| `S_max_step` | 9.862e+06 | 9.862e+06 | 0.000 % |
| `S_vm_step` | 9.317e+06 | 9.3175e+06 | 0.005 % |
| `r` | 0.2947 | 0.29473 | 0.010 % |
| `F_M` | 1.095 | 1.0951 | 0.012 % |
| `r_prime` | 0.5895 | 0.58946 | 0.007 % |
| `F_M_prime` | 1.532 | 1.5325 | 0.031 % |
| `P_d` | 4844 | 4844 | 0.000 % |
| `P_l` | 48440 | 48440 | 0.000 % |
| `S_d_support` | 2.126e+06 | 2.1262e+06 | 0.007 % |
| `S_L_support` | 1.519e+07 | 1.5194e+07 | 0.025 % |
| `S_o_support` | 3.529e+07 | 3.5286e+07 | 0.011 % |
| `S_d_step` | 1.02e+06 | 1.0195e+06 | 0.046 % |
| `S_L_step` | 7.286e+06 | 7.2857e+06 | 0.004 % |
| `S_o_step` | 9.056e+06 | 9.0558e+06 | 0.002 % |
| `P_c` | 3.52e+07 | 3.5197e+07 | 0.009 % |
| `P_t` | 4.964e+08 | 4.9638e+08 | 0.005 % |

Desviación máxima: **0.046 %**. Estado global del motor: `warning`.

## Criterios de interpretación adoptados

Donde la norma deja margen, el motor adopta la opción conservadora y lo informa:

| Tema | Decisión del motor |
|---|---|
| Esfuerzos por presión (6-11) | Presión de **operación** manométrica, como en los ejemplos |
| Presión externa admisible (6-13) | Se compara con la presión de **diseño**, usando S a la temperatura de diseño |
| Corrosión (6-2) | Se evalúan los tres casos: nominal, A y t reducidos en c, B y t reducidos en c; vale el peor |
| Magnificación (6-9) | Dentro de la banda 0,8 < r < 1,2 se usa 1/(2ζ); fuera, 1/│1 − r²│ |
| Banda de captura (6-8.4) | Si el límite es 0,8·f_n^c, además se rechaza 0,4 ≤ fs/f_n^c ≤ 0,6 en régimen permanente |
| Paso por resonancia (6-8.5) | Solo con opción explícita, fluido gas o vapor y un límite de fatiga para los ciclos de arranque que da el usuario; el resultado queda en ámbar |
| fs ≥ f_n^c (6-12.5) | Operación supercrítica: se rechaza por estar fuera del alcance |
| Estado del metal (tabla 6-12.3-1) | Roscado, soldado o socket weld: "as welded"; bridado: "welded, then machined"; Van Stone y sanitario: "no welds". Se puede cambiar |
| S_f en la base del escalón | El mismo que en el soporte, como en el ejemplo 8-2 |
| Conexión sanitaria | Fuera del alcance de la norma: se usa H_c de conexión roscada y se avisa |
| Soldado o socket weld (6-7) | Radio de acuerdo b = 0 en H_c y K_t, aunque exista filete exterior |
| Ámbar | Un criterio que cumple con margen menor al 10 % se muestra en ámbar (configurable) |
| Collares de soporte | Nunca se proponen como solución |
