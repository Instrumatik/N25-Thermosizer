"""Datos de fábrica de materiales.

IMPORTANTE: los valores de módulo elástico y esfuerzo admisible son **aproximados**,
compilados de fuentes públicas (hojas técnicas de fabricantes y valores típicos de
ASME B31.1/B31.3 y BPVC II-D). Todos quedan marcados ``verified = 0`` y la memoria de
cálculo lo informa. Antes de usar el programa en proyectos reales deben contrastarse
con la edición vigente del código aplicable. Las temperaturas están en °C, el módulo
en GPa y los esfuerzos en MPa; la capa de datos los convierte a SI al cargarlos.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Final

PUBLIC_SOURCE: Final = "public-compilation-2026"
TABLE_SOURCE: Final = "ASME-PTC-19.3-TW-2016-T6-12.3-1"


@dataclass(frozen=True, slots=True)
class MaterialSeed:
    """Material de la biblioteca de fábrica."""

    id: str
    name: str
    spec: str
    uns: str
    family: str
    fatigue_class: str
    fatigue_table_covered: bool
    e_ref_gpa: float
    max_temp_c: float
    min_temp_c: float
    density: float
    nace_ok: bool
    b16_5_group: str | None
    elastic_modulus_gpa: Mapping[int, float]
    allowable_stress_mpa: Mapping[int, float]
    notes_es: str = ""
    notes_en: str = ""
    scc_chlorides: bool = False
    tags: tuple[str, ...] = field(default=())


_E_CARBON = {20: 203, 100: 198, 200: 192, 300: 185, 400: 176, 450: 170, 500: 162}
_E_LOW_CR = {20: 204, 100: 200, 200: 194, 300: 187, 400: 180, 500: 171, 550: 166, 600: 160}
_E_9CR = {20: 213, 100: 209, 200: 203, 300: 197, 400: 189, 500: 181, 600: 171, 650: 165}
_E_AUSTENITIC = {20: 195, 100: 189, 200: 183, 300: 176, 400: 169, 500: 161, 600: 153,
                 700: 145, 800: 136}
_E_DUPLEX = {20: 200, 100: 194, 200: 186, 300: 180}

MATERIALS: Final[tuple[MaterialSeed, ...]] = (
    MaterialSeed(
        "A105", "Acero al carbono A105", "ASTM A105", "K03504", "carbon", "A", True, 202,
        427, -29, 7850, True, "1.1", _E_CARBON,
        {20: 138, 200: 138, 260: 137, 316: 134, 343: 122, 371: 108, 399: 90, 427: 74},
        "Uso general en hidrocarburos, vapor y agua. Grafitización sobre 427 °C.",
        "General service. Graphitization above 427 °C.",
    ),
    MaterialSeed(
        "F11", "Acero 1¼Cr-½Mo F11 cl. 2", "ASTM A182 F11 Cl.2", "K11572", "low_alloy", "A",
        True, 213, 593, -29, 7850, True, "1.9", _E_LOW_CR,
        {20: 138, 300: 138, 400: 133, 450: 128, 482: 113, 500: 93, 538: 50, 566: 33, 593: 21},
        "Vapor y servicio a alta temperatura moderada.",
        "Steam and moderate high-temperature service.",
    ),
    MaterialSeed(
        "F22", "Acero 2¼Cr-1Mo F22 cl. 3", "ASTM A182 F22 Cl.3", "K21590", "low_alloy", "A",
        True, 213, 593, -29, 7850, True, "1.10", _E_LOW_CR,
        {20: 148, 300: 145, 400: 140, 450: 135, 482: 128, 500: 112, 538: 74, 566: 54, 593: 37},
        "Vapor de alta presión, hidrotratamiento.", "High-pressure steam, hydrotreating.",
    ),
    MaterialSeed(
        "F91", "Acero 9Cr-1Mo-V F91", "ASTM A182 F91", "K90901", "low_alloy", "A", True, 202,
        649, -29, 7770, False, None, _E_9CR,
        {20: 167, 400: 160, 450: 155, 500: 145, 538: 125, 550: 118, 575: 96, 600: 77,
         625: 58, 649: 41},
        "Vapor principal y recalentado en centrales; requiere tratamiento térmico controlado.",
        "Main and reheat steam; requires controlled heat treatment.",
    ),
    MaterialSeed(
        "SS304", "Inoxidable 304/304L", "ASTM A182 F304/F304L", "S30400", "austenitic", "B",
        True, 195, 816, -196, 7900, True, "2.1", _E_AUSTENITIC,
        {20: 138, 150: 138, 200: 129, 250: 122, 300: 116, 350: 112, 400: 108, 450: 105,
         500: 101, 550: 97, 600: 64, 650: 48, 700: 32, 750: 22, 800: 14},
        "Uso general; sensible a corrosión bajo tensión por cloruros sobre 60 °C.",
        "General use; chloride stress-corrosion cracking above 60 °C.",
        scc_chlorides=True,
    ),
    MaterialSeed(
        "SS316", "Inoxidable 316/316L", "ASTM A182 F316/F316L", "S31600", "austenitic", "B",
        True, 195, 816, -196, 8000, True, "2.2", _E_AUSTENITIC,
        {20: 138, 200: 134, 250: 129, 300: 124, 350: 121, 400: 119, 450: 117, 500: 115,
         550: 110, 600: 90, 650: 59, 700: 40, 750: 26, 800: 17},
        "Material estándar de termopozos; mejor que 304 frente a cloruros y ácidos débiles.",
        "Standard thermowell material; better than 304 against chlorides.",
        scc_chlorides=True,
    ),
    MaterialSeed(
        "SS321", "Inoxidable 321", "ASTM A182 F321", "S32100", "austenitic", "B", True, 195,
        816, -196, 7900, True, "2.4", _E_AUSTENITIC,
        {20: 138, 200: 132, 300: 121, 400: 113, 500: 106, 550: 100, 600: 83, 650: 52,
         700: 34, 800: 15},
        "Estabilizado con Ti; servicio cíclico a alta temperatura.",
        "Ti-stabilized; cyclic high-temperature service.",
        scc_chlorides=True,
    ),
    MaterialSeed(
        "SS347", "Inoxidable 347", "ASTM A182 F347", "S34700", "austenitic", "B", True, 195,
        816, -196, 7960, True, "2.5", _E_AUSTENITIC,
        {20: 138, 200: 134, 300: 125, 400: 117, 500: 110, 550: 103, 600: 92, 650: 63,
         700: 38, 800: 16},
        "Estabilizado con Nb; resiste sensibilización a alta temperatura.",
        "Nb-stabilized; resists sensitization at high temperature.",
        scc_chlorides=True,
    ),
    MaterialSeed(
        "D2205", "Dúplex 2205", "ASTM A182 F51 / F60", "S32205", "duplex", "A", True, 202,
        315, -50, 7800, True, "2.8", _E_DUPLEX,
        {20: 177, 100: 177, 200: 165, 300: 158, 315: 156},
        "Alta resistencia y buena resistencia a cloruros; máximo 315 °C (fragilización).",
        "High strength and chloride resistance; 315 °C maximum (embrittlement).",
    ),
    MaterialSeed(
        "SD2507", "Súper dúplex 2507", "ASTM A182 F53", "S32750", "duplex", "A", True, 202,
        315, -50, 7800, True, "2.8", _E_DUPLEX,
        {20: 228, 100: 220, 200: 205, 300: 196, 315: 194},
        "Agua de mar y salmueras; máximo 315 °C.", "Seawater and brines; 315 °C maximum.",
    ),
    MaterialSeed(
        "N06600", "Inconel 600", "ASTM B564 N06600", "N06600", "nickel", "B", True, 195,
        649, -196, 8470, True, None,
        {20: 214, 100: 210, 200: 205, 300: 199, 400: 194, 500: 188, 600: 181, 650: 177},
        {20: 138, 400: 138, 500: 138, 550: 125, 600: 82, 649: 55},
        "Atmósferas oxidantes y cloruros a alta temperatura.",
        "Oxidizing atmospheres and high-temperature chlorides.",
    ),
    MaterialSeed(
        "N06625", "Inconel 625", "ASTM B564 N06625", "N06625", "nickel", "B", True, 195,
        649, -196, 8440, True, None,
        {20: 208, 100: 204, 200: 200, 300: 194, 400: 188, 500: 182, 600: 176, 650: 172},
        {20: 236, 200: 228, 300: 222, 400: 220, 500: 213, 600: 209, 649: 200},
        "Muy alta resistencia mecánica y a la corrosión localizada.",
        "Very high strength and pitting resistance.",
    ),
    MaterialSeed(
        "N10276", "Hastelloy C276", "ASTM B564 N10276", "N10276", "nickel", "B", True, 195,
        677, -196, 8890, True, None,
        {20: 205, 100: 202, 200: 196, 300: 190, 400: 185, 500: 178, 600: 172, 677: 167},
        {20: 197, 200: 182, 300: 172, 400: 166, 500: 160, 600: 152, 677: 145},
        "Ácidos reductores y oxidantes, cloro húmedo, cloruros calientes.",
        "Reducing and oxidizing acids, wet chlorine, hot chlorides.",
    ),
    MaterialSeed(
        "N04400", "Monel 400", "ASTM B564 N04400", "N04400", "nickel_copper", "B", True, 179,
        482, -196, 8800, True, None,
        {20: 179, 100: 176, 200: 172, 300: 168, 400: 164, 482: 159},
        {20: 115, 100: 108, 200: 104, 300: 101, 400: 98, 482: 80},
        "Ácido fluorhídrico, agua de mar, álcalis.", "Hydrofluoric acid, seawater, alkalis.",
    ),
    MaterialSeed(
        "TI2", "Titanio grado 2", "ASTM B381 F2", "R50400", "titanium", "A", False, 202, 316,
        -60, 4510, True, None,
        {20: 107, 100: 103, 200: 97, 300: 91, 316: 90},
        {20: 99, 100: 87, 200: 66, 300: 52, 316: 50},
        "Agua de mar, cloro húmedo; no figura en la tabla de fatiga de la norma.",
        "Seawater, wet chlorine; not in the standard's fatigue table.",
    ),
    MaterialSeed(
        "TA", "Tantalio", "ASTM B365 R05200", "R05200", "refractory", "A", False, 202, 250, -60,
        16690, False, None,
        {20: 186, 100: 185, 250: 183},
        {20: 49, 100: 46, 250: 40},
        "Ácidos muy agresivos (HCl, H₂SO₄ caliente); se oxida en aire sobre 250 °C.",
        "Very aggressive acids; oxidizes in air above 250 °C.",
    ),
)

COATINGS: Final[tuple[tuple[str, str, str, str, float], ...]] = (
    # (id, nombre ES, nombre EN, uso, temperatura máxima °C)
    ("STELLITE6", "Recargue de estelita 6", "Stellite 6 hardfacing", "erosion", 800.0),
    ("WC_HVOF", "Carburo de tungsteno (HVOF)", "Tungsten carbide (HVOF)", "erosion", 500.0),
    ("STELLITE1", "Recargue de estelita 1 (mayor dureza)", "Stellite 1 hardfacing (harder)",
     "erosion", 800.0),
    ("CRC_HVOF", "Carburo de cromo (HVOF)", "Chromium carbide (HVOF)", "erosion", 850.0),
    ("PTFE", "Revestimiento de PTFE", "PTFE lining", "corrosion", 200.0),
    ("PFA", "Revestimiento de PFA", "PFA lining", "corrosion", 230.0),
    ("PVDF", "Revestimiento de PVDF (Kynar)", "PVDF (Kynar) lining", "corrosion", 90.0),
    ("TANTALUM", "Funda de tantalio", "Tantalum sheath", "corrosion", 250.0),
    ("CERAMIC", "Funda cerámica (alúmina)", "Ceramic sheath (alumina)", "temperature", 1600.0),
)
