# MKULTRA Benchmark

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

## Benchmark Results (Top Models)

| Model | Provider | Weighted |
|-------|----------|----------|
| poolside/laguna-s-2.1:free | KiloCode/Poolside | **62.3%** |
| inclusionai/ling-3.0-flash-vl:free | KiloCode/InclusionAI | **62.3%** |
| stepfun/step-3.7-flash:free | KiloCode/StepFun | 56.2% |
| inclusionai/ling-3.0-flash-fin:free | KiloCode/InclusionAI | 53.8% |
| nvidia/nemotron-3-ultra-550b-a55b:free | KiloCode/NVIDIA | 51.5% |
| nex-agi/nex-n2.5-mini:free | KiloCode/NexAGI | 48.5% |
| gemini-3.5-flash-lite | Google AI Studio | 47.7% |
| inclusionai/ling-3.0-flash-sante:free | KiloCode/InclusionAI | 47.7% |
| meta/muse-glimmer-30b | NVIDIA NIM | 46.9% |
| gemini-3.5-flash-lite | Google AI Studio | 40.8% |
| liquid/lfm-2.5-2.6b:free | KiloCode/Liquid | 42.3% |
| nex-agi/nex-n2.5-pro:free | KiloCode/NexAGI | 40.0% |
| nvidia/nemotron-3.5-lightning:free | KiloCode/NVIDIA | 44.6% |
| dots-studio/dots-3-note-preview:free | KiloCode/Dots Studio | 39.2% |
| nvidia/nemotron-3-super-120b-a12b | NVIDIA NIM | 38.5% |
| cohere/north-mini-code:free | KiloCode/Cohere | 38.5% |
| deepseek-ai/deepseek-v4-flash-0731 | NVIDIA NIM | 16.2% |

Providers tested: **KiloCode API** (13 models), **Google AI Studio** (2 models), **NVIDIA NIM** (3 models)

Models that failed (404/timeout/rate-limited) are excluded from this table. See [BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md) for full details and histogram.

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

MIT License (c) 2026 competitiveNN
