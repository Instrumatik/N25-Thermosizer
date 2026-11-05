"""Exportación a Excel: resultados por tag, resumen del proyecto y lista de materiales."""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from thermowell_sizer.core.models import CheckStatus
from thermowell_sizer.core.units import QuantityKind
from thermowell_sizer.reports.common import Fmt, TagReport, short_ref
from thermowell_sizer.reports.datasheet import calc_rows, enum_name, sections

HEADER_FILL = PatternFill("solid", fgColor="1F4E8C")
HEADER_FONT = Font(bold=True, color="FFFFFF")
STATUS_FILL = {CheckStatus.PASS: "C6EFCE", CheckStatus.WARNING: "FFEB9C",
               CheckStatus.FAIL: "FFC7CE", CheckStatus.NOT_APPLICABLE: "EDEDED"}
MAX_COL_WIDTH = 60
SHEET_NAME_MAX = 31


def _header(ws: Worksheet, row: int, values: list[str]) -> None:
    for col, v in enumerate(values, 1):
        cell = ws.cell(row=row, column=col, value=v)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(vertical="center", wrap_text=True)


def _autofit(ws: Worksheet) -> None:
    for col in ws.columns:
        length = max((len(str(c.value)) for c in col if c.value is not None), default=8)
        ws.column_dimensions[get_column_letter(col[0].column)].width = min(length + 2,
                                                                           MAX_COL_WIDTH)


def _status_cell(ws: Worksheet, row: int, col: int, status: CheckStatus | None, f: Fmt) -> None:
    cell = ws.cell(row=row, column=col, value=f.status(status))
    if status is not None:
        cell.fill = PatternFill("solid", fgColor=STATUS_FILL[status])
        cell.font = Font(bold=True)


def _disclaimer(ws: Worksheet, f: Fmt) -> None:
    row = ws.max_row + 2
    ws.cell(row=row, column=1, value=f.disclaimer).font = Font(bold=True, color="8A4B00")
    ws.cell(row=row + 1, column=1, value=f.footer()).font = Font(italic=True, size=8)


def _tag_sheet(wb: Workbook, rep: TagReport) -> None:
    f = rep.fmt
    ws = wb.create_sheet(rep.tag[:SHEET_NAME_MAX])
    ws.append([f.t("ds.title"), rep.tag])
    ws["A1"].font = Font(bold=True, size=13)
    _status_cell(ws, 1, 3, rep.evaluation.status, f)
    for title, rows in sections(rep):
        ws.append([])
        _header(ws, ws.max_row + 1, [title, ""])
        for k, v in rows:
            ws.append([k, v])
    res = rep.evaluation.result
    if res is not None:
        ws.append([])
        _header(ws, ws.max_row + 1, [f.t("sec.calc"), ""])
        for k, v in calc_rows(rep):
            ws.append([k, v])
        ws.append([])
        start = ws.max_row + 1
        _header(ws, start, [f.t("criterion"), f.t("case"), f.t("value") + " (SI)",
                            f.t("limit") + " (SI)", f.t("margin") + " %", f.t("status"),
                            f.t("reference")])
        for c in res.checks:
            r = ws.max_row + 1
            ws.cell(row=r, column=1, value=f.criterion(c.criterion_id))
            ws.cell(row=r, column=2, value=f.scope(c.flow_case))
            ws.cell(row=r, column=3, value=c.value)
            ws.cell(row=r, column=4, value=c.limit)
            ws.cell(row=r, column=5, value=round(c.margin_pct, 2))
            _status_cell(ws, r, 6, c.status, f)
            ws.cell(row=r, column=7, value=short_ref(c.reference))
        ws.append([])
        _header(ws, ws.max_row + 1, [f.t("case"), f.t("symbol"), f.t("description"),
                                     f.t("value") + " (SI)", f.t("value"), f.t("reference")])
        for e in res.trace:
            ws.append([f.scope(e.scope) if e.scope else f.t("m.common"), e.symbol,
                       f.t(e.description_key), e.value, f.q(e.value, e.kind),
                       short_ref(e.reference)])
    _disclaimer(ws, f)
    _autofit(ws)


