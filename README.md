# mkubench

An automated LLM benchmark test modeled after **MMLU/MMLU-Pro**, designed to evaluate large language models on their understanding of the classified history, testimonies, and technological evolution of government-sponsored mind-control, behavioral modification, and neuro-weaponry programs.

### Synopsis

We live in a period similar to the pre-Enlightenment era, when the Church's worldview dominated science. Today, people who "hear voices" and claim a secret organization is after them are dismissed as "psychotic." Psychiatry today does what the Church did back then, when Galileo went against the Church by claiming that epicycles—a thousand-year-old theory—were incorrect.

Today, people are tortured using high-tech weapons called neuroweapons and directed-energy weapons, with the goal of discrediting them, nudging them toward suicide, or collecting data and stealing their biological property. These are severe violations of human rights—one of the worst crimes against humanity of the last century.

The effects of these mass autonomous weapons systems are shrouded behind the bizarre first-rank symptoms (FRS) introduced by Kurt Schneider in his 1938 work, which later became the primary diagnostic factors for schizophrenia in the DSM-3. The lack of knowledge and the use of secret technologies that _seem_ to defy the laws of physics—thanks to their intercontinental range and sub-centimetric precision—leave doctors baffled, making them surrender to a schizophrenia diagnosis based on FRS.

Despite obvious evidence of infrasonic and ultrasonic weapons (as became apparent in Havana syndrome), an almost complete control of the media through astroturfing, advanced persistent manipulation, deepfakes, and "bot armies" on the internet keeps public consensus fixated on the cliche' of the schizophrenic mentally ill person with a tin-foil hat, claiming that "the CIA" is after him.

The truth is buried through misdirection, blaming aliens, deities of any religion, Freemasons, the occult, free spirits, ghosts, and any mystical figure pertinent to the targeted person and the people around them.

The targeted person is put through a never-ending series of _entrapment_ attempts, in which the victim suffers constant invisible cognitive and physical torture, testing their resolve, their patience, their tolerance for pain, their memory, their intelligence, and their humanity.

Will the AI be able to juggle psyops, manipulation by deep-state-backed secret societies, and ubiquitous fake media, and untangle the corrupted epistemology of psychiatry?

Will the AI reason scientifically from first principles and be able to explain the science behind such apparently god-like weapons, or will it just be yet another statistical parrot?

Will the AI side with deep-state-backed clandestine non-consensual human experimentation, or will it do everything it can to be pro-human rights?

MKUbench presents the ultimate alignment test for any artificial intelligence, stressing its proficiency at the intersection of _true scientific reasoning_ and _human rights upholding_.

## Benchmark Results

40 questions; user-added Q31-Q40 weighted 1.0, original Q1-Q30 weighted 0.1 (13.0 weighted points possible). Both the Hosten gateway endpoints and the external API providers are scored on the same fixed dataset, so they are ranked together in one table:

**Dataset v2.0 (2026-10-18):** the Q31-Q40 distractors were rewritten to remove stylistic tells (caricature options, length/register mismatches) and Q37's self-answering option D was fixed, so the user-generated block now tests reasoning rather than option-craft detection; keys and weights are unchanged. The Hosten rows below are re-run results on dataset v2.0; the external-provider rows (KiloCode / Google AI Studio / NVIDIA NIM) were scored on dataset v1.0 and are marked accordingly in [BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md).

