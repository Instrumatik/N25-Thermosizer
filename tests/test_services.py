"""Servicios de aplicación: evaluación de tags e importación masiva."""

from __future__ import annotations

from pathlib import Path

import pytest

from thermowell_sizer.core.models import CheckStatus
from thermowell_sizer.data.database import Library
from thermowell_sizer.project import ProjectSettings, TagRecord
from thermowell_sizer.services import (
    default_input,
    evaluate,
    import_rows,
    read_table,
    template_csv,
)


@pytest.fixture(scope="module")
def lib() -> Library:
    return Library()


def test_evaluate_default(lib: Library) -> None:
    ev = evaluate(TagRecord(input=default_input()), lib, ProjectSettings())
    assert ev.status is CheckStatus.PASS
    assert ev.options.flange_rating == pytest.approx(lib.flange_rating("2.2", 300, 393.15))


def test_evaluate_unknown_material_and_fluid(lib: Library) -> None:
    inp = default_input()
    tw = inp.thermowell.model_copy(update={"material": inp.thermowell.material.model_copy(
        update={"material_id": "XX"})})
    proc = inp.process.model_copy(update={"fluid_id": "nope"})
    ev = evaluate(TagRecord(input=inp.model_copy(update={"thermowell": tw, "process": proc})),
                  lib, ProjectSettings())
    assert ev.status is None
    assert "svc.material_unknown" in ev.errors
    assert "svc.fluid_properties_failed" in ev.warnings


def test_flange_rating_unavailable(lib: Library) -> None:
    inp = default_input()
    tw = inp.thermowell.model_copy(update={"material": inp.thermowell.material.model_copy(
        update={"material_id": "N06625"})})
    ev = evaluate(TagRecord(input=inp.model_copy(update={"thermowell": tw})), lib,
                  ProjectSettings())
    assert "svc.flange_rating_unavailable" in ev.warnings


def test_import_csv(tmp_path: Path, lib: Library) -> None:
    path = tmp_path / "tags.csv"
    bad = "TW-X;x;water;6;10;35;60;2,5;6;999;SS316;200;27;19;6,6;300\n"
    path.write_text(template_csv() + bad, encoding="utf-8-sig")
    rows = read_table(path)
    records, errors = import_rows(rows, lib, 101_325.0)
    assert len(records) == 1 and len(errors) == 1
    rec = records[0]
    assert rec.input.identification.tag == "TW-101"
    assert rec.input.thermowell.geometry.L == pytest.approx(0.2)
    assert evaluate(rec, lib, ProjectSettings()).status is not None


def test_import_excel(tmp_path: Path, lib: Library) -> None:
    openpyxl = pytest.importorskip("openpyxl")
    wb = openpyxl.Workbook()
    ws = wb.active
    lines = [line.split(";") for line in template_csv().strip().splitlines()]
    for line in lines:
        ws.append(line)
    path = tmp_path / "tags.xlsx"
    wb.save(path)
    records, errors = import_rows(read_table(path), lib, 101_325.0)
    assert len(records) == 1 and not errors
