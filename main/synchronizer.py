from docsapi.docsapi import DocsAPIProtocol

import os
from os import PathLike
from pathlib import Path


class Synchronizer:
    def __init__(self, docsapi: DocsAPIProtocol, gitapi: GitAPIProtocol):
        self.docsapi = docsapi
        self.docs_folder = os.environ["DOCS_FOLDER"]
        self.gitapi = gitapi

    def read_document(self, document_path: PathLike) -> str:
        path = Path(self.docs_folder) / document_path
        with open(path, "r") as f:
            return f.read()

    def sync_document_by_path(self, document_path: PathLike) -> None:
        """
        Args:
        document_path: document name related to the DOCS_FOLDER. For example feature/specific/option.md
        """
        content = self.read_document(document_path)
        self.docsapi.sync_document_by_path(str(document_path), content=content)

    def sync_documents(self, changes: str) -> None:
        """
        Pushes all the documents in DOCS_FOLDER into remote resource
        """
