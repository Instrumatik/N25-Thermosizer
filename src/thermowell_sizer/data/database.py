"""Acceso a la biblioteca local (SQLite).

La base se crea y se completa con los datos de fábrica la primera vez. Cuando cambia
``SEED_VERSION`` se reescriben solo las filas de fábrica; lo que agregó el usuario
(``user_defined = 1``) se conserva.
"""

from __future__ import annotations

import difflib
import sqlite3
import unicodedata
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

import numpy as np

from thermowell_sizer.core.models import FatigueClass, MaterialProperties
from thermowell_sizer.core.units import BAR_PA, INCH_M, KELVIN_OFFSET
from thermowell_sizer.data import seed_library, seed_materials, seed_tables

SEED_VERSION = "2026.11.1"
GPA = 1.0e9
MPA = 1.0e6
MPA_S = 1.0e-3


def _c(t: float) -> float:
    return t + KELVIN_OFFSET


@dataclass(frozen=True, slots=True)
class MaterialInfo:
    """Ficha de un material para listas y la biblioteca."""

    id: str
    name: str
    spec: str
    uns: str
    family: str
    fatigue_class: str
    fatigue_covered: bool
    max_temperature: float
    min_temperature: float | None
    density: float
    nace_ok: bool
    b16_5_group: str | None
    scc_chlorides: bool
    notes_es: str
    notes_en: str
    verified: bool
    user_defined: bool


@dataclass(frozen=True, slots=True)
class FluidInfo:
    """Fluido de la biblioteca."""

    id: str
    name_es: str
    name_en: str
    coolprop_name: str | None
    default_phase: str
    user_defined: bool


@dataclass(frozen=True, slots=True)
class PipeInfo:
    """Tubería ASME B36.10M."""

    nps: str
    dn: int
    schedule: str
    outer_diameter: float
    wall_thickness: float

    @property
    def inner_diameter(self) -> float:
        """Diámetro interno, m."""
        return self.outer_diameter - 2.0 * self.wall_thickness


@dataclass(frozen=True, slots=True)
class GlossaryEntry:
    """Término del glosario."""

    id: str
    term_es: str
    term_en: str
    definition_es: str
    definition_en: str
    formula: str
    diagram: str


@dataclass(frozen=True, slots=True)
class SearchHit:
    """Resultado del buscador global."""

    kind: str
    ref_id: str
    title: str
    score: float


def _normalize(text: str) -> str:
    folded = unicodedata.normalize("NFKD", text.casefold())
    return "".join(ch for ch in folded if not unicodedata.combining(ch))


