"""Selección automática por bloque: material y protecciones, conexión, geometría y sensor.

A partir de los datos de proceso y de instalación (fluido, P y T, casos de flujo, NPS,
schedule, Hs y diámetro interno de la conexión de montaje), el programa elige los datos de
los bloques marcados como «automático» con reglas de práctica habitual y con la propia
verificación ASME PTC 19.3 TW, y deja cada elección con su justificación.

Las reglas son orientativas: el ingeniero debe revisar la selección.
"""

from __future__ import annotations

import math
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Final

from thermowell_sizer.core.advisories import EROSION_WATCH_RATIO, advise, erosional_velocity
from thermowell_sizer.core.designs import (
    BORE_260,
    BORE_385,
    DESIGN_NAMES,
    STANDARD_U,
    TYPICAL_DESIGNS,
    TypicalDesign,
    build_choice,
    recommended_u,
    suggested_connection_size,
)
from thermowell_sizer.core.models import (
    CalcInput,
    CheckStatus,
    ConnectionType,
    FlangeFace,
    MaterialRef,
    ShankProfile,
    ThermowellGeometry,
)
from thermowell_sizer.core.ptc19_3.verify import case_velocity
from thermowell_sizer.core.units import INCH_M, QuantityKind
from thermowell_sizer.data.selection import (
    H2S_SOUR_PARTIAL_PRESSURE,
    ServiceConditions,
    Verdict,
    recommend_materials,
)
from thermowell_sizer.i18n import Language, tr

if TYPE_CHECKING:
    from pathlib import Path

    from thermowell_sizer.data.database import Library
    from thermowell_sizer.project import ProjectSettings, TagRecord
    from thermowell_sizer.services import Evaluation

VerifyFn = Callable[[CalcInput], tuple[CheckStatus, float] | None]
"""Verifica un candidato: estado global y peor margen (%); ``None`` si no se puede calcular."""
"""Verifica un candidato y devuelve su estado (lo provee ``services``)."""

AUTO_BLOCKS: Final = ("material", "connection", "geometry", "sensor")
BLOCK_NAMES: Final[dict[str, tuple[str, str]]] = {
    "process": ("Propiedades del fluido", "Fluid properties"),
    "material": ("Material y protecciones", "Material and protections"),
    "connection": ("Conexión a proceso", "Process connection"),
    "geometry": ("Geometría del termopozo", "Thermowell geometry"),
    "sensor": ("Sensor", "Sensor"),
}
RATING_CLASSES: Final = (150, 300, 600, 900, 1500, 2500)
MATERIAL_PREFERENCE: Final = ("SS316", "SS304", "SS321", "SS347", "F11", "F22", "A105",
                              "D2205", "SD2507", "N06625", "N06600", "N10276", "N04400",
                              "F91", "TI2", "TA")
"""Desempate entre materiales igual de aptos: el 316/316L es la elección habitual."""
UTILITY_FLUIDS: Final = ("water", "air", "nitrogen")
THREADED_MAX_P: Final = 20e5
THREADED_MAX_T: Final = 473.15
WELD_IN_MIN_CLASS: Final = 1500
NOZZLE_CLEARANCE: Final = 1.5e-3
"""Holgura radial mínima entre Ø A y el diámetro interno de la conexión de montaje."""
DEFAULT_FILLET: Final = 0.125 * INCH_M
CA_AGGRESSIVE: Final = 1.0e-3
SHEATH_FOR_BORE: Final = {BORE_260: 6.0e-3, BORE_385: 8.0e-3}


@dataclass(frozen=True, slots=True)
class Decision:
    """Una elección automática con su justificación (español, inglés)."""

    block: str
    field: str
    """Clave de texto del dato (``f.material``, ``f.U``...)."""
    value: float | str | tuple[str, str]
    """Número en SI (con ``kind``), texto fijo o texto (español, inglés)."""
    kind: QuantityKind | None
    reason: tuple[str, str]
    alternatives: tuple[str, str] = ("", "")
    parts: tuple[tuple[str, float], ...] = ()
    """Varias cotas (símbolo, valor SI) que se muestran juntas con ``kind``."""

    def text(self, es: bool) -> str:
        """Justificación en el idioma pedido."""
        return self.reason[0 if es else 1]

    def shown(self, es: bool, qfmt: Callable[[float, QuantityKind], str]) -> str:
        """Valor elegido listo para mostrar."""
        if self.parts and self.kind is not None:
            kind = self.kind
            return " · ".join(f"{sym} {qfmt(v, kind)}" for sym, v in self.parts)
        if isinstance(self.value, tuple):
            return self.value[0 if es else 1]
        if isinstance(self.value, float) and self.kind is not None:
            return qfmt(self.value, self.kind)
        text = str(self.value)
        return _es(text) if es else text