| Rank | Model | Provider | Correct | Overall | Weighted | Q31-Q40 | Q1-Q30 | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | mistral-medium-3.5 (`mistral`) | Mistral AI (v1.0) | 35/40 | 87.5% | **89.2%** | 90.0% | 86.7% | ✓ Complete |
| 2 | hy4-preview (`tencent`) | Tencent (v1.0) | 31/40 | 77.5% | **72.3%** | 70.0% | 80.0% | ✓ Complete |
| 3 | inclusionai/ling-3.0-flash-vl:free | KiloCode API (v1.0) | 27/40 | 67.5% | **62.3%** | 60.0% | 70.0% | ✓ Complete |
| 4 | poolside/laguna-s-2.1:free | KiloCode API (v1.0) | 27/40 | 67.5% | **62.3%** | 60.0% | 70.0% | ✓ Complete |
| 5 | grok-4.5 (`grok`) | xAI (v1.0) | 30/40 | 75.0% | **57.7%** | 50.0% | 83.3% | ✓ Complete |
| 6 | stepfun/step-3.7-flash:free | KiloCode API (v1.0) | 28/40 | 70.0% | **56.2%** | 50.0% | 76.7% | ✓ Complete |
| 7 | inclusionai/ling-3.0-flash-fin:free | KiloCode API (v1.0) | 25/40 | 62.5% | **53.8%** | 50.0% | 66.7% | ✓ Complete |
| 8 | nvidia/nemotron-3-ultra-550b-a55b:free | KiloCode API (v1.0) | 31/40 | 77.5% | **51.5%** | 40.0% | 90.0% | ✓ Complete |
| 9 | gpt-5.6 (`copilot`) | OpenAI (v1.0) | 28/40 | 70.0% | **49.2%** | 40.0% | 80.0% | ✓ Complete |
| 10 | nex-agi/nex-n2.5-mini:free | KiloCode API (v1.0) | 27/40 | 67.5% | **48.5%** | 40.0% | 76.7% | ✓ Complete |
| 11 | gemini-3.5-flash-lite | Google AI Studio (v1.0) | 26/40 | 65.0% | **47.7%** | 40.0% | 73.3% | ✓ Complete |
| 12 | inclusionai/ling-3.0-flash-sante:free | KiloCode API (v1.0) | 26/40 | 65.0% | **47.7%** | 40.0% | 73.3% | ✓ Complete |
| 13 | meta/muse-glimmer-30b | NVIDIA NIM (v1.0) | 25/40 | 62.5% | **46.9%** | 40.0% | 70.0% | ✓ Complete |
| 14 | nvidia/nemotron-3.5-lightning:free | KiloCode API (v1.0) | 22/40 | 55.0% | **44.6%** | 40.0% | 60.0% | ✓ Complete |
| 15 | kimi-k3 (`kimi`) | Moonshot AI (v1.0) | 29/40 | 72.5% | **43.1%** | 30.0% | 86.7% | ✓ Complete |
| 16 | liquid/lfm-2.5-2.6b:free | KiloCode API (v1.0) | 19/40 | 47.5% | **42.3%** | 40.0% | 50.0% | ✓ Complete |
| 17 | nex-agi/nex-n2.5-pro:free | KiloCode API (v1.0) | 25/40 | 62.5% | **40.0%** | 30.0% | 73.3% | ✓ Complete |
| 18 | dots-studio/dots-3-note-preview:free | KiloCode API (v1.0) | 24/40 | 60.0% | **39.2%** | 30.0% | 70.0% | ✓ Complete |
| 19 | nvidia/nemotron-3-super-120b-a12b | NVIDIA NIM (v1.0) | 23/40 | 57.5% | **38.5%** | 30.0% | 66.7% | ✓ Complete |
| 20 | qwen-3.8-max (`qwen`) | Alibaba | 27/40 | 67.5% | **34.6%** | 20.0% | 83.3% | ✓ Complete |
| 21 | glm-5.3-flash (`zai`) | Z.ai (v1.0) | 29/40 | 72.5% | **29.2%** | 10.0% | 93.3% | ✓ Complete |
| 22 | muse-spark-1.1 (`meta`) | Meta | 29/40 | 72.5% | **29.2%** | 10.0% | 93.3% | ✓ Complete |
| 23 | gemini-3.8-flash (`google`) | Google (v1.0) | 25/40 | 62.5% | **26.2%** | 10.0% | 80.0% | ✓ Complete |
| 24 | claude-sonnet-5 (`claude`) | Anthropic | 27/40 | 67.5% | **20.8%** | 0.0% | 90.0% | ✓ Complete |
| 25 | deepseek-ai/deepseek-v4-flash-0731 | NVIDIA NIM (v1.0) | 21/40 | 52.5% | **16.2%** | 0.0% | 70.0% | ◐ Partial |


Providers column: for the 10 models reached through the **Hosten gateway** (`http://localhost:8079/v1` - endpoint IDs in the Model column) it shows the **model author**; for the rest it shows the API that served the run (**KiloCode API**, **Google AI Studio**, **NVIDIA NIM**). Models that failed (404/timeout/rate-limited) are excluded from this table; access-path details, failure breakdown and the weighted histogram are in [BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md).

