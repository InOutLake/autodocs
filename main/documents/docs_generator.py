import json
import os
from pathlib import Path
from main.documents.docs_manager import DocsManager, Document
from git_tracker import GitTracker
from llm.llm import Llm


def read_config(path: str, name: str):
    with open(Path(path) / name, "r") as f:
        return f.read()


class DocsGenerator:
    # TODO: refactor to work with documents as buffers
    # Not sure where do I place main logic: in the main function or right there in the interface functions.
    # It may be beneficial to exclude gitapi logic and make one more abstraction layer or store diff and other values in self variables
    def __init__(self, docs_manager: DocsManager, llm: Llm):
        self.docs_manager = docs_manager
        self.llm = llm
        self.language = os.environ["LANGUAGE"]

    # TODO: may pass the diff directly instead of commit hash
    def documents_to_change(
        self,
        diff: str,
        custom_request: str | None = None,
    ) -> list[Document]:
        existing_documents = self.docs_manager.list_documents_dicts(
            fields=["path", "template"]
        )
        existing_documents = json.dumps(existing_documents)
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
        return requested_documents_to_change

    def update_document(
        self,
        document: Document,
        diff: str,
        custom_request: str | None = None,
    ) -> None:
        templates = self.docs_manager.list_templates()
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
            custom_request=custom_request,
        )
        document.change_lines(update.model_dump())

    def update_docs(
        self,
        documents: list[Document],
        diff: str,
        custom_request: str | None = None,
    ) -> None:
        for document in documents:
            self.update_document(document, diff, custom_request)
