import os

from llm.llmagent import LlmAgent
import requests


class OllamaLLM(LlmAgent):
    def __init__(self):
        self.model = os.environ["OLLAMA_MODEL"]
        self.url = os.environ["OLLAMA_URL"]

    def answer(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 10000,
    ) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature, "max_tokens": max_tokens},
        }
        response = requests.get(self.url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
