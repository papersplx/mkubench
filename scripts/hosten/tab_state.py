#!/usr/bin/env python3
"""Dump the visible state of a gateway tab via the debug route."""
import sys
import urllib.parse
import urllib.request

model = sys.argv[1]
js = """() => {
  const q = (s) => document.querySelectorAll(s).length;
  const tas = [...document.querySelectorAll('textarea,[contenteditable="true"]')]
      .map(t => ({tag: t.tagName, ph: (t.placeholder||'').slice(0,32),
                  dis: !!(t.disabled || t.getAttribute('aria-disabled') === 'true')}));
  return JSON.stringify({
    url: location.href.slice(0, 70),
    title: document.title,
    tas: tas,
    tail: document.body.innerText.slice(-240)
  });
}"""
url = f"http://localhost:8079/debug/js?model={model}&js={urllib.parse.quote(js)}"
try:
    print(urllib.request.urlopen(url, timeout=90).read().decode()[:1400])
except Exception as e:  # noqa: BLE001
    detail = getattr(e, "read", lambda: b"")()
    try:
        detail = detail().decode(errors="replace")
    except Exception:  # noqa: BLE001
        detail = ""
    print(f"ERR {type(e).__name__}: {e} {detail[:300]}")
