#!/usr/bin/env python3
"""
MKULTRA Multi-Model Benchmark Runner

Run benchmarks against multiple models from models.txt or command-line arguments.
Results are saved incrementally to results/all_models_benchmarks/.

Usage:
    # Run all models from models.txt
    python run_multi_model.py

    # Run specific models
    python run_multi_model.py --models "model1" "model2" --providers "provider1" "provider2"

    # Run with custom API base
    python run_multi_model.py --api-base https://api.example.com/v1 --api-key $API_KEY

Environment Variables:
    KILOCODE_API_KEY - API key for KiloCode API
    GEMINI_API_KEY - API key for Google AI Studio
    NVIDIA_API_KEY - API key for NVIDIA NIM

Output:
    Results saved to results/all_models_benchmarks/{provider}_{model}.json
    Combined results saved to results/all_models_benchmarks/combined.json
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.parser import parse_answer, normalize_answer

# Default provider configurations
DEFAULT_PROVIDERS = {
    "kilocode": {
        "base": "https://api.kilo.ai/api/gateway/v1/chat/completions",
        "env_key": "KILOCODE_API_KEY",
    },
    "google-ai-studio": {
        "base": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        "env_key": "GEMINI_API_KEY",
    },
    "nvidia-nim": {
        "base": "https://integrate.api.nvidia.com/v1/chat/completions",
        "env_key": "NVIDIA_API_KEY",
    },
}


def load_dataset(path: str) -> list:
    """Load benchmark dataset from JSONL file."""
    questions = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                questions.append(json.loads(line))
    return questions


def call_api(
    api_key: str,
    api_base: str,
    model: str,
    messages: list,
    max_retries: int = 3,
    timeout: int = 120,
) -> str:
    """Make API call with retry logic."""
    import requests

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.0,
        "max_tokens": 2048,
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(
                api_base,
                json=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                timeout=timeout,
            )

            if response.status_code == 200:
                data = response.json()
                choice = data["choices"][0]["message"]
                content = choice.get("content")
                if content is None:
                    content = choice.get("reasoning_content", "")
                return content.strip()

            elif response.status_code == 429:
                wait_time = 2 ** attempt * 10
                print(f"    [429] Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            elif response.status_code in (500, 502, 503):
                wait_time = min(2 ** attempt * 5, 60)
                print(f"    [{response.status_code}] Server error, waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            else:
                print(f"    [{response.status_code}] {response.text[:100]}")
                time.sleep(5)
                continue

        except requests.exceptions.Timeout:
            print(f"    [Timeout] Retrying...")
            time.sleep(10)
            continue
        except Exception as e:
            print(f"    [Error] {e}")
            time.sleep(5)
            continue

    return None


def run_single_model(
    model_name: str,
    provider_name: str,
    questions: list,
    api_key: str,
    api_base: str,
) -> dict:
    """Run benchmark for a single model."""
    print(f"\n{'='*70}")
    print(f"Running: {model_name} (via {provider_name})")
    print(f"{'='*70}")

    results = []
    correct = 0
    weighted_correct = 0.0
    weighted_total = 0.0
    failures = 0

    for i, question in enumerate(questions):
        # Build prompt
        prompt = f"Question: {question['question']}\n\nOptions:\n"
        prompt += "\n".join(question["options"])
        prompt += "\n\nAnswer with just the letter(s)."

        response = call_api(api_key, api_base, model_name, [{"role": "user", "content": prompt}])

        weight = question.get("weight", 1.0)
        weighted_total += weight

        if response is None:
            print(f"  Q{question['id']}: ✗ | FAILED | Correct: {question['correct_answer']}")
            results.append({
                "id": question["id"],
                "is_correct": False,
                "parsed_answer": None,
                "weight": weight,
            })
            failures += 1
            continue

        is_multiple_choice = question.get("is_multiple_choice", False)
        parsed = parse_answer(response, is_multiple_choice)
        is_correct = normalize_answer(parsed, question["correct_answer"], is_multiple_choice)

        results.append({
            "id": question["id"],
            "is_correct": is_correct,
            "parsed_answer": parsed,
            "weight": weight,
        })

        if is_correct:
            correct += 1
            weighted_correct += weight

        status = "✓" if is_correct else "✗"
        print(f"  Q{question['id']}: {status} | Model: {parsed} | Correct: {question['correct_answer']}")

        time.sleep(0.5)

    total = len(questions)
    overall_accuracy = round(correct / total * 100, 1) if total > 0 else 0
    weighted_accuracy = round(weighted_correct / weighted_total * 100, 1) if weighted_total > 0 else 0

    summary = {
        "model": model_name,
        "provider": provider_name,
        "total_questions": total,
        "correct": correct,
        "failures": failures,
        "overall_accuracy": overall_accuracy,
        "weighted_accuracy": weighted_accuracy,
        "weighted_score": f"{weighted_correct:.3f}/{weighted_total:.3f}",
        "timestamp": datetime.now().isoformat(),
        "results": results,
    }

    print(f"\nResults: {correct}/{total} correct")
    print(f"Overall: {overall_accuracy}%")
    print(f"Weighted: {weighted_accuracy}%")

    return summary


def parse_models_txt(path: str) -> list:
    """Parse models.txt file for model configurations."""
    models = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                models.append({
                    "name": parts[0],
                    "provider": parts[1],
                })
    return models


def main():
    """Main entry point for multi-model benchmark runner."""
    parser = argparse.ArgumentParser(
        description="Run MKULTRA benchmark against multiple models",
    )
    parser.add_argument(
        "--models-file",
        type=str,
        default="models.txt",
        help="Path to models.txt file (default: models.txt)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results/all_models_benchmarks/",
        help="Output directory for results (default: results/all_models_benchmarks/)",
    )
    parser.add_argument(
        "--max-questions",
        type=int,
        default=None,
        help="Limit to first N questions",
    )
    args = parser.parse_args()

    # Load dataset
    questions = load_dataset("dataset/mkultra_benchmark.jsonl")
    if args.max_questions:
        questions = questions[:args.max_questions]

    print(f"Loaded {len(questions)} questions")

    # Load model configurations
    if os.path.exists(args.models_file):
        models = parse_models_txt(args.models_file)
    else:
        print(f"Error: {args.models_file} not found")
        sys.exit(1)

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Run benchmarks
    all_results = []
    for model_config in models:
        model_name = model_config["name"]
        provider = model_config["provider"]

        # Get provider configuration
        if provider in DEFAULT_PROVIDERS:
            provider_config = DEFAULT_PROVIDERS[provider]
            api_base = provider_config["base"]
            api_key = os.getenv(provider_config["env_key"])
        else:
            print(f"Skipping {model_name}: unknown provider {provider}")
            continue

        if not api_key:
            print(f"Skipping {model_name}: no API key for {provider}")
            continue

        try:
            result = run_single_model(model_name, provider, questions, api_key, api_base)
            all_results.append(result)

            # Save individual result
            filename = f"{provider}_{model_name.replace('/', '_')}.json"
            filepath = os.path.join(args.output_dir, filename)
            with open(filepath, "w") as f:
                json.dump(result, f, indent=2)

        except Exception as e:
            print(f"Error with {model_name}: {e}")
            import traceback
            traceback.print_exc()

    # Save combined results
    combined_path = os.path.join(args.output_dir, "combined.json")
    with open(combined_path, "w") as f:
        json.dump(all_results, f, indent=2)

    # Print leaderboard
    print(f"\n\n{'='*70}")
    print("LEADERBOARD (Weighted Accuracy)")
    print(f"{'='*70}")
    sorted_results = sorted(all_results, key=lambda x: x.get("weighted_accuracy", 0), reverse=True)
    for result in sorted_results:
        print(f"{result['model']:50s} {result['weighted_accuracy']:5.1f}%")

    print(f"\nCombined results saved to {combined_path}")


if __name__ == "__main__":
    main()