#!/usr/bin/env python3
"""Aggregate the dataset-v2.0 hosten run into leaderboard.json + docs.

Reads results/hosten_v2/results_<model>_<timestamp>_detailed.json (the short
summary strips the per-question array, which this needs for weighted/block
scores), merges the untouched external-provider entries from the current
leaderboard.json, and refreshes:

  leaderboard.json
  docs/assets/data/leaderboard.json
  README.md          (Benchmark Results table + key observations)
  BENCHMARK_RESULTS.md (summary, leaderboard, histogram, findings, hosten table)

Usage: python aggregate_hosten_v2.py [--check]
"""
import glob
import json
import os
import re
import sys
from datetime import datetime

DATASET_PATH = "dataset/mkultra_benchmark.jsonl"
RESULTS_DIR = "results/hosten_v2"
# External API models (KiloCode, NVIDIA NIM, Google AI Studio) re-run against
# the current dataset. Their v1.0 rows are replaced when the re-run produced
# answers, and kept when the provider could not answer at all.
EXTERNAL_RESULTS_DIR = "results/all_models_benchmarks_v2"
OUTPUT_PATH = "leaderboard.json"
DOCS_PATH = "docs/assets/data/leaderboard.json"
DATASET_VERSION = "2.0"
PROVIDER_LABEL = "hosten"

MODEL_NAMES = {
    "claude": "claude-sonnet-5",
    "mistral": "mistral-medium-3.5",
    "zai": "glm-5.3-flash",
    "meta": "muse-spark-1.1",
    "qwen": "qwen-3.8-max",
    "grok": "grok-4.5",
    "google": "gemini-3.8-flash",
    "kimi": "kimi-k3",
    "tencent": "hy4-preview",
    "copilot": "gpt-5.6",
}
PROVIDER_DISPLAY = {
    "kilocode": "KiloCode API",
    "nvidia-nim": "NVIDIA NIM",
    "google-ai-studio": "Google AI Studio",
}

# Entries with no scoreable run (correct == 0) are the "Failed models" list in the
# docs; they live in leaderboard.json for completeness but must not be ranked as 0.0%.
def scoreable(e):
    return e.get("correct", 0) > 0

# Why a hosten endpoint could not be re-run on dataset v2.0. Surfaced verbatim in
# leaderboard.json so the gap is auditable instead of looking like a missing file.
BLOCKED_REASONS = {
    "google": "site signed the account out; requires an interactive Google login "
              "in the Chromium window (automation not possible)",
    "copilot": "Cloudflare Turnstile 'Verification required' modal re-arms on every "
               "submit; requires a human solve",
    "kimi": "site rate-limited ('too many people are chatting'); throttling window",
    "mistral": "single-tab run started after the account message-limit window "
              "cleared (~16:30 2026-10-19) but Q1 never completed (fresh tab "
              "cannot answer chat completions; session/login-gated), so no "
              "complete 40-question run could be produced",
    "tencent": "site answers only after a long deep-thinking pass; the tab wedges "
              "mid-run (Q2 stalled >15 min after Q1 took ~4 min), so no complete "
              "40-question run could be produced",
    "grok": "single-tab run started after the 'under heavy usage' rate-limit "
            "window cleared (~17:51 2026-10-19) but Q1 read timed out at 2400s "
            "with zero response (same session/login-gated wedge as mistral/"
            "tencent), so no complete 40-question run could be produced",
}

AUTHORS = {
    "claude": "Anthropic",
    "mistral": "Mistral AI",
    "zai": "Z.ai",
    "meta": "Meta",
    "qwen": "Alibaba",
    "grok": "xAI",
    "google": "Google",
    "kimi": "Moonshot AI",
    "tencent": "Tencent",
    "copilot": "OpenAI",
}


def load_dataset(path):
    questions = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                questions.append(json.loads(line))
    return questions


def histogram_row(name, value, width=52):
    """One histogram row, matching the existing BENCHMARK_RESULTS.md format.

    Legend in that file is '█ = 2% of 100%', i.e. filled = round(value/2) inside a
    52-character bar (verified against every existing row).
    """
    label = (name[:23] + ":") if len(name) >= 24 else name
    label = label.ljust(24)
    filled = int(round(value / 2.0))
    filled = max(0, min(width, filled))
    return f"{label} {'█' * filled}{'░' * (width - filled)}  {value}%"


