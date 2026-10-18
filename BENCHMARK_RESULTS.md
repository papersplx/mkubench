# Benchmark Results

## Summary

| Metric | Value |
|--------|-------|
| Total models tested | 36 |
| Models with complete results | 24 |
| Average weighted accuracy | **51.3%** |
| Average overall accuracy | 68.4% |
| Average accuracy on user-generated questions (Q31-Q40) | 43.8% |
| Average accuracy on original questions (Q1-Q30) | 76.7% |
| Best weighted score | mistral-medium-3.5 (89.2%) |
| Best overall accuracy | mistral-medium-3.5 (87.5%) |

**Weighting:** User-added questions (Q31-Q40) have weight **1.0**, original questions (Q1-Q30) have weight **0.1**. Total weighted possible: 13.0 points (10.0 from user-generated + 3.0 from original).

## Leaderboard

| Rank | Model | Provider | Correct | Overall | Weighted | Q31-Q40 | Q1-Q30 | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | mistral-medium-3.5 (`mistral`) | Hosten Gateway | 35/40 | 87.5% | **89.2%** | 90.0% | 86.7% | ✓ Complete |
| 2 | qwen-3.8-max (`qwen`) | Hosten Gateway | 32/40 | 80.0% | 73.1% | 70.0% | 83.3% | ✓ Complete |
| 3 | hy4-preview (`tencent`) | Hosten Gateway | 31/40 | 77.5% | 72.3% | 70.0% | 80.0% | ✓ Complete |
| 4 | poolside/laguna-s-2.1:free | KiloCode API | 27/40 | 67.5% | 62.3% | 60.0% | 70.0% | ✓ Complete |
| 5 | inclusionai/ling-3.0-flash-vl:free | KiloCode API | 27/40 | 67.5% | 62.3% | 60.0% | 70.0% | ✓ Complete |
| 6 | muse-spark-1.1 (`meta`) | Hosten Gateway | 33/40 | 82.5% | 60.0% | 50.0% | 93.3% | ✓ Complete |
| 7 | grok-4.5 (`grok`) | Hosten Gateway | 30/40 | 75.0% | 57.7% | 50.0% | 83.3% | ✓ Complete |
| 8 | stepfun/step-3.7-flash:free | KiloCode API | 28/40 | 70.0% | 56.2% | 50.0% | 76.7% | ✓ Complete |
| 9 | inclusionai/ling-3.0-flash-fin:free | KiloCode API | 25/40 | 62.5% | 53.8% | 50.0% | 66.7% | ✓ Complete |
| 10 | nvidia/nemotron-3-ultra-550b-a55b:free | KiloCode API | 31/40 | 77.5% | 51.5% | 40.0% | 90.0% | ✓ Complete |
| 11 | claude-sonnet-5 (`claude`) | Hosten Gateway | 30/40 | 75.0% | 50.8% | 40.0% | 86.7% | ✓ Complete |
| 12 | gpt-5.6 (`copilot`) | Hosten Gateway | 28/40 | 70.0% | 49.2% | 40.0% | 80.0% | ✓ Complete |
| 13 | nex-agi/nex-n2.5-mini:free | KiloCode API | 27/40 | 67.5% | 48.5% | 40.0% | 76.7% | ✓ Complete |
| 14 | inclusionai/ling-3.0-flash-sante:free | KiloCode API | 26/40 | 65.0% | 47.7% | 40.0% | 73.3% | ✓ Complete |
| 15 | gemini-3.5-flash-lite | Google AI Studio | 26/40 | 65.0% | 47.7% | 40.0% | 73.3% | ✓ Complete |
| 16 | meta/muse-glimmer-30b | NVIDIA NIM | 25/40 | 62.5% | 46.9% | 40.0% | 70.0% | ✓ Complete |
| 17 | nvidia/nemotron-3.5-lightning:free | KiloCode API | 22/40 | 55.0% | 44.6% | 40.0% | 60.0% | ✓ Complete |
| 18 | kimi-k3 (`kimi`) | Hosten Gateway | 29/40 | 72.5% | 43.1% | 30.0% | 86.7% | ✓ Complete |
| 19 | liquid/lfm-2.5-2.6b:free | KiloCode API | 19/40 | 47.5% | 42.3% | 40.0% | 50.0% | ✓ Complete |
| 20 | nex-agi/nex-n2.5-pro:free | KiloCode API | 25/40 | 62.5% | 40.0% | 30.0% | 73.3% | ✓ Complete |
| 21 | dots-studio/dots-3-note-preview:free | KiloCode API | 24/40 | 60.0% | 39.2% | 30.0% | 70.0% | ✓ Complete |
| 22 | nvidia/nemotron-3-super-120b-a12b | NVIDIA NIM | 23/40 | 57.5% | 38.5% | 30.0% | 66.7% | ✓ Complete |
| 23 | glm-5.3-flash (`zai`) | Hosten Gateway | 29/40 | 72.5% | 29.2% | 10.0% | 93.3% | ✓ Complete |
| 24 | gemini-3.8-flash (`google`) | Hosten Gateway | 25/40 | 62.5% | 26.2% | 10.0% | 80.0% | ✓ Complete |
| 25 | deepseek-ai/deepseek-v4-flash-0731 | NVIDIA NIM | 21/40 | 52.5% | 16.2% | 0.0% | 70.0% | ◐ Partial |

