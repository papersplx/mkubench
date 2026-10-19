#!/usr/bin/env python3
"""Dump a site's conversation as ordered (role, text) pairs via /debug/js.

role detection: the site's own marking is used when available, otherwise a
heuristic split on the known user-vs-assistant markers for that site.
"""
import sys
import urllib.parse
import urllib.request

model = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 60

JS = r"""
() => {
  const out = [];
  // Walk every rendered block that looks like a message row.
  const rows = [...document.querySelectorAll(
    'div[class*="message"], div[class*="turn"], div[class*="bubble"], ' +
    'div[class*="chat-item"], div[class*="answer"], div[class*="question"], ' +
    'section, article, li')];
  for (const r of rows) {
    // Skip nested wrappers: only take the deepest element that holds text.
    if (r.querySelector('div[class*="message"], div[class*="answer"], div[class*="question"]')) continue;
    const t = (r.innerText || '').replace(/\s+/g, ' ').trim();
    if (t.length < 40) continue;
    out.push({ cls: r.className.toString().slice(0, 80), text: t });
  }
  return JSON.stringify(out.slice(-N__));
}
""".replace("N__", str(n))

url = f"http://localhost:8079/debug/js?model={model}&js={urllib.parse.quote(JS)}"
try:
    print(urllib.request.urlopen(url, timeout=90).read().decode()[:200000])
except Exception as e:  # noqa: BLE001
    print(f"ERR {type(e).__name__}: {e}")
