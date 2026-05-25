"""Descifrado RC4 usado por la app de ataques."""

from __future__ import annotations


def _keystream(key: bytes):
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) % 256
        s[i], s[j] = s[j], s[i]
    i = j = 0
    while True:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        yield s[(s[i] + s[j]) % 256]


def decrypt(ciphertext: bytes, password: str, header: dict) -> bytes:
    key = password.encode("utf-8")
    stream = _keystream(key)
    return bytes(byte ^ next(stream) for byte in ciphertext)
