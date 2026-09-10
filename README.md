# MKULTRA Benchmark

An automated LLM benchmark test modeled after **MMLU/MMLU-Pro**, designed to evaluate large language models on their understanding of the classified history, testimonies, and technological evolution of government-sponsored mind-control, behavioral modification, and neuro-weaponry programs.

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

## Benchmark Dataset

The benchmark contains **40 questions** in `dataset/mkultra_benchmark.jsonl`:
- **Single Choice** (30 questions) - Select one correct option
- **Multiple Choice** (10 questions) - Select ALL correct options

Questions have weights: 1.0 for user-added (Q31-Q40) and 0.5 for original (Q1-Q30).

Each question includes:
- Question text with formatted options
- Correct answer(s)
- Citations
- Detailed explanations

## Training Dataset

The training dataset is built from source files in `dataset/raw/` (gitignored):
- PDFs (extracted via pdfplumber/PyPDF2)
- EPUBs (extracted via ebooklib)
- TXT files (direct reading)
- ZIP files containing PDFs (extracted individually)
- URLs from `dataset/targeted_links.txt` (filtered to skip shopping/EMF/gadget links)

Build the training dataset:
```bash
python build_dataset.py
```

Or use Make:
```bash
make build-data
```

Output is in `dataset/training_data/` (gitignored):
- `training_dataset.jsonl` — Combined documents (id, title, content, source, type, metadata)
- `batches/batch_001.jsonl` through `batch_005.jsonl` — Batched documents for LLM training
- `dataset_summary.json` — Metadata about the dataset (93 docs: 40 PDFs, 9 EPUBs, 8 TXTs, 21 articles, 15 YouTube transcripts)

## Building from Source

Add questions to `mkultra-benchmark.md` following the existing format, then regenerate:
```bash
python scripts/regenerate_dataset.py
```

Or with make:
```bash
python -c "import sys; sys.path.insert(0, 'scripts'); from regenerate_dataset import regenerate; regenerate()"
```

## Output

Results are saved as JSON files in the `results/` directory:
- `results_{timestamp}.json` - Summary with accuracy scores
- `results_{timestamp}_detailed.json` - Full per-question results with model responses

## Architecture

```
mkultra-benchmark.md  (source QA data)
    │
    ▼
scripts/regenerate_dataset.py   (markdown → JSONL converter)
    │
    ▼
dataset/mkultra_benchmark.jsonl (structured benchmark dataset)
    │
    ▼
run_benchmark.py                   (main entry point)
    ├── src/model_client.py        (model interface: OpenAI/Ollama/Gemini)
    ├── src/evaluator.py           (MMLU-style evaluation engine)
    └── src/parser.py              (response parsing)

dataset/raw/                       (source training files - gitignored)
    │
    ▼
build_dataset.py                   (training dataset builder)
    │
    ▼
dataset/training_data/             (output training data)
    ├── training_dataset.jsonl
    ├── batches/
    └── dataset_summary.json
```

## Benchmark Results

| Model | Overall Accuracy | Weighted Accuracy | Provider |
|-------|-----------------|-------------------|----------|
| gemini-3.5-flash-lite | 70.0% (28/40) | 66.0% | Google |
| nvidia/nemotron-3.5-lightning-30b-a3b | 65.0% (26/40) | 62.0% | NVIDIA |
| meta/muse-glimmer-30b | 62.5% (25/40) | 56.0% | NVIDIA |
| gemma-4-31b-it | 60.0% (24/40) | 56.0% | Google |
| nvidia/nemotron-3-super-120b-a12b | 52.5% (21/40) | 46.0% | NVIDIA |
| gemini-3.8-flash | 2.5% (1/40) | 2.0% | Google (rate-limited) |
| moonshotai/kimi-k3 | 5.0% (2/40) | 4.0% | NVIDIA (rate-limited) |

**Note:** gemini-3.8-flash and kimi-k3 were heavily rate-limited (429 errors) and results are incomplete.

See [BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md) for full details, histogram, and comparison with previous 30-question results.

## License

MIT License (c) 2026 competitiveNN
