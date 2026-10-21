#!/usr/bin/env bash
# Benchmark all models on the Hosten endpoint (http://localhost:8079/v1)
# Runs ONE model at a time (sequential).
set -u
BASE="http://localhost:8079/v1"
KEY="dummy"
OUTDIR="results/hosten"
mkdir -p "$OUTDIR"

# Endpoint ID -> underlying model name (for reporting only)
declare -A MAP
MAP[claude]="claude-sonnet-5"
MAP[mistral]="mistral-medium-3.5"
MAP[zai]="glm-5.3-flash"
MAP[meta]="muse-spark-1.1"
MAP[qwen]="qwen-3.8-max"
MAP[grok]="grok-4.5"
MAP[google]="gemini-3.8-flash"
MAP[kimi]="kimi-k3"
MAP[copilot]="gpt-5.6"
# deepseek: NOT AVAILABLE

MODELS=(claude mistral zai meta qwen grok google kimi copilot)

for m in "${MODELS[@]}"; do
  echo "=== START $m (${MAP[$m]}) ==="
  python run_benchmark.py \
    --client openai \
    --model "$m" \
    --api-base "$BASE" \
    --api-key "$KEY" \
    --output "$OUTDIR" \
    --no-save-json 2>&1 \
    | tee "$OUTDIR/${m}.log"
  echo "=== END $m ==="
done
echo "ALL DONE"