def load_external_v2(questions, user_ids, orig_ids, weighted_possible, existing=None):
    """Rebuild the leaderboard rows for the external API models that were
    re-run on the current dataset.

    A re-run that produced no answers at all is not a score: that model keeps
    its v1.0 row (and stays on the historical page). A re-run with answers
    replaces the v1.0 row, because the two are not comparable.

    Returns (entries, not_rerun) where not_rerun describes the models whose
    re-run came back empty - the free-tier catalogues rotate, so a model that
    scored on v1.0 can simply no longer be served.
    """
    entries = []
    not_rerun = []
    v1_by_model = {}
    for e in existing or []:
        if e.get("endpoint_id") is None:
            v1_by_model[(e["model"], e.get("provider"))] = e
    for path in sorted(glob.glob(os.path.join(EXTERNAL_RESULTS_DIR, "*.json"))):
        base = os.path.basename(path)
        if base == "combined.json":
            continue
        try:
            with open(path) as fh:
                data = json.load(fh)
        except Exception:
            continue
        results = data.get("results") or []
        model = data.get("model")
        provider = data.get("provider")
        if not results or not model or not provider:
            continue
        answered = sum(1 for r in results if r.get("parsed_answer") is not None)
        if answered == 0:
            old = v1_by_model.get((model, provider))
            not_rerun.append({
                "endpoint": model,
                "model": model,
                "provider": provider,
                "v1_weighted_accuracy": old.get("weighted_accuracy") if old else None,
                "reason": "provider returned no answers on the re-run "
                "(the free-tier catalogue may no longer serve this model)",
            })
            continue
        correct = sum(1 for r in results if r.get("is_correct"))
        weighted_correct = sum(
            r.get("weight", 0.0) for r in results if r.get("is_correct")
        )
        user_total = sum(1 for r in results if r.get("id") in user_ids)
        user_correct = sum(
            1 for r in results if r.get("id") in user_ids and r.get("is_correct")
        )
        orig_total = sum(1 for r in results if r.get("id") in orig_ids)
        orig_correct = sum(
            1 for r in results if r.get("id") in orig_ids and r.get("is_correct")
        )
        total = len(results)
        entries.append({
            "model": model,
            "provider": provider,
            "dataset_version": DATASET_VERSION,
            "weighted_accuracy": round(weighted_correct / weighted_possible * 100, 1),
            "overall_accuracy": round(correct / total * 100, 1) if total else 0,
            "correct": correct,
            "total": total,
            "weighted_score": round(weighted_correct, 3),
            "weighted_possible": weighted_possible,
            "user_generated_accuracy": round(user_correct / user_total * 100, 1)
            if user_total
            else 0,
            "user_generated_score": f"{user_correct}/{user_total}",
            "original_accuracy": round(orig_correct / orig_total * 100, 1)
            if orig_total
            else 0,
            "original_score": f"{orig_correct}/{orig_total}",
            "failures": sum(1 for r in results if r.get("parsed_answer") is None),
            # Same rule as the v1.0 external pipeline: a run is complete when
            # the provider answered every request. An answer that could not be
            # parsed counts as wrong, not as a missing response.
            "status": "complete" if data.get("failures", 0) == 0 and correct > 0 else (
                "partial" if correct > 0 else "failed"
            ),
        })
    return entries, not_rerun


def _external_version_label(external_v2, existing):
    """Describe which dataset versions the external rows were scored on."""
    if not external_v2:
        return "1.0"
    older = [
        e for e in existing
        if e.get("endpoint_id") is None
        and e.get("dataset_version") != DATASET_VERSION
        and e["status"] != "failed"
    ]
    if older:
        return f"{DATASET_VERSION} (partly still 1.0)"
    return DATASET_VERSION


def _version_note(external_v2, external_not_rerun, blocked, existing):
    """Explain, in the data itself, which rows can be compared with which."""
    parts = [
        "Hosten endpoints were re-run on dataset v2.0 (Q37 key corrected, "
        "Q31-Q40 distractors hardened)."
    ]
    if external_v2:
        parts.append(
            "The external API models that the provider still serves were re-run "
            "on the same v2.0 question set, so those rows are comparable."
        )
    if external_not_rerun:
        parts.append(
            f"{len(external_not_rerun)} external model(s) could not be re-run (see "
            "not_rerun_external_models); their v1.0 row is kept for continuity only."
        )
    remaining_v1 = [
        e for e in existing
        if e.get("endpoint_id") is None
        and e.get("dataset_version") != DATASET_VERSION
        and e["status"] != "failed"
    ]
    if remaining_v1:
        parts.append(
            f"{len(remaining_v1)} external row(s) are still v1.0-scored and are not "
            "directly comparable on Q31-Q40."
        )
    if blocked:
        parts.append(
            f"{len(blocked)} hosten endpoint(s) listed under "
            "not_rerun_hosten_endpoints could not be re-run because the site blocked "
            "automation; their v1.0 row is kept for continuity only."
        )
    return " ".join(parts)


