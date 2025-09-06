# DocsManager

A module responsible for managing documentation files within a project. It provides functionality to create, read, update, and delete documentation, as well as list available documents and templates. Designed to work with version-controlled projects, it integrates with Git to track changes and synchronize documentation accordingly.
## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Common Scenarios](#common-scenarios)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
## Overview
The `DocsManager` class handles all operations related to documentation files in the project. It works with two main entities: `Document` and `Template`. Each document is associated with a template that defines its structure and type. The module supports creating new documents, retrieving existing ones, updating content, and deleting files. It also provides utilities for listing all documents and templates in the system.
## Getting Started
### Prerequisites
- Environment variable `DOCS_DIR` must be set to the root directory of documentation files
- Environment variable `TEMPLATES_DIR` must point to the directory containing documentation templates
- Python 3.10+ with required dependencies installed
### Installation/Setup
The DocsManager is initialized automatically when imported. Ensure environment variables are properly configured before use:

```bash
export DOCS_DIR="/path/to/docs"
export TEMPLATES_DIR="/path/to/templates"
```
### Quick Example
```python
from main.docs_manager import DocsManager

# Initialize the manager
docs_manager = DocsManager()

# List all documents
documents = docs_manager.list_documents()

# Create a new document with a template
doc = docs_manager.create_document("api/guide.md", "userguide")
```
## API Reference
### Endpoints/Methods
#### list_documents
- **Description**: Returns a list of all Document objects in the documentation directory
- **Parameters**: None
- **Returns**: List[Document] - A list of Document instances representing all documentation files
- **Exceptions**: None
- **Example**: ```python
documents = docs_manager.list_documents()```
#### list_documents_dicts
- **Description**: Returns a list of dictionaries containing document metadata. Can filter by specific fields.
- **Parameters**: 
  - `documents`: Optional list of Document objects to process (defaults to all documents)
  - `fields`: Optional list of field names to include in the output (e.g., ["path", "template"])
- **Returns**: List[dict] - List of dictionaries with document information
- **Exceptions**: None
- **Example**: ```python
# Get all document paths
paths = docs_manager.list_documents_dicts(fields=["path"])```
#### list_templates
- **Description**: Returns a list of all available templates. Results are cached for performance.
- **Parameters**: None
- **Returns**: List[Template] - A list of Template objects available for use
- **Exceptions**: None
- **Example**: ```python
templates = docs_manager.list_templates()```
#### get_document
- **Description**: Retrieves a Document object for a specific file path
- **Parameters**: 
  - `document_path`: Path object or string representing the document path relative to DOCS_DIR
- **Returns**: Document - An instance of the Document class
- **Exceptions**: FileNotFoundError if the document does not exist
- **Example**: ```python
doc = docs_manager.get_document("user/guide.md")```
#### create_document
- **Description**: Creates a new document file with the specified template
- **Parameters**: 
  - `document_path`: Path where the document should be created
  - `template`: String name of the template to use (must match an existing template)
- **Returns**: Document - The newly created Document instance
- **Exceptions**: FileExistsError if the document already exists
- **Example**: ```python
doc = docs_manager.create_document("new/api.md", "userguide")```
#### delete_document
- **Description**: Deletes a document file from the filesystem
- **Parameters**: 
  - `document_path`: Path of the document to delete
- **Returns**: None
- **Exceptions**: FileNotFoundError if the document doesn't exist
- **Example**: ```python
docs_manager.delete_document("outdated/file.md")```
#### edit_document
- **Description**: Loads a document for editing. Note: This method currently only returns the document object; actual content modification requires using Document methods.
- **Parameters**: 
  - `document_path`: Path of the document to edit
  - `content`: String content to write to the document
- **Returns**: Document - The loaded Document instance
- **Exceptions**: FileNotFoundError if the document doesn't exist
- **Example**: ```python
doc = docs_manager.edit_document("guide.md", "updated content")```
## Usage Examples
### Creating Multiple Documents
```python
# Create several documents using different templates
docs_to_create = [
    ("api/v1.md", "api"),
    ("tutorials/basics.md", "tutorial"),
    ("scenarios/payment_flow.md", "scenario")
]

for path, template in docs_to_create:
    docs_manager.create_document(path, template)
```
### Processing All Documents
```python
# Iterate through all documents and perform operations
for doc in docs_manager.list_documents():
    print(f"Processing {doc.path}")
    # Perform updates or analysis
    if "deprecated" in doc.template:
        docs_manager.delete_document(doc.path)
```
## Common Scenarios
### Initializing Documentation Structure
When setting up a new project, use DocsManager to create the initial documentation structure:

```python
docs_manager = DocsManager()

# Create essential documentation files
docs_manager.create_document("README.md", "userguide")
docs_manager.create_document("API.md", "api")
docs_manager.create_document("CONTRIBUTING.md", "contribution")
```
### Migrating Documentation
When updating documentation formats, use the manager to systematically process files:

```python
# Find all documents using old template
all_docs = docs_manager.list_documents_dicts()

for doc_info in all_docs:
    if doc_info["template"] == "legacy_guide":
        # Create new version with updated template
        new_path = doc_info["path"].replace("legacy_", "")
        docs_manager.create_document(new_path, "userguide")
        # Delete old document
        docs_manager.delete_document(doc_info["path"])
```
## Configuration
The DocsManager module uses the following environment variables:

- `DOCS_DIR`: Root directory for documentation files (required)
- `TEMPLATES_DIR`: Directory containing documentation templates (required)

These variables must be set before initializing the DocsManager class.
## Troubleshooting
- **FileNotFoundError when calling get_document**: Ensure the requested document exists in the DOCS_DIR directory
- **FileExistsError when creating document**: The document path already exists; either delete it first or use a different path
- **EnvironmentError on initialization**: Verify that DOCS_DIR and TEMPLATES_DIR environment variables are properly set and point to valid directories
- **Template not found**: Confirm that the template name matches exactly with a file in the TEMPLATES_DIR directory