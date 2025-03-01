import os
from penvy.libroot import get_libroot


def load_possible_executable_paths():
    file_path = f"{get_libroot()}/conda/conda_executable_paths.txt"
    homedir = os.path.expanduser("~")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

        return [line.replace("~", homedir) for line in lines]
