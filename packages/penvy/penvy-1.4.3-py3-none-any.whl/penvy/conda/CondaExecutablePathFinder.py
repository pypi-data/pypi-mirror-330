import os
import shutil


class CondaExecutablePathFinder:
    def __init__(self, possible_executable_paths: list):
        self._possible_executable_paths = possible_executable_paths

    def find(self):
        if shutil.which("conda"):
            return shutil.which("conda")

        for possible_executable_path in self._possible_executable_paths:
            if os.path.isfile(possible_executable_path):
                return possible_executable_path

        raise Exception("Unable to find Conda executable, exiting...")