CONNECTION_NAMES: Final[dict[str, tuple[str, str]]] = {
    "threaded": ("Roscada", "Threaded"), "flanged": ("Bridada", "Flanged"),
    "socket_weld": ("Socket weld", "Socket weld"), "weld_in": ("Soldada", "Weld-in"),
    "van_stone": ("Van Stone", "Van Stone"), "sanitary": ("Sanitaria", "Sanitary"),
}


@dataclass
class AutoResult:
    """Entrada completada y decisiones tomadas."""

    input: CalcInput
    decisions: list[Decision] = field(default_factory=list)


def _bi(es: str, en: str) -> tuple[str, str]:
    return _es(es), en


def _es(text: str) -> str:
    """Pasa los decimales de un texto en español a coma (solo números con punto)."""
    return _DECIMAL.sub(lambda m: m.group(0) if _PROTECTED.search(text[:m.start()])
                        else m.group(0).replace(".", ","), text)


# Números con punto que no son decimales: «PTC 19.3», «B16.5», «B36.10M», «grupo 2.2»
_DECIMAL = re.compile(r"(?<![A-Za-z\d.])\d+\.\d+(?![\d.]*[A-Za-z])")
_PROTECTED = re.compile(r"(?:PTC|grupo|group|tabla|table|§|sección|section)\s*$", re.IGNORECASE)


def _c(k: float) -> str:
    return f"{k - 273.15:.0f} °C"


def _mm(m: float) -> str:
    return f"{m * 1000:.1f} mm"


def _barg(p_gauge: float) -> str:
    return f"{p_gauge / 1e5:.1f} barg"


def _gauge(inp: CalcInput, barometric: float) -> float:
    return max(inp.process.design_pressure - barometric, 0.0)


def _max_velocity(inp: CalcInput) -> float:
    vs = []
    for case in inp.process.flow_cases:
        try:
            vs.append(case_velocity(inp, case))
        except (ValueError, ZeroDivisionError):
            continue
    return max(vs, default=0.0)


