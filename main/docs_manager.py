from functools import cache
import os
from pathlib import Path
from typing import Any


class Document:
    # TODO: It is uclear whether document represents existing file or not.
    # I might create it on init if it does not exist, but how do I handle template field then?
    # Also I may move docs manager logic to Document classmethods
    def __init__(self, path: Path, docs_folder: Path):
        self.absolute_path = docs_folder / path
        self.path = self.absolute_path.relative_to(docs_folder)
        self.lines = []
        self.template = ""

    @classmethod
    def from_path(cls, path: Path, docs_folder: Path) -> "Document":
        document = cls(path, docs_folder)
        if document.absolute_path.exists():
            document.lines = path.read_text().split("\n")
        else:
            raise FileNotFoundError()
        document.template = document.lines[0].replace("<", "").replace(">", "")
        return document

    @classmethod
    def create(cls, path: Path, docs_folder: Path, template: str) -> "Document":
        document = cls(path, docs_folder)
        document.template = template
        document.absolute_path.parent.mkdir(parents=True, exist_ok=True)
        document.absolute_path.touch(exist_ok=False)
        document.absolute_path.write_text(f"<<{template}>>\n")
        document.lines = document.absolute_path.read_text()
        document.template = template
        return document

    @property
    def content(self):
        return "\n".join(self.lines)

    def save(self):
        self.absolute_path.write_text(self.content, "utf-8")
        self.lines = self.absolute_path.read_text().split("\n")

    def delete(self):
        self.absolute_path.unlink()

    def read(self):
        self.lines = self.absolute_path.read_text().split("\n")
        return self.lines

    def to_dict(self, fields: list[str] | None = None) -> dict[str, Any]:
        all_fields = {
            "path": str(self.path),
            "content": self.lines,
            "template": self.template,
            "exists": self.path.absolute().exists(),
        }

        if fields is None:
            return all_fields

        return {field: all_fields[field] for field in fields if field in all_fields}

    def numbered_content(self):
        result = []
        for i, line in enumerate(self.lines):
            result.append(f"{i:>4d}|{line}")


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
