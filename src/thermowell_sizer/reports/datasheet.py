"""Hoja de datos del termopozo en PDF A4 (formato tipo ISA-TR20)."""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable

from thermowell_sizer.core.analysis.sensitivity import max_allowable_velocity
from thermowell_sizer.core.models import CheckStatus, ConnectionType
from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.reports.common import STATUS_RGB, TagReport
from thermowell_sizer.reports.drawing import thermowell_drawing
from thermowell_sizer.reports.pdfbase import (
    FONT,
    FONT_BOLD,
    FOOTER_H,
    HEADER_H,
    LINE,
    MARGIN,
    PAGE_H,
    PAGE_W,
    SHADE,
    STYLES,
    NumberedCanvas,
    footer,
    title_block,
)

LEFT_W = 112 * mm
RIGHT_W = PAGE_W - 2 * MARGIN - LEFT_W - 3 * mm
Row = tuple[str, str]


def enum_name(rep: TagReport, value: str) -> str:
    """Nombre traducido de un valor de enumeración."""
    return _enum(rep, value)


def _enum(rep: TagReport, value: str) -> str:
    from thermowell_sizer.ui.text import ENUM_TEXT

    pair = ENUM_TEXT.get(value, (value, value))
    return pair[0] if rep.fmt.lang.value == "es" else pair[1]


def sections(rep: TagReport) -> list[tuple[str, list[Row]]]:
    """Secciones de datos de la hoja (también se usan en Excel y Word)."""
    f = rep.fmt
    inp = rep.evaluation.input
    idn, proc, pipe = inp.identification, inp.process, inp.pipe
    tw, g, sensor = inp.thermowell, inp.thermowell.geometry, inp.sensor
    try:
        fluid = rep.library.fluid(proc.fluid_id)
        fluid_name = fluid.name_es if f.lang.value == "es" else fluid.name_en
    except KeyError:
        fluid_name = proc.fluid_id
    try:
        mat = rep.library.material(tw.material.material_id)
        mat_name = f"{mat.name} ({mat.spec})"
    except KeyError:
        mat_name = tw.material.material_id
    coating = "—"
    for c in rep.library.coatings():
        if c[0] == tw.material.coating:
            coating = c[1] if f.lang.value == "es" else c[2]
    conn = tw.connection
    rating = (f"{conn.rating_class} / {conn.face.value if conn.face else '—'}"
              if conn.type in (ConnectionType.FLANGED, ConnectionType.VAN_STONE) else "—")
    cases = "; ".join(
        f"{f.scope(c.label)}: " + (f.q(c.velocity, QuantityKind.VELOCITY) if c.velocity is not None
                                  and c.basis.value == "velocity" else
                                  f.q(c.mass_flow, QuantityKind.MASS_FLOW)
                                  if c.basis.value == "mass_flow" else
                                  f.q(c.volume_flow, QuantityKind.VOLUME_FLOW))
        for c in proc.flow_cases)
    return [
        (f.t("sec.general"), [
            (f.t("tag"), idn.tag), (f.t("service"), idn.service or "—"),
            (f.t("line"), idn.line_or_equipment or "—"), (f.t("pid"), idn.pid or "—"),
            (f.t("location"), idn.location or "—"),
        ]),
        (f.t("sec.process"), [
            (f.t("fluid"), fluid_name), (f.t("phase"), _enum(rep, proc.phase.value)),
            (f.t("p_op"), f.pressure(proc.operating_pressure)),
            (f.t("p_design"), f.pressure(proc.design_pressure)),
            (f.t("t_op"), f.q(proc.operating_temperature, QuantityKind.TEMPERATURE)),
            (f.t("t_design"), f.q(proc.design_temperature, QuantityKind.TEMPERATURE)),
            (f.t("density"), f.q(proc.properties.density, QuantityKind.DENSITY)),
            (f.t("viscosity"), f.q(proc.properties.dynamic_viscosity,
                                   QuantityKind.DYNAMIC_VISCOSITY)),
            (f.t("case"), cases),
        ]),
        (f.t("sec.pipe"), [
            (f.t("pipe_size"), f"NPS {pipe.nominal_size} / Sch {pipe.schedule}"
             if pipe.nominal_size else "—"),
            (f.t("pipe_id"), f.q(pipe.inner_diameter, QuantityKind.DIAMETER)),
            (f.t("orientation"), _enum(rep, pipe.orientation.value)),
            (f.t("nozzle"), f.q(pipe.nozzle_length, QuantityKind.LENGTH)),
        ]),
        (f.t("sec.thermowell"), [
            (f.t("construction"), f.t("bar_stock")),
            (f.t("profile"), _enum(rep, g.profile.value)),
            (f.t("material"), mat_name), (f.t("coating"), coating),
            (f.t("connection"), f"{_enum(rep, conn.type.value)} {conn.size}".strip()),
            (f.t("rating"), rating),
            (f.t("U"), f.q(g.U, QuantityKind.LENGTH)),
            (f.t("L"), f.q(g.L, QuantityKind.LENGTH)),
            (f.t("A"), f.q(g.A, QuantityKind.DIAMETER)),
            (f.t("B"), f.q(g.B, QuantityKind.DIAMETER)),
            (f.t("d"), f.q(g.d, QuantityKind.DIAMETER)),
            (f.t("t"), f.q(g.t, QuantityKind.LENGTH)),
            (f.t("b"), f.q(g.b, QuantityKind.LENGTH)),
            (f.t("lag"), f.q(g.T_lag, QuantityKind.LENGTH)),
            (f.t("ca"), f.q(g.corrosion_allowance, QuantityKind.LENGTH)),
        ]),
        (f.t("sec.sensor"), [
            (f.t("sensor_type"), _enum(rep, sensor.type.value)),
            (f.t("sheath"), f.q(sensor.sheath_diameter, QuantityKind.DIAMETER)),
        ]),
    ]


