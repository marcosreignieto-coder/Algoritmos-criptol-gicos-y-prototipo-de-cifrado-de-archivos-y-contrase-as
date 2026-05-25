"""Estructuras de datos para estadísticas y resultados de ataques."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class AttackStats:
    total_tests: int = 0
    current_rate: float = 0.0
    average_rate: float = 0.0
    min_rate: float = 0.0
    max_rate: float = 0.0
    elapsed: float = 0.0


@dataclass
class AttackResult:
    success: bool
    output_path: Optional[Path]
    algorithm: str
    attack_type: str
    found_value: Optional[str]
    stats: AttackStats
    message: str
    password_length: Optional[int] = None
    password_type: Optional[str] = None
