"""Reportes: hoja de datos, memoria, Excel, Word y resumen de proyecto."""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("reportlab")

from openpyxl import load_workbook

from thermowell_sizer.core.units import UnitSystem
from thermowell_sizer.data.database import Library
from thermowell_sizer.i18n import Language
from thermowell_sizer.project import Project, ProjectInfo, TagRecord
from thermowell_sizer.reports.common import Fmt, tag_report
from thermowell_sizer.reports.datasheet import build_datasheet
from thermowell_sizer.reports.excel import build_excel
from thermowell_sizer.reports.mathrender import plain, render_png
from thermowell_sizer.reports.memo import build_memo
from thermowell_sizer.reports.summary import build_summary
from thermowell_sizer.reports.word import build_word
from thermowell_sizer.services import default_input

DISCLAIMER_FRAGMENT = b"ingeniero"


@pytest.fixture(scope="module")
def lib() -> Library:
    return Library()


@pytest.fixture(scope="module")
def project() -> Project:
    a = default_input("TW-101")
    b = default_input("TW-102")
    g = b.thermowell.geometry.model_copy(update={"L": 0.6, "U": 0.6})
    case = b.process.flow_cases[0].model_copy(update={"velocity": 6.0})
    b = b.model_copy(update={
        "thermowell": b.thermowell.model_copy(update={"geometry": g}),
        "process": b.process.model_copy(update={"flow_cases": (case,)})})
    return Project(info=ProjectInfo(name="Prueba", document_number="DOC-1"),
                   tags=(TagRecord(input=a), TagRecord(input=b), TagRecord(input=a)))


def _pdf_ok(path: Path) -> None:
    data = path.read_bytes()
    assert data.startswith(b"%PDF") and len(data) > 5000


def test_datasheet_and_memo(tmp_path: Path, project: Project, lib: Library) -> None:
    rep = tag_report(project, 0, lib)
    _pdf_ok(build_datasheet(rep, tmp_path / "ds.pdf"))
    _pdf_ok(build_memo(rep, tmp_path / "memo.pdf"))
    failing = tag_report(project, 1, lib, Fmt(Language.EN, UnitSystem.IMPERIAL))
    _pdf_ok(build_memo(failing, tmp_path / "memo_en.pdf"))
    _pdf_ok(build_datasheet(failing, tmp_path / "ds_en.pdf"))


def test_excel_and_bom(tmp_path: Path, project: Project, lib: Library) -> None:
    reps = [tag_report(project, i, lib) for i in range(len(project.tags))]
    path = build_excel(reps, tmp_path / "r.xlsx")
    wb = load_workbook(path)
    assert wb.sheetnames[:2] == ["Resumen", "BOM"]
    assert "TW-101" in wb.sheetnames
    bom = wb["BOM"]
    quantities = [row[1] for row in bom.iter_rows(min_row=4, max_col=2, values_only=True)
                  if isinstance(row[1], int)]
    assert sorted(quantities) == [1, 2]
    only = load_workbook(build_excel(reps, tmp_path / "b.xlsx", bom_only=True))
    assert only.sheetnames == ["BOM"]


def test_word_and_summary(tmp_path: Path, project: Project, lib: Library) -> None:
    reps = [tag_report(project, i, lib) for i in range(len(project.tags))]
    assert build_word(reps[0], tmp_path / "m.docx").stat().st_size > 10_000
    _pdf_ok(build_summary(reps, tmp_path / "s.pdf"))


def test_fmt() -> None:
    f = Fmt()
    assert f.num(1234.5678) == "1234,6"
    assert f.num(1.2e-8) == "1,2000e-08"
    assert f.num(None) == "—"
    assert f.num(float("inf")) == "∞"
    assert Fmt(Language.EN).num(0.5) == "0.5"
    assert f.scope("max|root_corrosion") == "Máx. · corr. raíz"
    assert f.scope("") == "—"


def test_math_render() -> None:
    assert render_png(r"f_s = N_S V / B") is not None
    assert render_png(r"\badcommand{") is None
    assert "ρ" in plain(r"\rho V \text{o} x")
