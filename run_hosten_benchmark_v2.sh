#!/usr/bin/env bash
# Benchmark all models on the Hosten endpoint (http://localhost:8079/v1)
# Dataset v2.0 run. Sequential, per-model, results land in results/hosten_v2/.
#
# The client timeout is 2400s (not the 120s default): a client-side timeout does
# NOT cancel the server-side request, it just abandons it and the tab lock stays
# held for up to first_token_timeout, so the next question queues behind it.
# Waiting is strictly better than a 120s abandon-then-queue cascade.
set -u
BASE="http://localhost:8079/v1"
KEY="dummy"
OUTDIR="results/hosten_v2"
mkdir -p "$OUTDIR"

declare -A MAP
MAP[claude]="claude-sonnet-5"
MAP[mistral]="mistral-medium-3.5"
MAP[zai]="glm-5.3-flash"
MAP[meta]="muse-spark-1.1"
MAP[qwen]="qwen-3.8-max"
MAP[grok]="grok-4.5"
MAP[google]="gemini-3.8-flash"
MAP[kimi]="kimi-k3"
MAP[tencent]="hy4-preview"
MAP[copilot]="gpt-5.6"

MODELS=(${MODELS_OVERRIDE:-claude mistral zai meta qwen grok google kimi tencent copilot})

for m in "${MODELS[@]}"; do
  # Resume-safe: skip a model that already produced a short summary file.
  # (The *_detailed.json sibling holds the per-question dump and must NOT count as
  # a completed run - a run aborted after saving both files still left the short one.)
  summary_done=""
  for f in "$OUTDIR"/results_"$m"_*.json; do
    case "$f" in
      *_detailed.json) continue ;;
      *) [ -e "$f" ] && summary_done="$f" && break ;;
    esac
  done
  if [ -n "$summary_done" ]; then
    echo "=== SKIP $m (already complete: $summary_done) ==="
    continue
  fi
  echo "=== START $m (${MAP[$m]}) ==="
  python run_benchmark.py \
    --client openai \
    --model "$m" \
    --api-base "$BASE" \
    --api-key "$KEY" \
    --output "$OUTDIR" \
    --timeout 2400 \
    --max-retries 1 \
    2>&1 | tee "$OUTDIR/${m}.log"
  echo "=== END $m ==="
done
echo "ALL DONE"
