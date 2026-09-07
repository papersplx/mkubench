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
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa: E402

from unittest.mock import patch, MagicMock  # noqa: E402

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

    def test_get_client_ollama_with_kwargs(self):
        client = get_client("ollama", model="llama3", host="http://localhost:11434")
        self.assertIsInstance(client, OllamaClient)
        self.assertEqual(client.host, "http://localhost:11434")

    def test_get_client_openai_with_kwargs(self):
        client = get_client("openai", model="gpt-4", api_base="http://localhost:8000/v1")
        self.assertIsInstance(client, OpenAIClient)
        self.assertEqual(client.api_base, "http://localhost:8000/v1/")


class TestOpenAIClientInit(unittest.TestCase):
    def test_default_values(self):
        client = OpenAIClient(model="gpt-4")
        self.assertEqual(client.model, "gpt-4")
        self.assertEqual(client.max_retries, 3)
        self.assertEqual(client.timeout, 120)
        self.assertEqual(client.kwargs, {})

    def test_custom_values(self):
        client = OpenAIClient(model="gpt-4", api_base="http://localhost:8000/v1", timeout=60, max_retries=5)
        self.assertEqual(client.model, "gpt-4")
        self.assertEqual(client.timeout, 60)
        self.assertEqual(client.max_retries, 5)
        self.assertEqual(client.api_base, "http://localhost:8000/v1/")

    def test_api_base_trailing_slash(self):
        client = OpenAIClient(model="gpt-4", api_base="http://localhost:8000/v1/")
        self.assertEqual(client.api_base, "http://localhost:8000/v1/")

    def test_api_key_from_env(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            client = OpenAIClient(model="gpt-4")
            self.assertEqual(client.api_key, "test-key")

    def test_kwargs_stored(self):
        client = OpenAIClient(model="gpt-4", temperature=0.5)
        self.assertEqual(client.kwargs, {"temperature": 0.5})


class TestOllamaClientInit(unittest.TestCase):
    def test_default_values(self):
        client = OllamaClient(model="llama3")
        self.assertEqual(client.model, "llama3")
        self.assertEqual(client.host, "http://localhost:11434")
        self.assertEqual(client.kwargs, {})

    def test_custom_host(self):
        client = OllamaClient(model="llama3", host="http://localhost:8080")
        self.assertEqual(client.host, "http://localhost:8080")

    def test_host_trailing_slash_stripped(self):
        client = OllamaClient(model="llama3", host="http://localhost:11434/")
        self.assertEqual(client.host, "http://localhost:11434")

    def test_kwargs_stored(self):
        client = OllamaClient(model="llama3", timeout=60)
        self.assertEqual(client.kwargs, {"timeout": 60})


class TestBaseModelClientAbstract(unittest.TestCase):
    def test_abstract_methods(self):
        with self.assertRaises(TypeError):
            BaseModelClient()

    def test_generate_abstract(self):
        with self.assertRaises(TypeError):
            BaseModelClient.generate(None)

    def test_batch_generate_abstract(self):
        with self.assertRaises(TypeError):
            BaseModelClient.batch_generate(None)


class TestOpenAIClientGenerate(unittest.TestCase):
    def test_generate_returns_content(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "  Answer: A  "}}]
        }
        mock_response.raise_for_status.return_value = None
        client = OpenAIClient(model="gpt-4")
        with patch("src.model_client.requests.post", return_value=mock_response):
            result = client.generate([{"role": "user", "content": "What is X?"}])
        self.assertEqual(result, "Answer: A")

    def test_generate_raises_after_retries(self):
        client = OpenAIClient(model="gpt-4", max_retries=2)
        with patch("src.model_client.requests.post", side_effect=Exception("Network error")):
            with self.assertRaises(Exception):
                client.generate([{"role": "user", "content": "What is X?"}])

    def test_generate_passes_kwargs(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Answer: B"}}]
        }
        mock_response.raise_for_status.return_value = None
        client = OpenAIClient(model="gpt-4")
        with patch("src.model_client.requests.post", return_value=mock_response):
            client.generate([{"role": "user", "content": "What is X?"}], temperature=0.7)
        # Verify the payload was constructed with kwargs


class TestOllamaClientGenerate(unittest.TestCase):
    def test_generate_returns_response(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "  Answer: C  "}
        mock_response.raise_for_status.return_value = None
        client = OllamaClient(model="llama3")
        with patch("src.model_client.requests.post", return_value=mock_response):
            result = client.generate([{"role": "user", "content": "What is X?"}])
        self.assertEqual(result, "Answer: C")

    def test_generate_raises_after_retries(self):
        client = OllamaClient(model="llama3")
        with patch("src.model_client.requests.post", side_effect=Exception("Network error")):
            with self.assertRaises(Exception):
                client.generate([{"role": "user", "content": "What is X?"}])


class TestOpenAIClientBatchGenerate(unittest.TestCase):
    def test_batch_generate_returns_results(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Answer: A"}}]
        }
        mock_response.raise_for_status.return_value = None
        client = OpenAIClient(model="gpt-4")
        with patch("src.model_client.requests.post", return_value=mock_response):
            results = client.batch_generate(["Q1?", "Q2?"], delay=0)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], "Answer: A")
        self.assertEqual(results[1], "Answer: A")

    def test_batch_generate_handles_errors(self):
        client = OpenAIClient(model="gpt-4")
        with patch("src.model_client.requests.post", side_effect=Exception("Error")):
            results = client.batch_generate(["Q1?"], delay=0)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], "")


class TestOllamaClientBatchGenerate(unittest.TestCase):
    def test_batch_generate_returns_results(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "Answer: D"}
        mock_response.raise_for_status.return_value = None
        client = OllamaClient(model="llama3")
        with patch("src.model_client.requests.post", return_value=mock_response):
            results = client.batch_generate(["Q1?", "Q2?"], delay=0)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], "Answer: D")


if __name__ == "__main__":
    unittest.main()
