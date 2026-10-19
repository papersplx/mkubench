#!/usr/bin/env bash
# Run ONE model on dataset v2.0, aborting early when the site rate-limits it.
#
# Usage: run_one_v2.sh <model>
# Exit codes: 0 = complete, 75 = site rate-limit detected, 1 = other failure.
#
# The gateway's first_token_timeout is 1800s, so a rate-limited site would stall
# an attempt for 30 minutes. This polls the live tab and bails out as soon as the
# page shows a known throttle message.
set -u
MODEL="$1"
OUTDIR="results/hosten_v2"
BASE="http://localhost:8079/v1"
# Logs live in the repo (results/ is gitignored) so they survive a reboot and
# stay next to the results they describe.
LOGDIR="results/logs"
mkdir -p "$LOGDIR"
LOGF="${2:-$LOGDIR/run_one_${MODEL}.log}"
WATCH="$LOGDIR/watch_${MODEL}.txt"
# Locate this script's directory so the helpers stay relocatable.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALID="$HERE/v2_valid.py"

cd /var/home/fra/dev/mkubench || exit 1

# A run only counts as complete when it has all 40 questions AND no empty
# responses; a rate-limited run leaves a 40-question file full of blanks.
if /usr/bin/python3 "$VALID" "$MODEL" >/dev/null 2>&1; then
  echo "already complete: $MODEL"
  exit 0
fi

: > "$LOGF"
python run_benchmark.py \
  --client openai \
  --model "$MODEL" \
  --api-base "$BASE" \
  --api-key dummy \
  --output "$OUTDIR" \
  --timeout 2400 \
  --max-retries 1 \
  >> "$LOGF" 2>&1 &
RUN_PID=$!
echo "$(date '+%H:%M:%S') started $MODEL (pid $RUN_PID)" >> "$LOGF"

# Site throttle phrases. NOTE: a bare "limit" false-positives on marketing copy
# ("Limited-time offer"), so match full phrases only.
RL="messages? limit reached|limit will reset|too many people|under heavy usage|high demand|rate.?limit|quota exceeded|try again later|peak hours|request failed|已达上限|请稍后|验证"

while kill -0 "$RUN_PID" 2>/dev/null; do
  sleep 45
  if /usr/bin/python3 "$VALID" "$MODEL" >/dev/null 2>&1; then
    wait "$RUN_PID" 2>/dev/null
    echo "$(date '+%H:%M:%S') COMPLETE $MODEL" >> "$LOGF"
    exit 0
  fi
  # Rate-limit watch on the live tab (bounded; a failed probe is not fatal).
  if timeout 60 /usr/bin/python3 "$HERE/tab_state.py" "$MODEL" 2>/dev/null \
      | grep -aiE "$RL" > "$WATCH"; then
    echo "$(date '+%H:%M:%S') RATE LIMIT detected for $MODEL:" >> "$LOGF"
    head -c 300 "$WATCH" >> "$LOGF"
    echo >> "$LOGF"
    kill "$RUN_PID" 2>/dev/null
    sleep 2
    kill -9 "$RUN_PID" 2>/dev/null
    # also kill any child spawned by the runner
    pkill -P "$RUN_PID" 2>/dev/null
    echo "$(date '+%H:%M:%S') aborted $MODEL (exit 75)" >> "$LOGF"
    exit 75
  fi
done
wait "$RUN_PID" 2>/dev/null
rc=$?
if /usr/bin/python3 "$VALID" "$MODEL" >/dev/null 2>&1; then
  echo "$(date '+%H:%M:%S') COMPLETE $MODEL (rc=$rc)" >> "$LOGF"
  exit 0
fi
echo "$(date '+%H:%M:%S') EXIT $MODEL rc=$rc without completion" >> "$LOGF"
exit 1
