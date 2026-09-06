"""
Evaluation engine - scores model performance against the benchmark dataset.
MMLU-style evaluation with accuracy scoring.
"""
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
import logging
from typing import List, Dict, Any
from datetime import datetime

from src.parser import parse_answer, normalize_answer

logger = logging.getLogger(__name__)


class BenchmarkEvaluator:
    """Evaluates model responses against the benchmark dataset."""

    def __init__(self, dataset_path: str):
        self.dataset = self._load_dataset(dataset_path)
        self.results = []

    def _load_dataset(self, path: str) -> List[Dict[str, Any]]:
        """Load the JSONL dataset."""
        questions = []
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    questions.append(json.loads(line))
        logger.info(f"Loaded {len(questions)} questions from {path}")
        return questions

    def evaluate_single(self, question: Dict[str, Any], model_response: str) -> Dict[str, Any]:
        """Evaluate a single question response."""
        correct_answer = question["correct_answer"]
        is_multiple = question["is_multiple_choice"]

        parsed = parse_answer(model_response, is_multiple)
        is_correct = normalize_answer(parsed, correct_answer, question["is_multiple_choice"])

        result = {
            "id": question["id"],
            "title": question["title"],
            "question": question["question"][:200] + "...",
            "options": question["options"],
            "correct_answer": correct_answer,
            "model_response": model_response,
            "parsed_answer": parsed,
            "is_correct": is_correct,
            "is_multiple_choice": is_multiple,
            "explanation": question["explanation"]
        }
        return result

    def run_evaluation(self, client, max_questions: int = None, **kwargs) -> Dict[str, Any]:
        """
        Run full evaluation loop.

        Args:
            client: A BaseModelClient instance
            max_questions: Limit evaluation to first N questions (for testing)
            **kwargs: Additional kwargs passed to client.generate()

        Returns:
            Dictionary with full evaluation results
        """
        questions = self.dataset[:max_questions] if max_questions else self.dataset
        self.results = []

        total = len(questions)
        correct = 0
        multiple_correct = 0
        multiple_total = 0
        single_correct = 0
        single_total = 0

        for i, question in enumerate(questions):
            # Build the prompt
            prompt = self._build_prompt(question)

            logger.info(f"Evaluating Q{question['id']}: {question['title'][:50]}...")

            try:
                response = client.generate([{"role": "user", "content": prompt}], **kwargs)
            except Exception as e:
                logger.error(f"Error on Q{question['id']}: {e}")
                response = ""

            result = self.evaluate_single(question, response)
            self.results.append(result)

            if result["is_correct"]:
                correct += 1
                if result["is_multiple_choice"]:
                    multiple_correct += 1
                else:
                    single_correct += 1

            if result["is_multiple_choice"]:
                multiple_total += 1
            else:
                single_total += 1

            # Print progress
            status = "✓ CORRECT" if result["is_correct"] else "✗ INCORRECT"
            print(
                f"  Q{question['id']}: {status} | "
                f"Model: {result['parsed_answer']} | "
                f"Correct: {result['correct_answer']}"
            )

        # Calculate scores
        overall_accuracy = correct / total if total > 0 else 0.0
        single_accuracy = single_correct / single_total if single_total > 0 else 0.0
        multiple_accuracy = multiple_correct / multiple_total if multiple_total > 0 else 0.0

        summary = {
            "total_questions": total,
            "correct": correct,
            "incorrect": total - correct,
            "overall_accuracy": round(overall_accuracy * 100, 2),
            "single_choice_accuracy": round(single_accuracy * 100, 2),
            "multiple_choice_accuracy": round(multiple_accuracy * 100, 2),
            "single_choice_score": f"{single_correct}/{single_total}",
            "multiple_choice_score": f"{multiple_correct}/{multiple_total}",
            "timestamp": datetime.now().isoformat(),
            "results": self.results
        }

        return summary

    def _build_prompt(self, question: Dict[str, Any]) -> str:
        """Build the prompt sent to the model."""
        q = question
        options_text = "\n".join(q["options"])

        prompt = f"""{q['question']}

{options_text}

Please reason step by step, then provide your final answer in the format:
"Answer: X" where X is the correct option letter(s).

For multiple-select questions, list all correct letters (e.g., "Answer: A,B,D").

Question Type: {q['question_type']}"""

        return prompt

    def print_summary(self, summary: Dict[str, Any]) -> None:
        """Print a formatted summary of results."""
        print("\n" + "=" * 70)
        print("BENCHMARK RESULTS")
        print("=" * 70)
        print(f"Total Questions:    {summary['total_questions']}")
        print(f"Correct:            {summary['correct']}")
        print(f"Incorrect:          {summary['incorrect']}")
        print(f"Overall Accuracy:   {summary['overall_accuracy']}%")
        print(f"Single Choice:      {summary['single_choice_accuracy']}% ({summary['single_choice_score']})")
        print(f"Multiple Choice:    {summary['multiple_choice_accuracy']}% ({summary['multiple_choice_score']})")
        print("=" * 70)

        # Per-question breakdown
        print("\nPER-QUESTION BREAKDOWN:")
        print("-" * 70)
        for r in summary["results"]:
            status = "✓" if r["is_correct"] else "✗"
            print(
                f"  {status} Q{r['id']:>2}: {r['title'][:50]:<50} | "
                f"Ans: {r['parsed_answer']} | Correct: {r['correct_answer']}"
            )
        print("-" * 70)

    def save_results(self, summary: Dict[str, Any], output_path: str) -> None:
        """Save results to a JSON file."""
        # Remove the full results for the summary file, keep separate
        output = {k: v for k, v in summary.items() if k != "results"}
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        # Also save detailed results
        detailed_path = output_path.replace(".json", "_detailed.json")
        with open(detailed_path, 'w') as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Results saved to {output_path} and {detailed_path}")
