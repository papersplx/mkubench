# Benchmark Results

## Summary

| Metric | Value |
|--------|-------|
| Total models tested | 27 |
| Models with complete results | 15 |
| Average weighted accuracy | **48.2%** |
| Average overall accuracy | 63.5% |
| Average accuracy on user-generated questions (Q31-Q40) | 41.3% |
| Average accuracy on original questions (Q1-Q30) | 70.9% |
| Best weighted score | poolside/laguna-s-2.1:free (62.3%) |
| Best overall accuracy | nvidia/nemotron-3-ultra-550b-a55b:free (77.5%) |

**Weighting:** User-added questions (Q31-Q40) have weight **1.0**, original questions (Q1-Q30) have weight **0.1**. Total weighted possible: 13.0 points (10.0 from user-generated + 3.0 from original).

## Leaderboard

| Rank | Model | Provider | Weighted | Overall | Q31-Q40 | Q1-Q30 |
|------|-------|----------|----------|---------|---------|--------|
| 1 | poolside/laguna-s-2.1:free | KiloCode/Poolside | **62.3%** | 67.5% | 60.0% | 70.0% |
| 2 | inclusionai/ling-3.0-flash-vl:free | KiloCode/InclusionAI | **62.3%** | 67.5% | 60.0% | 70.0% |
| 3 | stepfun/step-3.7-flash:free | KiloCode/StepFun | 56.2% | 70.0% | 50.0% | 76.7% |
| 4 | inclusionai/ling-3.0-flash-fin:free | KiloCode/InclusionAI | 53.8% | 62.5% | 50.0% | 66.7% |
| 5 | nvidia/nemotron-3-ultra-550b-a55b:free | KiloCode/NVIDIA | 51.5% | 77.5% | 40.0% | 86.7% |
| 6 | nex-agi/nex-n2.5-mini:free | KiloCode/NexAGI | 48.5% | 67.5% | 40.0% | 76.7% |
| 7 | gemini-3.5-flash-lite | Google AI Studio | 47.7% | 65.0% | 40.0% | 73.3% |
| 8 | inclusionai/ling-3.0-flash-sante:free | KiloCode/InclusionAI | 47.7% | 65.0% | 40.0% | 73.3% |
| 9 | meta/muse-glimmer-30b | NVIDIA NIM | 46.9% | 62.5% | 40.0% | 70.0% |
| 10 | nvidia/nemotron-3.5-lightning:free | KiloCode/NVIDIA | 44.6% | 55.0% | 40.0% | 60.0% |
| 11 | liquid/lfm-2.5-2.6b:free | KiloCode/Liquid | 42.3% | 47.5% | 40.0% | 50.0% |
| 12 | gemini-3.5-flash-lite | Google AI Studio | 40.8% | 65.0% | 30.0% | 76.7% |
| 13 | nex-agi/nex-n2.5-pro:free | KiloCode/NexAGI | 40.0% | 62.5% | 30.0% | 73.3% |
| 14 | nvidia/nemotron-3-super-120b-a12b | NVIDIA NIM | 38.5% | 57.5% | 30.0% | 66.7% |
| 15 | cohere/north-mini-code:free | KiloCode/Cohere | 38.5% | 57.5% | 30.0% | 66.7% |
| 16 | dots-studio/dots-3-note-preview:free | KiloCode/Dots Studio | 39.2% | 60.0% | 30.0% | 70.0% |
| 17 | deepseek-ai/deepseek-v4-flash-0731 | NVIDIA NIM | 16.2% | 52.5% | 0.0% | 70.0% |

*Models with failures (404/timeout/rate-limited) are excluded from this table.*

## Accuracy Histogram (Weighted)

```
Poolside/laguna-s-2.1      ████████████████████████████████████████████░░░░░░░░  62.3%
ling-3.0-flash-vl          ████████████████████████████████████████████░░░░░░░░  62.3%
stepfun-step-3.7-flash     ██████████████████████████████████████████████░░░░░░░░  56.2%
ling-3.0-flash-fin         ████████████████████████████████████████████████░░░░░░  53.8%
nemotron-3-ultra-550b      █████████████████████████████████████████████████░░░░░  51.5%
nex-n2.5-mini              ██████████████████████████████████████████████████  48.5%
gemini-3.5-flash-lite      ███████████████████████████████████████████████████░░  47.7%
ling-3.0-flash-sante       ███████████████████████████████████████████████████░░  47.7%
muse-glimmer-30b           ███████████████████████████████████████████████████░░  46.9%
nemotron-3.5-lightning     █████████████████████████████████████████████████████  44.6%
lfm-2.5-2.6b               ██████████████████████████████████████████████████████  42.3%
gemini-3.5-flash-lite      ██████████████████████████████████████████████████████  40.8%
nex-n2.5-pro               ██████████████████████████████████████████████████████░░  40.0%
dots-3-note-preview        █████████████████████████████████████████████████████░░░  39.2%
north-mini-code            █████████████████████████████████████████████████████░░░  38.5%
nemotron-super-120b        █████████████████████████████████████████████████████░░░  38.5%
deepseek-v4-flash          █████████████████████████                           16.2%

                       0%  10%  20%  30%  40%  50%  60%  70%  80%  90% 100%
                          ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────|
```

