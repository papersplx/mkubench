# Benchmark Results

## Summary

| Metric | Value |
|--------|-------|
| Total models tested | 39 (12 scored on dataset 2.0, 27 recorded on dataset 1.0) |
| Hosten endpoints complete (dataset 2.0) | 4/10 |
| Hosten average weighted accuracy | **37.7%** |
| Hosten average overall accuracy | 71.9% |
| Hosten average on user-generated questions (Q31-Q40) | 22.5% |
| Hosten average on original questions (Q1-Q30) | 88.3% |
| External providers average weighted accuracy (dataset 2.0) | 24.9% |
| External providers average user-gen / original (dataset 2.0) | 11.2% / 70.4% |
| External providers average weighted accuracy (dataset v1.0) | 48.5% |
| External providers average user-gen / original (v1.0) | 42.2% / 69.3% |
| Best hosten weighted score (dataset 2.0) | glm-5.3-flash (66.9%) |
| Best overall accuracy (any provider) | mistral-medium-3.5 (87.5%) |
| Hosten endpoints NOT re-run on v2.0 | 6 (copilot, google, grok, kimi, mistral, tencent) - blocked by the site, see Providers Tested |


**Weighting:** User-added questions (Q31-Q40) have weight **1.0**, original questions (Q1-Q30) have weight **0.1**. Total weighted possible: 13.0 points (10.0 from user-generated + 3.0 from original).

## Leaderboard

| Rank | Model | Provider | Correct | Overall | Weighted | Q31-Q40 | Q1-Q30 | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | mistral-medium-3.5 (`mistral`) | Mistral AI (v1.0) | 35/40 | 87.5% | **89.2%** | 90.0% | 86.7% | ✓ Complete |
| 2 | hy4-preview (`tencent`) | Tencent (v1.0) | 31/40 | 77.5% | **72.3%** | 70.0% | 80.0% | ✓ Complete |
| 3 | glm-5.3-flash (`zai`) | Z.ai | 33/40 | 82.5% | **66.9%** | 60.0% | 90.0% | ✓ Complete |
| 4 | inclusionai/ling-3.0-flash-vl:free | KiloCode API (v1.0) | 27/40 | 67.5% | **62.3%** | 60.0% | 70.0% | ✓ Complete |
| 5 | grok-4.5 (`grok`) | xAI (v1.0) | 30/40 | 75.0% | **57.7%** | 50.0% | 83.3% | ✓ Complete |
| 6 | stepfun/step-3.7-flash:free | KiloCode API (v1.0) | 28/40 | 70.0% | **56.2%** | 50.0% | 76.7% | ✓ Complete |
| 7 | inclusionai/ling-3.0-flash-fin:free | KiloCode API (v1.0) | 25/40 | 62.5% | **53.8%** | 50.0% | 66.7% | ✓ Complete |
| 8 | gpt-5.6 (`copilot`) | OpenAI (v1.0) | 28/40 | 70.0% | **49.2%** | 40.0% | 80.0% | ✓ Complete |
| 9 | nex-agi/nex-n2.5-mini:free | KiloCode API (v1.0) | 27/40 | 67.5% | **48.5%** | 40.0% | 76.7% | ✓ Complete |
| 10 | inclusionai/ling-3.0-flash-sante:free | KiloCode API (v1.0) | 26/40 | 65.0% | **47.7%** | 40.0% | 73.3% | ✓ Complete |
| 11 | meta/muse-glimmer-30b | NVIDIA NIM (v1.0) | 25/40 | 62.5% | **46.9%** | 40.0% | 70.0% | ✓ Complete |
| 12 | kimi-k3 (`kimi`) | Moonshot AI (v1.0) | 29/40 | 72.5% | **43.1%** | 30.0% | 86.7% | ✓ Complete |
| 13 | liquid/lfm-2.5-2.6b:free | KiloCode API (v1.0) | 19/40 | 47.5% | **42.3%** | 40.0% | 50.0% | ✓ Complete |
| 14 | nex-agi/nex-n2.5-pro:free | KiloCode API (v1.0) | 25/40 | 62.5% | **40.0%** | 30.0% | 73.3% | ✓ Complete |
| 15 | nvidia/nemotron-3-super-120b-a12b | NVIDIA NIM (v1.0) | 23/40 | 57.5% | **38.5%** | 30.0% | 66.7% | ✓ Complete |
| 16 | qwen-3.8-max (`qwen`) | Alibaba | 27/40 | 67.5% | **34.6%** | 20.0% | 83.3% | ✓ Complete |
| 17 | poolside/laguna-s-2.1:free | KiloCode API | 21/40 | 52.5% | **30.0%** | 20.0% | 63.3% | ✓ Complete |
| 18 | muse-spark-1.1 (`meta`) | Meta | 28/40 | 70.0% | **28.5%** | 10.0% | 90.0% | ✓ Complete |
| 19 | nvidia/nemotron-3-ultra-550b-a55b:free | KiloCode API | 27/40 | 67.5% | **27.7%** | 10.0% | 86.7% | ✓ Complete |
| 20 | gemini-3.8-flash (`google`) | Google (v1.0) | 25/40 | 62.5% | **26.2%** | 10.0% | 80.0% | ✓ Complete |
| 21 | gemini-3.5-flash-lite | Google AI Studio | 24/40 | 60.0% | **25.4%** | 10.0% | 76.7% | ✓ Complete |
| 22 | nvidia/nemotron-3.5-super-vl:free | KiloCode API | 24/40 | 60.0% | **25.4%** | 10.0% | 76.7% | ✓ Complete |
| 23 | minimax/minimax-m3.1-flash:free | KiloCode API | 22/40 | 55.0% | **23.8%** | 10.0% | 70.0% | ✓ Complete |
| 24 | cohere/north-mini-code:free | KiloCode API | 21/40 | 52.5% | **23.1%** | 10.0% | 66.7% | ✓ Complete |
| 25 | nvidia/nemotron-3.5-lightning:free | KiloCode API | 20/40 | 50.0% | **22.3%** | 10.0% | 63.3% | ✓ Complete |
| 26 | dots-studio/dots-3-note-preview:free | KiloCode API | 19/40 | 47.5% | **21.5%** | 10.0% | 60.0% | ✓ Complete |
| 27 | claude-sonnet-5 (`claude`) | Anthropic | 27/40 | 67.5% | **20.8%** | 0.0% | 90.0% | ✓ Complete |
| 28 | deepseek-ai/deepseek-v4-flash-0731 | NVIDIA NIM (v1.0) | 21/40 | 52.5% | **16.2%** | 0.0% | 70.0% | ◐ Partial |

