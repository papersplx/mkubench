#!/usr/bin/env python3
"""Ping a set of gateway models in parallel; log status per model."""
import json
import sys
import threading
import urllib.request

MODELS = sys.argv[1:] or [
    "claude", "mistral", "zai", "meta", "qwen", "grok",
    "google", "kimi", "tencent", "copilot",
]
OUT = "/tmp/ping_set.txt"
lock = threading.Lock()


def ping(m):
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
        with urllib.request.urlopen(req, timeout=200) as r:
            data = json.loads(r.read().decode())
        text = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
        line = f"{m}: OK len={len(text)} :: {text[:60]!r}"
    except Exception as e:  # noqa: BLE001
        body = getattr(e, "read", lambda: b"")()
        try:
            detail = body().decode()[:160].replace("\n", " ")
        except Exception:
            detail = ""
        line = f"{m}: FAIL {type(e).__name__} {detail}"
    with lock:
        with open(OUT, "a") as fh:
            fh.write(line + "\n")
            fh.flush()


with open(OUT, "w") as fh:
    fh.write("")
threads = [threading.Thread(target=ping, args=(m,), daemon=True) for t in []]
threads = [threading.Thread(target=ping, args=(m,), daemon=True) for m in MODELS]
for t in threads:
    t.start()
for t in threads:
    t.join()
print("done")
