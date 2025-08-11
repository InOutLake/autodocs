from typing import Any, Protocol


class DocsAPIProtocol(Protocol):
    def sync_document_by_path(self, path: str, content: str) -> Any: ...
