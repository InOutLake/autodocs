import os
import requests
from enum import Enum
from llm.llmagent import LlmAgent


class QwenModelsEnum(str, Enum):
    QWEN_7B_CHAT = "qwen-7b-chat"
    QWEN_14B_CHAT = "qwen-14b-chat"
    QWEN_72B_CHAT = "qwen-72b-chat"


class QwenLlm(LlmAgent):
    def __init__(self):
        self.apikey = os.environ["QWEN_API_KEY"]
        self.url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"  # Qwen/Tongyi API endpoint

    def answer(
        self,
        prompt: str,
        max_tokens: int = 2000,
        model: QwenModelsEnum = QwenModelsEnum.QWEN_72B_CHAT,
        temperature: float = 0.2,
        **kwargs,
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.apikey}",
            "Content-Type": "application/json",
            "X-DashScope-SSE": "enable",  # For Qwen API
        }
        payload = {
            "model": model,
            "input": {"messages": [{"role": "user", "content": prompt}]},
            "parameters": {
                "max_tokens": max_tokens,
                "temperature": temperature,
                **kwargs,
            },
        }
        response = requests.post(self.url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["output"]["text"]
