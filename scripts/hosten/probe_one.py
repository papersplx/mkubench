#!/usr/bin/env python3
"""Probe one gateway model, printing full HTTP error detail."""
import json
import sys
import urllib.request

m = sys.argv[1]
body = json.dumps({
    "model": m,
    "messages": [{"role": "user", "content": "Reply with the single word: pong"}],
    "temperature": 0,
}).encode()
req = urllib.request.Request(
    "http://localhost:8079/v1/chat/completions",
    data=body,
    headers={"Content-Type": "application/json", "Authorization": "Bearer dummy"},
)
try:
    with urllib.request.urlopen(req, timeout=240) as r:
        data = json.loads(r.read().decode())
    text = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
    print(f"{m}: OK len={len(text)} :: {text[:120]!r}")
except urllib.error.HTTPError as e:
    detail = e.read().decode(errors="replace")[:800]
    print(f"{m}: HTTP {e.code}\n{detail}")
except Exception as e:  # noqa: BLE001
    print(f"{m}: {type(e).__name__}: {e}")
