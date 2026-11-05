"""Servicios de aplicación: orquestan biblioteca, propiedades y motor sin depender de Qt.

La interfaz llama a estas funciones; así la lógica queda probada sin ventanas.
"""

from __future__ import annotations

import csv
import io
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from thermowell_sizer.core.advisories import Advisory, advise
from thermowell_sizer.core.models import (
    CalcInput,
    CheckStatus,
    ConnectionType,
    EngineOptions,
    FlangeFace,
    FlowBasis,
    FlowCase,
    FluidProperties,
    Identification,
    MaterialProperties,
    MaterialRef,
    Phase,
    PipeData,
    ProcessConditions,
    ProcessConnection,
    PropertySource,
    SensorSpec,
    SensorType,
    ShankProfile,
    Thermowell,
    ThermowellGeometry,
)
from thermowell_sizer.core.ptc19_3.verify import VerificationResult, case_velocity, verify
from thermowell_sizer.core.tools.heat import (
    THERMAL_BY_FAMILY,
    film_coefficient,
    immersion_error,
    time_constant,
)
from thermowell_sizer.core.units import (
    BAR_PA,
    INCH_M,
    KELVIN_OFFSET,
    STANDARD_ATMOSPHERE_PA,
    QuantityKind,
)
from thermowell_sizer.data.database import Library
from thermowell_sizer.i18n import Language, tr
from thermowell_sizer.project import ProjectSettings, TagRecord
from thermowell_sizer.properties.fluids import (
    FluidPropertyError,
    fluid_state,
    standard_density,
    thermal_properties,
)

FLANGED_TYPES = (ConnectionType.FLANGED, ConnectionType.VAN_STONE)


AMBIENT_TEMPERATURE = 293.15
"""Temperatura supuesta en la base del termopozo (cabezal), K."""
IMMERSION_TOLERANCE = 0.1
"""Error de conducción objetivo para la inmersión mínima recomendada, K."""


@dataclass(frozen=True, slots=True)
class ThermalEstimate:
    """Criterios adicionales (fuera de PTC 19.3 TW): error de inmersión y respuesta."""

    h: float
    immersion_error: float
    min_immersion: float | None
    exposed_length: float
    tau: float
    t90: float
    generic_fluid_data: bool


@dataclass(slots=True)
class Evaluation:
    """Resultado de evaluar un tag completo."""

    input: CalcInput
    options: EngineOptions
    material: MaterialProperties | None = None
    result: VerificationResult | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    thermal: ThermalEstimate | None = None
    advisories: list[Advisory] = field(default_factory=list)

    @property
    def status(self) -> CheckStatus | None:
        """Estado global, o ``None`` si no se pudo calcular."""
        return None if self.result is None else self.result.status


def default_input(tag: str = "TW-001") -> CalcInput:
    """Plantilla razonable para un tag nuevo (agua, 316, cónico, bridado 1½" 300# RF)."""
    geometry = ThermowellGeometry(
        profile=ShankProfile.TAPERED, L=0.150, A=1.0625 * INCH_M, B=0.75 * INCH_M,
        d=0.26 * INCH_M, t=0.25 * INCH_M, b=0.125 * INCH_M, U=0.150,
    )
    return CalcInput(
        identification=Identification(tag=tag),
        process=ProcessConditions(
            fluid_id="water",
            phase=Phase.LIQUID,
            operating_pressure=10 * BAR_PA + STANDARD_ATMOSPHERE_PA,
            design_pressure=15 * BAR_PA + STANDARD_ATMOSPHERE_PA,
            operating_temperature=80 + KELVIN_OFFSET,
            design_temperature=120 + KELVIN_OFFSET,
            flow_cases=(FlowCase(label="normal", basis=FlowBasis.VELOCITY, velocity=2.0),),
            properties=FluidProperties(density=972.0, dynamic_viscosity=3.5e-4,
                                       source=PropertySource.USER),
        ),
        pipe=PipeData(nominal_size="6", schedule="40", inner_diameter=0.15405),
        thermowell=Thermowell(
            geometry=geometry,
            material=MaterialRef(material_id="SS316"),
            connection=ProcessConnection(type=ConnectionType.FLANGED, size="1-1/2",
                                         rating_class=300, face=FlangeFace.RF),
        ),
        sensor=SensorSpec(type=SensorType.RTD_PT100, sheath_diameter=6e-3),
    )