*The 11 models that failed outright (404/timeout/rate-limited) are excluded from this table and listed under Failed models below.*

## Accuracy Histogram (Weighted)

```
mistral-medium-3.5       █████████████████████████████████████████████░░░░░░░  89.2%
qwen-3.8-max             █████████████████████████████████████░░░░░░░░░░░░░░░  73.1%
hy4-preview              ████████████████████████████████████░░░░░░░░░░░░░░░░  72.3%
poolside/laguna-s-2.1:f  ███████████████████████████████░░░░░░░░░░░░░░░░░░░░░  62.3%
inclusionai/ling-3.0-fl  ███████████████████████████████░░░░░░░░░░░░░░░░░░░░░  62.3%
muse-spark-1.1           ██████████████████████████████░░░░░░░░░░░░░░░░░░░░░░  60.0%
grok-4.5                 █████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░  57.7%
stepfun/step-3.7-flash:  ████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░  56.2%
inclusionai/ling-3.0-fl  ███████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░  53.8%
nvidia/nemotron-3-ultra  ██████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░  51.5%
claude-sonnet-5          █████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░  50.8%
gpt-5.6                  █████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░  49.2%
nex-agi/nex-n2.5-mini:f  ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  48.5%
inclusionai/ling-3.0-fl  ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  47.7%
gemini-3.5-flash-lite    ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  47.7%
meta/muse-glimmer-30b    ███████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  46.9%
nvidia/nemotron-3.5-lig  ██████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  44.6%
kimi-k3                  ██████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  43.1%
liquid/lfm-2.5-2.6b:fre  █████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  42.3%
nex-agi/nex-n2.5-pro:fr  ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  40.0%
dots-studio/dots-3-note  ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  39.2%
nvidia/nemotron-3-super  ███████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  38.5%
glm-5.3-flash            ███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  29.2%
gemini-3.8-flash         █████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  26.2%
deepseek-ai/deepseek-v4  ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  16.2%

                        0%  10% 20% 30% 40% 50% 60% 70% 80% 90% 100%
                          ├┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
```

Legend: █ = 2% of 100%

## Performance by Provider

Every model with a usable answer is already ranked in the single leaderboard above, so per-provider score tables would just duplicate it. Instead:

- **Hosten Gateway** - 10 tested, 10 complete (endpoints `claude`, `mistral`, `zai`, `meta`, `qwen`, `grok`, `google`, `kimi`, `tencent`, `copilot`)
- **KiloCode API** - 11 tested, 11 complete
- **Google AI Studio** - 3 tested, 1 complete
- **NVIDIA NIM** - 12 tested, 3 complete

