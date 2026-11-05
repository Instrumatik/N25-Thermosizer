from thermowell_sizer.core.constants import Range, ref
from thermowell_sizer.core.models import Construction, ShankProfile, ThermowellGeometry
from thermowell_sizer.core.units import INCH_M
from thermowell_sizer.core.validation import Severity, validate_geometry


def _keys(g: ThermowellGeometry) -> set[tuple[str, str]]:
    return {(i.field, i.message_key) for i in validate_geometry(g)}


def test_reference_helper() -> None:
    assert ref("eq. (6-4-1)") == "ASME PTC 19.3 TW-2016, eq. (6-4-1)"
    assert Range(None, 1.0).contains(-5.0)
    assert not Range(0.0, None).contains(-1.0)


def test_tapered_in_scope(tapered_geometry: ThermowellGeometry) -> None:
    assert validate_geometry(tapered_geometry) == []


def test_short_well_out_of_scope(tapered_geometry: ThermowellGeometry) -> None:
    g = tapered_geometry.model_copy(update={"L": 2.0 * INCH_M})
    issues = validate_geometry(g)
    assert ("L", "validation.out_of_range") in {(i.field, i.message_key) for i in issues}
    assert all(i.severity is Severity.ERROR for i in issues)


def test_long_well_is_info(tapered_geometry: ThermowellGeometry) -> None:
    g = tapered_geometry.model_copy(update={"L": 30 * INCH_M})
    issues = validate_geometry(g)
    assert [(i.message_key, i.severity) for i in issues] == [
        ("validation.long_well_ok", Severity.INFO)
    ]


def test_thin_wall_tip_rough_and_fabricated(tapered_geometry: ThermowellGeometry) -> None:
    g = tapered_geometry.model_copy(
        update={
            "d": 0.6 * INCH_M,
            "t": 0.1 * INCH_M,
            "surface_finish_ra": 3.2e-6,
            "construction": Construction.FABRICATED,
        }
    )
    keys = _keys(g)
    assert ("d", "validation.wall_too_thin") in keys
    assert ("t", "validation.tip_too_thin") in keys
    assert ("surface_finish_ra", "validation.rough_surface") in keys
    assert ("construction", "validation.fabricated_out_of_scope") in keys


def _stepped(**kw: float) -> ThermowellGeometry:
    base: dict[str, object] = {
        "profile": ShankProfile.STEPPED,
        "L": 10 * INCH_M,
        "A": 1.0625 * INCH_M,
        "B": 0.875 * INCH_M,
        "d": 0.26 * INCH_M,
        "t": 0.25 * INCH_M,
        "Ls": 4 * INCH_M,
    }
    return ThermowellGeometry.model_validate(base | kw)


def test_stepped_in_scope() -> None:
    assert validate_geometry(_stepped()) == []


def test_stepped_bad_ratio_and_length() -> None:
    keys = _keys(_stepped(A=1.75 * INCH_M, Ls=7 * INCH_M))
    assert ("A", "validation.out_of_range") in keys
    assert ("Ls", "validation.out_of_range") in keys


def test_stepped_non_standard_tip() -> None:
    keys = _keys(_stepped(B=0.7 * INCH_M, A=1.0 * INCH_M, d=0.25 * INCH_M))
    assert ("B", "validation.stepped_tip_not_standard") in keys
