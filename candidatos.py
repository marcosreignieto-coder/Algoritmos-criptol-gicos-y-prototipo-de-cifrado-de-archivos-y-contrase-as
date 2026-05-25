"""Ataque por cabecera PNG.

Este archivo agrupa los ataques que usan bytes conocidos de la cabecera PNG.
Por ahora sirve para:
- César;
- Vigenère con clave periódica de hasta 16 caracteres/bytes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

from .. import cesar
from .. import vigenere
from ..file_format import AttackError, get_algorithm
from ..stats import AttackResult, AttackStats

ProgressCallback = Optional[Callable[[AttackStats, str], None]]
StopCallback = Optional[Callable[[], bool]]


def attack_png_header(
    encrypted_path: str | Path,
    output_dir: str | Path,
    progress_callback: ProgressCallback = None,
    stop_callback: StopCallback = None,
    max_iterations: int | None = None,
) -> AttackResult:
    algorithm = get_algorithm(encrypted_path)
    if algorithm == "CESAR":
        return cesar.header_png(encrypted_path, output_dir, progress_callback, stop_callback, max_iterations)
    if algorithm == "VIGNERE":
        return vigenere.header_png(encrypted_path, output_dir, progress_callback=progress_callback, stop_callback=stop_callback, max_iterations=max_iterations)
    raise AttackError("El ataque por cabecera PNG solo está implementado para CESAR y VIGNERE.")
