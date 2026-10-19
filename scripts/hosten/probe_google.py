#!/usr/bin/env python3
"""Inspect the google tab's input state via the gateway debug route."""
import json
import urllib.parse
import urllib.request

js = """() => {
  const tas=[...document.querySelectorAll('textarea, [contenteditable="true"]')].map(t=>({tag:t.tagName, ph:(t.placeholder||'').slice(0,40), al:(t.getAttribute('aria-label')||'').slice(0,40)}));
  return JSON.stringify({
    url: location.href, title: document.title,
    msPrompt: document.querySelectorAll('ms-prompt-box').length,
    tas: tas,
    text: document.body.innerText.slice(0, 300)
  });
}"""
url = "http://localhost:8079/debug/js?model=google&js=" + urllib.parse.quote(js)
try:
    r = urllib.request.urlopen(url, timeout=60).read().decode()
    print(r[:1600])
except Exception as e:  # noqa: BLE001
    detail = getattr(e, "read", lambda: b"")()
    try:
        detail = detail().decode(errors="replace")
    except Exception:  # noqa: BLE001
        detail = ""
    print(f"ERR {type(e).__name__}: {e} {detail[:400]}")
