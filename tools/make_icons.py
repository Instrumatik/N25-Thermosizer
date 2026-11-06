"""Genera el logo, los íconos y el .ico a partir del logo maestro «THWS».

Uso: ``python tools/make_icons.py <logo_maestro.png>``

- ``assets/logo_tws.png``: logo completo recortado (reportes, Acerca de, Licencia).
- ``assets/icon_tws.png``: logo completo en un cuadrado de 256 px (íconos grandes).
- ``assets/icon_t.png``: solo el termopozo negro (la «T»), para 16–48 px.
- ``packaging/thermowell_sizer.ico``: 16, 24, 32, 48 (termopozo) y 64, 128, 256 (logo).
"""

from __future__ import annotations

import io
import struct
import sys
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src" / "thermowell_sizer" / "assets"
ICO = ROOT / "packaging" / "thermowell_sizer.ico"
SMALL = (16, 24, 32, 48)
LARGE = (64, 128, 256)


def _bbox(mask: Image.Image) -> tuple[int, int, int, int]:
    box = mask.getbbox()
    if box is None:
        raise SystemExit("El logo está vacío")
    return box


def _square(img: Image.Image, pad: float) -> Image.Image:
    side = int(max(img.size) * (1 + 2 * pad))
    out = Image.new("RGB", (side, side), "white")
    out.paste(img, ((side - img.width) // 2, (side - img.height) // 2))
    return out


def main(src: Path) -> None:
    """Genera los recursos gráficos a partir del logo maestro ``src``."""
    logo = Image.open(src).convert("RGB")
    # contenido = todo lo que no es blanco
    content = ImageChops.difference(logo, Image.new("RGB", logo.size, "white")).convert("L")
    content = content.point(lambda v: 255 if v > 24 else 0)
    x0, y0, x1, y1 = _bbox(content)
    m = int(0.03 * max(x1 - x0, y1 - y0))
    full = logo.crop((max(x0 - m, 0), max(y0 - m, 0), min(x1 + m, logo.width),
                      min(y1 + m, logo.height)))
    w = 900
    full.resize((w, round(full.height * w / full.width)), Image.Resampling.LANCZOS).save(
        ASSETS / "logo_tws.png", optimize=True)

    # termopozo: píxeles oscuros y poco saturados (el azul de «HWS» queda afuera)
    r, g, b = logo.split()
    dark = Image.eval(ImageChops.lighter(ImageChops.lighter(r, g), b),
                      lambda v: 255 if v < 90 else 0)
    t_box = _bbox(dark)
    t_only = Image.composite(logo, Image.new("RGB", logo.size, "white"), dark.point(
        lambda v: v)).crop(t_box)
    icon_t = _square(t_only, 0.04).resize((256, 256), Image.Resampling.LANCZOS)
    icon_t.save(ASSETS / "icon_t.png", optimize=True)
    icon_full = _square(full, 0.02).resize((256, 256), Image.Resampling.LANCZOS)
    icon_full.save(ASSETS / "icon_tws.png", optimize=True)

    # .ico con entradas PNG (Windows Vista en adelante)
    entries: list[tuple[int, bytes]] = []
    for size in (*SMALL, *LARGE):
        base = icon_t if size in SMALL else icon_full
        buf = io.BytesIO()
        base.resize((size, size), Image.Resampling.LANCZOS).save(buf, "PNG")
        entries.append((size, buf.getvalue()))
    header = struct.pack("<HHH", 0, 1, len(entries))
    offset = 6 + 16 * len(entries)
    table, blobs = b"", b""
    for size, data in entries:
        dim = 0 if size >= 256 else size
        table += struct.pack("<BBBBHHII", dim, dim, 0, 0, 1, 32, len(data), offset)
        offset += len(data)
        blobs += data
    ICO.write_bytes(header + table + blobs)
    print(f"logo {full.size} → {ASSETS / 'logo_tws.png'}; ícono {ICO}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
