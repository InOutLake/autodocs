from functools import cache
import os
from pathlib import Path
from typing import Any

from docsapi.docsapi import DocsAPIProtocol
from git_tracker import GitTracker


class Document:
    # TODO: It is uclear whether document represents existing file or not.
    # I might create it on init if it does not exist, but how do I handle template field then?
    # Also I may move docs manager logic to Document classmethods
    def __init__(self, path: Path, docs_folder: Path):
        self.absolute_path = docs_folder / path
        self.path = self.absolute_path.relative_to(docs_folder)
        try:
            self.content = path.read_text()
            self.template = (
                self.content.split("\n")[0].replace("<", "").replace(">", "")
            )
        except Exception as _:
            ...

    def create(self, template: str) -> None:
        self.absolute_path.parent.mkdir(parents=True, exist_ok=True)
        self.absolute_path.touch(exist_ok=False)
        self.absolute_path.write_text(f"<<{template}>>")

    def edit(self, new_content: str) -> None:
        self.absolute_path.write_text(new_content)

    def delete(self):
        self.absolute_path.unlink()

    def read(self):
        return self.content

    def to_dict(self, fields: list[str] | None = None) -> dict[str, Any]:
        all_fields = {
            "path": str(self.path),
            "content": self.content,
            "template": self.template,
            "exists": self.path.absolute().exists(),
        }

        if fields is None:
            return all_fields

        return {field: all_fields[field] for field in fields if field in all_fields}


class Template(Document): ...


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
        return [Template(path, self.templates_folder) for path in path_list]

    def get_document(self, document_path: Path) -> Document:
        return Document(document_path, self.docs_folder)

    def create_document(self, document_path: Path, template: str) -> Document:
        document = Document(document_path, self.docs_folder)
        document.create(template)
        return document

    def edit_document(self, document_path: Path, content: str) -> Document:
        document = Document(document_path, self.docs_folder)
        document.edit(content)
        return document

    def delete_document(self, document_path: Path):
        document = Document(document_path, self.docs_folder)
        document.delete()
