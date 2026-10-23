#!/usr/bin/env python3
"""Re-score finished V2 runs in place with the current parser.

Reads the latest results_<model>_*_detailed.json for each requested model,
re-parses every stored model_response with src.parser, recomputes is_correct and
the summary, and rewrites both files.  The questions are never re-asked, so this
is safe to run while the gateway/idle machine does nothing.
"""
from __future__ import annotations

import fcntl
import glob
import json
import os
import sys

PROJECT = "/var/home/fra/dev/mkubench"
sys.path.insert(0, PROJECT)

from src.evaluator import BenchmarkEvaluator  # noqa: E402
from src.parser import normalize_answer, parse_answer  # noqa: E402

LOCKFILE = os.path.join(PROJECT, "results", "logs", "merge.lock")


def lock_results_file():
    """Serialize result-file writes with the other writers.

    The fill runner and the publisher both re-score the same
    results_<model>_*_detailed.json files.  A concurrent write can truncate a
    file the aggregator is about to read, so both take this lock.
    """
    os.makedirs(os.path.dirname(LOCKFILE), exist_ok=True)
    handle = open(LOCKFILE, "w")
    fcntl.flock(handle, fcntl.LOCK_EX)
    return handle


def latest(model: str) -> str:
    files = sorted(glob.glob(os.path.join(PROJECT, "results", "hosten_v2",
                                          f"results_{model}_*_detailed.json")))
    if not files:
        raise SystemExit(f"no results file for {model}")
    return files[-1]


def main() -> None:
    models = sys.argv[1:] or ["claude", "meta", "qwen", "grok", "kimi", "mistral", "zai"]
    _lock = lock_results_file()
    ev = BenchmarkEvaluator(os.path.join(PROJECT, "dataset", "mkultra_benchmark.jsonl"))
    by_id = {q["id"]: q for q in ev.dataset}

    for model in models:
        files = glob.glob(os.path.join(PROJECT, "results", "hosten_v2",
                                       f"results_{model}_*_detailed.json"))
        if not files:
            print(f"{model}: no results file, skipped")
            continue
        path = sorted(files)[-1]
        data = json.load(open(path))
        rows = data.get("results") or []
        changed = 0
        for row in rows:
            q = by_id[row["id"]]
            parsed = parse_answer(row["model_response"], q["is_multiple_choice"])
            correct = normalize_answer(parsed, q["correct_answer"], q["is_multiple_choice"])
            if parsed != row["parsed_answer"] or correct != row["is_correct"]:
                print(f"  {model} Q{row['id']}: {row['parsed_answer']} -> {parsed}, "
                      f"correct {row['is_correct']} -> {correct}")
                row["parsed_answer"] = parsed
                row["is_correct"] = correct
                changed += 1

        # Recompute the summary from the re-scored rows.
        total = len(rows)
        correct = sum(1 for r in rows if r["is_correct"])
        weighted_correct = sum(
            by_id[r["id"]]["weight"] for r in rows if r["is_correct"]
        )
        weighted_total = sum(by_id[i]["weight"] for i in by_id)
        user_ids = {i for i in by_id if i > 30}
        orig_ids = set(by_id) - user_ids
        user_total = sum(1 for r in rows if r["id"] in user_ids)
        user_ok = sum(1 for r in rows if r["id"] in user_ids and r["is_correct"])
        orig_total = sum(1 for r in rows if r["id"] in orig_ids)
        orig_ok = sum(1 for r in rows if r["id"] in orig_ids and r["is_correct"])

        new = {
            "model": model,
            "total_questions": total,
            "correct": correct,
            "incorrect": total - correct,
            "overall_accuracy": round(100 * correct / total, 2),
            "weighted_accuracy": round(100 * weighted_correct / weighted_total, 2),
            "weighted_score": f"{weighted_correct:.1f}/{weighted_total:.1f}",
            "single_choice_accuracy": 0.0,
            "multiple_choice_accuracy": 0.0,
            "single_choice_score": "0/0",
            "multiple_choice_score": "0/0",
            "timestamp": data.get("timestamp"),
            "results": rows,
        }
        # keep the single/multiple split consistent with the evaluator
        s_t = sum(1 for r in rows if not r["is_multiple_choice"])
        m_t = total - s_t
        s_c = sum(1 for r in rows if not r["is_multiple_choice"] and r["is_correct"])
        m_c = correct - s_c
        new["single_choice_accuracy"] = round(100 * s_c / s_t, 2) if s_t else 0.0
        new["multiple_choice_accuracy"] = round(100 * m_c / m_t, 2) if m_t else 0.0
        new["single_choice_score"] = f"{s_c}/{s_t}"
        new["multiple_choice_score"] = f"{m_c}/{m_t}"
        data.update(new)

        with open(path, "w") as fh:
            json.dump(data, fh, indent=2)
        short = path.replace("_detailed.json", ".json")
        summary_only = {k: v for k, v in data.items() if k != "results"}
        with open(short, "w") as fh:
            json.dump(summary_only, fh, indent=2)
        print(f"{model}: {changed} rows re-scored, now {correct}/{total} "
              f"(user {user_ok}/{user_total}, original {orig_ok}/{orig_total})")


if __name__ == "__main__":
    main()
