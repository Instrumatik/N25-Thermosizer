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


def rich_text(text: str) -> str:
    """Texto de ficha a HTML: párrafos separados por línea en blanco y listas.

    Las líneas que empiezan con «- » forman una lista con viñetas y las que empiezan con
    «1. », «2. »… una lista numerada.
    """
    out: list[str] = []
    for block in text.split("\n\n"):
        lines = [ln.strip() for ln in block.strip().splitlines() if ln.strip()]
        if not lines:
            continue
        if all(ln.startswith("- ") for ln in lines):
            items = "".join(f"<li>{html.escape(ln[2:])}</li>" for ln in lines)
            out.append(f"<ul>{items}</ul>")
        elif all(ln.split(" ", 1)[0].rstrip(".").isdigit() and ln.split(" ", 1)[0].endswith(".")
                 for ln in lines):
            items = "".join(f"<li>{html.escape(ln.split(' ', 1)[1])}</li>" for ln in lines)
            out.append(f"<ol>{items}</ol>")
        else:
            out.append(f"<p>{html.escape(' '.join(lines))}</p>")
    return "".join(out)


def _table_html(card: Card, es: bool) -> str:
    """Tabla de guía con la fila de la ficha resaltada."""
    lang = 0 if es else 1
    head, *rows = card.table
    out = [f"<h4>{SECTION_TITLES['table'][lang]}</h4>",
           '<table border="1" cellspacing="0" cellpadding="4" width="100%"><tr>']
    out += [f"<th>{html.escape(c[lang])}</th>" for c in head]
    out.append("</tr>")
    for i, row in enumerate(rows, start=1):
        style = ' style="background-color:#fff3c4"' if i == card.highlight else ""
        out.append(f"<tr{style}>")
        for j, c in enumerate(row):
            txt = html.escape(c[lang])
            out.append(f"<td><b>{txt}</b></td>" if j == 0 else f"<td>{txt}</td>")
        out.append("</tr>")
    out.append("</table>")
    if card.table_note[lang]:
        out.append(f"<p><i>{html.escape(card.table_note[lang])}</i></p>")
    return "".join(out)


def render_card(card: Card, ev: Evaluation | None, reference: Evaluation | None, *,
                es: bool, qfmt: QFmt, tag: str = "", images: bool = True) -> RenderedCard:
    """HTML de la ficha. ``ev`` es el tag actual; ``reference`` el caso de referencia."""
    out = RenderedCard("")
    lang = "es" if es else "en"
    parts = [f"<h2>{html.escape(card.title[0 if es else 1])}</h2>"]
    for sec in SECTIONS:
        text = card.text(sec, es)
        if text:
            parts.append(f"<h4>{SECTION_TITLES[sec][0 if es else 1]}</h4>{rich_text(text)}")
    if card.table:
        parts.append(_table_html(card, es))
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
    for row in card.table:
        for cell in row:
            chunks += list(cell)
    chunks += list(card.table_note)
    return " ".join(chunks).lower()
