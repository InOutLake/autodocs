import os
from pathlib import Path


class TaskRequests:
    def __init__(self):
        config_dir = Path(os.environ["CONFIG_DIR"])
        self.config = {f.stem: f.read_text() for f in config_dir.iterdir()}

    def __getitem__(self, item: str):
        return self.config[item]
