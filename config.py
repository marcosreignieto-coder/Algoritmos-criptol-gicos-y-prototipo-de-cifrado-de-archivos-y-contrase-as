"""Punto central para que la interfaz llame a los ataques.

La interfaz no contiene lógica criptográfica: solo llama a este módulo.
La lógica concreta está separada por algoritmo y por tipo de ataque.
"""

from __future__ import annotations

import itertools
from pathlib import Path
from typing import Callable, Optional

from . import cesar
from .file_format import AttackError, get_algorithm
from .stats import AttackResult, AttackStats
from .tipos_ataques import ataque_cabecera, ataque_diccionario, ataque_fuerza_bruta, ataque_inteligente, ataque_recurrentes
from .tipos_ataques.candidatos import dictionary_candidates, recurrent_passwords, smart_candidates, unique

ProgressCallback = Optional[Callable[[AttackStats, str], None]]
StopCallback = Optional[Callable[[], bool]]


def attack_png_auto(
    encrypted_path: str | Path,
    output_dir: str | Path,
    progress_callback: ProgressCallback = None,
    stop_callback: StopCallback = None,
    dictionary_path: str | Path | None = None,
    min_password_len: int | None = None,
    max_password_len: int | None = None,
    password_type_filter: str | None = None,
    max_iterations: int | None = None,
) -> AttackResult:
    """Elige el ataque recomendado según el algoritmo detectado."""
    algorithm = get_algorithm(encrypted_path)
    if algorithm == "CESAR":
        return cesar.brute_force_png(encrypted_path, output_dir, progress_callback, stop_callback, max_iterations)
    if algorithm == "VIGNERE":
        return ataque_cabecera.attack_png_header(encrypted_path, output_dir, progress_callback, stop_callback, max_iterations)
    if algorithm in {"RC4", "DES", "AES"}:
        return attack_password_full(encrypted_path, output_dir, progress_callback, stop_callback, dictionary_path, min_password_len, max_password_len, password_type_filter, max_iterations)
    raise AttackError(f"Algoritmo no soportado o desconocido: {algorithm or 'desconocido'}")


def attack_caesar_bruteforce(
    encrypted_path: str | Path,
    output_dir: str | Path,
    progress_callback: ProgressCallback = None,
    stop_callback: StopCallback = None,
    max_iterations: int | None = None,
) -> AttackResult:
    return cesar.brute_force_png(encrypted_path, output_dir, progress_callback, stop_callback, max_iterations)


def attack_header(
    encrypted_path: str | Path,
    output_dir: str | Path,
    progress_callback: ProgressCallback = None,
    stop_callback: StopCallback = None,
    max_iterations: int | None = None,
) -> AttackResult:
    return ataque_cabecera.attack_png_header(encrypted_path, output_dir, progress_callback, stop_callback, max_iterations)


def attack_recurrent(
    encrypted_path: str | Path,
    output_dir: str | Path,
    progress_callback: ProgressCallback = None,
    stop_callback: StopCallback = None,
    min_password_len: int | None = None,
    max_password_len: int | None = None,
    password_type_filter: str | None = None,
    max_iterations: int | None = None,
) -> AttackResult:
    return ataque_recurrentes.attack_recurrent(encrypted_path, output_dir, progress_callback, stop_callback, min_password_len, max_password_len, password_type_filter, max_iterations)



def attack_intelligent(
    encrypted_path: str | Path,
    output_dir: str | Path,
    progress_callback: ProgressCallback = None,
    stop_callback: StopCallback = None,
    dictionary_path: str | Path | None = None,
    min_password_len: int | None = None,
    max_password_len: int | None = None,
    password_type_filter: str | None = None,
    max_iterations: int | None = None,
) -> AttackResult:
    return ataque_inteligente.attack_intelligent(encrypted_path, output_dir, dictionary_path, progress_callback, stop_callback, min_password_len, max_password_len, password_type_filter, max_iterations)


def attack_dictionary(
    encrypted_path: str | Path,
    output_dir: str | Path,
    progress_callback: ProgressCallback = None,
    stop_callback: StopCallback = None,
    dictionary_path: str | Path | None = None,
    min_password_len: int | None = None,
    max_password_len: int | None = None,
    password_type_filter: str | None = None,
    max_iterations: int | None = None,
) -> AttackResult:
    return ataque_diccionario.attack_dictionary(encrypted_path, output_dir, dictionary_path, progress_callback, stop_callback, min_password_len, max_password_len, password_type_filter, max_iterations)


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
    return ataque_fuerza_bruta.attack_bruteforce(encrypted_path, output_dir, progress_callback, stop_callback, min_password_len, max_password_len, password_type_filter, max_iterations)


def attack_password_full(
    encrypted_path: str | Path,
    output_dir: str | Path,
    progress_callback: ProgressCallback = None,
    stop_callback: StopCallback = None,
    dictionary_path: str | Path | None = None,
    min_password_len: int | None = None,
    max_password_len: int | None = None,
    password_type_filter: str | None = None,
    max_iterations: int | None = None,
) -> AttackResult:
    """Ataque recomendado para RC4/DES/AES.

    Orden:
    1. claves recurrentes;
    2. ataque inteligente de nombres/apellidos/años/símbolos;
    3. diccionario por librería y mutaciones;
    4. fuerza bruta limitada.
    """
    from .tipos_ataques.password_attack import attack_password_candidates

    candidates = smart_candidates(dictionary_path)
    return attack_password_candidates(
        encrypted_path,
        output_dir,
        candidates,
        "ataque completo por contraseña",
        progress_callback,
        stop_callback,
        min_password_len,
        max_password_len,
        password_type_filter,
        max_iterations,
    )
