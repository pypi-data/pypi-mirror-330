import platform
from pathlib import Path
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface


class PoetryBinWindowsPathAppender(SetupStepInterface):
    def __init__(self, poetry_home: str, logger: Logger):
        self._poetry_home = poetry_home
        self._poetry_bin = str(Path(poetry_home).joinpath("bin"))
        self._logger = logger

    def run(self):
        self._logger.info("Adding Poetry to PATH (modifying Windows user PATH)")

        self._update_windows_path()

        self._logger.info("You might need to restart shell for updated path to take effect")

    def get_description(self):
        return "Add Poetry to PATH (modifying Windows user PATH)"

    def should_be_run(self) -> bool:
        return platform.system() == "Windows" and self._poetry_bin not in self._get_windows_path()

    def _update_windows_path(self):
        updated_path = self._get_windows_path() + ";" + self._poetry_bin

        self._set_windows_path(updated_path)

    def _get_windows_path(self) -> str:
        # Can't be imported on unix platforms
        # pylint: disable=import-error,import-outside-toplevel
        import winreg

        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root:
            with winreg.OpenKey(root, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                path, _ = winreg.QueryValueEx(key, "PATH")

                return path

    def _set_windows_path(self, path: str):
        # Can't be imported on unix platforms
        # pylint: disable=import-error,import-outside-toplevel
        import winreg

        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root:
            with winreg.OpenKey(root, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, path)
