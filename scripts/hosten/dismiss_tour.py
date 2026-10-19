#!/usr/bin/env python3
"""Dismiss an onboarding/product-tour modal on a gateway tab.

Only clicks benign navigation controls (Next / Skip / Got it / Close / X).
Never touches security controls (CAPTCHA/Turnstile/login walls).
"""
import sys
import urllib.parse
import urllib.request

model = sys.argv[1]
js = r"""() => {
  const clicked = [];
  const labels = /^\s*(next|skip|got it|close|done|later|maybe later|not now|no thanks|dismiss|x)\s*$/i;
  for (let i = 0; i < 6; i++) {
    let hit = null;
    for (const el of document.querySelectorAll('button, [role="button"], a[role="button"], .close, [class*="close" i], [class*="skip" i], [class*="next" i]')) {
      const txt = (el.innerText || el.getAttribute('aria-label') || '').trim();
      if (labels.test(txt) && el.offsetParent !== null) { hit = el; break; }
    }
    if (!hit) break;
    const t = (hit.innerText || hit.getAttribute('aria-label') || '').trim().slice(0, 20);
    hit.click();
    clicked.push(t);
    // let the UI settle
    const s = Date.now(); while (Date.now() - s < 400) {}
  }
  const leftovers = [...document.querySelectorAll('[role="dialog"], [class*="tour" i], [class*="onboard" i], [class*="modal" i]')]
      .filter(e => e.offsetParent !== null).length;
  return JSON.stringify({clicked: clicked, visible_modals_left: leftovers});
}"""
url = f"http://localhost:8079/debug/js?model={model}&js={urllib.parse.quote(js)}"
try:
    print(urllib.request.urlopen(url, timeout=90).read().decode()[:600])
except Exception as e:  # noqa: BLE001
    print(f"ERR {type(e).__name__}: {e}")
