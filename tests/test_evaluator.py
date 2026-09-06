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

"""Tests for the evaluator module."""
import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


if __name__ == "__main__":
    unittest.main()
