#!/usr/bin/env python3
"""Reproduce sbsllm's inject+submit on one model tab and report each step."""
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, "/home/fra/dev/sbsllm")
from sbsllm.inject import inject_prompt, submit_js  # noqa: E402

model = sys.argv[1]
prompt = sys.argv[2] if len(sys.argv) > 2 else "Reply with the single word: pong"


def run(js, timeout=60):
    url = f"http://localhost:8079/debug/js?model={model}&js={urllib.parse.quote(js)}"
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read().decode()


try:
    inject = inject_prompt(model, prompt)
    print("--- inject result ---")
    print(run(inject)[:600])
except Exception as e:  # noqa: BLE001
    print("inject ERR", type(e).__name__, e)

try:
    submit = submit_js(model)
    print("--- submit result ---")
    print(run(submit)[:600])
except Exception as e:  # noqa: BLE001
    print("submit ERR", type(e).__name__, e)
