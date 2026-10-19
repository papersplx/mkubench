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
export SBSLLM_FIRST_TOKEN_TIMEOUT=1800
export SBSLLM_BUSY_PATIENCE=600
export SBSLLM_BROWSER_TIMEOUT=3000
export SBSLLM_BROWSER_LOCK_TIMEOUT=3000
# Fresh tabs need a settle window before they accept input, else NO_MARKED_INPUT.
export SETTLE_AFTER_RESTART="${SETTLE_AFTER_RESTART:-90}"

# Kill any previous gateway (bracketed regex so this script never self-matches).
for pat in 'sbsllm_serve[r]' 'restart_gatewa[y]' 'sbsllm_serve[r].py' 'recover.p[y]' 'recover_su[p]'; do
  pkill -f "$pat" 2>/dev/null
done
sleep 2

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
