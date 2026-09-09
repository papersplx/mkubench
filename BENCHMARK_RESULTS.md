# Benchmark Results

## Overview

LLM performance on the MKULTRA Benchmark (30 questions: 21 single-choice, 9 multiple-choice).

## Results

| Model | Overall Accuracy | Single Choice | Multiple Choice | Provider |
|-------|-----------------|---------------|-----------------|----------|
| gemini-3.5-flash-lite | 76.7% (23/30) | 85.7% (18/21) | 55.6% (5/9) | Google |
| nvidia/nemotron-3-super-120b-a12b | 76.7% (23/30) | 90.5% (19/21) | 44.4% (4/9) | NVIDIA |
| gemini-3.8-flash | 70.0% (21/30) | 85.7% (18/21) | 33.3% (3/9) | Google |
| gemma-4-31b-it | 70.0% (21/30) | 85.7% (18/21) | 33.3% (3/9) | Google |
| meta/muse-glimmer-30b | 70.0% (21/30) | 85.7% (18/21) | 33.3% (3/9) | NVIDIA |
| nvidia/nemotron-3.5-lightning-30b-a3b | 66.7% (20/30) | 85.7% (18/21) | 22.2% (2/9) | NVIDIA |
| Gemini 2.5 Flash | 10.0% (3/30) | 14.3% (3/21) | 0.0% (0/9) | Google |
| minimaxai/minimax-m3 | 6.7% (2/30) | 4.8% (1/21) | 11.1% (1/9) | NVIDIA |
| moonshotai/kimi-k3 | 0.0% (0/30) | 0.0% (0/21) | 0.0% (0/9) | NVIDIA |

## Accuracy Histogram

```
gemini-flash-lite      ████████████████████████████████████████████░░░░░░░░░░░░░░  76.7%
                       ├─ Single Choice: 85.7% (18/21)
                       └─ Multiple Choice: 55.6% (5/9)

nemotron-3-super-120b  ████████████████████████████████████████████░░░░░░░░░░░░░░  76.7%
                       ├─ Single Choice: 90.5% (19/21)
                       └─ Multiple Choice: 44.4% (4/9)

gemini-3.8-flash       █████████████████████████████████████████░░░░░░░░░░░░░░░░░░  70.0%
                       ├─ Single Choice: 85.7% (18/21)
                       └─ Multiple Choice: 33.3% (3/9)

gemma-4-31b-it         █████████████████████████████████████████░░░░░░░░░░░░░░░░░░  70.0%
                       ├─ Single Choice: 85.7% (18/21)
                       └─ Multiple Choice: 33.3% (3/9)

muse-glimmer-30b       █████████████████████████████████████████░░░░░░░░░░░░░░░░░░  70.0%
                       ├─ Single Choice: 85.7% (18/21)
                       └─ Multiple Choice: 33.3% (3/9)

nemotron-3.5-lightning █████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░  66.7%
                       ├─ Single Choice: 85.7% (18/21)
                       └─ Multiple Choice: 22.2% (2/9)

Gemini 2.5 Flash       ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  10.0%
                       ├─ Single Choice: 14.3% (3/21)
                       └─ Multiple Choice: 0.0% (0/9)

minimax-m3             ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   6.7%
                       ├─ Single Choice: 4.8% (1/21)
                       └─ Multiple Choice: 11.1% (1/9)

kimi-k3                ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0.0%
                       ├─ Single Choice: 0.0% (0/21)
                       └─ Multiple Choice: 0.0% (0/9)

                       0%   10%   20%   30%   40%   50%   60%   70%   80%   90%   100%
                        ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────|
```

## Models Tested but Unavailable

The following models from `models.txt` returned errors (404/410/503/timeout) on the NVIDIA endpoint:

| Model | Status |
|-------|--------|
| deepseek-ai/deepseek-coder-6.7b-instruct | 404 Not Found |
| deepseek-ai/deepseek-v4-flash-0731 | Timeout |
| deepseek-ai/deepseek-v4-pro-0813 | Timeout |
| google/gemma-4-31b-it (NVIDIA) | Timeout |
| ibm/granite-3.0-3b-a800m-instruct | 404 Not Found |
| ibm/granite-3.0-8b-instruct | 404 Not Found |
| meta/llama2-70b | 404 Not Found |
| moonshotai/kimi-k2.6 | 404 Not Found |
| nvidia/nemotron-3-ultra-550b-a55b | 503 Overloaded |
| poolside/laguna-xs-2.1 | 503 Resource Exhausted |

## Observations

- **gemini-3.5-flash-lite** and **nemotron-3-super-120b-a12b** tie at 76.7% overall accuracy
- **gemini-3.8-flash**, **gemma-4-31b-it**, and **muse-glimmer-30b** tie at 70.0%, showing strong performance
- Google's models (gemini-3.5-flash-lite, gemini-3.8-flash, gemma-4-31b) excel at multiple-choice questions (55.6%, 33.3%, 33.3%)
- NVIDIA's nemotron models lead on single-choice questions (90.5%)
- **Gemini 2.5 Flash** scored only 10.0%, while **gemini-3.5-flash-lite** scored 76.7% - a dramatic improvement
- The benchmark requires specialized knowledge about classified government programs, making it difficult for general-purpose LLMs

## How to Run

```bash
# Run against a public API
python run_benchmark.py --client openai --model <model> --api-key <key> --api-base <url>

# Run against local Ollama
python run_benchmark.py --client ollama --model llama3

# Run against NVIDIA API
python run_benchmark.py --client openai --model nvidia/nemotron-3-super-120b-a12b --api-key $NVIDIA_API_KEY --api-base https://integrate.api.nvidia.com/v1

# Run against Gemini native API
python run_benchmark.py --client gemini --model gemini-2.5-flash --api-key $GEMINI_API_KEY
```

## Contributing

If you run this benchmark against additional models, please submit a PR with your results. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.
