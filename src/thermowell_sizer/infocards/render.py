"""Arma el HTML de una ficha con sus imágenes (fórmulas, diagramas, curvas y ejemplo)."""

from __future__ import annotations

import html
from collections.abc import Callable
from dataclasses import dataclass, field

from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.infocards.content import SECTION_TITLES, SECTIONS, Card
from thermowell_sizer.infocards.curves import curve
from thermowell_sizer.infocards.images import (
    connection_diagram,
    mount_diagram,
    orientation_diagram,
    thermowell_diagram,
)
from thermowell_sizer.reports.mathrender import plain, render_png
from thermowell_sizer.services import Evaluation
from thermowell_sizer.summary import input_rows

QFmt = Callable[[float, QuantityKind], str]

# Ficha → dato de entrada de la planilla (para el valor del tag en el ejemplo)
_INPUT_OF = {"f.p_op": "in.pressure", "f.t_op": "in.temperature", "f.density": "in.density",
             "f.viscosity": "in.viscosity", "f.pipe_id": "in.pipe_id", "f.mount": "in.hs",
             "f.nozzle_id": "in.nozzle_id", "f.A": "in.root", "f.B": "in.tip",
             "f.d": "in.bore", "f.E_manual": "in.E", "f.S_manual": "in.S",
             "f.L": "in.unsupported", "f.U": "in.unsupported", "f.value": "in.flow",
             "f.basis": "in.flow"}


@dataclass
class RenderedCard:
    """HTML listo para un QTextBrowser y las imágenes que referencia (``img:<nombre>``)."""

    html: str
    images: dict[str, bytes] = field(default_factory=dict)


def _sym_match(symbol: str, wanted: str) -> bool:
    return symbol == wanted or symbol.startswith(wanted + "_")


def _example_rows(card: Card, ev: Evaluation | None, qfmt: QFmt, es: bool,
                  images: dict[str, bytes] | None = None, prefix: str = "") -> list[str]:
    """Filas «símbolo = expresión = sustitución = valor» con los datos de una evaluación."""
    if ev is None:
        return []
    rows: list[str] = []
    key = _INPUT_OF.get(card.id)
    if key is not None:
        for r in input_rows(ev, auto_properties=True):
            if r.key == key and isinstance(r.value, float) and r.kind is not None:
                rows.append(f"<li>{html.escape(card.title[0 if es else 1])} = "
                            f"<b>{html.escape(qfmt(r.value, r.kind))}</b></li>")
    if ev.result is None:
        return rows
    first_scope = ev.result.cases[0].scope if ev.result.cases else ""
    seen: set[str] = set()
    for wanted in card.symbols:
        for e in ev.result.trace:
            if not _sym_match(e.symbol, wanted) or e.symbol in seen:
                continue
            if e.scope not in ("", first_scope):
                continue
            seen.add(e.symbol)
            subs = ", ".join(f"{k} = {qfmt(v, e.input_kinds.get(k, QuantityKind.DIMENSIONLESS))}"
                             for k, v in e.inputs.items())
            line = f"<b>{html.escape(e.symbol)}</b>"
            png = render_png(e.expression) if e.expression and images is not None else None
            if png is not None and images is not None:
                name = f"{prefix}{len(images)}"
                images[name] = png
                line += f': <img src="img:{name}" style="vertical-align:middle">'
            elif e.expression:
                line += f": {html.escape(plain(e.expression))}"
            if subs:
                line += f"<br/>&nbsp;&nbsp;{html.escape(subs)}"
            line += f"<br/>&nbsp;&nbsp;→ <b>{html.escape(qfmt(e.value, e.kind))}</b>"
            rows.append(f"<li>{line}</li>")
            break
    return rows


def render_card(card: Card, ev: Evaluation | None, reference: Evaluation | None, *,
                es: bool, qfmt: QFmt, tag: str = "", images: bool = True) -> RenderedCard:
    """HTML de la ficha. ``ev`` es el tag actual; ``reference`` el caso de referencia."""
    out = RenderedCard("")
    lang = "es" if es else "en"
    parts = [f"<h2>{html.escape(card.title[0 if es else 1])}</h2>"]
    for sec in SECTIONS:
        text = card.text(sec, es)
        if text:
            parts.append(f"<h4>{SECTION_TITLES[sec][0 if es else 1]}</h4>"
                         f"<p>{html.escape(text)}</p>")
    if card.formulas:
        parts.append(f"<h4>{SECTION_TITLES['formulas'][0 if es else 1]}</h4>")
        for i, expr in enumerate(card.formulas):
            png = render_png(expr) if images else None
            if png is None:
                parts.append(f"<p><code>{html.escape(plain(expr))}</code></p>")
            else:
                name = f"f{i}"
                out.images[name] = png
                parts.append(f'<p><img src="img:{name}"></p>')
    if card.diagram and images:
        kind, _, dim = card.diagram.partition(":")
        png = {"tw": lambda: thermowell_diagram(dim, lang), "mount": lambda: mount_diagram(lang),
               "orientation": lambda: orientation_diagram(lang),
               "connection": lambda: connection_diagram(lang)}[kind]()
        out.images["diagram"] = png
        parts.append(f"<h4>{SECTION_TITLES['diagram'][0 if es else 1]}</h4>"
                     '<p><img src="img:diagram"></p>')
    if card.curves and images and ev is not None:
        pngs = [(cid, curve(cid, ev, es)) for cid in card.curves]
        pngs = [(cid, p) for cid, p in pngs if p is not None]
        if pngs:
            parts.append(f"<h4>{SECTION_TITLES['curves'][0 if es else 1]}</h4>")
            for cid, png in pngs:
                assert png is not None
                out.images[f"c_{cid}"] = png
                parts.append(f'<p><img src="img:c_{cid}"></p>')
    pool = out.images if images else None
    current = _example_rows(card, ev, qfmt, es, pool, "ex")
    ref = _example_rows(card, reference, qfmt, es, pool, "rx")
    if current or ref:
        parts.append(f"<h4>{SECTION_TITLES['example'][0 if es else 1]}</h4>")
        if current:
            head = (f"Con los datos del tag {tag}" if es else f"With the data of tag {tag}")
            parts.append(f"<p><i>{html.escape(head.strip())}:</i></p><ul>{''.join(current)}</ul>")
        if ref:
            head = ("Caso de referencia (plantilla del programa: agua a 80 °C, 2 m/s, 316 cónico "
                    "bridado 1½\" 300#, L = 150 mm)" if es else
                    "Reference case (program template: water at 80 °C, 2 m/s, tapered 316 "
                    "flanged 1½\" 300#, L = 150 mm)")
            parts.append(f"<p><i>{html.escape(head)}:</i></p><ul>{''.join(ref)}</ul>")
    out.html = "".join(parts)
    return out


def search_text(card: Card) -> str:
    """Texto en ambos idiomas para la búsqueda Ctrl+K."""
    chunks = [card.id, *card.title]
    for sec in SECTIONS:
        chunks += list(getattr(card, sec))
    return " ".join(chunks).lower()
