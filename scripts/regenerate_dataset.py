#!/usr/bin/env python3
"""Regenerate the JSONL/JSON dataset from the markdown source."""

# Copyright (c) 2026 defnlnotme
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import json
import os
import re


def regenerate() -> None:
    """Regenerate the dataset from the markdown source file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    md_path = os.path.join(base_dir, 'dataset', 'mkultra-benchmark.md')
    with open(md_path, 'r') as f:
        content = f.read()
    blocks = content.split('---')
    questions = []
    for block in blocks:
        block = block.strip()
        if not block or 'Question' not in block:
            continue
        hm = re.match(r'### Question (\d+):\s*(.+)', block)
        if not hm:
            continue
        q_num = int(hm.group(1))
        q_title = hm.group(2).strip()
        tm = re.search(r'\*\*Question Type:\*\*\s*(.+)', block)
        q_type = tm.group(1).strip() if tm else "Single Choice"
        qm = re.search(r'\*\*Question:\*\*\s*(.+?)(?=\n\s*- [A-D]\))', block, re.DOTALL)
        q_text = qm.group(1).strip() if qm else ""
        options = []
        for om in re.finditer(r'-\s*([A-D])\)\s*(.+)', block):
            options.append({"letter": om.group(1), "text": om.group(2).strip()})
        am = re.search(r'\*\*Correct Answer:\*\*\s*(.+)', block)
        correct_answer = am.group(1).strip() if am else ""
        cm = re.search(r'\*\*Citations:\*\*\s*(.+)', block)
        citations = cm.group(1).strip() if cm else ""
        em = re.search(r'\*\*Explanation:\*\*\s*(.+)', block, re.DOTALL)
        explanation = em.group(1).strip() if em else ""
        is_multiple = "Multiple Choice" in q_type or "Select ALL" in q_text
        options_formatted = [f"{opt['letter']}) {opt['text']}" for opt in options]
        questions.append({
            "id": q_num, "category": "mkultra", "title": q_title,
            "question": q_text, "options": options_formatted, "options_raw": options,
            "correct_answer": correct_answer, "is_multiple_choice": is_multiple,
            "citations": citations, "explanation": explanation, "question_type": q_type
        })
    os.makedirs(os.path.join(base_dir, 'dataset'), exist_ok=True)
    with open(os.path.join(base_dir, 'dataset', 'mkultra_benchmark.jsonl'), 'w') as f:
        for q in questions:
            f.write(json.dumps(q) + '\n')
    with open(os.path.join(base_dir, 'dataset', 'mkultra_benchmark.json'), 'w') as f:
        json.dump(questions, f, indent=2)
    print(f"Dataset regenerated: {len(questions)} questions")


def main() -> None:
    """Regenerate the benchmark dataset."""
    regenerate()


if __name__ == "__main__":
    main()
