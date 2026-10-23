#!/usr/bin/env bash
# Fill the dataset-v2.0 answer gaps of the hosten endpoints.
#
# The gateway keeps ONE long conversation per site tab, and the tabs wedge as
# that context grows (grok stopped answering at Q32, google left 18 blanks).
# Re-asking all 40 only grows the context further, so each attempt here:
#   1. resets the tab to its configured chat URL (a fresh conversation), then
#   2. asks ONLY the questions the model has not answered yet, then
#   3. merges that answer into the model's record.
# A reset keeps the same browser profile, so the site stays signed in.
#
# Usage: fill_gaps_v2.sh <model> [more models...]      (sequential, one tab)
set -u
cd /var/home/fra/dev/mkubench || exit 1
LOGDIR="results/logs"
mkdir -p "$LOGDIR"
# Prevent two fill_gaps_v2.sh instances (or two concurrent calls in one
# session) from touching the gateway's shared Chromium tab at once. The lock
# is fd-based and released automatically if this process dies.
LOCKFILE="$LOGDIR/fill.lock"
exec 9>"$LOCKFILE"
if ! flock -n 9; then
  echo "$(date '+%F %H:%M:%S') another fill is already running ($LOCKFILE held); skipping" \
    | tee -a "$LOGDIR/fill_gaps.log"
  exit 0
fi
ATTEMPTS="${ATTEMPTS:-3}"
BASE="http://localhost:8079/v1"
export DISPLAY="${DISPLAY:-:0}"

for MODEL in "$@"; do
  LOG="$LOGDIR/fill_${MODEL}.log"
  echo "=== $(date '+%F %H:%M:%S') fill $MODEL ===" | tee -a "$LOG"

  try=1
  while [ "$try" -le "$ATTEMPTS" ]; do
    if /usr/bin/python3 scripts/hosten/v2_valid.py "$MODEL" >/dev/null 2>&1; then
      echo "$MODEL: COMPLETE already" | tee -a "$LOG"
      break
    fi
    echo "$(date '+%F %H:%M:%S') attempt $try: compute missing questions" | tee -a "$LOG"
    /usr/bin/python3 scripts/hosten/ask_missing_v2.py "$MODEL" >>"$LOG" 2>&1 || {
      echo "attempt $try: cannot compute missing questions" | tee -a "$LOG"
    }
    MISS="dataset/mkultra_missing_${MODEL}.jsonl"
    if [ ! -s "$MISS" ]; then
      echo "attempt $try: no missing-questions file ($MISS)" | tee -a "$LOG"
      try=$((try+1))
      continue
    fi
    NQ=$(grep -c . "$MISS")
    # Some sites drop the FIRST question of a session (the page is not warm
    # yet): tencent's Q1 came back empty in every run only because it was
    # always asked first. WARMUP=<id> prepends an already-answered question so
    # the real ones are asked on a warm page. Its answer is a real answer to
    # the same question, so the merge may take it - that is fine.
    if [ -n "${WARMUP:-}" ]; then
      /usr/bin/python3 - "$WARMUP" "$MISS" >>"$LOG" 2>&1 <<'PY'
import json
import sys

qid, miss = int(sys.argv[1]), sys.argv[2]
ds = "/var/home/fra/dev/mkubench/dataset/mkultra_benchmark.jsonl"
warm = None
for line in open(ds):
    if line.strip():
        q = json.loads(line)
        if q["id"] == qid:
            warm = line
            break
if warm is None:
    print(f"  warmup Q{qid} not found in the dataset")
    sys.exit(0)
rows = [warm] + [l for l in open(miss) if l.strip()]
with open(miss, "w") as fh:
    fh.writelines(rows)
print(f"  warmup Q{qid} prepended")
PY
      NQ=$(grep -c . "$MISS")
    fi
    # A fresh conversation helps a lot: the sites slow down / stop answering as
    # one chat grows, which is what wedged the full runs. The gateway's
    # /debug/navigate (the tab reset) is only served when debug_endpoints is on,
    # so it is opt-in: RESET_TAB=1 fill_gaps_v2.sh ... ; without it the missing
    # questions are asked in the conversation the tab already has.
    if [ "${RESET_TAB:-0}" = "1" ]; then
      /usr/bin/python3 - "$MODEL" "$LOG" <<'PY' >>"$LOG" 2>&1