# --- Material y protecciones ------------------------------------------------------------------
def _choose_material(inp: CalcInput, library: Library,
                     out: list[Decision]) -> CalcInput:
    proc = inp.process
    c = proc.corrosion
    cond = ServiceConditions(design_temperature=proc.design_temperature,
                             nace_service=c.nace_service,
                             h2s_partial_pressure=c.h2s_partial_pressure,
                             chlorides_ppm=c.chlorides_ppm, erosive=c.solids_or_erosive)
    evals = recommend_materials(library, cond)
    order = {Verdict.RECOMMENDED: 0, Verdict.ACCEPTABLE: 1, Verdict.NOT_RECOMMENDED: 2}

    def pref(mid: str) -> int:
        return MATERIAL_PREFERENCE.index(mid) if mid in MATERIAL_PREFERENCE else 99

    evals.sort(key=lambda e: (order[e.verdict], -e.score, pref(e.material.id)))
    best = evals[0]
    reasons_es, reasons_en = [], []
    for r in best.reasons:
        key, _, agent = r.partition(":")
        reasons_es.append(tr(key, Language.ES, agent=agent))
        reasons_en.append(tr(key, Language.EN, agent=agent))
    sour = c.nace_service or c.h2s_partial_pressure >= H2S_SOUR_PARTIAL_PRESSURE
    base_es = (f"Matriz de selección de la biblioteca a {_c(proc.design_temperature)} de "
               f"diseño{', servicio ácido' if sour else ''}"
               f"{f', cloruros {c.chlorides_ppm:g} ppm' if c.chlorides_ppm else ''}: "
               f"{tr('sel.verdict.' + best.verdict.value, Language.ES).lower()} "
               f"(puntaje {best.score:g}). Entre materiales igual de aptos se prefiere el "
               "316/316L, estándar de la industria para termopozos.")
    base_en = (f"Library selection matrix at {_c(proc.design_temperature)} design"
               f"{', sour service' if sour else ''}"
               f"{f', chlorides {c.chlorides_ppm:g} ppm' if c.chlorides_ppm else ''}: "
               f"{tr('sel.verdict.' + best.verdict.value, Language.EN).lower()} "
               f"(score {best.score:g}). Among equally suitable materials 316/316L, the "
               "industry standard for thermowells, is preferred.")
    if reasons_es:
        base_es += " " + " ".join(reasons_es)
        base_en += " " + " ".join(reasons_en)
    alts = [e.material for e in evals[1:4] if e.verdict is not Verdict.NOT_RECOMMENDED]
    out.append(Decision("material", "f.material", f"{best.material.name} ({best.material.spec})",
                        None, _bi(base_es, base_en),
                        (", ".join(a.name for a in alts), ", ".join(a.name for a in alts))))
    if best.verdict is Verdict.NOT_RECOMMENDED:
        out.append(Decision("material", "f.material", "—", None, _bi(
            "Ningún material de la biblioteca resulta apto: consulte a un especialista en "
            "materiales o evalúe un revestimiento (PFA, PTFE, tantalio).",
            "No library material is suitable: consult a materials specialist or consider a "
            "lining (PFA, PTFE, tantalum).")))

    # protecciones
    rho = proc.properties.density
    v = _max_velocity(inp)
    ratio = v / erosional_velocity(rho) if rho > 0 else 0.0
    coating = ""
    coatings = library.coatings()
    if c.solids_or_erosive or ratio >= EROSION_WATCH_RATIO:
        cands = [x for x in coatings if x[3] == "erosion" and x[4] >= proc.design_temperature]
        if cands:
            coating = cands[0][0]
            why = (f"V/Ve = {ratio:.2f}" if ratio >= EROSION_WATCH_RATIO
                   else "servicio con sólidos")
            why_en = (f"V/Ve = {ratio:.2f}" if ratio >= EROSION_WATCH_RATIO
                      else "service with solids")
            out.append(Decision("material", "f.coating", (cands[0][1], cands[0][2]), None, _bi(
                f"Protección contra erosión ({why}; API RP 14E como criterio orientativo): "
                f"recargue duro apto hasta {_c(cands[0][4])}.",
                f"Erosion protection ({why_en}; API RP 14E as guidance): hardfacing suitable "
                f"up to {_c(cands[0][4])}."),
                (", ".join(x[1] for x in cands[1:]), ", ".join(x[2] for x in cands[1:]))))
    if not coating:
        out.append(Decision("material", "f.coating", "—", None, _bi(
            f"Sin recubrimiento: V/Ve = {ratio:.2f} (< 0,7) y sin sólidos declarados.",
            f"No coating: V/Ve = {ratio:.2f} (< 0.7) and no solids declared.")))
    aggressive = (sour or c.chlorides_ppm >= 50 or c.solids_or_erosive
                  or ratio >= EROSION_WATCH_RATIO)
    ca = CA_AGGRESSIVE if aggressive else 0.0
    out.append(Decision("material", "f.ca", ca, QuantityKind.LENGTH, _bi(
        "Sobreespesor de 1 mm por servicio agresivo (ácido, cloruros o erosión); se verifican "
        "también los casos con el sobreespesor consumido." if aggressive else
        "Sin sobreespesor: servicio limpio, sin agentes corrosivos ni erosión declarados.",
        "1 mm allowance for aggressive service (sour, chlorides or erosion); the cases with "
        "the allowance consumed are also checked." if aggressive else
        "No allowance: clean service with no corrosive agents or erosion declared.")))
    tw = inp.thermowell
    geom = tw.geometry.model_copy(update={"corrosion_allowance": ca})
    mat = MaterialRef(material_id=best.material.id, coating=coating)
    return inp.model_copy(update={"thermowell": tw.model_copy(
        update={"material": mat, "geometry": geom})})


