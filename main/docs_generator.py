"""
TODO
Based on the changes logs and ruleset (dont forget cache) create new docs or change existing with LLM.
Insert change history in the table with short changes summary.
"""

import os
from pathlib import Path
from docs_manager import DocsManager
from llm.llm import Llm


def read_config(path: str, name: str):
    with open(Path(path) / name, "r") as f:
        return f.read()


class DocsGenerator:
    def __init__(self, docs_manager: DocsManager, llm: Llm):
        self.docs_manager = docs_manager
        self.llm = llm
        self.config_folder = os.environ["CONFIG_FOLDER"]
        self.language = os.environ["LANGUAGE"]

    def update_docs(self):
        diff = self.docs_manager.gitapi.last_sync_to_head_changes()
        ruleset = read_config(self.config_folder, "ruleset.md")
        files_to_change_request = read_config(
            self.config_folder, "files_to_change_request.md"
        )
        change_files_request = read_config(
            self.config_folder, "change_files_request.md"
        )
        existing_files = [str(doc) for doc in self.docs_manager.list_documents()]
        files_to_change = self.llm.get_files_to_change(
            ruleset,
            files_to_change_request,
            diff,
            existing_files,
        )
        print(files_to_change)

        self.llm.update_docs(
            ruleset,
            change_files_request,
            diff,
            templates,
            files_to_change,
            language=self.language,
        )
