#!/usr/bin/env python3
"""Inject a real dataset prompt into a tab and submit it, mimicking the gateway."""
import json
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, "/home/fra/dev/sbsllm")
from sbsllm.inject import inject_prompt, submit_js  # noqa: E402

model = sys.argv[1]
qid = int(sys.argv[2]) if len(sys.argv) > 2 else 1
DS = "/var/home/fra/dev/mkubench/dataset/mkultra_benchmark.jsonl"

qs = {}
with open(DS) as fh:
    for line in fh:
        if line.strip():
            q = json.loads(line)
            qs[q["id"]] = q

q = qs[qid]
options_text = "\n".join(q["options"])
prompt = f"""{q['question']}

{options_text}

Please reason step by step, then provide your final answer in the format:
"Answer: X" where X is the correct option letter(s).

For multiple-select questions, list all correct letters (e.g., "Answer: A,B,D").

Question Type: {q['question_type']}"""


def run(js, timeout=60):
    url = f"http://localhost:8079/debug/js?model={model}&js={urllib.parse.quote(js)}"
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read().decode()


t0 = time.time()
inj = run(inject_prompt(model, prompt))
print(f"inject ({time.time()-t0:.2f}s):", inj[:160])
time.sleep(0.3)
t1 = time.time()
sub = run(submit_js(model))
print(f"submit ({time.time()-t1:.2f}s):", sub[:160])
print(f"prompt length: {len(prompt)} chars")
