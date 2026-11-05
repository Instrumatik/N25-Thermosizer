import json
from pathlib import Path

import pytest

from thermowell_sizer.core.models import CalcInput
from thermowell_sizer.i18n import Language, format_number, parse_number, tr
from thermowell_sizer.project import (
    Project,
    ProjectFileError,
    ProjectInfo,
    TagRecord,
    load_project,
    save_project,
)


def test_project_round_trip(tmp_path: Path, calc_input: CalcInput) -> None:
    project = Project(info=ProjectInfo(name="Demo"), tags=(TagRecord(input=calc_input),))
    path = tmp_path / "demo.tws"
    save_project(project, path)
    assert load_project(path) == project
    assert not list(tmp_path.glob(".tws-*"))


@pytest.mark.parametrize(
    "content", ["no es json", json.dumps({"schema_version": 99}), json.dumps({"x": 1}),
                json.dumps({"schema_version": 1, "info": {}})]
)
def test_bad_files(tmp_path: Path, content: str) -> None:
    path = tmp_path / "bad.tws"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ProjectFileError):
        load_project(path)


def test_number_format_and_parse() -> None:
    assert format_number(1234.5, 1, Language.ES, grouping=True) == "1.234,5"
    assert format_number(1234.5, 1, Language.EN, grouping=True) == "1,234.5"
    assert parse_number("1.234,5", Language.ES) == 1234.5
    assert parse_number("12.5", Language.ES) == 12.5
    assert parse_number("1,234.5", Language.EN) == 1234.5


def test_translation_fallbacks() -> None:
    assert "rango" in tr("validation.out_of_range", Language.ES, value=1, min=0, max=2)
    assert tr("validation.tip_too_thin", Language.EN).startswith("Tip")
    assert tr("clave.inexistente", Language.EN) == "clave.inexistente"
