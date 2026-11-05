"""Cada clave de mensaje que usa el motor existe en español y en inglés."""

from __future__ import annotations

import re
from pathlib import Path

from thermowell_sizer.i18n.catalog import CATALOG

SRC = Path(__file__).resolve().parents[1] / "src" / "thermowell_sizer" / "core"
KEY = re.compile(r'"((?:check|note|opt\.reason|trace|validation)\.[a-z_.]+)"')


def test_all_engine_keys_translated() -> None:
    keys = {m for f in SRC.rglob("*.py") for m in KEY.findall(f.read_text(encoding="utf-8"))}
    assert len(keys) > 50
    for lang in ("es", "en"):
        missing = sorted(keys - CATALOG[lang].keys())
        assert not missing, (lang, missing)