def with_fluid_properties(inp: CalcInput, library: Library) -> tuple[CalcInput, Phase | None]:
    """Recalcula ρ y μ a las condiciones de operación.

    Returns:
        La entrada actualizada y la fase detectada (o ``None`` si se dejó como estaba).

    Raises:
        FluidPropertyError: si no hay datos del fluido.
    """
    proc = inp.process
    state = fluid_state(library, proc.fluid_id, proc.operating_temperature,
                        proc.operating_pressure)
    props = state.properties.model_copy(
        update={"standard_density": standard_density(library, proc.fluid_id)})
    new_proc = proc.model_copy(update={"properties": props, "phase": state.phase})
    return inp.model_copy(update={"process": new_proc}), state.phase


def resolve_options(
    inp: CalcInput, options: EngineOptions, library: Library, settings: ProjectSettings
) -> tuple[EngineOptions, list[str]]:
    """Completa las opciones con la presión barométrica y el rating de brida de biblioteca."""
    notes: list[str] = []
    update: dict[str, object] = {"barometric_pressure": settings.barometric_pressure}
    conn = inp.thermowell.connection
    if conn.type in FLANGED_TYPES and options.flange_rating is None and conn.rating_class:
        try:
            group = library.material(inp.thermowell.material.material_id).b16_5_group
        except KeyError:
            group = None
        rating = library.flange_rating(group, conn.rating_class,
                                       inp.process.design_temperature)
        if rating is None:
            notes.append("svc.flange_rating_unavailable")
        else:
            update["flange_rating"] = rating
    return options.model_copy(update=update), notes


def evaluate(record: TagRecord, library: Library, settings: ProjectSettings) -> Evaluation:
    """Evalúa un tag: propiedades del fluido, material, rating de brida y verificación."""
    inp = record.input
    ev = Evaluation(input=inp, options=record.options)
    if record.auto_properties:
        try:
            inp, _ = with_fluid_properties(inp, library)
            ev.input = inp
        except FluidPropertyError:
            ev.warnings.append("svc.fluid_properties_failed")
    try:
        ev.material = library.material_properties(
            inp.thermowell.material.material_id,
            inp.process.operating_temperature,
            inp.process.design_temperature,
        )
    except KeyError:
        ev.errors.append("svc.material_unknown")
        return ev
    ev.options, notes = resolve_options(inp, record.options, library, settings)
    ev.warnings.extend(notes)
    ev.result = verify(inp, ev.material, ev.options)
    ev.thermal = thermal_estimate(inp, library)
    coating = inp.thermowell.material.coating
    coating_max = next((c[4] for c in library.coatings() if c[0] == coating), None)
    ev.advisories = advise(inp, coating_max_temperature=coating_max)
    return ev


def render_advisory(adv: Advisory, lang: Language,
                    qfmt: Callable[[float, QuantityKind], str],
                    nfmt: Callable[[float], str]) -> str:
    """Texto del aviso con sus valores en las unidades y el idioma pedidos."""
    params: dict[str, object] = {}
    for key, value in adv.params.items():
        if key in adv.kinds and isinstance(value, float):
            params[key] = qfmt(value, adv.kinds[key])
        elif isinstance(value, float):
            params[key] = nfmt(value)
        else:
            params[key] = value
    return tr(adv.key, lang, **params)


def thermal_estimate(inp: CalcInput, library: Library) -> ThermalEstimate | None:
    """Error por conducción e inercia térmica para el caso de mayor velocidad."""
    proc = inp.process
    g = inp.thermowell.geometry
    try:
        info = library.material(inp.thermowell.material.material_id)
    except KeyError:
        return None
    k_wall, cp_wall = THERMAL_BY_FAMILY.get(info.family, THERMAL_BY_FAMILY["austenitic"])
    k_f, cp_f, generic = thermal_properties(library, proc.fluid_id, proc.operating_temperature,
                                            proc.operating_pressure, proc.phase)
    rho, mu = proc.properties.density, proc.properties.dynamic_viscosity
    v = max(case_velocity(inp, c) for c in proc.flow_cases)
    d_mean = (g.A + g.B) / 2
    h = film_coefficient(rho, v, d_mean, mu, k_f, cp_f)
    exposed = max(g.L - g.L0, 1e-6)
    imm = immersion_error(fluid_temperature=proc.operating_temperature,
                          base_temperature=AMBIENT_TEMPERATURE, h=h, length=exposed,
                          outer_diameter=d_mean, bore=g.d, conductivity=k_wall,
                          tolerance=IMMERSION_TOLERANCE)
    h_tip = film_coefficient(rho, v, g.B, mu, k_f, cp_f)
    tau = time_constant(h=h_tip, outer_diameter=g.B, bore=g.d, wall_density=info.density,
                        wall_specific_heat=cp_wall,
                        sensor_diameter=min(inp.sensor.sheath_diameter, g.d))
    return ThermalEstimate(h, imm.error, imm.min_length, exposed, tau.total, tau.t90, generic)


