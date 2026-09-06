"""Tests for the evaluator module."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluator import BenchmarkEvaluator
import unittest


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


if __name__ == "__main__":
    unittest.main()
