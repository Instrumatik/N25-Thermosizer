"""Modelo de datos del cálculo de un termopozo.

Todos los campos numéricos están en **SI coherente** (m, kg, s, Pa absolutos, K),
según la política de :mod:`thermowell_sizer.core.units`. Los modelos son inmutables
(``frozen``): una modificación produce un objeto nuevo, lo que simplifica deshacer,
rehacer y el autoguardado.

Los nombres de los atributos siguen la nomenclatura de ASME PTC 19.3 TW-2016,
sección 2 (A, B, d, L, t, b, Ls, bs...), para que el código se lea junto a la norma.
"""

from __future__ import annotations

import math
from enum import StrEnum
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

# --- Tipos con restricciones ---------------------------------------------------------
Positive = Annotated[float, Field(gt=0.0)]
NonNegative = Annotated[float, Field(ge=0.0)]
AbsTemperature = Annotated[float, Field(gt=0.0, description="Temperatura absoluta, K")]
AbsPressure = Annotated[float, Field(ge=0.0, description="Presión absoluta, Pa")]


class _Model(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", validate_assignment=True)


# --- Enumeraciones -------------------------------------------------------------------
class Phase(StrEnum):
    """Fase del fluido de proceso."""

    LIQUID = "liquid"
    GAS = "gas"
    STEAM = "steam"
    TWO_PHASE = "two_phase"


class PropertySource(StrEnum):
    """Origen de las propiedades del fluido (se informa en la memoria)."""

    COOLPROP = "coolprop"
    LIBRARY = "library"
    USER = "user"


class FlowBasis(StrEnum):
    """Forma en que el usuario especificó el flujo."""

    MASS_FLOW = "mass_flow"
    VOLUME_FLOW = "volume_flow"
    VELOCITY = "velocity"


class ShankProfile(StrEnum):
    """Perfil del vástago (ASME PTC 19.3 TW-2016, figs. 4-1-2 a 4-1-4)."""

    STRAIGHT = "straight"
    TAPERED = "tapered"
    STEPPED = "stepped"


class Construction(StrEnum):
    """Construcción del termopozo. Solo ``BAR_STOCK`` está dentro del alcance (párr. 1-2)."""

    BAR_STOCK = "bar_stock"
    FABRICATED = "fabricated"


class ConnectionType(StrEnum):
    """Conexión a proceso."""

    THREADED = "threaded"
    FLANGED = "flanged"
    SOCKET_WELD = "socket_weld"
    WELD_IN = "weld_in"
    VAN_STONE = "van_stone"
    SANITARY = "sanitary"


class FlangeFace(StrEnum):
    """Cara de la brida."""

    RF = "RF"
    RTJ = "RTJ"
    FF = "FF"


class MountingOrientation(StrEnum):
    """Orientación de montaje respecto de la tubería."""

    PERPENDICULAR = "perpendicular"
    ANGLED = "angled"
    ELBOW_TIP_UPSTREAM = "elbow_tip_upstream"
    ELBOW_TIP_DOWNSTREAM = "elbow_tip_downstream"


class SensorType(StrEnum):
    """Tipo de sensor alojado en el termopozo."""

    RTD_PT100 = "rtd_pt100"
    RTD_PT1000 = "rtd_pt1000"
    TC_K = "tc_k"
    TC_J = "tc_j"
    TC_T = "tc_t"
    TC_E = "tc_e"
    TC_N = "tc_n"
    TC_R = "tc_r"
    TC_S = "tc_s"
    TC_B = "tc_b"
    BIMETALLIC = "bimetallic"


class FatigueClass(StrEnum):
    """Clase de material para el límite de fatiga (ASME PTC 19.3 TW-2016, tabla 6-12.3-1)."""

    A = "A"
    B = "B"


# --- 1. Identificación ---------------------------------------------------------------
class Identification(_Model):
    """Datos de identificación del punto de medición."""

    tag: str = Field(min_length=1, max_length=64)
    service: str = ""
    line_or_equipment: str = ""
    pid: str = ""
    location: str = ""


# --- 2. Proceso ----------------------------------------------------------------------
class FlowCase(_Model):
    """Un caso de flujo (mínimo, normal o máximo). Solo se usa el campo de ``basis``."""

    label: str = Field(description="min | normal | max | personalizado")
    basis: FlowBasis
    mass_flow: NonNegative | None = Field(default=None, description="kg/s")
    volume_flow: NonNegative | None = Field(default=None, description="m³/s")
    velocity: NonNegative | None = Field(default=None, description="m/s")

    @model_validator(mode="after")
    def _value_for_basis(self) -> Self:
        if getattr(self, self.basis.value) is None:
            raise ValueError(f"Falta el valor de '{self.basis.value}' para el caso '{self.label}'")
        return self


class FluidProperties(_Model):
    """Propiedades del fluido a las condiciones de operación."""

    density: Positive = Field(description="ρ, kg/m³")
    dynamic_viscosity: Positive = Field(description="μ, Pa·s")
    source: PropertySource
    source_note: str = Field(default="", description="p. ej. 'CoolProp 6.6, HEOS::Water'")


class CorrosionData(_Model):
    """Agentes corrosivos y condiciones de servicio agresivo."""

    h2s_partial_pressure: NonNegative = Field(default=0.0, description="Pa absolutos")
    chlorides_ppm: NonNegative = 0.0
    ph: float | None = Field(default=None, ge=0.0, le=14.0)
    co2_partial_pressure: NonNegative = Field(default=0.0, description="Pa absolutos")
    solids_or_erosive: bool = False
    nace_service: bool = False


class ProcessConditions(_Model):
    """Condiciones de proceso del punto."""

    fluid_id: str = Field(description="Id. de la biblioteca o 'custom:<nombre>'")
    phase: Phase
    operating_pressure: AbsPressure
    design_pressure: AbsPressure
    operating_temperature: AbsTemperature
    design_temperature: AbsTemperature
    flow_cases: tuple[FlowCase, ...] = Field(min_length=1)
    properties: FluidProperties
    corrosion: CorrosionData = CorrosionData()

    @model_validator(mode="after")
    def _design_envelopes_operation(self) -> Self:
        if self.design_pressure < self.operating_pressure:
            raise ValueError("La presión de diseño no puede ser menor que la de operación")
        if self.design_temperature < self.operating_temperature:
            raise ValueError("La temperatura de diseño no puede ser menor que la de operación")
        return self


# --- 3. Tubería / equipo -------------------------------------------------------------
class PipeData(_Model):
    """Tubería o equipo donde se instala el termopozo."""

    nominal_size: str = Field(description="p. ej. 'NPS 6' o 'DN 150'")
    schedule: str = ""
    inner_diameter: Positive = Field(description="m")
    material_id: str = ""
    orientation: MountingOrientation = MountingOrientation.PERPENDICULAR
    insulation_thickness: NonNegative = Field(default=0.0, description="m")
    nozzle_length: NonNegative = Field(default=0.0, description="Longitud de tobera o niple, m")


# --- 4. Termopozo --------------------------------------------------------------------
class ProcessConnection(_Model):
    """Conexión a proceso del termopozo."""

    type: ConnectionType
    size: str = Field(default="", description="p. ej. '1-1/2 in' o '3/4 NPT'")
    rating_class: int | None = Field(default=None, description="Clase ASME B16.5: 150...2500")
    face: FlangeFace | None = None

    @model_validator(mode="after")
    def _flange_fields(self) -> Self:
        flanged = self.type in (ConnectionType.FLANGED, ConnectionType.VAN_STONE)
        if flanged and self.rating_class is None:
            raise ValueError("Una conexión bridada requiere la clase de presión")
        return self


class ThermowellGeometry(_Model):
    """Geometría del termopozo (ASME PTC 19.3 TW-2016, fig. 4-1-1 y sección 2).

    Attributes:
        profile: perfil del vástago.
        L: longitud no soportada, de la punta al plano de soporte, m.
        A: diámetro exterior en la raíz o el plano de soporte, m.
        B: diámetro exterior en la punta, m.
        d: diámetro del agujero (bore), m.
        t: espesor mínimo de la punta, m.
        b: radio de acuerdo en la raíz del vástago, m.
        Ls: longitud del tramo de diámetro reducido (solo escalonado), m.
        bs: radio de acuerdo en el escalón (solo escalonado), m.
        U: longitud de inserción, para la hoja de datos, m.
        T_lag: longitud de lag (extensión), m.
        L0: longitud del vástago protegida del flujo (dentro de la tobera), m.
        surface_finish_ra: rugosidad Ra, m.
        corrosion_allowance: sobreespesor de corrosión c, m.

    """

    profile: ShankProfile
    construction: Construction = Construction.BAR_STOCK
    L: Positive
    A: Positive
    B: Positive
    d: Positive
    t: Positive
    b: NonNegative = 0.0
    Ls: NonNegative = 0.0
    bs: NonNegative = 0.0
    U: Positive | None = None
    T_lag: NonNegative = 0.0
    L0: NonNegative = 0.0
    surface_finish_ra: Positive = Field(default=0.81e-6, description="m; 0,81 µm = 32 µin")
    corrosion_allowance: NonNegative = 0.0

    @model_validator(mode="after")
    def _consistency(self) -> Self:
        # Solo coherencia geométrica básica; los límites de la norma están en validation.py
        if self.d >= self.B:
            raise ValueError("El diámetro del agujero d debe ser menor que el de punta B")
        if self.B > self.A:
            raise ValueError("El diámetro de punta B no puede superar el de raíz A")
        if self.profile is ShankProfile.STRAIGHT and not math.isclose(self.A, self.B):
            raise ValueError("En un perfil recto A debe ser igual a B")
        if self.profile is ShankProfile.STEPPED and not 0.0 < self.Ls < self.L:
            raise ValueError("En un perfil escalonado se requiere 0 < Ls < L")
        if self.L0 >= self.L:
            raise ValueError("La longitud protegida L0 debe ser menor que L")
        return self


class MaterialRef(_Model):
    """Referencia al material del termopozo en la biblioteca."""

    material_id: str = Field(description="p. ej. 'SS316' o 'A105'")
    coating: str = ""


class Thermowell(_Model):
    """Termopozo completo: geometría, material y conexión."""

    geometry: ThermowellGeometry
    material: MaterialRef
    connection: ProcessConnection


# --- 5. Sensor -----------------------------------------------------------------------
class SensorSpec(_Model):
    """Sensor alojado (influye en Ha,s, factor de masa del sensor)."""

    type: SensorType
    sheath_diameter: Positive = Field(description="m")
    mass: NonNegative | None = Field(default=None, description="kg; None = estimar")
    density: Positive | None = Field(
        default=None, description="ρs, densidad media del sensor, kg/m³"
    )
    spring_loaded: bool = True


# --- Entrada completa del cálculo -----------------------------------------------------
class CalcInput(_Model):
    """Todo lo necesario para verificar un tag."""

    identification: Identification
    process: ProcessConditions
    pipe: PipeData
    thermowell: Thermowell
    sensor: SensorSpec


# --- Resultado -----------------------------------------------------------------------
class CheckStatus(StrEnum):
    """Estado de un criterio (semáforo)."""

    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"
    NOT_APPLICABLE = "n/a"


class CheckResult(_Model):
    """Resultado de un criterio de verificación con su margen."""

    criterion_id: str = Field(description="p. ej. 'frequency_limit', 'dynamic_stress_root'")
    flow_case: str = ""
    status: CheckStatus
    value: float
    limit: float
    margin_pct: float = Field(description="(límite − valor)/límite × 100; negativo = no cumple")
    reference: str
    message_key: str
