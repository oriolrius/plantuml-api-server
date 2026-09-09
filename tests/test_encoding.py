"""Encoding unit tests and encode/decode endpoints."""

from __future__ import annotations

import pytest

from app.encoding import decode, encode


@pytest.mark.parametrize(
    "source",
    [
        "@startuml\nAlice -> Bob: Hello\n@enduml",
        '@startuml\n!include <awslib/AWSCommon>\nEC2(a, "b", "c")\n@enduml',
        '@startjson\n{"k": [1, 2, 3]}\n@endjson',
        "áéí ünïcödë 你好 — diagram",
    ],
)
def test_encode_decode_roundtrip(source: str) -> None:
    assert decode(encode(source)) == source


def test_hex_form_decodes() -> None:
    src = "@startuml\nA->B\n@enduml"
    assert decode("~h" + src.encode("utf-8").hex()) == src


def test_encode_endpoint(client) -> None:
    r = client.post("/api/v1/encode", json={"source": "@startuml\nAlice -> Bob\n@enduml"})
    assert r.status_code == 200
    body = r.json()
    assert body["encoded"]
    assert body["editor_url"].startswith("http://testserver/editor/uml/")
    assert body["svg_url"].endswith(body["encoded"])
    # Round-trips back through decode.
    assert decode(body["encoded"]) == "@startuml\nAlice -> Bob\n@enduml"


def test_decode_endpoint(client) -> None:
    token = encode("@startuml\nA -> B\n@enduml")
    r = client.post("/api/v1/decode", json={"encoded": token})
    assert r.status_code == 200
    assert r.json()["source"] == "@startuml\nA -> B\n@enduml"


def test_decode_bad_token(client) -> None:
    r = client.post("/api/v1/decode", json={"encoded": "!!!not-valid!!!"})
    assert r.status_code == 422
