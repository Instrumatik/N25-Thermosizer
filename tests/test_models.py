import pytest
from pydantic import ValidationError

from thermowell_sizer.core.models import (
    CalcInput,
    ConnectionType,
    FlowBasis,
    FlowCase,
    ProcessConnection,
    ShankProfile,
    ThermowellGeometry,
)


def test_valid_input_is_frozen(calc_input: CalcInput) -> None:
    with pytest.raises(ValidationError):
        calc_input.identification.tag = "otro"  # type: ignore[misc]


def test_flow_case_requires_value_for_basis() -> None:
    with pytest.raises(ValidationError, match="mass_flow"):
        FlowCase(label="max", basis=FlowBasis.MASS_FLOW, velocity=3.0)


def test_design_below_operation_rejected(calc_input: CalcInput) -> None:
    data = calc_input.process.model_dump()
    data["design_pressure"] = data["operating_pressure"] - 1.0
    with pytest.raises(ValidationError, match="presión de diseño"):
        type(calc_input.process).model_validate(data)
    data = calc_input.process.model_dump()
    data["design_temperature"] = data["operating_temperature"] - 1.0
    with pytest.raises(ValidationError, match="temperatura de diseño"):
        type(calc_input.process).model_validate(data)


def test_flanged_requires_rating() -> None:
    with pytest.raises(ValidationError, match="clase"):
        ProcessConnection(type=ConnectionType.FLANGED)
    assert ProcessConnection(type=ConnectionType.THREADED).rating_class is None


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"d": 0.02}, "agujero"),
        ({"B": 0.03}, "punta B"),
        ({"profile": ShankProfile.STRAIGHT}, "recto"),
        ({"profile": ShankProfile.STEPPED, "Ls": 0.0}, "escalonado"),
        ({"L0": 0.3}, "L0"),
    ],
)
def test_geometry_consistency(
    tapered_geometry: ThermowellGeometry, changes: dict[str, object], message: str
) -> None:
    data = tapered_geometry.model_dump() | changes
    with pytest.raises(ValidationError, match=message):
        ThermowellGeometry.model_validate(data)


def test_json_round_trip(calc_input: CalcInput) -> None:
    assert CalcInput.model_validate_json(calc_input.model_dump_json()) == calc_input
