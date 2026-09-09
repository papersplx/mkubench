#!/usr/bin/env python3
"""
Run benchmarks against remaining NVIDIA models from models.txt.
"""

import os
import sys
import time
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.model_client import OpenAIClient
from src.evaluator import BenchmarkEvaluator


MODELS = [
    "meta/muse-glimmer-30b",
]


def run_benchmark(model_name: str, api_key: str) -> dict:
    """Run benchmark for a single model."""
    print(f"\n{'='*70}")
    print(f"Running: {model_name}")
    print(f"{'='*70}")

    client = OpenAIClient(
        model=model_name,
        api_base="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
        timeout=120
    )

    dataset_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "dataset", "mkultra_benchmark.jsonl"
    )
    evaluator = BenchmarkEvaluator(dataset_path=dataset_path)

    summary = evaluator.run_evaluation(
        client,
        temperature=0.0,
        max_tokens=2048,
        delay=0.5
    )

    evaluator.print_summary(summary)
    return summary


def main():
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        print("NVIDIA_API_KEY not set")
        sys.exit(1)

    output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "results", "nvidia_models"
    )
    os.makedirs(output_dir, exist_ok=True)

    results = {}
    for model in MODELS:
        try:
            summary = run_benchmark(model, api_key)
            results[model] = summary

            # Save individual result
            timestamp = datetime.now().isoformat().replace(":", "-")
            output_file = os.path.join(output_dir, f"{model.replace('/', '_')}_{timestamp}.json")
            with open(output_file, 'w') as f:
                json.dump(summary, f, indent=2)
            print(f"\nSaved to {output_file}")

            # Delay between models
            time.sleep(2)
        except Exception as e:
            print(f"Error with {model}: {e}")
            results[model] = {"error": str(e)}

    # Save combined results
    combined_file = os.path.join(output_dir, f"combined_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(combined_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n\n{'='*70}")
    print("COMBINED RESULTS")
    print(f"{'='*70}")
    for model, result in results.items():
        if "error" not in result:
            print(f"{model:50s} {result['overall_accuracy']:5.1f}% ({result['correct']}/{result['total_questions']})")
        else:
            print(f"{model:50s} ERROR: {result['error']}")


if __name__ == "__main__":
    main()
