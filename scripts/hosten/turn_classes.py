#!/usr/bin/env python3
"""Dump the turn structure (role classes) of a chat tab."""
import sys
import urllib.parse
import urllib.request

model = sys.argv[1]
js = r"""() => {
  const out = [];
  const hosts = [...document.querySelectorAll('[class*="chat-user"], [class*="chat-assistant"], [class*="assistant"], [class*="message"]')];
  for (const h of hosts.slice(-8)) {
    const cls = (h.className || '').toString().slice(0, 70);
    const txt = (h.innerText || '').replace(/\s+/g, ' ').trim();
    const kind = /chat-user|user-message/i.test(cls) ? 'USER'
               : /chat-assistant|assistant/i.test(cls) ? 'ASSISTANT' : 'OTHER';
    out.push({kind, cls, len: txt.length, head: txt.slice(0, 70)});
  }
  return JSON.stringify({turns: out, total: hosts.length});
}"""
url = f"http://localhost:8079/debug/js?model={model}&js={urllib.parse.quote(js)}"
try:
    print(urllib.request.urlopen(url, timeout=60).read().decode()[:2500])
except Exception as e:  # noqa: BLE001
    print(f"ERR {type(e).__name__}: {e}")
