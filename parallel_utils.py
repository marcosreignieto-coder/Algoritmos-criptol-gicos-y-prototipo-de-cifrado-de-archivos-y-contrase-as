"""Ataque por diccionario con librería.

Usa ``wordfreq`` para obtener un diccionario amplio de palabras frecuentes en
español e inglés, sin tener que guardar un TXT gigante dentro del proyecto.
Además aplica mutaciones típicas y permite añadir un diccionario externo.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

from ..stats import AttackResult, AttackStats
from .candidatos import dictionary_candidates
from .password_attack import attack_password_candidates

ProgressCallback = Optional[Callable[[AttackStats, str], None]]
StopCallback = Optional[Callable[[], bool]]


def attack_dictionary(
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
        dictionary_candidates(dictionary_path, mutate=True),
        "diccionario por librería + mutaciones",
        progress_callback,
        stop_callback,
        min_password_len,
        max_password_len,
        password_type_filter,
        max_iterations,
    )
