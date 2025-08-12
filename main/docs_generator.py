import json
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

    def update_docs(self) -> None:
        diff = self.docs_manager.gitapi.last_sync_to_head_changes()
        ruleset = read_config(self.config_folder, "ruleset.md")
        files_to_change_request = read_config(
            self.config_folder, "files_to_change_request.md"
        )
        change_files_request = read_config(
            self.config_folder, "change_files_request.md"
        )
        existing_documents = self.docs_manager.list_documents_with_types()
        existing_documents = json.dumps(existing_documents)
        files_to_change = self.llm.get_files_to_change(
            ruleset,
            files_to_change_request,
            diff,
            existing_documents,
        )
        print(files_to_change)
        files_to_change = json.loads(files_to_change)

        request_files_to_change = {}
        needed_templates = set()
        for file, action in files_to_change:
            match action:
                case "create", document_type:
                    self.docs_manager.create_document(file, document_type)
                    if document_type not in needed_templates:
                        needed_templates.add(document_type)
                    request_files_to_change[file] = Path(file).read_text()
                case "update":
                    request_files_to_change[file] = Path(file).read_text()
                case "delete":
                    self.docs_manager.delete_document(Path(file))

        templates = self.docs_manager.templates()
        templates = "\n\n".join(
            [template.stem for template in templates if template in needed_templates]
        )

        update = self.llm.update_docs(
            ruleset,
            change_files_request,
            diff,
            templates,
            files_to_change,
            language=self.language,
        )
        print(update)
