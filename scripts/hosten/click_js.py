#!/usr/bin/env python3
"""Run arbitrary JS on a gateway tab (debug route) with optional sleep+reprobe."""
import sys
import time
import urllib.parse
import urllib.request

model = sys.argv[1]
js = sys.argv[2]
sleep_s = float(sys.argv[3]) if len(sys.argv) > 3 else 0
js2 = sys.argv[4] if len(sys.argv) > 4 else None


def run(m, expr):
    u = f"http://localhost:8079/debug/js?model={m}&js={urllib.parse.quote(expr)}"
    try:
        return urllib.request.urlopen(u, timeout=90).read().decode()
    except Exception as e:  # noqa: BLE001
        return f"ERR {type(e).__name__}: {e}"


print(run(model, js))
if sleep_s:
    time.sleep(sleep_s)
if js2:
    print(run(model, js2))