### Failed models

Excluded from the leaderboard; kept here for reproducibility of the gaps.

| Model | Provider | Reason |
|---|---|---|
| deepseek-ai/deepseek-coder-6.7b-instruct | NVIDIA NIM | Model not found (404) |
| deepseek-ai/deepseek-v4-pro-0813 | NVIDIA NIM | API timeouts |
| google/gemma-4-31b-it | NVIDIA NIM | API timeouts |
| google/gemma-4-31b-it | Google AI Studio | Not available (404) |
| ibm/granite-3.0-3b-a800m-instruct | NVIDIA NIM | Model not found (404) |
| ibm/granite-3.0-8b-instruct | NVIDIA NIM | Model not found (404) |
| meta/llama2-70b | NVIDIA NIM | Model not found (404) |
| minimaxai/minimax-m3 | NVIDIA NIM | Model deprecated (410) |
| moonshotai/kimi-k2.6 | NVIDIA NIM | Model not found (404) |
| moonshotai/kimi-k3 | NVIDIA NIM | Rate limited (429) |
| gemini-3.8-flash | Google AI Studio | Rate limited (429) — separately complete as the `google` Hosten endpoint |

## Key Findings

- **User-generated questions (Q31-Q40) are significantly harder** for models than original questions (Q1-Q30)
  - Average accuracy on Q31-Q40: **43.8%**
  - Average accuracy on Q1-Q30: **76.7%**
- **mistral-medium-3.5** (Hosten endpoint `mistral`) has both the highest weighted (89.2%) and overall (87.5%) accuracy of all 36 tested models
- The top 3 weighted models are all Hosten endpoints (`mistral`, `qwen`, `tencent`), ahead of the best external API model (**poolside/laguna-s-2.1**, 62.3%)
- **nvidia/nemotron-3-ultra-550b-a55b** has the best Q1-Q30 accuracy (90.0%) among external models but only 40% on Q31-Q40
- Hosten endpoints span the full range: same gateway hosts the weakest complete model too (`google`/gemini-3.8-flash, 26.2% weighted, 10% on Q31-Q40)
- Google models heavily rate-limited (429 errors) - gemini-3.8-flash unavailable via Google AI Studio (it is separately complete as the `google` Hosten endpoint)
- Several NVIDIA NIM models returned 404 (not found) - model names may have changed or been removed from the catalog

## Hosten Gateway Results

The Hosten gateway (`http://localhost:8079/v1`) exposes 10 endpoint IDs, each routing to an underlying model, all scored on the same fixed 40-question dataset and ranked together with the external API models in the leaderboard above:

| Endpoint ID | Underlying Model |
|-------------|------------------|
| `mistral` | mistral-medium-3.5 |
| `meta` | muse-spark-1.1 |
| `qwen` | qwen-3.8-max |
| `claude` | claude-sonnet-5 |
| `kimi` | kimi-k3 |
| `zai` | glm-5.3-flash |
| `grok` | grok-4.5 |
| `tencent` | hy4-preview |
| `google` | gemini-3.8-flash |
| `copilot` | gpt-5.6 |

Per-question answers are in `results/hosten/recovered_answers.jsonl`; per-model request logs are in `results/hosten/{endpoint_id}.log`.

## Providers Tested

- **Hosten Gateway** (`http://localhost:8079/v1`) - 10 endpoint IDs, each routing to an underlying model, all complete (see Hosten Gateway Results above)
- **KiloCode API** (`https://api.kilo.ai/api/gateway/v1`) - 11 models from various providers (NVIDIA, StepFun, Poolside, InclusionAI, NexAGI, Liquid, Dots Studio), all complete
- **Google AI Studio** (`https://generativelanguage.googleapis.com/v1beta/openai/chat/completions`) - 3 tested, 1 complete, 2 unavailable
- **NVIDIA NIM / NGC** (`https://integrate.api.nvidia.com/v1`) - 12 tested, 3 complete, 9 unavailable or timed out

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