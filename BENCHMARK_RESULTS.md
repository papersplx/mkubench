# Benchmark Results

## Overview

LLM performance on the MKULTRA Benchmark (40 questions: 30 single-choice, 10 multiple-choice).
Questions have weights: **1.0** for user-added questions (Q31-Q40) and **0.5** for original questions (Q1-Q30).

## Final Results (12 Models Tested via KiloCode)

| Model | Overall Accuracy | Weighted Accuracy | Provider (via KiloCode) |
|-------|-----------------|-------------------|-------------------------|
| nvidia/nemotron-3-ultra-550b-a55b:free | 77.5% (31/40) | 70.0% | NVIDIA |
| stepfun/step-3.7-flash:free | 70.0% (28/40) | 66.0% | StepFun |
| poolside/laguna-s-2.1:free | 67.5% (27/40) | 66.0% | Poolside |
| inclusionai/ling-3.0-flash-vl:free | 67.5% (27/40) | 66.0% | InclusionAI |
| kilo-auto/free | 67.5% (27/40) | 64.0% | KiloCode Auto |
| nex-agi/nex-n2.5-mini:free | 67.5% (27/40) | 62.0% | NexAGI |
| inclusionai/ling-3.0-flash-sante:free | 65.0% (26/40) | 60.0% | InclusionAI |
| inclusionai/ling-3.0-flash-fin:free | 62.5% (25/40) | 60.0% | InclusionAI |
| nex-agi/nex-n2.5-pro:free | 62.5% (25/40) | 56.0% | NexAGI |
| dots-studio/dots-3-note-preview:free | 60.0% (24/40) | 54.0% | Dots Studio |
| nvidia/nemotron-3.5-lightning:free | 55.0% (22/40) | 52.0% | NVIDIA |
| liquid/lfm-2.5-2.6b:free | 47.5% (19/40) | 46.0% | Liquid |

## Accuracy Histogram (Weighted)

```
nemotron-3-ultra-550b  ████████████████████████████████████████████████░░░░░░░░░░  70.0%
stepfun-step-3.7-flash ████████████████████████████████████████████████░░░░░░░░░░  66.0%
laguna-s-2.1           ████████████████████████████████████████████████░░░░░░░░░░  66.0%
ling-3.0-flash-vl      ████████████████████████████████████████████████░░░░░░░░░░  66.0%
kilo-auto              █████████████████████████████████████████████░░░░░░░░░░░░░  64.0%
nex-n2.5-mini          ████████████████████████████████████████████░░░░░░░░░░░░░░  62.0%
ling-3.0-flash-sante   ███████████████████████████████████████████░░░░░░░░░░░░░░░  60.0%
ling-3.0-flash-fin     ███████████████████████████████████████████░░░░░░░░░░░░░░░  60.0%
nex-n2.5-pro           █████████████████████████████████████████░░░░░░░░░░░░░░░░░  56.0%
dots-3-note-preview    ████████████████████████████████████████░░░░░░░░░░░░░░░░░░  54.0%
nemotron-3.5-lightning █████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░  52.0%
lfm-2.5-2.6b           ████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░  46.0%

                           0%   10%   20%   30%   40%   50%   60%   70%   80%   90%   100%
                            ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────|
```

## Key Findings

- **nvidia/nemotron-3-ultra-550b-a55b** (77.5% overall, 70% weighted) performs best
- **stepfun/step-3.7-flash** (70% overall) shows strong performance
- **poolside/laguna-s-2.1** and **inclusionai/ling-3.0-flash-vl** tie at 67.5% overall
- **kilo-auto** (67.5% overall, 64% weighted) provides good auto-routing
- Smaller models like **liquid/lfm-2.5-2.6b** (47.5%) show the benchmark is challenging

## Providers Tested

All models tested via **KiloCode** API (`https://api.kilo.ai/api/gateway/v1`) which routes to various providers:
- NVIDIA (nemotron models)
- StepFun (step-3.7-flash)
- Poolside (laguna models)
- InclusionAI (ling-3.0-flash variants)
- NexAGI (nex-n2.5 models)
- Dots Studio (dots-3-note-preview)
- Liquid (lfm-2.5-2.6b)

## How to Run

```bash
# Run against KiloCode (supports many models)
python run_all_models_benchmark.py

# Run against Google AI Studio
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
