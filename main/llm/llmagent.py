from typing import Protocol


class LlmAgent(Protocol):
    def answer(self, prompt: str) -> str: ...
