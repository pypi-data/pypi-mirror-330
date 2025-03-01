import os
from logging import Logger
from pathlib import Path
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.shell.home_path_shortener import shorten_home_path


class ShellFileCreator(SetupStepInterface):
    def __init__(
        self,
        file_path: str,
        expected_shell_is_running: callable,
        logger: Logger,
    ):
        self._file_path = file_path
        self._file_path_shorten = shorten_home_path(file_path)
        self._expected_shell_is_running = expected_shell_is_running
        self._logger = logger

    def get_description(self):
        return f"Create {self._file_path_shorten}"

    def run(self):
        self._logger.info(f"Creating {self._file_path_shorten}")

        Path(self._file_path).touch()

    def should_be_run(self) -> bool:
        return self._expected_shell_is_running and not os.path.isfile(self._file_path)