def calc_rows(rep: TagReport) -> list[Row]:
    """Resultados principales para la hoja de datos."""
    f = rep.fmt
    ev = rep.evaluation
    res = ev.result
    if res is None:
        return []
    worst_case = max(res.cases, key=lambda c: c.fs / c.fnc if c.fnc else 0.0)
    ratio_lim = (f" ({f.num(worst_case.frequency_ratio_limit, 2)})"
                 if worst_case.frequency_ratio_limit else "")
    rows: list[Row] = [
        (f.t("fs"), f.q(worst_case.fs, QuantityKind.FREQUENCY)),
        (f.t("fnc"), f.q(worst_case.fnc, QuantityKind.FREQUENCY)),
        (f.t("ratio"), f.num(worst_case.fs / worst_case.fnc, 3) + ratio_lim
         if worst_case.fnc else "—"),
        (f.t("scruton"), f.num(worst_case.scruton, 2)),
    ]
    for cid, key in (("dynamic_stress_support", "dyn"), ("steady_stress_support", "steady")):
        c = res.worst(cid)
        if c is not None:
            rows.append((f.t(key), f"{f.q(c.value, QuantityKind.STRESS)} / "
                                   f"{f.q(c.limit, QuantityKind.STRESS)}"))
    pr = res.worst("pressure_rating")
    if pr is not None:
        rows.append((f.t("pr"), f"{f.pressure(pr.value + f.barometric)} / "
                                f"{f.pressure(pr.limit + f.barometric)}"))
    if ev.material is not None:
        vmax = max_allowable_velocity(ev.input, ev.material, ev.options, samples=120)
        rows.append((f.t("vmax"), f.q(vmax, QuantityKind.VELOCITY) if vmax else "> 200 m/s"))
    if ev.thermal is not None:
        rows.append((f.t("tau"), f"{f.num(ev.thermal.tau, 0)} s / {f.num(ev.thermal.t90, 0)} s"))
    return rows


def _kv_table(sections_: list[tuple[str, list[Row]]], width: float, start: int = 1,
              label_ratio: float = 0.42) -> Table:
    data: list[list[object]] = []
    style: list[tuple[object, ...]] = [
        ("FONT", (0, 0), (-1, -1), FONT, 7.2),
        ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2),
    ]
    n = start
    for title, rows in sections_:
        style += [("SPAN", (0, len(data)), (-1, len(data))),
                  ("BACKGROUND", (0, len(data)), (-1, len(data)), SHADE),
                  ("FONT", (0, len(data)), (-1, len(data)), FONT_BOLD, 7.4)]
        data.append([title, "", ""])
        for label, value in rows:
            data.append([str(n), Paragraph(escape(label), STYLES["cell"]),
                         Paragraph(escape(value), STYLES["cell"])])
            n += 1
    label_w = (width - 7 * mm) * label_ratio
    return Table(data, colWidths=[7 * mm, label_w, width - 7 * mm - label_w],
                 style=TableStyle(style))


