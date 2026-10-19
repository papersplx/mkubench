#!/usr/bin/env python3
"""Is a model's dataset-v2 run complete AND usable?

Exits 0 only when a results_<model>_<ts>.json (short summary) exists whose
_detailed.json sibling has all 40 questions AND no empty model_response.
A run with missing questions must be re-run, so mere file existence is not
enough - mistral's limit-limited run produced 35/40 empty responses.
"""
import glob
import json
import os
import sys

model = sys.argv[1]
DS = "/var/home/fra/dev/mkubench/dataset/mkultra_benchmark.jsonl"
OUTDIR = "/var/home/fra/dev/mkubench/results/hosten_v2"

n_questions = sum(1 for line in open(DS) if line.strip())

short = [
    p
    for p in sorted(glob.glob(os.path.join(OUTDIR, f"results_{model}_*.json")))
    if not p.endswith("_detailed.json")
]
if not short:
    print(f"{model}: INCOMPLETE (no summary file)")
    sys.exit(1)

for det in short:
    det_path = det[: -len(".json")] + "_detailed.json"
    if not os.path.exists(det_path):
        continue
    try:
        data = json.load(open(det_path))
    except Exception as e:  # noqa: BLE001
        print(f"{model}: INCOMPLETE (unreadable {os.path.basename(det_path)}: {e})")
        sys.exit(1)
    res = data.get("results") or []
    empty = sum(1 for r in res if not (r.get("model_response") or "").strip())
    if len(res) >= n_questions and empty == 0:
        ok = sum(1 for r in res if r.get("is_correct"))
        print(f"{model}: COMPLETE {ok}/{len(res)} (0 empty) - {os.path.basename(det_path)}")
        sys.exit(0)
    # keep looking at older/newer files
    print(
        f"{model}: INCOMPLETE {os.path.basename(det_path)}: {len(res)}/{n_questions} "
        f"questions, {empty} empty responses"
    )

print(f"{model}: INCOMPLETE (no valid run found)")
sys.exit(1)
