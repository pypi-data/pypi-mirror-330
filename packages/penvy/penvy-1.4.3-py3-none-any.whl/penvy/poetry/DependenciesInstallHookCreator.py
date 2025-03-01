import os
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.shell.home_path_shortener import shorten_home_path
from penvy.string.string_in_file import file_contains_string


class DependenciesInstallHookCreator(SetupStepInterface):
    def __init__(
        self,
        post_merge_hook_path: str,
        conda_executable_path: str,
        venv_dir: str,
        poetry_executable_path: str,
        logger: Logger,
    ):
        self._post_merge_hook_path = post_merge_hook_path
        self._conda_executable_path = conda_executable_path
        self._venv_dir = venv_dir
        self._poetry_executable_path = poetry_executable_path
        self._logger = logger

    def get_description(self):
        return "Create git-hook to automatically install new project dependencies after git pull/merge"

    def run(self):
        self._logger.info("Adding poetry install to post-merge git hook")

        cmd_parts = [
            shorten_home_path(self._conda_executable_path),
            "run",
            "-p",
            shorten_home_path(self._venv_dir),
            "python",
            shorten_home_path(self._poetry_executable_path),
            "install",
            "--no-root",
        ]

        with open(self._post_merge_hook_path, "a", encoding="utf-8") as f:
            f.write(" ".join(cmd_parts) + "\n")

    def should_be_run(self) -> bool:
        return os.path.isdir(os.path.dirname(self._post_merge_hook_path)) and (
            not os.path.isfile(self._post_merge_hook_path)
            or not file_contains_string("poetry install --no-root", self._post_merge_hook_path)
        )
