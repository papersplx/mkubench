#!/usr/bin/env python3
"""Resumable single-model benchmark driver for the hosten gateway.

The stock run_benchmark.py has no resume: it restarts Q1 every time, and a run
that dies before the last question leaves no results file at all.  This driver
keeps a per-model cache of answers (results/hosten_v2/cache/<model>.json) and
writes it after every question, so an aborted attempt keeps its progress.

It also repairs a real failure mode of the gateway: a web chat answer that is
still streaming when it is captured can be returned as the answer to the NEXT
question.  Any response that shares a long common prefix with the previous
question's answer is rejected, the complete copy is promoted to the earlier
question, and the question is re-asked.

On completion it re-uses BenchmarkEvaluator to produce ordinary
results_<model>_<ts>[_detailed].json files, which aggregate_hosten_v2.py picks
up unchanged.

Usage: /usr/bin/python3 run_driver.py <model> [--timeout 900] [--settle 12]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

PROJECT = "/var/home/fra/dev/mkubench"
sys.path.insert(0, PROJECT)

from src.evaluator import BenchmarkEvaluator  # noqa: E402
from src.model_client import get_client  # noqa: E402

CACHE_DIR = os.path.join(PROJECT, "results", "hosten_v2", "cache")
OUTPUT_DIR = os.path.join(PROJECT, "results", "hosten_v2")

SETTLE_AFTER = 12.0   # let the tab stop streaming before the next question
STALE_RATIO = 0.40    # common-prefix share that marks a reused answer

RETRYABLE = (
    "timed out",
    "TimeoutError",
    "502",
    "504",
    "inject_submit_failed",
    "no_output",
    "no_response",
    "busy",
    "tab_busy",
    "browser_error_recovering",
)


def log(msg: str) -> None:
    print(msg, flush=True)


def load_cache(model: str) -> dict:
    path = os.path.join(CACHE_DIR, f"{model}.json")
    if os.path.exists(path):
        try:
            with open(path) as fh:
                return json.load(fh)
        except Exception:
            pass
    return {"model": model, "responses": {}}


def save_cache(model: str, cache: dict) -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{model}.json")
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(cache, fh)
    os.replace(tmp, path)


def prefix_ratio(a: str, b: str) -> float:
    """Share of the shorter string that both answers agree on from the start."""
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i / n


def ordered_ids(evaluator: BenchmarkEvaluator) -> list:
    return [q["id"] for q in evaluator.dataset]


def prev_response(cache: dict, evaluator: BenchmarkEvaluator, qid: int):
    """Nearest earlier question that already has an answer."""
    ids = ordered_ids(evaluator)
    try:
        idx = ids.index(qid)
    except ValueError:
        return None, ""
    for prev_id in reversed(ids[:idx]):
        txt = (cache["responses"].get(str(prev_id)) or "").strip()
        if txt:
            return prev_id, cache["responses"][str(prev_id)]
    return None, ""


def repair_stale_cache(cache: dict, evaluator: BenchmarkEvaluator) -> int:
    """Find an answer that is a re-capture of its predecessor's answer.

    Returns the number of questions blanked so they are asked again.
    """
    fixed = 0
    for qid in ordered_ids(evaluator):
        cur = cache["responses"].get(str(qid))
        if not cur or not cur.strip():
            continue
        prev_id, prev_txt = prev_response(cache, evaluator, qid)
        if prev_id is None:
            continue
        if prefix_ratio(cur, prev_txt) > STALE_RATIO:
            if len(cur) > len(prev_txt):
                # cur is the complete copy of the same answer: promote it to the
                # earlier question it really belongs to.
                cache["responses"][str(prev_id)] = cur
            cache["responses"][str(qid)] = ""
            fixed += 1
            log(f"[cache repair] Q{qid} reused Q{prev_id}'s answer; blanked")
    return fixed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--attempts", type=int, default=4, help="retries per question")
    ap.add_argument("--settle", type=float, default=SETTLE_AFTER)
    ap.add_argument("--deadline", type=str, default=None,
                    help="HH:MM local time; stop starting new questions after it")
    args = ap.parse_args()

    evaluator = BenchmarkEvaluator(os.path.join(PROJECT, "dataset", "mkultra_benchmark.jsonl"))
    cache = load_cache(args.model)
    repair_stale_cache(cache, evaluator)
    save_cache(args.model, cache)
    todo = [q for q in evaluator.dataset if not (cache["responses"].get(str(q["id"])) or "").strip()]
    log(f"[{args.model}] cached={len(evaluator.dataset) - len(todo)} missing={len(todo)}")

    if todo:
        client = get_client(
            client_type="openai",
            model=args.model,
            api_base="http://localhost:8079/v1",
            api_key="dummy",
            timeout=args.timeout,
            max_retries=1,
        )
        for question in todo:
            qid = str(question["id"])
            if args.deadline:
                now = time.localtime()
                hh, mm = (int(x) for x in args.deadline.split(":"))
                now_min = now.tm_hour * 60 + now.tm_min
                stop_min = hh * 60 + mm
                if stop_min <= now_min:
                    stop_min += 24 * 60  # deadline wraps past midnight
                if now_min >= stop_min:
                    log(f"[{args.model}] deadline {args.deadline} reached at Q{qid}; stopping")
                    break
            prompt = evaluator._build_prompt(question)
            answer = ""
            for attempt in range(1, args.attempts + 1):
                error = ""
                try:
                    answer = client.generate(
                        [{"role": "user", "content": prompt}],
                        temperature=0.0,
                        max_tokens=2048,
                    )
                except Exception as exc:  # noqa: BLE001
                    error = str(exc)
                    log(f"[{args.model}] Q{qid} attempt {attempt}: {type(exc).__name__}: {exc}")
                    answer = ""

                if (answer or "").strip():
                    prev_id, prev_txt = prev_response(cache, evaluator, question["id"])
                    if prev_id is not None and prefix_ratio(answer, prev_txt) > STALE_RATIO:
                        if len(answer) > len(prev_txt):
                            cache["responses"][str(prev_id)] = answer
                            save_cache(args.model, cache)
                            log(f"[{args.model}] promoted the complete answer to Q{prev_id}"
                                f" ({len(answer)} chars)")
                        log(f"[{args.model}] Q{qid} attempt {attempt} STALE "
                            f"(re-used Q{prev_id}'s answer); waiting {args.settle:.0f}s")
                        time.sleep(args.settle)
                        answer = ""
                        continue
                    cache["responses"][qid] = answer
                    save_cache(args.model, cache)
                    log(f"[{args.model}] Q{qid} cached ({len(answer)} chars)")
                    break

                # Not a stale answer: an empty or failed one. Retryable failures
                # get a backoff, then another attempt.
                if attempt >= args.attempts:
                    log(f"[{args.model}] Q{qid} GIVING UP this pass (left blank)")
                    cache["responses"][qid] = ""
                    save_cache(args.model, cache)
                    break
                wait = min(300, 45 * attempt)
                retryable = any(tok.lower() in error.lower() for tok in RETRYABLE)
                log(f"[{args.model}] Q{qid} attempt {attempt} empty/failed "
                    f"(retryable={retryable}); retry in {wait}s")
                time.sleep(wait)
            time.sleep(args.settle)

    complete = all(
        (cache["responses"].get(str(q["id"])) or "").strip() for q in evaluator.dataset
    )
    if not complete:
        missing = [
            q["id"] for q in evaluator.dataset
            if not (cache["responses"].get(str(q["id"])) or "").strip()
        ]
        log(f"[{args.model}] incomplete; missing question ids: {missing}")
        return 2

    results = []
    correct = 0
    weighted_correct = 0.0
    weighted_total = 0.0
    multiple_correct = multiple_total = single_correct = single_total = 0
    for question in evaluator.dataset:
        response = cache["responses"][str(question["id"])]
        row = evaluator.evaluate_single(question, response)
        results.append(row)
        weight = question.get("weight", 1.0)
        weighted_total += weight
        if row["is_correct"]:
            correct += 1
            weighted_correct += weight
            if row["is_multiple_choice"]:
                multiple_correct += 1
            else:
                single_correct += 1
        if row["is_multiple_choice"]:
            multiple_total += 1
        else:
            single_total += 1
    total = len(results)
    summary = {
        "model": args.model,
        "total_questions": total,
        "correct": correct,
        "incorrect": total - correct,
        "overall_accuracy": round(100.0 * correct / total, 2),
        "weighted_accuracy": round(100.0 * weighted_correct / weighted_total, 2),
        "weighted_score": f"{weighted_correct:.1f}/{weighted_total:.1f}",
        "single_choice_accuracy": round(100.0 * single_correct / single_total, 2) if single_total else 0.0,
        "multiple_choice_accuracy": round(100.0 * multiple_correct / multiple_total, 2) if multiple_total else 0.0,
        "single_choice_score": f"{single_correct}/{single_total}",
        "multiple_choice_score": f"{multiple_correct}/{multiple_total}",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "results": results,
    }
    evaluator.save_results(summary, OUTPUT_DIR)
    log(f"[{args.model}] wrote results to {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
