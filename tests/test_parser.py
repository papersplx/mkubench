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
