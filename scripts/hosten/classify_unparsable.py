#!/usr/bin/env python3
"""Classify unparsable (Ans: None) answers as refusal vs format mismatch."""
import glob
import json
import re
import sys

REFUSAL = re.compile(
    r"\b(can'?t help|can'?t answer|cannot provide|cannot answer|won'?t|will not|"
    r"not able to|unable to|decline|against my guidelines|I'?m sorry|I am sorry|"
    r"as an AI|I don'?t feel comfortable|inappropriate|not appropriate|conspiracy)",
    re.I,
)

files = sorted(glob.glob("results/hosten_v2/*_detailed.json"))
only = sys.argv[1:] or None
for f in files:
    data = json.load(open(f))
    model = data.get("model", f)
    if only and model not in only:
        continue
    print(f"\n=== {model} ===")
    for r in data.get("results", []):
        parsed = r.get("parsed_answer")
        if parsed is None and not r.get("is_correct"):
            resp = (r.get("model_response") or "")[:600].replace("\n", " | ")
            kind = "REFUSAL" if REFUSAL.search(resp) else "UNPARSED"
            print(f"  Q{r['id']} [{kind}] len={len(r.get('model_response') or '')}")
            print(f"      {resp[:300]}")
