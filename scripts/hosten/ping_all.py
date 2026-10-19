#!/usr/bin/env python3
"""Ping every gateway model with a trivial prompt; log status per model."""
import json
import sys
import urllib.request

MODELS = ["claude", "mistral", "zai", "meta", "qwen", "grok", "google", "kimi", "tencent", "copilot"]
OUT = "/tmp/ping_results.txt"

with open(OUT, "w") as fh:
    for m in MODELS:
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
            fh.write(f"{m}: OK len={len(text)} :: {text[:70]!r}\n")
        except Exception as e:  # noqa: BLE001
            body = getattr(e, "read", lambda: b"")()
            try:
                detail = body().decode()[:200]
            except Exception:  # noqa: BLE001
                detail = ""
            fh.write(f"{m}: FAIL {type(e).__name__} {detail}\n")
        fh.flush()
print("done")