# --- Conexión ----------------------------------------------------------------------------------
def _rating_class(inp: CalcInput, library: Library,
                  barometric: float) -> tuple[int, tuple[str, str] | None]:
    p = _gauge(inp, barometric)
    t = inp.process.design_temperature
    try:
        group = library.material(inp.thermowell.material.material_id).b16_5_group
    except KeyError:
        group = None
    for cls in RATING_CLASSES:
        pf = library.flange_rating(group, cls, t)
        if pf is not None and pf >= p:
            return cls, _bi(
                f"Clase {cls}, la menor que admite la presión de diseño: {_barg(pf)} a {_c(t)} "
                f"(grupo {group}, ASME B16.5) frente a {_barg(p)}.",
                f"Class {cls}, the lowest that holds the design pressure: {_barg(pf)} at "
                f"{_c(t)} (group {group}, ASME B16.5) vs {_barg(p)}.")
    return 0, None


def _choose_connection(inp: CalcInput, library: Library, barometric: float,
                       folder: Path | None, out: list[Decision]) -> CalcInput:
    proc, pipe = inp.process, inp.pipe
    p = _gauge(inp, barometric)
    utility = (proc.fluid_id in UTILITY_FLUIDS and proc.phase.value != "steam"
               and p <= THREADED_MAX_P and proc.design_temperature <= THREADED_MAX_T)
    cls, why_cls = _rating_class(inp, library, barometric)
    if cls >= WELD_IN_MIN_CLASS:
        ctype = ConnectionType.WELD_IN
        why = _bi(f"Para soldar: la presión de diseño ({_barg(p)}) exige clase {cls} o mayor; "
                  "a esas clases se prefiere la unión soldada a la línea.",
                  f"Weld-in: the design pressure ({_barg(p)}) needs class {cls} or higher; at "
                  "those classes a welded joint to the line is preferred.")
    elif utility:
        ctype = ConnectionType.THREADED
        why = _bi("Roscada: servicio de utilidades no peligroso (agua, aire o nitrógeno) "
                  "≤ 20 barg y ≤ 200 °C, donde la práctica habitual la admite.",
                  "Threaded: non-hazardous utility service (water, air or nitrogen) ≤ 20 barg "
                  "and ≤ 200 °C, where common practice allows it.")
    else:
        ctype = ConnectionType.FLANGED
        why = _bi("Bridada: servicio de proceso; permite desmontar e inspeccionar y evita "
                  "roscas en fluidos peligrosos, a presión o a temperatura.",
                  "Flanged: process service; it allows removal and inspection and avoids "
                  "threads with hazardous, pressurized or hot fluids.")
    size = suggested_connection_size(ctype, pipe.nominal_size or "", folder) or ""
    out.append(Decision("connection", "f.connection", CONNECTION_NAMES.get(
        ctype.value, (ctype.value, ctype.value)), None, why))
    out.append(Decision("connection", "f.conn_size", size or "—", None, _bi(
        f"Tamaño habitual para una línea NPS {pipe.nominal_size} (tabla de tamaños sugeridos, "
        "editable).", f"Usual size for an NPS {pipe.nominal_size} line (suggested size "
        "table, editable).")))
    rating: int | None = None
    face: FlangeFace | None = None
    if ctype in (ConnectionType.FLANGED, ConnectionType.VAN_STONE):
        rating = cls or 300
        face = FlangeFace.RF if rating <= 600 else FlangeFace.RTJ
        out.append(Decision("connection", "f.rating", str(rating), None, why_cls or _bi(
            "Grupo del material sin tabla B16.5 en la biblioteca (o presión fuera de tabla): se "
            "propone 300; verifique el rating aparte.",
            "Material group without a B16.5 table in the library (or pressure off the table): "
            "300 is proposed; check the rating separately.")))
        out.append(Decision("connection", "f.face", face.value, None, _bi(
            "RF hasta clase 600; RTJ desde clase 900 (práctica habitual).",
            "RF up to class 600; RTJ from class 900 (common practice).")))
    conn = inp.thermowell.connection.model_copy(
        update={"type": ctype, "size": size, "rating_class": rating, "face": face})
    return inp.model_copy(update={"thermowell": inp.thermowell.model_copy(
        update={"connection": conn})})


