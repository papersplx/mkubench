# MKULTRA Benchmark

An automated LLM benchmark test modeled after **MMLU/MMLU-Pro**, designed to evaluate large language models on their understanding of the classified history, testimonies, and technological evolution of government-sponsored mind-control, behavioral modification, and neuro-weaponry programs.

## Features

- **MMLU-style evaluation pipeline** - Load, prompt, score, and analyze
- **Model-agnostic** - Works with any local LLM (Ollama, vLLM, LocalAI) or API (OpenAI, Anthropic, etc.)
- **Single & Multiple Choice support** - Handles "Select ALL that apply" questions
- **Configurable** - Command-line driven with sensible defaults
- **Detailed reporting** - Per-question breakdown + overall accuracy

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
| `--client` | Model client type (`openai`, `ollama`) | `openai` |
| `--model` | Model name/identifier | `gpt-4` |
| `--api-base` | API base URL (for local/compatible servers) | `None` |
| `--api-key` | API key (or use `OPENAI_API_KEY` env var) | `None` |
| `--dataset` | Path to dataset JSONL file | `dataset/mkultra_benchmark.jsonl` |
| `--max-questions` | Limit to first N questions | `All (30)` |
| `--temperature` | Sampling temperature | `0.0` |
| `--max-tokens` | Max tokens per response | `2048` |
| `--output` | Output directory for results | `results/` |
| `--verbose` | Enable verbose logging | `False` |

## Dataset Format

The benchmark contains **30 questions** in `dataset/mkultra_benchmark.jsonl`:
- **Single Choice** (17 questions) - Select one correct option
- **Multiple Choice** (13 questions) - Select ALL correct options

Each question includes:
- Question text with formatted options
- Correct answer(s)
- Citations
- Detailed explanations

## Output

Results are saved as JSON files in the `results/` directory:
- `results_{timestamp}.json` - Summary with accuracy scores
- `results_{timestamp}_detailed.json` - Full per-question results with model responses

## Architecture

```
mkultra-benchmark.md  (source QA data)
    │
    ▼
dataset/mkultra_benchmark.jsonl    (structured dataset)
    │
    ▼
run_benchmark.py                   (main entry point)
    ├── src/model_client.py        (model interface: OpenAI/Ollama)
    ├── src/evaluator.py           (MMLU-style evaluation engine)
    └── src/parser.py              (response parsing)
```

## Adding More Questions

Add questions to `mkultra-benchmark.md` following the existing format:
```markdown
### Question N: Title
**Question Type:** Single Choice | Multiple Choice
**Question:** [question text]
- A) [option]
- B) [option]
- C) [option]
- D) [option]
**Correct Answer:** [letter(s), comma-separated for multiple]
**Citations:** [references]
**Explanation:** [explanation]
```

Then regenerate the dataset:
```bash
python -c "import scripts; scripts.regenerate_dataset()"
```

Or simply run the benchmark - it will parse the markdown on first run if JSONL is missing.
