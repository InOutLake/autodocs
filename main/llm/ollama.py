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
        max_tokens: int = 1000,
        temperature: float = 0.2,
        json_response: bool = False,
        **kwargs,
    ) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "think": False,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if json_response:
            payload["format"] = "json"
        response = requests.post(self.url + "/api/generate", json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