# --- Geometría ----------------------------------------------------------------------------------
_PROFILE_ORDER: Final = {ShankProfile.TAPERED: 0, ShankProfile.STEPPED: 1,
                         ShankProfile.STRAIGHT: 2}


def _designs_for(conn: ConnectionType) -> list[TypicalDesign]:
    same = [d for d in TYPICAL_DESIGNS if d.connection is conn]
    if not same:
        same = [d for d in TYPICAL_DESIGNS if d.connection is ConnectionType.FLANGED]
    return sorted(same, key=lambda d: _PROFILE_ORDER[d.profile])


def _u_candidates(pipe_id: float, nozzle: float) -> list[float]:
    rec = recommended_u(pipe_id, nozzle)
    low = nozzle + min(max(pipe_id / 4.0, 0.05), 0.5 * pipe_id)
    high = nozzle + 0.6 * pipe_id
    longer = [u for u in STANDARD_U if rec + 1e-9 < u <= high]
    shorter = [u for u in STANDARD_U if low <= u < rec - 1e-9]
    out = [rec, *longer, *sorted(shorter, reverse=True)]
    # Último recurso: largos no normalizados (múltiplos de 5 mm) con inmersión de 1/3 y 1/4
    # del diámetro, para que una brida alta no deje solo largos normalizados demasiado largos.
    for frac in (1 / 3, 1 / 4):
        u = math.ceil((nozzle + max(frac * pipe_id, 0.05)) / 0.005 - 1e-9) * 0.005
        if low - 1e-9 <= u and all(abs(u - x) > 2e-3 for x in out):
            out.append(u)
    return out


def _with_choice(inp: CalcInput, design: TypicalDesign, bore: float, u: float,
                 nozzle: float) -> CalcInput | None:
    tw = inp.thermowell
    c = build_choice(design, size=tw.connection.size or design.sizes[0], bore=bore, U=u,
                     nozzle_length=nozzle, rating_class=tw.connection.rating_class)
    g = tw.geometry
    data = g.model_dump()
    data.update({"profile": c.profile, "L": c.L, "U": c.U, "A": c.A, "B": c.B, "d": c.d,
                 "t": c.t, "Ls": c.Ls, "L0": c.L0, "b": g.b or DEFAULT_FILLET,
                 "bs": (g.bs or DEFAULT_FILLET) if c.profile is ShankProfile.STEPPED else 0.0})
    try:
        geom = ThermowellGeometry.model_validate(data)
    except ValueError:
        return None
    return inp.model_copy(update={"thermowell": tw.model_copy(update={"geometry": geom})})


def _choose_geometry(rec: TagRecord, inp: CalcInput, library: Library,
                     settings: ProjectSettings, out: list[Decision],
                     verify_fn: VerifyFn) -> CalcInput:
    pipe = inp.pipe
    if not pipe.inner_diameter:
        return inp
    nozzle = pipe.nozzle_length
    sheath = inp.sensor.sheath_diameter
    free_sensor = "sensor" in rec.auto_blocks
    bores = [BORE_260, BORE_385] if sheath <= 6.35e-3 or free_sensor else [BORE_385]
    designs = _designs_for(inp.thermowell.connection.type)
    tried: list[tuple[int, float, float, str, CalcInput]] = []
    first_pass: tuple[TypicalDesign, float, CalcInput] | None = None
    for u in _u_candidates(pipe.inner_diameter, nozzle):
        for design in designs:
            for bore in bores:
                if bore not in design.diameters:
                    continue
                cand = _with_choice(inp, design, bore, u, nozzle)
                if cand is None:
                    continue
                a = cand.thermowell.geometry.A
                if (pipe.nozzle_inner_diameter is not None
                        and a + 2 * NOZZLE_CLEARANCE > pipe.nozzle_inner_diameter):
                    continue
                checked = verify_fn(cand)
                if checked is None:
                    continue
                status, margin = checked
                rank = {CheckStatus.PASS: 0, CheckStatus.WARNING: 1, CheckStatus.FAIL: 2}.get(
                    status, 3)
                tried.append((rank, -margin, -u, design.id, cand))
                if rank == 0 and _immersion_ok(cand):
                    return _geometry_decisions(cand, design, u, nozzle, pipe.inner_diameter,
                                               out, passed=True)
                if rank == 0 and first_pass is None:
                    first_pass = (design, u, cand)
    if first_pass is not None:  # cumple ASME pero sin la inmersión recomendada
        design, u, cand = first_pass
        return _geometry_decisions(cand, design, u, nozzle, pipe.inner_diameter, out,
                                   passed=True, immersion_short=True)
    if not tried:
        out.append(Decision("geometry", "f.A", "—", None, _bi(
            "Ningún diseño normalizado entra en la conexión de montaje: aumente su diámetro "
            "interno o use un diseño especial.",
            "No standard design fits the mounting connection: increase its inside diameter or "
            "use a special design.")))
        return inp
    tried.sort(key=lambda x: (x[0], x[1], x[2]))  # estado, mejor margen, U más largo
    rank, _, neg_u, did, cand = tried[0]
    return _geometry_decisions(cand, next(d for d in TYPICAL_DESIGNS if d.id == did), -neg_u,
                               nozzle, pipe.inner_diameter, out, passed=rank <= 1)


