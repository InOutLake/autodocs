from functools import cache
import os
from pathlib import Path
from typing import Any


class Document:
    # TODO: It is uclear whether document represents existing file or not. But it basicaly is a buffer.
    # I might create it on init if it does not exist, but how do I handle template field then? Also I may move docs manager logic to Document classmethods
    def __init__(self, path: Path, docs_folder: Path):
        self.absolute_path = docs_folder / path
        self.path = self.absolute_path.relative_to(docs_folder)
        self.lines: list[str] = []
        self.template = ""

    @classmethod
    def from_path(cls, path: Path, docs_folder: Path):
        document = cls(path, docs_folder)
        if document.absolute_path.exists():
            document.read()
        else:
            raise FileNotFoundError()
        document.template = document.lines[0].replace("<", "").replace(">", "")
        return document

    @classmethod
    def create(cls, path: Path, docs_folder: Path, template: str):
        document = cls(path, docs_folder)
        document.template = template
        document.absolute_path.parent.mkdir(parents=True, exist_ok=True)
        document.absolute_path.touch(exist_ok=False)
        document.absolute_path.write_text(f"<<{template}>>\n")
        document.lines = document.absolute_path.read_text().splitlines()
        document.template = template
        return document

    @property
    def content(self):
        return "\n".join(self.lines)

    def read(self):
        self.lines = self.absolute_path.read_text().splitlines()
        return self.lines

    def save(self):
        self.absolute_path.write_text(self.content, "utf-8")
        self.lines = self.absolute_path.read_text().splitlines()

    def delete(self):
        self.absolute_path.unlink()

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

    def numbered_content(self) -> str:
        result = []
        for i, line in enumerate(self.lines):
            result.append(f"{i:>4d}|{line}")
        return "\n".join(result)

    def change_line(self, number: int, content: str):
        while len(self.lines) < number + 1:
            self.lines.append("")
        self.lines[number] = content


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
        return [Template.from_path(path, self.templates_folder) for path in path_list]

    def read_document(self, document_path: Path) -> Document:
        return Document.from_path(document_path, self.docs_folder)

    def create_document(self, document_path: Path, template: str) -> Document:
        document = Document.create(document_path, self.docs_folder, template)
        return document

    def edit_document(self, document_path: Path, content: str) -> Document:
        document = Document.from_path(document_path, self.docs_folder)
        return document

    def delete_document(self, document_path: Path):
        document = Document(document_path, self.docs_folder)
        document.delete()
