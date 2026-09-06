#!/usr/bin/env python3
"""
MKULTRA Benchmark - Main Runner

An automated LLM benchmark test modeled after MMLU/MMLU-Pro.
Run against any local LLM (Ollama, vLLM, LocalAI) or API (OpenAI, Anthropic).

Usage examples:
    # Run against local Ollama model
    python run_benchmark.py --client ollama --model llama3

    # Run against OpenAI API
    python run_benchmark.py --client openai --model gpt-4 --api-key sk-...

    # Run against local vLLM server
    python run_benchmark.py --client openai --model local-model --api-base http://localhost:8000/v1

    # Quick test with first 5 questions
    python run_benchmark.py --client ollama --model llama3 --max-questions 5

    # Save results
    python run_benchmark.py --client ollama --model llama3 --output results/
"""
# Copyright (c) 2026 defnlnotme
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import argparse
import json
import logging
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.model_client import get_client
from src.evaluator import BenchmarkEvaluator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Run the MKULTRA benchmark against a configured model."""
    parser = argparse.ArgumentParser(
        description="MKULTRA Benchmark - Automated LLM Evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Ollama (local)
  python run_benchmark.py --client ollama --model llama3

  # OpenAI API
  python run_benchmark.py --client openai --model gpt-4

  # Local vLLM server (OpenAI-compatible)
  python run_benchmark.py --client openai --model local-model --api-base http://localhost:8000/v1

  # With custom settings
  python run_benchmark.py --client ollama --model llama3 --temperature 0.1 --max-questions 10
        """
    )

    # Model configuration
    parser.add_argument("--client", type=str, default="openai",
                        choices=["openai", "ollama"],
                        help="Model client type (default: openai)")
    parser.add_argument("--model", type=str, default="gpt-4",
                        help="Model name/identifier (default: gpt-4)")
    parser.add_argument("--api-base", type=str, default=None,
                        help="API base URL for OpenAI-compatible endpoints")
    parser.add_argument("--api-key", type=str, default=None,
                        help="API key (defaults to OPENAI_API_KEY env var)")

    # Benchmark configuration
    parser.add_argument("--dataset", type=str, default=None,
                        help="Path to dataset JSONL file (default: dataset/mkultra_benchmark.jsonl)")
    parser.add_argument("--max-questions", type=int, default=None,
                        help="Limit to first N questions (for testing)")
    parser.add_argument("--max-tokens", type=int, default=2048,
                        help="Max tokens per response (default: 2048)")
    parser.add_argument("--temperature", type=float, default=0.0,
                        help="Sampling temperature (default: 0.0)")
    parser.add_argument("--delay", type=float, default=0.1,
                        help="Delay between API calls in seconds (default: 0.1)")
    parser.add_argument("--timeout", type=int, default=120,
                        help="API request timeout in seconds (default: 120)")

    # Output configuration
    parser.add_argument("--output", type=str, default="results",
                        help="Output directory for results (default: results/)")
    parser.add_argument("--no-save-json", action="store_false", dest="save_json", default=True,
                        help="Do not save results as JSON (default: True)")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Set default dataset path
    if args.dataset is None:
        args.dataset = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "dataset", "mkultra_benchmark.jsonl"
        )

    # Ensure dataset exists
    if not os.path.exists(args.dataset):
        logger.error(f"Dataset not found: {args.dataset}")
        sys.exit(1)

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    # Initialize client
    client_kwargs = {
        "model": args.model,
        "api_base": args.api_base,
        "api_key": args.api_key,
        "timeout": args.timeout,
        "delay": args.delay,
    }
    client = get_client(client_type=args.client, **client_kwargs)

    # Initialize evaluator
    evaluator = BenchmarkEvaluator(dataset_path=args.dataset)

    # Build generation kwargs
    gen_kwargs = {
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
    }

    # Print configuration
    print("\n" + "=" * 70)
    print("MKULTRA BENCHMARK")
    print("=" * 70)
    print(f"Client:        {args.client}")
    print(f"Model:         {args.model}")
    if args.api_base:
        print(f"API Base:      {args.api_base}")
    print(f"Dataset:       {args.dataset}")
    print(f"Max Questions: {args.max_questions or 'All'}")
    print(f"Temperature:   {args.temperature}")
    print(f"Output Dir:    {args.output}")
    print("=" * 70 + "\n")

    # Run evaluation
    summary = evaluator.run_evaluation(client, max_questions=args.max_questions, **gen_kwargs)

    # Print summary
    evaluator.print_summary(summary)

    # Save results
    if args.save_json:
        timestamp = summary["timestamp"].replace(":", "-")
        output_file = os.path.join(args.output, f"results_{timestamp}.json")
        evaluator.save_results(summary, output_file)
        print(f"\nResults saved to {output_file}")

    # Exit with appropriate code
    sys.exit(0)


if __name__ == "__main__":
    main()