Legend: █ = 2% of 100%

## Performance by Provider

### KiloCode API (13 models)

| Model | Weighted | Overall | Q31-Q40 | Q1-Q30 |
|-------|----------|---------|---------|--------|
| poolside/laguna-s-2.1:free | 62.3% | 67.5% | 60.0% | 70.0% |
| inclusionai/ling-3.0-flash-vl:free | 62.3% | 67.5% | 60.0% | 70.0% |
| stepfun/step-3.7-flash:free | 56.2% | 70.0% | 50.0% | 76.7% |
| inclusionai/ling-3.0-flash-fin:free | 53.8% | 62.5% | 50.0% | 66.7% |
| nvidia/nemotron-3-ultra-550b-a55b:free | 51.5% | 77.5% | 40.0% | 86.7% |
| nex-agi/nex-n2.5-mini:free | 48.5% | 67.5% | 40.0% | 76.7% |
| inclusionai/ling-3.0-flash-sante:free | 47.7% | 65.0% | 40.0% | 73.3% |
| nvidia/nemotron-3.5-lightning:free | 44.6% | 55.0% | 40.0% | 60.0% |
| nex-agi/nex-n2.5-pro:free | 40.0% | 62.5% | 30.0% | 73.3% |
| liquid/lfm-2.5-2.6b:free | 42.3% | 47.5% | 40.0% | 50.0% |
| dots-studio/dots-3-note-preview:free | 39.2% | 60.0% | 30.0% | 70.0% |
| cohere/north-mini-code:free | 38.5% | 57.5% | 30.0% | 66.7% |

### Google AI Studio (2 models completed)

| Model | Weighted | Overall | Q31-Q40 | Q1-Q30 | Status |
|-------|----------|---------|---------|--------|--------|
| gemini-3.5-flash-lite | 47.7% | 65.0% | 40.0% | 73.3% | ✓ Complete |
| gemini-3.5-flash-lite | 40.8% | 65.0% | 30.0% | 76.7% | ✓ Complete |
| gemini-3.8-flash | - | - | - | - | ✗ Rate limited (429) |
| google/gemma-4-31b-it | - | - | - | - | ✗ Not available (404) |

### NVIDIA NIM (3 models completed)

| Model | Weighted | Overall | Q31-Q40 | Q1-Q30 | Status |
|-------|----------|---------|---------|--------|--------|
| meta/muse-glimmer-30b | 46.9% | 62.5% | 40.0% | 70.0% | ✓ Complete |
| nvidia/nemotron-3-super-120b-a12b | 38.5% | 57.5% | 30.0% | 66.7% | ✓ Complete |
| deepseek-ai/deepseek-v4-flash-0731 | 16.2% | 52.5% | 0.0% | 70.0% | ⚠ Partial (timeouts) |
| deepseek-ai/deepseek-coder-6.7b-instruct | 0.0% | 0.0% | 0.0% | 0.0% | ✗ Model not found (404) |
| deepseek-ai/deepseek-v4-pro-0813 | 0.0% | 0.0% | 0.0% | 0.0% | ✗ API timeouts |
| google/gemma-4-31b-it | 0.0% | 0.0% | 0.0% | 0.0% | ✗ API timeouts |
| ibm/granite-3.0-3b-a800m-instruct | 0.0% | 0.0% | 0.0% | 0.0% | ✗ Model not found (404) |
| ibm/granite-3.0-8b-instruct | 0.0% | 0.0% | 0.0% | 0.0% | ✗ Model not found (404) |
| meta/llama2-70b | 0.0% | 0.0% | 0.0% | 0.0% | ✗ Model not found (404) |
| minimaxai/minimax-m3 | 0.0% | 0.0% | 0.0% | 0.0% | ✗ Model deprecated (410) |
| moonshotai/kimi-k2.6 | 0.0% | 0.0% | 0.0% | 0.0% | ✗ Model not found (404) |
| moonshotai/kimi-k3 | 0.0% | 0.0% | 0.0% | 0.0% | ✗ Rate limited (429) |

## Key Findings

- **User-generated questions (Q31-Q40) are significantly harder** for models than original questions (Q1-Q30)
  - Average accuracy on Q31-Q40: **41.3%**
  - Average accuracy on Q1-Q30: **70.9%**
