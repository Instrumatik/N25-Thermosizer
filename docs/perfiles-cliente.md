# Perfiles de especificación de cliente

Un perfil es un archivo JSON que describe los termopozos normalizados de una
especificación de empresa. ThermoWell Sizer lo usa para elegir el modelo según la línea
y cargar sus cotas. Los perfiles **no se distribuyen con el programa**: cada usuario
importa los de sus clientes desde *Termopozo › Diseño típico / especificación… ›
Importar perfil…*, y quedan en `%APPDATA%\InstruMatik\ThermoWellSizer\perfiles`.

Las especificaciones de empresa suelen ser documentos privados: cargue en el perfil solo
los datos que necesita (modelos, largos y tablas de aplicación) y respete las
condiciones de uso del documento original.

## Formato

```json
{
  "id": "mi_cliente",
  "name": "Cliente X — especificación de termopozos",
  "description": "Texto libre.",
  "private": true,
  "default_bore_mm": 6.6,
  "max_nps": "16",
  "models": {
    "F1": {"design": "flanged_tapered", "U_mm": 250, "size": "1-1/2"},
    "F2": {"design": "flanged_tapered", "U_mm": 320, "size": "1-1/2",
           "A_mm": 27.0, "B_mm": 19.0, "bore_mm": 7.0, "nozzle_mm": 150,
           "note": "Texto que se muestra al elegir el modelo."}
  },
  "rules": [
    {"connection": "flanged", "mounting": "perpendicular",
     "rating_min": 0, "rating_max": 600,
     "by_nps": {"3": "F1", "8": "F2", "2": null}}
  ],
  "nozzles": [
    {"rating_max": 600, "length_mm": 150},
    {"rating_max": 99999, "length_mm": 200}
  ],
  "notes": ["Notas generales del perfil."]
}
```

| Campo | Significado |
|---|---|
| `models.<id>.design` | Ejecución del catálogo genérico: `threaded_tapered`, `threaded_straight`, `threaded_stepped`, `flanged_tapered`, `flanged_straight`, `flanged_stepped`, `socket_tapered`, `weld_in_tapered`, `van_stone_tapered`. |
| `U_mm` | Largo de inserción del modelo, mm (se usa también como L). |
| `A_mm`, `B_mm`, `bore_mm` | Opcionales: diámetros propios del modelo. Si faltan se usan los del catálogo genérico adaptados al agujero. |
| `nozzle_mm` | Opcional: proyección de tobera o acople del modelo (L0). Si falta se usa la tabla `nozzles` por rating. |
| `rules` | Tabla de aplicación. `connection`: `flanged`, `threaded`, `weld_in`, `socket_weld`, `van_stone`; `mounting`: `elbow` o `perpendicular`. `by_nps` asigna un modelo a cada NPS; `null` = montaje no permitido. |
| `max_nps` | Las líneas mayores usan la columna de este NPS. |

Reglas de selección: el programa usa la columna del NPS igual o inmediato inferior al de
la línea; si la línea es menor que el primer NPS de la tabla, avisa que debe ampliarse.
Cuando el tag ya tiene una longitud de tobera cargada, se respeta esa.
