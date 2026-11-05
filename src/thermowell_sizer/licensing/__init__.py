"""Licencias firmadas fuera de línea con Ed25519.

El programa lleva solo la clave pública; las licencias se emiten con la clave privada,
que nunca se publica (ver ``tools/keygen.py``). Una licencia es un texto
``TWS1.<datos>.<firma>`` en base64url, con los datos en JSON: titular, correo,
edición, fecha de emisión, vencimiento opcional y huella de equipo opcional.

Sin licencia el programa funciona completo y los reportes llevan la marca
"versión de evaluación".
"""

from __future__ import annotations

import base64
import hashlib
import json
import platform
import uuid
from dataclasses import asdict, dataclass
from datetime import date
from enum import StrEnum
from pathlib import Path
from typing import Final

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

PREFIX: Final = "TWS1"
PRODUCT: Final = "ThermoWell Sizer"
PUBLIC_KEY_B64: Final = "i82Je0PbXh5jSElhoXcJxHn7/n8SsnZikdUtiwkSmgg="
LICENSE_FILE: Final = "licencia.txt"
FINGERPRINT_LEN: Final = 16


class Edition(StrEnum):
    """Ediciones comerciales."""

    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


@dataclass(frozen=True, slots=True)
class License:
    """Datos firmados de una licencia."""

    holder: str
    email: str
    edition: Edition
    issued: str
    expires: str | None = None
    machine: str | None = None
    product: str = PRODUCT

    def to_json(self) -> bytes:
        """JSON canónico (claves ordenadas, sin espacios) que se firma."""
        data = asdict(self)
        data["edition"] = self.edition.value
        return json.dumps(data, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False).encode("utf-8")


class LicenseError(ValueError):
    """Licencia mal formada, adulterada, vencida o de otro equipo."""


def _b64e(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64d(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def machine_fingerprint() -> str:
    """Huella estable del equipo (nombre + MAC + sistema), sin datos personales legibles."""
    raw = f"{platform.node()}|{uuid.getnode():012x}|{platform.system()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:FINGERPRINT_LEN].upper()


def encode(lic: License, signature: bytes) -> str:
    """Arma el texto de la licencia."""
    return f"{PREFIX}.{_b64e(lic.to_json())}.{_b64e(signature)}"


def verify(text: str, *, today: date | None = None, public_key_b64: str = PUBLIC_KEY_B64,
           fingerprint: str | None = None) -> License:
    """Valida firma, producto, vencimiento y equipo.

    Raises:
        LicenseError: con el motivo.
    """
    parts = "".join(text.split()).split(".")
    if len(parts) != 3 or parts[0] != PREFIX:
        raise LicenseError("Formato de licencia no reconocido")
    try:
        payload, signature = _b64d(parts[1]), _b64d(parts[2])
        data = json.loads(payload.decode("utf-8"))
        lic = License(holder=data["holder"], email=data.get("email", ""),
                      edition=Edition(data["edition"]), issued=data["issued"],
                      expires=data.get("expires"), machine=data.get("machine"),
                      product=data.get("product", PRODUCT))
    except (ValueError, KeyError, TypeError) as exc:
        raise LicenseError("Licencia ilegible") from exc
    key = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key_b64))
    try:
        key.verify(signature, lic.to_json())
    except InvalidSignature as exc:
        raise LicenseError("Firma inválida: la licencia fue modificada o no es auténtica") \
            from exc
    if lic.product != PRODUCT:
        raise LicenseError("La licencia es de otro producto")
    if lic.expires and (today or date.today()) > date.fromisoformat(lic.expires):
        raise LicenseError(f"Licencia vencida el {lic.expires}")
    if lic.machine and lic.machine != (fingerprint or machine_fingerprint()):
        raise LicenseError("La licencia corresponde a otro equipo")
    return lic


def load(folder: Path) -> License | None:
    """Licencia instalada en ``folder``, o ``None`` si no hay o no es válida."""
    path = folder / LICENSE_FILE
    if not path.exists():
        return None
    try:
        return verify(path.read_text(encoding="utf-8"))
    except LicenseError:
        return None


def install(folder: Path, text: str) -> License:
    """Valida y guarda una licencia.

    Raises:
        LicenseError: si no es válida (no se guarda nada).
    """
    lic = verify(text)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / LICENSE_FILE).write_text("".join(text.split()), encoding="utf-8")
    return lic