def summary_rows(reps: list[TagReport]) -> tuple[list[str], list[list[object]]]:
    """Filas del resumen de proyecto (también para el PDF)."""
    f = reps[0].fmt
    head = [f.t("tag"), f.t("service"), f.t("material"), f.t("connection"), "L", "A", "B",
            "f_s/f_n,c", f.t("dyn"), f.t("status")]
    rows: list[list[object]] = []
    for rep in reps:
        inp = rep.evaluation.input
        g = inp.thermowell.geometry
        res = rep.evaluation.result
        ratio = max((c.fs / c.fnc for c in res.cases if c.fnc), default=None) if res else None
        dyn = res.worst("dynamic_stress_support") if res else None
        conn = inp.thermowell.connection
        rows.append([rep.tag, inp.identification.service, inp.thermowell.material.material_id,
                     f"{enum_name(rep, conn.type.value)} {conn.size} "
                     f"{conn.rating_class or ''}".strip(),
                     f.q(g.L, QuantityKind.LENGTH), f.q(g.A, QuantityKind.DIAMETER),
                     f.q(g.B, QuantityKind.DIAMETER), f.num(ratio, 3) if ratio else "—",
                     f"{f.num(dyn.margin_pct, 1)} %" if dyn else "—", rep.evaluation.status])
    return head, rows


def bom_rows(reps: list[TagReport]) -> tuple[list[str], list[list[object]]]:
    """Lista de materiales: termopozos agrupados por especificación idéntica."""
    f = reps[0].fmt
    groups: dict[tuple[str, ...], list[str]] = {}
    for rep in reps:
        inp = rep.evaluation.input
        g = inp.thermowell.geometry
        conn = inp.thermowell.connection
        try:
            mat = rep.library.material(inp.thermowell.material.material_id).spec
        except KeyError:
            mat = inp.thermowell.material.material_id
        desc = (f"{f.t('sec.thermowell').capitalize()} {enum_name(rep, g.profile.value)}, "
                f"{f.t('bar_stock')}, {enum_name(rep, conn.type.value)} {conn.size} "
                f"{conn.rating_class or ''} "
                f"{conn.face.value if conn.face else ''}".strip())
        dims = (f"U={f.q(g.U or g.L, QuantityKind.LENGTH)}, A={f.q(g.A, QuantityKind.DIAMETER)}, "
                f"B={f.q(g.B, QuantityKind.DIAMETER)}, d={f.q(g.d, QuantityKind.DIAMETER)}")
        key = (desc, mat, dims, inp.thermowell.material.coating or "—")
        groups.setdefault(key, []).append(rep.tag)
    head = [f.t("item"), f.t("qty"), f.t("description"), f.t("material"), "Dim.",
            f.t("coating"), f.t("tag")]
    rows = [[i, len(tags), *key[:3], key[3], ", ".join(tags)]
            for i, (key, tags) in enumerate(groups.items(), 1)]
    return head, rows


def build_excel(reps: list[TagReport], path: Path, *, bom_only: bool = False) -> Path:
    """Libro con resumen, lista de materiales y una hoja por tag."""
    wb = Workbook()
    f = reps[0].fmt
    ws = wb.active
    assert ws is not None
    if not bom_only:
        ws.title = "Resumen" if f.lang.value == "es" else "Summary"
        ws.append([f.t("summary.title"), reps[0].project.info.name])
        ws["A1"].font = Font(bold=True, size=13)
        head, rows = summary_rows(reps)
        _header(ws, 3, head)
        for r in rows:
            status = r[-1]
            ws.append([*r[:-1], ""])
            _status_cell(ws, ws.max_row, len(head), status if isinstance(status, CheckStatus)
                         else None, f)
        _disclaimer(ws, f)
        _autofit(ws)
        bom = wb.create_sheet("BOM")
    else:
        bom = ws
        bom.title = "BOM"
    bom.append([f.t("bom.title"), reps[0].project.info.name])
    bom["A1"].font = Font(bold=True, size=13)
    head, rows = bom_rows(reps)
    _header(bom, 3, head)
    for r in rows:
        bom.append(r)
    _disclaimer(bom, f)
    _autofit(bom)
    if not bom_only:
        for rep in reps:
            _tag_sheet(wb, rep)
    wb.save(path)
    return path
