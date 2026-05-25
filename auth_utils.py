"""Descifrado AES usado por la app de ataques.

Compatible con el AES-128 CBC tradicional de la Cripto App didáctica.
"""

from __future__ import annotations

from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def normalize_key(password: str) -> bytes:
    raw = password.encode("utf-8")
    return raw[:16] if len(raw) >= 16 else raw + b"\x00" * (16 - len(raw))


def decrypt(ciphertext: bytes, password: str, header: dict) -> bytes:
    key = normalize_key(password)
    iv = b64decode(header["iv"].encode("ascii"))
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)
