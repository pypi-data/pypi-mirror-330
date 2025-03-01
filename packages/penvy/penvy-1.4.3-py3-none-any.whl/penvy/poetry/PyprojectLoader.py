from typing import Dict
from penvy.poetry import config_reader


class PyprojectLoader:
    def __init__(
        self,
        pyproject_path: str,
    ):
        self._pyproject_path = pyproject_path

    def load(self) -> Dict:
        return config_reader.read(self._pyproject_path)
