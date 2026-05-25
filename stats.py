"""Información didáctica sobre la contraseña encontrada."""

from __future__ import annotations

SPANISH_EXTRA_LETTERS = set("áéíóúÁÉÍÓÚüÜñÑ")


def password_length(password: str | None) -> str:
    if not password:
        return "-"
    return str(len(password))


def classify_password(password: str | None) -> str:
    """Clasifica una contraseña en categorías simples para la interfaz."""
    if not password:
        return "-"
    if password.isdigit():
        return "Numérica"
    if all(ch.isalpha() or ch in SPANISH_EXTRA_LETTERS for ch in password):
        return "Alfabética (español)"
    if password.isalnum():
        return "Alfanumérica"
    return "Alfanumérica con símbolos"


def password_type_matches(password: str | None, requested_type: str | None) -> bool:
    """Comprueba si una candidata encaja con el tipo elegido en la interfaz."""
    if not requested_type or requested_type == "Cualquiera":
        return True
    return classify_password(password) == requested_type
