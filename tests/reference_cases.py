"""Casos de referencia: ejemplos resueltos de ASME PTC 19.3 TW-2016, sección 8.

Solo se transcriben los datos de entrada y los resultados numéricos intermedios que
publica la norma, con el número de párrafo de cada uno, para comparar el motor.
"""

from __future__ import annotations

from thermowell_sizer.core.models import (
    CalcInput,
    ConnectionType,
    EngineOptions,
    FatigueClass,
    FlowBasis,
    FlowCase,
    FluidProperties,
    Identification,
    MaterialProperties,
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
from thermowell_sizer.core.units import (
    FOOT_M,
    INCH_M,
    KELVIN_OFFSET,
    POUND_KG,
    PSI_PA,
    STANDARD_ATMOSPHERE_PA,
)

LB_FT3 = POUND_KG / FOOT_M**3
LB_IN3 = POUND_KG / INCH_M**3


def _fahrenheit(t: float) -> float:
    return (t - 32.0) / 1.8 + KELVIN_OFFSET


def example_8_1() -> tuple[CalcInput, MaterialProperties, EngineOptions]:
    """Termopozo cónico soldado, cabezal de vapor (párr. 8-1, unidades US)."""
    p_abs = 235.0 * PSI_PA + STANDARD_ATMOSPHERE_PA
    inp = CalcInput(
        identification=Identification(tag="EJ-8-1"),
        process=ProcessConditions(
            fluid_id="water",
            phase=Phase.STEAM,
            operating_pressure=p_abs,
            design_pressure=p_abs,
            operating_temperature=_fahrenheit(450.0),
            design_temperature=_fahrenheit(450.0),
            flow_cases=(FlowCase(label="normal", basis=FlowBasis.VELOCITY,
                                 velocity=295.0 * FOOT_M),),
            properties=FluidProperties(density=0.499 * LB_FT3, dynamic_viscosity=0.0171e-3,
                                       source=PropertySource.USER),
        ),
        pipe=PipeData(nominal_size="NPS 6", inner_diameter=6 * INCH_M),
        thermowell=Thermowell(
            geometry=ThermowellGeometry(
                profile=ShankProfile.TAPERED, L=4.06 * INCH_M, A=1.5 * INCH_M,
                B=1.0 * INCH_M, d=0.26 * INCH_M, t=0.188 * INCH_M, b=0.0,
            ),
            material=MaterialRef(material_id="A105"),
            connection=ProcessConnection(type=ConnectionType.WELD_IN),
        ),
        sensor=SensorSpec(type=SensorType.RTD_PT100, sheath_diameter=0.25 * INCH_M,
                          density=169.0 * LB_FT3),
    )
    material = MaterialProperties(
        material_id="A105",
        density=0.284 * LB_IN3,
        elastic_modulus=27.5e6 * PSI_PA,
        elastic_modulus_reference=29.3e6 * PSI_PA,
        allowable_stress=19_800.0 * PSI_PA,
        fatigue_class=FatigueClass.A,
    )
    return inp, material, EngineOptions()


#: Resultados publicados en los párrs. 8-1.1.5 a 8-1.8 (unidades SI, convertidos).
EXPECTED_8_1: dict[str, float] = {
    "Re": 1.068e6,
    "N_S": 0.22,
    "f_a": 2095.0,
    "H_f": 1.352,
    "H_af": 0.9995,  # el paso 3 imprime 0,9922 por error; el paso 5 usa 0,9995
    "H_as": 0.9922,
    "f_n": 2809.0,
    "H_c": 0.7746,
    "f_nc": 2176.0,
    "N_Sc": 4.525,
    "f_s": 778.8,
    "V_IR": 412.0 * FOOT_M,
    "G_SP": 29.05,
    "S_o_IR_support": 58_430.0 * PSI_PA,
    "F_T": 0.9386,
    "S_f_adm": 2816.0 * PSI_PA,
    "S_t_support": 249.6 * PSI_PA,
    "S_a_support": 242.3 * PSI_PA,
    "P_D": 6.561 * PSI_PA,
    "S_D_support": 190.6 * PSI_PA,
    "S_max_support": 432.9 * PSI_PA,
    "S_vm_support": 191.0 * PSI_PA,
    "r": 0.3580,
    "F_M": 1.147,
    "r_prime": 0.7159,
    "F_M_prime": 2.052,
    "P_d": 0.4686 * PSI_PA,
    "S_d_support": 27.93 * PSI_PA,
    "S_L_support": 156.1 * PSI_PA,
    "S_o_support": 348.9 * PSI_PA,
    "P_c": 9389.0 * PSI_PA,
    "P_t": 79_630.0 * PSI_PA,
}


def example_8_2() -> tuple[CalcInput, MaterialProperties, EngineOptions]:
    """Termopozo escalonado roscado, agua caliente (párr. 8-2, unidades SI)."""
    p_abs = 0.400e6 + STANDARD_ATMOSPHERE_PA
    inp = CalcInput(
        identification=Identification(tag="EJ-8-2"),
        process=ProcessConditions(
            fluid_id="water",
            phase=Phase.LIQUID,
            operating_pressure=p_abs,
            design_pressure=p_abs,
            operating_temperature=85.0 + KELVIN_OFFSET,
            design_temperature=85.0 + KELVIN_OFFSET,
            flow_cases=(FlowCase(label="normal", basis=FlowBasis.VELOCITY, velocity=10.0),),
            properties=FluidProperties(density=968.8, dynamic_viscosity=3.334e-4,
                                       source=PropertySource.USER),
        ),
        pipe=PipeData(nominal_size="NPS 4", inner_diameter=0.1023),
        thermowell=Thermowell(
            geometry=ThermowellGeometry(
                profile=ShankProfile.STEPPED, L=0.19, A=0.0222, B=0.0127, d=0.0066,
                t=0.0048, b=0.0, Ls=0.0635, bs=0.0032,
            ),
            material=MaterialRef(material_id="SS316"),
            connection=ProcessConnection(type=ConnectionType.THREADED),
        ),
        sensor=SensorSpec(type=SensorType.RTD_PT100, sheath_diameter=6e-3),
    )
    # El párr. 8-2.1.3 indica E = 1,93e11 Pa, pero los cálculos de 8-2.2 y 8-2.5.1 usan
    # 1,91e11 Pa; se usa este último para reproducir los resultados publicados.
    material = MaterialProperties(
        material_id="SS316",
        density=8000.0,
        elastic_modulus=1.91e11,
        elastic_modulus_reference=1.95e11,
        allowable_stress=122.0e6,
        fatigue_class=FatigueClass.B,
    )
    return inp, material, EngineOptions()


#: Resultados publicados en los párrs. 8-2.1.1 a 8-2.8.
EXPECTED_8_2: dict[str, float] = {
    "Re": 3.690e5,
    "N_S": 0.2040,
    "f_a": 438.5,
    "H_f": 1.503,
    "H_af": 0.9395,
    "H_as": 0.9836,
    "f_n": 609.1,
    "H_c": 0.8948,
    "f_nc": 545.0,
    "N_Sc": 0.02974,
    "f_s": 160.6,
    "V_IR": 16.01,
    "G_SP": 286.4,
    "P_d_IR": 12_420.0,
    "S_d_IR_support": 3558e6,
    "K_t_SP": 2.3,
    "S_o_IR_support": 8183e6,
    "F_T": 0.9795,
    "S_f_adm": 36.44e6,
    "G_RD": 137.3,
    "S_d_IR_step": 1706e6,
    "K_t_RD": 1.231,
    "S_o_IR_step": 2100e6,
    "S_t_support": 0.4776e6,
    "S_a_support": 0.4388e6,
    "P_D": 0.06782e6,
    "S_D_support": 19.42e6,
    "S_max_support": 19.86e6,
    "S_vm_support": 19.42e6,
    "S_t_step": 0.6960e6,
    "S_a_step": 0.5480e6,
    "S_D_step": 9.31e6,
    "S_max_step": 9.862e6,
    "S_vm_step": 9.317e6,
    "r": 0.2947,
    "F_M": 1.095,
    "r_prime": 0.5895,
    "F_M_prime": 1.532,
    "P_d": 4844.0,
    "P_l": 48_440.0,
    "S_d_support": 2.126e6,
    "S_L_support": 15.19e6,
    "S_o_support": 35.29e6,
    "S_d_step": 1.020e6,
    "S_L_step": 7.286e6,
    "S_o_step": 9.056e6,
    "P_c": 35.20e6,
    "P_t": 496.4e6,
}