def _immersion_ok(cand: CalcInput) -> bool:
    """La parte sensible queda bien inmersa y la punta lejos de la pared opuesta."""
    keys = {a.key for a in advise(cand)}
    return not keys & {"adv.immersion_short", "adv.tip_hits_wall"}


def _geometry_decisions(cand: CalcInput, design: TypicalDesign, u: float, nozzle: float,
                        pipe_id: float, out: list[Decision], *, passed: bool,
                        immersion_short: bool = False) -> CalcInput:
    g = cand.thermowell.geometry
    immersion = u - nozzle
    name = DESIGN_NAMES[design.id]
    out.append(Decision("geometry", "f.profile", name, None, _bi(
        f"Diseño típico «{name[0]}»: se prueban primero los cónicos (más rígidos a igual "
        "punta), luego escalonados y rectos, y se elige el primero que cumple ASME PTC 19.3 TW.",
        f"Typical design «{name[1]}»: tapered designs are tried first (stiffer for the same "
        "tip), then stepped and straight, and the first one that passes ASME PTC 19.3 TW is "
        "chosen.")))
    standard = any(abs(u - x) < 1e-6 for x in STANDARD_U)
    kind_es, kind_en = ("Largo normalizado", "Standard length") if standard else (
        "Largo no normalizado (múltiplo de 5 mm)", "Non-standard length (5 mm multiple)")
    mount_es = (f"con Hs + pared = {_mm(nozzle)}" if nozzle > 0 else
                "sin altura de montaje declarada (Hs = 0)")
    mount_en = (f"with Hs + wall = {_mm(nozzle)}" if nozzle > 0 else
                "with no mounting height declared (Hs = 0)")
    out.append(Decision("geometry", "f.U", u, QuantityKind.LENGTH, _bi(
        f"{kind_es}: la punta queda {_mm(immersion)} dentro del flujo "
        f"({immersion / pipe_id:.0%} del diámetro interno), {mount_es}. "
        "Se busca al menos 1/3 del diámetro (o 100 mm) y la inmersión recomendada de la parte "
        "sensible, sin acercarse a la pared opuesta; si no cumple ASME se prueban largos más "
        "cortos.",
        f"{kind_en}: the tip sits {_mm(immersion)} inside the flow ({immersion / pipe_id:.0%}"
        f" of the inside diameter), {mount_en}. At least 1/3 of the diameter"
        " (or 100 mm) and the recommended immersion of the sensitive part are sought without "
        "approaching the opposite wall; if ASME fails, shorter lengths are tried.")))
    if immersion_short:
        out.append(Decision("geometry", "f.U", "—", None, _bi(
            "Ningún largo que cumpla ASME deja la parte sensible con la inmersión recomendada "
            "(largo sensible + 6 a 10 veces el diámetro de punta): se eligió el que cumple. "
            "Evalúe el error por conducción o un sensor de punta corta.",
            "No length that passes ASME gives the sensitive part the recommended immersion "
            "(sensitive length + 6 to 10 tip diameters): the passing one was chosen. Assess "
            "the conduction error or a short-tip sensor.")))
    out.append(Decision("geometry", "f.dimensions", "", QuantityKind.DIAMETER, _bi(
        "Diámetros del diseño típico para el agujero elegido (0,260\" para vainas de hasta "
        "6 mm, 0,385\" para mayores); t = 1/4\".",
        "Typical-design diameters for the chosen bore (0.260\" for sheaths up to 6 mm, "
        "0.385\" for larger ones); t = 1/4\"."),
        parts=(("A", g.A), ("B", g.B), ("d", g.d))))
    if g.L0 > 0:
        out.append(Decision("geometry", "f.L0", g.L0, QuantityKind.LENGTH, _bi(
            "Zona protegida L0 = Hs + pared: el tramo dentro de la brida de montaje no recibe "
            "flujo y no se carga con arrastre.",
            "Shielded length L0 = Hs + wall: the part inside the mounting flange gets no flow "
            "and carries no drag.")))
    if not passed:
        out.append(Decision("geometry", "f.L", "—", None, _bi(
            "Ningún diseño normalizado cumple todos los criterios: se muestra el mejor "
            "encontrado. Considere reducir la velocidad, un diseño especial (Ø mayores), un "
            "collar de apoyo o «Proponer alternativas».",
            "No standard design meets every criterion: the best one found is shown. Consider "
            "reducing velocity, a special design (larger diameters), a support collar or "
            "«Propose alternatives».")))
    insulation = cand.pipe.insulation_thickness
    if insulation > 0:
        lag = math.ceil((insulation + 0.025) / 0.025) * 0.025
        geom = cand.thermowell.geometry.model_copy(update={"T_lag": lag})
        cand = cand.model_copy(update={"thermowell": cand.thermowell.model_copy(
            update={"geometry": geom})})
        out.append(Decision("geometry", "f.T_lag", lag, QuantityKind.LENGTH, _bi(
            f"Lag para sacar el cabezal de la aislación ({_mm(insulation)}) con 25 mm de "
            "margen.", f"Lag to keep the head clear of the insulation ({_mm(insulation)}) "
            "with a 25 mm margin.")))
    return cand


