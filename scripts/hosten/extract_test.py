#!/usr/bin/env python3
"""Run sbsllm's response extractor on a model tab and print the raw result."""
import json
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, "/home/fra/dev/sbsllm")
from sbsllm.inject import extract_js  # noqa: E402

model = sys.argv[1]
js = extract_js(model)
url = f"http://localhost:8079/debug/js?model={model}&js={urllib.parse.quote(js)}"
for i in range(int(sys.argv[2]) if len(sys.argv) > 2 else 3):
    try:
        raw = urllib.request.urlopen(url, timeout=60).read().decode()
        d = json.loads(raw)
        res = d["result"]
        if isinstance(res, str):
            res = json.loads(res)
        print(f"--- attempt {i + 1} ---")
        print(json.dumps(res, indent=1)[:1500])
    except Exception as e:  # noqa: BLE001
        print("ERR", type(e).__name__, e)
    time.sleep(2)
