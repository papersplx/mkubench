#!/usr/bin/env python3
"""
Run benchmarks for Google AI Studio models with incremental progress saving.
"""
import os, sys, json, requests, time
from datetime import datetime
sys.path.insert(0, '/var/home/fra/dev/mkubench')
from src.parser import parse_answer, normalize_answer

questions = []
with open('/var/home/fra/dev/mkubench/dataset/mkultra_benchmark.jsonl') as f:
    for line in f:
        if line.strip():
            questions.append(json.loads(line))

GOOGLE_KEYS = [os.getenv('GEMINI_API_KEY'), os.getenv('GEMINI_API_KEY_2'), os.getenv('GEMINI_API_KEY_3'), os.getenv('GEMINI_API_KEY_4'), os.getenv('GEMINI_API_KEY_5')]
GOOGLE_KEYS = [k for k in GOOGLE_KEYS if k]

api_base = 'https://generativelanguage.googleapis.com/v1beta/openai'
output_dir = '/var/home/fra/dev/mkubench/results/all_models_benchmarks'
os.makedirs(output_dir, exist_ok=True)
combined_file = os.path.join(output_dir, 'combined.json')

model_names = ['gemini-3.5-flash-lite', 'google/gemma-4-31b-it']

for model_name in model_names:
    print(f'Running: {model_name} (via google-ai-studio)', flush=True)
    results, correct, failures = [], 0, 0
    wcorrect, wtotal = 0.0, 0.0
    key_idx = 0
    
    for i, q in enumerate(questions):
        if i > 0 and i % 2 == 0:
            key_idx += 1
        api_key = GOOGLE_KEYS[key_idx % len(GOOGLE_KEYS)]
        
        prompt = f'''Question: {q['question']}

Options:
{chr(10).join(q['options'])}

Answer with just the letter(s).'''
        
        payload = {'model': model_name, 'messages': [{'role': 'user', 'content': prompt}], 'temperature': 0.0, 'max_tokens': 2048}
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        url = f'{api_base.rstrip("/")}/chat/completions'
        
        response = None
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=30)
            if r.status_code == 200:
                data = r.json()
                if 'choices' in data:
                    content = data['choices'][0]['message'].get('content')
                    if not content:
                        content = data['choices'][0]['message'].get('reasoning', '')
                    if not content:
                        content = data['choices'][0]['message'].get('reasoning_content', '')
                    response = content.strip() if content else ''
            elif r.status_code == 404:
                print(f'  Q{i+1}: 404', flush=True)
                failures += 1
            elif r.status_code == 429:
                print(f'  Q{i+1}: 429', flush=True)
                time.sleep(10)
                failures += 1
            else:
                print(f'  Q{i+1}: {r.status_code}', flush=True)
                failures += 1
        except Exception as e:
            print(f'  Q{i+1}: timeout', flush=True)
            failures += 1
        
        weight = q.get('weight', 1.0)
        wtotal += weight
        
        if response is None:
            results.append({'id': q['id'], 'is_correct': False, 'parsed_answer': None, 'weight': weight})
            if failures >= 2:
                print(f'  [Early termination: model unavailable]', flush=True)
                break
        else:
            parsed = parse_answer(response, q['is_multiple_choice'])
            is_correct = normalize_answer(parsed, q['correct_answer'], q['is_multiple_choice'])
            results.append({'id': q['id'], 'is_correct': is_correct, 'parsed_answer': parsed, 'weight': weight})
            if is_correct:
                correct += 1
                wcorrect += weight
            status = 'OK' if is_correct else 'FAIL'
            print(f'  Q{i+1}: {status}', flush=True)
        
        # Save incremental progress
        summary = {
            'model': model_name,
            'provider': 'google-ai-studio',
            'total_questions': len(questions),
            'correct': correct,
            'failures': failures,
            'overall_accuracy': round(correct / len(questions) * 100, 1),
            'weighted_accuracy': round(wcorrect / wtotal * 100 if wtotal > 0 else 0, 1),
            'weighted_score': f'{wcorrect:.1f}/{wtotal:.1f}',
            'timestamp': datetime.now().isoformat(),
            'results': results,
        }
        safe_name = model_name.replace('/', '_').replace(':', '_')
        outfile = os.path.join(output_dir, f'google-ai-studio_{safe_name}.json')
        with open(outfile, 'w') as f:
            json.dump(summary, f, indent=2)
        with open(combined_file) as f:
            all_results = json.load(f)
        all_results[f'google-ai-studio/{model_name}'] = summary
        with open(combined_file, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
    
    # Fill remaining as failures
    tested = len(results)
    for j in range(tested, len(questions)):
        q = questions[j]
        weight = q.get('weight', 1.0)
        wtotal += weight
        results.append({'id': q['id'], 'is_correct': False, 'parsed_answer': None, 'weight': weight})
    
    total = len(questions)
    overall = correct / total * 100
    weighted = wcorrect / wtotal * 100 if wtotal > 0 else 0
    
    summary = {
        'model': model_name,
        'provider': 'google-ai-studio',
        'total_questions': total,
        'correct': correct,
        'failures': failures,
        'overall_accuracy': round(overall, 1),
        'weighted_accuracy': round(weighted, 1),
        'weighted_score': f'{wcorrect:.1f}/{wtotal:.1f}',
        'timestamp': datetime.now().isoformat(),
        'results': results,
    }
    safe_name = model_name.replace('/', '_').replace(':', '_')
    outfile = os.path.join(output_dir, f'google-ai-studio_{safe_name}.json')
    with open(outfile, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f'  Overall: {overall:.1f}% | Weighted: {weighted:.1f}% | Failures: {failures}', flush=True)
    print(f'  Saved!', flush=True)
    print()

print('Google models done!', flush=True)
