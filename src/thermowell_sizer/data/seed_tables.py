"""Tablas de fábrica: bridas, tuberías, fluidos, sensores y compatibilidad química.

Los ratings de bridas y la compatibilidad química son **orientativos** y quedan
marcados como "a verificar". Unidades de las tablas: °C, bar manométricos, pulgadas.
"""

from __future__ import annotations

from typing import Final

# --- ASME B16.5: ratings clase 150 y 300 (bar manométricos) ---------------------------
# Las clases 600 a 2500 se obtienen proporcionalmente de la clase 300 (factores 2, 3, 5
# y 25/3), que es como B16.5 construye sus tablas a partir del índice de clase.
FLANGE_TEMPS_C: Final = (38, 50, 100, 150, 200, 250, 300, 325, 350, 375, 400, 425, 450,
                         475, 500, 538)
FLANGE_RATINGS: Final[dict[str, dict[int, tuple[float, ...]]]] = {
    "1.1": {
        150: (19.6, 19.2, 17.7, 15.8, 13.8, 12.1, 10.2, 9.3, 8.4, 7.4, 6.5, 5.5, 4.6, 3.7,
              2.8, 1.4),
        300: (51.1, 50.1, 46.6, 45.1, 43.8, 41.9, 39.8, 38.7, 37.6, 36.4, 34.7, 28.8, 23.0,
              17.4, 11.8, 5.9),
    },
    "2.1": {
        150: (19.0, 18.3, 15.7, 14.2, 13.2, 12.1, 10.2, 9.3, 8.4, 7.4, 6.5, 5.5, 4.6, 3.7,
              2.8, 1.4),
        300: (49.6, 47.8, 40.9, 37.0, 34.5, 32.5, 30.9, 30.2, 29.6, 29.0, 28.4, 28.0, 27.4,
              26.9, 26.5, 24.4),
    },
    "2.2": {
        150: (19.0, 18.4, 16.2, 14.8, 13.7, 12.1, 10.2, 9.3, 8.4, 7.4, 6.5, 5.5, 4.6, 3.7,
              2.8, 1.4),
        300: (49.6, 48.1, 42.2, 38.5, 35.7, 33.4, 31.6, 30.9, 30.3, 29.9, 29.4, 29.1, 28.8,
              28.7, 28.2, 25.2),
    },
}
CLASS_FACTORS_FROM_300: Final = {600: 2.0, 900: 3.0, 1500: 5.0, 2500: 25.0 / 3.0}
FLANGE_SOURCE: Final = "public-compilation-b16.5"

# --- ASME B36.10M / B36.19M: diámetro exterior y espesores (pulgadas) ---------------
# Compilación de tablas públicas de cañerías; valores «a verificar» contra la norma.
# Los schedules con sufijo S son de ASME B36.19M (inoxidable).
PIPE_OD_IN: Final = {
    "1/8": 0.405, "1/4": 0.540, "3/8": 0.675, "1/2": 0.840, "3/4": 1.050, "1": 1.315,
    "1-1/4": 1.660, "1-1/2": 1.900, "2": 2.375, "2-1/2": 2.875, "3": 3.500, "3-1/2": 4.000,
    "4": 4.500, "5": 5.563, "6": 6.625, "8": 8.625, "10": 10.750, "12": 12.750,
    "14": 14.000, "16": 16.000, "18": 18.000, "20": 20.000, "22": 22.000, "24": 24.000,
    "26": 26.000, "28": 28.000, "30": 30.000, "32": 32.000, "34": 34.000, "36": 36.000,
    "42": 42.000, "48": 48.000,
}
PIPE_DN: Final = {
    "1/8": 6, "1/4": 8, "3/8": 10, "1/2": 15, "3/4": 20, "1": 25, "1-1/4": 32, "1-1/2": 40,
    "2": 50, "2-1/2": 65, "3": 80, "3-1/2": 90, "4": 100, "5": 125, "6": 150, "8": 200,
    "10": 250, "12": 300, "14": 350, "16": 400, "18": 450, "20": 500, "22": 550, "24": 600,
    "26": 650, "28": 700, "30": 750, "32": 800, "34": 850, "36": 900, "42": 1050, "48": 1200,
}


def _row(sizes: str, walls: str) -> dict[str, float]:
    return dict(zip(sizes.split(), (float(w) for w in walls.split()), strict=True))


_SMALL = "1/8 1/4 3/8 1/2 3/4 1 1-1/4 1-1/2 2 2-1/2 3 3-1/2 4 5 6 8 10"
_LARGE_STD = "12 14 16 18 20 22 24 26 28 30 32 34 36 42 48"
_SCH40_SMALL = (".068 .088 .091 .109 .113 .133 .140 .145 .154 .203 .216 .226 .237 .258 .280 "
                ".322 .365")
_SCH80_SMALL = ".095 .119 .126 .147 .154 .179 .191 .200 .218 .276 .300 .318 .337 .375 .432 .500"

