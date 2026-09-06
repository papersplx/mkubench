"""Tests for the model client module."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.model_client import OpenAIClient, OllamaClient, BaseModelClient, get_client
import unittest


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
