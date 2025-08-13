from docs_manager import DocsManager, Document
from docsapi.docsapi import DocsAPIProtocol


class DocsSync:
    def __init__(
        self,
        docs_manager: DocsManager,
        docsapi: DocsAPIProtocol,
    ):
        self.docs_manager = docs_manager
        self.docsapi = docsapi

    def sync_document(self, document: Document) -> None:
        updated_content = self.docsapi.sync_document_by_path(
            str(document.path),
            content=document.read(),
        )
        document.edit(updated_content)

    def sync_documents(self) -> None:
        documents = self.docs_manager.list_documents()
        for doc in documents:
            self.sync_document(doc)
