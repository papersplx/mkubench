# Copyright (c) 2026 competitiveNN
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

"""Tests for the evaluator module."""
import os  # noqa: E402
import sys  # noqa: E402
import json  # noqa: E402
import tempfile  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa: E402

from unittest.mock import MagicMock  # noqa: E402

from src.evaluator import BenchmarkEvaluator  # noqa: E402
import unittest  # noqa: E402


class TestBenchmarkEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = BenchmarkEvaluator('dataset/mkultra_benchmark.jsonl')

    def test_dataset_loaded(self):
        self.assertGreater(len(self.evaluator.dataset), 0)

    def test_dataset_has_questions(self):
        for q in self.evaluator.dataset:
            self.assertIn("id", q)
            self.assertIn("question", q)
            self.assertIn("options", q)
            self.assertIn("correct_answer", q)
            self.assertIn("is_multiple_choice", q)

    def test_evaluation_count(self):
        self.assertEqual(len(self.evaluator.dataset), 30)

    def test_single_choice_questions(self):
        single = [q for q in self.evaluator.dataset if not q["is_multiple_choice"]]
        self.assertGreater(len(single), 0)

    def test_multiple_choice_questions(self):
        multiple = [q for q in self.evaluator.dataset if q["is_multiple_choice"]]
        self.assertGreater(len(multiple), 0)

    def test_category(self):
        for q in self.evaluator.dataset:
            self.assertEqual(q.get("category", ""), "mkultra")

    def test_load_dataset(self):
        questions = self.evaluator._load_dataset('dataset/mkultra_benchmark.jsonl')
        self.assertEqual(len(questions), 30)

    def test_load_dataset_empty_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            f.write("")
            tmp_path = f.name
        try:
            questions = self.evaluator._load_dataset(tmp_path)
            self.assertEqual(len(questions), 0)
        finally:
            os.unlink(tmp_path)

    def test_load_dataset_invalid_line(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            f.write('{"id": 1}\nnot json\n{"id": 2}\n')
            tmp_path = f.name
        try:
            with self.assertRaises(json.JSONDecodeError):
                self.evaluator._load_dataset(tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_evaluate_single_correct(self):
        question = {
            "id": 1, "title": "Test Q", "question": "What is X?",
            "options": ["A) Yes", "B) No"], "correct_answer": "A",
            "is_multiple_choice": False, "explanation": "A is correct"
        }
        result = self.evaluator.evaluate_single(question, "The answer is A")
        self.assertTrue(result["is_correct"])
        self.assertEqual(result["parsed_answer"], "A")
        self.assertEqual(result["correct_answer"], "A")

    def test_evaluate_single_wrong(self):
        question = {
            "id": 1, "title": "Test Q", "question": "What is X?",
            "options": ["A) Yes", "B) No"], "correct_answer": "A",
            "is_multiple_choice": False, "explanation": "A is correct"
        }
        result = self.evaluator.evaluate_single(question, "The answer is B")
        self.assertFalse(result["is_correct"])
        self.assertEqual(result["parsed_answer"], "B")

    def test_evaluate_single_multiple_choice(self):
        question = {
            "id": 1, "title": "Test Q", "question": "Pick all",
            "options": ["A) Yes", "B) No", "C) Maybe", "D) Nope"],
            "correct_answer": "A,B,D", "is_multiple_choice": True,
            "explanation": "A,B,D are correct"
        }
        result = self.evaluator.evaluate_single(question, "Answer: A,B,D")
        self.assertTrue(result["is_correct"])

    def test_evaluate_single_multiple_choice_wrong(self):
        question = {
            "id": 1, "title": "Test Q", "question": "Pick all",
            "options": ["A) Yes", "B) No", "C) Maybe", "D) Nope"],
            "correct_answer": "A,B,D", "is_multiple_choice": True,
            "explanation": "A,B,D are correct"
        }
        result = self.evaluator.evaluate_single(question, "Answer: A,B")
        self.assertFalse(result["is_correct"])

    def test_build_prompt(self):
        question = {
            "id": 1, "title": "Test Q", "question": "What is X?",
            "options": ["A) Yes", "B) No"], "correct_answer": "A",
            "is_multiple_choice": False, "explanation": "A is correct",
            "question_type": "Single Choice"
        }
        prompt = self.evaluator._build_prompt(question)
        self.assertIn("What is X?", prompt)
        self.assertIn("A) Yes", prompt)
        self.assertIn("B) No", prompt)
        self.assertIn("Answer: X", prompt)

    def test_build_prompt_multiple_choice(self):
        question = {
            "id": 1, "title": "Test Q", "question": "Pick all",
            "options": ["A) Yes", "B) No"], "correct_answer": "A,B",
            "is_multiple_choice": True, "explanation": "Both correct",
            "question_type": "Multiple Choice"
        }
        prompt = self.evaluator._build_prompt(question)
        self.assertIn("Pick all", prompt)
        self.assertIn("Answer: A,B", prompt)

    def test_run_evaluation_with_mock_client(self):
        def mock_generate(messages, **kwargs):
            return "Answer: B"
        mock_client = MagicMock()
        mock_client.generate.side_effect = mock_generate
        summary = self.evaluator.run_evaluation(mock_client, max_questions=1)
        self.assertEqual(summary["total_questions"], 1)
        self.assertEqual(summary["correct"], 1)
        self.assertEqual(summary["overall_accuracy"], 100.0)

    def test_run_evaluation_max_questions(self):
        def mock_generate(messages, **kwargs):
            return "Answer: B"
        mock_client = MagicMock()
        mock_client.generate.side_effect = mock_generate
        summary = self.evaluator.run_evaluation(mock_client, max_questions=5)
        self.assertEqual(len(summary["results"]), 5)
        # Only questions with correct_answer "B" will be correct
        correct_count = sum(1 for q in self.evaluator.dataset[:5] if q["correct_answer"] == "B")
        self.assertEqual(summary["correct"], correct_count)

    def test_run_evaluation_partial_correct(self):
        def mock_generate(messages, **kwargs):
            return "The answer is wrong"
        mock_client = MagicMock()
        mock_client.generate.side_effect = mock_generate
        summary = self.evaluator.run_evaluation(mock_client, max_questions=5)
        self.assertEqual(summary["correct"], 0)
        self.assertEqual(summary["overall_accuracy"], 0.0)

    def test_run_evaluation_handles_errors(self):
        mock_client = MagicMock()
        mock_client.generate.side_effect = Exception("API Error")
        summary = self.evaluator.run_evaluation(mock_client, max_questions=3)
        self.assertEqual(summary["total_questions"], 3)
        self.assertEqual(summary["correct"], 0)

    def test_save_results(self):
        summary = {
            "total_questions": 30,
            "correct": 20,
            "overall_accuracy": 66.67,
            "timestamp": "2026-01-01T00:00:00",
            "results": [{"id": 1, "is_correct": True}]
        }
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            tmp_path = f.name
        try:
            self.evaluator.save_results(summary, tmp_path)
            with open(tmp_path) as f:
                data = json.load(f)
            self.assertEqual(data["total_questions"], 30)
            self.assertNotIn("results", data)
            # Check detailed file exists
            detailed_path = os.path.splitext(tmp_path)[0] + "_detailed.json"
            self.assertTrue(os.path.exists(detailed_path))
            with open(detailed_path) as f:
                detailed = json.load(f)
            self.assertIn("results", detailed)
        finally:
            os.unlink(tmp_path)
            detailed_path = os.path.splitext(tmp_path)[0] + "_detailed.json"
            if os.path.exists(detailed_path):
                os.unlink(detailed_path)

    def test_print_summary(self):
        summary = {
            "total_questions": 30,
            "correct": 20,
            "incorrect": 10,
            "overall_accuracy": 66.67,
            "single_choice_accuracy": 70.0,
            "single_choice_score": "14/20",
            "multiple_choice_accuracy": 60.0,
            "multiple_choice_score": "6/10",
            "results": [
                {"id": 1, "is_correct": True, "title": "Q1", "parsed_answer": "A", "correct_answer": "A"},
                {"id": 2, "is_correct": False, "title": "Q2", "parsed_answer": "B", "correct_answer": "A"},
            ]
        }
        # Should not raise
        self.evaluator.print_summary(summary)

    def test_save_results_with_colon_in_timestamp(self):
        summary = {
            "total_questions": 30,
            "correct": 20,
            "overall_accuracy": 66.67,
            "timestamp": "2026-01-01T12:30:00",
            "results": [{"id": 1, "is_correct": True}]
        }
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            tmp_path = f.name
        try:
            self.evaluator.save_results(summary, tmp_path)
            # Verify no error from colons in filename
            self.assertTrue(os.path.exists(tmp_path))
        finally:
            os.unlink(tmp_path)
            detailed_path = os.path.splitext(tmp_path)[0] + "_detailed.json"
            if os.path.exists(detailed_path):
                os.unlink(detailed_path)


if __name__ == "__main__":
    unittest.main()
