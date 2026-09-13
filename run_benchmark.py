#!/usr/bin/env python3
"""
MKULTRA Benchmark Runner

A unified entry point for running benchmarks against LLMs.
Supports single-model evaluation, multi-model batch runs, and various providers.

Usage:
    # Run against a local Ollama model
    python run_benchmark.py --client ollama --model llama3

    # Run against OpenAI API
    python run_benchmark.py --client openai --model gpt-4 --api-key sk-xxxxx

    # Run against a local vLLM server (OpenAI-compatible)
    python run_benchmark.py --client openai --model local-model --api-base http://localhost:8000/v1

    # Run against Google AI Studio (OpenAI-compatible)
    python run_benchmark.py --client openai --model gemini-3.5-flash-lite \
        --api-key $GEMINI_API_KEY \
        --api-base https://generativelanguage.googleapis.com/v1beta/openai

    # Run against NVIDIA NIM
    python run_benchmark.py --client openai --model nvidia/nemotron-3-super-120b-a12b \
        --api-key $NVIDIA_API_KEY \
        --api-base https://integrate.api.nvidia.com/v1

    # Run against Gemini native API
    python run_benchmark.py --client gemini --model gemini-2.5-flash --api-key $GEMINI_API_KEY

    # Quick test with subset
    python run_benchmark.py --client ollama --model llama3 --max-questions 5

Output:
    Results are saved as JSON files in the results/ directory:
    - results_{timestamp}.json - Summary with accuracy scores
    - results_{timestamp}_detailed.json - Full per-question results with model responses
"""

import argparse
import logging
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.evaluator import BenchmarkEvaluator
from src.model_client import get_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point for the benchmark runner."""
    parser = argparse.ArgumentParser(
        description="MKULTRA Benchmark - Evaluate LLMs on classified history knowledge",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run against local Ollama
  python run_benchmark.py --client ollama --model llama3

  # Run against OpenAI API
  python run_benchmark.py --client openai --model gpt-4 --api-key sk-xxxxx

  # Run against Google AI Studio
  python run_benchmark.py --client openai --model gemini-3.5-flash-lite \\
      --api-key $GEMINI_API_KEY \\
      --api-base https://generativelanguage.googleapis.com/v1beta/openai

  # Quick test with 5 questions
  python run_benchmark.py --client ollama --model llama3 --max-questions 5
        """,
    )

    # Required arguments
    parser.add_argument(
        "--client",
        type=str,
        choices=["openai", "ollama", "gemini"],
        default="openai",
        help="Model client type (default: openai)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4",
        help="Model name/identifier (default: gpt-4)",
    )

    # API configuration
    parser.add_argument(
        "--api-base",
        type=str,
        default=None,
        help="API base URL (for local/compatible servers)",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="API key (or use OPENAI_API_KEY env var)",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="dataset/mkultra_benchmark.jsonl",
        help="Path to dataset JSONL file (default: dataset/mkultra_benchmark.jsonl)",
    )

    # Execution options
    parser.add_argument(
        "--max-questions",
        type=int,
        default=None,
        help="Limit to first N questions (default: all 40)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Sampling temperature (default: 0.0)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2048,
        help="Max tokens per response (default: 2048)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/",
        help="Output directory for results (default: results/)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.1,
        help="Delay between API calls in seconds (default: 0.1)",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/default_config.yaml",
        help="Path to YAML config file (default: configs/default_config.yaml)",
    )
    parser.add_argument(
        "--no-save-json",
        action="store_true",
        help="Skip saving results as JSON file",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Get API key from environment if not provided
    api_key = args.api_key
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("NVIDIA_API_KEY")

    logger.info(f"Starting MKULTRA Benchmark")
    logger.info(f"Client: {args.client}")
    logger.info(f"Model: {args.model}")
    logger.info(f"Dataset: {args.dataset}")

    # Create evaluator and client
    evaluator = BenchmarkEvaluator(args.dataset)
    client = get_client(
        client_type=args.client,
        model=args.model,
        api_base=args.api_base,
        api_key=api_key,
    )

    # Run evaluation
    summary = evaluator.run_evaluation(
        client,
        max_questions=args.max_questions,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        delay=args.delay,
    )

    # Print summary
    evaluator.print_summary(summary)

    # Save results
    if not args.no_save_json:
        output_dir = args.output
        os.makedirs(output_dir, exist_ok=True)
        evaluator.save_results(summary, output_dir)
        logger.info(f"Results saved to {output_dir}")

    return summary


if __name__ == "__main__":
    main()