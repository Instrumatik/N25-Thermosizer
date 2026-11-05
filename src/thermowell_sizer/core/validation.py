"""Validación en tiempo real de la geometría frente a los límites de alcance de la norma.

A diferencia de los validadores de :mod:`models` (que rechazan datos imposibles),
estas comprobaciones devuelven **avisos** que la interfaz muestra junto a cada campo:
el dato es físicamente posible pero queda fuera del alcance de la norma o es dudoso.
Los mensajes se resuelven con el catálogo i18n a partir de ``message_key``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from dataclasses import field as dc_field
from enum import StrEnum

from thermowell_sizer.core import constants as k
from thermowell_sizer.core.models import Construction, ShankProfile, ThermowellGeometry


class Severity(StrEnum):
    """Gravedad de un aviso de validación."""

    ERROR = "error"
    """Fuera del alcance: el cálculo no puede declararse conforme."""
    WARNING = "warning"
    """Se puede calcular, pero el resultado requiere juicio de ingeniería."""
    INFO = "info"


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """Aviso asociado a un campo de la entrada."""

    field: str
    severity: Severity
    message_key: str
    reference: str
    params: dict[str, float | str] = dc_field(default_factory=dict)


def _check_range(
    issues: list[ValidationIssue],
    field_name: str,
    value: float,
    rng: k.Range,
    reference: str,
    severity: Severity = Severity.ERROR,
) -> None:
    if not rng.contains(value):
        issues.append(
            ValidationIssue(
                field=field_name,
                severity=severity,
                message_key="validation.out_of_range",
                reference=reference,
                params={
                    "value": value,
                    "min": rng.minimum if rng.minimum is not None else "—",
                    "max": rng.maximum if rng.maximum is not None else "—",
                },
            )
        )


def validate_geometry(g: ThermowellGeometry) -> list[ValidationIssue]:
    """Comprueba la geometría contra las tablas 4-1-1 / 4-2-1 y el párr. 1-2.

    Returns:
        Lista de avisos, vacía si la geometría está dentro del alcance.

    """
    issues: list[ValidationIssue] = []

    if g.construction is Construction.FABRICATED:
        issues.append(
            ValidationIssue(
                "construction", Severity.ERROR, "validation.fabricated_out_of_scope",
                k.ref("para. 1-2"),
            )
        )

    wall = (g.B - g.d) / 2.0
    if wall < k.MIN_WALL_THICKNESS:
        issues.append(
            ValidationIssue(
                "d", Severity.ERROR, "validation.wall_too_thin", k.TABLE_4_1_1,
                {"value": wall, "min": k.MIN_WALL_THICKNESS},
            )
        )
    if g.t < k.MIN_TIP_THICKNESS:
        issues.append(
            ValidationIssue(
                "t", Severity.ERROR, "validation.tip_too_thin", k.TABLE_4_1_1,
                {"value": g.t, "min": k.MIN_TIP_THICKNESS},
            )
        )
    if g.surface_finish_ra > k.REFERENCE_SURFACE_FINISH_RA:
        issues.append(
            ValidationIssue(
                "surface_finish_ra", Severity.WARNING, "validation.rough_surface", k.PARA_4_2,
                {"value": g.surface_finish_ra, "max": k.REFERENCE_SURFACE_FINISH_RA},
            )
        )

    if g.profile is ShankProfile.STEPPED:
        _validate_stepped(g, issues)
    else:
        _validate_straight_tapered(g, issues)
    return issues


def _validate_straight_tapered(g: ThermowellGeometry, issues: list[ValidationIssue]) -> None:
    ref = k.TABLE_4_1_1
    # Por debajo del mínimo: fuera de alcance (nota 1). Por encima del máximo las
    # ecuaciones siguen valiendo (nota 2): solo se informa.
    l_min, l_max = k.STRAIGHT_TAPERED_L.minimum, k.STRAIGHT_TAPERED_L.maximum
    if l_min is not None and l_min > g.L:
        _check_range(issues, "L", g.L, k.STRAIGHT_TAPERED_L, ref)
    elif l_max is not None and l_max < g.L:
        issues.append(
            ValidationIssue("L", Severity.INFO, "validation.long_well_ok", ref, {"value": g.L})
        )
    _check_range(issues, "d", g.d, k.STRAIGHT_TAPERED_D_BORE, ref)
    _check_range(issues, "B", g.B, k.STRAIGHT_TAPERED_B, ref)
    _check_range(issues, "B", g.B / g.A, k.STRAIGHT_TAPERED_TAPER_RATIO, ref)
    _check_range(issues, "d", g.d / g.B, k.STRAIGHT_TAPERED_BORE_RATIO, ref)
    _check_range(issues, "L", g.L / g.B, k.STRAIGHT_TAPERED_ASPECT_RATIO, ref)


def _validate_stepped(g: ThermowellGeometry, issues: list[ValidationIssue]) -> None:
    ref = k.TABLE_4_2_1
    _check_range(issues, "L", g.L, k.STEPPED_L, ref)
    _check_range(issues, "d", g.d, k.STEPPED_D_BORE, ref)
    _check_range(issues, "Ls", g.Ls / g.L, k.STEPPED_LENGTH_RATIO, ref)

    tip = next(
        (
            b
            for b in k.STEPPED_TIP_DIAMETERS
            if math.isclose(g.B, b, rel_tol=k.TOLERANCE_DIAMETER_REL)
        ),
        None,
    )
    if tip is None:
        # La correlación de fn escalonada no aplica; el resto de los métodos sí (nota 1).
        issues.append(
            ValidationIssue(
                "B", Severity.WARNING, "validation.stepped_tip_not_standard", ref,
                {"value": g.B},
            )
        )
        return
    _check_range(issues, "A", g.B / g.A, k.STEPPED_STEP_RATIO_BY_TIP[tip], ref)
