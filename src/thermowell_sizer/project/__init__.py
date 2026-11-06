"""Proyecto: datos generales, lista de tags, revisiones y archivo ``.tws``.

Un proyecto se guarda como un único archivo JSON con extensión ``.tws``. Lleva un
número de versión de esquema para poder migrar archivos viejos cuando el modelo cambie.
Los valores se guardan en SI; las unidades de presentación son solo una preferencia.
"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import date
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from thermowell_sizer.core.models import CalcInput, CheckStatus, EngineOptions
from thermowell_sizer.core.units import STANDARD_ATMOSPHERE_PA, UnitSystem
from thermowell_sizer.i18n import Language

SCHEMA_VERSION = 1
FILE_EXTENSION = ".tws"


class _Model(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class Revision(_Model):
    """Entrada del control de revisiones."""

    rev: str
    date: date
    description: str
    prepared_by: str = ""
    checked_by: str = ""
    approved_by: str = ""


class ProjectInfo(_Model):
    """Datos del encabezado de los reportes."""

    name: str
    client: str = ""
    plant: str = ""
    document_number: str = ""
    revisions: tuple[Revision, ...] = ()


class ProjectSettings(_Model):
    """Preferencias de presentación del proyecto."""

    unit_system: UnitSystem = UnitSystem.SI
    language: Language = Language.ES
    barometric_pressure: float = Field(default=STANDARD_ATMOSPHERE_PA, gt=0.0, description="Pa")
    pressure_as_gauge: bool = True


class TagRecord(_Model):
    """Un punto de medición del proyecto con el estado de su último cálculo."""

    input: CalcInput
    options: EngineOptions = EngineOptions()
    auto_properties: bool = Field(
        default=True, description="Recalcular ρ y μ con CoolProp al cambiar P o T"
    )
    auto_blocks: tuple[str, ...] = Field(
        default=(), description="Bloques en modo automático: material, connection, geometry, "
                                "sensor")
    last_status: CheckStatus | None = None
    notes: str = ""


class Project(_Model):
    """Proyecto completo, tal como se guarda en el archivo ``.tws``."""

    schema_version: int = SCHEMA_VERSION
    info: ProjectInfo
    settings: ProjectSettings = ProjectSettings()
    tags: tuple[TagRecord, ...] = ()


class ProjectFileError(Exception):
    """El archivo no es un proyecto válido o es de una versión no soportada."""


def save_project(project: Project, path: Path) -> None:
    """Guarda el proyecto de forma atómica (archivo temporal + reemplazo).

    Así un corte de energía durante el autoguardado no deja un archivo corrupto.
    """
    data = project.model_dump_json(indent=2)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tws-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(data)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def load_project(path: Path) -> Project:
    """Carga y valida un archivo ``.tws``.

    Raises:
        ProjectFileError: si el archivo es ilegible, inválido o de una versión futura.

    """
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProjectFileError(f"No se pudo leer el proyecto: {exc}") from exc
    version = raw.get("schema_version") if isinstance(raw, dict) else None
    if not isinstance(version, int) or version > SCHEMA_VERSION:
        raise ProjectFileError(f"Versión de archivo no soportada: {version!r}")
    try:
        return Project.model_validate(raw)
    except ValueError as exc:
        raise ProjectFileError(f"Proyecto inválido: {exc}") from exc
