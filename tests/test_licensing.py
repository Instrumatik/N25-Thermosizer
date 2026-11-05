"""Licencias firmadas: emisión, validación, adulteración, vencimiento y equipo."""

from __future__ import annotations

import importlib.util
from datetime import date
from pathlib import Path
from types import ModuleType

import pytest

from thermowell_sizer import licensing
from thermowell_sizer.licensing import Edition, License, LicenseError

ROOT = Path(__file__).resolve().parents[1]


def _keygen() -> ModuleType:
    spec = importlib.util.spec_from_file_location("keygen", ROOT / "tools" / "keygen.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def keypair(tmp_path_factory: pytest.TempPathFactory) -> tuple[ModuleType, Path, str]:
    kg = _keygen()
    key = tmp_path_factory.mktemp("k") / "priv.pem"
    return kg, key, kg.new_key(key)


def _lic(**kw: object) -> License:
    base: dict[str, object] = {"holder": "Planta Norte S.A.", "email": "a@b.com",
                               "edition": Edition.PROFESSIONAL, "issued": "2026-01-01"}
    base.update(kw)
    return License(**base)  # type: ignore[arg-type]


def test_issue_and_verify(keypair: tuple[ModuleType, Path, str]) -> None:
    kg, key, pub = keypair
    text = kg.issue(key, _lic())
    assert text.startswith("TWS1.")
    lic = licensing.verify(text, public_key_b64=pub)
    assert lic.holder == "Planta Norte S.A."
    assert lic.edition is Edition.PROFESSIONAL
    # Espacios y saltos de línea al pegar no afectan.
    wrapped = "\n".join(text[i:i + 40] for i in range(0, len(text), 40))
    assert licensing.verify(wrapped, public_key_b64=pub) == lic


def test_tampered_payload_rejected(keypair: tuple[ModuleType, Path, str]) -> None:
    kg, key, pub = keypair
    text = kg.issue(key, _lic())
    other = licensing.encode(_lic(holder="Otra"), licensing._b64d(text.split(".")[2]))
    with pytest.raises(LicenseError, match="Firma"):
        licensing.verify(other, public_key_b64=pub)


def test_wrong_key_rejected(keypair: tuple[ModuleType, Path, str]) -> None:
    kg, key, _ = keypair
    with pytest.raises(LicenseError, match="Firma"):
        licensing.verify(kg.issue(key, _lic()))  # clave pública de producción


@pytest.mark.parametrize("bad", ["", "hola", "TWS1.xx", "TWS2.a.b", "TWS1.@@@.###"])
def test_malformed(bad: str) -> None:
    with pytest.raises(LicenseError):
        licensing.verify(bad)


def test_expiry(keypair: tuple[ModuleType, Path, str]) -> None:
    kg, key, pub = keypair
    text = kg.issue(key, _lic(expires="2027-06-30"))
    assert licensing.verify(text, public_key_b64=pub, today=date(2027, 6, 30))
    with pytest.raises(LicenseError, match="vencida"):
        licensing.verify(text, public_key_b64=pub, today=date(2027, 7, 1))


def test_machine_binding(keypair: tuple[ModuleType, Path, str]) -> None:
    kg, key, pub = keypair
    text = kg.issue(key, _lic(machine="ABCDEF0123456789"))
    assert licensing.verify(text, public_key_b64=pub, fingerprint="ABCDEF0123456789")
    with pytest.raises(LicenseError, match="otro equipo"):
        licensing.verify(text, public_key_b64=pub, fingerprint="0000000000000000")


def test_other_product(keypair: tuple[ModuleType, Path, str]) -> None:
    _, key, pub = keypair
    lic = _lic(product="Otro")
    from cryptography.hazmat.primitives import serialization

    priv = serialization.load_pem_private_key(key.read_bytes(), password=None)
    text = licensing.encode(lic, priv.sign(lic.to_json()))  # type: ignore[union-attr,call-arg]
    with pytest.raises(LicenseError, match="producto"):
        licensing.verify(text, public_key_b64=pub)


def test_fingerprint_stable() -> None:
    fp = licensing.machine_fingerprint()
    assert fp == licensing.machine_fingerprint()
    assert len(fp) == licensing.FINGERPRINT_LEN
    int(fp, 16)


def test_install_and_load(tmp_path: Path, keypair: tuple[ModuleType, Path, str],
                          monkeypatch: pytest.MonkeyPatch) -> None:
    kg, key, pub = keypair
    assert licensing.load(tmp_path) is None
    with pytest.raises(LicenseError):
        licensing.install(tmp_path, "basura")
    assert not (tmp_path / licensing.LICENSE_FILE).exists()
    text = kg.issue(key, _lic())
    monkeypatch.setattr(licensing.verify, "__kwdefaults__",
                        {**licensing.verify.__kwdefaults__, "public_key_b64": pub})
    lic = licensing.install(tmp_path, text)
    assert licensing.load(tmp_path) == lic
    (tmp_path / licensing.LICENSE_FILE).write_text(text[:-4] + "AAAA", encoding="utf-8")
    assert licensing.load(tmp_path) is None


def test_keygen_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    kg = _keygen()
    key = tmp_path / "k.pem"
    assert kg.main(["nueva-clave", "--salida", str(key)]) == 0
    pub = capsys.readouterr().out.split(":")[-1].strip()
    with pytest.raises(SystemExit):
        kg.main(["nueva-clave", "--salida", str(key)])
    assert kg.main(["emitir", "--clave", str(key), "--titular", "X", "--edicion",
                    "enterprise", "--vence", "2030-01-01"]) == 0
    text = capsys.readouterr().out.strip()
    assert licensing.verify(text, public_key_b64=pub).edition is Edition.ENTERPRISE
