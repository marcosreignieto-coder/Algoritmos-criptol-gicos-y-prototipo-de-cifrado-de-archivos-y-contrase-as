"""Ataque inteligente basado en patrones humanos.

Se centra en contraseñas como nombres, apellidos, nombre+apellido,
nombre+apellido+año y variantes con símbolos en medio. Usa Faker es_ES y
wordfreq en español, no un diccionario cerrado y pequeño.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

from ..stats import AttackResult, AttackStats
from .candidatos import intelligent_attack_candidates
from .password_attack import attack_password_candidates

ProgressCallback = Optional[Callable[[AttackStats, str], None]]
StopCallback = Optional[Callable[[], bool]]


def attack_intelligent(
    encrypted_path: str | Path,
    output_dir: str | Path,
    dictionary_path: str | Path | None = None,
    progress_callback: ProgressCallback = None,
    stop_callback: StopCallback = None,
    min_password_len: int | None = None,
    max_password_len: int | None = None,
    password_type_filter: str | None = None,
    max_iterations: int | None = None,
) -> AttackResult:
    return attack_password_candidates(
        encrypted_path,
        output_dir,
        intelligent_attack_candidates(dictionary_path),
        "ataque inteligente",
        progress_callback,
        stop_callback,
        min_password_len,
        max_password_len,
        password_type_filter,
        max_iterations,
    )
