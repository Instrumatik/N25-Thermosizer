"""Emisor de licencias de ThermoWell Sizer (uso interno de InstruMatik).

Uso:
    python tools/keygen.py nueva-clave --salida clave_privada.pem
    python tools/keygen.py emitir --clave clave_privada.pem --titular "Empresa S.A." \
        --correo compras@empresa.com [--edicion professional] [--vence 2027-12-31] \
        [--equipo HUELLA]

La clave privada NUNCA debe subirse al repositorio. Si se genera una clave nueva, hay
que copiar la clave pública que imprime este programa en
``src/thermowell_sizer/licensing/__init__.py`` (PUBLIC_KEY_B64) y publicar una versión nueva.
"""

from __future__ import annotations

import argparse
import base64
import sys
from datetime import date
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from thermowell_sizer.licensing import Edition, License, encode, verify


def new_key(out: Path) -> str:
    """Crea un par de claves; guarda la privada y devuelve la pública en base64."""
    key = Ed25519PrivateKey.generate()
    out.write_bytes(key.private_bytes(serialization.Encoding.PEM,
                                      serialization.PrivateFormat.PKCS8,
                                      serialization.NoEncryption()))
    pub = key.public_key().public_bytes(serialization.Encoding.Raw,
                                        serialization.PublicFormat.Raw)
    return base64.b64encode(pub).decode("ascii")


def issue(key_file: Path, lic: License) -> str:
    """Firma la licencia con la clave privada."""
    key = serialization.load_pem_private_key(key_file.read_bytes(), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise SystemExit("La clave no es Ed25519")
    text = encode(lic, key.sign(lic.to_json()))
    pub = base64.b64encode(key.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)).decode("ascii")
    verify(text, public_key_b64=pub, fingerprint=lic.machine)
    return text


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada de la línea de comandos."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_new = sub.add_parser("nueva-clave", help="genera un par de claves")
    p_new.add_argument("--salida", type=Path, required=True)
    p_iss = sub.add_parser("emitir", help="emite una licencia")
    p_iss.add_argument("--clave", type=Path, required=True)
    p_iss.add_argument("--titular", required=True)
    p_iss.add_argument("--correo", default="")
    p_iss.add_argument("--edicion", default=Edition.PROFESSIONAL.value,
                       choices=[e.value for e in Edition])
    p_iss.add_argument("--vence", default=None, help="AAAA-MM-DD")
    p_iss.add_argument("--equipo", default=None, help="huella del equipo (Ayuda > Licencia)")
    args = parser.parse_args(argv)
    if args.cmd == "nueva-clave":
        if args.salida.exists():
            raise SystemExit(f"{args.salida} ya existe; no se sobrescribe")
        print("Clave pública (copiar en PUBLIC_KEY_B64):", new_key(args.salida))
        return 0
    lic = License(holder=args.titular, email=args.correo, edition=Edition(args.edicion),
                  issued=date.today().isoformat(), expires=args.vence, machine=args.equipo)
    print(issue(args.clave, lic))
    return 0


if __name__ == "__main__":
    sys.exit(main())
