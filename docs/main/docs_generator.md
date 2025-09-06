# DocsGenerator

Automated documentation generator that synchronizes project documentation with code changes using LLMs. The system analyzes git diffs and updates documentation files according to predefined templates and rulesets.

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Common Scenarios](#common-scenarios)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Overview
DocsGenerator automatically maintains up-to-date documentation by analyzing code changes in the repository and updating relevant documentation files. It uses a Large Language Model (LLM) to interpret git diffs and apply appropriate updates to documentation based on template structures.

The system consists of several components:
- **DocsManager**: Handles document creation, reading, and organization
- **GitTracker**: Tracks code changes between commits
- **Llm**: Uses language models to determine necessary documentation changes
- **Config**: Manages configuration settings

## Getting Started
### Prerequisites
- Python 3.10+
- Git repository with tracked changes
- Environment variables configured (see Configuration section)
- Access to a supported LLM provider (Cerebras, Ollama)

### Installation/Setup
1. Install dependencies: `pip install pydantic gitpython requests`
2. Set required environment variables
3. Create documentation and templates directories
4. Initialize with proper folder structure

### Quick Example
```python
from main.docs_generator import DocsGenerator
from main.docs_manager import DocsManager
from main.git_tracker import GitTracker
from main.llm.llm import Llm
from main.llm.cerebras import CerebrasLlm
from main.config import Config

docs_manager = DocsManager()
gitapi = GitTracker()
llm = Llm(CerebrasLlm())
config = Config()
docs_generator = DocsGenerator(docs_manager, gitapi, llm, config)
docs_generator.update_docs()
```

## API Reference
### Endpoints/Methods

#### update_docs
- **Description**: Analyzes recent code changes and updates all affected documentation files
- **Parameters**: None
- **Returns**: None
- **Exceptions**: Raises Exception if template is not found for a document
- **Example**: `docs_generator.update_docs()`

#### get_files_to_change
- **Description**: Determines which documentation files need to be created, updated, or deleted based on code changes
- **Parameters**: 
  - `ruleset`: String containing documentation rules
  - `request`: String describing what changes to look for
  - `diff`: Git diff between last sync and current head
  - `templates_list`: List of available template names
  - `existing_files`: JSON string of current documentation files
- **Returns**: DocumentsToChangeList object mapping file paths to actions (create, update, delete)
- **Example**: `llm.get_files_to_change(ruleset, request, diff, templates_list, existing_files)`

#### update_document
- **Description**: Generates specific updates for a single documentation file
- **Parameters**:
  - `ruleset`: Documentation rules
  - `request`: Update request instructions
  - `document`: Document object to update
  - `template`: Template object for the document
  - `diff`: Relevant code changes
  - `language`: Language for documentation output
- **Returns**: DocumentChangeList containing line ranges and new content
- **Example**: `llm.update_document(ruleset, request, document, template, diff, "en")`

## Usage Examples
### Basic Documentation Update
```python
# Initialize components
docs_manager = DocsManager()
gitapi = GitTracker()
llm = Llm(CerebrasLlm())
config = Config()

docs_generator = DocsGenerator(docs_manager, gitapi, llm, config)

docs_generator.update_docs()
```

### Custom LLM Integration
```python
# Using Ollama instead of Cerebras
from main.llm.ollama import OllamaLLM

llm = Llm(OllamaLLM())
docs_generator = DocsGenerator(docs_manager, gitapi, llm, config)
docs_generator.update_docs()
```

## Common Scenarios
### Adding New Documentation for New Files
When new code files are added to the project:
1. GitTracker detects the new files in the diff
2. LLM determines appropriate documentation files to create
3. DocsManager creates new documents using specified templates
4. Documentation is generated and saved

### Updating API Documentation After Endpoint Changes
When API endpoints are modified:
1. Git diff shows changes to endpoint implementations
2. LLM identifies affected documentation files
3. Specific sections of documentation are updated to reflect changes
4. Changes are applied and documentation is saved

## Configuration
Required environment variables:
- `DOCS_DIR`: Path to documentation directory
- `TEMPLATES_DIR`: Path to templates directory
- `REPO_PATH`: Path to the git repository
- `TRACK_PATHS`: Colon-separated paths to track for changes
- `CONFIG_DIR`: Path to configuration files directory
- `LANGUAGE`: Language code for documentation output (e.g., "en")
- `CEREBRAS_API_KEY`: API key for Cerebras LLM (if used)
- `OLLAMA_MODEL`: Model name for Ollama (if used)
- `OLLAMA_URL`: URL for Ollama server (if used)
- `WIKI_TOKEN`: OAuth token for Yandex Wiki integration
- `WIKI_PUBLIC_API`: Public API endpoint for Yandex Wiki
- `ORG_ID`: Organization ID for Yandex Wiki

## Troubleshooting
### Template Not Found
**Issue**: `Exception` raised during document update
**Solution**: Ensure all templates used in documentation exist in the TEMPLATES_DIR and are properly named

### Missing Environment Variables
**Issue**: `KeyError` when accessing environment variables
**Solution**: Verify all required environment variables are set before running the generator

### Git Repository Access Issues
**Issue**: Cannot access repository or read commit history
**Solution**: Ensure REPO_PATH points to a valid git repository with proper read permissions

### LLM API Connection Errors
**Issue**: Failed requests to LLM provider
**Solution**: Check API key validity and network connectivity to the LLM service