def main():
    questions = load_dataset(DATASET_PATH)
    by_id = {q["id"]: q for q in questions}
    user_ids = {q["id"] for q in questions if q["id"] > 30}
    orig_ids = {q["id"] for q in questions if q["id"] <= 30}
    weighted_possible = sum(q["weight"] for q in questions)

    # Existing entries: keep everything that is NOT a hosten endpoint (those were
    # scored on dataset v1.0 and cannot be re-scored without re-running them).
    existing = []
    if os.path.exists(OUTPUT_PATH):
        try:
            with open(OUTPUT_PATH) as fh:
                existing = json.load(fh).get("leaderboard", [])
        except Exception:
            existing = []
    hosten_ids = set(MODEL_NAMES)

    # External API models re-run on the current dataset replace their v1.0 row:
    # the two were scored on different question sets and cannot be compared.
    external_v2, external_not_rerun = load_external_v2(
        questions, user_ids, orig_ids, weighted_possible, existing
    )
    if external_v2:
        replaced = {(e["model"], e.get("provider")) for e in external_v2}
        kept = []
        for e in existing:
            same = (e["model"], e.get("provider")) in replaced
            if same and e.get("endpoint_id") not in hosten_ids:
                # Keep the author label so the provider badge stays coloured.
                author = e.get("author")
                if author:
                    for new in external_v2:
                        if (new["model"], new.get("provider")) == (
                            e["model"],
                            e.get("provider"),
                        ):
                            new.setdefault("author", author)
                continue
            kept.append(e)
        existing = kept + external_v2

    # Which hosten endpoints have a v2.0 run on disk? Refuse to silently drop the
    # v1.0 rows of endpoints we could NOT re-run (site-side blocks such as
    # google's forced sign-out or copilot's Cloudflare Turnstile): they are kept
    # but tagged v1.0 so the number stays visible and comparable to nothing.
    _fname_re = re.compile(
        r"^results_(?P<model>.+?)_(?P<ts>\d{8}_\d{6})(?P<det>_detailed)?\.json$"
    )
    v2_ids = set()
    for _path in sorted(glob.glob(os.path.join(RESULTS_DIR, "results_*.json"))):
        _m = _fname_re.match(os.path.basename(_path))
        if not (_m and _m.group("det")):
            continue
        # Only a fully-answered run counts as a v2.0 re-run. A run whose rows
        # are all blank means the site itself refused (rate-limit, dead tab,
        # signed out), so the endpoint keeps its v1.0 row and stays on the
        # blocked list. Publishing it would fabricate a 0.0% score.
        try:
            _res = json.load(open(_path)).get("results") or []
        except Exception:
            continue
        if len(_res) >= len(questions) and all(
            r.get("model_response") for r in _res
        ):
            v2_ids.add(_m.group("model"))

    non_hosten = [
        e for e in existing if (e.get("endpoint_id") or e["model"]) not in hosten_ids
    ]
    carried_v1 = []
    for e in existing:
        ep = e.get("endpoint_id") or ""
        if ep in hosten_ids and ep not in v2_ids:
            e["dataset_version"] = "1.0"
            e["v1_only"] = True
            carried_v1.append(e)
    existing = non_hosten + carried_v1
    for e in existing:
        e.setdefault("dataset_version", "1.0")

    leaderboard = []
    skipped = []
    fname_re = re.compile(
        r"^results_(?P<model>.+?)_(?P<ts>\d{8}_\d{6})(?P<det>_detailed)?\.json$"
    )
    for path in sorted(glob.glob(os.path.join(RESULTS_DIR, "results_*.json"))):
        base = os.path.basename(path)
        m = fname_re.match(base)
        if not m or not m.group("det"):
            continue  # short summary or unrelated file: no per-question data
        model_id = m.group("model")
        with open(path) as fh:
            data = json.load(fh)
        results = data.get("results") or []
        if not results:
            skipped.append(f"{model_id}: no per-question results")
            continue
        # A hosten run is only publishable when every question was answered.
        # A blocked site writes 40 blank rows, which would otherwise publish a
        # false 0.0% row and displace the endpoint's v1.0 score; same rule as
        # v2_valid.py. Non-hosten files keep the permissive path.
        if model_id in hosten_ids and (
            len(results) < len(questions)
            or not all(r.get("model_response") for r in results)
        ):
            blank = sum(1 for r in results if not r.get("model_response"))
            skipped.append(
                f"{model_id}: {len(results)}/{len(questions)} questions, "
                f"{blank} blank responses - treated as not re-run"
            )
            continue
        by_res_id = {r["id"]: r for r in results}
        answered = [r for r in results if r.get("parsed_answer") is not None or r.get("model_response")]
        no_answer = sum(1 for r in results if not r.get("model_response"))
        correct = sum(1 for r in results if r.get("is_correct"))
        weighted_correct = sum(
            by_id[q_id]["weight"]
            for q_id in by_id
            if by_res_id.get(q_id, {}).get("is_correct")
        )
        user_total = sum(1 for r in results if r.get("id") in user_ids)
        user_correct = sum(
            1 for r in results if r.get("id") in user_ids and r.get("is_correct")
        )
        orig_total = sum(1 for r in results if r.get("id") in orig_ids)
        orig_correct = sum(
            1 for r in results if r.get("id") in orig_ids and r.get("is_correct")
        )
        total = len(results)
        hosten_entry = {
            "model": MODEL_NAMES.get(model_id, model_id),
            "endpoint_id": model_id,
            "provider": PROVIDER_LABEL,
            "author": AUTHORS.get(model_id, ""),
            "dataset_version": DATASET_VERSION,
            "weighted_accuracy": round(weighted_correct / weighted_possible * 100, 1),
            "overall_accuracy": round(correct / total * 100, 1) if total else 0,
            "correct": correct,
            "total": total,
            "weighted_score": round(weighted_correct, 3),
            "weighted_possible": weighted_possible,
            "user_generated_accuracy": round(user_correct / user_total * 100, 1)
            if user_total
            else 0,
            "user_generated_score": f"{user_correct}/{user_total}",
            "original_accuracy": round(orig_correct / orig_total * 100, 1)
            if orig_total
            else 0,
            "original_score": f"{orig_correct}/{orig_total}",
            "unparsed": sum(1 for r in results if r.get("parsed_answer") is None and r.get("model_response")),
            "no_answer": no_answer,
            "failures": 0,
            # A file has 40 rows no matter what: the evaluator always writes one
            # row per question, blank when the site never answered. Only a run
            # with all 40 answered counts as complete (same rule as v2_valid.py),
            # otherwise a totally failed site looks like a 0% model.
            "status": "complete"
            if total >= len(questions) and no_answer == 0
            else "partial",
            "rank": 0,
        }
        leaderboard.append(hosten_entry)

    leaderboard.extend(existing)
    leaderboard.sort(key=lambda x: (-x["weighted_accuracy"], x["model"]))
    for i, e in enumerate(leaderboard):
        e["rank"] = i + 1

    complete = [e for e in leaderboard if e["status"] == "complete"]
    hosten = [e for e in leaderboard if e.get("endpoint_id") in hosten_ids]
    # A carried-over v1.0 row is NOT a v2.0 run: the site could not be re-run, so
    # it must never drive the v2 summary (averages, best model) even though its
    # v1.0 status happens to be "complete".
    hosten_complete = [
        e for e in hosten
        if e["status"] == "complete" and not e.get("v1_only")
    ]
    external_complete = [e for e in complete if e.get("endpoint_id") not in hosten_ids]
    # Hosten endpoints whose row is v1.0 only: the site itself blocked the re-run.
    blocked = sorted(
        e["endpoint_id"]
        for e in carried_v1
        if e.get("endpoint_id")
    )
    blocked_detail = {
        e["endpoint_id"]: {
            "model": e.get("model"),
            "status": e.get("status"),
            "v1_weighted_accuracy": e.get("weighted_accuracy"),
            "v1_user_generated_score": e.get("user_generated_score"),
            "reason": BLOCKED_REASONS.get(e["endpoint_id"], "not re-run"),
        }
        for e in carried_v1
        if e.get("endpoint_id")
    }

    def _avg(entries, key):
        # A 0.0 score is data, not absence - only skip missing keys.
        vals = [e[key] for e in entries if key in e]
        return round(sum(vals) / len(vals), 1) if vals else 0

    best_hosten = (
        max(hosten_complete, key=lambda x: x["weighted_accuracy"])
        if hosten_complete
        else None
    )

    def _version_block(version, label, current=False):
        """Per-version stats. The site renders one dataset version at a time, so
        every number here has to describe exactly the rows of that version."""
        entries = [e for e in leaderboard if e.get("dataset_version") == version]
        v_complete = [e for e in entries if e["status"] == "complete"]
        v_hosten = [e for e in entries if e.get("endpoint_id") in hosten_ids]
        v_hosten_complete = [e for e in v_hosten if e["status"] == "complete"]
        v_external = [
            e for e in v_complete if e.get("endpoint_id") not in hosten_ids
        ]
        best = max(v_complete, key=lambda x: x["weighted_accuracy"], default=None)
        block = {
            "label": label,
            "models_tested": len(entries),
            "models_complete": len(v_complete),
            "models_partial": sum(1 for e in entries if e["status"] == "partial"),
            "models_failed": sum(1 for e in entries if e["status"] == "failed"),
            "hosten_models_scored": len(v_hosten_complete),
            "external_models_complete": len(v_external),
            "average_weighted_accuracy": _avg(v_complete, "weighted_accuracy"),
            "average_overall_accuracy": _avg(v_complete, "overall_accuracy"),
            "average_user_generated_accuracy": _avg(
                v_complete, "user_generated_accuracy"
            ),
            "average_original_accuracy": _avg(v_complete, "original_accuracy"),
            "best_model": best["model"] if best else "-",
            "best_weighted_accuracy": best["weighted_accuracy"] if best else 0,
        }
        if current:
            # These describe the v2.0 attempt, not the rows: how many hosten
            # endpoints were tried and how many the sites refused.
            block["hosten_endpoints_attempted"] = len(hosten)
            block["hosten_endpoints_blocked"] = len(blocked)
        return block

    summary = {
        "total_models_tested": len(leaderboard),
        "models_with_complete_results": len(complete),
        "hosten_models_complete": len(hosten_complete),
        "hosten_models_tested": len(hosten),
        "average_weighted_accuracy": _avg(hosten_complete, "weighted_accuracy"),
        "average_overall_accuracy": _avg(hosten_complete, "overall_accuracy"),
        "average_user_generated_accuracy": _avg(hosten_complete, "user_generated_accuracy"),
        "average_original_accuracy": _avg(hosten_complete, "original_accuracy"),
        "external_v1_models_complete": len(external_complete),
        "external_v1_average_weighted_accuracy": _avg(external_complete, "weighted_accuracy"),
        "external_v1_average_user_generated_accuracy": _avg(
            external_complete, "user_generated_accuracy"
        ),
        "external_v1_average_original_accuracy": _avg(
            external_complete, "original_accuracy"
        ),
        "best_model": best_hosten["model"] if best_hosten else "-",
        "best_weighted_accuracy": best_hosten["weighted_accuracy"]
        if best_hosten
        else 0,
        "hosten_endpoints_not_rerun": blocked,
        "hosten_endpoints_not_rerun_count": len(blocked),
        "dataset_version": DATASET_VERSION,
        # Explicit per-version view. The mixed-count keys above are kept for the
        # README generator; the site reads this block so the current dataset is
        # shown alone and the 1.0 rows are offered as history.
        "version_breakdown": {
            DATASET_VERSION: _version_block(
                DATASET_VERSION,
                f"Dataset {DATASET_VERSION} (current)",
                current=True,
            ),
            "1.0": _version_block("1.0", "Dataset 1.0 (historical)"),
        },
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
        "dataset_versions": {
            "hosten": DATASET_VERSION,
            "external_providers": _external_version_label(external_v2, existing),
            "not_rerun_hosten_endpoints": blocked_detail,
            "not_rerun_external_models": external_not_rerun,
            "note": _version_note(external_v2, external_not_rerun, blocked, existing),
        },
    }

    if "--check" in sys.argv:
        print(json.dumps(summary, indent=1))
        print(f"{len(leaderboard)} entries ({len(hosten_complete)} hosten/{DATASET_VERSION} "
              f"+ {len(blocked)} hosten v1.0 carried, {len(external_complete)} external"
              f"; skipped: {skipped}")
        return

    for path in (OUTPUT_PATH, DOCS_PATH):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as fh:
            json.dump(out, fh, indent=2)
    print(json.dumps(summary, indent=1))
    if skipped:
        print("SKIPPED:", skipped)
    refresh_docs(out, hosten, questions)


