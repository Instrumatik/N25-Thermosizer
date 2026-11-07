# ThermoWell Sizer

Aplicación de escritorio para dimensionar, verificar y seleccionar termopozos
(termovainas) según **ASME PTC 19.3 TW-2016**, con emisión de hoja de datos y
memoria de cálculo trazable.

> **Aviso:** los resultados deben ser revisados por un ingeniero calificado y no
> sustituyen la consulta de la edición vigente de las normas.

## Estado

Versión 1.4.0: las 7 fases del plan, las mejoras de la fase 8 y las revisiones 1.2, 1.3 y 1.4 están completas ([cambios](CHANGELOG.md)).

| Documento | Contenido |
|---|---|
| [Manual de usuario](docs/manual-usuario.md) | Instalación, licencia, flujo de trabajo, ejemplos |
| [Arquitectura](docs/arquitectura.md) | Diseño, modelo de datos, plan de fases |
| [Validación del motor](docs/validacion-motor.md) | Casos de referencia de la norma |
| [Biblioteca de datos](docs/datos-biblioteca.md) | Materiales, fluidos, bridas, fuentes |
| [Interfaz](docs/interfaz.md), [calculadoras](docs/calculadoras.md), [reportes](docs/reportes.md) | Detalle de cada módulo |
| [Licencias y distribución](docs/licencias.md) | Emisión de licencias e instalador (uso interno) |

Proyectos de ejemplo en [`examples/`](examples/) (se regeneran con
`python tools/make_examples.py`).

## Desarrollo

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -e ".[dev,gui,reports,licensing]"
pytest --cov                      # pruebas + cobertura del motor
mypy                              # tipado estricto
ruff check .                      # estilo
```

Requiere Python 3.12 o superior. Para abrir el programa: `thermowell-sizer`.
El instalador de Windows se genera con el flujo *Release Windows* de GitHub Actions
(ver [licencias y distribución](docs/licencias.md)).
