# MKULTRA Benchmark Dataset

The benchmark contains **40 questions** in `mkultra_benchmark.jsonl`:
- **Single Choice** (30 questions) - Select one correct option
- **Multiple Choice** (10 questions) - Select ALL correct options

Questions have weights: **1.0** for user-added questions (Q31-Q40) and **0.1** for original questions (Q1-Q30).

## File Structure

- `mkultra_benchmark.jsonl` - Structured benchmark dataset (JSON Lines format)
- `mkultra-benchmark.md` - Source QA data in markdown format
- `targeted_links.txt` - URLs for additional training data extraction

## Question Format

Each question includes:
- Question text with formatted options
- Correct answer(s)
- Citations
- Detailed explanations

## Training Dataset

The training dataset is built from source files in `raw/` (gitignored):
- PDFs (extracted via pdfplumber/PyPDF2)
- EPUBs (extracted via ebooklib)
- TXT files (direct reading)
- ZIP files containing PDFs (extracted individually)
- URLs from `targeted_links.txt` (filtered to skip shopping/EMF/gadget links)

Build the training dataset:
```bash
python ../build_dataset.py
```

Or use Make:
```bash
cd .. && make build-data
```

Output is in `training_data/` (gitignored):
- `training_dataset.jsonl` — Combined documents (id, title, content, source, type, metadata)
- `batches/batch_001.jsonl` through `batch_005.jsonl` — Batched documents for LLM training
- `dataset_summary.json` — Metadata about the dataset (93 docs: 40 PDFs, 9 EPUBs, 8 TXTs, 21 articles, 15 YouTube transcripts)

## Building from Source

Add questions to `mkultra-benchmark.md` following the existing format, then regenerate:
```bash
python ../scripts/regenerate_dataset.py
```

Or with make:
```bash
cd .. && python -c "import sys; sys.path.insert(0, 'scripts'); from regenerate_dataset import regenerate; regenerate()"
```