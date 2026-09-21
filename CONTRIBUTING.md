# Contributing to mkubench

Thank you for your interest in contributing! This document outlines how to contribute to the project.

## Types of Contributions

### Benchmark Results

We welcome benchmark results from additional models! If you run the benchmark against a model not already listed in [BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md), please submit a PR with:

1. The benchmark results JSON file in the `results/` directory
2. An entry in the results table in `BENCHMARK_RESULTS.md`
3. The model name, provider, and any relevant configuration details

#### Running Benchmarks

To run a benchmark against a single model:

```bash
# Run against local Ollama
python run_benchmark.py --client ollama --model llama3

# Run against OpenAI-compatible API
python run_benchmark.py --client openai --model gpt-4 --api-key sk-xxxxx

# Run against Google AI Studio
python run_benchmark.py --client openai --model gemini-3.5-flash-lite \
    --api-key $GEMINI_API_KEY \
    --api-base https://generativelanguage.googleapis.com/v1beta/openai
```

To run multiple models at once:

```bash
# Run all models from models.txt
python run_multi_model.py

# Run specific providers
python run_google_benchmark.py    # Google AI Studio models
python run_nvidia_remaining.py    # NVIDIA NIM remaining models
```

#### Validating and Regenerating Results

After adding new benchmark results, validate and regenerate the leaderboard:

```bash
# Validate all result JSON files against expected schema
python validate_results.py

# Regenerate leaderboard.json from results
python regenerate_leaderboard.py

# Generate visualization
python visualize_results.py
```

Or use Make targets:

```bash
make validate-results          # Validate result files
make regenerate-leaderboard    # Regenerate leaderboard.json
make visualize                 # Generate charts
```

** PRs for additional model benchmarks are accepted and encouraged! **

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Adding Questions

To add new benchmark questions:

1. Add questions to `mkultra-benchmark.md` following the existing format
2. Regenerate the dataset: `python scripts/regenerate_dataset.py`
3. Submit a PR with both files

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Add docstrings to all public functions
- Run `make lint` before submitting

## Testing

Run the full test suite:

```bash
make test
```

Run validation on benchmark results:

```bash
make validate-results
```

All tests must pass before submitting a PR.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
