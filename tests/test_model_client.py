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

"""Tests for the model client module."""
import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.model_client import OpenAIClient, OllamaClient, BaseModelClient, get_client  # noqa: E402
import unittest  # noqa: E402


class TestModelClientFactory(unittest.TestCase):
    def test_openai_client(self):
        client = get_client("openai", model="gpt-4")
        self.assertIsInstance(client, OpenAIClient)

    def test_ollama_client(self):
        client = get_client("ollama", model="llama3")
        self.assertIsInstance(client, OllamaClient)

    def test_default_client(self):
        client = get_client("unknown")
        self.assertIsInstance(client, OpenAIClient)


class TestOpenAIClientInit(unittest.TestCase):
    def test_default_values(self):
        client = OpenAIClient(model="gpt-4")
        self.assertEqual(client.model, "gpt-4")
        self.assertEqual(client.max_retries, 3)


class TestOllamaClientInit(unittest.TestCase):
    def test_default_values(self):
        client = OllamaClient(model="llama3")
        self.assertEqual(client.model, "llama3")


class TestBaseModelClientAbstract(unittest.TestCase):
    def test_abstract_methods(self):
        with self.assertRaises(TypeError):
            BaseModelClient()


if __name__ == "__main__":
    unittest.main()
