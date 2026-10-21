#!/usr/bin/env python3
"""
Aggregate per-model benchmark JSON results from results/hosten/ into the
shared leaderboard.json format, then regenerate the website + BENCHMARK_RESULTS.md.

Reads results/hosten/results_<model>_<timestamp>.json files produced by
run_benchmark.py (with --output results/hosten).
"""
import glob
import json
import os
from datetime import datetime

DATASET_PATH = "dataset/mkultra_benchmark.jsonl"
RESULTS_DIR = "results/hosten"
OUTPUT_PATH = "leaderboard.json"

# Mapping: endpoint ID -> underlying model name (for display)
MODEL_NAMES = {
    "claude": "claude-sonnet-5",
    "mistral": "mistral-medium-3.5",
    "zai": "glm-5.3-flash",
    "meta": "muse-spark-1.1",
    "qwen": "qwen-3.8-max",
    "grok": "grok-4.5",
    "google": "gemini-3.8-flash",
    "kimi": "kimi-k3",
    "copilot": "gpt-5.6",
}
PROVIDER = "hosten"


def load_dataset(path):
    questions = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                questions.append(json.loads(line))
    return questions


def main():
    questions = load_dataset(DATASET_PATH)
    user_ids = set(q["id"] for q in questions if q["id"] > 30)
    orig_ids = set(q["id"] for q in questions if q["id"] <= 30)
    weighted_possible = sum(q["weight"] for q in questions)

    files = sorted(glob.glob(os.path.join(RESULTS_DIR, "results_*.json")))
    # Skip detailed files (they end with _detailed.json)
    files = [f for f in files if not f.endswith("_detailed.json")]

    # Merge with any pre-existing leaderboard entries (e.g. KiloCode / NVIDIA)
    existing = []
    if os.path.exists(OUTPUT_PATH):
        try:
            with open(OUTPUT_PATH) as fh:
                existing = json.load(fh).get("leaderboard", [])
        except Exception:
            existing = []
    existing_ids = {e.get("endpoint_id") or e["model"] for e in existing}
    existing = [e for e in existing if (e.get("endpoint_id") or e["model"]) not in set(MODEL_NAMES.keys())]

    leaderboard = []
    for f in files:
        with open(f) as fh:
            data = json.load(fh)
        results = data.get("results", [])
        total = len(results)
        correct = sum(1 for r in results if r.get("is_correct"))
        weighted_correct = sum(
            q["weight"] for q, r in zip(questions, results)
            if r.get("is_correct") and q["id"] == r["id"]
        )
        # Map by id to be safe
        by_id = {r["id"]: r for r in results}
        weighted_correct = sum(
            q["weight"] for q in questions if by_id.get(q["id"], {}).get("is_correct")
        )
        user_total = sum(1 for r in results if r.get("id") in user_ids)
        user_correct = sum(1 for r in results if r.get("id") in user_ids and r.get("is_correct"))
        orig_total = sum(1 for r in results if r.get("id") in orig_ids)
        orig_correct = sum(1 for r in results if r.get("id") in orig_ids and r.get("is_correct"))

        # model id from filename: results_<model>_<timestamp>.json
        base = os.path.basename(f)
        model_id = base[len("results_"):-len(".json")]
        # strip trailing _YYYYMMDD_HHMMSS
        parts = model_id.rsplit("_", 2)
        if len(parts) == 3 and len(parts[1]) == 8 and len(parts[2]) == 6:
            model_id = parts[0]

        model_name = MODEL_NAMES.get(model_id, model_id)
        failures = data.get("incorrect", total) - (total - correct)
        status = "complete" if (failures == 0 and correct > 0) else ("partial" if correct > 0 else "failed")

        leaderboard.append({
            "model": model_name,
            "endpoint_id": model_id,
            "provider": PROVIDER,
            "weighted_accuracy": round(weighted_correct / weighted_possible * 100, 1),
            "overall_accuracy": round(correct / total * 100, 1) if total else 0,
            "correct": correct,
            "total": total,
            "weighted_score": round(weighted_correct, 3),
            "weighted_possible": weighted_possible,
            "user_generated_accuracy": round(user_correct / user_total * 100, 1) if user_total else 0,
            "user_generated_score": f"{user_correct}/{user_total}",
            "original_accuracy": round(orig_correct / orig_total * 100, 1) if orig_total else 0,
            "original_score": f"{orig_correct}/{orig_total}",
            "failures": failures,
            "status": status,
            "rank": 0,
        })

    leaderboard.extend(existing)
    leaderboard.sort(key=lambda x: x["weighted_accuracy"], reverse=True)
    for i, e in enumerate(leaderboard):
        e["rank"] = i + 1

    completed = [e for e in leaderboard if e["status"] == "complete"]
    summary = {
        "total_models_tested": len(leaderboard),
        "models_with_complete_results": len(completed),
        "average_weighted_accuracy": round(sum(e["weighted_accuracy"] for e in completed) / len(completed), 1) if completed else 0,
        "average_overall_accuracy": round(sum(e["overall_accuracy"] for e in completed) / len(completed), 1) if completed else 0,
        "average_user_generated_accuracy": round(sum(e["user_generated_accuracy"] for e in completed) / len(completed), 1) if completed else 0,
        "average_original_accuracy": round(sum(e["original_accuracy"] for e in completed) / len(completed), 1) if completed else 0,
        "best_model": leaderboard[0]["model"] if leaderboard else "-",
        "best_weighted_accuracy": leaderboard[0]["weighted_accuracy"] if leaderboard else 0,
    }

    out = {
        "generated_at": datetime.now().isoformat(),
        "summary": summary,
        "leaderboard": leaderboard,
        "weights": {
            "user_generated_questions": "Q31-Q40 (weight 1.0)",
            "original_questions": "Q1-Q30 (weight 0.1)",
            "total_weighted_possible": weighted_possible,
        },
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()