#!/usr/bin/env python3
"""Broad check: is a chat tab logged in / does it have a composer?"""
import sys
import urllib.parse
import urllib.request

model = sys.argv[1]
js = r"""() => {
  const tas = [...document.querySelectorAll('textarea')].map(t => ({
    ph: t.placeholder || '', cls: (t.className || '').toString().slice(0, 40),
  }));
  const edits = [...document.querySelectorAll('[contenteditable="true"]')].length;
  const loginish = [...document.querySelectorAll('a, button')]
      .filter(e => /^\s*(log ?in|登录|sign ?in)\s*$/i.test(e.innerText || ''))
      .map(e => (e.innerText || '').trim()).slice(0, 5);
  return JSON.stringify({
    textareas: tas,
    contenteditable: edits,
    login_controls: loginish,
    has_chat: document.body.innerText.includes('Ask me anything'),
    body_len: document.body.innerText.length,
  });
}"""
url = f"http://localhost:8079/debug/js?model={model}&js={urllib.parse.quote(js)}"
try:
    print(urllib.request.urlopen(url, timeout=60).read().decode()[:1200])
except Exception as e:  # noqa: BLE001
    print(f"ERR {type(e).__name__}: {e}")
