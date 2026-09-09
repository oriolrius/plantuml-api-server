#!/usr/bin/env python3
"""Minimal client for the PlantUML API server (stdlib only).

Base URL: --base, else $PLANTUML_API_BASE, else https://plantuml.joor.net

Examples:
  plantuml_api.py render diagram.puml --format svg --out diagram.svg
  plantuml_api.py check diagram.puml
  plantuml_api.py encode diagram.puml
  plantuml_api.py decode <token>
  plantuml_api.py libraries | themes | examples
  plantuml_api.py example c4-container
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_BASE = "https://plantuml.joor.net"


def base_url(args: argparse.Namespace) -> str:
    return (args.base or os.environ.get("PLANTUML_API_BASE") or DEFAULT_BASE).rstrip("/")


def _read(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _post(base: str, path: str, payload: dict) -> urllib.request.addinfourl:
    req = urllib.request.Request(
        base + path,
        data=json.dumps(payload).encode(),
        headers={"content-type": "application/json"},
    )
    return urllib.request.urlopen(req, timeout=40)


def _get(base: str, path: str) -> urllib.request.addinfourl:
    return urllib.request.urlopen(base + path, timeout=40)


def cmd_render(args: argparse.Namespace) -> int:
    base = base_url(args)
    source = _read(args.file)
    try:
        resp = _post(base, "/api/v1/render", {"source": source, "format": args.format})
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"render failed: HTTP {e.code} {e.read().decode('utf-8', 'replace')}\n")
        return 1
    data = resp.read()
    if args.out:
        with open(args.out, "wb") as fh:
            fh.write(data)
        print(f"wrote {args.out} ({len(data)} bytes, {resp.headers.get('content-type')})")
    else:
        sys.stdout.buffer.write(data)
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    base = base_url(args)
    source = _read(args.file)
    try:
        _post(base, "/api/v1/render", {"source": source, "format": "svg"})
        print("OK — renders cleanly")
        return 0
    except urllib.error.HTTPError as e:
        print(f"ERROR — HTTP {e.code}: {e.read().decode('utf-8', 'replace')}")
        return 1


def cmd_encode(args: argparse.Namespace) -> int:
    base = base_url(args)
    resp = _post(base, "/api/v1/encode", {"source": _read(args.file)})
    print(json.dumps(json.loads(resp.read()), indent=2))
    return 0


def cmd_decode(args: argparse.Namespace) -> int:
    base = base_url(args)
    resp = _post(base, "/api/v1/decode", {"encoded": args.token})
    print(json.loads(resp.read())["source"])
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    base = base_url(args)
    resp = _get(base, f"/api/v1/{args.command}")
    print(json.dumps(json.loads(resp.read()), indent=2))
    return 0


def cmd_example(args: argparse.Namespace) -> int:
    base = base_url(args)
    resp = _get(base, f"/api/v1/examples/{args.id}")
    print(json.dumps(json.loads(resp.read()), indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="PlantUML API client")
    p.add_argument("--base", help="API base URL (default: $PLANTUML_API_BASE or the public host)")
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("render", help="render a .puml file")
    r.add_argument("file")
    r.add_argument("--format", default="svg", choices=["svg", "png", "txt", "pdf", "eps"])
    r.add_argument("--out")
    r.set_defaults(func=cmd_render)

    c = sub.add_parser("check", help="validate a .puml renders")
    c.add_argument("file")
    c.set_defaults(func=cmd_check)

    e = sub.add_parser("encode", help="encode a .puml file → token + URLs")
    e.add_argument("file")
    e.set_defaults(func=cmd_encode)

    d = sub.add_parser("decode", help="decode a token → source")
    d.add_argument("token")
    d.set_defaults(func=cmd_decode)

    for name in ("libraries", "themes", "examples"):
        s = sub.add_parser(name, help=f"list {name}")
        s.set_defaults(func=cmd_list)

    x = sub.add_parser("example", help="one example by id")
    x.add_argument("id")
    x.set_defaults(func=cmd_example)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