PIPE_WALL_IN: Final[dict[str, dict[str, float]]] = {
    "5S": _row("1/2 3/4 1 1-1/4 1-1/2 2 2-1/2 3 3-1/2 4 5 6 8 10 12 14 16 18 20 22 24 30",
               ".065 .065 .065 .065 .065 .065 .083 .083 .083 .083 .109 .109 .109 .134 .156 "
               ".156 .165 .165 .188 .188 .218 .250"),
    "10S": _row("1/8 1/4 3/8 1/2 3/4 1 1-1/4 1-1/2 2 2-1/2 3 3-1/2 4 5 6 8 10 12 14 16 18 "
                "20 22 24 30",
                ".049 .065 .065 .083 .083 .109 .109 .109 .109 .120 .120 .120 .120 .134 .134 "
                ".148 .165 .180 .188 .188 .188 .218 .218 .250 .312"),
    "10": _row("14 16 18 20 22 24 26 28 30 32 34 36",
               ".250 .250 .250 .250 .250 .250 .312 .312 .312 .312 .344 .312"),
    "20": _row("8 10 12 14 16 18 20 22 24 26 28 30 32 34 36",
               ".250 .250 .250 .312 .312 .312 .375 .375 .375 .500 .500 .500 .500 .500 .500"),
    "30": _row("8 10 12 14 16 18 20 22 24 28 30 32 34 36",
               ".277 .307 .330 .375 .375 .438 .500 .500 .562 .625 .625 .625 .625 .625"),
    "40": _row(_SMALL + " 12 14 16 18 20 24 32 34 36",
               _SCH40_SMALL + " .406 .438 .500 .562 .594 .688 .688 .688 .750"),
    "40S": _row(_SMALL + " 12 14 16 18 20 22 24",
                _SCH40_SMALL + " .375 .375 .375 .375 .375 .375 .375"),
    "STD": _row(_SMALL + " " + _LARGE_STD, _SCH40_SMALL + " .375" * 15),
    "60": _row("8 10 12 14 16 18 20 22 24",
               ".406 .500 .562 .594 .656 .750 .812 .875 .969"),
    "80": _row(_SMALL.removesuffix(" 10") + " 10 12 14 16 18 20 22 24",
               _SCH80_SMALL + " .594 .688 .750 .844 .938 1.031 1.125 1.219"),
    "80S": _row(_SMALL + " 12 14 16 18 20 22 24",
                _SCH80_SMALL + " .500 .500 .500 .500 .500 .500 .500 .500"),
    "XS": _row(_SMALL + " " + _LARGE_STD, _SCH80_SMALL + " .500" * 16),
    "100": _row("8 10 12 14 16 18 20 22 24",
                ".594 .719 .844 .938 1.031 1.156 1.281 1.375 1.531"),
    "120": _row("4 5 6 8 10 12 14 16 18 20 22 24",
                ".438 .500 .562 .719 .844 1.000 1.094 1.219 1.375 1.500 1.625 1.812"),
    "140": _row("8 10 12 14 16 18 20 22 24",
                ".812 1.000 1.125 1.250 1.438 1.562 1.750 1.875 2.062"),
    "160": _row("1/2 3/4 1 1-1/4 1-1/2 2 2-1/2 3 4 5 6 8 10 12 14 16 18 20 22 24",
                ".188 .219 .250 .250 .281 .344 .375 .438 .531 .625 .719 .906 1.125 1.312 "
                "1.406 1.594 1.781 1.969 2.125 2.344"),
    "XXS": _row("1/2 3/4 1 1-1/4 1-1/2 2 2-1/2 3 4 5 6 8 10 12",
                ".294 .308 .358 .382 .400 .436 .552 .600 .674 .750 .864 .875 1.000 1.000"),
}

