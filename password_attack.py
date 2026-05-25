"""Ataque por fuerza bruta limitada.

No intenta fuerza bruta total porque no es realista en Python. Prueba rangos
útiles para demostración: números cortos y minúsculas cortas.
"""

from __future__ import annotations

import itertools
from pathlib import Path
from typing import Callable, Iterable, Optional

from ..stats import AttackResult, AttackStats
from .candidatos import lowercase_candidates, numeric_candidates, unique
from .password_attack import attack_password_candidates

ProgressCallback = Optional[Callable[[AttackStats, str], None]]
StopCallback = Optional[Callable[[], bool]]


def default_bruteforce_candidates(max_password_len: int | None = None) -> Iterable[str]:
    # Fuerza bruta limitada: números hasta 8 y minúsculas hasta 4 como máximo.
    numeric_max = min(max_password_len or 6, 8)
    lower_max = min(max_password_len or 4, 4)
    return unique(itertools.chain(numeric_candidates(numeric_max), lowercase_candidates(lower_max)))


def attack_bruteforce(
    encrypted_path: str | Path,
    output_dir: str | Path,
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
        default_bruteforce_candidates(max_password_len),
        "fuerza bruta limitada",
        progress_callback,
        stop_callback,
        min_password_len,
        max_password_len,
        password_type_filter,
        max_iterations,
    )
