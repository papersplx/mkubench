"""
Model client module - supports any OpenAI-compatible API or local LLM server.
Supports: Ollama, vLLM, LocalAI, OpenAI, Anthropic (via compatible endpoints)
"""
import os
import json
import time
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

import requests

logger = logging.getLogger(__name__)


class BaseModelClient(ABC):
    """Abstract base class for model clients."""

    @abstractmethod
    def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response from the model."""
        pass

    @abstractmethod
    def batch_generate(self, prompts: List[str], **kwargs) -> List[str]:
        """Generate responses in batch."""
        pass


class OpenAIClient(BaseModelClient):
    """Client for any OpenAI-compatible API endpoint."""

    def __init__(
        self,
        model: str = "gpt-4",
        api_base: str = None,
        api_key: str = None,
        timeout: int = 120,
        max_retries: int = 3,
        **kwargs
    ):
        self.model = model
        self.api_base = api_base or os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "dummy-key-for-local")
        self.timeout = timeout
        self.max_retries = max_retries
        self.kwargs = kwargs

        # Ensure api_base has trailing slash for compatibility
        if not self.api_base.endswith("/"):
            self.api_base += "/"

    def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send messages to the model and return the response text."""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.0),
            "max_tokens": kwargs.get("max_tokens", 2048),
            "top_p": kwargs.get("top_p", 1.0),
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{self.api_base}chat/completions",
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    timeout=self.timeout,
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            except requests.exceptions.RequestException as e:
                logger.warning(f"API call attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise

        return ""

    def batch_generate(self, prompts: List[str], **kwargs) -> List[str]:
        """Generate responses for a list of prompts (sequential with rate limiting)."""
        results = []
        for i, prompt in enumerate(prompts):
            messages = [{"role": "user", "content": prompt}]
            try:
                resp = self.generate(messages, **kwargs)
                results.append(resp)
            except Exception as e:
                logger.error(f"Failed on prompt {i}: {e}")
                results.append("")
            time.sleep(kwargs.get("delay", 0.1))
        return results


class OllamaClient(BaseModelClient):
    """Client for Ollama local LLM server."""

    def __init__(self, model: str = "llama3", host: str = "http://localhost:11434", **kwargs):
        self.model = model
        self.host = host.rstrip("/")
        self.kwargs = kwargs

    def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send messages to Ollama and return response."""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.0),
                "num_predict": kwargs.get("max_tokens", 2048),
            }
        }

        for attempt in range(3):
            try:
                response = requests.post(
                    f"{self.host}/api/generate",
                    json=payload,
                    timeout=self.kwargs.get("timeout", 120),
                )
                response.raise_for_status()
                data = response.json()
                return data.get("response", "").strip()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Ollama call attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    time.sleep(2 ** attempt)
                else:
                    raise

        return ""

    def batch_generate(self, prompts: List[str], **kwargs) -> List[str]:
        results = []
        for i, prompt in enumerate(prompts):
            messages = [{"role": "user", "content": prompt}]
            try:
                resp = self.generate(messages, **kwargs)
                results.append(resp)
            except Exception as e:
                logger.error(f"Failed on prompt {i}: {e}")
                results.append("")
            time.sleep(kwargs.get("delay", 0.5))
        return results


def get_client(client_type: str = "openai", **kwargs) -> BaseModelClient:
    """Factory function to get the appropriate client."""
    if client_type == "ollama":
        return OllamaClient(**kwargs)
    elif client_type == "openai":
        return OpenAIClient(**kwargs)
    else:
        return OpenAIClient(**kwargs)
