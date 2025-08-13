import json
import os
from pathlib import Path
from config import Config
from docs_manager import DocsManager
from git_tracker import GitTracker
from llm.llm import Llm


def read_config(path: str, name: str):
    with open(Path(path) / name, "r") as f:
        return f.read()


class DocsGenerator:
    def __init__(
        self, docs_manager: DocsManager, gitapi: GitTracker, llm: Llm, config: Config
    ):
        self.docs_manager = docs_manager
        self.gitapi = gitapi
        self.llm = llm
        self.config = config
        self.language = os.environ["LANGUAGE"]

    def update_docs(self) -> None:
        existing_documents = self.docs_manager.list_documents()
        existing_documents = json.dumps(existing_documents)
        diff = self.gitapi.last_sync_to_head_changes()
        files_to_change = self.llm.get_files_to_change(
            self.config["ruleset"],
            self.config["files_to_change_request"],
            diff,
            existing_documents,
        )
        print(files_to_change)
        try:
            files_to_change = json.loads(files_to_change)
        except Exception as _:
            ...

        request_files_to_change = {}
        needed_templates = set()
        for file, action in files_to_change:
            match action:
                case "create", document_type:
                    self.docs_manager.create_document(Path(file), document_type)
                    if document_type not in needed_templates:
                        needed_templates.add(document_type)
                    request_files_to_change[file] = Path(file).read_text()
                case "update":
                    request_files_to_change[file] = Path(file).read_text()
                case "delete":
                    self.docs_manager.delete_document(Path(file))

        templates = self.docs_manager.list_templates()
        templates = "\n\n".join(
            [
                template.path.stem + "\n" + template.content
                for template in templates
                if template in needed_templates
            ]
        )

        update = self.llm.update_docs(
            self.config["ruleset"],
            self.config["change_files_request"],
            diff,
            templates,
            files_to_change,
            language=self.language,
        )
        print(update)
