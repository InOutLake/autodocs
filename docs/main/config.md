# Config Module

Brief description of what this service/module does and its main purpose. The `Config` module loads configuration files from a specified directory and provides dictionary-style access to their contents, enabling centralized and environment-driven configuration management for the documentation system.

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Common Scenarios](#common-scenarios)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Overview
The `Config` class reads all text-based configuration files from a directory defined by the `CONFIG_DIR` environment variable. Each file's stem (filename without extension) becomes a key, and its content becomes the value in an in-memory dictionary. This allows components of the system to access configuration rules, prompts, and settings dynamically.

## Getting Started
### Prerequisites
- Set the `CONFIG_DIR` environment variable to point to the directory containing configuration files.
- Configuration files must be plain text files (e.g., `.txt`, `.md`, no binary formats).

### Installation/Setup
Ensure that the `CONFIG_DIR` environment variable is properly set before initializing the `Config` class. Example:

```bash
export CONFIG_DIR="./config/rules"
```

### Quick Example
```python
from main.config import Config

cfg = Config()
print(cfg["ruleset"])  # Prints content of 'ruleset.txt' from CONFIG_DIR
```

## API Reference
### Endpoints/Methods

#### Config.__init__
- **Description**: Initializes the Config instance by loading all configuration files from the `CONFIG_DIR` directory.
- **Parameters**: None (uses `CONFIG_DIR` from environment)
- **Returns**: None
- **Exceptions**: KeyError if `CONFIG_DIR` is not set in environment
- **Example**: `config = Config()`

#### Config.__getitem__
- **Description**: Retrieves the content of a configuration file by its filename stem.
- **Parameters**: 
  - `item` (str): The stem of the configuration file (e.g., 'ruleset' for 'ruleset.txt')
- **Returns**: The full text content of the requested configuration file
- **Exceptions**: KeyError if the requested config key does not exist
- **Example**: `rules = config["ruleset"]`

## Usage Examples
Load and use a configuration rule set for documentation generation:

```python
config = Config()
ruleset = config["ruleset"]
files_to_change_request = config["files_to_change_request"]
```

These values can then be passed to the `Llm` class to determine which documentation files need updates based on code changes.

## Common Scenarios
- Centralizing prompt templates for LLM interactions in `.txt` files for easy editing without code changes.
- Managing different configuration sets for various environments (e.g., dev, prod) by switching `CONFIG_DIR`.

## Configuration
- `CONFIG_DIR`: Environment variable specifying the path to the directory containing configuration files. All files in this directory are loaded at initialization.

## Troubleshooting
- **Error: `KeyError` when accessing config["..."]**
  - Cause: The requested configuration file does not exist in `CONFIG_DIR`.
  - Solution: Verify the filename and ensure it is present in the configured directory.

- **Error: `CONFIG_DIR` not found in environment**
  - Cause: The environment variable is missing.
  - Solution: Set `CONFIG_DIR` before creating a `Config` instance.