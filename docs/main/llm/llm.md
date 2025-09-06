# LLM Module

Brief description of what this service/module does and its main purpose. The LLM module orchestrates documentation updates by leveraging large language models to analyze code changes and modify documentation files accordingly. It integrates with version control, documentation storage, and external LLM APIs to automate the maintenance of accurate, up-to-date technical documentation.

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Common Scenarios](#common-scenarios)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Overview
The LLM module acts as an intelligent automation layer for documentation management. It uses a pluggable LLM agent (e.g., Cerebras, Ollama) to interpret git diffs, determine which documentation files need creation, update, or deletion, and generate precise content changes in structured JSON format. This enables fully automated, context-aware documentation synchronization across projects.

## Getting Started
### Prerequisites
- Python 3.10+
- Git repository with tracked changes
- Environment variables configured (see Configuration section)
- Access to an LLM provider (Cerebras, Ollama, etc.)

### Installation/Setup
1. Install dependencies: `pip install pydantic requests gitpython`
2. Set required environment variables
3. Ensure documentation and templates directories exist and are populated
4. Run the main script: `python main.py`

### Quick Example
```python
from main.docs_generator import DocsGenerator
from main.docs_manager import DocsManager
from main.git_tracker import GitTracker
from main.llm.cerebras import CerebrasLlm
from main.llm.llm import Llm
from main.config import Config

llm_agent = CerebrasLlm()
llm = Llm(llm_agent)
docs_manager = DocsManager()
gitapi = GitTracker()
config = Config()

docs_generator = DocsGenerator(docs_manager, gitapi, llm, config)
docs_generator.update_docs()
```

## API Reference
### Endpoints/Methods

#### get_files_to_change
- **Description**: Determines which documentation files should be created, updated, or deleted based on recent code changes and current documentation state
- **Parameters**: 
  - `ruleset`: (str) Guidelines for documentation changes
  - `request`: (str) Instruction prompt for the LLM
  - `diff`: (str) JSON-formatted git diff between last sync and current HEAD
  - `templates_list`: (list[str]) Available template types for new documents
  - `existing_files`: (str) JSON list of current documentation files and their metadata
- **Returns**: `DocumentsToChangeList` - A dictionary mapping file paths to actions (`create`, `update`, `delete`)
- **Exceptions**: May raise if LLM response is malformed or cannot be parsed
- **Example**: See Quick Example above

#### update_document
- **Description**: Generates specific line-level changes for a given documentation file based on code diffs and template
- **Parameters**:
  - `ruleset`: (str) Guidelines for documentation changes
  - `request`: (str) Instruction prompt for the LLM
  - `document`: (Document) Current document to update
  - `template`: (Template) Template used to guide formatting
  - `diff`: (str) JSON-formatted git diff
  - `language`: (str) Language in which to write the documentation
- **Returns**: `DocumentChangeList` - List of changes with line ranges and new content
- **Exceptions**: May raise if LLM response is malformed
- **Example**: See Quick Example above

## Usage Examples
Automatically update API documentation after adding a new endpoint:

1. Code change introduces new `/v2/adjust_position` endpoint
2. `get_files_to_change` identifies `api.md` needs update
3. `update_document` returns:
```json
[{
  "line_start": 4,
  "line_end": 7,
  "content": "## GET /v2/adjust_position\nAdjusts position of an object\nV2 has additional fields:"
}]
```
4. System applies changes to `api.md`

## Common Scenarios
### Updating API Documentation
When API endpoints change:
1. Ensure `TRACK_PATHS` includes API implementation files
2. Run `docs_generator.update_docs()`
3. LLM detects change and updates corresponding API documentation
4. Changes are printed and can be reviewed before finalization

### Creating New Guide Files
When new features are added:
1. LLM determines new guide is needed (e.g., `userguide.md`)
2. `get_files_to_change` returns action `create` with template type
3. `DocsManager` creates file with proper template header
4. `update_document` populates initial content

## Configuration
Required environment variables:
- `CEREBRAS_API_KEY`: API key for Cerebras LLM service
- `DOCS_DIR`: Path to documentation files directory
- `TEMPLATES_DIR`: Path to templates directory
- `REPO_PATH`: Path to git repository root
- `TRACK_PATHS`: Colon-separated paths to monitor for changes
- `CONFIG_DIR`: Path to configuration files directory
- `LANGUAGE`: Language for generated documentation (e.g., "English")
- `WIKI_TOKEN`, `WIKI_PUBLIC_API`, `ORG_ID`: For Yandex Wiki integration
- `OLLAMA_MODEL`, `OLLAMA_URL`: For Ollama LLM backend

## Troubleshooting
- **LLM API errors**: Verify API keys and network connectivity
- **Missing files**: Ensure `DOCS_DIR` and `TEMPLATES_DIR` paths are correct and accessible
- **No changes detected**: Check that modified files are within `TRACK_PATHS`
- **Parsing errors**: Validate that template files start with `<<template_type>>` tag
- **Git errors**: Confirm repository path is valid and git is initialized