class _StatusBox(Flowable):
    """Recuadro de color con el resultado global."""

    def __init__(self, text: str, status: CheckStatus | None, width: float) -> None:
        super().__init__()
        self.text = text
        self.status = status
        self.width = width
        self.height = 11 * mm

    def draw(self) -> None:
        rgb = STATUS_RGB.get(self.status, (0.5, 0.5, 0.5)) if self.status else (0.5, 0.5, 0.5)
        self.canv.setFillColorRGB(*rgb)
        self.canv.roundRect(0, 0, self.width, self.height, 3, stroke=0, fill=1)
        self.canv.setFillColor(colors.white)
        self.canv.setFont(FONT_BOLD, 13)
        self.canv.drawCentredString(self.width / 2, self.height / 2 - 4.5, self.text)


def signature_table(rep: TagReport, width: float) -> Table:
    """Tabla de revisiones y firmas."""
    f = rep.fmt
    head = [f.t("rev"), f.t("date"), f.t("description"), f.t("prepared"), f.t("checked"),
            f.t("approved")]
    revs = rep.project.info.revisions[-3:]
    rows = [[r.rev, r.date.isoformat(), r.description, r.prepared_by, r.checked_by,
             r.approved_by] for r in revs] or [["0", "", "", "", "", ""]]
    widths = [10 * mm, 20 * mm, width - 10 * mm - 20 * mm - 3 * 30 * mm, 30 * mm, 30 * mm, 30 * mm]
    return Table([head, *rows], colWidths=widths, rowHeights=[5 * mm] + [7 * mm] * len(rows),
                 style=TableStyle([("FONT", (0, 0), (-1, -1), FONT, 7),
                                   ("FONT", (0, 0), (-1, 0), FONT_BOLD, 7),
                                   ("BACKGROUND", (0, 0), (-1, 0), SHADE),
                                   ("GRID", (0, 0), (-1, -1), 0.3, LINE),
                                   ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))


def build_datasheet(rep: TagReport, path: Path) -> Path:
    """Genera la hoja de datos y devuelve la ruta."""
    f = rep.fmt
    doc = SimpleDocTemplate(str(path), pagesize=(PAGE_W, PAGE_H), leftMargin=MARGIN,
                            rightMargin=MARGIN, topMargin=MARGIN + HEADER_H + 3 * mm,
                            bottomMargin=MARGIN + FOOTER_H, title=f"{f.t('ds.title')} {rep.tag}",
                            author="InstruMatik · ThermoWell Sizer")
    left = _kv_table(sections(rep), LEFT_W)
    inp = rep.evaluation.input
    drawing = thermowell_drawing(inp.thermowell.geometry, inp.thermowell.connection.type, f,
                                 RIGHT_W, 58 * mm)
    calc = _kv_table([(f.t("sec.calc"), calc_rows(rep))], RIGHT_W, start=100, label_ratio=0.55)
    status = rep.evaluation.status
    right = Table([[drawing], [Spacer(1, 2 * mm)], [calc], [Spacer(1, 3 * mm)],
                   [_StatusBox(f"{f.t('result')}: {f.status(status)}", status, RIGHT_W)]],
                  colWidths=[RIGHT_W], style=TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0),
                                                         ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                                         ("BOX", (0, 0), (0, 0), 0.3, LINE)]))
    body = Table([[left, right]], colWidths=[LEFT_W + 3 * mm, RIGHT_W],
                 style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    notes = [f.t(w) for w in rep.evaluation.warnings]
    if rep.evaluation.result is not None:
        notes += [f.t(n) for n in rep.evaluation.result.notes]
    if rep.record.notes:
        notes.append(rep.record.notes)
    story: list[Flowable] = [body, Spacer(1, 3 * mm),
                             Paragraph(f"<b>{f.t('sec.notes')}</b>", STYLES["body"])]
    story += [Paragraph(f"{i}. {n}", STYLES["small"]) for i, n in enumerate(notes, 1)] or [
        Paragraph("—", STYLES["small"])]
    story += [Spacer(1, 3 * mm), signature_table(rep, PAGE_W - 2 * MARGIN)]

    def decorate(c: NumberedCanvas, page: int, total: int) -> None:
        title_block(c, rep.project, f, f.t("ds.title"), f"{rep.tag} — "
                    f"{inp.identification.service}".strip(" —"), page, total)
        footer(c, f)

    doc.build(story, canvasmaker=lambda *a, **k: NumberedCanvas(*a, decorate=decorate, **k))
    return path
