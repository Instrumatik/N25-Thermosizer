# ThermoWell Sizer

Aplicación de escritorio para dimensionar, verificar y seleccionar termopozos
(termovainas) según **ASME PTC 19.3 TW-2016**, con emisión de hoja de datos y
memoria de cálculo trazable.

> **Aviso:** los resultados deben ser revisados por un ingeniero calificado y no
> sustituyen la consulta de la edición vigente de las normas.

## Estado

Fase 1 de 7: arquitectura, modelo de datos y estructura de carpetas.
Ver [`docs/arquitectura.md`](docs/arquitectura.md).

## Desarrollo

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -e ".[dev,gui,reports]"
pytest --cov                      # pruebas + cobertura del motor
mypy                              # tipado estricto
ruff check .                      # estilo
```

Requiere Python 3.12 o superior.
