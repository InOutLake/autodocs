from pathlib import Path
from typing import Any
import copy


class Document:
    # TODO: It is uclear whether document represents existing file or not. But it basicaly is a buffer.
    # I might create it on init if it does not exist, but how do I handle template field then? Also I may move docs manager logic to Document classmethods
    # TODO: refactor Document class -- it is only a buffer to be written.
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
    def new(cls, path: Path, docs_folder: Path, template: str):
        document = cls(path, docs_folder)
        document.template = template
        document.lines[0] = f"<<{template}>>\n"
        return document

    @property
    def content(self):
        return "\n".join(self.lines)

    def read(self):
        self.lines = self.absolute_path.read_text().splitlines()
        return self.lines

    def save(self):
        if not self.absolute_path.exists():
            self.absolute_path.parent.mkdir(parents=True, exist_ok=True)
            self.absolute_path.touch(exist_ok=False)
        self.absolute_path.write_text(self.content, "utf-8")

    def normalize(self) -> None:
        buffer_lines = copy.copy(self.lines)
        for line in self.lines:
            splitlines = line.splitlines()
            for subline in splitlines:
                buffer_lines.append(subline)
        self.lines = buffer_lines

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

    def change_line(self, number: int, content: str) -> None:
        while len(self.lines) < number + 1:
            self.lines.append("")
        self.lines[number] = content
        self.normalize()

    def change_lines(self, changes: dict[int, str]) -> None:
        for line, content in changes.items():
            self.change_line(line, content)

    def edit(self, changes: str):
        self.lines = changes.splitlines()


class Template(Document): ...
