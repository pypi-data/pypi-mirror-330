import os
import re
import urllib.request
import tempfile
from distutils.version import StrictVersion
from logging import Logger
from shutil import which
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.shell.runner import run_with_live_output, run_and_read_line
from penvy.string.random_string_generator import generate_random_string


class PoetryInstaller(SetupStepInterface):
    def __init__(
        self,
        conda_executable_path: str,
        poetry_executable_path: str,
        install_version: str,
        poetry_home: str,
        logger: Logger,
    ):
        self._conda_executable_path = conda_executable_path
        self._poetry_executable_path = poetry_executable_path
        self._install_version = install_version
        self._poetry_home = poetry_home
        self._logger = logger

    def get_description(self):
        return f"Install poetry {self._install_version}"

    def run(self):
        self._logger.info("Installing Poetry globally")

        tmp_dir = tempfile.gettempdir()
        target_file_name = tmp_dir + f"/install-poetry_{generate_random_string(5)}.py"

        url = "https://install.python-poetry.org"
        urllib.request.urlretrieve(url, target_file_name)

        cmd_parts = [self._conda_executable_path, "run", "-n", "base", "python", target_file_name, "-y"]

        install_poetry_env_vars = {
            "POETRY_HOME": self._poetry_home,
            "POETRY_VERSION": self._install_version,
        }

        run_with_live_output(" ".join(cmd_parts), env={**os.environ, **install_poetry_env_vars}, shell=True)

    def should_be_run(self) -> bool:
        return which("poetry") is None

    def _poetry_installed(self):
        return os.path.isfile(self._poetry_executable_path)

    def _poetry_up_to_date(self):
        current_version = self._get_poetry_version()

        return StrictVersion(current_version) >= StrictVersion(self._install_version)

    def _get_poetry_version(self):
        version_cmd_output = run_and_read_line(f"{self._poetry_executable_path} --version", shell=True)

        match = re.match(r"^Poetry \(?version (\w+\.\w+\.\w+)\)?$", version_cmd_output)

        if not match:
            raise Exception(f"Unable to resolve current poetry version. Try updating poetry manually to {self._install_version}")

        return match.group(1)