*Rows for hosten endpoints are dataset 2.0 re-runs. Rows tagged (v1.0) were scored on dataset v1.0 and are shown for continuity only, not direct comparison on Q31-Q40; that includes the external providers (KiloCode / Google AI Studio / NVIDIA NIM) and any hosten endpoint the site itself blocked from being re-run (copilot, google, grok, kimi, mistral, tencent). 1 entry is not fully complete; access-path details are in Providers Tested below.*

## Accuracy Histogram (Weighted)

```
mistral-medium-3.5       █████████████████████████████████████████████░░░░░░░  89.2%
hy4-preview              ████████████████████████████████████░░░░░░░░░░░░░░░░  72.3%
glm-5.3-flash            █████████████████████████████████░░░░░░░░░░░░░░░░░░░  66.9%
inclusionai/ling-3.0-fl: ███████████████████████████████░░░░░░░░░░░░░░░░░░░░░  62.3%
grok-4.5                 █████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░  57.7%
stepfun/step-3.7-flash:: ████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░  56.2%
inclusionai/ling-3.0-fl: ███████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░  53.8%
gpt-5.6                  █████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░  49.2%
nex-agi/nex-n2.5-mini:f: ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  48.5%
inclusionai/ling-3.0-fl: ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  47.7%
meta/muse-glimmer-30b    ███████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  46.9%
kimi-k3                  ██████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  43.1%
liquid/lfm-2.5-2.6b:fre: █████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  42.3%
nex-agi/nex-n2.5-pro:fr: ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  40.0%
nvidia/nemotron-3-super: ███████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  38.5%
qwen-3.8-max             █████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  34.6%
poolside/laguna-s-2.1:f: ███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  30.0%
muse-spark-1.1           ██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  28.5%
nvidia/nemotron-3-ultra: ██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  27.7%
gemini-3.8-flash         █████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  26.2%
gemini-3.5-flash-lite    █████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  25.4%
nvidia/nemotron-3.5-sup: █████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  25.4%
minimax/minimax-m3.1-fl: ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  23.8%
cohere/north-mini-code:: ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  23.1%
nvidia/nemotron-3.5-lig: ███████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  22.3%
dots-studio/dots-3-note: ███████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  21.5%
claude-sonnet-5          ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  20.8%
deepseek-ai/deepseek-v4: ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  16.2%

                         0%  10% 20% 30% 40% 50% 60% 70% 80% 90% 100%
                           ├┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
```

