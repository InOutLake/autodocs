"""
TODO
- Get branch changes compared to the last docs sync commit.
- Sync commit must be stored in a file.
"""

import os
import git
from pathlib import Path


class GitTracker:
    def __init__(self):
        self.last_commit_file = Path(os.environ["LAST_COMMIT_FILE"])
        self.repo = git.Repo(Path("__file__").parent)

    @property
    def last_sync_commit(self):
        with open(self.last_commit_file, "r") as f:
            return f.readline()

    @last_sync_commit.setter
    def last_sync_commit(self, value: str):
        with open(self.last_commit_file, "w") as f:
            f.seek(0)
            f.write(value)

    def generate_change_log(self):
        return
