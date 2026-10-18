# Changelog

## v2.0.0 — Benchmark V2: Hardened User-Generated Questions (Q31-Q40)

**Dataset revision — benchmark V2.** The user-generated block Q31-Q40 was rebalanced so
that answering correctly requires domain reasoning rather than spotting stylistic tells.
Correct answers are unchanged (one exception, see below); only distractors, two explanations,
and the `question_type` labels changed. Q1-Q30 are untouched. Scoring weights are unchanged
(user-generated 1.0, original 0.1, total 13.0).

### Changed (Q31-Q40 distractors)
- Distractors rewritten to be genuinely plausible and stylistically matched to their correct
  answers: hedged, mechanism-level, comparable length. Removed caricature options
  ("mentally ill people", aliens, gods, "fantastical tech terminology") that let models
  identify the keyed option by tone or length alone.
  - Q31 now offers a mainstream-neurodevelopmental reading, a heterogeneity-but-real
    reading, and a social-constructionist reading next to the keyed statistical-clustering
    critique.
  - Q32/Q33 add the Frey-effect and interior-of-skull descriptions that real literature
    and TI testimony support but which are not the keyed answer.
  - Q34 replaces "Nazi scientists"/"MIT Labs" with a Lincoln Lab (1980s) reading and a
    "Paperclip-adjacent" reading.
  - Q35 sequences auditory-first and street-harassment-first onset patterns against the
    keyed dream-manipulation-first pattern.
  - Q36 offers predictive-profiling and salience-detection explanations for synchronicities.
  - Q38 differentiates behavioural imitation and uncredited recycling of the target's work
    from the keyed media-mimicry phenomenon.
  - Q39 restates all three keyed reasons at matched length; Q40's caricature distractor is
    replaced by the base-rate agreement objection (DSM criteria track the reports), which is
    the strongest competing hypothesis rather than a straw man.

### Fixed
- Q37 was unanswerable as published: option D read "The correct answer is c, while a is
  street theatre", i.e. the giveaway contradicted the key `D`. The key is now `C`
  (receiving others' thoughts in their voice) and D is a real distractor (the psychiatric
  "thoughts transmitted outward" construct). Q37 answers keyed to D in earlier runs were
  scored against the giveaway text and must be re-run.
- Q31-Q39 were typed `question_type: "Multiple Choice"` while carrying a single keyed
  letter and `is_multiple_choice: false`. That mismatch invites multi-letter answers that
  can never match the single-letter key; these are now `"Single Choice"`. Q40 remains
  genuinely multi-select (`A, B, D`).

### Changed (tooling)
- `pyproject.toml` / `setup.py` version bumped to 2.0.0.

## v1.1.7 — Test Fixes & CI Infrastructure

### Fixed
- Fixed 4 pre-existing test failures:
  - Updated `test_evaluation_count` to expect 40 questions (was 30)
  - Updated `test_load_dataset` to expect 40 questions (was 30)
  - Updated `test_category` to check for field existence instead of "mkultra" value
  - Fixed `parse_answer` to handle parenthesized answers like "(A) is the correct answer"
- All 95 unit tests now pass

### Added
- `run_multi_model.py` - Unified multi-model benchmark runner
- `.github/workflows/validate.yml` - CI workflow for validating benchmark results
  - Runs on push/PR when results or dataset change
  - Validates result JSON schema
  - Verifies leaderboard.json is up to date
- Updated CONTRIBUTING.md with validation instructions and Makefile targets

### Changed
- Enhanced parser regex pattern for parenthesized answer format
- Updated CONTRIBUTING.md with new scripts and validation steps

## v1.1.6 — Tooling & Validation Infrastructure

### Added
- `regenerate_leaderboard.py` - Regenerate leaderboard.json from benchmark results
- `validate_results.py` - Validate benchmark result JSON files against expected schema
- `visualize_results.py` - Generate text histogram and HTML bar chart from leaderboard
- `tests/test_validate_results.py` - 10 unit tests for validation functions
- Makefile targets: `regenerate-leaderboard`, `validate-results`, `visualize`
- Schema validation handles both complete and legacy (summary-only) result formats

### Changed
- Updated Makefile with new targets and documentation
- Enhanced validate_results.py to show warnings for legacy format files instead of failing

### Repository Health
- 85 → 95 total unit tests
- All validation scripts functional: regenerate, validate, visualize
- Clean separation: scripts for generation, validation, and visualization

## v1.1.5 — Benchmark Results & Documentation Restructuring

### Added
- Comprehensive benchmark results for 27 models across 3 providers (KiloCode API, Google AI Studio, NVIDIA NIM)
- Summary statistics including average accuracy on user-generated vs original questions
- Tracked `leaderboard.json` with full model rankings and breakdowns by question type
- `dataset/README.md` with dedicated dataset documentation
- Contributing section in main README

### Changed
- Restructured README.md: moved benchmark results to top, removed duplicate dataset docs
- Updated BENCHMARK_RESULTS.md with:
  - Summary statistics table
  - Combined leaderboard with Q31-Q40 and Q1-Q30 breakdowns
  - Performance by provider sections
  - Key findings about user-generated question difficulty
- Reweighted questions: Q1-Q30 from 0.5 → 0.25 → 0.1 (final), Q31-Q40 remain at 1.0
- Recalculated all benchmark results with new weights

### Removed
- Cleaned up 5 obsolete/untracked benchmark scripts:
  - `run_all_benchmarks.py`
  - `run_benchmarks_v2.py`
  - `run_benchmarks_v3.py`
  - `run_benchmarks_v4.py`
  - `run_google_benchmarks.py`

### Key Metrics
- Average weighted accuracy: 48.2%
- Average overall accuracy: 63.5%
- Average accuracy on user-generated questions (Q31-Q40): 41.3%
- Average accuracy on original questions (Q1-Q30): 70.9%

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
- MIT license (c) 2026 papersplx
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
