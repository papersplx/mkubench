#!/usr/bin/env python3
"""Ask a hosten endpoint ONLY the dataset-v2.0 questions it has not answered.

The gateway's Chromium tabs hold one long conversation per site, so a single
40-question run wedges partway through. Re-asking all 40 every time is both
slow and ever more likely to wedge on a longer context. This writes a small
JSONL with just the unanswered question ids so the next run only asks those.

Usage: ask_missing_v2.py <model> [more models...]
Prints the question ids to ask and writes dataset/mkultra_missing_<model>.jsonl
"""
from __future__ import annotations

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

PROJECT = "/var/home/fra/dev/mkubench"
OUTDIR = os.path.join(PROJECT, "results", "hosten_v2")
DS = os.path.join(PROJECT, "dataset", "mkultra_benchmark.jsonl")

from merge_fill_v2 import same_dataset  # noqa: E402  (same compatibility rule)


def missing_ids(model, dataset):
    answered = set()
    for path in sorted(glob.glob(os.path.join(OUTDIR, f"results_{model}_*_detailed.json"))):
        try:
            rows = json.load(open(path)).get("results") or []
        except Exception:  # noqa: BLE001
            continue
        for r in rows:
            q = dataset.get(r["id"])
            if q and same_dataset(r, q) and (r.get("model_response") or "").strip():
                answered.add(r["id"])
    return sorted(set(dataset) - answered)


def main():
    models = sys.argv[1:]
    dataset = {}
    for line in open(DS):
        if line.strip():
            q = json.loads(line)
            dataset[q["id"]] = q

    for model in models:
        miss = missing_ids(model, dataset)
        print(f"{model}: {len(miss)} question(s) to ask: {miss}")
        if not miss:
            continue
        out = os.path.join(PROJECT, "dataset", f"mkultra_missing_{model}.jsonl")
        with open(out, "w") as fh:
            for qid in miss:
                fh.write(json.dumps(dataset[qid]) + "\n")
        print(f"  wrote {out}")


if __name__ == "__main__":
    main()
