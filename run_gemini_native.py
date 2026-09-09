#!/usr/bin/env python3
"""
Run Gemini benchmark with proper rate limiting.
Gemini free tier: 20 requests per minute = 3 second minimum delay.
"""

import os
import sys
import time
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.model_client import GeminiClient
from src.evaluator import BenchmarkEvaluator


def wait_for_rate_limit_reset(api_key: str) -> None:
    """Wait until Gemini rate limit resets."""
    import requests
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": "hi"}]}],
        "generationConfig": {"maxOutputTokens": 1}
    }

    while True:
        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                print("Rate limit reset, starting benchmark...")
                return
            elif response.status_code == 429:
                # Parse retry time
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "")
                import re
                retry_match = re.search(r"retry in ([\d.]+)s", error_msg)
                if retry_match:
                    wait_time = float(retry_match.group(1)) + 2
                else:
                    wait_time = 60
                print(f"Rate limited. Waiting {wait_time:.0f}s...")
                time.sleep(wait_time)
            else:
                print(f"Unexpected status: {response.status_code}")
                time.sleep(30)
        except Exception as e:
            print(f"Error checking rate limit: {e}")
            time.sleep(30)


def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not set")
        sys.exit(1)

    # Wait for rate limit to reset
    print("Checking Gemini API rate limit...")
    wait_for_rate_limit_reset(api_key)

    # Initialize client
    client = GeminiClient(
        model="gemini-2.5-flash",
        api_key=api_key,
        timeout=120
    )

    # Load evaluator
    dataset_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "dataset", "mkultra_benchmark.jsonl"
    )
    evaluator = BenchmarkEvaluator(dataset_path=dataset_path)

    # Run evaluation with 5 second delay between requests
    print(f"\n{'='*70}")
    print("MKULTRA BENCHMARK - Gemini 2.5 Flash (Native API)")
    print(f"{'='*70}")
    print(f"Questions: 30")
    print(f"Delay between requests: 5s (rate limit: 20 req/min)")
    print(f"{'='*70}\n")

    summary = evaluator.run_evaluation(
        client,
        temperature=0.0,
        max_tokens=2048,
        delay=5.0
    )

    # Print summary
    evaluator.print_summary(summary)

    # Save results
    output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "results", "gemini_native"
    )
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().isoformat().replace(":", "-")
    output_file = os.path.join(output_dir, f"results_{timestamp}.json")
    evaluator.save_results(summary, output_file)
    print(f"\nResults saved to {output_file}")

    # Also save detailed results
    detailed_file = os.path.join(output_dir, f"results_{timestamp}_detailed.json")
    with open(detailed_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Detailed results saved to {detailed_file}")


if __name__ == "__main__":
    main()
