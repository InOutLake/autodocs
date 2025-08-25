import os
import requests
from enum import Enum
from llm.llmagent import LlmAgent


class OpenAIModelsEnum(str, Enum):
    GPT_35_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4O = "gpt-4o"


class OpenAiLlm(LlmAgent):
    def __init__(self):
        self.apikey = os.environ["OPENAI_API_KEY"]
        self.url = "https://api.openai.com/v1/chat/completions"

    def answer(
        self,
        prompt: str,
        max_tokens: int = 1000,
        model: OpenAIModelsEnum = OpenAIModelsEnum.GPT_35_TURBO,
        temperature: float = 0.2,
        **kwargs,
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.apikey}",
            "Content-Type": "application/json",
        }
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "model": model,
            "temperature": temperature,
            **kwargs,
        }
        response = requests.post(self.url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
