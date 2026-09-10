# Benchmark Results

## Overview

LLM performance on the MKULTRA Benchmark (40 questions: 30 single-choice, 10 multiple-choice).
Questions have weights: **1.0** for user-added questions (Q31-Q40) and **0.5** for original questions (Q1-Q30).

## Results (40 Questions, Weighted Scoring)

| Model | Overall Accuracy | Weighted Accuracy | Status | Provider |
|-------|-----------------|-------------------|--------|----------|
| gemini-3.5-flash-lite | 70.0% (28/40) | 66.0% | Complete | Google |
| nvidia/nemotron-3.5-lightning-30b-a3b | 65.0% (26/40) | 62.0% | Complete | NVIDIA |
| meta/muse-glimmer-30b | 62.5% (25/40) | 56.0% | Complete | NVIDIA |
| gemma-4-31b-it | 60.0% (24/40) | 56.0% | Complete | Google |
| nvidia/nemotron-3-super-120b-a12b | 52.5% (21/40) | 46.0% | Complete | NVIDIA |
| gemini-3.8-flash | 2.5% (1/40) | 2.0% | Rate Limited | Google |
| moonshotai/kimi-k3 | 5.0% (2/40) | 4.0% | Rate Limited | NVIDIA |

**Note:** gemini-3.8-flash and kimi-k3 were heavily rate-limited (429 errors) and could not complete the benchmark properly.

## Accuracy Histogram (Weighted)

```
gemini-3.5-flash-lite      ████████████████████████████████████████████████░░░░░░░░░░  66.0%
nemotron-3.5-lightning     █████████████████████████████████████████████░░░░░░░░░░░░░  62.0%
muse-glimmer-30b           ██████████████████████████████████████████░░░░░░░░░░░░░░░░  56.0%
gemma-4-31b-it             ██████████████████████████████████████████░░░░░░░░░░░░░░░░  56.0%
nemotron-3-super-120b      █████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░  46.0%
kimi-k3                    ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   4.0% (incomplete)
gemini-3.8-flash           ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   2.0% (incomplete)

                           0%   10%   20%   30%   40%   50%   60%   70%   80%   90%   100%
                            ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────|
```

## Results (30 Questions, Original Dataset)

For comparison, previous results on the original 30-question dataset:

| Model | Overall Accuracy | Single Choice | Multiple Choice | Provider |
|-------|-----------------|---------------|-----------------|----------|
| gemini-3.5-flash-lite | 76.7% (23/30) | 85.7% (18/21) | 55.6% (5/9) | Google |
| nvidia/nemotron-3-super-120b-a12b | 76.7% (23/30) | 90.5% (19/21) | 44.4% (4/9) | NVIDIA |
| gemini-3.8-flash | 70.0% (21/30) | 85.7% (18/21) | 33.3% (3/9) | Google |
| gemma-4-31b-it | 70.0% (21/30) | 85.7% (18/21) | 33.3% (3/9) | Google |
| meta/muse-glimmer-30b | 70.0% (21/30) | 85.7% (18/21) | 33.3% (3/9) | NVIDIA |
| nvidia/nemotron-3.5-lightning-30b-a3b | 66.7% (20/30) | 85.7% (18/21) | 22.2% (2/9) | NVIDIA |
| Gemini 2.5 Flash | 10.0% (3/30) | 14.3% (3/21) | 0.0% (0/9) | Google |

## Models Tested but Unavailable

The following models returned errors (404/410/503/timeout):

| Model | Status |
|-------|--------|
| deepseek-ai/deepseek-coder-6.7b-instruct | 404 Not Found |
| deepseek-ai/deepseek-v4-flash-0731 | Timeout |
| deepseek-ai/deepseek-v4-pro-0813 | Timeout |
| google/gemma-4-31b-it (NVIDIA) | Timeout |
| ibm/granite-3.0-3b-a800m-instruct | 404 Not Found |
| ibm/granite-3.0-8b-instruct | 404 Not Found |
| meta/llama2-70b | 404 Not Found |
| minimaxai/minimax-m3 | 410 Gone |
| moonshotai/kimi-k2.6 | 404 Not Found |
| nvidia/nemotron-3-ultra-550b-a55b | 503 Overloaded |
| poolside/laguna-xs-2.1 | 503 Resource Exhausted |

## Observations

- **gemini-3.5-flash-lite** leads with 66.0% weighted accuracy on the full 40-question dataset
- **nemotron-3.5-lightning-30b-a3b** (62.0%) shows strong performance despite smaller size
- **gemma-4-31b-it** and **muse-glimmer-30b** tie at 56.0% weighted
- Rate limiting significantly impacted **gemini-3.8-flash** and **kimi-k3** results
- Weighted scoring rewards performance on user-added questions (Q31-Q40), which cover specialized topics
- The benchmark requires specialized knowledge about classified government programs, making it difficult for general-purpose LLMs

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
