"""Tests for the response parser module."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parser import parse_answer, normalize_answer
import unittest


class TestParseAnswer(unittest.TestCase):
    def test_answer_letter(self):
        self.assertEqual(parse_answer("The answer is B"), "B")
    
    def test_answer_multiple_choice(self):
        self.assertEqual(parse_answer("Answer: A,B,D"), "A,B,D")
    
    def test_letter_format(self):
        self.assertEqual(parse_answer("B"), "B")
    
    def test_final_answer(self):
        self.assertEqual(parse_answer("Final answer: D"), "D")
    
    def test_empty_response(self):
        self.assertIsNone(parse_answer(""))
    
    def test_none_response(self):
        self.assertIsNone(parse_answer(None))
    
    def test_wrong_answer(self):
        self.assertEqual(parse_answer("Answer: C"), "C")


class TestNormalizeAnswer(unittest.TestCase):
    def test_single_correct(self):
        self.assertTrue(normalize_answer("B", "B", False))
    
    def test_single_wrong(self):
        self.assertFalse(normalize_answer("A", "B", False))
    
    def test_multiple_correct(self):
        self.assertTrue(normalize_answer("A,B,D", "A,B,D", True))
    
    def test_multiple_wrong(self):
        self.assertFalse(normalize_answer("A,B,C", "A,B,D", True))
    
    def test_multiple_partial(self):
        self.assertFalse(normalize_answer("A,B", "A,B,D", True))


if __name__ == "__main__":
    unittest.main()
