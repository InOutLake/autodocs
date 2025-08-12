import os
from os import PathLike
from pathlib import Path

from docsapi.docsapi import DocsAPIProtocol
from git_tracker import GitTracker


class DocsManager:
    def __init__(self, docsapi: DocsAPIProtocol, gitapi: GitTracker):
        self.docsapi = docsapi
        self.docs_folder = Path(os.environ["DOCS_FOLDER"])
        self.gitapi = gitapi

    def list_folder(self, folder: PathLike) -> list[PathLike]:
        folder = Path(folder)
        files_list = []
        for f in folder.iterdir():
            if f.is_file():
                files_list.append(str(f))
            else:
                files_list += self.list_folder(f)
        return files_list

    def list_documents(self) -> list[PathLike]:
        return self.list_folder(self.docs_folder)

    def sync_document_by_path(self, document_path: PathLike) -> None:
        path = Path(self.docs_folder) / document_path
        with open(path, "rw") as f:
            updated_document = self.docsapi.sync_document_by_path(
                str(document_path), content=f.read()
            )
            f.seek(0)
            f.write(updated_document.content)

    def sync_documents(self) -> None:
        documents = self.list_documents()
        for doc in documents:
            self.sync_document_by_path(doc)
