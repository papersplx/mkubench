#!/usr/bin/env python3
"""Regenerate the JSONL/JSON dataset from the markdown source."""
import re, json, os

def regenerate():
    md_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mkultra-continuation-benchmark.md')
    with open(md_path, 'r') as f:
        content = f.read()
    blocks = content.split('---')
    questions = []
    for block in blocks:
        block = block.strip()
        if not block or 'Question' not in block: continue
        hm = re.match(r'### Question (\d+):\s*(.+)', block)
        if not hm: continue
        q_num = int(hm.group(1)); q_title = hm.group(2).strip()
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
            "id": q_num, "category": "mkultra_continuation", "title": q_title,
            "question": q_text, "options": options_formatted, "options_raw": options,
            "correct_answer": correct_answer, "is_multiple_choice": is_multiple,
            "citations": citations, "explanation": explanation, "question_type": q_type
        })
    os.makedirs('dataset', exist_ok=True)
    with open('dataset/mkultra_benchmark.jsonl', 'w') as f:
        for q in questions: f.write(json.dumps(q) + '\n')
    with open('dataset/mkultra_benchmark.json', 'w') as f:
        json.dump(questions, f, indent=2)
    print(f"Dataset regenerated: {len(questions)} questions")

if __name__ == "__main__": regenerate()
