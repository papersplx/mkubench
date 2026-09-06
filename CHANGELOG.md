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

## v1.1.0 — Bug Fixes, Quality Improvements & Infrastructure

### Fixed
- Fixed corrupted `fetch_yt_transcripts.py` header (duplicate docstring from build_dataset.py)
- Fixed `scripts/regenerate_dataset.py` undefined `base_dir` variable causing NameError
- Fixed `run_benchmark.py` `--save-json` argument bug (was `store_true` with `default=True`, impossible to disable; changed to `--no-save-json` with `store_false`)
- Made `build_dataset.py` imports defensive (`requests`, `bs4` wrapped in try/except)
- Added `None` guard in `fetch_url_content` for missing dependencies

### Improved
- Added `-> None` return type annotations to all public functions across 6 files
- Added `Optional[str]` type hints for parameters defaulting to `None` in `OpenAIClient.__init__` and `build_dataset()`
- Added `**kwargs: Any` type annotations to all `**kwargs` parameters in `model_client.py`
- Added docstrings to all 15+ functions missing documentation
- Updated `setup.py` with missing `regenerate-dataset` entry point
- Added `[tool.pytest.ini_options]` to `pyproject.toml`
- Updated `.github/workflows/test.yml` to use `python3` and added dependency check step
- Updated `Makefile` with `PYTHON` variable auto-detecting venv Python and `check-env` target
- Fixed `src/__init__.py`, `scripts/__init__.py`, `tests/__init__.py`, `src/parser.py` license header ordering
- Added `main()` function wrapper to `src/parser.py` test code
- Updated `src/model_client.py` type hints for `BaseModelClient`, `OpenAIClient`, `OllamaClient`, and `get_client`

### Verified
- All 24 unit tests passing
- `make check-env`, `make test`, `make build-data` all functional
- Clean working tree, all commits pushed to origin/master
- Zero functions missing return types or docstrings
- All source files compile cleanly

## v1.1.1 — Data Fixes & API Compatibility

### Fixed
- Fixed YouTube transcript API compatibility: changed `YouTubeTranscriptApi.get_transcript()` to `YouTubeTranscriptApi().fetch()` for youtube-transcript-api v2
- Rebuilt training dataset with correct `content` field name (was `text`)
- Updated dataset structure: 78 documents (40 PDFs, 9 EPUBs, 8 TXTs, 21 articles) in 4 batches
- Cleaned up stale batch_005.jsonl and batch_006.jsonl files

### Changed
- `build_dataset.py` output field: `text` → `content` for document content
- `README.md`: updated dataset description to reflect correct field names and batch count
