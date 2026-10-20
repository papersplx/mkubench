#!/usr/bin/env python3
"""Re-run the external API models against the current dataset (v2.0).

The external providers (KiloCode, NVIDIA NIM, Google AI Studio) were last
scored on dataset v1.0, before the Q37 key fix and the Q31-Q40 distractor
hardening. Their v1.0 rows are therefore not comparable with the v2.0 hosten
rows and are kept on the historical page only.

This script re-runs every external model that already has a leaderboard row
and whose provider still has credentials, using the same request/parse path as
run_all_models_benchmark.py. Results land in results/all_models_benchmarks_v2/
and are folded into leaderboard.json by merge_external_v2.py.

Usage:
    python scripts/hosten/run_external_v2.py [--only provider] [--limit N]
                       [--models-file FILE]
"""

import argparse
import json
import os
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO)
os.chdir(REPO)

from run_all_models_benchmark import (  # noqa: E402
    GOOGLE_KEYS,
    NVIDIA_KEYS,
    PROVIDERS,
    load_dataset,
    run_model,
)

DATASET_PATH = "dataset/mkultra_benchmark.jsonl"
OUTPUT_DIR = "results/all_models_benchmarks_v2"
LEADERBOARD = "leaderboard.json"


def provider_ready(provider):
    """A provider is usable when it has at least one working credential."""
    if provider == "google-ai-studio":
        return bool(GOOGLE_KEYS)
    if provider == "nvidia-nim":
        return bool(NVIDIA_KEYS)
    return bool(PROVIDERS.get(provider, {}).get("key"))


def collect_models(only=None, limit=None, models_file=None):
    """Every external model with a leaderboard row, plus the models.txt entries
    for providers that are configured. Duplicates are collapsed."""
    models = []
    seen = set()

    def add(model, provider):
        key = (model, provider)
        if key in seen:
            return
        seen.add(key)
        models.append(key)

    if os.path.exists(LEADERBOARD):
        with open(LEADERBOARD) as fh:
            lb = json.load(fh)
        for entry in lb.get("leaderboard", []):
            provider = entry.get("provider")
            if provider in PROVIDERS and provider_ready(provider):
                add(entry["model"], provider)

    if os.path.exists("models.txt"):
        with open("models.txt") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 2 and parts[1] in PROVIDERS and provider_ready(parts[1]):
                    add(parts[0], parts[1])

    if models_file:
        # Extra models the provider currently offers that have no leaderboard
        # row yet (free-tier catalogues rotate, so the v1.0 model set ages).
        with open(models_file) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 2 and parts[1] in PROVIDERS and provider_ready(parts[1]):
                    add(parts[0], parts[1])

    if only:
        models = [m for m in models if m[1] == only]
    if limit:
        models = models[:limit]
    return models


def already_done(model, provider):
    safe = model.replace("/", "_").replace(":", "_")
    path = os.path.join(OUTPUT_DIR, f"{provider}_{safe}.json")
    if not os.path.exists(path):
        return False
    try:
        with open(path) as fh:
            data = json.load(fh)
    except Exception:
        return False
    results = data.get("results") or []
    # A run counts when the provider answered every request. An answer the
    # parser could not read is a wrong answer, not a missing response, so it
    # does not make the run incomplete.
    return len(results) >= 40 and data.get("failures", 0) == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="restrict to one provider")
    parser.add_argument("--limit", type=int, help="stop after N models")
    parser.add_argument("--models-file", help="extra 'model|provider' lines")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    questions = load_dataset(DATASET_PATH)
    models = collect_models(args.only, args.limit, args.models_file)
    print(f"dataset: {len(questions)} questions ({DATASET_PATH})")
    print(f"models to run: {len(models)}")
    for model, provider in models:
        print(f"  {provider:18s} {model}")
    if args.dry_run:
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    started = time.time()
    for i, (model, provider) in enumerate(models, 1):
        if already_done(model, provider):
            print(f"[{i}/{len(models)}] skip {provider}/{model} (already complete)")
            continue
        print(f"[{i}/{len(models)}] running {provider}/{model}", flush=True)
        try:
            run_model(model, provider, questions, OUTPUT_DIR)
        except Exception as exc:  # keep going: one bad model must not stop the rest
            print(f"  [ERROR] {model}: {exc}", flush=True)
        time.sleep(3)
    print(f"done in {(time.time() - started) / 60:.1f} min -> {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
