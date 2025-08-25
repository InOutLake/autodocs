import json
import os
from pathlib import Path
from config import TaskRequests
from docs_manager import DocsManager, Document
from git_tracker import GitTracker
from llm.llm import Llm


def read_config(path: str, name: str):
    with open(Path(path) / name, "r") as f:
        return f.read()


class DocsGenerator:
    def __init__(self, docs_manager: DocsManager, gitapi: GitTracker, llm: Llm):
        self.docs_manager = docs_manager
        self.gitapi = gitapi
        self.llm = llm
        self.language = os.environ["LANGUAGE"]

    def update_docs(self, custom_request: str | None = None) -> None:
        existing_documents = self.docs_manager.list_documents_dicts(
            fields=["path", "template"]
        )
        existing_documents = json.dumps(existing_documents)
        diff = self.gitapi.last_sync_to_head_changes()
        templates = self.docs_manager.list_templates()
        templates_stems = [t.path.stem for t in templates]
        files_to_change = self.llm.get_files_to_change(
            diff,
            templates_stems,
            existing_documents,
            custom_request=custom_request,
        )
        requested_documents_to_change: list[Document] = []
        for file, action in files_to_change.model_dump().items():
            match action:
                case "create", document_type:
                    document = self.docs_manager.create_document(
                        Path(file), document_type
                    )
                    requested_documents_to_change.append(document)
                case "update":
                    document = self.docs_manager.read_document(Path(file))
                    requested_documents_to_change.append(document)
                case "delete":
                    self.docs_manager.delete_document(Path(file))

        for document in requested_documents_to_change:
            doc_template = None
            for template in templates:
                if template.template == document.template:
                    doc_template = template
            if doc_template is None:
                raise Exception()
            doc_template = doc_template.content
            update = self.llm.update_document(
                document,
                doc_template,
                diff,
                language=self.language,
            )
            for number, content in update.model_dump().items():
                document.change_line(number, content)
            document.save()
            print(document.content)
