"""
TODO
Integrate with YW. Probably simply replace all the documents with new ones.
"""

from enum import StrEnum, auto
import os
from typing import Any
from docsapi.docsapi import DocsAPIProtocol
import requests


class PageTypeEnum(StrEnum):
    PAGE = auto()
    GRID = auto()
    CLOUD_PAGE = auto()
    WYSIWYG = auto()
    TEMPLATE = auto()


class YandexWiki(DocsAPIProtocol):
    def __init__(self):
        self.oauth_token = os.environ["WIKI_TOKEN"]
        self.public_api = os.environ["WIKI_PUBLIC_API"]
        self.org_id = os.environ["ORG_ID"]

    @property
    def auth_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"OAuth {self.oauth_token}",
            "X-Org-Id": self.org_id,
        }

    @property
    def url(self) -> str:
        return f"{self.public_api}/pages/"

    def create_document(
        self,
        slug: str,
        title: str,
        page_type: PageTypeEnum = PageTypeEnum.PAGE,
    ) -> None:
        body = {
            "page_type": page_type.value,
            "slug": slug,
            "title": title,
            "content": "",
        }
        response = requests.post(self.url, json=body, headers=self.auth_headers)
        response.raise_for_status()

    def get_document_by_path(self, path: str) -> Any:
        params = {"slug": path}
        response = requests.get(self.url, params=params)
        response.raise_for_status()
        return response.json()

    def sync_document_by_id(
        self, document_id: str, content: str, allow_merge=True
    ) -> Any:
        url = self.url + document_id
        body = {"content": content}
        params = {"allow_merge": allow_merge}
        response = requests.post(url, json=body, params=params)
        response.raise_for_status()
        return response.json()

    def sync_document_by_path(self, path: str, content: str) -> Any:
        document_id = self.get_document_by_path(path).id
        updated_document = self.sync_document_by_id(document_id, content)
        return updated_document
