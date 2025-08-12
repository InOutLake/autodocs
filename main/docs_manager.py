from _typeshed import StrPath
import os
from os import PathLike
from pathlib import Path

from docsapi.docsapi import DocsAPIProtocol
from git_tracker import GitTracker


class Document(Path):
    def __init__(self, path: StrPath):
        super().__init__(path)


class DocsManager:
    def __init__(self, docsapi: DocsAPIProtocol, gitapi: GitTracker):
        self.docsapi = docsapi
        self.gitapi = gitapi
        self.docs_folder = Path(os.environ["DOCS_FOLDER"])
        self.templates_folder = Path(os.environ["TEMPLATES_FOLDER"])

    def list_folder(self, folder: Path) -> list[Path]:
        files_list = []
        for f in folder.iterdir():
            if f.is_file():
                files_list.append(str(f))
            elif f.is_dir():
                files_list += self.list_folder(f)
            else:
                raise Exception("Unknown file type in docs (probably symlink)")
        return files_list

    def list_documents_with_types(self) -> dict[Path, str]:
        documents_with_types = {}
        documents_list = self.list_folder(self.docs_folder)
        for document in documents_list:
            with open(document, "r") as d:
                documents_with_types[document] = d.readline()
        return documents_with_types

    def list_documents_with_content(self) -> dict[str, str]:
        documents_with_content = {}
        documents_list = self.list_folder(self.docs_folder)
        for document in documents_list:
            with open(document, "r") as d:
                documents_with_content[Path(document).relative_to(self.docs_folder)] = (
                    d.read()
                )
        return documents_with_content

    def sync_document_by_path(self, document_path: PathLike) -> None:
        path = Path(self.docs_folder) / document_path
        with open(path, "rw") as f:
            updated_document = self.docsapi.sync_document_by_path(
                str(document_path), content=f.read()
            )
            f.seek(0)
            f.write(updated_document.content)

    def sync_documents(self) -> None:
        documents = self.list_documents_with_types().keys()
        documents = [Path(doc).relative_to(self.docs_folder) for doc in documents]
        for doc in documents:
            self.sync_document_by_path(doc)

    def templates(self) -> dict[Path, str]:
        templates = {}
        templates_list = self.list_folder(self.templates_folder)
        for template in templates_list:
            with open(template, "r") as t:
                templates[template.read_text] = {
                    "content": t.read(),
                }
        return templates

    def create_document(self, document_path: Path, document_type: str):
        document_path.write_text(f"<<Template={document_type}>>")

    def edit_document(self, document_path: Path, content: str):
        document_path.write_text(content)

    def delete_document(self, document_path: Path):
        document_path.unlink()
