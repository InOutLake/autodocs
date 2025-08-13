from functools import cache
import os
from pathlib import Path

from docsapi.docsapi import DocsAPIProtocol
from git_tracker import GitTracker


class Document:
    def __init__(self, path: Path, docs_folder: Path):
        self.path = path.relative_to(docs_folder)
        try:
            self.content = path.read_text()
            self.template = (
                self.content.split("\n")[0].replace("<", "").replace(">", "")
            )
        except Exception as _:
            ...

    def create(self, template: str) -> None:
        self.path.touch(exist_ok=False)
        self.path.write_text(f"<<{template}>>")

    def edit(self, new_content: str) -> None:
        self.path.write_text(new_content)

    def delete(self):
        self.path.unlink()

    def read(self):
        return self.content


class Template(Document): ...


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

    def list_documents(self) -> list[Document]:
        paths_list = self.list_folder(self.docs_folder)
        return [Document(path, self.docs_folder) for path in paths_list]

    def sync_document(self, document: Document) -> None:
        updated_content = self.docsapi.sync_document_by_path(
            str(document.path),
            content=document.read(),
        )
        document.edit(updated_content)

    def sync_documents(self) -> None:
        documents = self.list_documents()
        for doc in documents:
            self.sync_document(doc)

    @cache
    def list_templates(self) -> list[Template]:
        path_list = self.list_folder(self.templates_folder)
        return [Template(path, self.templates_folder) for path in path_list]

    def create_document(self, document_path: Path, document_template: str):
        document_path.write_text(f"<<{document_template}>>")

    def edit_document(self, document_path: Path, content: str):
        document_path.write_text(content)

    def delete_document(self, document_path: Path):
        document_path.unlink()
