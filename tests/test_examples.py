"""Los ejemplos de ``examples/`` abren y dan el resultado que indica el manual."""

from __future__ import annotations

from pathlib import Path

import pytest

from thermowell_sizer.data.database import Library
from thermowell_sizer.project import load_project
from thermowell_sizer.services import evaluate

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


@pytest.mark.parametrize(("name", "status"), [
    ("ejemplo_1_agua.tws", "pass"),
    ("ejemplo_2_vapor.tws", "pass"),
    ("ejemplo_3_gas_no_cumple.tws", "fail"),
])
def test_example_result(name: str, status: str) -> None:
    project = load_project(EXAMPLES / name)
    ev = evaluate(project.tags[0], Library(), project.settings)
    assert not ev.errors
    assert ev.status == status
