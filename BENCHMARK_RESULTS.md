# Benchmark Results

## Overview

LLM performance on the MKULTRA Benchmark (40 questions: 30 single-choice, 10 multiple-choice).
Questions have weights: **1.0** for user-added questions (Q31-Q40) and **0.1** for original questions (Q1-Q30).

## Final Results (26 Models Tested)

### Via KiloCode API (13 models)

| Model | Overall | Weighted | Provider |
|-------|---------|----------|----------|
| poolside/laguna-s-2.1:free | 67.5% (27/40) | 62.3% | Poolside |
| inclusionai/ling-3.0-flash-vl:free | 67.5% (27/40) | 62.3% | InclusionAI |
| stepfun/step-3.7-flash:free | 70.0% (28/40) | 56.2% | StepFun |
| inclusionai/ling-3.0-flash-fin:free | 62.5% (25/40) | 53.8% | InclusionAI |
| nvidia/nemotron-3-ultra-550b-a55b:free | 77.5% (31/40) | 51.5% | NVIDIA |
| nex-agi/nex-n2.5-mini:free | 67.5% (27/40) | 48.5% | NexAGI |
| inclusionai/ling-3.0-flash-sante:free | 65.0% (26/40) | 47.7% | InclusionAI |
| gemini-3.5-flash-lite | 65.0% (26/40) | 47.7% | Google |
| meta/muse-glimmer-30b | 62.5% (25/40) | 46.9% | Meta |
| nvidia/nemotron-3.5-lightning:free | 55.0% (22/40) | 44.6% | NVIDIA |
| liquid/lfm-2.5-2.6b:free | 47.5% (19/40) | 42.3% | Liquid |
| gemini-flash-lite-latest | 65.0% (26/40) | 40.8% | Google |
| nex-agi/nex-n2.5-pro:free | 62.5% (25/40) | 40.0% | NexAGI |
| dots-studio/dots-3-note-preview:free | 60.0% (24/40) | 39.2% | Dots Studio |
| cohere/north-mini-code:free | 57.5% (23/40) | 38.5% | Cohere |
| nvidia/nemotron-3-super-120b-a12b | 57.5% (23/40) | 38.5% | NVIDIA |
| deepseek-ai/deepseek-v4-flash-0731 | 52.5% (21/40) | 16.2% | DeepSeek |

### Via Google AI Studio (3 models tested)

| Model | Overall | Weighted | Status |
|-------|---------|----------|--------|
| gemini-3.5-flash-lite | 65.0% (26/40) | 47.7% | ✓ Complete |
| gemini-flash-lite-latest | 65.0% (26/40) | 40.8% | ✓ Complete |
| gemini-3.8-flash | 0.0% (0/40) | 0.0% | ✗ Rate limited (429) |
| google/gemma-4-31b-it | - | - | ✗ Not available (404) |

### Via NVIDIA NIM / NGC (7 models tested)

| Model | Overall | Weighted | Failures | Status |
|-------|---------|----------|----------|--------|
| meta/muse-glimmer-30b | 62.5% (25/40) | 46.9% | 0 | ✓ Complete |
| nvidia/nemotron-3-super-120b-a12b | 57.5% (23/40) | 38.5% | 0 | ✓ Complete |
| deepseek-ai/deepseek-v4-flash-0731 | 52.5% (21/40) | 16.2% | 11 | ⚠ Partial (timeouts) |
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
Poolside/laguna-s-2.1      ████████████████████████████████████████████░░░░░░░░  62.3%
ling-3.0-flash-vl          ████████████████████████████████████████████░░░░░░░░  62.3%
stepfun-step-3.7-flash     ██████████████████████████████████████████████░░░░░░░░  56.2%
ling-3.0-flash-fin         ████████████████████████████████████████████████░░░░░░  53.8%
nemotron-3-ultra-550b      █████████████████████████████████████████████████░░░░░  51.5%
nex-n2.5-mini              ██████████████████████████████████████████████████  48.5%
ling-3.0-flash-sante       ███████████████████████████████████████████████████░░  47.7%
gemini-3.5-flash-lite      ███████████████████████████████████████████████████░░  47.7%
muse-glimmer-30b           ███████████████████████████████████████████████████░░  46.9%
nemotron-3.5-lightning     █████████████████████████████████████████████████████  44.6%
lfm-2.5-2.6b               ██████████████████████████████████████████████████████  42.3%
gemini-flash-lite-latest   ██████████████████████████████████████████████████████  40.8%
nex-n2.5-pro               ██████████████████████████████████████████████████████░░  40.0%
dots-3-note-preview        █████████████████████████████████████████████████████░░░  39.2%
north-mini-code            █████████████████████████████████████████████████████░░░  38.5%
nemotron-super-120b        █████████████████████████████████████████████████████░░░  38.5%
deepseek-v4-flash          █████████████████████████                           16.2%

                       0%  10%  20%  30%  40%  50%  60%  70%  80%  90% 100%
                          ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────|
```

Legend: █ = 2% of 100%

## Key Findings

- **poolside/laguna-s-2.1** and **inclusionai/ling-3.0-flash-vl** tie for highest weighted score (62.3%)
- **nvidia/nemotron-3-ultra-550b-a55b** has the highest overall accuracy (77.5%) but a lower weighted score (51.5%) due to the scoring weighting heavily toward user-added questions (Q31-Q40)
- **gemini-3.5-flash-lite** (65% overall, 47.7% weighted) is the best-performing Google model tested
- **meta/muse-glimmer-30b** (62.5% overall, 46.9% weighted) is the best-performing NVIDIA-direct model
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