"""Idiomas (español / inglés) y formato numérico.

Los textos se buscan por clave. Si una clave falta en el idioma activo se usa el
español y, si tampoco existe, la propia clave (así una traducción faltante se ve
en pantalla en lugar de romper la aplicación).
"""

from __future__ import annotations

from enum import StrEnum

from thermowell_sizer.i18n.catalog import CATALOG


class Language(StrEnum):
    """Idiomas disponibles."""

    ES = "es"
    EN = "en"


DECIMAL_SEPARATOR: dict[Language, str] = {Language.ES: ",", Language.EN: "."}
THOUSANDS_SEPARATOR: dict[Language, str] = {Language.ES: ".", Language.EN: ","}


def tr(key: str, lang: Language = Language.ES, **params: object) -> str:
    """Traduce ``key`` e interpola ``params`` con la sintaxis de ``str.format``."""
    template = CATALOG.get(lang, {}).get(key) or CATALOG[Language.ES].get(key) or key
    return template.format(**params) if params else template


def format_number(
    value: float, decimals: int = 2, lang: Language = Language.ES, *, grouping: bool = False
) -> str:
    """Formatea un número con los separadores del idioma, sin depender del locale del SO.

    >>> format_number(1234.5, 1, Language.ES, grouping=True)
    '1.234,5'
    """
    text = f"{value:,.{decimals}f}" if grouping else f"{value:.{decimals}f}"
    return (
        text.replace(",", "\0")
        .replace(".", DECIMAL_SEPARATOR[lang])
        .replace("\0", THOUSANDS_SEPARATOR[lang])
    )


def parse_number(text: str, lang: Language = Language.ES) -> float:
    """Convierte texto ingresado por el usuario en número.

    Acepta el separador decimal del idioma y también el punto, porque es habitual
    pegar valores desde otras planillas.

    Raises:
        ValueError: si el texto no es un número.

    """
    cleaned = text.strip().replace(" ", "")
    dec = DECIMAL_SEPARATOR[lang]
    thousands = THOUSANDS_SEPARATOR[lang]
    if dec in cleaned:
        cleaned = cleaned.replace(thousands, "").replace(dec, ".")
    return float(cleaned)
