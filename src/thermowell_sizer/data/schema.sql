-- Esquema de la base local de ThermoWell Sizer (SQLite).
-- Todas las magnitudes en SI coherente: m, kg, s, Pa absolutos, K.
-- Cada dato técnico lleva su fuente (source_id) para la trazabilidad de la memoria.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- Fuentes bibliográficas citadas por los datos.
CREATE TABLE IF NOT EXISTS source (
    id        TEXT PRIMARY KEY,           -- p. ej. 'ASME-PTC19.3TW-2016-T6-12.3-1'
    citation  TEXT NOT NULL,
    note      TEXT NOT NULL DEFAULT '',
    verified  INTEGER NOT NULL DEFAULT 0  -- 0 = "a verificar" contra la fuente primaria
);

-- Materiales -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS material (
    id                TEXT PRIMARY KEY,   -- 'SS316', 'A105', 'F91'...
    name              TEXT NOT NULL,
    spec              TEXT NOT NULL,      -- 'ASTM A182 F316/F316L'
    uns               TEXT NOT NULL DEFAULT '',
    family            TEXT NOT NULL,      -- carbon, low_alloy, austenitic, duplex, nickel, ...
    fatigue_class     TEXT NOT NULL CHECK (fatigue_class IN ('A', 'B')),
    fatigue_covered   INTEGER NOT NULL DEFAULT 1, -- figura en la tabla 6-12.3-1
    e_ref             REAL NOT NULL,      -- E_ref para F_T, Pa
    scc_chlorides     INTEGER NOT NULL DEFAULT 0,
    notes_es          TEXT NOT NULL DEFAULT '',
    notes_en          TEXT NOT NULL DEFAULT '',
    max_temperature   REAL NOT NULL,      -- K
    min_temperature   REAL,               -- K
    density           REAL NOT NULL,      -- kg/m³ a temperatura ambiente
    nace_ok           INTEGER NOT NULL DEFAULT 0,
    b16_5_group       TEXT,               -- grupo de material ASME B16.5 (p. ej. '2.2')
    user_defined      INTEGER NOT NULL DEFAULT 0,
    source_id         TEXT REFERENCES source(id)
);

-- Propiedades en función de la temperatura (se interpolan linealmente).
CREATE TABLE IF NOT EXISTS material_property_point (
    material_id  TEXT NOT NULL REFERENCES material(id) ON DELETE CASCADE,
    property     TEXT NOT NULL CHECK (property IN
                   ('elastic_modulus', 'allowable_stress', 'yield_strength',
                    'tensile_strength', 'thermal_expansion', 'thermal_conductivity')),
    temperature  REAL NOT NULL,           -- K
    value        REAL NOT NULL,           -- SI
    source_id    TEXT REFERENCES source(id),
    PRIMARY KEY (material_id, property, temperature)
);

CREATE TABLE IF NOT EXISTS coating (
    id               TEXT PRIMARY KEY,
    name_es          TEXT NOT NULL,
    name_en          TEXT NOT NULL,
    purpose          TEXT NOT NULL,       -- erosion | corrosion
    max_temperature  REAL NOT NULL        -- K
);

-- Fluidos ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fluid (
    id              TEXT PRIMARY KEY,     -- 'water', 'methane', 'custom:crudo_api_30'
    name_es         TEXT NOT NULL,
    name_en         TEXT NOT NULL,
    coolprop_name   TEXT,                 -- NULL si CoolProp no lo soporta
    default_phase   TEXT NOT NULL,
    user_defined    INTEGER NOT NULL DEFAULT 0,
    source_id       TEXT REFERENCES source(id)
);

-- Propiedades tabuladas para fluidos que CoolProp no cubre.
CREATE TABLE IF NOT EXISTS fluid_property_point (
    fluid_id           TEXT NOT NULL REFERENCES fluid(id) ON DELETE CASCADE,
    temperature        REAL NOT NULL,     -- K
    pressure           REAL NOT NULL,     -- Pa abs
    density            REAL NOT NULL,     -- kg/m³
    dynamic_viscosity  REAL NOT NULL,     -- Pa·s
    PRIMARY KEY (fluid_id, temperature, pressure)
);

-- Bridas ASME B16.5: presión-temperatura por grupo de material y clase -----------------
CREATE TABLE IF NOT EXISTS flange_rating (
    material_group  TEXT NOT NULL,
    class           INTEGER NOT NULL,
    temperature     REAL NOT NULL,        -- K
    pressure        REAL NOT NULL,        -- Pa manométricos (así los tabula B16.5)
    source_id       TEXT REFERENCES source(id),
    PRIMARY KEY (material_group, class, temperature)
);

-- Tuberías ASME B36.10M / B36.19M -----------------------------------------------------
CREATE TABLE IF NOT EXISTS pipe_size (
    nps             TEXT NOT NULL,
    dn              INTEGER NOT NULL,
    schedule        TEXT NOT NULL,
    outer_diameter  REAL NOT NULL,        -- m
    wall_thickness  REAL NOT NULL,        -- m
    PRIMARY KEY (nps, schedule)
);

-- Sensores -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sensor_model (
    id               TEXT PRIMARY KEY,
    type             TEXT NOT NULL,
    sheath_diameter  REAL NOT NULL,       -- m
    mass_per_length  REAL,                -- kg/m
    density          REAL,                -- kg/m³
    max_temperature  REAL                 -- K
);

-- Compatibilidad química (A = recomendado, B = aceptable, C = no recomendado) ----------
CREATE TABLE IF NOT EXISTS chemical_compatibility (
    material_id  TEXT NOT NULL REFERENCES material(id) ON DELETE CASCADE,
    agent        TEXT NOT NULL,
    rating       TEXT NOT NULL CHECK (rating IN ('A', 'B', 'C', 'N/D')),
    max_temperature REAL,                 -- K
    note         TEXT NOT NULL DEFAULT '',
    source_id    TEXT REFERENCES source(id),
    PRIMARY KEY (material_id, agent)
);

-- Biblioteca: glosario y fichas de normas (texto propio, nunca copiado de las normas) --
CREATE TABLE IF NOT EXISTS glossary_term (
    id            TEXT PRIMARY KEY,
    term_es       TEXT NOT NULL,
    term_en       TEXT NOT NULL,
    definition_es TEXT NOT NULL,
    definition_en TEXT NOT NULL,
    formula       TEXT NOT NULL DEFAULT '',   -- LaTeX
    example_es    TEXT NOT NULL DEFAULT '',
    example_en    TEXT NOT NULL DEFAULT '',
    diagram       TEXT NOT NULL DEFAULT ''    -- nombre de recurso SVG
);

CREATE TABLE IF NOT EXISTS standard_summary (
    id          TEXT PRIMARY KEY,         -- 'ASME-PTC-19.3-TW-2016'
    title       TEXT NOT NULL,
    edition     TEXT NOT NULL,
    summary_es  TEXT NOT NULL,
    summary_en  TEXT NOT NULL,
    url         TEXT NOT NULL DEFAULT ''
);

-- Índice de búsqueda global con tolerancia a errores (se complementa con fuzzy en Python).
CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(
    kind, ref_id, title, body, tokenize = 'unicode61 remove_diacritics 2'
);
