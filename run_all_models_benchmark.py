#!/usr/bin/env python3
"""
Comprehensive benchmark runner for all models in models.txt.
Uses PROVIDER_BASE_URL env vars for API endpoints.
"""

import json
import os
import sys
import time
import requests
from datetime import datetime

sys.path.insert(0, '.')
from src.parser import parse_answer, normalize_answer


# Provider configurations from env
PROVIDERS = {
    'kilocode': {
        'base': os.getenv('KILOCODE_BASE_URL', 'https://api.kilo.ai/api/gateway/v1'),
        'key': os.getenv('KILOCODE_API_KEY'),
        'models': []
    },
    'nvidia-nim': {
        'base': os.getenv('NVIDIA_BASE_URL', 'https://integrate.api.nvidia.com/v1'),
        'key': os.getenv('NVIDIA_API_KEY'),
        'models': []
    },
    'google-ai-studio': {
        'base': os.getenv('GEMINI_BASE_URL', 'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions'),
        'key': os.getenv('GEMINI_API_KEY'),
        'models': []
    },
    'ollama-cloud': {
        'base': os.getenv('OLLAMA_BASE_URL', 'https://api.ollama.ai/v1'),
        'key': os.getenv('OLLAMA_API_KEY'),
        'models': []
    }
}

# Additional Google keys for rotation
GOOGLE_KEYS = [
    os.getenv("GEMINI_API_KEY"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
    os.getenv("GEMINI_API_KEY_4"),
    os.getenv("GEMINI_API_KEY_5"),
]
GOOGLE_KEYS = [k for k in GOOGLE_KEYS if k]

# Additional NVIDIA keys
NVIDIA_KEYS = [
    os.getenv("NVIDIA_API_KEY"),
    os.getenv("NVIDIA_API_KEY_2"),
    os.getenv("NVIDIA_API_KEY_3"),
]
NVIDIA_KEYS = [k for k in NVIDIA_KEYS if k]


def load_dataset(path):
    questions = []
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line))
    return questions


def call_api(api_key, api_base, model, messages, provider, max_retries=3):
    """Make API call with retry logic."""
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.0,
        "max_tokens": 2048,
    }
    
    # Some providers use different auth patterns
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # Construct URL - some bases already include /chat/completions
    if '/chat/completions' in api_base:
        url = api_base
    else:
        url = f"{api_base.rstrip('/')}/chat/completions"
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=60,
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'choices' not in data:
                    print(f"    [Error] No choices in response: {str(data)[:100]}", flush=True)
                    time.sleep(3)
                    continue
                choice = data["choices"][0]["message"]
                content = choice.get("content")
                # Handle kilocode format where content is empty but reasoning has the answer
                if not content:
                    content = choice.get("reasoning", "")
                if not content:
                    content = choice.get("reasoning_content", "")
                return content.strip()
            
            elif response.status_code == 429:
                wait_time = 10 + (attempt * 5)
                print(f"    [429] Rate limited, waiting {wait_time}s...", flush=True)
                time.sleep(wait_time)
                continue
            
            elif response.status_code in (500, 502, 503):
                wait_time = min(2 ** attempt * 5, 30)
                print(f"    [{response.status_code}] Server error, waiting {wait_time}s...", flush=True)
                time.sleep(wait_time)
                continue
            
            elif response.status_code == 401:
                print(f"    [401] Unauthorized - check API key", flush=True)
                return None

            elif response.status_code == 404:
                print(f"    [404] Model not found: {model}", flush=True)
                return None
            
            else:
                print(f"    [{response.status_code}] {response.text[:100]}", flush=True)
                time.sleep(5)
                continue
                
        except requests.exceptions.Timeout:
            print(f"    [Timeout] Retry in 15s...", flush=True)
            time.sleep(15)
            continue
        except Exception as e:
            print(f"    [Error] {e}", flush=True)
            time.sleep(5)
            continue
    
    return None


