from docsapi.docsapi import DocsAPIProtocol
from documents.docs_manager import DocsManager, Document


class DocsSync:
    def __init__(self, docsapi: DocsAPIProtocol, docs_manager: DocsManager):
        self.docsapi = docsapi
        # Using docs manager instead of simple Document interfaces to make sure
        # only existing saved files are being synced
        self.docs_manager = docs_manager

    def sync_document(self, document: Document) -> None:
        updated_content = self.docsapi.sync_document_by_path(
            str(document.path),
            document.content,
        )
        document.edit(updated_content)
        document.save()

    def sync_documents(self, documents: list[Document] | None = None) -> None:
        if documents is None:
            documents = self.docs_manager.list_documents()
        for doc in documents:
            self.sync_document(doc)
