"""Diseños típicos de termopozos y perfiles de especificación de cliente.

El catálogo genérico recoge las ejecuciones habituales de la industria (series de
agujero 0,260" y 0,385", punta de 1/4", largos de inserción U normalizados en
pulgadas). Son valores **típicos**: cada fabricante tiene sus propias tablas y las
cotas finales deben confirmarse con el plano del proveedor.

Un *perfil de cliente* es un archivo JSON con los modelos normalizados de una
especificación de empresa (por ejemplo, modelos por longitud de inserción y una tabla
que elige el modelo según el NPS de la línea, el rating y el tipo de montaje). Los
perfiles los carga el usuario y no se distribuyen con el programa, porque las
especificaciones de empresa suelen ser documentos privados.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final

from pydantic import BaseModel, ConfigDict, Field

from thermowell_sizer.core.models import ConnectionType, ShankProfile

INCH: Final = 0.0254
BORE_260: Final = 0.260 * INCH
BORE_385: Final = 0.385 * INCH
TIP_THICKNESS: Final = 0.25 * INCH
STEP_LENGTH: Final = 2.5 * INCH
MIN_WALL: Final = 3.2e-3
"""Pared mínima que se respeta al adaptar un diseño a un agujero no tabulado, m."""
STANDARD_U: Final = tuple(x * INCH for x in (2.5, 4.5, 7.5, 10.5, 13.5, 16.5, 22.5))
"""Largos de inserción U normalizados más comunes (2½" a 22½")."""

PROFILE_DIR: Final = "perfiles"


@dataclass(frozen=True)
class TypicalDesign:
    """Ejecución típica: perfil, conexión y diámetros según el agujero."""

    id: str
    profile: ShankProfile
    connection: ConnectionType
    sizes: tuple[str, ...]
    # diámetros (A, B) por agujero d, m
    diameters: dict[float, tuple[float, float]]
    min_u: float = 0.0
    rating_required: bool = False


def _inch(a: float, b: float) -> tuple[float, float]:
    return a * INCH, b * INCH


TYPICAL_DESIGNS: Final[tuple[TypicalDesign, ...]] = (
    TypicalDesign("threaded_tapered", ShankProfile.TAPERED, ConnectionType.THREADED,
                  ("3/4 NPT", "1 NPT"),
                  {BORE_260: _inch(0.875, 0.625), BORE_385: _inch(0.875, 0.75)}),
    TypicalDesign("threaded_straight", ShankProfile.STRAIGHT, ConnectionType.THREADED,
                  ("1/2 NPT", "3/4 NPT", "1 NPT"),
                  {BORE_260: _inch(0.75, 0.75), BORE_385: _inch(0.875, 0.875)}),
    TypicalDesign("threaded_stepped", ShankProfile.STEPPED, ConnectionType.THREADED,
                  ("3/4 NPT", "1 NPT"),
                  {BORE_260: _inch(0.875, 0.5)}, min_u=4.5 * INCH),
    TypicalDesign("flanged_tapered", ShankProfile.TAPERED, ConnectionType.FLANGED,
                  ("1-1/2", "2"),
                  {BORE_260: _inch(1.0625, 0.75), BORE_385: _inch(1.25, 0.875)},
                  rating_required=True),
    TypicalDesign("flanged_straight", ShankProfile.STRAIGHT, ConnectionType.FLANGED,
                  ("1-1/2", "2"),
                  {BORE_260: _inch(1.0, 1.0), BORE_385: _inch(1.0, 1.0)},
                  rating_required=True),
    TypicalDesign("flanged_stepped", ShankProfile.STEPPED, ConnectionType.FLANGED,
                  ("1-1/2", "2"),
                  {BORE_260: _inch(1.0, 0.625)}, min_u=4.5 * INCH, rating_required=True),
    TypicalDesign("socket_tapered", ShankProfile.TAPERED, ConnectionType.SOCKET_WELD,
                  ("3/4", "1", "1-1/4", "1-1/2"),
                  {BORE_260: _inch(0.875, 0.625), BORE_385: _inch(1.0, 0.75)}),
    TypicalDesign("weld_in_tapered", ShankProfile.TAPERED, ConnectionType.WELD_IN,
                  ("1", "1-1/4", "1-1/2"),
                  {BORE_260: _inch(1.0625, 0.75), BORE_385: _inch(1.25, 0.875)}),
    TypicalDesign("van_stone_tapered", ShankProfile.TAPERED, ConnectionType.VAN_STONE,
                  ("1-1/2", "2"),
                  {BORE_260: _inch(1.0625, 0.75), BORE_385: _inch(1.25, 0.875)},
                  rating_required=True),
)

DESIGNS_BY_ID: Final = {d.id: d for d in TYPICAL_DESIGNS}

DESIGN_NAMES: Final[dict[str, tuple[str, str]]] = {
    "threaded_tapered": ("Roscada, vástago cónico", "Threaded, tapered shank"),
    "threaded_straight": ("Roscada, vástago recto", "Threaded, straight shank"),
    "threaded_stepped": ("Roscada, vástago escalonado", "Threaded, stepped shank"),
    "flanged_tapered": ("Bridada, vástago cónico", "Flanged, tapered shank"),
    "flanged_straight": ("Bridada, vástago recto", "Flanged, straight shank"),
    "flanged_stepped": ("Bridada, vástago escalonado", "Flanged, stepped shank"),
    "socket_tapered": ("Socket weld, vástago cónico", "Socket weld, tapered shank"),
    "weld_in_tapered": ("Para soldar (weld-in), cónico", "Weld-in, tapered"),
    "van_stone_tapered": ("Van Stone, vástago cónico", "Van Stone, tapered shank"),
}
"""Nombre de cada ejecución (es, en)."""



@dataclass(frozen=True)
class DesignChoice:
    """Resultado a aplicar en el editor: geometría y conexión."""

    profile: ShankProfile
    connection: ConnectionType
    size: str
    U: float
    L: float
    A: float
    B: float
    d: float
    t: float
    Ls: float = 0.0
    L0: float = 0.0
    rating_class: int | None = None
    model: str = ""
    notes: list[str] = field(default_factory=list)


def nozzle_projection(nozzle_length: float, U: float) -> float:
    """Tramo del vástago protegido dentro de la tobera (L0 < L)."""
    return min(max(nozzle_length, 0.0), 0.95 * U)


def recommended_u(pipe_id: float, nozzle_length: float = 0.0,
                  standard: tuple[float, ...] = STANDARD_U,
                  min_immersion: float = 0.1) -> float:
    """Largo U normalizado más corto que deja la punta bien inmersa en el flujo.

    Regla práctica de instalación: la punta debe entrar al menos 1/3 del diámetro
    interno y, si la línea lo permite, unos ``min_immersion`` (100 mm) para que el
    error por conducción sea chico, sin pasar de la mitad del diámetro por esa regla
    ni acercarse a la pared opuesta (0,9·D). Un largo menor reduce la carga dinámica,
    de modo que se elige el más corto que cumpla. Si ningún largo normalizado sirve,
    se devuelve el mínimo redondeado a 5 mm.
    """
    target = nozzle_length + max(pipe_id / 3.0, min(min_immersion, pipe_id / 2.0))
    limit = nozzle_length + 0.9 * pipe_id
    for u in standard:
        if target <= u <= limit:
            return u
    return math.ceil(target / 0.005) * 0.005


def build_choice(design: TypicalDesign, *, size: str, bore: float, U: float,
                 nozzle_length: float = 0.0, rating_class: int | None = None,
                 model: str = "") -> DesignChoice:
    """Arma la geometría de un diseño típico para el largo U y el agujero dados."""
    if bore in design.diameters:
        A, B = design.diameters[bore]
    else:  # agujero no tabulado: diámetros del agujero tabulado más cercano
        key = min(design.diameters, key=lambda k: abs(k - bore))
        A, B = design.diameters[key]
        A, B = max(A, bore + 2 * MIN_WALL), max(B, bore + 2 * MIN_WALL)
        if design.profile is ShankProfile.STRAIGHT:
            A = B = max(A, B)
    notes: list[str] = []
    Ls = 0.0
    if design.profile is ShankProfile.STEPPED:
        Ls = min(STEP_LENGTH, 0.6 * U)
    if design.min_u > U:
        notes.append("short_for_design")
    return DesignChoice(profile=design.profile, connection=design.connection, size=size,
                        U=U, L=U, A=A, B=B, d=bore, t=TIP_THICKNESS, Ls=Ls,
                        L0=nozzle_projection(nozzle_length, U),
                        rating_class=rating_class if design.rating_required else None,
                        model=model, notes=notes)


# --- Perfiles de especificación de cliente ------------------------------------------
class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class ProfileModel(_Frozen):
    """Modelo normalizado de una especificación (p. ej. 'H2': U = 320 mm)."""

    design: str = Field(description="id de TYPICAL_DESIGNS")
    U_mm: float = Field(gt=0)
    bore_mm: float | None = Field(default=None, gt=0)
    A_mm: float | None = Field(default=None, gt=0)
    B_mm: float | None = Field(default=None, gt=0)
    size: str = ""
    nozzle_mm: float | None = Field(default=None, ge=0)
    note: str = ""


class ProfileRule(_Frozen):
    """Fila de la tabla de aplicación: modelo por NPS para un montaje y rango de rating."""

    connection: ConnectionType
    mounting: str = Field(pattern="^(elbow|perpendicular)$")
    rating_min: int = 0
    rating_max: int = 99999
    by_nps: dict[str, str | None]


class NozzleRule(_Frozen):
    """Proyección de tobera típica para un rango de rating."""

    rating_max: int
    length_mm: float


class ClientProfile(_Frozen):
    """Perfil de especificación de cliente, leído de un JSON."""

    id: str
    name: str
    description: str = ""
    private: bool = True
    default_bore_mm: float | None = None
    max_nps: str | None = None
    models: dict[str, ProfileModel]
    rules: list[ProfileRule]
    nozzles: list[NozzleRule] = []
    notes: list[str] = []

    def nozzle_length(self, rating_class: int | None, model: str = "") -> float | None:
        """Proyección de tobera típica (m) del modelo o del rating, si el perfil la define."""
        m = self.models.get(model)
        if m is not None and m.nozzle_mm is not None:
            return m.nozzle_mm / 1000.0
        r = rating_class or 150
        for rule in sorted(self.nozzles, key=lambda n: n.rating_max):
            if r <= rule.rating_max:
                return rule.length_mm / 1000.0
        return None


def _nps_value(nps: str) -> float:
    """'1-1/2' → 1.5; texto no numérico → nan."""
    try:
        whole, _, frac = nps.strip().partition("-")
        if "/" in whole and not frac:
            whole, frac = "0", whole
        value = float(whole)
        if frac:
            num, den = frac.split("/")
            value += float(num) / float(den)
        return value
    except ValueError:
        return math.nan


@dataclass(frozen=True)
class ProfileSelection:
    """Modelo elegido por la tabla del perfil, o el motivo por el que no hay modelo."""

    model: str | None
    reason: str = ""
    nps_used: str = ""


def select_model(profile: ClientProfile, *, connection: ConnectionType, nps: str,
                 rating_class: int | None, elbow: bool) -> ProfileSelection:
    """Busca el modelo normalizado según el tipo de conexión, la línea y el montaje."""
    mounting = "elbow" if elbow else "perpendicular"
    rating = rating_class or 150
    rules = [r for r in profile.rules if r.connection is connection
             and r.mounting == mounting and r.rating_min <= rating <= r.rating_max]
    if not rules:
        return ProfileSelection(None, "no_rule")
    rule = rules[0]
    value = _nps_value(nps)
    if math.isnan(value):
        return ProfileSelection(None, "no_nps")
    sizes = sorted(rule.by_nps, key=_nps_value)
    if profile.max_nps and value > _nps_value(profile.max_nps):
        value = _nps_value(profile.max_nps)
    if value < _nps_value(sizes[0]):
        return ProfileSelection(None, "line_too_small", sizes[0])
    used = max((s for s in sizes if _nps_value(s) <= value), key=_nps_value)
    model = rule.by_nps[used]
    if model is None:
        return ProfileSelection(None, "not_allowed", used)
    return ProfileSelection(model, "", used)


def profile_choice(profile: ClientProfile, model_id: str, *, size: str = "",
                   nozzle_length: float = 0.0,
                   rating_class: int | None = None) -> DesignChoice:
    """Geometría del modelo ``model_id`` del perfil."""
    m = profile.models[model_id]
    design = DESIGNS_BY_ID[m.design]
    bore_mm = m.bore_mm or profile.default_bore_mm
    bore = bore_mm / 1000.0 if bore_mm else next(iter(design.diameters))
    choice = build_choice(design, size=m.size or size or design.sizes[0], bore=bore,
                          U=m.U_mm / 1000.0, nozzle_length=nozzle_length,
                          rating_class=rating_class, model=model_id)
    A = m.A_mm / 1000.0 if m.A_mm else choice.A
    B = m.B_mm / 1000.0 if m.B_mm else choice.B
    if design.profile is ShankProfile.STRAIGHT:
        B = A
    notes = list(choice.notes)
    if m.note:
        notes.append(m.note)
    return DesignChoice(**{**choice.__dict__, "A": A, "B": min(A, B), "notes": notes})


def load_profile(path: Path) -> ClientProfile:
    """Lee y valida un perfil JSON. Lanza ``ValueError`` si no es válido."""
    try:
        data: Any = json.loads(path.read_text(encoding="utf-8"))
        profile = ClientProfile.model_validate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"{path.name}: {exc}") from exc
    for key, m in profile.models.items():
        if m.design not in DESIGNS_BY_ID:
            raise ValueError(f"{path.name}: modelo {key}: diseño desconocido '{m.design}'")
    for rule in profile.rules:
        for model in rule.by_nps.values():
            if model is not None and model not in profile.models:
                raise ValueError(f"{path.name}: la tabla usa el modelo '{model}' "
                                 "que no está definido")
    return profile


def load_profiles(folder: Path | None) -> list[ClientProfile]:
    """Perfiles válidos de la carpeta del usuario (los inválidos se ignoran)."""
    if folder is None or not folder.is_dir():
        return []
    out: list[ClientProfile] = []
    for path in sorted(folder.glob("*.json")):
        try:
            out.append(load_profile(path))
        except ValueError:
            continue
    return out


# --- Tamaños de conexión ---------------------------------------------------------------
CONNECTION_SIZES: Final[dict[ConnectionType, tuple[str, ...]]] = {
    ConnectionType.THREADED: ("1/2 NPT", "3/4 NPT", "1 NPT", "1-1/4 NPT", "1-1/2 NPT"),
    ConnectionType.FLANGED: ("1", "1-1/2", "2", "3"),
    ConnectionType.VAN_STONE: ("1", "1-1/2", "2", "3"),
    ConnectionType.SOCKET_WELD: ("3/4", "1", "1-1/4", "1-1/2", "2"),
    ConnectionType.WELD_IN: ("3/4", "1", "1-1/4", "1-1/2", "2"),
    ConnectionType.SANITARY: ("1-1/2 clamp", "2 clamp", "3 clamp"),
}
"""Tamaños de conexión habituales por tipo."""

SUGGESTED_SIZE: Final[dict[ConnectionType, tuple[tuple[float, str], ...]]] = {
    # (NPS de línea desde, tamaño sugerido); se toma la última fila cuyo NPS es ≤ al de línea
    ConnectionType.THREADED: ((0.0, "3/4 NPT"), (3.0, "1 NPT")),
    ConnectionType.FLANGED: ((0.0, "1"), (3.0, "1-1/2"), (24.0, "2")),
    ConnectionType.VAN_STONE: ((0.0, "1"), (3.0, "1-1/2"), (24.0, "2")),
    ConnectionType.SOCKET_WELD: ((0.0, "3/4"), (3.0, "1")),
    ConnectionType.WELD_IN: ((0.0, "1"), (6.0, "1-1/2")),
    ConnectionType.SANITARY: ((0.0, "1-1/2 clamp"), (4.0, "2 clamp")),
}
"""Tamaño sugerido según el NPS de la línea (práctica habitual; editable por el usuario)."""

SIZE_TABLE_FILE: Final = "tamanos_conexion.json"


def suggested_connection_size(connection: ConnectionType, nps: str,
                              folder: Path | None = None) -> str | None:
    """Tamaño de conexión sugerido para la línea, o ``None`` si el NPS no es numérico.

    Si ``folder`` contiene ``tamanos_conexion.json`` ({"flanged": [[0, "1"], [3, "1-1/2"]]}),
    esa tabla reemplaza a la de fábrica para los tipos que defina.
    """
    value = _nps_value(nps)
    if math.isnan(value):
        return None
    table = SUGGESTED_SIZE[connection]
    if folder is not None and (folder / SIZE_TABLE_FILE).is_file():
        try:
            custom = json.loads((folder / SIZE_TABLE_FILE).read_text(encoding="utf-8"))
            rows = custom.get(connection.value)
            if rows:
                table = tuple((float(a), str(b)) for a, b in rows)
        except (OSError, ValueError, TypeError, AttributeError):
            pass
    size = table[0][1]
    for start, candidate in sorted(table):
        if value >= start:
            size = candidate
    return size
