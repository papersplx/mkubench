#!/usr/bin/env python3
"""Dump the last few chat turns (user + assistant) from a tab, with busy state."""
import sys
import urllib.parse
import urllib.request

model = sys.argv[1]
js = r"""() => {
  const squash = (s) => (s || '').replace(/\s+/g, ' ').trim();
  const out = {url: location.href.slice(0, 80), turns: [], busy_signals: []};
  const userSels = ['.agent-chat__list__item--user', '[class*="user"] .hyc-content-md',
                    '.hyc-user', '[data-role="user"]'];
  const aiSels = ['.agent-chat__list__item--ai', '.hyc-content-md'];
  const items = [...document.querySelectorAll('.agent-chat__list__item--user, .agent-chat__list__item--ai')];
  for (const it of items.slice(-6)) {
    const isUser = it.classList.contains('agent-chat__list__item--user');
    out.turns.push({
      role: isUser ? 'user' : 'ai',
      len: (it.innerText || '').length,
      txt: squash(it.innerText).slice(0, 120),
    });
  }
  if (!items.length) {
    // generic fallback: any element with a long text
    const blocks = [...document.querySelectorAll('main *, [class*="chat"] *')]
      .filter(e => e.children.length === 0 && (e.innerText || '').length > 40)
      .slice(-8).map(e => squash(e.innerText).slice(0, 100));
    out.fallback_blocks = blocks;
  }
  for (const s of ['.t-loading', '[class*="loading"]', '.hyc-content-loading',
                   '.stop-generating-btn', '[aria-busy="true"]']) {
    const n = document.querySelectorAll(s).length;
    if (n) out.busy_signals.push({sel: s, n: n});
  }
  out.body_tail = squash(document.body.innerText).slice(-200);
  return JSON.stringify(out);
}"""
url = f"http://localhost:8079/debug/js?model={model}&js={urllib.parse.quote(js)}"
try:
    print(urllib.request.urlopen(url, timeout=60).read().decode()[:2500])
except Exception as e:  # noqa: BLE001
    detail = getattr(e, "read", lambda: b"")()
    try:
        detail = detail().decode(errors="replace")[:300]
    except Exception:
        detail = ""
    print(f"ERR {type(e).__name__}: {e} {detail}")