import sys
import time
import urllib.parse
import urllib.request

model, log = sys.argv[1], sys.argv[2]
sys.path.insert(0, "/home/fra/dev/sbsllm")
from sbsllm.sites import get_site  # noqa: E402

url = (get_site(model) or {}).get("url")
if not url:
    print(f"  no configured URL for {model}; skipping reset")
    sys.exit(0)
api = "http://localhost:8079/debug/navigate?model=" + urllib.parse.quote(model) \
      + "&url=" + urllib.parse.quote(url)
try:
    with urllib.request.urlopen(api, timeout=120) as r:
        print(f"  tab reset -> {url} ({r.status})")
except Exception as e:  # noqa: BLE001
    detail = ""
    if hasattr(e, "read"):
        try:
            detail = e.read().decode(errors="replace")[:200]
        except Exception:
            detail = ""
    print(f"  tab reset failed: {type(e).__name__} {e} {detail}")
time.sleep(20)  # let the page settle before the first question
PY
    else
      echo "  (no tab reset: gateway debug endpoints are disabled)" | tee -a "$LOG"
    fi

    # Sites that throttle mid-conversation (tencent answers 3, then returns 200
    # with an empty body for the next 2) benefit from pacing: ask the questions
    # one at a time with a pause between them. run_benchmark's --delay only
    # affects an unused batch path, so the pacing has to live here.
    PAUSE="${PAUSE:-0}"
    echo "$(date '+%F %H:%M:%S') attempt $try: ask $NQ question(s) (pause ${PAUSE}s)" \
      | tee -a "$LOG"
    # Unique temp file so concurrent fill_gaps_v2.sh runs for the same model do
    # not clobber each other's per-question dataset (which produced "Extra data"
    # JSON parse errors and duplicate/blank rows). Cleaned up on exit.
    ONEDS="$(mktemp dataset/one_${MODEL}.XXXXXX.jsonl)"
    trap 'rm -f "$ONEDS"' EXIT
    if [ "$PAUSE" -gt 0 ] && [ "$NQ" -gt 1 ]; then
      n=0
      while IFS= read -r line; do
        printf '%s\n' "$line" > "$ONEDS"
        qid=$(/usr/bin/python3 -c "import json,sys;print(json.loads(sys.argv[1])['id'])" "$line")
        echo "$(date '+%F %H:%M:%S') ask Q$qid alone" >>"$LOG"
        python run_benchmark.py \
          --client openai \
          --model "$MODEL" \
          --api-base "$BASE" \
          --api-key dummy \
          --dataset "$ONEDS" \
          --output results/hosten_v2 \
          --timeout 2400 \
          --max-retries 1 \
          >>"$LOG" 2>&1
        n=$((n+1))
        if [ "$n" -lt "$NQ" ]; then sleep "$PAUSE"; fi
      done < "$MISS"
    else
      python run_benchmark.py \
        --client openai \
        --model "$MODEL" \
        --api-base "$BASE" \
        --api-key dummy \
        --dataset "$MISS" \
        --output results/hosten_v2 \
        --timeout 2400 \
        --max-retries 1 \
        >>"$LOG" 2>&1
    fi
    rc=$?
    echo "$(date '+%F %H:%M:%S') attempt $try rc=$rc" | tee -a "$LOG"
    try=$((try+1))
  done

  # Merge every answered attempt into one record, then re-parse it.
  /usr/bin/python3 scripts/hosten/merge_fill_v2.py "$MODEL" --apply 2>&1 | tee -a "$LOG"
  /usr/bin/python3 scripts/hosten/rescore_v2.py "$MODEL" 2>&1 | tee -a "$LOG"
  /usr/bin/python3 scripts/hosten/v2_valid.py "$MODEL" 2>&1 | tail -1 | tee -a "$LOG"
done
echo "=== $(date '+%F %H:%M:%S') fill-gaps DONE ===" | tee -a "$LOGDIR/fill_gaps.log"
