#!/usr/bin/env python3
"""
Run benchmarks against Google AI Studio OpenAI-compatible endpoint.
Uses multiple API keys for higher rate limits.
Models: gemini-3.5-flash-lite, gemma-4-31b-it
"""

import os
import sys
import time
import json
import requests
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.parser import parse_answer, normalize_answer


MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemma-4-31b-it",
]

API_KEYS = [
    os.getenv("GEMINI_API_KEY"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
    os.getenv("GEMINI_API_KEY_4"),
    os.getenv("GEMINI_API_KEY_5"),
]
API_KEYS = [k for k in API_KEYS if k]

API_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"


def load_dataset(path):
    """Load JSONL dataset."""
    questions = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                questions.append(json.loads(line))
    return questions


def call_api(api_key, model, messages, max_retries=5):
    """Make API call with retry logic for 429, 500, 503 errors."""
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.0,
        "max_tokens": 2048,
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                API_BASE,
                json=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                timeout=120,
            )
            
            if response.status_code == 200:
                data = response.json()
                choice = data["choices"][0]["message"]
                content = choice.get("content")
                if content is None:
                    content = choice.get("reasoning_content", "")
                return content.strip()
            
            # Handle rate limiting
            elif response.status_code == 429:
                import re
                error_msg = response.text
                retry_match = re.search(r"retry in ([\d.]+)s", error_msg)
                wait_time = float(retry_match.group(1)) + 2 if retry_match else 60
                print(f"    [429] Rate limited, waiting {wait_time:.0f}s...")
                time.sleep(wait_time)
                continue
            
            # Handle server errors with exponential backoff
            elif response.status_code in (500, 502, 503):
                wait_time = min(2 ** attempt * 5, 60)
                print(f"    [{response.status_code}] Server error, waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
            
            else:
                print(f"    [{response.status_code}] {response.text[:200]}")
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


def run_benchmark(model_name, questions):
    """Run benchmark for a single model using multiple keys."""
    print(f"\n{'='*70}")
    print(f"Running: {model_name}")
    print(f"Using {len(API_KEYS)} API keys")
    print(f"{'='*70}")

    results = []
    correct = 0
    multiple_correct = 0
    multiple_total = 0
    key_index = 0

    for i, question in enumerate(questions):
        # Rotate keys every 3 requests
        if i > 0 and i % 3 == 0:
            key_index += 1
        
        api_key = API_KEYS[key_index % len(API_KEYS)]
        
        prompt = f"""Question: {question['question']}

Options:
{chr(10).join(question['options'])}

Answer with just the letter(s)."""

        response = call_api(api_key, model_name, [{"role": "user", "content": prompt}])
        
        if response is None:
            print(f"  Q{i+1}: ✗ | FAILED (no response) | Correct: {question['correct_answer']}")
            results.append({
                "id": question["id"],
                "is_correct": False,
                "parsed_answer": None,
                "is_multiple_choice": question["is_multiple_choice"],
                "model_response": None,
            })
            if question["is_multiple_choice"]:
                multiple_total += 1
            continue
        
        parsed = parse_answer(response, question["is_multiple_choice"])
        is_correct = normalize_answer(parsed, question["correct_answer"], question["is_multiple_choice"])
        
        results.append({
            "id": question["id"],
            "is_correct": is_correct,
            "parsed_answer": parsed,
            "is_multiple_choice": question["is_multiple_choice"],
            "model_response": response[:500],
        })
        
        if is_correct:
            correct += 1
        if question["is_multiple_choice"]:
            multiple_total += 1
            if is_correct:
                multiple_correct += 1
        
        status = "✓" if is_correct else "✗"
        print(f"  Q{i+1}: {status} | Model: {parsed} | Correct: {question['correct_answer']}")
        
        time.sleep(0.5)

    total = len(questions)
    single_total = total - multiple_total
    single_correct = correct - multiple_correct
    
    summary = {
        "total_questions": total,
        "correct": correct,
        "incorrect": total - correct,
        "overall_accuracy": round(correct / total * 100, 2) if total > 0 else 0,
        "single_choice_accuracy": round(single_correct / single_total * 100, 2) if single_total > 0 else 0,
        "multiple_choice_accuracy": round(multiple_correct / multiple_total * 100, 2) if multiple_total > 0 else 0,
        "single_choice_score": f"{single_correct}/{single_total}",
        "multiple_choice_score": f"{multiple_correct}/{multiple_total}",
        "timestamp": datetime.now().isoformat(),
        "results": results
    }

    print(f"\n{'='*70}")
    print("BENCHMARK RESULTS")
    print(f"{'='*70}")
    print(f"Total Questions:    {total}")
    print(f"Correct:            {correct}")
    print(f"Incorrect:          {total - correct}")
    print(f"Overall Accuracy:   {summary['overall_accuracy']}%")
    print(f"Single Choice:      {summary['single_choice_accuracy']}% ({summary['single_choice_score']})")
    print(f"Multiple Choice:    {summary['multiple_choice_accuracy']}% ({summary['multiple_choice_score']})")

    return summary


def main():
    dataset_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "dataset", "mkultra_benchmark.jsonl"
    )
    questions = load_dataset(dataset_path)
    print(f"Loaded {len(questions)} questions")

    output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "results", "google_ai_studio"
    )
    os.makedirs(output_dir, exist_ok=True)

    all_results = {}
    for model in MODELS:
        try:
            summary = run_benchmark(model, questions)
            all_results[model] = summary

            # Save individual result
            timestamp = datetime.now().isoformat().replace(":", "-")
            output_file = os.path.join(output_dir, f"{model}_{timestamp}.json")
            with open(output_file, 'w') as f:
                json.dump(summary, f, indent=2)
            print(f"\nSaved to {output_file}")

            # Delay between models
            time.sleep(10)
        except Exception as e:
            print(f"Error with {model}: {e}")
            import traceback
            traceback.print_exc()
            all_results[model] = {"error": str(e)}

    # Save combined results
    combined_file = os.path.join(output_dir, f"combined_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(combined_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\n\n{'='*70}")
    print("COMBINED RESULTS")
    print(f"{'='*70}")
    for model, result in all_results.items():
        if "error" not in result:
            print(f"{model:50s} {result['overall_accuracy']:5.1f}% ({result['correct']}/{result['total_questions']})")
        else:
            print(f"{model:50s} ERROR: {result['error']}")


if __name__ == "__main__":
    main()
