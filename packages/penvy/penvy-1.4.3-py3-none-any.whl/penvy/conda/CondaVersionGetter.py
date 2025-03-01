import re
from penvy.shell.runner import run_and_read_line


class CondaVersionGetter:
    def __init__(self, conda_executable_path: str):
        self._conda_executable_path = conda_executable_path

    def get(self):
        first_line = run_and_read_line(f"{self._conda_executable_path} --version", shell=True)

        return re.sub(r"^conda ([\d.]+).*$", "\\1", first_line)