# --- Importación masiva ---------------------------------------------------------------
CSV_COLUMNS = ("tag", "service", "fluid_id", "p_op_barg", "p_design_barg", "t_op_c",
               "t_design_c", "velocity_m_s", "nps", "schedule", "material_id", "L_mm",
               "A_mm", "B_mm", "d_mm", "rating_class")


class RowImportError(ValueError):
    """Fila inválida en un archivo de importación."""


def _num(row: dict[str, str], key: str) -> float:
    text = (row.get(key) or "").strip().replace(",", ".")
    if not text:
        raise RowImportError(f"Falta '{key}'")
    return float(text)


def import_rows(
    rows: list[dict[str, str]], library: Library, barometric: float
) -> tuple[list[TagRecord], list[str]]:
    """Convierte filas (columnas :data:`CSV_COLUMNS`) en tags; devuelve también los errores."""
    records: list[TagRecord] = []
    errors: list[str] = []
    base = default_input()
    for n, row in enumerate(rows, start=2):
        try:
            pipe = library.pipe(row["nps"].strip(), row["schedule"].strip())
            geom = base.thermowell.geometry.model_copy(update={
                "L": _num(row, "L_mm") / 1e3, "A": _num(row, "A_mm") / 1e3,
                "B": _num(row, "B_mm") / 1e3, "d": _num(row, "d_mm") / 1e3,
                "U": _num(row, "L_mm") / 1e3,
                "profile": ShankProfile.STRAIGHT if row["A_mm"] == row["B_mm"]
                else ShankProfile.TAPERED,
            })
            inp = CalcInput.model_validate({
                **base.model_dump(),
                "identification": {"tag": row["tag"].strip(),
                                   "service": row.get("service", "")},
                "process": {
                    **base.process.model_dump(),
                    "fluid_id": row["fluid_id"].strip(),
                    "operating_pressure": _num(row, "p_op_barg") * BAR_PA + barometric,
                    "design_pressure": _num(row, "p_design_barg") * BAR_PA + barometric,
                    "operating_temperature": _num(row, "t_op_c") + KELVIN_OFFSET,
                    "design_temperature": _num(row, "t_design_c") + KELVIN_OFFSET,
                    "flow_cases": [{"label": "max", "basis": "velocity",
                                    "velocity": _num(row, "velocity_m_s")}],
                },
                "pipe": {"nominal_size": pipe.nps, "schedule": pipe.schedule,
                         "inner_diameter": pipe.inner_diameter},
                "thermowell": {
                    "geometry": geom.model_dump(),
                    "material": {"material_id": row["material_id"].strip()},
                    "connection": {**base.thermowell.connection.model_dump(),
                                   "rating_class": int(_num(row, "rating_class"))},
                },
            })
            library.material(inp.thermowell.material.material_id)
            records.append(TagRecord(input=inp))
        except (KeyError, ValueError) as exc:
            errors.append(f"Fila {n}: {exc}")
    return records, errors


def read_table(path: Path) -> list[dict[str, str]]:
    """Lee un CSV (``;`` o ``,``) o la primera hoja de un Excel como lista de filas."""
    if path.suffix.lower() in (".xlsx", ".xlsm"):
        from openpyxl import load_workbook

        wb = load_workbook(path, read_only=True, data_only=True)
        ws = wb.worksheets[0]
        values = [["" if c is None else str(c) for c in r]
                  for r in ws.iter_rows(values_only=True)]
        wb.close()
        if not values:
            return []
        header = [h.strip() for h in values[0]]
        return [dict(zip(header, r, strict=False)) for r in values[1:] if any(r)]
    text = path.read_text(encoding="utf-8-sig")
    dialect = csv.Sniffer().sniff(text.splitlines()[0], delimiters=";,\t")
    return list(csv.DictReader(io.StringIO(text), dialect=dialect))


def template_csv() -> str:
    """Plantilla CSV con una fila de ejemplo."""
    example = ("TW-101", "Agua de enfriamiento", "water", "6", "10", "35", "60", "2,5", "6",
               "40", "SS316", "200", "27", "19", "6,6", "300")
    return ";".join(CSV_COLUMNS) + "\n" + ";".join(example) + "\n"
