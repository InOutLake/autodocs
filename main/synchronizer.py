from docsapi.docsapi import DocsAPIProtocol
from git_tracker import GitTracker

import os
from os import PathLike
from pathlib import Path


class Synchronizer:
    def __init__(self, docsapi: DocsAPIProtocol, gitapi: GitTracker):
        self.docsapi = docsapi
        self.docs_folder = Path(os.environ["DOCS_FOLDER"])
        self.gitapi = gitapi

    def sync_document_by_path(self, document_path: PathLike) -> None:
        """
        Args:
        - document_path: document name related to the DOCS_FOLDER. Example: feature/specific/option.md
        """
        path = Path(self.docs_folder) / document_path
        with open(path, "rw") as f:
            updated_document = self.docsapi.sync_document_by_path(
                str(document_path), content=f.read()
            )
            f.seek(0)
            f.write(updated_document.content)

    def sync_documents(self) -> None:
        """
        Pushes all the documents in DOCS_FOLDER into remote resource
        """
        self.sync_folder(self.docs_folder)

    def sync_folder(self, path: PathLike) -> None:
        path = Path(path)
        for f in path.iterdir():
            if f.is_file():
                with open(f, "r") as file:
                    self.docsapi.sync_document_by_path(
                        str(path.relative_to(self.docs_folder)), file.read()
                    )
            else:
                self.sync_folder(f)
