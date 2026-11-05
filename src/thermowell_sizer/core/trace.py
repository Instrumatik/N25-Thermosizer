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

    """

    symbol: str
    description_key: str
    value: float
    kind: QuantityKind
    reference: str
    expression: str
    inputs: Mapping[str, float] = field(default_factory=dict)
    input_kinds: Mapping[str, QuantityKind] = field(default_factory=dict)


class CalcTrace:
    """Secuencia ordenada de pasos de cálculo con acceso por símbolo."""

    def __init__(self) -> None:
        self._entries: list[TraceEntry] = []
        self._by_symbol: dict[str, TraceEntry] = {}

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
    ) -> float:
        """Registra un paso y devuelve ``value`` para poder encadenar cálculos.

        Raises:
            ValueError: si el símbolo ya fue registrado (evita sobrescrituras silenciosas).

        """
        if symbol in self._by_symbol:
            raise ValueError(f"El símbolo '{symbol}' ya está registrado en la traza")
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
        )
        self._entries.append(entry)
        self._by_symbol[symbol] = entry
        return value

    def __getitem__(self, symbol: str) -> TraceEntry:
        """Devuelve el paso que produjo ``symbol``."""
        return self._by_symbol[symbol]

    def __contains__(self, symbol: object) -> bool:
        """Indica si ``symbol`` fue registrado."""
        return symbol in self._by_symbol

    def __iter__(self) -> Iterator[TraceEntry]:
        """Itera los pasos en el orden en que se calcularon."""
        return iter(self._entries)

    def __len__(self) -> int:
        """Cantidad de pasos registrados."""
        return len(self._entries)
