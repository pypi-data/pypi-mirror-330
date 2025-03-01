from typing import Dict
from pathlib import Path
from penvy import toml


def read(path: str) -> Dict:
    allowed_files = ["pyproject.toml", "poetry.lock"]

    if Path(path).name not in allowed_files:
        raise Exception(f"Invalid file, allowed files are {allowed_files}")

    with open(path, mode="r", encoding="utf-8") as f:
        return toml.loads(f.read())
