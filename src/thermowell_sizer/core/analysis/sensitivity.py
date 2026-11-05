"""Análisis de sensibilidad: barrido de velocidad y de longitud no soportada.

Alimenta las gráficas de la memoria de cálculo (fs y f_n^c frente a la velocidad,
esfuerzo frente a la longitud de inserción) y la velocidad máxima admisible.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from thermowell_sizer.core.models import (
    CalcInput,
    CheckStatus,
    EngineOptions,
    FlowBasis,
    FlowCase,
    MaterialProperties,
)
from thermowell_sizer.core.ptc19_3.verify import VerificationResult, verify

_VIBRATION_CRITERIA = ("frequency_limit", "inline_lockin_dwell", "dynamic_stress", "steady_stress")
VELOCITY_RESOLUTION = 0.01
"""Resolución de la búsqueda de la velocidad máxima, m/s (criterio del programa)."""


@dataclass(frozen=True, slots=True)
class SweepPoint:
    """Un punto de un barrido."""

    x: float
    fs: float
    fnc: float
    fs_limit: float | None
    dynamic_stress: float
    dynamic_allowable: float
    steady_stress: float
    steady_allowable: float
    status: CheckStatus


def _single_case(inp: CalcInput, velocity: float) -> CalcInput:
    case = FlowCase(label="sweep", basis=FlowBasis.VELOCITY, velocity=velocity)
    process = inp.process.model_copy(update={"flow_cases": (case,)})
    return inp.model_copy(update={"process": process})


def _nominal_options(options: EngineOptions | None) -> EngineOptions:
    return (options or EngineOptions()).model_copy(update={"corrosion_cases": False})


def _vibration_status(result: VerificationResult) -> CheckStatus:
    relevant = [
        c.status
        for c in result.checks
        if c.criterion_id.startswith(_VIBRATION_CRITERIA)
        and c.status is not CheckStatus.NOT_APPLICABLE
    ]
    if CheckStatus.FAIL in relevant:
        return CheckStatus.FAIL
    if CheckStatus.WARNING in relevant:
        return CheckStatus.WARNING
    return CheckStatus.PASS


def _point(x: float, result: VerificationResult) -> SweepPoint:
    case = result.cases[0]
    dyn = result.worst("dynamic_stress_support")
    stat = result.worst("steady_stress_support")
    return SweepPoint(
        x=x,
        fs=case.fs,
        fnc=case.fnc,
        fs_limit=case.frequency_ratio_limit * case.fnc
        if case.frequency_ratio_limit is not None
        else None,
        dynamic_stress=dyn.value if dyn else 0.0,
        dynamic_allowable=dyn.limit if dyn else 0.0,
        steady_stress=stat.value if stat else 0.0,
        steady_allowable=stat.limit if stat else 0.0,
        status=_vibration_status(result),
    )


def velocity_sweep(
    inp: CalcInput,
    material: MaterialProperties,
    velocities: Sequence[float],
    options: EngineOptions | None = None,
) -> list[SweepPoint]:
    """Evalúa la geometría nominal para cada velocidad (m/s)."""
    opts = _nominal_options(options)
    return [_point(v, verify(_single_case(inp, v), material, opts)) for v in velocities]


def length_sweep(
    inp: CalcInput,
    material: MaterialProperties,
    lengths: Sequence[float],
    velocity: float,
    options: EngineOptions | None = None,
) -> list[SweepPoint]:
    """Evalúa la velocidad dada para cada longitud no soportada L (m)."""
    opts = _nominal_options(options)
    base = _single_case(inp, velocity)
    points: list[SweepPoint] = []
    for length in lengths:
        geom = base.thermowell.geometry.model_copy(update={"L": length, "U": length})
        tw = base.thermowell.model_copy(update={"geometry": geom})
        result = verify(base.model_copy(update={"thermowell": tw}), material, opts)
        points.append(_point(length, result))
    return points


def max_allowable_velocity(
    inp: CalcInput,
    material: MaterialProperties,
    options: EngineOptions | None = None,
    *,
    v_max: float = 200.0,
    samples: int = 400,
) -> float | None:
    """Velocidad máxima tal que todas las velocidades menores cumplen los criterios.

    Recorre el intervalo (0, v_max] y refina por bisección el primer fallo. Considera solo
    los criterios que dependen de la velocidad (frecuencia y esfuerzos).

    Returns:
        La velocidad en m/s, o ``None`` si no hay fallos hasta ``v_max``.
    """
    opts = _nominal_options(options)

    def fails(v: float) -> bool:
        result = verify(_single_case(inp, v), material, opts)
        return _vibration_status(result) is CheckStatus.FAIL

    step = v_max / samples
    previous = 0.0
    for i in range(1, samples + 1):
        v = i * step
        if fails(v):
            lo, hi = previous, v
            while hi - lo > VELOCITY_RESOLUTION:
                mid = (lo + hi) / 2.0
                lo, hi = (lo, mid) if fails(mid) else (mid, hi)
            return lo
        previous = v
    return None
