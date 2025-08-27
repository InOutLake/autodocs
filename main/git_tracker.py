import datetime
import os
import git
from pathlib import Path
import json


# TODO: refactor. Make more general, figure out function I do need to implement side branch documentation update logic
class GitTracker:
    def __init__(self):
        self.last_commit_file = Path(__file__).parent / "data" / "last_commit.txt"
        self.repo = git.Repo(Path(os.environ["REPO_PATH"]))
        self.paths: list[Path] = [Path(p) for p in os.environ["TRACK_PATHS"].split(":")]

    @property
    def last_sync_commit(self) -> str:
        return json.loads(self.last_commit_file.read_text())["hash"]

    @last_sync_commit.setter
    def last_sync_commit(self, value: str) -> None:
        self.last_commit_file.write_text(
            json.dumps({"timestamp": datetime.datetime.now(), "hash": value})
        )

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

    def commit_to_head_changes(self, commit_hash: str | None = None) -> str:
        if commit_hash is None:
            commit_hash = self.last_sync_commit
        return self.generate_change_log(
            commit_hash,
            self.repo.head.commit.hexsha,
        )

    def create_branch(self, branch_name: str | None = None) -> git.Head:
        active_branch = self.repo.active_branch
        if branch_name is None:
            branch_name = f"[docs]/{str(active_branch.name)}"
        return self.repo.create_head(branch_name, active_branch.name)