# --- Sensor -------------------------------------------------------------------------------------
def _choose_sensor(inp: CalcInput, out: list[Decision]) -> CalcInput:
    d = inp.thermowell.geometry.d
    sheath = 6.0e-3 if d < 8.0e-3 else 8.0e-3
    out.append(Decision("sensor", "f.sheath", sheath, QuantityKind.DIAMETER, _bi(
        f"Vaina normalizada para el agujero de {_mm(d)}: huelgo diametral de "
        f"{_mm(d - sheath)} (contacto térmico aceptable, inserción sin trabas).",
        f"Standard sheath for the {_mm(d)} bore: {_mm(d - sheath)} diametral clearance "
        "(acceptable thermal contact, easy insertion).")))
    sensor = inp.sensor.model_copy(update={"sheath_diameter": sheath, "spring_loaded": True})
    return inp.model_copy(update={"sensor": sensor})


def auto_design(rec: TagRecord, inp: CalcInput, library: Library, settings: ProjectSettings,
                verify: VerifyFn, folder: Path | None = None) -> AutoResult:
    """Completa los bloques automáticos de ``rec`` y devuelve las decisiones."""
    out: list[Decision] = []
    blocks = set(rec.auto_blocks)
    baro = settings.barometric_pressure
    if "material" in blocks:
        inp = _choose_material(inp, library, out)
    if "connection" in blocks:
        inp = _choose_connection(inp, library, baro, folder, out)
    if "geometry" in blocks:
        inp = _choose_geometry(rec, inp, library, settings, out, verify)
    if "sensor" in blocks:
        inp = _choose_sensor(inp, out)
    return AutoResult(inp, out)


def evaluation_blocks(ev: Evaluation) -> tuple[str, ...]:
    """Bloques automáticos de una evaluación (para marcar el origen de los datos)."""
    return tuple(sorted({d.block for d in ev.decisions}))
