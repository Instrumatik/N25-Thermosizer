"""Propiedades de fluidos con CoolProp y caída a la biblioteca local."""

from __future__ import annotations

from dataclasses import dataclass

from thermowell_sizer.core.models import FluidProperties, Phase, PropertySource
from thermowell_sizer.data.database import Library

try:  # CoolProp es dependencia obligatoria, pero se degrada con elegancia si falta.
    import CoolProp
    from CoolProp.CoolProp import PropsSI

    COOLPROP_VERSION: str | None = str(CoolProp.__version__)
except ImportError:  # pragma: no cover - entorno sin CoolProp
    COOLPROP_VERSION = None


class FluidPropertyError(ValueError):
    """No se pudieron obtener propiedades para el fluido y estado pedidos."""


@dataclass(frozen=True, slots=True)
class FluidState:
    """Propiedades más la fase detectada y datos auxiliares para la interfaz."""

    properties: FluidProperties
    phase: Phase
    compressibility: float | None = None
    saturation_temperature: float | None = None


def _coolprop_phase(fluid: str, temperature: float, pressure: float) -> Phase:
    index = PropsSI("Phase", "T", temperature, "P", pressure, fluid)
    liquid = {CoolProp.iphase_liquid}
    two_phase = {CoolProp.iphase_twophase}
    if index in two_phase:
        return Phase.TWO_PHASE
    if index in liquid:
        return Phase.LIQUID
    return Phase.STEAM if fluid.endswith("Water") else Phase.GAS


def fluid_state(
    library: Library, fluid_id: str, temperature: float, pressure: float
) -> FluidState:
    """Calcula ρ y μ del fluido a T (K) y P (Pa absolutos).

    Raises:
        FluidPropertyError: si no hay modelo ni tabla, o el estado es inválido.
    """
    try:
        info = library.fluid(fluid_id)
    except KeyError as exc:
        raise FluidPropertyError(f"Fluido desconocido: {fluid_id}") from exc

    if info.coolprop_name and COOLPROP_VERSION is not None:
        name = info.coolprop_name
        try:
            rho = float(PropsSI("D", "T", temperature, "P", pressure, name))
            mu = float(PropsSI("V", "T", temperature, "P", pressure, name))
            z = float(PropsSI("Z", "T", temperature, "P", pressure, name))
            try:
                phase = _coolprop_phase(name, temperature, pressure)
            except ValueError:  # mezclas: la fase no siempre está disponible
                phase = Phase(info.default_phase)
            try:
                t_sat: float | None = float(PropsSI("T", "P", pressure, "Q", 0, name))
            except ValueError:
                t_sat = None
        except ValueError as exc:
            raise FluidPropertyError(str(exc)) from exc
        props = FluidProperties(
            density=rho,
            dynamic_viscosity=mu,
            source=PropertySource.COOLPROP,
            source_note=f"CoolProp {COOLPROP_VERSION}, {name}",
        )
        return FluidState(props, phase, z, t_sat)

    tab = library.tabulated_fluid(fluid_id, temperature)
    if tab is None:
        raise FluidPropertyError(f"Sin datos para {fluid_id}")
    rho, mu = tab
    props = FluidProperties(
        density=rho,
        dynamic_viscosity=mu,
        source=PropertySource.USER if info.user_defined else PropertySource.LIBRARY,
        source_note=f"Tabla de biblioteca ({info.name_es}), interpolada en T",
    )
    return FluidState(props, Phase(info.default_phase))


def gas_density(
    temperature: float, pressure: float, molar_mass: float, compressibility: float = 1.0
) -> float:
    """Densidad de un gas real ρ = P·M / (Z·R·T) (P en Pa abs, M en kg/mol)."""
    gas_constant = 8.314_462_618  # J/(mol·K), CODATA 2018 exacto
    return pressure * molar_mass / (compressibility * gas_constant * temperature)


GENERIC_THERMAL = {"liquid": (0.6, 4180.0), "gas": (0.03, 1100.0), "steam": (0.05, 2100.0),
                   "two_phase": (0.6, 4180.0)}
"""(k W/m·K, cp J/kg·K) genéricos cuando no hay modelo del fluido."""


def thermal_properties(
    library: Library, fluid_id: str, temperature: float, pressure: float, phase: Phase
) -> tuple[float, float, bool]:
    """Conductividad y calor específico del fluido.

    Returns:
        (k, cp, es_genérico): el último indica que se usaron valores típicos de la fase.
    """
    try:
        name = library.fluid(fluid_id).coolprop_name
    except KeyError:
        name = None
    if name and COOLPROP_VERSION is not None:
        try:
            k = float(PropsSI("L", "T", temperature, "P", pressure, name))
            cp = float(PropsSI("C", "T", temperature, "P", pressure, name))
            if k > 0 and cp > 0:
                return k, cp, False
        except ValueError:
            pass
    k, cp = GENERIC_THERMAL[phase.value]
    return k, cp, True