# --- Fluidos -------------------------------------------------------------------------
# (id, nombre ES, nombre EN, nombre CoolProp, fase por defecto)
FLUIDS: Final[tuple[tuple[str, str, str, str | None, str], ...]] = (
    ("water", "Agua / vapor de agua", "Water / steam", "Water", "liquid"),
    ("air", "Aire", "Air", "Air", "gas"),
    ("nitrogen", "Nitrógeno", "Nitrogen", "Nitrogen", "gas"),
    ("oxygen", "Oxígeno", "Oxygen", "Oxygen", "gas"),
    ("hydrogen", "Hidrógeno", "Hydrogen", "Hydrogen", "gas"),
    ("methane", "Metano", "Methane", "Methane", "gas"),
    ("ethane", "Etano", "Ethane", "Ethane", "gas"),
    ("propane", "Propano", "Propane", "n-Propane", "gas"),
    ("nbutane", "n-Butano", "n-Butane", "n-Butane", "gas"),
    ("isobutane", "Isobutano", "Isobutane", "IsoButane", "gas"),
    ("ethylene", "Etileno", "Ethylene", "Ethylene", "gas"),
    ("propylene", "Propileno", "Propylene", "Propylene", "gas"),
    ("co2", "Dióxido de carbono", "Carbon dioxide", "CarbonDioxide", "gas"),
    ("co", "Monóxido de carbono", "Carbon monoxide", "CarbonMonoxide", "gas"),
    ("ammonia", "Amoníaco", "Ammonia", "Ammonia", "gas"),
    ("h2s", "Sulfuro de hidrógeno", "Hydrogen sulfide", "HydrogenSulfide", "gas"),
    ("so2", "Dióxido de azufre", "Sulfur dioxide", "SulfurDioxide", "gas"),
    ("helium", "Helio", "Helium", "Helium", "gas"),
    ("argon", "Argón", "Argon", "Argon", "gas"),
    ("nhexane", "n-Hexano", "n-Hexane", "n-Hexane", "liquid"),
    ("nheptane", "n-Heptano", "n-Heptane", "n-Heptane", "liquid"),
    ("benzene", "Benceno", "Benzene", "Benzene", "liquid"),
    ("toluene", "Tolueno", "Toluene", "Toluene", "liquid"),
    ("methanol", "Metanol", "Methanol", "Methanol", "liquid"),
    ("ethanol", "Etanol", "Ethanol", "Ethanol", "liquid"),
    ("acetone", "Acetona", "Acetone", "Acetone", "liquid"),
    ("r134a", "Refrigerante R-134a", "Refrigerant R-134a", "R134a", "gas"),
    ("natural_gas", "Gas natural típico (90 % CH₄)", "Typical natural gas (90 % CH₄)",
     "HEOS::Methane[0.90]&Ethane[0.06]&Propane[0.04]", "gas"),
    ("crude_api30", "Petróleo crudo API 30", "Crude oil API 30", None, "liquid"),
    ("diesel", "Gasoil / diésel", "Diesel", None, "liquid"),
    ("glycol50", "Agua-etilenglicol 50 %", "Water-ethylene glycol 50 %", None, "liquid"),
)

# Propiedades tabuladas (aproximadas) de los fluidos sin modelo en CoolProp:
# id -> [(T °C, ρ kg/m³, μ mPa·s)] a presión moderada.
TABULATED_FLUIDS: Final[dict[str, tuple[tuple[float, float, float], ...]]] = {
    "crude_api30": ((15, 876, 12.0), (40, 860, 6.0), (80, 833, 2.6), (150, 786, 0.9)),
    "diesel": ((15, 840, 4.0), (40, 824, 2.4), (80, 797, 1.3), (150, 750, 0.6)),
    "glycol50": ((0, 1082, 7.5), (20, 1071, 3.8), (60, 1050, 1.3), (100, 1023, 0.6)),
}

# --- Sensores ------------------------------------------------------------------------
# (id, tipo, diámetro de vaina mm, temperatura máxima °C)
SENSORS: Final = (
    ("PT100_3", "rtd_pt100", 3.0, 600), ("PT100_4.5", "rtd_pt100", 4.5, 600),
    ("PT100_6", "rtd_pt100", 6.0, 600), ("PT100_8", "rtd_pt100", 8.0, 600),
    ("TCK_3", "tc_k", 3.0, 1100), ("TCK_6", "tc_k", 6.0, 1200), ("TCK_8", "tc_k", 8.0, 1200),
    ("TCJ_6", "tc_j", 6.0, 750), ("TCT_6", "tc_t", 6.0, 350), ("TCE_6", "tc_e", 6.0, 900),
    ("TCN_6", "tc_n", 6.0, 1200), ("TCS_6", "tc_s", 6.0, 1600), ("TCR_6", "tc_r", 6.0, 1600),
)
SENSOR_DENSITY: Final = 2700.0

# --- Compatibilidad química orientativa (A recomendado, B aceptable, C no recomendado)
AGENTS: Final = ("chlorides", "seawater", "h2s_wet", "co2_wet", "hcl", "h2so4_dil",
                 "hno3", "naoh", "nh3", "hf", "organic_acids")
COMPATIBILITY: Final[dict[str, str]] = {
    # material: ratings en el orden de AGENTS
    "A105": "CCBCCCCBACC",
    "F11": "CCBCCCCBACC",
    "F22": "CCBBCCCBACC",
    "F91": "CCBBCCCBACC",
    "SS304": "CCBACBABACB",
    "SS316": "BCBACBABACA",
    "SS321": "CCBACBABACB",
    "SS347": "CCBACBABACB",
    "D2205": "ABAACBAAACA",
    "SD2507": "AAAABBAAACA",
    "N06600": "BBBACCBAABA",
    "N06625": "AAAABBAAABA",
    "N10276": "AAAAAAAABAA",
    "N04400": "BACBCBCACAB",
    "TI2": "AAAACCABACA",
    "TA": "AAAAAAAACCA",
}
