#!/usr/bin/env python3
"""mkubench gateway wrapper.

Starts the sbsllm OpenAI-compatible gateway with the timeouts the benchmark
needs (cli.py never forwards first_token_timeout/busy_patience, so a plain
`sbsllm --server` silently reverts them to 60s/20s and deep-thinking models
time out mid-question).

Env knobs (all optional):
  GATEWAY_MODELS     comma list of site ids to open tabs for
  GATEWAY_HOST/PORT  bind address (defaults: 127.0.0.1 / 8079)
  SBSLLM_FIRST_TOKEN_TIMEOUT, SBSLLM_BUSY_PATIENCE,
  SBSLLM_BROWSER_TIMEOUT, SBSLLM_BROWSER_LOCK_TIMEOUT
  SETTLE_AFTER_RESTART  seconds to wait after tabs open before binding sockets
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, "/var/home/fra/dev/sbsllm")

# Playwright does not forward our display variables; browser.py (commit 83c5a94)
# copies DISPLAY/WAYLAND_DISPLAY/XAUTHORITY/XDG_RUNTIME_DIR/XDG_SESSION_TYPE, so
# they must be set on THIS process before the browser launches. XAUTHORITY's
# cookie filename changes with each login, so discover it rather than hardcode.
if "XAUTHORITY" not in os.environ or not os.path.isfile(os.environ.get("XAUTHORITY", "")):
    import glob as _glob

    cands = sorted(_glob.glob("/run/user/1000/xauth_*"))
    if cands:
        os.environ["XAUTHORITY"] = cands[0]

from sbsllm.browser import ensure_browser  # noqa: E402
from sbsllm.cli import _open_tabs, _start_server  # noqa: E402
from sbsllm.config import load_config  # noqa: E402
from sbsllm.server import create_server  # noqa: E402
from sbsllm.sites import get_site  # noqa: E402

MODELS = [m.strip() for m in os.environ.get(
    "GATEWAY_MODELS",
    "claude,mistral,zai,meta,qwen,grok,google,kimi,tencent,copilot",
).split(",") if m.strip()]

HOST = os.environ.get("GATEWAY_HOST", "127.0.0.1")
PORT = int(os.environ.get("GATEWAY_PORT", "8079"))


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def main() -> int:
    cfg = Path("/var/home/fra/dev/sbsllm/config.yaml")
    config = load_config(cfg if cfg.exists() else None)
    browser_bin = config.chrome_bin
    user_data_dir = config.user_data_dir

    # Reuse a running Chromium if possible; only launch when absent.
    try:
        ensure_browser(browser_bin, user_data_dir)
        print("[gateway] browser ensured", flush=True)
    except Exception as e:  # noqa: BLE001
        print(f"[gateway] ERROR ensure_browser: {e}", file=sys.stderr, flush=True)
        return 1

    urls = []
    for chat in MODELS:
        site = get_site(chat)
        if not site or "url" not in site:
            print(f"[gateway] unknown site '{chat}', skipping", file=sys.stderr, flush=True)
            urls.append(None)
            continue
        urls.append(site["url"])

    print(f"[gateway] opening {len(MODELS)} tabs...", flush=True)
    pairs = [(c, u) for c, u in zip(MODELS, urls) if u]
    pages = _open_tabs([c for c, _ in pairs], [u for _, u in pairs], browser_bin, user_data_dir)

    successful = {chat: page for chat, page in zip([c for c, _ in pairs], pages) if page is not None}
    failed = [c for c, _ in pairs if c not in successful]
    if failed:
        print(f"[gateway] WARNING: tabs failed: {failed}", file=sys.stderr, flush=True)
    if not successful:
        print("[gateway] no tabs opened, exiting", file=sys.stderr, flush=True)
        return 1

    settle = _env_float("SETTLE_AFTER_RESTART", 0.0)
    if settle:
        print(f"[gateway] settling {settle:g}s before binding...", flush=True)
        import time
        time.sleep(settle)

    browser_timeout = _env_float("SBSLLM_BROWSER_TIMEOUT", config.browser_timeout)
    browser_lock_timeout = _env_float("SBSLLM_BROWSER_LOCK_TIMEOUT", config.browser_lock_timeout)
    first_token_timeout = _env_float("SBSLLM_FIRST_TOKEN_TIMEOUT", 1800.0)
    busy_patience = _env_float("SBSLLM_BUSY_PATIENCE", 600.0)

    server = create_server(
        model_map={chat: chat for chat in successful},
        tab_map=successful,
        host=HOST,
        port=PORT,
        browser_timeout=int(browser_timeout),
        browser_lock_timeout=int(browser_lock_timeout),
        response_idle_timeout=config.response_idle_timeout,
        thinking_patience=config.thinking_patience,
        duplicate_prompt_cooldown=config.duplicate_prompt_cooldown,
        busy_patience=busy_patience,
        first_token_timeout=first_token_timeout,
        # fill_gaps_v2.sh resets the tab to a fresh conversation through
        # /debug/navigate before asking the missing questions; without this the
        # reset 404s and the fill runs against the wedged conversation.
        debug_endpoints=config.debug_endpoints,
    )
    print(
        "[sbsllm_server] timeouts: "
        f"{{'first_token_timeout': {first_token_timeout:g}, "
        f"'busy_patience': {busy_patience:g}, "
        f"'browser_timeout': {browser_timeout:g}, "
        f"'browser_lock_timeout': {browser_lock_timeout:g}}}",
        flush=True,
    )

    thread = _start_server(server, announce=True)
    if thread is None:
        print("[gateway] server failed to start", file=sys.stderr, flush=True)
        return 1
    print("[gateway] server ready", flush=True)
    try:
        thread.join()
    except KeyboardInterrupt:
        print("\n[gateway] shutting down...", flush=True)
        server.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
