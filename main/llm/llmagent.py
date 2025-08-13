from typing import Protocol


class LlmAgent(Protocol):
    def answer(self, prompt: str, max_tokens: int, **kwargs) -> str: ...
