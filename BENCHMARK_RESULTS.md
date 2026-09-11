# Benchmark Results

## Overview

LLM performance on the MKULTRA Benchmark (40 questions: 30 single-choice, 10 multiple-choice).
Questions have weights: **1.0** for user-added questions (Q31-Q40) and **0.5** for original questions (Q1-Q30).

## Final Results (13 Models Tested)

### Via KiloCode API (12 models)

| Model | Overall | Weighted | Provider |
|-------|---------|----------|----------|
| nvidia/nemotron-3-ultra-550b-a55b:free | 77.5% (31/40) | 70.0% | NVIDIA |
| stepfun/step-3.7-flash:free | 70.0% (28/40) | 66.0% | StepFun |
| poolside/laguna-s-2.1:free | 67.5% (27/40) | 66.0% | Poolside |
| inclusionai/ling-3.0-flash-vl:free | 67.5% (27/40) | 66.0% | InclusionAI |
| kilo-auto/free | 67.5% (27/40) | 64.0% | KiloCode |
| nex-agi/nex-n2.5-mini:free | 67.5% (27/40) | 62.0% | NexAGI |
| inclusionai/ling-3.0-flash-sante:free | 65.0% (26/40) | 60.0% | InclusionAI |
| inclusionai/ling-3.0-flash-fin:free | 62.5% (25/40) | 60.0% | InclusionAI |
| nex-agi/nex-n2.5-pro:free | 62.5% (25/40) | 56.0% | NexAGI |
| dots-studio/dots-3-note-preview:free | 60.0% (24/40) | 54.0% | Dots Studio |
| nvidia/nemotron-3.5-lightning:free | 55.0% (22/40) | 52.0% | NVIDIA |
| liquid/lfm-2.5-2.6b:free | 47.5% (19/40) | 46.0% | Liquid |

### Via Google AI Studio (1 model)

| Model | Overall | Weighted | Status |
|-------|---------|----------|--------|
| gemini-3.5-flash-lite | 62.5% (25/40) | 58.0% | ✓ Complete |
| gemini-3.8-flash | 0.0% (0/40) | 0.0% | ✗ Rate limited |
| gemma-4-31b-it | - | - | ✗ Not tested |

## Accuracy Histogram (Weighted)

```
nemotron-3-ultra-550b  ████████████████████████████████████████████████░░░░░░░░░░  70.0%
stepfun-step-3.7-flash ████████████████████████████████████████████████░░░░░░░░░░  66.0%
laguna-s-2.1           ████████████████████████████████████████████████░░░░░░░░░░  66.0%
ling-3.0-flash-vl      ████████████████████████████████████████████████░░░░░░░░░░  66.0%
kilo-auto              █████████████████████████████████████████████░░░░░░░░░░░░  64.0%
nex-n2.5-mini          ████████████████████████████████████████████░░░░░░░░░░░░░░  62.0%
ling-3.0-flash-sante   ███████████████████████████████████████████░░░░░░░░░░░░░  60.0%
ling-3.0-flash-fin     ███████████████████████████████████████████░░░░░░░░░░░░░  60.0%
nex-n2.5-pro           █████████████████████████████████████████░░░░░░░░░░░░░░░░░  56.0%
dots-3-note-preview    ████████████████████████████████████████░░░░░░░░░░░░░░░░  54.0%
nemotron-3.5-lightning █████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░  52.0%
lfm-2.5-2.6b           ████████████████████████████████████░░░░░░░░░░░░░░░░░░░░  46.0%

                           0%   10%   20%   30%   40%   50%   60%   70%   80%   90%   100%
                            ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────|
```

## Key Findings

- **nvidia/nemotron-3-ultra-550b-a55b** (77.5% overall, 70% weighted) performs best
- **stepfun/step-3.7-flash** (70% overall, 66% weighted) shows strong performance
- **poolside/laguna-s-2.1** and **inclusionai/ling-3.0-flash-vl** tie at 67.5% overall
- **kilo-auto** (67.5% overall, 64% weighted) provides good auto-routing
- Smaller models like **liquid/lfm-2.5-2.6b** (47.5%) show the benchmark is challenging
- Google models heavily rate-limited (429 errors) - only gemini-3.5-flash-lite completed

## Providers Tested

- **KiloCode API** (`https://api.kilo.ai/api/gateway/v1`) - 12 models from various providers
- **Google AI Studio** (`https://generativelanguage.googleapis.com/v1beta/openai/chat/completions`) - 1 model completed

## How to Run

```bash
# Run against KiloCode (supports many models)
python run_all_models_benchmark.py

# Run Google models only
python run_google_benchmarks.py

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