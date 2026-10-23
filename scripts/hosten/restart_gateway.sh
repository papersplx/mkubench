#!/usr/bin/env bash
# Restart the mkubench gateway wrapper with the benchmark's timeouts.
# Usage: restart_gateway.sh [--wait]
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
LOG="$REPO/results/logs/sbsllm.log"
export XAUTHORITY="$(ls /run/user/1000/xauth_* 2>/dev/null | head -1)"
export DISPLAY=:0
export WAYLAND_DISPLAY=wayland-0
export XDG_RUNTIME_DIR=/run/user/1000
export SBSLLM_FIRST_TOKEN_TIMEOUT=300
export SBSLLM_BUSY_PATIENCE=300
export SBSLLM_BROWSER_TIMEOUT=1800
export SBSLLM_BROWSER_LOCK_TIMEOUT=1800
# Fresh tabs need a settle window before they accept input, else NO_MARKED_INPUT.
export SETTLE_AFTER_RESTART="${SETTLE_AFTER_RESTART:-90}"

# Kill any previous gateway WITHOUT self-matching. `pkill -f` matches the full
# cmdline, and this script's own cmdline is "bash .../restart_gateway.sh", so a
# pattern containing the literal "restart_gateway" would SIGTERM the script
# itself before it ever reached the launch below (the bracket trick only stops
# pkill matching its own pkill process, not the parent script). Kill by the
# server's script name only.
pkill -f 'sbsllm_serve[r]' 2>/dev/null
# Also the plain CLI gateway (`sbsllm --server --port 8079`): the pattern above
# does not match it, so it would keep port 8079 bound and the browser profile
# locked, and the new gateway could neither bind nor open its tabs.
pkill -f 'sbsllm --serve[r]' 2>/dev/null
sleep 2

# The Chromium instance is a child of the old gateway.  SIGTERM gives the
# gateway no chance to tear the browser down, so the profile directory stays
# locked (the new gateway then fails to open its tabs).  Release the profile
# explicitly and wait until it is free.
pkill -f 'sbsllm/chrom[e]' 2>/dev/null
for _ in $(seq 1 30); do
  grep -als 'sbsllm/chrome' /proc/[0-9]*/cmdline >/dev/null 2>&1 || break
  sleep 2
done

nohup setsid /usr/bin/python3 "$HERE/sbsllm_server.py" >> "$LOG" 2>&1 &
echo "gateway starting, log: $LOG"

if [ "${1:-}" = "--wait" ]; then
  for i in $(seq 1 60); do
    if curl -s -m 3 http://localhost:8079/v1/models | grep -q '"data"'; then
      echo "gateway ready"
      exit 0
    fi
    sleep 10
  done
  echo "gateway NOT ready after 600s"
  exit 1
fi
