"""Catálogo de textos. Se ampliará en cada fase; las claves se agrupan por prefijo."""

from __future__ import annotations

from typing import Final

from thermowell_sizer.i18n.catalog_engine import ENGINE_EN, ENGINE_ES

CATALOG: Final[dict[str, dict[str, str]]] = {
    "es": {
        "validation.out_of_range": (
            "Valor {value} fuera del rango de la norma ({min} a {max})."
        ),
        "validation.wall_too_thin": (
            "Pared (B − d)/2 demasiado delgada. Aumente B o reduzca el agujero d."
        ),
        "validation.tip_too_thin": "Espesor de punta t por debajo del mínimo. Auméntelo.",
        "validation.rough_surface": (
            "Rugosidad superior a 0,81 µm Ra: los límites de fatiga de la norma no son "
            "válidos. Especifique un acabado más fino."
        ),
        "validation.fabricated_out_of_scope": (
            "Los termopozos fabricados (de tubo o soldados) están fuera del alcance de la "
            "norma. Use un termopozo de barra maciza."
        ),
        "validation.long_well_ok": (
            "L supera el máximo tabulado; las ecuaciones siguen siendo válidas para "
            "vástagos de una sola pieza."
        ),
        "validation.stepped_tip_not_standard": (
            "El diámetro de punta no es 12,7 ni 22,23 mm: la correlación de frecuencia "
            "natural escalonada no aplica."
        ),
    },
    "en": {
        "validation.out_of_range": "Value {value} outside the standard's range ({min} to {max}).",
        "validation.wall_too_thin": "Wall (B − d)/2 too thin. Increase B or reduce bore d.",
        "validation.tip_too_thin": "Tip thickness t below minimum. Increase it.",
        "validation.rough_surface": (
            "Surface roughness above 0.81 µm Ra: the standard's fatigue limits are not "
            "valid. Specify a finer finish."
        ),
        "validation.fabricated_out_of_scope": (
            "Fabricated (pipe or welded) thermowells are outside the standard's scope. "
            "Use a bar-stock thermowell."
        ),
        "validation.long_well_ok": (
            "L exceeds the tabulated maximum; the equations remain valid for single-piece "
            "shanks."
        ),
        "validation.stepped_tip_not_standard": (
            "Tip diameter is neither 12.7 nor 22.23 mm: the step-shank natural frequency "
            "correlation does not apply."
        ),
    },
}

CATALOG["es"].update(ENGINE_ES)
CATALOG["en"].update(ENGINE_EN)
