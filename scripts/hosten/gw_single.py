#!/usr/bin/env python3
"""Send one chat-completion request to the gateway and print the response."""
import json
import sys
import urllib.request

model = sys.argv[1]
prompt = sys.argv[2] if len(sys.argv) > 2 else "Reply with the single word: pong"
body = json.dumps({
    "model": model,
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0,
}).encode()
req = urllib.request.Request(
    "http://localhost:8079/v1/chat/completions",
    data=body,
    headers={"Content-Type": "application/json", "Authorization": "Bearer dummy"},
)
try:
    with urllib.request.urlopen(req, timeout=int(sys.argv[3]) if len(sys.argv) > 3 else 180) as r:
        data = json.loads(r.read().decode())
    msg = (data.get("choices") or [{}])[0].get("message", {})
    print("content:", repr(msg.get("content"))[:300])
    print("reasoning:", repr(msg.get("reasoning_content") or msg.get("reasoning"))[:200])
    print("usage:", data.get("usage"))
except urllib.error.HTTPError as e:
    print("HTTP", e.code)
    print(e.read().decode(errors="replace")[:800])
except Exception as e:  # noqa: BLE001
    print("ERR", type(e).__name__, e)
