#!/usr/bin/env bash
# Run one or more models on dataset v2.0 concurrently (one background process each).
# Each model gets its own log + result files, so a wedged tab only costs its own model.
# Usage: run_v2_parallel.sh meta grok kimi [qwen ...]
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

for m in "$@"; do
  # Resume-safe: skip a model that already produced a short summary file.
  summary_done=""
  for f in "$OUTDIR"/results_"$m"_*.json; do
    case "$f" in
      *_detailed.json) continue ;;
      *) [ -e "$f" ] && summary_done="$f" && break ;;
    esac
  done
  if [ -n "$summary_done" ]; then
    echo "=== SKIP $m (already complete) ==="
    continue
  fi
  echo "=== START $m (${MAP[$m]}) ==="
  nohup bash -c "python run_benchmark.py \
    --client openai \
    --model '$m' \
    --api-base '$BASE' \
    --api-key '$KEY' \
    --output '$OUTDIR' \
    --timeout 2400 \
    --max-retries 1 \
    2>&1 | tee '$OUTDIR/${m}.log'" > /dev/null 2>&1 &
  echo "  pid $! -> $OUTDIR/${m}.log"
done
echo "launched"