- **poolside/laguna-s-2.1** and **inclusionai/ling-3.0-flash-vl** tie for highest weighted score (62.3%) - both excel at user-generated questions
- **nvidia/nemotron-3-ultra-550b-a55b** has the highest overall accuracy (77.5%) and best Q1-Q30 accuracy (86.7%) but only 40% on Q31-Q40
- **gemini-3.5-flash-lite** (65% overall, 47.7% weighted) is the best-performing Google model tested
- Smaller models like **liquid/lfm-2.5-2.6b** (47.5%) show the benchmark is challenging
- Google models heavily rate-limited (429 errors) - gemini-3.8-flash unavailable
- Several NVIDIA NIM models returned 404 (not found) - model names may have changed or been removed from the catalog

## Hosten Gateway Results

The Hosten gateway (`http://localhost:8079/v1`) exposes 10 endpoint IDs, each routing to an underlying model. All 10 were benchmarked sequentially on the fixed dataset (`/tmp/mkultra_fixed.jsonl`, 40 questions, Q31-Q40 weighted 1.0, Q1-Q30 weighted 0.1).

| Endpoint ID | Underlying Model | Correct | Overall | Weighted | Q31-Q40 | Q1-Q30 | Status |
|-------------|------------------|---------|---------|----------|---------|--------|--------|
| `mistral` | mistral-medium-3.5 | 34/40 | 85.0% | 88.5% | 90.0% | 83.3% | ✓ Complete |
| `meta` | muse-spark-1.1 | 33/40 | 82.5% | 60.0% | 50.0% | 93.3% | ✓ Complete |
| `qwen` | qwen-3.8-max | 32/40 | 80.0% | 73.1% | 70.0% | 83.3% | ✓ Complete |
| `claude` | claude-sonnet-5 | 29/40 | 72.5% | 50.0% | 40.0% | 83.3% | ✓ Complete |
| `kimi` | kimi-k3 | 24/40 | 60.0% | 18.5% | 0.0% | 80.0% | ✓ Complete |
| `zai` | glm-5.3-flash | 20/40 | 50.0% | 15.4% | 0.0% | 66.7% | ✓ Complete |
| `grok` | grok-4.5 | 20/40 | 50.0% | 15.4% | 0.0% | 66.7% | ✓ Complete |
| `tencent` | hy4-preview | 15/40 | 37.5% | 32.3% | 30.0% | 40.0% | ✓ Complete |
| `google` | gemini-3.8-flash | 12/40 | 30.0% | 9.2% | 0.0% | 40.0% | ✓ Complete |
| `copilot` | gpt-5.6 | 0/40 | 0.0% | 0.0% | 0.0% | 0.0% | ✗ 502 Bad Gateway |

**Key observations:**
- **mistral-medium-3.5** is the top performer (85% overall, 88.5% weighted)
- **gpt-5.6** (copilot) returns 502 Bad Gateway on every chat completion — the underlying model is unavailable on the gateway, so no answers were collected
- Several models (zai, grok, google, kimi, copilot) failed all Q31-Q40 questions, typically due to endpoint timeouts
- Q1-Q30 accuracy is consistently higher than Q31-Q40 across all models

Per-model logs are in `results/hosten/{endpoint_id}.log`.

## Providers Tested

- **KiloCode API** (`https://api.kilo.ai/api/gateway/v1`) - 13 models from various providers (NVIDIA, StepFun, Poolside, InclusionAI, NexAGI, Cohere, Dots Studio, Liquid)
- **Google AI Studio** (`https://generativelanguage.googleapis.com/v1beta/openai/chat/completions`) - 2 models completed, 2 unavailable
- **NVIDIA NIM / NGC** (`https://integrate.api.nvidia.com/v1`) - 3 models completed, 9 unavailable or timed out

## How to Run

```bash
# Run against KiloCode (supports many models)
python run_all_models_benchmark.py

# Run remaining NVIDIA models (resumable)
python run_nvidia_remaining.py

# Run Google AI Studio models
python run_google_benchmark.py

# Run against Google AI Studio (OpenAI-compatible)
python run_benchmark.py --client openai --model gemini-3.5-flash-lite --api-key $GEMINI_API_KEY --api-base https://generativelanguage.googleapis.com/v1beta/openai

# Run against NVIDIA API
python run_benchmark.py --client openai --model nvidia/nemotron-3-super-120b-a12b --api-key $NVIDIA_API_KEY --api-base https://integrate.api.nvidia.com/v1

# Run against Gemini native API
python run_benchmark.py --client gemini --model gemini-2.5-flash --api-key $GEMINI_API_KEY

# Run against local Ollama
python run_benchmark.py --client ollama --model llama3
```

## Contributing

If you run this benchmark against additional models, please submit a PR with your results. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.