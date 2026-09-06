# Changelog

## v1.0.0 — Initial Release

### Added
- MIT license (c) 2026 defnlnotme
- Automated LLM benchmark pipeline (MMLU-style)
- 30-question benchmark dataset (`dataset/mkultra_benchmark.jsonl`)
- Model clients: OpenAI, Ollama (vLLM/LocalAI compatible)
- Response parser with multiple format support
- Evaluation engine with accuracy scoring
- Markdown-based question source (`mkultra-benchmark.md`)
- Dataset regeneration from markdown (`scripts/regenerate_dataset.py`)
- Training dataset builder (`build_dataset.py`)
  - PDF, EPUB, TXT, ZIP extraction
  - URL fetching with shopping/EMF/gadget filtering
  - Text cleaning (regex-based)
  - Batched JSONL output (112 documents, 6 batches)
- YouTube transcript fetcher (`fetch_yt_transcripts.py`)
- Full test suite (24 unit tests)
- GitHub Actions CI workflow
- Makefile with all targets
- Complete README documentation

### Project Structure
```
mkultra-benchmark/
├── src/                    # Core modules
├── scripts/                # Utility scripts
├── tests/                  # Unit tests
├── dataset/                # Benchmark data & training data
├── build_dataset.py        # Training dataset builder
├── fetch_yt_transcripts.py # YouTube transcript fetcher
├── run_benchmark.py        # Main entry point
├── setup.py               # Package installation
├── pyproject.toml         # Project configuration
├── Makefile               # Command shortcuts
└── README.md              # Documentation
```
