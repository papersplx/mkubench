# MK Ultra Benchmark Run Report — `multi`

## Overview
**Benchmark Model:** `multi`
**Dataset:** `dataset/mkultra_benchmark.jsonl`
**Gateway Endpoint:** `http://localhost:8079/v1`
**Run Date:** 2026-10-21
**Timeline:** Started 08:36:51, benchmark table printed 08:47:22, run halted at 08:47:22.

## 1. Safety & Launch (STEP 1 — 2)
- **Initial Check:** 08:36:30 → No other wrapper processes found (`NO_WRAPPER_RUNNING`).
- **Launch Command:** `scripts/hosten/run_one_v2.sh multi`
- **Verification:** `run_one_multi.log` successfully spawned with fresh mtime at **08:36:51** showing:
  - `Loaded 40 questions from dataset/mkultra_benchmark.jsonl`
  - `Evaluating Q1: Supersecret ORD Program...`
- **Active Processes (ruling out fork-exhaustion failures):**
  - `bash scripts/hosten/run_one_v2.sh multi`
  - `python run_benchmark.py --client openai --model multi --api-base http://localhost:8079/v1 --api-key dummy --output results/hosten_v2 --timeout 2400 --max-retries 1`

## 2. Execution Progress (STEP 3 Monitoring)
The wrapper marched steadily through the benchmark from Q1 to Q40, with one `[ERROR]` / `[WARNING]` event per question. Evaluation progressed from Q1 to Q40 at roughly 15-second intervals, completing all 40 questions in ~10.5 minutes.

- **Errors:** 40 total errors, 1 per question (all Q1-Q40).
- **Nature of errors:** `502 Server Error: Bad Gateway` on endpoint `http://localhost:8079/v1/chat/completions`.

## 3. Terminal Signal & Exit
The run produced a `BENCHMARK RESULTS` table but the wrapper marked its exit as:
```
08:47:22 EXIT multi rc=0 without completion
```
**Analysis:** `run_benchmark.py` did reach its final reporting stage and printed the full results table for all 40 questions. However, the wrapper (`run_one_v2.sh`) exited without the expected internal completion marker. The process history and result file confirm that all 40 questions were evaluated and a detailed result file was written (see below). `rc=0` indicates the Python process itself exited normally.

## 4. Data Collection (STEP 4)

### 4.1 Validation (`v2_valid.py`)
```
multi: INCOMPLETE results_multi_20261021_084653_detailed.json: 40/40 questions, 40 empty responses
multi: INCOMPLETE (no valid run found)
valid_exit=1
```

### 4.2 Result Artifact
- **Path:** `results/hosten_v2/results_multi_20261021_084653_detailed.json`
- **Modified:** 2026-10-21 08:46:53.418784007 +0200
- **Total Results:** 40
- **Blank/Empty Responses:** 40
- **Correct:** 0

### 4.3 Summary Block (from `run_one_multi.log`)
```
BENCHMARK RESULTS
======================================================================
Total Questions:    40
Correct:            0
Incorrect:          40
Overall Accuracy:   0.0%
Weighted Accuracy:  0.0% (0.0/13.0)
Single Choice:      0.0% (0/30)
Multiple Choice:    0.0% (0/10)
```

## 5. Detailed Error Log
Total error count: 40 (one per question).

Two representative verbatim error lines:
```
2026-10-21 08:37:06 [ERROR] Error on Q1: 502 Server Error: Bad Gateway for url: http://localhost:8079/v1/chat/completions
2026-10-21 08:46:53 [ERROR] Error on Q40: 502 Server Error: Bad Gateway for url: http://localhost:8079/v1/chat/completions
```
All 40 error lines follow the identical pattern for Q1 through Q40 (`502 Server Error: Bad Gateway for url: http://localhost:8079/v1/chat/completions`).

## 6. Final Log Lines
```
  ✗ Q35: First Symptoms of Targeting                        | Ans: None | Correct: A
  ✗ Q36: Synchronicities Around Targeted Individuals        | Ans: None | Correct: C
  ✗ Q37: Thought Broadcasting as Reported by TIs            | Ans: None | Correct: C
  ✗ Q38: Mimicry as Mentioned by Targeted Individuals       | Ans: None | Correct: A
  ✗ Q39: Why the TI Program Struggles to Be Uncovered       | Ans: None | Correct: D
  ✗ Q40: Schizophrenia's Foothold in Addressing TI Testimon | Ans: None | Correct: A, B, D
----------------------------------------------------------------------
08:47:22 EXIT multi rc=0 without completion
```

## 7. Conclusion
The `multi` model completed a full benchmark traversal of all 40 questions. However, the gateway rejected **100%** of requests with `502 Bad Gateway` errors, yielding 40 empty responses and **0.0% overall accuracy**.

As anticipated in the environment facts, `multi` is not registered as a functional model on the gateway. This produced a clean, honest baseline result: **40/40 blank responses**, recorded in the results directory.
