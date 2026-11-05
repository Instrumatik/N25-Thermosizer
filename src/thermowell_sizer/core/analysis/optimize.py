"""Optimización automática: alternativas cuando el diseño no cumple.

Orden de preferencia: reducir L, aumentar el diámetro de raíz A, cambiar a perfil
cónico, cambiar el material y, por último, cambiar la conexión. No se proponen
collares de soporte: la edición vigente de la norma los deja fuera de su alcance y
desaconseja su uso (párr. 6-7 e).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import StrEnum

from thermowell_sizer.core import constants as k
from thermowell_sizer.core.models import (
    CalcInput,
    CheckStatus,
    ConnectionType,
    EngineOptions,
    MaterialProperties,
    ShankProfile,
    ThermowellGeometry,
)
from thermowell_sizer.core.ptc19_3.verify import VerificationResult, verify

LENGTH_RESOLUTION = 0.001
"""Resolución de la búsqueda de L, m (criterio del programa)."""
DIAMETER_STEP = 0.0005
"""Paso de la búsqueda del diámetro de raíz, m (criterio del programa)."""
NO_COLLARS_NOTE = "note.no_velocity_collars"


class AlternativeKind(StrEnum):
    """Tipo de alternativa propuesta."""

    REDUCE_LENGTH = "reduce_length"
    INCREASE_ROOT = "increase_root"
    TAPERED_PROFILE = "tapered_profile"
    CHANGE_MATERIAL = "change_material"
    CHANGE_CONNECTION = "change_connection"


REASONS: dict[AlternativeKind, str] = {
    AlternativeKind.REDUCE_LENGTH: "opt.reason.reduce_length",
    AlternativeKind.INCREASE_ROOT: "opt.reason.increase_root",
    AlternativeKind.TAPERED_PROFILE: "opt.reason.tapered_profile",
    AlternativeKind.CHANGE_MATERIAL: "opt.reason.change_material",
    AlternativeKind.CHANGE_CONNECTION: "opt.reason.change_connection",
}


@dataclass(frozen=True, slots=True)
class Alternative:
    """Una alternativa que cumple, con el resultado de su verificación."""

    kind: AlternativeKind
    reason_key: str
    input: CalcInput
    material: MaterialProperties
    result: VerificationResult
    changes: dict[str, float | str]


def _passes(result: VerificationResult) -> bool:
    return result.status is not CheckStatus.FAIL


def _with_geometry(inp: CalcInput, **changes: object) -> CalcInput | None:
    data = inp.thermowell.geometry.model_dump() | changes
    try:
        geom = ThermowellGeometry.model_validate(data)
    except ValueError:
        return None
    tw = inp.thermowell.model_copy(update={"geometry": geom})
    return inp.model_copy(update={"thermowell": tw})


def _search_max(
    lo: float, hi: float, ok: Callable[[float], bool], resolution: float
) -> float | None:
    """Mayor x en [lo, hi] con ok(x), suponiendo ok monótona decreciente."""
    if not ok(lo):
        return None
    while hi - lo > resolution:
        mid = (lo + hi) / 2.0
        lo, hi = (mid, hi) if ok(mid) else (lo, mid)
    return lo


def propose_alternatives(
    inp: CalcInput,
    material: MaterialProperties,
    options: EngineOptions | None = None,
    *,
    candidate_materials: Sequence[MaterialProperties] = (),
    min_length: float | None = None,
) -> list[Alternative]:
    """Propone alternativas que cumplen, ordenadas por preferencia.

    Args:
        inp: datos del tag que no cumple.
        material: material actual.
        options: opciones del motor.
        candidate_materials: materiales a probar (ya evaluados a la temperatura).
        min_length: L mínima aceptable por la medición; por defecto el mínimo de la
            tabla 4-1-1 o 4-2-1.

    Returns:
        Lista de alternativas; vacía si el diseño actual ya cumple o nada funciona.
    """
    opts = options or EngineOptions()
    if _passes(verify(inp, material, opts)):
        return []
    g = inp.thermowell.geometry
    out: list[Alternative] = []

    def evaluate(candidate: CalcInput | None, mat: MaterialProperties) -> VerificationResult | None:
        if candidate is None:
            return None
        result = verify(candidate, mat, opts)
        return result if _passes(result) else None

    def add(kind: AlternativeKind, candidate: CalcInput | None, mat: MaterialProperties,
            changes: dict[str, float | str]) -> None:
        result = evaluate(candidate, mat)
        if result is not None and candidate is not None:
            out.append(Alternative(kind, REASONS[kind], candidate, mat, result, changes))

    # 1. Reducir L (sube f_n^c con 1/L² y baja el momento flector con L²).
    stepped = g.profile is ShankProfile.STEPPED
    table_min = k.STEPPED_L.minimum if stepped else k.STRAIGHT_TAPERED_L.minimum
    floor = max(min_length or 0.0, table_min or 0.0, g.Ls * 1.01 if stepped else 0.0)
    if floor < g.L:
        def length_ok(length: float) -> bool:
            cand = _with_geometry(inp, L=length, U=length)
            return evaluate(cand, material) is not None

        best = _search_max(floor, g.L, length_ok, LENGTH_RESOLUTION)
        if best is not None:
            add(AlternativeKind.REDUCE_LENGTH, _with_geometry(inp, L=best, U=best), material,
                {"L": best})

    # 2. Aumentar el diámetro de raíz A (sube EI y baja el esfuerzo).
    if g.profile is not ShankProfile.STRAIGHT:
        if stepped:
            tip = min(k.STEPPED_TIP_DIAMETERS, key=lambda b: abs(b - g.B))
            ratio = k.STEPPED_STEP_RATIO_BY_TIP[tip].minimum or 0.5
        else:
            ratio = k.STRAIGHT_TAPERED_TAPER_RATIO.minimum or 0.58
        a_max = g.B / ratio
        a = g.A + DIAMETER_STEP
        while a <= a_max:
            cand = _with_geometry(inp, A=a)
            if evaluate(cand, material) is not None:
                add(AlternativeKind.INCREASE_ROOT, cand, material, {"A": a})
                break
            a += DIAMETER_STEP

    # 3. Perfil cónico (recto → cónico con la mayor raíz admitida por la tabla 4-1-1).
    if g.profile is ShankProfile.STRAIGHT:
        ratio = k.STRAIGHT_TAPERED_TAPER_RATIO.minimum or 0.58
        a_new = g.B / ratio
        cand = _with_geometry(inp, profile=ShankProfile.TAPERED, A=a_new)
        add(AlternativeKind.TAPERED_PROFILE, cand, material, {"profile": "tapered", "A": a_new})

    # 4. Cambiar el material.
    for mat in candidate_materials:
        if mat.material_id != material.material_id:
            add(AlternativeKind.CHANGE_MATERIAL, inp, mat, {"material_id": mat.material_id})

    # 5. Cambiar la conexión (roscada → bridada: mejor H_c, K_t y S_f).
    if inp.thermowell.connection.type in (ConnectionType.THREADED, ConnectionType.SANITARY):
        conn = inp.thermowell.connection.model_copy(
            update={"type": ConnectionType.FLANGED, "rating_class": 300}
        )
        tw = inp.thermowell.model_copy(update={"connection": conn})
        add(AlternativeKind.CHANGE_CONNECTION, inp.model_copy(update={"thermowell": tw}),
            material, {"connection": ConnectionType.FLANGED.value})
    return out
