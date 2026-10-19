#!/usr/bin/env python3
"""Check tencent send-button state (the submit_js selector chain)."""
import sys
import urllib.parse
import urllib.request

model = sys.argv[1] if len(sys.argv) > 1 else "tencent"
js = """() => {
  const out = {};
  const chain = [
    'div.hy-chat-input-send-btn:not(.hy-chat-input-send-btn--disabled)',
    'div.hy-chat-input-send-btn',
    'div[class*="hy-chat-input-send"]',
    'button[data-testid="send-button"]',
    'button[aria-label="Send"]',
    'button[aria-label="Submit"]',
    'button[class*="send"]',
    'button[class*="Send"]',
    'button[type="submit"]',
  ];
  out.chain = chain.map(s => {
    try {
      const el = document.querySelector(s);
      if (!el) return {sel: s, found: false};
      const st = window.getComputedStyle(el);
      return {sel: s, found: true, tag: el.tagName,
              dis: !!(el.disabled || el.getAttribute('aria-disabled') === 'true') || el.classList.contains('hy-chat-input-send-btn--disabled'),
              vis: st.display + '/' + st.visibility,
              txt: (el.innerText || el.getAttribute('aria-label') || '').slice(0, 30)};
    } catch (e) { return {sel: s, err: String(e)}; }
  });
  const ta = document.querySelector('textarea.t-textarea__inner') ||
             document.querySelector('textarea[placeholder*="Ask"]') ||
             document.querySelector('textarea');
  out.textarea = ta ? {found: true, val: (ta.value || '').slice(0, 40), ph: ta.placeholder} : {found: false};
  const items = document.querySelectorAll('.agent-chat__list__item--ai').length;
  const md = document.querySelectorAll('.hyc-content-md').length;
  out.turn_items = items;
  out.answer_md = md;
  return JSON.stringify(out);
}"""
url = f"http://localhost:8079/debug/js?model={model}&js={urllib.parse.quote(js)}"
try:
    print(urllib.request.urlopen(url, timeout=60).read().decode()[:2500])
except Exception as e:  # noqa: BLE001
    detail = getattr(e, "read", lambda: b"")()
    try:
        detail = detail().decode(errors="replace")[:400]
    except Exception:
        detail = ""
    print(f"ERR {type(e).__name__}: {e} {detail}")
