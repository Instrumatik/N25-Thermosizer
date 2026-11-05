"""Datos de prueba compartidos (valores ilustrativos, no tomados de la norma)."""

from __future__ import annotations

import pytest

from thermowell_sizer.core.models import (
    CalcInput,
    ConnectionType,
    FlangeFace,
    FlowBasis,
    FlowCase,
    FluidProperties,
    Identification,
    MaterialRef,
    Phase,
    PipeData,
    ProcessConditions,
    ProcessConnection,
    PropertySource,
    SensorSpec,
    SensorType,
    ShankProfile,
    Thermowell,
    ThermowellGeometry,
)
from thermowell_sizer.core.units import BAR_PA, INCH_M, KELVIN_OFFSET


@pytest.fixture
def tapered_geometry() -> ThermowellGeometry:
    return ThermowellGeometry(
        profile=ShankProfile.TAPERED,
        L=10 * INCH_M,
        A=1.0 * INCH_M,
        B=0.75 * INCH_M,
        d=0.26 * INCH_M,
        t=0.25 * INCH_M,
        b=0.125 * INCH_M,
    )


@pytest.fixture
def calc_input(tapered_geometry: ThermowellGeometry) -> CalcInput:
    return CalcInput(
        identification=Identification(tag="TW-1001", service="Vapor de media"),
        process=ProcessConditions(
            fluid_id="water",
            phase=Phase.STEAM,
            operating_pressure=20 * BAR_PA,
            design_pressure=25 * BAR_PA,
            operating_temperature=300 + KELVIN_OFFSET,
            design_temperature=350 + KELVIN_OFFSET,
            flow_cases=(FlowCase(label="max", basis=FlowBasis.VELOCITY, velocity=40.0),),
            properties=FluidProperties(
                density=8.0, dynamic_viscosity=2.0e-5, source=PropertySource.USER
            ),
        ),
        pipe=PipeData(nominal_size="NPS 8", schedule="40", inner_diameter=0.2027),
        thermowell=Thermowell(
            geometry=tapered_geometry,
            material=MaterialRef(material_id="F22"),
            connection=ProcessConnection(
                type=ConnectionType.FLANGED, size="1-1/2", rating_class=300, face=FlangeFace.RF
            ),
        ),
        sensor=SensorSpec(type=SensorType.RTD_PT100, sheath_diameter=6e-3),
    )
