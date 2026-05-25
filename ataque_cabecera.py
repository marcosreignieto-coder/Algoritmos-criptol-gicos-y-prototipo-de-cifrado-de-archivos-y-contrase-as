"""Utilidades comunes para validar y guardar PNG recuperados."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def is_valid_png(data: bytes) -> bool:
    """Comprueba que los bytes forman un PNG no corrupto.

    No solo mira la firma: también recorre chunks, valida IHDR/IEND y CRC.
    """
    if not data.startswith(PNG_SIGNATURE):
        return False
    if len(data) < 33:
        return False

    pos = len(PNG_SIGNATURE)
    seen_ihdr = False
    seen_iend = False

    try:
        while pos + 8 <= len(data):
            length = struct.unpack(">I", data[pos : pos + 4])[0]
            chunk_type = data[pos + 4 : pos + 8]
            pos += 8

            if pos + length + 4 > len(data):
                return False

            chunk_data = data[pos : pos + length]
            pos += length
            expected_crc = struct.unpack(">I", data[pos : pos + 4])[0]
            pos += 4

            real_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
            if real_crc != expected_crc:
                return False

            if chunk_type == b"IHDR":
                if seen_ihdr or length != 13:
                    return False
                seen_ihdr = True
            elif chunk_type == b"IEND":
                if length != 0:
                    return False
                seen_iend = True
                break

        return seen_ihdr and seen_iend
    except Exception:
        return False


def safe_filename_part(text: str) -> str:
    text = (text or "imagen").strip()
    for char in '<>:"/\\|?*':
        text = text.replace(char, "_")
    text = text.strip(" .")
    return text or "imagen"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1
