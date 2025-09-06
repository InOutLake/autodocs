from docsapi.docsapi import DocsAPIProtocol
from documents.Document import Document
from documents.docs_generator import DocsGenerator
from main.documents.docs_manager import DocsManager
from main.llm.llm import Llm
from git_tracker import GitTracker
from main.documents.docs_synchronizer import DocsSync


class DocsOrchestrator:
    def __init__(
        self,
        llm: Llm,
        gitapi: GitTracker,
        docs_manager: DocsManager,
        docs_api: DocsAPIProtocol,
    ):
        self.gitapi = gitapi
        self.docs_manager = docs_manager
        self.docs_generator = DocsGenerator(docs_manager, llm)
        self.docs_synchronizer = DocsSync(docs_api, docs_manager)

    def update_docs(
        self, commit_hash: str | None = None, custom_request: str | None = None
    ) -> list[Document]:
        self.gitapi.switch_to_new()
        diff = self.gitapi.commit_to_head_changes(commit_hash)
        documents = self.docs_manager.list_documents()
        self.docs_generator.update_docs(
            documents,
            diff,
            custom_request,
        )
        return documents

    def save(self, documents: list[Document]):
        

    def sync_docs(self):
        self.docs_synchronizer.sync_documents()