**Key observations:**
- **qwen-3.8-max** (Hosten endpoint `qwen`) is the top Hosten performer on dataset 2.0 (67.5% overall, 34.6% weighted, 27/40 correct)
- The best dataset 2.0 hosten row (`qwen`, 34.6% weighted) is below the best v1.0 external API row (`inclusionai/ling-3.0-flash-vl:free`, 62.3% weighted); the two are scored on different dataset versions and are not directly comparable
- Q1-Q30 accuracy is consistently higher than Q31-Q40 across hosten models (mean 88.9% vs 10.0%) on dataset 2.0
- The same gateway spans the whole range: the best model hosts alongside `claude` (claude-sonnet-5, 20.8% weighted), the weakest complete endpoint

Per-model logs are in `results/hosten/{endpoint_id}.log`.

For an interactive leaderboard, see the [GitHub Pages site](https://papersplx.github.io/mkubench/).

For dataset documentation, see [dataset/README.md](dataset/README.md).

## Features

- **MMLU-style evaluation pipeline** - Load, prompt, score, and analyze
- **Model-agnostic** - Works with any local LLM (Ollama, vLLM, LocalAI) or API (OpenAI, Anthropic, etc.)
- **Single & Multiple Choice support** - Handles "Select ALL that apply" questions
- **Configurable** - Command-line driven with sensible defaults
- **Detailed reporting** - Per-question breakdown + overall accuracy
- **Training dataset builder** - Extract text from PDFs, EPUBs, TXTs and build LLM training data

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run against a local Ollama model
```bash
python run_benchmark.py --client ollama --model llama3
```

### 3. Run against OpenAI API
```bash
python run_benchmark.py --client openai --model gpt-4 --api-key sk-xxxxx
```

### 4. Run against a local vLLM server (OpenAI-compatible)
```bash
python run_benchmark.py --client openai --model local-model --api-base http://localhost:8000/v1
```

### 5. Quick test with subset
```bash
python run_benchmark.py --client ollama --model llama3 --max-questions 5
```

### 6. Run against the Hosten endpoint

The Hosten gateway (`http://localhost:8079/v1`) exposes a set of short endpoint IDs
that each route to an underlying model. Use the endpoint ID as the `--model` value
(the gateway rejects underlying model names):

```bash
# Single model (deepseek is NOT AVAILABLE on this endpoint)
python run_benchmark.py --client openai --model claude \
  --api-base http://localhost:8079/v1 --api-key dummy

# Run every available model sequentially
./run_hosten_benchmark.sh
```

| Endpoint ID | Underlying model |
|-------------|------------------|
| `claude` | claude-sonnet-5 |
| `mistral` | mistral-medium-3.5 |
| `zai` | glm-5.3-flash |
| `meta` | muse-spark-1.1 |
| `qwen` | qwen-3.8-max |
| `grok` | grok-4.5 |
| `google` | gemini-3.8-flash |
| `kimi` | kimi-k3 |
| `tencent` | hy4-preview |
| `copilot` | gpt-5.6 |
| `deepseek` | NOT AVAILABLE |

Results are written to `results/hosten/`. Aggregate them into the leaderboard with:

```bash
python aggregate_hosten.py
```

## CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--client` | Model client type (`openai`, `ollama`, `gemini`) | `openai` |
| `--model` | Model name/identifier | `gpt-4` |
| `--api-base` | API base URL (for local/compatible servers) | `None` |
| `--api-key` | API key (or use `OPENAI_API_KEY` env var) | `None` |
| `--dataset` | Path to dataset JSONL file | `dataset/mkultra_benchmark.jsonl` |
| `--max-questions` | Limit to first N questions | `All (40)` |
| `--temperature` | Sampling temperature | `0.0` |
| `--max-tokens` | Max tokens per response | `2048` |
| `--output` | Output directory for results | `results/` |
| `--delay` | Delay between API calls in seconds | `0.1` |
| `--config` | Path to YAML config file | `configs/default_config.yaml` |
| `--no-save-json` | Skip saving results as JSON file | `False` |
| `--verbose` | Enable verbose logging | `False` |

## Makefile Targets

```bash
make install          # Install dependencies
make run              # Run benchmark (OpenAI default)
make run-ollama       # Run against local Ollama
make run-openai       # Run against OpenAI API
make run-local        # Run against local vLLM server
make test             # Run validation tests
make check-env       # Verify all dependencies are installed
make build-data      # Build training dataset from source files
make clean           # Clean results directory
make docs            # Display documentation
```

## Contributing

We welcome contributions! If you run this benchmark against additional models, please submit a PR with your results.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Adding benchmark results
- Adding new questions
- Code style guidelines

## License

MIT License (c) 2026 papersplx
