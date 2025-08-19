from typing import List, Literal
from docs_manager import Document, Template
from llm.llmagent import LlmAgent
from pydantic import BaseModel, Field, RootModel
import json


class DocumentsToChangeList(RootModel[dict[str, str | list]]): ...


class DocumentChange(BaseModel):
    line_start: int = Field(examples=[4])
    line_end: int = Field(examples=[7])
    content: str = Field(
        examples=[
            "## GET /v2/adjust_position\nAdjusts position of an object\nV2 has additional fields:"
        ]
    )


class DocumentChangeList(RootModel[list[DocumentChange]]): ...


class Llm:
    def __init__(self, agent: LlmAgent):
        self.agent = agent

    def get_files_to_change(
        self,
        ruleset: str,
        request: str,
        diff: str,
        templates_list: list[str],
        existing_files: str,
    ):
        templates_formatted = "\n".join(templates_list)
        prompt = f"""
        {ruleset}\n\n
        {request}\n\n
        Available templates:
        {templates_formatted}\n\n
        Current documentation has following files:\n
        {existing_files}\n\n
        Project has been changed in the following order:\n
        {diff}\n\n
        """
        return DocumentsToChangeList(json.loads(self.agent.answer(prompt)))

    def update_document(
        self,
        ruleset: str,
        request: str,
        document: Document,
        template: Template,
        diff: str,
        language: str,
    ) -> DocumentChangeList:
        prompt = f"""
        {ruleset}\n\n
        {request}\n\n
        The document to change:\n
        {document.path}\n
        {document.numbered_content()}\n\n
        Template:\n
        {template.content}\n\n
        Program difference:\n
        {diff}\n\n
        Write documentation in the {language} language.
        """
        return DocumentChangeList(json.loads(self.agent.answer(prompt)))
