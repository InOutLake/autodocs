import os
from typing import List, Sequence, cast
import git
from pathlib import Path
import json
from git.types import PathLike


class GitTracker:
    def __init__(self):
        self.last_commit_file = Path(__file__).parent / "data" / "last_commit.txt"
        self.repo = git.Repo(Path(os.environ["REPO_PATH"]))
        self.paths: List[Path] = [Path(p) for p in os.environ["TRACK_PATHS"].split(":")]

    @property
    def last_sync_commit(self):
        return self.last_commit_file.read_text()

    @last_sync_commit.setter
    def last_sync_commit(self, value: str):
        with open(self.last_commit_file, "w") as f:
            f.seek(0)
            f.write(value)

    def generate_change_log(self, a_commit: str, b_commit: str) -> str:
        diff = self.repo.commit(a_commit).diff(
            b_commit,
            create_patch=True,
            paths=self.paths,  # type: ignore
        )
        diff_json = {}

        for change in diff:
            if isinstance(change.diff, bytes):
                diff_content = change.diff.decode()
            else:
                diff_content = str(change.diff)
            diff_json[change.b_path] = {
                "diff": diff_content,
            }
        return json.dumps(diff_json, indent=2)

    def last_sync_to_head_changes(self) -> str:
        return self.generate_change_log(
            self.last_sync_commit,
            self.repo.head.commit.hexsha,
        )
