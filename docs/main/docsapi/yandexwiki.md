# YandexWiki Integration

Brief description of what this service/module does and its main purpose. This module enables synchronization of local documentation with Yandex Wiki, allowing automated updates to wiki pages based on code changes and documentation generation workflows.

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Common Scenarios](#common-scenarios)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Overview
High-level explanation of the service/module functionality and how it fits into the larger system. The `YandexWiki` class implements the `DocsAPIProtocol` to interact with the Yandex Wiki API, enabling creation, retrieval, and synchronization of documentation pages. It is used by the documentation generation pipeline to keep remote wiki pages up to date with the latest changes in the codebase.

## Getting Started
### Prerequisites
List any requirements or dependencies.
- Yandex organization account with API access
- OAuth token for Yandex Wiki API
- Environment variables configured: `WIKI_TOKEN`, `WIKI_PUBLIC_API`, `ORG_ID`

### Installation/Setup
Basic steps to get started using this service.
1. Set up environment variables for authentication and API endpoints
2. Ensure your local documentation files are properly formatted with template tags (e.g., `<<userguide>>`)
3. Run the documentation generator: `python main.py`

### Quick Example
Simple code example showing basic usage.
```python
from main.docsapi.yandexwiki import YandexWiki

wiki = YandexWiki()
wiki.create_document(slug="api-docs", title="API Documentation", page_type=PageTypeEnum.PAGE)
```

## API Reference
### Endpoints/Methods
Detailed documentation of all public APIs, methods, or interfaces.

#### create_document
- **Description**: Creates a new document/page in Yandex Wiki
- **Parameters**: 
  - `slug`: Unique identifier for the page URL
  - `title`: Display title of the page
  - `page_type`: Type of page to create (default: PageTypeEnum.PAGE)
- **Returns**: None
- **Exceptions**: Raises HTTPError if request fails
- **Example**: 
  ```python
  wiki.create_document(slug="getting-started", title="Getting Started", page_type=PageTypeEnum.PAGE)
  ```

#### get_document_by_path
- **Description**: Retrieves a document from Yandex Wiki by its slug/path
- **Parameters**: 
  - `path`: The slug/identifier of the page to retrieve
- **Returns**: JSON response containing document data
- **Exceptions**: Raises HTTPError if request fails
- **Example**: 
  ```python
  doc = wiki.get_document_by_path("api-docs")
  print(doc["title"])
  ```

#### sync_document_by_path
- **Description**: Updates an existing document in Yandex Wiki with new content
- **Parameters**: 
  - `path`: The slug/identifier of the page to update
  - `content`: New content to apply to the page
- **Returns**: Updated document data from API
- **Exceptions**: Raises HTTPError if request fails or if document does not exist
- **Example**: 
  ```python
  updated = wiki.sync_document_by_path("api-docs", "# New Content\nUpdated documentation here.")
  ```

## Usage Examples
Practical examples showing common use cases.

Syncing local documentation to Yandex Wiki:
```python
from main.docsapi.yandexwiki import YandexWiki
from main.docs_manager import DocsManager

docs_manager = DocsManager()
doc = docs_manager.get_document("api.md")

wiki = YandexWiki()
wiki.sync_document_by_path(str(doc.path), "\n".join(doc.lines))
```

## Common Scenarios
Step-by-step guides for typical workflows.

### Automated Documentation Deployment
1. Code changes are committed to the repository
2. CI/CD pipeline runs `main.py`
3. `DocsGenerator` analyzes git diff and determines which docs need updating
4. `YandexWiki` syncs updated documentation to the remote wiki

### Creating New Documentation Pages
1. Add a new `.md` file in the `docs/` directory with appropriate template tag
2. Run the documentation generator
3. The system automatically creates a corresponding page in Yandex Wiki

## Configuration
Available configuration options and their effects.
- `WIKI_TOKEN`: OAuth token for authenticating with Yandex Wiki API
- `WIKI_PUBLIC_API`: Base URL for Yandex Wiki API
- `ORG_ID`: Organization ID for Yandex Workspace

These must be set as environment variables.

## Troubleshooting
Common issues and their solutions.

- **Issue**: `HTTP 401 Unauthorized` when syncing documents
  - **Solution**: Verify that `WIKI_TOKEN` is correctly set and has sufficient permissions

- **Issue**: Document not found when trying to update
  - **Solution**: Ensure the document exists in Yandex Wiki or create it first using `create_document`

- **Issue**: `HTTP 400 Bad Request` during page creation
  - **Solution**: Check that `slug` contains only allowed characters and is unique