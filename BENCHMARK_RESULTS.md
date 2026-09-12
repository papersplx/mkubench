# Benchmark Results

## Overview

LLM performance on the MKULTRA Benchmark (40 questions: 30 single-choice, 10 multiple-choice).
Questions have weights: **1.0** for user-added questions (Q31-Q40) and **0.25** for original questions (Q1-Q30).

## Final Results (26 Models Tested)

### Via KiloCode API (13 models)

| Model | Overall | Weighted | Provider |
|-------|---------|----------|----------|
| poolside/laguna-s-2.1:free | 67.5% (27/40) | 64.3% | Poolside |
| inclusionai/ling-3.0-flash-vl:free | 67.5% (27/40) | 64.3% | InclusionAI |
| stepfun/step-3.7-flash:free | 70.0% (28/40) | 61.4% | StepFun |
| nvidia/nemotron-3-ultra-550b-a55b:free | 77.5% (31/40) | 61.4% | NVIDIA |
| inclusionai/ling-3.0-flash-fin:free | 62.5% (25/40) | 57.1% | InclusionAI |
| nex-agi/nex-n2.5-mini:free | 67.5% (27/40) | 55.7% | NexAGI |
| inclusionai/ling-3.0-flash-sante:free | 65.0% (26/40) | 54.3% | InclusionAI |
| gemini-3.5-flash-lite | 65.0% (26/40) | 54.3% | Google |
| meta/muse-glimmer-30b | 62.5% (25/40) | 52.9% | Meta |
| gemini-flash-lite-latest | 65.0% (26/40) | 50.0% | Google |
| nex-agi/nex-n2.5-pro:free | 62.5% (25/40) | 48.6% | NexAGI |
| nvidia/nemotron-3.5-lightning:free | 55.0% (22/40) | 48.6% | NVIDIA |
| dots-studio/dots-3-note-preview:free | 60.0% (24/40) | 47.1% | Dots Studio |
| nvidia/nemotron-3-super-120b-a12b:free | 57.5% (23/40) | 45.7% | NVIDIA |
| cohere/north-mini-code:free | 57.5% (23/40) | 45.7% | Cohere |
| liquid/lfm-2.5-2.6b:free | 47.5% (19/40) | 44.3% | Liquid |
| deepseek-ai/deepseek-v4-flash-0731 | 52.5% (21/40) | 30.0% | DeepSeek |

### Via Google AI Studio (3 models tested)

| Model | Overall | Weighted | Status |
|-------|---------|----------|--------|
| gemini-3.5-flash-lite | 65.0% (26/40) | 54.3% | ✓ Complete |
| gemini-flash-lite-latest | 65.0% (26/40) | 50.0% | ✓ Complete |
| gemini-3.8-flash | 0.0% (0/40) | 0.0% | ✗ Rate limited (429) |
| google/gemma-4-31b-it | - | - | ✗ Not available (404) |

### Via NVIDIA NIM / NGC (7 models tested)

| Model | Overall | Weighted | Failures | Status |
|-------|---------|----------|----------|--------|
| meta/muse-glimmer-30b | 62.5% (25/40) | 52.9% | 0 | ✓ Complete |
| nvidia/nemotron-3-super-120b-a12b | 57.5% (23/40) | 45.7% | 0 | ✓ Complete |
| deepseek-ai/deepseek-v4-flash-0731 | 52.5% (21/40) | 30.0% | 11 | ⚠ Partial (timeouts) |
| deepseek-ai/deepseek-coder-6.7b-instruct | 0.0% (0/40) | 0.0% | 40 | ✗ Model not found (404) |
| deepseek-ai/deepseek-v4-pro-0813 | 0.0% (0/40) | 0.0% | 40 | ✗ API timeouts |
| google/gemma-4-31b-it | 0.0% (0/40) | 0.0% | 40 | ✗ API timeouts |
| ibm/granite-3.0-3b-a800m-instruct | 0.0% (0/40) | 0.0% | 40 | ✗ Model not found (404) |
| ibm/granite-3.0-8b-instruct | 0.0% (0/40) | 0.0% | 40 | ✗ Model not found (404) |
| meta/llama2-70b | 0.0% (0/40) | 0.0% | 40 | ✗ Model not found (404) |
| minimaxai/minimax-m3 | 0.0% (0/40) | 0.0% | 40 | ✗ Model deprecated (410) |
| moonshotai/kimi-k2.6 | 0.0% (0/40) | 0.0% | 40 | ✗ Model not found (404) |
| moonshotai/kimi-k3 | 0.0% (0/40) | 0.0% | 40 | ✗ Rate limited (429) |

## Accuracy Histogram (Weighted)

```
Poolside/laguna-s-2.1      █████████████████████████████████████████░░░░░░░░░░  64.3%
ling-3.0-flash-vl          █████████████████████████████████████████░░░░░░░░░░  64.3%
stepfun-step-3.7-flash     ███████████████████████████████████████████░░░░░░░░  61.4%
nemotron-3-ultra-550b      ███████████████████████████████████████████░░░░░░░░  61.4%
ling-3.0-flash-fin         ████████████████████████████████████████████░░░░░░░░  57.1%
nex-n2.5-mini              █████████████████████████████████████████████░░░░░░  55.7%
ling-3.0-flash-sante       █████████████████████████████████████████████░░░░░░  54.3%
gemini-3.5-flash-lite      █████████████████████████████████████████████░░░░░░  54.3%
muse-glimmer-30b           ██████████████████████████████████████████████░░░░░  52.9%
gemini-flash-lite-latest   ███████████████████████████████████████████████░░░░  50.0%
nex-n2.5-pro               ███████████████████████████████████████████████░░░░  48.6%
nemotron-3.5-lightning     ███████████████████████████████████████████████░░░░  48.6%
north-mini-code            ███████████████████████████████████████████████░░░░  48.6%
dots-3-note-preview        ████████████████████████████████████████████████░░░  47.1%
nemotron-super-120b        ████████████████████████████████████████████████░░░  45.7%
lfm-2.5-2.6b               █████████████████████████████████████████████████░░  44.3%
deepseek-v4-flash          ████████████████████████████████████████████████████  30.0%

                       0%  10%  20%  30%  40%  50%  60%  70%  80%  90% 100%
                          ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────|
```

Legend: █ = 2% of 100%

## Key Findings

- **nvidia/nemotron-3-ultra-550b-a55b** (77.5% overall, 61.4% weighted) performs best overall across all tested models
- **poolside/laguna-s-2.1** and **inclusionai/ling-3.0-flash-vl** tie for highest weighted score (64.3%)
- **gemini-3.5-flash-lite** (65% overall, 54.3% weighted) is the best-performing Google model tested
- **meta/muse-glimmer-30b** (62.5% overall, 52.9% weighted) is the best-performing NVIDIA-direct model
- Smaller models like **liquid/lfm-2.5-2.6b** (47.5%) show the benchmark is challenging
- Google models heavily rate-limited (429 errors) - gemini-3.8-flash unavailable
- Several NVIDIA NIM models returned 404 (not found) - model names may have changed or been removed from the catalog
- DeepSeek models on NVIDIA NIM experienced significant API timeouts, resulting in partial results

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