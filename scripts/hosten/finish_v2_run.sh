#!/usr/bin/env bash
# Finish the dataset v2.0 benchmark run.
#
# One model at a time (concurrent runs caused 504s and tripped per-site rate
# limits). Each attempt runs through run_one_v2.sh, which aborts early when the
# live tab shows a throttle message (the gateway would otherwise stall 30 min on
# first_token_timeout). Models that already have a results_<m>_<ts>.json are
# skipped. Retries stop at the deadline.
set -u
cd /var/home/fra/dev/mkubench || exit 1
OUTDIR="results/hosten_v2"
BACKOFF=${BACKOFF:-900}          # seconds between failed attempts
DEADLINE_MIN=${DEADLINE_MIN:-200}
LOG=results/logs/finish_v2_run.log
mkdir -p results/logs
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_ONE="$HERE/run_one_v2.sh"
VALID="$HERE/v2_valid.py"

DEADLINE=$(( $(date +%s) + DEADLINE_MIN * 60 ))
log() { echo "$(date '+%H:%M:%S') $*" >> "$LOG"; }

# Complete = all 40 questions answered with no blank responses (v2_valid.py).
is_complete() {
  /usr/bin/python3 "$VALID" "$1" >/dev/null 2>&1
}

MODELS=${*}
[ -z "$MODELS" ] && MODELS="mistral kimi zai grok"

: > "$LOG"
log "finisher starting; models: $MODELS; deadline $(date -d @"$DEADLINE" '+%H:%M:%S')"

for m in $MODELS; do
  if is_complete "$m"; then
    log "SKIP $m (already complete)"
    continue
  fi
  attempt=0
  while [ "$(date +%s)" -lt "$DEADLINE" ]; do
    if is_complete "$m"; then
      log "DONE $m"
      break
    fi
    attempt=$((attempt + 1))
    left=$(( (DEADLINE - $(date +%s)) / 60 ))
    log "START $m attempt $attempt (deadline in ${left}min)"
    "$RUN_ONE" "$m" "results/logs/run_one_${m}.log"
    rc=$?
    if is_complete "$m"; then
      log "DONE $m after $attempt attempt(s)"
      break
    fi
    lastq=$(grep -aoE 'Evaluating Q[0-9]+' "results/logs/run_one_${m}.log" 2>/dev/null | tail -1)
    log "$m attempt $attempt rc=$rc $lastq; backoff ${BACKOFF}s"
    sleep "$BACKOFF"
  done
  is_complete "$m" || log "GAVE UP on $m at deadline"
done
log "finisher exiting"
