from requests import request
from config import TaskRequests
from docs_manager import Document
from llm.llmagent import LlmAgent
from pydantic import RootModel
import json


class DocumentsToChangeList(RootModel[dict[str, str | list]]): ...


class DocumentChangeList(RootModel[dict[int, str]]): ...


class Llm:
    def __init__(self, agent: LlmAgent):
        self.agent = agent
        self.requests = TaskRequests()

    def get_files_to_change(
        self,
        diff: str,
        templates_list: list[str],
        existing_files: str,
        custom_request: str | None = None,
    ):
        templates_formatted = "\n".join(templates_list)
        prompt = f"""
        {self.requests["ruleset"]}\n\n
        {self.requests["files_to_change_request"]}\n\n
        {"Additional info:\n" + self.requests["additional_info"] if self.requests["additional_info"] else ""}\n\n
        {self.requests["custom_request"] if custom_request is not None else ""}\n
        {custom_request if custom_request is not None else ""}\n\n
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
        document: Document,  # TODO: get rid of document object for better decoupling
        template: str,
        diff: str,
        language: str,
        custom_request: str | None = None,
    ) -> DocumentChangeList:
        prompt = f"""
        {self.requests["rulesetl"]}\n\n
        {self.requests["change_file_request"]}\n\n
        {"Additional info:\n" + self.requests["additional_info"] if self.requests["additional_info"] else ""}\n\n
        {self.requests["custom_request"] if custom_request is not None else ""}\n
        {custom_request if custom_request is not None else ""}\n\n
        The document to change:\n
        {document.path}\n
        {document.numbered_content()}\n\n
        Template:\n
        {template}\n\n
        Program difference:\n
        {diff}\n\n
        Write documentation in the {language} language.
        """
        return DocumentChangeList(json.loads(self.agent.answer(prompt)))
