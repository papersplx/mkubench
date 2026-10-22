#!/usr/bin/env python3
"""Merge all dataset-v2.0 runs of one hosten endpoint into one complete file.

The gateway's Chromium tabs wedge mid-run, so a single 40-question run often
stops short. Every row stored here is a real response from the same endpoint on
the same dataset, so filling a run's blanks from another run of the SAME
endpoint is a resume, not a new measurement: the newest non-empty answer for a
question wins and older runs only supply rows the newest one left blank.

Safety: a run is only merged when the stored question text matches the current
dataset for that id. Runs taken against an older/edited dataset (different
question text or key) are skipped so their answers cannot be mis-attributed.

Usage: merge_fill_v2.py <model> [--apply]
Without --apply the script only reports what it would do.
"""
from __future__ import annotations

import glob
import json
import os
import sys
from datetime import datetime

PROJECT = "/var/home/fra/dev/mkubench"
OUTDIR = os.path.join(PROJECT, "results", "hosten_v2")
DS = os.path.join(PROJECT, "dataset", "mkultra_benchmark.jsonl")

# The aggregator's filename regex: results_<model>_<YYYYmmdd_HHMMSS>[_detailed].json
PREFIX = "results_"
SUFFIX = "_detailed.json"


def load(path):
    try:
        return json.load(open(path))
    except Exception as e:  # noqa: BLE001
        print(f"  unreadable {os.path.basename(path)}: {e}")
        return None


def same_dataset(row, q):
    """Is this row the same question as today's dataset entry?

    The runner truncates the stored question text to ~200 chars for the log and
    the results file, so compare the fields it stores in full instead: title,
    options, the answer key and the single/multiple flag.
    """
    return (
        str(row.get("title")) == str(q.get("title"))
        and row.get("options") == q.get("options")
        and str(row.get("correct_answer")) == str(q.get("correct_answer"))
        and bool(row.get("is_multiple_choice")) == bool(q.get("is_multiple_choice"))
    )


def main():
    model = sys.argv[1]
    apply = "--apply" in sys.argv

    dataset = {}
    for line in open(DS):
        if line.strip():
            q = json.loads(line)
            dataset[q["id"]] = q
    n_q = len(dataset)

    paths = sorted(
        p for p in glob.glob(os.path.join(OUTDIR, f"results_{model}_*_detailed.json"))
        if os.path.basename(p).startswith(f"{PREFIX}{model}_")
        and os.path.basename(p).endswith(SUFFIX)
        and os.path.sep not in os.path.relpath(p, OUTDIR)
    )
    if not paths:
        print(f"{model}: no detailed files")
        sys.exit(1)
    print(f"{model}: {len(paths)} detailed files")

    runs = []  # (basename, mtime, {id: row}) newest last
    for path in paths:
        base = os.path.basename(path)
        stamp = base[len(PREFIX) + len(model) + 1: -len(SUFFIX)]
        data = load(path)
        if not data:
            continue
        rows = data.get("results") or []
        # Only runs whose stored questions match today's dataset count.
        mismatch = [
            r["id"] for r in rows
            if r["id"] in dataset and not same_dataset(r, dataset[r["id"]])
        ]
        if mismatch:
            print(f"  SKIP {base}: differs from the current dataset on ids "
                  f"{mismatch[:5]} - not merged")
            continue
        by_id = {r["id"]: r for r in rows}
        runs.append((base, stamp, by_id))

    if not runs:
        print(f"{model}: no run matches the current dataset")
        sys.exit(1)

    # newest non-empty answer wins; older runs fill the newest run's blanks
    best = {}
    for base, _stamp, by_id in runs:
        for qid, row in by_id.items():
            if (row.get("model_response") or "").strip():
                best[qid] = (base, row)
            else:
                best.setdefault(qid, (base, row))

    complete_runs = [b for b, _s, rows in runs
                     if len(rows) >= n_q and
                     all((r.get("model_response") or "").strip() for r in rows.values())]
    if complete_runs:
        print(f"  already complete in {complete_runs[-1]} - no merge needed")
        sys.exit(0)

    filled = [q for q, (_, r) in best.items() if (r.get("model_response") or "").strip()]
    missing = sorted(set(dataset) - set(filled))
    print(f"  answered by at least one run: {len(filled)}/{n_q}")
    print(f"  missing (no run ever answered): {missing}")
    if not apply or missing:
        return

    rows = []
    for qid in sorted(best):
        _, row = best[qid]
        row = dict(row)
        row.setdefault("id", qid)
        rows.append(row)
    if any(not (r.get("model_response") or "").strip() for r in rows):
        print("  refusing to write: some questions are still blank")
        sys.exit(1)

    # Write the merged record under the CURRENT time, so it is the newest run
    # of this model and the aggregator picks it up as the model's result. The
    # per-run files stay on disk untouched as the raw evidence.
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = os.path.join(OUTDIR, f"{PREFIX}{model}_{stamp}{SUFFIX}")
    json.dump(
        {
            "model": model,
            "total_questions": n_q,
            "merged_from": sorted(b for b, _s, _r in runs),
            "results": rows,
        },
        open(out, "w"),
        indent=2,
    )
    print(f"  wrote {os.path.basename(out)} ({len(rows)} rows, {len(filled)} answered)")


if __name__ == "__main__":
    main()
