import os

import requests
from llm.llmagent import LlmAgent
from enum import StrEnum


class CerebrasModelsEnum(StrEnum):
    QWEN_INSTRUCT = "qwen-3-235b-a22b-instruct-2507"


class CerebrasLlm(LlmAgent):
    # TODO: Add strict structured-output integration.  https://inference-docs.cerebras.ai/capabilities/structured-outputs
    def __init__(self):
        self.apikey = os.environ["CEREBRAS_API_KEY"]
        self.url = "https://api.cerebras.ai/v1/chat/completions"

    def answer(
        self,
        prompt: str,
        max_tokens: int = 10000,
        model: CerebrasModelsEnum = CerebrasModelsEnum.QWEN_INSTRUCT,
        temperature: float = 0.2,
        response_format: str = "json_schema",
        **kwargs,
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.apikey}",
            "Content-Type": "application/json",
        }
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            # "response_format": response_format,
            "max_completion_tokens": max_tokens,
            "model": model,
            "temperature": temperature,
            "stream": False,
            **kwargs,
        }
        response = requests.post(self.url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
