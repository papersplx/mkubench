#!/usr/bin/env python3
"""Print the full innerText of the last N chat turns on a tab."""
import sys
import urllib.parse
import urllib.request

model = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
js = r"""() => {
  const items = [...document.querySelectorAll('.agent-chat__list__item--user, .agent-chat__list__item--ai')];
  return JSON.stringify(items.slice(-N__).map(it => ({
    role: it.classList.contains('agent-chat__list__item--user') ? 'user' : 'ai',
    text: (it.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 300),
  })));
}""".replace("N__", str(n))
url = f"http://localhost:8079/debug/js?model={model}&js={urllib.parse.quote(js)}"
try:
    print(urllib.request.urlopen(url, timeout=60).read().decode()[:2000])
except Exception as e:  # noqa: BLE001
    print(f"ERR {type(e).__name__}: {e}")
