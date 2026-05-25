"""Utilidades para probar contraseñas contra archivos CIMG1.

La Cripto App de cifrado guarda un HMAC calculado con la contraseña original.
Eso permite descartar candidatos de forma rápida antes de descifrar el PNG.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from pathlib import Path
from typing import Optional

from .file_format import EncryptedPackage
from .png_utils import safe_filename_part, unique_path


def make_hmac(password: str, header_without_hmac: dict, ciphertext: bytes) -> str:
    key = password.encode("utf-8")
    encoded_header = json.dumps(header_without_hmac, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hmac.new(key, encoded_header + ciphertext, hashlib.sha256).digest()
    return base64.b64encode(digest).decode("ascii")


def password_matches_hmac(password: str, package: EncryptedPackage) -> bool:
    expected = package.header.get("hmac")
    if not expected:
        return False
    header_without_hmac = dict(package.header)
    header_without_hmac.pop("hmac", None)
    real = make_hmac(password, header_without_hmac, package.ciphertext)
    return hmac.compare_digest(expected, real)


def build_password_output_path(encrypted_path: str | Path, output_dir: str | Path, password: str) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = safe_filename_part(Path(encrypted_path).stem)
    safe_password = safe_filename_part(password)
    return unique_path(output_dir / f"{stem} (contraseña {safe_password}).png")
