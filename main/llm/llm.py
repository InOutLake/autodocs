from llm.llmagent import LlmAgent
import hashlib
import json


class Llm:
    def __init__(self, agent: LlmAgent):
        self.agent = agent

    def get_files_to_change(
        self, ruleset: str, request: str, diff: str, existing_files: list[str]
    ):
        files_str = "\n".join(existing_files)

        prompt = f"""
        {ruleset}\n
        {request}\n

        Current documentation has following files:\n
        {files_str}

        Project has been changed in the following order:\n
        {diff}
        """
        return self.agent.answer(prompt)

    def update_docs(
        self,
        diff: str,
        templates: str,
        docs_to_change: str,
        language: str,
    ):
        prompt = f"""
        {diff}
        """
