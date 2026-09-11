# Contributing to MKULTRA Benchmark

Thank you for your interest in contributing! This document outlines how to contribute to the project.

## Types of Contributions

### Benchmark Results

We welcome benchmark results from additional models! If you run the benchmark against a model not already listed in [BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md), please submit a PR with:

1. The benchmark results JSON file in the `results/` directory
2. An entry in the results table in `BENCHMARK_RESULTS.md`
3. The model name, provider, and any relevant configuration details

#### Running Multi-Model Benchmarks

To test multiple models at once, use the batch runner:

```bash
# Run all available models from models.txt
python run_all_models_benchmark.py

# Run specific provider benchmarks
python run_google_benchmark.py    # Google AI Studio models
python run_nvidia_remaining.py    # NVIDIA NIM remaining models
```

Results are saved incrementally to `results/all_models_benchmarks/combined.json`.
Models listed in `models.txt` are benchmarked using `PROVIDER_BASE_URL` and provider API keys from environment variables.

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

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
