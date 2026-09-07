# Changelog

## v1.1.4 — Proactive Improvements & CI Hardening

### Fixed
- Removed Python 3.14 from CI matrix (dependency compatibility)
- Updated CI to install package with `pip install -e .` and use `pytest --cov`
- Cleaned dead code in `build_dataset.py` (unused `text`/`first` assignments in zip path)
- Fixed `build_dataset.py` internal naming: `extract_zip_text` now returns `'content'` key instead of `'text'` for consistency with rest of codebase
- Improved `Makefile` `docs` target with comprehensive target listing
- Added `help` Makefile target
- Added pytest-cov coverage configuration to pyproject.toml
- Fixed .flake8 to exclude *.toml files
- Removed unused `yt-dlp` dependency from requirements.txt and pyproject.toml
- Added main class exports to `src/__init__.py`
- Added `pre-commit` configuration with black, flake8, mypy, and standard hooks

### Verified
- All 85 tests passing
- flake8 clean across entire codebase
- Package installs correctly via `pip install -e .`

## v1.1.3 — Test Coverage & Documentation

### Added
- Comprehensive test suite expansion: 24 → 85 tests
- Added mock-based tests for `OpenAIClient.generate()`, `batch_generate()`
- Added mock-based tests for `OllamaClient.generate()`, `batch_generate()`
- Added tests for `OpenAIClient` and `OllamaClient` initialization and attributes
- Added tests for `get_client()` factory with kwargs
- Added tests for `evaluate_single()`, `_build_prompt()`, `save_results()`
- Added tests for `run_evaluation()` with mock clients and edge cases
- Added tests for `_load_dataset()` with temporary files
- Added parser edge cases: parentheses, equals signs, whitespace, case handling
- Added `TestMain` test class for `parse_answer.main()` validation
- Added missing CLI args to README table (`--delay`, `--config`, `--no-save-json`)
- Added `check-env` and `docs` targets to Makefile documentation
- Fixed dataset statistics in README (21 single choice, 9 multiple choice)
- Added module docstring to `scripts/regenerate_dataset.py`
- Added `transcripts/` and `.coverage` to `.gitignore`

### Verified
- All 85 unit tests passing
- `make check-env`, `make test`, `make build-data` all functional
- flake8 clean across the entire codebase
## v1.1.2 — Code Quality & Infrastructure

### Fixed
- Updated CHANGELOG v1.0.0 dataset stats from 112 docs/6 batches to 78 docs/4 batches
- Bumped version from 1.0.0 to 1.1.1 in pyproject.toml, setup.py, and src/__init__.py
- Updated CI workflow to use pytest instead of unittest
- Added flake8 linting step to CI pipeline

### Improved
- Removed all flake8 warnings across the codebase
- Fixed unused imports, dead code, and ambiguous variable names
- Split long print statements and fixed f-string issues
- Added `.flake8` config with max-line-length=120
- Added `# noqa: E402` comments to test files requiring sys.path manipulation
- Stripped trailing whitespace from all Python files
- Rewrote scripts/regenerate_dataset.py with consistent formatting
## v1.1.1 — Data Fixes & API Compatibility

### Fixed
- Fixed YouTube transcript API compatibility: changed `YouTubeTranscriptApi.get_transcript()` to `YouTubeTranscriptApi().fetch()` for youtube-transcript-api v2
- Rebuilt training dataset with correct `content` field name (was `text`)
- Updated dataset structure: 78 documents (40 PDFs, 9 EPUBs, 8 TXTs, 21 articles) in 4 batches
- Cleaned up stale batch_005.jsonl and batch_006.jsonl files

### Changed
- `build_dataset.py` output field: `text` → `content` for document content
- `README.md`: updated dataset description to reflect correct field names and batch count
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
  - Batched JSONL output (78 documents, 4 batches)
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