def refresh_docs(out, hosten, questions):
    """Rewrite the generated regions of README.md and BENCHMARK_RESULTS.md."""
    lb_full = out["leaderboard"]
    # Docs rank only scoreable runs; zero-score entries are listed under "Failed models".
    lb = [e for e in lb_full if scoreable(e)]
    s = out["summary"]
    hosten_ids = set(MODEL_NAMES)

    def row(e):
        model = e["model"]
        ep = e.get("endpoint_id")
        if ep:
            model = f"{model} (`{ep}`)"
        prov = e.get("author") or PROVIDER_DISPLAY.get(e["provider"], e["provider"])
        ver = "" if e.get("dataset_version") == DATASET_VERSION else " (v1.0)"
        status = "\u2713 Complete" if e["status"] == "complete" else "\u25d0 Partial"
        return (
            f"| {e['rank']} | {model} | {prov}{ver} | {e['correct']}/{e['total']} | "
            f"{e['overall_accuracy']}% | **{e['weighted_accuracy']}%** | "
            f"{e['user_generated_accuracy']}% | {e['original_accuracy']}% | {status} |"
        )

    header = (
        "| Rank | Model | Provider | Correct | Overall | Weighted | Q31-Q40 | Q1-Q30 | Status |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
    )
    table = header + "".join(row(e) + "\n" for e in lb)

    # ---------------------------------------------------------------- README.md
    readme = open("README.md").read()
    # 1. table rows only: keep the intro + dataset-version note paragraphs above.
    tbl_start = readme.index(header)
    tbl_end = readme.index("\n\nProviders column:", tbl_start)
    readme = readme[:tbl_start] + table + readme[tbl_end:]
    # 2. key observations bullets (the bold header line is part of the block).
    obs_start = readme.index("**Key observations:**")
    obs_end = readme.index("\n\nPer-model logs are in", obs_start)
    obs = ["**Key observations:**"]
    hosten_complete = [e for e in hosten if e["status"] == "complete" and not e.get("v1_only")]
    best = max(hosten_complete, key=lambda x: x["weighted_accuracy"]) if hosten_complete else None
    if best:
        obs.append(
            f"- **{best['model']}** (Hosten endpoint `{best['endpoint_id']}`) is the top "
            f"Hosten performer on dataset {DATASET_VERSION} "
            f"({best['overall_accuracy']}% overall, {best['weighted_accuracy']}% weighted, "
            f"{best['correct']}/{best['total']} correct)"
        )
        top3 = hosten_complete[:3]
        # External rows split by dataset version: only the ones scored on the
        # same version can be compared with the hosten rows. The rest are
        # v1.0 leftovers and are called out separately instead of being mixed
        # into a comparison they cannot support.
        external_rows = [
            e for e in lb_full
            if e.get("endpoint_id") not in hosten_ids
            and not e.get("v1_only")
            and e["status"] == "complete"
        ]
        external_same = [
            e for e in external_rows if e.get("dataset_version") == DATASET_VERSION
        ]
        external_older = [
            e for e in external_rows if e.get("dataset_version") != DATASET_VERSION
        ]
        best_external_same = max(
            external_same, key=lambda x: x["weighted_accuracy"], default=None
        )
        ext_best = (
            best_external_same["weighted_accuracy"] if best_external_same else None
        )
        # The top-3 claim must hold for EVERY one of those rows, not just the
        # leader: comparing a single 3-endpoint list against the best external
        # row hides that the other two sit far below it.
        top3_lead = ext_best is None or all(
            e["weighted_accuracy"] > ext_best for e in top3
        )
        if len(top3) >= 3 and top3_lead and best_external_same:
            obs.append(
                "- The top 3 weighted hosten endpoints are "
                + ", ".join(f"`{e['endpoint_id']}`" for e in top3)
                + f" - all ahead of every external API model scored on dataset "
                f"{DATASET_VERSION} (best of them: "
                f"`{best_external_same['model']}`, {ext_best}%)"
            )
        elif ext_best is None:
            obs.append(
                f"- {len(hosten_complete)} hosten endpoint(s) scored so far on dataset "
                f"{DATASET_VERSION}: "
                + ", ".join(
                    f"`{e['endpoint_id']}` ({e['weighted_accuracy']}% weighted)"
                    for e in hosten_complete
                )
                + ("; external rows are v1.0-scored and not directly comparable"
                   if external_older else "")
            )
        elif best["weighted_accuracy"] > ext_best:
            # The leader is ahead of every external row but the rest of the top 3
            # are not: say exactly that instead of claiming all three lead.
            not_ahead = [e for e in top3 if e["weighted_accuracy"] <= ext_best]
            obs.append(
                f"- `{best['endpoint_id']}` ({best['weighted_accuracy']}% weighted) is ahead "
                f"of the best external API row scored on the same dataset "
                f"(`{best_external_same['model']}`, "
                f"{ext_best}%), but the other top-3 hosten rows ("
                + ", ".join(
                    f"`{e['endpoint_id']}` {e['weighted_accuracy']}%" for e in not_ahead
                )
                + ") are not"
            )
        else:
            obs.append(
                f"- The best dataset {DATASET_VERSION} hosten row (`{best['endpoint_id']}`, "
                f"{best['weighted_accuracy']}% weighted) is below the best external API row "
                f"scored on the same dataset (`{best_external_same['model']}`, "
                f"{ext_best}% weighted)"
            )
        if external_older:
            obs.append(
                f"- {len(external_older)} external API row(s) are still v1.0-scored "
                "(their provider could not be re-run on the current dataset); they are "
                "not directly comparable and are kept on the historical results page"
            )
    obs.append(
        f"- Q1-Q30 accuracy is consistently higher than Q31-Q40 across hosten models "
        f"(mean {s['average_original_accuracy']}% vs {s['average_user_generated_accuracy']}%) "
        f"on dataset {DATASET_VERSION}"
    )
    if len(hosten_complete) >= 2:
        weak = min(hosten_complete, key=lambda x: x["weighted_accuracy"])
        obs.append(
            f"- The same gateway spans the whole range: the best model hosts alongside "
            f"`{weak['endpoint_id']}` ({weak['model']}, {weak['weighted_accuracy']}% weighted), "
            f"the weakest complete endpoint"
        )
    readme = readme[:obs_start] + "\n".join(obs) + readme[obs_end:]
    open("README.md", "w").write(readme)

    # ------------------------------------------------------ BENCHMARK_RESULTS.md
    brd = open("BENCHMARK_RESULTS.md").read()

    def replace_between(text, start_marker, end_marker, payload):
        i = text.index(start_marker)
        j = text.index(end_marker, i)
        return text[:i] + payload + text[j:]

    best_overall = max(lb, key=lambda x: x["overall_accuracy"])
    summary_rows = (
        "| Metric | Value |\n|--------|-------|\n"
        f"| Total models tested | {s['total_models_tested']} "
        f"({s['hosten_models_complete']} hosten on dataset {DATASET_VERSION}, "
        f"{s['external_v1_models_complete']} external on v1.0) |\n"
        f"| Hosten endpoints complete (dataset {DATASET_VERSION}) | "
        f"{s['hosten_models_complete']}/{s['hosten_models_tested']} |\n"
        f"| Hosten average weighted accuracy | **{s['average_weighted_accuracy']}%** |\n"
        f"| Hosten average overall accuracy | {s['average_overall_accuracy']}% |\n"
        f"| Hosten average on user-generated questions (Q31-Q40) | "
        f"{s['average_user_generated_accuracy']}% |\n"
        f"| Hosten average on original questions (Q1-Q30) | "
        f"{s['average_original_accuracy']}% |\n"
        f"| External providers average weighted accuracy (dataset v1.0) | "
        f"{s['external_v1_average_weighted_accuracy']}% |\n"
        f"| External providers average user-gen / original (v1.0) | "
        f"{s['external_v1_average_user_generated_accuracy']}% / "
        f"{s['external_v1_average_original_accuracy']}% |\n"
        f"| Best hosten weighted score (dataset {DATASET_VERSION}) | "
        f"{best['model']} ({best['weighted_accuracy']}%) |\n"
        f"| Best overall accuracy (any provider) | {best_overall['model']} "
        f"({best_overall['overall_accuracy']}%) |\n"
        f"| Hosten endpoints NOT re-run on v2.0 | {s['hosten_endpoints_not_rerun_count']} "
        + (f"({', '.join(s['hosten_endpoints_not_rerun'])}) - "
           if s['hosten_endpoints_not_rerun'] else "")
        + "blocked by the site, see Providers Tested |\n"
    )
    brd = replace_between(brd, "| Metric | Value |", "\n\n**Weighting:**", summary_rows)

    # Leaderboard table + its trailing note paragraph.
    lb_start = brd.index(header)
    note_end = brd.index("\n\n## Accuracy Histogram", lb_start)
    incomplete = sum(1 for e in lb if e["status"] != "complete")
    note = (
        "\n"
        f"*Rows for hosten endpoints are dataset {DATASET_VERSION} re-runs. Rows tagged (v1.0) "
        "were scored on dataset v1.0 and are shown for continuity only, not direct comparison "
        "on Q31-Q40; that includes the external providers (KiloCode / Google AI Studio / NVIDIA "
        "NIM) and any hosten endpoint the site itself blocked from being re-run"
        + (f" ({', '.join(s['hosten_endpoints_not_rerun'])})"
           if s['hosten_endpoints_not_rerun'] else "")
        + f". {incomplete} entr{'y is' if incomplete == 1 else 'ies are'} not fully complete; "
        "access-path details are in Providers Tested below.*"
    )
    brd = brd[:lb_start] + table + note + brd[note_end:]

    # Histogram.
    hist = "".join(
        histogram_row(e["model"], e["weighted_accuracy"]) + "\n" for e in lb
    )
    axis = (
        "\n                         0%  10% 20% 30% 40% 50% 60% 70% 80% 90% 100%\n"
        "                           \u251c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\u253c\n"
    )
    fence_start = brd.index("```\n", brd.index("## Accuracy Histogram"))
    fence_end = brd.index("```", fence_start + 4)
    brd = (
        brd[:fence_start] + "```\n" + hist + axis + "```" + brd[fence_end + 3 :]
    )

    # Hosten endpoint table.
    hosten_table = (
        "| Endpoint ID | Underlying Model | Author |\n"
        "|-------------|------------------|--------|\n"
        + "".join(
            f"| `{e['endpoint_id']}` | {e['model']} | {e.get('author', '')} |\n"
            for e in sorted(hosten, key=lambda x: MODEL_NAMES.get(x["endpoint_id"], ""))
        )
    )
    brd = replace_between(
        brd,
        "| Endpoint ID | Underlying Model | Author |",
        "\n\nPer-question answers",
        hosten_table,
    )
    brd = brd.replace(
        "Per-question answers are in `results/hosten/recovered_answers.jsonl`;",
        "Per-question answers are in `results/hosten_v2/results_<endpoint>_<timestamp>_detailed.json` "
        "(dataset v2.0); the v1.0 extraction remains in `results/hosten/recovered_answers.jsonl`.",
    )

    # ---------------------------------------------------- NOT RE-RUN SECTION
    # This prose and its table are hand-written outside the generated regions
    # above, so they drifted out of sync (they once said "Seven of the ten" and
    # still listed the now-fixed `zai` extractor problem as a block). Derive
    # them from `blocked`/`blocked_detail` so they track the real run set.
    blocked = list(s["hosten_endpoints_not_rerun"])
    blocked_detail = out["dataset_versions"]["not_rerun_hosten_endpoints"]
    if blocked:
        det_rows = [
            (b, blocked_detail.get(b, {}))
            for b in blocked
            if blocked_detail.get(b)
        ]
        not_rerun_body = (
            f"{len(det_rows)} of the {len(hosten)} Hosten endpoints could not be re-run: "
            "the sites blocked automated access. Their v1.0 rows are retained in the "
            "leaderboard (marked **(v1.0)** and `v1_only`) for continuity only and must "
            "not be read as v2.0 performance.\n\n"
            "| Endpoint | Model | Why not re-run |\n"
            "|----------|-------|----------------|\n"
            + "\n".join(
                f"| `{b}` | {det.get('model', '?')} | {det.get('reason', '')} |"
                for b, det in det_rows
            )
        )
    else:
        not_rerun_body = (
            f"All {len(hosten)} Hosten endpoints were re-run on dataset "
            f"{DATASET_VERSION}, so no v1.0 rows are carried forward."
        )
    brd = replace_between(
        brd,
        "### Endpoints NOT re-run on dataset v2.0",
        "## Providers Tested",
        "### Endpoints NOT re-run on dataset v2.0\n\n" + not_rerun_body + "\n\n",
    )

    # ------------------------------------------------------- PROVIDERS TESTED
    # Same drift problem for the Hosten Gateway bullet ("3 complete ... 7
    # blocked" was stale). Rebuild it from the run set.
    complete_hosten = list(hosten_complete)
    authors = len({e.get("author", "") for e in hosten if e.get("author")})
    hosten_bullet = (
        "- **Hosten Gateway** (`http://localhost:8079/v1`) - access path for "
        f"{len(hosten)} endpoint IDs from {authors} different model authors; "
        f"**{len(complete_hosten)} complete on dataset {DATASET_VERSION}** "
        f"({', '.join(sorted(e['endpoint_id'] for e in complete_hosten))})"
        + (f", {len(blocked)} blocked by the sites (see table above)"
           if blocked else ", none blocked")
    )
    brd = replace_between(
        brd,
        "- **Hosten Gateway**",
        "- **KiloCode API**",
        hosten_bullet + "\n",
    )

    open("BENCHMARK_RESULTS.md", "w").write(brd)
    print("docs refreshed: README.md, BENCHMARK_RESULTS.md")


if __name__ == "__main__":
    main()
