import os
import requests
from enum import Enum
from llm.llmagent import LlmAgent


class ClaudeModelsEnum(str, Enum):
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
    CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_3_OPUS = "claude-3-opus-20240229"


class ClaudeLlm(LlmAgent):
    def __init__(self):
        self.apikey = os.environ["ANTHROPIC_API_KEY"]
        self.url = "https://api.anthropic.com/v1/messages"

    def answer(
        self,
        prompt: str,
        max_tokens: int = 1000,
        model: ClaudeModelsEnum = ClaudeModelsEnum.CLAUDE_3_HAIKU,
        temperature: float = 0.2,
        **kwargs,
    ) -> str:
        headers = {
            "x-api-key": self.apikey,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",  # Required header for Claude API
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
        return response.json()["content"][0]["text"]
