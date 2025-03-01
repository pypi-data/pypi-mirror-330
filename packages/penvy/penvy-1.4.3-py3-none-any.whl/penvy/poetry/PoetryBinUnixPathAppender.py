import os
import platform
from pathlib import Path
from logging import Logger
from penvy.string.string_in_file import file_contains_string
from penvy.setup.SetupStepInterface import SetupStepInterface


class PoetryBinUnixPathAppender(SetupStepInterface):
    def __init__(self, poetry_home: str, profile_path: str, expected_shell_is_running: callable, logger: Logger):
        self._poetry_home = poetry_home
        self._poetry_bin = str(Path(poetry_home).joinpath("bin"))
        self._profile_path = profile_path
        self._expected_shell_is_running = expected_shell_is_running
        self._logger = logger

    def run(self):
        self._logger.info(f'Adding Poetry to PATH (add "{self._get_path_modifying_command()}" into {self._profile_path})')

        self._update_unix_path()

        self._logger.info("You might need to logout and login for updated path to take effect")

    def get_description(self):
        return f'Add Poetry to PATH (add "{self._get_path_modifying_command()}" into {self._profile_path})'

    def should_be_run(self) -> bool:
        return (
            platform.system() != "Windows"
            and self._expected_shell_is_running
            and (not os.path.isfile(self._profile_path) or not file_contains_string(self._get_path_modifying_command(), self._profile_path))
        )

    def _update_unix_path(self):
        with open(self._profile_path, mode="a", encoding="utf-8") as f:
            f.write(f"\n{self._get_path_modifying_command()}\n")

    def _get_path_modifying_command(self) -> str:
        return f"export PATH=$PATH:{self._poetry_bin}"