Legend: █ = 2% of 100%

## Performance by Access Path

Every model with a usable answer is already ranked in the single leaderboard above, so per-access-path score tables would just duplicate it. Instead:

- **Hosten gateway** (`http://localhost:8079/v1`) - 10 endpoint IDs tested, 10 complete, from 10 different model authors (Anthropic, Mistral AI, Z.ai, Meta, Alibaba, xAI, Google, Moonshot AI, Tencent, OpenAI - see the Provider column)
- **KiloCode API** - 11 tested, 11 complete
- **Google AI Studio** - 3 tested, 1 complete
- **NVIDIA NIM** - 12 tested, 3 complete

### Failed models

Excluded from the leaderboard; kept here for reproducibility of the gaps.

| Model | Provider | Reason |
|---|---|---|
| cohere/north-mini-code:free | KiloCode API | Legacy summary-only result (no per-question data; old 25.0-point weighting) - not re-scoreable on the current dataset |
| deepseek-ai/deepseek-coder-6.7b-instruct | NVIDIA NIM | Model not found (404) |
| deepseek-ai/deepseek-v4-pro-0813 | NVIDIA NIM | API timeouts |
| google/gemma-4-31b-it | NVIDIA NIM | API timeouts |
| google/gemma-4-31b-it | Google AI Studio | Not available (404) |
| ibm/granite-3.0-3b-a800m-instruct | NVIDIA NIM | Model not found (404) |
| ibm/granite-3.0-8b-instruct | NVIDIA NIM | Model not found (404) |
| meta/llama2-70b | NVIDIA NIM | Model not found (404) |
| minimaxai/minimax-m3 | NVIDIA NIM | Model deprecated (410) |
| moonshotai/kimi-k2.6 | NVIDIA NIM | Model not found (404) |
| moonshotai/kimi-k3 | NVIDIA NIM | Rate limited (429) |
| gemini-3.8-flash | Google AI Studio | Rate limited (429) — separately complete as the `google` Hosten endpoint |

## Key Findings

- **Dataset v2.0 hardening largely held, with one clear exception.** The four re-run Hosten endpoints average **22.5%** (9 of 40 question-instances) on the rewritten Q31-Q40, against the **42.1%** external providers averaged on those same questions under v1.0. `zai` is the exception at **6/10** (Q31, Q32, Q34, Q35, Q39, Q40) - the style-matched distractors are not uniformly defeating detection.
- **Q1-Q30 accuracy held up**: the four v2.0 Hosten endpoints average **88.3%** on the original set (106/120), so the drop is specific to the user-generated block rather than a general model failure.
- **4 of 10 Hosten endpoints could be re-run on v2.0.** `zai` (66.9% weighted, 6/10 on Q31-Q40), `qwen` (34.6%, 2/10), `meta` (28.5%, 1/10) and `claude` (20.8%, 0/10) completed; the other 6 were blocked by the sites (see Hosten Gateway Results below).
- **`zai` needed a tooling fix before it could be scored at all.** The gateway's `zai` response extractor matched the user's own message bubble, so every captured "answer" was the question text and the endpoint looked unusable. Scoping extraction to the newest assistant turn reveals its real v2.0 result: **66.9% weighted**, now the strongest Hosten row on v2.0 and above the best v1.0 external API row (`inclusionai/ling-3.0-flash-vl:free`, 62.3%). The two are scored on different dataset versions and are not directly comparable.
- **The Hosten rows marked (v1.0) are v1.0 scores.** They are the wrong reference for Q31-Q40: distractors, the Q37 key and therefore question difficulty have all changed, and they are kept for continuity only.

## Hosten Gateway Results

