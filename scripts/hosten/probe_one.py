#!/usr/bin/env python3
"""Probe one gateway model, printing full HTTP error detail."""
import fcntl
import json
import os
import sys
import urllib.request

PROJECT = "/var/home/fra/dev/mkubench"
LOCKFILE = os.path.join(PROJECT, "results", "logs", "probe.lock")

# The probe submits a real prompt to the site's tab, so two probes at once
# would fight over the same tab (and over the gateway's browser lock).  Every
# caller takes this lock, whichever script it is.
os.makedirs(os.path.dirname(LOCKFILE), exist_ok=True)
_lock = open(LOCKFILE, "w")
fcntl.flock(_lock, fcntl.LOCK_EX)

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
    with urllib.request.urlopen(req, timeout=600) as r:
        data = json.loads(r.read().decode())
    text = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
    print(f"{m}: OK len={len(text)} :: {text[:120]!r}")
except urllib.error.HTTPError as e:
    detail = e.read().decode(errors="replace")[:800]
    print(f"{m}: HTTP {e.code}\n{detail}")
except Exception as e:  # noqa: BLE001
    print(f"{m}: {type(e).__name__}: {e}")
