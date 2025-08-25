import os

import requests
from llm.llmagent import LlmAgent
from enum import StrEnum


class OllamaModelsEnum(StrEnum):
    LAMA3 = "llama3"
    MISTRAL = "mistral"


class OllamaLlm(LlmAgent):
    def __init__(self):
        self.url = os.environ.get(
            "OLLAMA_API_URL", "http://localhost:11434/api/generate"
        )

    def answer(
        self,
        prompt: str,
        max_tokens: int = 10000,
        model: OllamaModelsEnum = OllamaModelsEnum.LAMA3,
        temperature: float = 0.2,
        **kwargs,
    ) -> str:
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                **kwargs,
            },
        }
        response = requests.post(self.url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["response"]