def run_model(model_name, provider_name, questions, output_dir):
    """Run benchmark for a single model."""
    provider = PROVIDERS[provider_name]
    api_base = provider['base']
    
    print(f"\n{'='*60}", flush=True)
    print(f"Running: {model_name} (via {provider_name})", flush=True)
    print(f"{'='*60}", flush=True)
    
    results = []
    correct = 0
    weighted_correct = 0.0
    weighted_total = 0.0
    key_index = 0
    failures = 0
    
    for i, q in enumerate(questions):
        # Rotate keys for providers with multiple keys
        if provider_name == 'google-ai-studio' and i > 0 and i % 2 == 0:
            key_index += 1
        elif provider_name == 'nvidia-nim' and i > 0 and i % 5 == 0:
            key_index += 1
        
        if provider_name == 'google-ai-studio':
            api_key = GOOGLE_KEYS[key_index % len(GOOGLE_KEYS)]
        elif provider_name == 'nvidia-nim':
            api_key = NVIDIA_KEYS[key_index % len(NVIDIA_KEYS)]
        else:
            api_key = provider['key']
        
        prompt = f"""Question: {q['question']}

Options:
{chr(10).join(q['options'])}

Answer with just the letter(s)."""
        
        response = call_api(api_key, api_base, model_name, [{"role": "user", "content": prompt}], provider_name)
        
        weight = q.get("weight", 1.0)
        weighted_total += weight
        
        if response is None:
            failures += 1
            print(f"  Q{i+1}: FAILED | Correct: {q['correct_answer']}", flush=True)
            results.append({"id": q["id"], "is_correct": False, "parsed_answer": None, "weight": weight})
            # Early termination: if model fails repeatedly, it's likely unavailable
            if failures >= 2:
                print(f"  [Early termination: {failures} consecutive failures, model likely unavailable]", flush=True)
                break
            continue
        
        parsed = parse_answer(response, q["is_multiple_choice"])
        is_correct = normalize_answer(parsed, q["correct_answer"], q["is_multiple_choice"])
        
        results.append({"id": q["id"], "is_correct": is_correct, "parsed_answer": parsed, "weight": weight})
        
        if is_correct:
            correct += 1
            weighted_correct += weight
        
        status = "OK" if is_correct else "FAIL"
        print(f"  Q{i+1}: {status} | Model: {parsed} | Correct: {q['correct_answer']}", flush=True)
        
        # Adaptive delay
        if provider_name == 'google-ai-studio':
            time.sleep(2)
        elif provider_name == 'nvidia-nim':
            time.sleep(2)
        else:
            time.sleep(1)
    
    # Fill in any remaining questions as failures (e.g., model unavailable)
    tested_count = len(results)
    for i in range(tested_count, len(questions)):
        q = questions[i]
        weight = q.get("weight", 1.0)
        weighted_total += weight
        failures += 1
        results.append({"id": q["id"], "is_correct": False, "parsed_answer": None, "weight": weight})

    total = len(questions)
    overall = correct / total * 100 if total > 0 else 0
    weighted = weighted_correct / weighted_total * 100 if weighted_total > 0 else 0
    
    summary = {
        "model": model_name,
        "provider": provider_name,
        "total_questions": total,
        "correct": correct,
        "failures": failures,
        "overall_accuracy": round(overall, 1),
        "weighted_accuracy": round(weighted, 1),
        "weighted_score": f"{weighted_correct:.1f}/{weighted_total:.1f}",
        "timestamp": datetime.now().isoformat(),
        "results": results,
    }
    
    os.makedirs(output_dir, exist_ok=True)
    safe_name = model_name.replace('/', '_').replace(':', '_')
    outfile = os.path.join(output_dir, f"{provider_name}_{safe_name}.json")
    with open(outfile, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n  Overall: {overall:.1f}% | Weighted: {weighted:.1f}% | Failures: {failures}", flush=True)
    print(f"  Saved to {outfile}", flush=True)
    
    return summary


def parse_models_txt(path):
    """Parse models.txt and group by provider."""
    models = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 2:
                model_name = parts[0]
                provider = parts[1]
                models.append((model_name, provider))
    return models


def main():
    questions = load_dataset("dataset/mkultra_benchmark.jsonl")
    print(f"Loaded {len(questions)} questions", flush=True)
    
    # Parse models.txt
    all_models = parse_models_txt("models.txt")
    print(f"Found {len(all_models)} models in models.txt", flush=True)
    
    # Filter to only providers we have keys for
    available_providers = set()
    for name, provider in all_models:
        if provider in PROVIDERS and PROVIDERS[provider]['key']:
            available_providers.add(provider)
    
    print(f"Available providers: {available_providers}", flush=True)
    
    # Filter models to available providers
    models_to_test = [(name, provider) for name, provider in all_models if provider in available_providers]
    print(f"Models to test: {len(models_to_test)}", flush=True)
    
    output_dir = "results/all_models_benchmarks"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load existing results
    all_results = {}
    combined_file = os.path.join(output_dir, "combined.json")
    if os.path.exists(combined_file):
        with open(combined_file, 'r') as f:
            all_results = json.load(f)
    
    # Test each model
    for model_name, provider_name in models_to_test:
        # Create unique key
        result_key = f"{provider_name}/{model_name}"
        
        # Skip if already completed with < 10 failures
        if result_key in all_results:
            r = all_results[result_key]
            if r.get('failures', 0) < 10:
                print(f"\nSkipping {result_key} (already completed)", flush=True)
                continue
        
        try:
            summary = run_model(model_name, provider_name, questions, output_dir)
            all_results[result_key] = summary
            
            # Save combined after each model
            with open(combined_file, 'w') as f:
                json.dump(all_results, f, indent=2, default=str)
            
            print(f"\n  Pausing 5s before next model...", flush=True)
            time.sleep(5)
        except Exception as e:
            print(f"Error: {e}", flush=True)
            import traceback
            traceback.print_exc()
            all_results[result_key] = {"error": str(e)}
    
    # Final leaderboard
    print(f"\n\n{'='*60}", flush=True)
    print("LEADERBOARD (Weighted Accuracy)", flush=True)
    print(f"{'='*60}", flush=True)
    sorted_models = sorted(
        [(n, r) for n, r in all_results.items() if "error" not in r],
        key=lambda x: x[1]["weighted_accuracy"],
        reverse=True,
    )
    for name, r in sorted_models:
        fail_str = f" ({r.get('failures', 0)} failed)" if r.get('failures', 0) > 0 else ""
        print(f"  {name:50s} {r['weighted_accuracy']:5.1f}% (overall: {r['overall_accuracy']}%){fail_str}", flush=True)
    
    print(f"\nResults saved to {output_dir}/", flush=True)


if __name__ == "__main__":
    main()
