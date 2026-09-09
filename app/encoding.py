"""PlantUML text-encoding / decoding.

PlantUML encodes diagram sources into URL-safe strings using raw DEFLATE followed
by a custom base64-like alphabet (``0-9A-Za-z-_``). This module implements that
transform (and its inverse) in pure Python so the API can build shareable URLs and
decode incoming PlantUML payloads without calling the backend.

Reference: https://plantuml.com/text-encoding
"""

from __future__ import annotations

import zlib

# 6-bit value -> character, ordered by value. Index 0..63.
_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
_DECODE = {c: i for i, c in enumerate(_ALPHABET)}


def _encode6bit(b: int) -> str:
    return _ALPHABET[b & 0x3F]


def _append3bytes(b1: int, b2: int, b3: int) -> str:
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return _encode6bit(c1) + _encode6bit(c2) + _encode6bit(c3) + _encode6bit(c4)


def _encode64(data: bytes) -> str:
    out: list[str] = []
    length = len(data)
    for i in range(0, length, 3):
        b1 = data[i]
        b2 = data[i + 1] if i + 1 < length else 0
        b3 = data[i + 2] if i + 2 < length else 0
        out.append(_append3bytes(b1, b2, b3))
    return "".join(out)


def _decode64(encoded: str) -> bytes:
    out = bytearray()
    for i in range(0, len(encoded), 4):
        chunk = encoded[i : i + 4]
        vals = [_DECODE.get(ch, 0) for ch in chunk]
        while len(vals) < 4:
            vals.append(0)
        c1, c2, c3, c4 = vals
        b1 = (c1 << 2) | (c2 >> 4)
        b2 = ((c2 & 0xF) << 4) | (c3 >> 2)
        b3 = ((c3 & 0x3) << 6) | c4
        out.append(b1 & 0xFF)
        # Only append the extra bytes that were actually present in the source chunk.
        if len(chunk) > 2:
            out.append(b2 & 0xFF)
        if len(chunk) > 3:
            out.append(b3 & 0xFF)
    return bytes(out)


def encode(text: str) -> str:
    """Encode PlantUML source into the URL path token used by the PlantUML Server."""
    raw = text.encode("utf-8")
    compressor = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
    deflated = compressor.compress(raw) + compressor.flush()
    return _encode64(deflated)


def decode(encoded: str) -> str:
    """Decode a PlantUML URL token back into diagram source.

    Supports the plain DEFLATE form, the ``~1`` DEFLATE prefix and the ``~h`` hex
    form used by newer PlantUML clients.
    """
    token = encoded.strip()
    if token.startswith("~h"):  # hex-encoded UTF-8, no compression
        return bytes.fromhex(token[2:]).decode("utf-8")
    if token.startswith("~1"):  # explicit DEFLATE marker
        token = token[2:]
    data = _decode64(token)
    decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
    return (decompressor.decompress(data) + decompressor.flush()).decode("utf-8")