class Library:
    """Repositorio de la biblioteca técnica."""

    def __init__(self, path: Path | str = ":memory:") -> None:
        self.path = str(path)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        schema = resources.files("thermowell_sizer.data").joinpath("schema.sql").read_text(
            encoding="utf-8"
        )
        self.conn.executescript(schema)
        if self._meta("seed_version") != SEED_VERSION:
            self._seed()

    # --- Gestión ----------------------------------------------------------------------
    def close(self) -> None:
        """Cierra la conexión."""
        self.conn.close()

    def _meta(self, key: str) -> str | None:
        row = self.conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return None if row is None else str(row["value"])

    def _seed(self) -> None:
        c = self.conn
        with c:
            c.execute("DELETE FROM material WHERE user_defined = 0")
            c.execute("DELETE FROM fluid WHERE user_defined = 0")
            for table in ("coating", "flange_rating", "pipe_size", "sensor_model",
                          "glossary_term", "standard_summary", "search_index"):
                c.execute(f"DELETE FROM {table}")
            c.executemany(
                "INSERT OR REPLACE INTO source (id, citation, note, verified) VALUES (?,?,?,?)",
                [
                    (seed_materials.PUBLIC_SOURCE, "Compilación de fuentes públicas",
                     "Valores aproximados: verificar contra ASME BPVC II-D / B31.1", 0),
                    (seed_materials.TABLE_SOURCE, "ASME PTC 19.3 TW-2016, Table 6-12.3-1",
                     "", 1),
                    (seed_tables.FLANGE_SOURCE, "Compilación pública de ratings ASME B16.5",
                     "Verificar contra la edición vigente de ASME B16.5", 0),
                ],
            )
            self._seed_materials()
            self._seed_tables()
            self._seed_library()
            c.execute(
                "INSERT OR REPLACE INTO meta (key, value) VALUES ('seed_version', ?)",
                (SEED_VERSION,),
            )

    def _seed_materials(self) -> None:
        c = self.conn
        for m in seed_materials.MATERIALS:
            c.execute(
                """INSERT INTO material (id, name, spec, uns, family, fatigue_class,
                fatigue_covered, e_ref, scc_chlorides, notes_es, notes_en, max_temperature,
                min_temperature, density, nace_ok, b16_5_group, user_defined, source_id)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0,?)""",
                (m.id, m.name, m.spec, m.uns, m.family, m.fatigue_class,
                 int(m.fatigue_table_covered), m.e_ref_gpa * GPA, int(m.scc_chlorides),
                 m.notes_es, m.notes_en, _c(m.max_temp_c), _c(m.min_temp_c), m.density,
                 int(m.nace_ok), m.b16_5_group, seed_materials.PUBLIC_SOURCE),
            )
            rows = [(m.id, "elastic_modulus", _c(t), v * GPA, seed_materials.PUBLIC_SOURCE)
                    for t, v in m.elastic_modulus_gpa.items()]
            rows += [(m.id, "allowable_stress", _c(t), v * MPA, seed_materials.PUBLIC_SOURCE)
                     for t, v in m.allowable_stress_mpa.items()]
            c.executemany(
                """INSERT INTO material_property_point
                (material_id, property, temperature, value, source_id) VALUES (?,?,?,?,?)""",
                rows,
            )
            c.execute("INSERT INTO search_index VALUES ('material', ?, ?, ?)",
                      (m.id, f"{m.name} {m.spec} {m.uns}", m.notes_es))
            for agent, rating in zip(seed_tables.AGENTS, seed_tables.COMPATIBILITY.get(m.id, ""),
                                     strict=False):
                c.execute(
                    """INSERT OR REPLACE INTO chemical_compatibility
                    (material_id, agent, rating) VALUES (?,?,?)""",
                    (m.id, agent, rating),
                )
        c.executemany(
            "INSERT INTO coating VALUES (?,?,?,?,?)",
            [(i, es, en, use, _c(t)) for i, es, en, use, t in seed_materials.COATINGS],
        )
        c.executemany(
            "INSERT INTO search_index VALUES ('coating', ?, ?, ?)",
            [(i, f"{es} {en}", use) for i, es, en, use, _ in seed_materials.COATINGS],
        )

    def _seed_tables(self) -> None:
        c = self.conn
        for group, classes in seed_tables.FLANGE_RATINGS.items():
            expanded = dict(classes)
            for cls, factor in seed_tables.CLASS_FACTORS_FROM_300.items():
                expanded[cls] = tuple(round(p * factor, 1) for p in classes[300])
            for cls, values in expanded.items():
                c.executemany(
                    "INSERT INTO flange_rating VALUES (?,?,?,?,?)",
                    [(group, cls, _c(t), p * BAR_PA, seed_tables.FLANGE_SOURCE)
                     for t, p in zip(seed_tables.FLANGE_TEMPS_C, values, strict=True)],
                )
        for schedule, walls in seed_tables.PIPE_WALL_IN.items():
            c.executemany(
                "INSERT INTO pipe_size VALUES (?,?,?,?,?)",
                [(nps, seed_tables.PIPE_DN[nps], schedule,
                  seed_tables.PIPE_OD_IN[nps] * INCH_M, w * INCH_M)
                 for nps, w in walls.items()],
            )
        for fid, es, en, cp, phase in seed_tables.FLUIDS:
            c.execute("INSERT INTO fluid VALUES (?,?,?,?,?,0,NULL)", (fid, es, en, cp, phase))
            c.execute("INSERT INTO search_index VALUES ('fluid', ?, ?, ?)", (fid, es, en))
        for fid, points in seed_tables.TABULATED_FLUIDS.items():
            c.executemany(
                "INSERT OR REPLACE INTO fluid_property_point VALUES (?,?,?,?,?)",
                [(fid, _c(t), 101_325.0, rho, mu * MPA_S) for t, rho, mu in points],
            )
        c.executemany(
            "INSERT INTO sensor_model VALUES (?,?,?,NULL,?,?)",
            [(i, typ, dia / 1000.0, seed_tables.SENSOR_DENSITY, _c(t))
             for i, typ, dia, t in seed_tables.SENSORS],
        )

    def _seed_library(self) -> None:
        c = self.conn
        for g in seed_library.GLOSSARY:
            c.execute(
                """INSERT INTO glossary_term (id, term_es, term_en, definition_es,
                definition_en, formula, diagram) VALUES (?,?,?,?,?,?,?)""",
                g,
            )
            c.execute("INSERT INTO search_index VALUES ('glossary', ?, ?, ?)",
                      (g[0], f"{g[1]} {g[2]}", f"{g[3]} {g[4]}"))
        for s in seed_library.STANDARDS:
            c.execute("INSERT INTO standard_summary VALUES (?,?,?,?,?,'')", s)
            c.execute("INSERT INTO search_index VALUES ('standard', ?, ?, ?)",
                      (s[0], s[1], s[3]))

    # --- Materiales ---------------------------------------------------------------------
    def materials(self) -> list[MaterialInfo]:
        """Lista de materiales (fábrica y usuario)."""
        rows = self.conn.execute(
            """SELECT m.*, COALESCE(s.verified, 0) AS verified FROM material m
            LEFT JOIN source s ON s.id = m.source_id ORDER BY m.user_defined, m.rowid"""
        ).fetchall()
        return [self._material_info(r) for r in rows]

    def material(self, material_id: str) -> MaterialInfo:
        """Ficha de un material.

        Raises:
            KeyError: si no existe.
        """
        row = self.conn.execute(
            """SELECT m.*, COALESCE(s.verified, 0) AS verified FROM material m
            LEFT JOIN source s ON s.id = m.source_id WHERE m.id = ?""",
            (material_id,),
        ).fetchone()
        if row is None:
            raise KeyError(material_id)
        return self._material_info(row)

    @staticmethod
    def _material_info(r: sqlite3.Row) -> MaterialInfo:
        return MaterialInfo(
            id=r["id"], name=r["name"], spec=r["spec"], uns=r["uns"], family=r["family"],
            fatigue_class=r["fatigue_class"], fatigue_covered=bool(r["fatigue_covered"]),
            max_temperature=r["max_temperature"], min_temperature=r["min_temperature"],
            density=r["density"], nace_ok=bool(r["nace_ok"]), b16_5_group=r["b16_5_group"],
            scc_chlorides=bool(r["scc_chlorides"]), notes_es=r["notes_es"],
            notes_en=r["notes_en"], verified=bool(r["verified"]),
            user_defined=bool(r["user_defined"]),
        )

    def property_curve(self, material_id: str, prop: str) -> list[tuple[float, float]]:
        """Puntos (T [K], valor SI) de una propiedad, ordenados por temperatura."""
        rows = self.conn.execute(
            """SELECT temperature, value FROM material_property_point
            WHERE material_id = ? AND property = ? ORDER BY temperature""",
            (material_id, prop),
        ).fetchall()
        return [(r["temperature"], r["value"]) for r in rows]

    def property_at(self, material_id: str, prop: str, temperature: float) -> float:
        """Interpolación lineal; fuera del rango se usa el extremo más cercano.

        Raises:
            KeyError: si el material no tiene datos de esa propiedad.
        """
        curve = self.property_curve(material_id, prop)
        if not curve:
            raise KeyError(f"{material_id}:{prop}")
        ts, vs = zip(*curve, strict=True)
        return float(np.interp(temperature, ts, vs))

    def material_properties(
        self, material_id: str, operating_temperature: float, design_temperature: float
    ) -> MaterialProperties:
        """Propiedades resueltas para el motor (párr. 7-4.3)."""
        info = self.material(material_id)
        e_ref = self.conn.execute(
            "SELECT e_ref FROM material WHERE id = ?", (material_id,)
        ).fetchone()["e_ref"]
        return MaterialProperties(
            material_id=info.id,
            name=info.name,
            density=info.density,
            elastic_modulus=self.property_at(material_id, "elastic_modulus",
                                             operating_temperature),
            elastic_modulus_reference=e_ref,
            allowable_stress=self.property_at(material_id, "allowable_stress",
                                              operating_temperature),
            allowable_stress_design=self.property_at(material_id, "allowable_stress",
                                                     design_temperature),
            fatigue_class=FatigueClass(info.fatigue_class),
            fatigue_table_covered=info.fatigue_covered,
            max_temperature=info.max_temperature,
            stress_corrosion_susceptible=info.scc_chlorides,
            source_note=("Valores de biblioteca, a verificar" if not info.verified
                         else "Biblioteca verificada"),
        )

    def add_user_material(
        self,
        info: MaterialInfo,
        e_ref: float,
        elastic_modulus: list[tuple[float, float]],
        allowable_stress: list[tuple[float, float]],
    ) -> None:
        """Agrega o reemplaza un material del usuario (valores SI, T en K)."""
        with self.conn:
            self.conn.execute(
                """INSERT OR REPLACE INTO material (id, name, spec, uns, family,
                fatigue_class, fatigue_covered, e_ref, scc_chlorides, notes_es, notes_en,
                max_temperature, min_temperature, density, nace_ok, b16_5_group,
                user_defined) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)""",
                (info.id, info.name, info.spec, info.uns, info.family, info.fatigue_class,
                 int(info.fatigue_covered), e_ref, int(info.scc_chlorides), info.notes_es,
                 info.notes_en, info.max_temperature, info.min_temperature, info.density,
                 int(info.nace_ok), info.b16_5_group),
            )
            self.conn.execute("DELETE FROM material_property_point WHERE material_id = ?",
                              (info.id,))
            rows = [(info.id, "elastic_modulus", t, v, None) for t, v in elastic_modulus]
            rows += [(info.id, "allowable_stress", t, v, None) for t, v in allowable_stress]
            self.conn.executemany(
                "INSERT INTO material_property_point VALUES (?,?,?,?,?)", rows
            )

    def coatings(self) -> list[tuple[str, str, str, str, float]]:
        """Recubrimientos: (id, nombre ES, nombre EN, uso, T máx K)."""
        rows = self.conn.execute("SELECT * FROM coating").fetchall()
        return [tuple(r) for r in rows]

    def compatibility(self, material_id: str) -> dict[str, str]:
        """Compatibilidad química orientativa del material: agente -> A/B/C."""
        rows = self.conn.execute(
            "SELECT agent, rating FROM chemical_compatibility WHERE material_id = ?",
            (material_id,),
        ).fetchall()
        return {r["agent"]: r["rating"] for r in rows}

    # --- Bridas y tuberías ----------------------------------------------------------------
    def flange_rating(
        self, group: str | None, rating_class: int, temperature: float
    ) -> float | None:
        """Presión admisible de la brida (Pa manométricos) a ``temperature`` (K).

        Devuelve ``None`` si el grupo o la clase no están en la biblioteca, o si la
        temperatura supera el último punto tabulado.
        """
        if group is None:
            return None
        rows = self.conn.execute(
            """SELECT temperature, pressure FROM flange_rating
            WHERE material_group = ? AND class = ? ORDER BY temperature""",
            (group, rating_class),
        ).fetchall()
        if not rows or temperature > rows[-1]["temperature"]:
            return None
        ts = [r["temperature"] for r in rows]
        ps = [r["pressure"] for r in rows]
        return float(np.interp(temperature, ts, ps))

    def flange_groups(self) -> list[str]:
        """Grupos de material con ratings cargados."""
        rows = self.conn.execute(
            "SELECT DISTINCT material_group FROM flange_rating ORDER BY material_group"
        ).fetchall()
        return [r[0] for r in rows]

    def pipe_sizes(self) -> list[str]:
        """Tamaños nominales NPS disponibles, en orden creciente."""
        rows = self.conn.execute(
            "SELECT DISTINCT nps, outer_diameter FROM pipe_size ORDER BY outer_diameter"
        ).fetchall()
        return [r["nps"] for r in rows]

    def schedules(self, nps: str) -> list[str]:
        """Schedules disponibles para un NPS."""
        rows = self.conn.execute(
            "SELECT schedule FROM pipe_size WHERE nps = ? ORDER BY wall_thickness", (nps,)
        ).fetchall()
        return list(dict.fromkeys(r[0] for r in rows))

    def pipe(self, nps: str, schedule: str) -> PipeInfo:
        """Dimensiones de una tubería.

        Raises:
            KeyError: si la combinación no existe.
        """
        r = self.conn.execute(
            "SELECT * FROM pipe_size WHERE nps = ? AND schedule = ?", (nps, schedule)
        ).fetchone()
        if r is None:
            raise KeyError(f"NPS {nps} Sch {schedule}")
        return PipeInfo(r["nps"], r["dn"], r["schedule"], r["outer_diameter"],
                        r["wall_thickness"])

    # --- Fluidos y sensores -------------------------------------------------------------
    def fluids(self) -> list[FluidInfo]:
        """Fluidos disponibles."""
        rows = self.conn.execute("SELECT * FROM fluid ORDER BY user_defined, rowid").fetchall()
        return [FluidInfo(r["id"], r["name_es"], r["name_en"], r["coolprop_name"],
                          r["default_phase"], bool(r["user_defined"])) for r in rows]

    def fluid(self, fluid_id: str) -> FluidInfo:
        """Fluido por id.

        Raises:
            KeyError: si no existe.
        """
        for f in self.fluids():
            if f.id == fluid_id:
                return f
        raise KeyError(fluid_id)

    def tabulated_fluid(self, fluid_id: str, temperature: float) -> tuple[float, float] | None:
        """(ρ, μ) interpolados de las tablas del fluido, o ``None`` si no hay tabla."""
        rows = self.conn.execute(
            """SELECT temperature, density, dynamic_viscosity FROM fluid_property_point
            WHERE fluid_id = ? ORDER BY temperature""",
            (fluid_id,),
        ).fetchall()
        if not rows:
            return None
        ts = [r[0] for r in rows]
        rho = float(np.interp(temperature, ts, [r[1] for r in rows]))
        # La viscosidad varía de forma aproximadamente exponencial con T.
        mu = float(np.exp(np.interp(temperature, ts, [np.log(r[2]) for r in rows])))
        return rho, mu

    def add_user_fluid(
        self, fluid_id: str, name: str, phase: str, points: list[tuple[float, float, float]]
    ) -> None:
        """Agrega un fluido tabulado del usuario: puntos (T [K], ρ, μ [Pa·s])."""
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO fluid VALUES (?,?,?,NULL,?,1,NULL)",
                (fluid_id, name, name, phase),
            )
            self.conn.execute("DELETE FROM fluid_property_point WHERE fluid_id = ?",
                              (fluid_id,))
            self.conn.executemany(
                "INSERT INTO fluid_property_point VALUES (?,?,?,?,?)",
                [(fluid_id, t, 101_325.0, rho, mu) for t, rho, mu in points],
            )

    def sensors(self) -> list[tuple[str, str, float, float]]:
        """Sensores: (id, tipo, diámetro de vaina m, T máx K)."""
        rows = self.conn.execute(
            "SELECT id, type, sheath_diameter, max_temperature FROM sensor_model"
        ).fetchall()
        return [(r[0], r[1], r[2], r[3]) for r in rows]

    # --- Biblioteca -------------------------------------------------------------------------
    def glossary(self) -> list[GlossaryEntry]:
        """Términos del glosario en orden alfabético español."""
        rows = self.conn.execute("SELECT * FROM glossary_term ORDER BY term_es").fetchall()
        return [GlossaryEntry(r["id"], r["term_es"], r["term_en"], r["definition_es"],
                              r["definition_en"], r["formula"], r["diagram"]) for r in rows]

    def standards(self) -> list[tuple[str, str, str, str, str]]:
        """Fichas de normas: (id, título, edición, resumen ES, resumen EN)."""
        rows = self.conn.execute(
            "SELECT id, title, edition, summary_es, summary_en FROM standard_summary"
        ).fetchall()
        return [tuple(r) for r in rows]

    def search(self, text: str, limit: int = 15) -> list[SearchHit]:
        """Buscador global tolerante a errores de escritura y sin distinguir acentos."""
        query = _normalize(text.strip())
        if not query:
            return []
        rows = self.conn.execute("SELECT kind, ref_id, title, body FROM search_index").fetchall()
        hits: list[SearchHit] = []
        for r in rows:
            title = _normalize(r["title"])
            body = _normalize(r["body"])
            words = title.split()
            if query in title:
                score = 1.0
            elif query in body:
                score = 0.7
            else:
                best = max((difflib.SequenceMatcher(None, query, w).ratio() for w in words),
                           default=0.0)
                score = best * 0.9 if best >= 0.7 else 0.0
            if score > 0:
                hits.append(SearchHit(r["kind"], r["ref_id"], r["title"], score))
        hits.sort(key=lambda h: -h.score)
        return hits[:limit]
