from functools import cache
from documents.Document import Document, Template
import os
from pathlib import Path
from typing import Any


class DocsManager:
    def __init__(self):
        self.docs_folder = Path(os.environ["DOCS_DIR"])
        self.templates_folder = Path(os.environ["TEMPLATES_DIR"])

    def list_folder(self, folder: Path) -> list[Path]:
        files_list = list[Path]()
        for f in folder.iterdir():
            if f.is_file():
                files_list.append(f)
            elif f.is_dir():
                files_list += self.list_folder(f)
            else:
                raise Exception(f"Unprocessable file type in docs: {str(f)}")
        return files_list

    def list_documents(self) -> list[Document]:
        paths_list = self.list_folder(self.docs_folder)
        return [Document(path, self.docs_folder) for path in paths_list]

    def list_documents_dicts(
        self,
        documents: list[Document] | None = None,
        fields: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        if documents is None:
            documents = self.list_documents()
        return [doc.to_dict(fields) for doc in documents]

    @cache
    def list_templates(self) -> list[Template]:
        path_list = self.list_folder(self.templates_folder)
        return [Template.from_path(path, self.templates_folder) for path in path_list]

    def list_templates_dicts(
        self,
        templates: list[Template] | None = None,
        fields: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        if templates is None:
            templates = self.list_templates()
        return [template.to_dict(fields) for template in templates]

    def read_document(self, document_path: Path) -> Document:
        return Document.from_path(document_path, self.docs_folder)

    def create_document(self, document_path: Path, template: str) -> Document:
        document = Document.new(document_path, self.docs_folder, template)
        return document

    def edit_document(self, document_path: Path, content: str) -> Document:
        document = Document.from_path(document_path, self.docs_folder)
        return document

    def delete_document(self, document_path: Path):
        document = Document(document_path, self.docs_folder)
        document.delete()

    def saveall(self, documents: list[Document]) -> None:
        [doc.save() for doc in documents]
