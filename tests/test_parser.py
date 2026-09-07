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

"""Tests for the response parser module."""
import sys  # noqa: E402
import os  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa: E402

from src.parser import parse_answer, normalize_answer  # noqa: E402
import unittest  # noqa: E402


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

    def test_whitespace_response(self):
        self.assertIsNone(parse_answer("   "))

    def test_whitespace_only_response(self):
        self.assertIsNone(parse_answer(""))

    def test_answer_equals(self):
        self.assertEqual(parse_answer("Answer: A"), "A")

    def test_answer_with_spaces(self):
        self.assertEqual(parse_answer("Answer: A, B, D"), "A,B,D")

    def test_correct_answer_is(self):
        self.assertEqual(parse_answer("The correct answer is A"), "A")

    def test_answer_would_choose(self):
        self.assertEqual(parse_answer("I would choose C"), "C")

    def test_answer_was(self):
        self.assertEqual(parse_answer("My answer was B"), "B")

    def test_parenthesized_answer(self):
        self.assertEqual(parse_answer("(A) is the correct answer"), "A")

    def test_correct_option(self):
        self.assertEqual(parse_answer("Correct option: C"), "C")

    def test_selected_option(self):
        self.assertEqual(parse_answer("Selected option: D"), "D")

    def test_answer_with_close_paren(self):
        self.assertEqual(parse_answer("Answer: A)"), "A")

    def test_uppercase_answer_letter(self):
        self.assertEqual(parse_answer("The answer is A"), "A")

    def test_multiple_letters_with_spaces(self):
        self.assertEqual(parse_answer("Answer: A , B , D"), "A,B,D")

    def test_letters_at_end(self):
        self.assertEqual(parse_answer("I think the answer is A"), "A")

    def test_embedded_letters_multiple_choice(self):
        self.assertEqual(parse_answer("The options are A, B, C, D. My answer is A,B,D", True), "A,B,D")

    def test_no_valid_letters(self):
        self.assertIsNone(parse_answer("I don't know the answer", True))

    def test_only_lowercase_letters_ignored(self):
        self.assertIsNone(parse_answer("The answer is true or false"))

    def test_multiple_choice_finds_all_letters(self):
        result = parse_answer("I would choose A, B, D", True)
        self.assertIn(result, ["A,B,D"])


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

    def test_none_returns_false(self):
        self.assertFalse(normalize_answer(None, "A", False))

    def test_empty_returns_false(self):
        self.assertFalse(normalize_answer("", "A", False))

    def test_case_insensitive_single(self):
        self.assertTrue(normalize_answer("a", "A", False))
        self.assertTrue(normalize_answer("B", "b", False))

    def test_case_insensitive_multiple(self):
        self.assertTrue(normalize_answer("a,b,d", "A,B,D", True))

    def test_whitespace_insensitive(self):
        self.assertTrue(normalize_answer(" A , B ", "A,B", True))

    def test_partial_multiple_returns_false(self):
        self.assertFalse(normalize_answer("A,B,C", "A,B,D,E", True))

    def test_extra_letters_multiple_choice(self):
        self.assertFalse(normalize_answer("A,B,C,D", "A,B,D", True))


class TestMain(unittest.TestCase):
    def test_main_runs(self):
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            from src.parser import main
            main()
        output = f.getvalue()
        self.assertIn("All tests passed: True", output)


if __name__ == "__main__":
    unittest.main()