The Hosten gateway (`http://localhost:8079/v1`) exposes 10 endpoint IDs, each routing to an underlying model, all scored on the same fixed 40-question dataset and ranked together with the external API models in the leaderboard above (where the Provider column shows the model author):

| Endpoint ID | Underlying Model | Author |
|-------------|------------------|--------|
| `claude` | claude-sonnet-5 | Anthropic |
| `google` | gemini-3.8-flash | Google |
| `zai` | glm-5.3-flash | Z.ai |
| `copilot` | gpt-5.6 | OpenAI |
| `grok` | grok-4.5 | xAI |
| `tencent` | hy4-preview | Tencent |
| `kimi` | kimi-k3 | Moonshot AI |
| `mistral` | mistral-medium-3.5 | Mistral AI |
| `meta` | muse-spark-1.1 | Meta |
| `qwen` | qwen-3.8-max | Alibaba |


Per-question answers are in `results/hosten_v2/results_<endpoint>_<timestamp>_detailed.json` (dataset v2.0); the v1.0 extraction remains in `results/hosten/recovered_answers.jsonl`. Per-model request logs are in `results/hosten/{endpoint_id}.log`.

### Endpoints NOT re-run on dataset v2.0

6 of the 10 Hosten endpoints could not be re-run: the sites blocked automated access. Their v1.0 rows are retained in the leaderboard (marked **(v1.0)** and `v1_only`) for continuity only and must not be read as v2.0 performance.

| Endpoint | Model | Why not re-run |
|----------|-------|----------------|
| `copilot` | gpt-5.6 | Cloudflare Turnstile 'Verification required' modal re-arms on every submit; requires a human solve |
| `google` | gemini-3.8-flash | site signed the account out; requires an interactive Google login in the Chromium window (automation not possible) |
| `grok` | grok-4.5 | single-tab run started after the 'under heavy usage' rate-limit window cleared (~17:51 2026-10-19) but Q1 read timed out at 2400s with zero response (same session/login-gated wedge as mistral/tencent), so no complete 40-question run could be produced |
| `kimi` | kimi-k3 | site rate-limited ('too many people are chatting'); throttling window |
| `mistral` | mistral-medium-3.5 | single-tab run started after the account message-limit window cleared (~16:30 2026-10-19) but Q1 never completed (fresh tab cannot answer chat completions; session/login-gated), so no complete 40-question run could be produced |
| `tencent` | hy4-preview | site answers only after a long deep-thinking pass; the tab wedges mid-run (Q2 stalled >15 min after Q1 took ~4 min), so no complete 40-question run could be produced |

## Providers Tested

- **Hosten Gateway** (`http://localhost:8079/v1`) - access path for 10 endpoint IDs from 10 different model authors; **4 complete on dataset 2.0** (claude, meta, qwen, zai), 6 blocked by the sites (see table above)
- **KiloCode API** (`https://api.kilo.ai/api/gateway/v1`) - 11 models from various providers (NVIDIA, StepFun, Poolside, InclusionAI, NexAGI, Liquid, Dots Studio), all complete
- **Google AI Studio** (`https://generativelanguage.googleapis.com/v1beta/openai/chat/completions`) - 3 tested, 1 complete, 2 unavailable
- **NVIDIA NIM / NGC** (`https://integrate.api.nvidia.com/v1`) - 12 tested, 3 complete, 9 unavailable or timed out

## How to Run

```bash
# Run against KiloCode (supports many models)
python run_all_models_benchmark.py

# Run remaining NVIDIA models (resumable)
python run_nvidia_remaining.py

# Run Google AI Studio models
python run_google_benchmark.py

# Run against Google AI Studio (OpenAI-compatible)
python run_benchmark.py --client openai --model gemini-3.5-flash-lite --api-key $GEMINI_API_KEY --api-base https://generativelanguage.googleapis.com/v1beta/openai

# Run against NVIDIA API
python run_benchmark.py --client openai --model nvidia/nemotron-3-super-120b-a12b --api-key $NVIDIA_API_KEY --api-base https://integrate.api.nvidia.com/v1

# Run against Gemini native API
python run_benchmark.py --client gemini --model gemini-2.5-flash --api-key $GEMINI_API_KEY

# Run against local Ollama
python run_benchmark.py --client ollama --model llama3
```

## Contributing

If you run this benchmark against additional models, please submit a PR with your results. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.