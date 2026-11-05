"""Registro trazable de cálculo.

Cada valor que aparece en la memoria de cálculo se registra como un
:class:`TraceEntry` con su símbolo, la referencia a la ecuación de la norma, la
expresión simbólica, los valores sustituidos y el resultado. Las funciones del motor
son puras y no conocen este registro: es el orquestador quien llama a
:meth:`CalcTrace.record` después de cada paso.

Las expresiones se escriben con redacción propia (LaTeX simplificado); de la norma
solo se cita el número de ecuación o de párrafo.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field

from thermowell_sizer.core.units import QuantityKind


@dataclass(frozen=True, slots=True)
class TraceEntry:
    """Un paso del cálculo, listo para mostrarse en la memoria.

    Attributes:
        symbol: símbolo del resultado (p. ej. ``"f_s"``).
        description_key: clave i18n de la descripción (p. ej. ``"trace.fs"``).
        value: resultado en SI.
        kind: magnitud física del resultado, para convertir unidades al reportar.
        reference: referencia normativa (p. ej. ``"ASME PTC 19.3 TW-2016, eq. (6-4-1)"``).
        expression: expresión simbólica en LaTeX.
        inputs: símbolos de entrada usados en la sustitución y sus valores SI.
        input_kinds: magnitud de cada entrada, para presentar la sustitución.
        scope: caso al que pertenece el paso (p. ej. ``"max"`` o ``"max · corrosión raíz"``);
            vacío para valores comunes a todos los casos.

    """

    symbol: str
    description_key: str
    value: float
    kind: QuantityKind
    reference: str
    expression: str
    inputs: Mapping[str, float] = field(default_factory=dict)
    input_kinds: Mapping[str, QuantityKind] = field(default_factory=dict)
    scope: str = ""


class CalcTrace:
    """Secuencia ordenada de pasos de cálculo con acceso por símbolo."""

    def __init__(self) -> None:
        self._entries: list[TraceEntry] = []
        self._by_key: dict[tuple[str, str], TraceEntry] = {}

    def record(
        self,
        symbol: str,
        value: float,
        *,
        kind: QuantityKind,
        reference: str,
        expression: str,
        description_key: str,
        inputs: Mapping[str, tuple[float, QuantityKind]] | None = None,
        scope: str = "",
    ) -> float:
        """Registra un paso y devuelve ``value`` para poder encadenar cálculos.

        Raises:
            ValueError: si el símbolo ya fue registrado en el mismo ``scope``
                (evita sobrescrituras silenciosas).

        """
        key = (scope, symbol)
        if key in self._by_key:
            raise ValueError(f"El símbolo '{symbol}' ya está registrado en la traza ({scope})")
        raw = inputs or {}
        entry = TraceEntry(
            symbol=symbol,
            description_key=description_key,
            value=value,
            kind=kind,
            reference=reference,
            expression=expression,
            inputs={k: v for k, (v, _) in raw.items()},
            input_kinds={k: q for k, (_, q) in raw.items()},
            scope=scope,
        )
        self._entries.append(entry)
        self._by_key[key] = entry
        return value

    def get(self, symbol: str, scope: str = "") -> TraceEntry:
        """Devuelve el paso que produjo ``symbol`` en ``scope``.

        Raises:
            KeyError: si no existe.
        """
        return self._by_key[(scope, symbol)]

    def value(self, symbol: str, scope: str = "") -> float:
        """Atajo para el valor SI de ``symbol`` en ``scope``."""
        return self.get(symbol, scope).value

    def __getitem__(self, symbol: str) -> TraceEntry:
        """Devuelve el paso que produjo ``symbol`` sin ``scope``."""
        return self.get(symbol)

    def __contains__(self, symbol: object) -> bool:
        """Indica si ``symbol`` fue registrado sin ``scope``."""
        return ("", symbol) in self._by_key

    def scopes(self) -> list[str]:
        """Casos presentes en la traza, en orden de aparición."""
        return list(dict.fromkeys(e.scope for e in self._entries))

    def __iter__(self) -> Iterator[TraceEntry]:
        """Itera los pasos en el orden en que se calcularon."""
        return iter(self._entries)

    def __len__(self) -> int:
        """Cantidad de pasos registrados."""
        return len(self._entries)
