#!/usr/bin/env python3
"""
Regenerate leaderboard.json from benchmark results in results/all_models_benchmarks/.

Usage:
    python regenerate_leaderboard.py

This script:
1. Reads all JSON result files from results/all_models_benchmarks/
2. Loads the dataset to get question weights
3. Recalculates weighted scores for each model
4. Generates leaderboard.json with rankings and summary statistics
"""

import json
import glob
import os
from datetime import datetime

DATASET_PATH = "dataset/mkultra_benchmark.jsonl"
RESULTS_DIR = "results/all_models_benchmarks"
OUTPUT_PATH = "leaderboard.json"


def load_dataset(path):
    """Load benchmark dataset from JSONL file."""
    questions = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                questions.append(json.loads(line))
    return questions


def calculate_model_stats(data, questions, user_generated_ids, original_ids, total_weighted_possible):
    """Calculate statistics for a single model from its result data."""
    model_name = data.get("model", "Unknown")
    provider = data.get("provider", "unknown")
    results_list = data["results"]
    
    total = len(results_list)
    correct = sum(1 for r in results_list if r.get("is_correct"))
    
    # Calculate user-generated question stats
    user_total = sum(1 for r in results_list if r.get("id") in user_generated_ids)
    user_correct = sum(1 for r in results_list if r.get("id") in user_generated_ids and r.get("is_correct"))
    
    # Calculate original question stats
    orig_total = sum(1 for r in results_list if r.get("id") in original_ids)
    orig_correct = sum(1 for r in results_list if r.get("id") in original_ids and r.get("is_correct"))
    
    # Calculate weighted score
    weighted_correct = 0.0
    for r in results_list:
        if r.get("is_correct"):
            q_id = r.get("id")
            weight = next((q["weight"] for q in questions if q["id"] == q_id), 1.0)
            weighted_correct += weight
    
    failures = data.get("failures", 0)
    
    return {
        "model": model_name,
        "provider": provider,
        "weighted_accuracy": round(weighted_correct / total_weighted_possible * 100, 1),
        "overall_accuracy": round(correct / total * 100, 1) if total > 0 else 0,
        "correct": correct,
        "total": total,
        "weighted_score": round(weighted_correct, 3),
        "weighted_possible": total_weighted_possible,
        "user_generated_accuracy": round(user_correct / user_total * 100, 1) if user_total > 0 else 0,
        "user_generated_score": f"{user_correct}/{user_total}",
        "original_accuracy": round(orig_correct / orig_total * 100, 1) if orig_total > 0 else 0,
        "original_score": f"{orig_correct}/{orig_total}",
        "failures": failures,
        "status": "complete" if failures == 0 and correct > 0 else ("partial" if correct > 0 else "failed")
    }


def regenerate_leaderboard():
    """Main function to regenerate the leaderboard from benchmark results."""
    # Load dataset
    questions = load_dataset(DATASET_PATH)
    
    user_generated_ids = set(q["id"] for q in questions if q["id"] > 30)
    original_ids = set(q["id"] for q in questions if q["id"] <= 30)
    total_weighted_possible = sum(q["weight"] for q in questions)
    
    # Process each result file
    result_files = glob.glob(os.path.join(RESULTS_DIR, "*.json"))
    leaderboard = []
    
    for result_file in result_files:
        if "combined.json" in result_file:
            continue
        
        with open(result_file, "r") as f:
            data = json.load(f)
        
        if "results" not in data or not isinstance(data.get("results"), list):
            continue
        
        stats = calculate_model_stats(data, questions, user_generated_ids, original_ids, total_weighted_possible)
        leaderboard.append(stats)
    
    # Sort by weighted accuracy
    leaderboard.sort(key=lambda x: x["weighted_accuracy"], reverse=True)
    
    # Add rank
    for i, entry in enumerate(leaderboard):
        entry["rank"] = i + 1
    
    # Calculate summary statistics
    completed = [e for e in leaderboard if e["status"] == "complete"]
    summary = {
        "total_models_tested": len(leaderboard),
        "models_with_complete_results": len(completed),
        "average_weighted_accuracy": round(sum(e["weighted_accuracy"] for e in completed) / len(completed), 1) if completed else 0,
        "average_overall_accuracy": round(sum(e["overall_accuracy"] for e in completed) / len(completed), 1) if completed else 0,
        "average_user_generated_accuracy": round(sum(e["user_generated_accuracy"] for e in completed) / len(completed), 1) if completed else 0,
        "average_original_accuracy": round(sum(e["original_accuracy"] for e in completed) / len(completed), 1) if completed else 0,
        "best_model": completed[0]["model"] if completed else None,
        "best_weighted_accuracy": completed[0]["weighted_accuracy"] if completed else 0,
    }
    
    # Build output
    output = {
        "generated_at": datetime.now().isoformat(),
        "summary": summary,
        "leaderboard": leaderboard,
        "weights": {
            "user_generated_questions": "Q31-Q40 (weight 1.0)",
            "original_questions": "Q1-Q30 (weight 0.1)",
            "total_weighted_possible": total_weighted_possible,
        },
    }
    
    # Write output
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Regenerated leaderboard with {len(leaderboard)} models")
    print(f"Output written to {OUTPUT_PATH}")
    if completed:
        print(f"Average weighted accuracy: {summary['average_weighted_accuracy']}%")
        print(f"Best model: {summary['best_model']} ({summary['best_weighted_accuracy']}%)")


if __name__ == "__main__":
    regenerate_leaderboard()