"""Genera los proyectos de ejemplo de ``examples/`` (casos resueltos del manual).

Uso: ``python tools/make_examples.py``. Cada ejemplo se evalúa al generarse para
comprobar que el resultado documentado en el manual sigue siendo el mismo.
"""

from __future__ import annotations

import sys
from pathlib import Path

from thermowell_sizer.core.models import (
    CalcInput,
    FlowBasis,
    FlowCase,
    MaterialRef,
    ShankProfile,
)
from thermowell_sizer.core.units import BAR_PA, INCH_M, KELVIN_OFFSET, STANDARD_ATMOSPHERE_PA
from thermowell_sizer.data.database import Library
from thermowell_sizer.project import (
    Project,
    ProjectInfo,
    ProjectSettings,
    TagRecord,
    save_project,
)
from thermowell_sizer.services import default_input, evaluate

OUT = Path(__file__).resolve().parents[1] / "examples"


def _barg(value: float) -> float:
    return value * BAR_PA + STANDARD_ATMOSPHERE_PA


def _celsius(value: float) -> float:
    return value + KELVIN_OFFSET


def _with(inp: CalcInput, **sections: dict[str, object]) -> CalcInput:
    """Copia ``inp`` cambiando campos de sus secciones (process, pipe, thermowell...)."""
    update: dict[str, object] = {}
    for name, fields in sections.items():
        update[name] = getattr(inp, name).model_copy(update=fields)
    return inp.model_copy(update=update)


def water_line() -> TagRecord:
    """Ejemplo 1: agua de refrigeración, cónico 316 bridado; cumple."""
    inp = default_input("TW-101")
    inp = inp.model_copy(update={"identification": inp.identification.model_copy(
        update={"service": "Agua de refrigeración", "line_or_equipment": "6\"-CW-101",
                "pid": "P&ID-001"})})
    return TagRecord(input=inp)


def steam_header() -> TagRecord:
    """Ejemplo 2: vapor sobrecalentado 40 barg / 400 °C, F22 cónico corto; cumple.

    El grupo B16.5 del F22 no está tabulado en la biblioteca: el programa avisa que
    el rating de la brida debe verificarse aparte.
    """
    base = default_input("TW-201")
    geom = base.thermowell.geometry.model_copy(update={
        "profile": ShankProfile.TAPERED, "L": 0.125, "U": 0.125, "A": 1.25 * INCH_M,
        "B": 1.0 * INCH_M})
    well = base.thermowell.model_copy(update={
        "geometry": geom, "material": MaterialRef(material_id="F22"),
        "connection": base.thermowell.connection.model_copy(update={"rating_class": 600})})
    inp = _with(
        base,
        identification={"service": "Colector de vapor de alta", "pid": "P&ID-002"},
        process={"fluid_id": "water", "operating_pressure": _barg(40),
                 "design_pressure": _barg(45), "operating_temperature": _celsius(400),
                 "design_temperature": _celsius(425),
                 "flow_cases": (FlowCase(label="normal", basis=FlowBasis.VELOCITY,
                                         velocity=25.0),
                                FlowCase(label="max", basis=FlowBasis.VELOCITY,
                                         velocity=35.0))},
        pipe={"nominal_size": "8", "schedule": "80", "inner_diameter": 0.19368},
    )
    return TagRecord(input=inp.model_copy(update={"thermowell": well}))


def gas_failing() -> TagRecord:
    """Ejemplo 3: gas natural a alta velocidad con vástago largo y delgado; NO cumple."""
    base = default_input("TW-301")
    geom = base.thermowell.geometry.model_copy(update={
        "L": 0.400, "U": 0.400, "A": 0.75 * INCH_M, "B": 0.625 * INCH_M})
    well = base.thermowell.model_copy(update={
        "geometry": geom,
        "connection": base.thermowell.connection.model_copy(update={"rating_class": 600})})
    inp = _with(
        base,
        identification={"service": "Gas natural a turbina", "pid": "P&ID-003"},
        process={"fluid_id": "natural_gas", "operating_pressure": _barg(50),
                 "design_pressure": _barg(60), "operating_temperature": _celsius(30),
                 "design_temperature": _celsius(60),
                 "flow_cases": (FlowCase(label="max", basis=FlowBasis.VELOCITY,
                                         velocity=30.0),)},
        pipe={"nominal_size": "12", "schedule": "40", "inner_diameter": 0.30323,  # 12" sch 40
              "nozzle_length": 0.150},
    )
    return TagRecord(input=inp.model_copy(update={"thermowell": well}))


def main() -> int:
    """Escribe los ejemplos y muestra el estado de cada tag."""
    library = Library()
    OUT.mkdir(exist_ok=True)
    examples = {
        "ejemplo_1_agua.tws": ("Ejemplo 1 · Agua de refrigeración", [water_line()]),
        "ejemplo_2_vapor.tws": ("Ejemplo 2 · Vapor de alta presión", [steam_header()]),
        "ejemplo_3_gas_no_cumple.tws": ("Ejemplo 3 · Gas natural (no cumple)",
                                        [gas_failing()]),
    }
    for file, (title, tags) in examples.items():
        project = Project(info=ProjectInfo(name=title, client="Ejemplo",
                                           document_number=file.split(".")[0].upper()),
                          settings=ProjectSettings(), tags=tags)
        for rec in tags:
            ev = evaluate(rec, library, project.settings)
            print(f"{file}: {rec.input.identification.tag} -> {ev.status}"
                  f"{' ' + str(ev.errors) if ev.errors else ''}")
        save_project(project, OUT / file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
