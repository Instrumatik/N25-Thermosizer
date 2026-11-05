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

# --- ASME B36.10M: diámetro exterior y espesores (pulgadas) --------------------------
PIPE_OD_IN: Final = {
    "1/2": 0.840, "3/4": 1.050, "1": 1.315, "1-1/2": 1.900, "2": 2.375, "3": 3.500,
    "4": 4.500, "6": 6.625, "8": 8.625, "10": 10.750, "12": 12.750, "14": 14.000,
    "16": 16.000, "18": 18.000, "20": 20.000, "24": 24.000,
}
PIPE_DN: Final = {
    "1/2": 15, "3/4": 20, "1": 25, "1-1/2": 40, "2": 50, "3": 80, "4": 100, "6": 150,
    "8": 200, "10": 250, "12": 300, "14": 350, "16": 400, "18": 450, "20": 500, "24": 600,
}
PIPE_WALL_IN: Final[dict[str, dict[str, float]]] = {
    "40": {"1/2": .109, "3/4": .113, "1": .133, "1-1/2": .145, "2": .154, "3": .216,
           "4": .237, "6": .280, "8": .322, "10": .365, "12": .406, "14": .438, "16": .500,
           "18": .562, "20": .594, "24": .688},
    "80": {"1/2": .147, "3/4": .154, "1": .179, "1-1/2": .200, "2": .218, "3": .300,
           "4": .337, "6": .432, "8": .500, "10": .594, "12": .688, "14": .750, "16": .844,
           "18": .938, "20": 1.031, "24": 1.219},
    "160": {"1/2": .188, "3/4": .219, "1": .250, "1-1/2": .281, "2": .344, "3": .438,
            "4": .531, "6": .719, "8": .906, "10": 1.125, "12": 1.312, "14": 1.406,
            "16": 1.594, "18": 1.781, "20": 1.969, "24": 2.344},
    "STD": {"1/2": .109, "3/4": .113, "1": .133, "1-1/2": .145, "2": .154, "3": .216,
            "4": .237, "6": .280, "8": .322, "10": .365, "12": .375, "14": .375, "16": .375,
            "18": .375, "20": .375, "24": .375},
    "XS": {"1/2": .147, "3/4": .154, "1": .179, "1-1/2": .200, "2": .218, "3": .300,
           "4": .337, "6": .432, "8": .500, "10": .500, "12": .500, "14": .500, "16": .500,
           "18": .500, "20": .500, "24": .500},
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
