# Benchmark Results

## Overview

LLM performance on the MKULTRA Benchmark (40 questions: 30 single-choice, 10 multiple-choice).
Questions have weights: **1.0** for user-added questions (Q31-Q40) and **0.5** for original questions (Q1-Q30).

## Final Results (12 Models Tested)

### Fully Completed Models

| Model | Overall Accuracy | Weighted Accuracy | Failures | Provider |
|-------|-----------------|-------------------|----------|----------|
| gemini-3.1-flash-lite | 75.0% (30/40) | 68.0% | 0 | Google |
| nvidia/nemotron-3.5-lightning-30b-a3b | 70.0% (28/40) | 68.0% | 0 | NVIDIA |
| gemini-3.5-flash | 70.0% (28/40) | 62.0% | 0 | Google |
| nvidia/nemotron-3-super-120b-a12b | 60.0% (24/40) | 54.0% | 0 | NVIDIA |
| gemma-4-26b-a4b-it | 57.5% (23/40) | 56.0% | 0 | Google |
| gemma-4-31b-it | 52.5% (21/40) | 50.0% | 6 | Google |

### Partially Completed (Rate-Limited)

| Model | Overall Accuracy | Weighted Accuracy | Failures | Provider |
|-------|-----------------|-------------------|----------|----------|
| gemini-3.8-flash | 57.5% (23/40) | 48.0% | 16 | Google |
| meta/muse-glimmer-30b | 52.5% (21/40) | 48.0% | 11 | NVIDIA |
| gemini-2.5-flash | 20.0% (8/40) | 18.0% | 24 | Google |

### Not Completed

| Model | Status | Provider |
|-------|--------|----------|
| moonshotai/kimi-k3 | Rate limited (429) | NVIDIA |
| poolside/laguna-xs-2.1 | Not started | NVIDIA |

## Accuracy Histogram (Weighted)

```
gemini-3.1-flash-lite      ████████████████████████████████████████████████░░░░░░░░░░  68.0%
nemotron-3.5-lightning     ████████████████████████████████████████████████░░░░░░░░░░  68.0%
gemini-3.5-flash           █████████████████████████████████████████████░░░░░░░░░░░░░  62.0%
nemotron-3-super-120b      ██████████████████████████████████████████░░░░░░░░░░░░░░░░  54.0%
gemma-4-26b-a4b-it         █████████████████████████████████████████░░░░░░░░░░░░░░░░░  56.0%
gemma-4-31b-it             ████████████████████████████████████████░░░░░░░░░░░░░░░░░░  50.0%
gemini-3.8-flash (16 fail) █████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░  48.0%
muse-glimmer-30b (11 fail) █████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░  48.0%
gemini-2.5-flash (24 fail) ██████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  18.0%

                           0%   10%   20%   30%   40%   50%   60%   70%   80%   90%   100%
                            ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────|
```

## Key Findings

- **gemini-3.1-flash-lite** (75% overall, 68% weighted) performs best on the full dataset
- **nvidia/nemotron-3.5-lightning-30b-a3b** ties for weighted accuracy (68%) despite 70% overall
- **gemini-3.5-flash** achieves 70% overall, strong for a non-lite model
- **gemma-4-26b-a4b-it** (56% weighted) outperforms gemma-4-31b-it (50% weighted)
- Rate limiting significantly impacted results: models with >10 failures would likely score higher
- Google's "flash-lite" variants consistently outperform their larger counterparts on this benchmark

## Comparison with Previous 30-Question Results

| Model | Previous (30q) | Current (40q, weighted) |
|-------|---------------|------------------------|
| gemini-3.5-flash-lite | 76.7% | 66.0% |
| gemini-3.1-flash-lite | - | 68.0% |
| nemotron-3.5-lightning | 66.7% | 68.0% |
| gemini-3.5-flash | - | 62.0% |

## How to Run

```bash
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
