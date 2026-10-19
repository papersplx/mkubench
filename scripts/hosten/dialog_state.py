#!/usr/bin/env python3
"""Report any visible modal dialogs on a gateway tab (tencent-style blocker)."""
import sys
import urllib.parse
import urllib.request

model = sys.argv[1]
js = """() => {
  const isVisible = (el) => {
    if (!el) return false;
    const s = window.getComputedStyle(el);
    if (!s) return true;
    if (s.display === 'none') return false;
    if (s.visibility === 'hidden' || s.visibility === 'collapse') return false;
    if (s.opacity !== '' && Number(s.opacity) < 0.05) return false;
    return el.getClientRects().length > 0;
  };
  const sel = ['[role="dialog"][aria-modal="true"]', '[role="alertdialog"]',
               '[role="dialog"]', '.t-dialog', '.hy-dialog'];
  const out = [];
  for (const s of sel) {
    for (const el of document.querySelectorAll(s)) {
      if (isVisible(el)) {
        out.push({sel: s, cls: (el.className || '').toString().slice(0, 80),
                  text: (el.innerText || '').replace(/\\s+/g, ' ').trim().slice(0, 300)});
      }
    }
  }
  const btns = [...document.querySelectorAll('[role="dialog"] button, [role="dialog"] [class*="close" i]')]
      .map(b => ({cls: (b.className||'').toString().slice(0,60), txt: (b.innerText||'').slice(0,40)}))
      .slice(0, 8);
  return JSON.stringify({url: location.href.slice(0, 90), dialogs: out, buttons: btns});
}"""
url = f"http://localhost:8079/debug/js?model={model}&js={urllib.parse.quote(js)}"
try:
    print(urllib.request.urlopen(url, timeout=60).read().decode()[:2000])
except Exception as e:  # noqa: BLE001
    detail = getattr(e, "read", lambda: b"")()
    try:
        detail = detail().decode(errors="replace")[:400]
    except Exception:
        detail = ""
    print(f"ERR {type(e).__name__}: {e} {detail}")
