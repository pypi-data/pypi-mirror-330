from distutils.version import StrictVersion
from logging import Logger
from penvy.check.CheckInterface import CheckInterface
from penvy.conda.CondaVersionGetter import CondaVersionGetter


class CondaVersionCheck(CheckInterface):
    def __init__(
        self,
        conda_executable_path: str,
        minimal_version: str,
        conda_version_getter: CondaVersionGetter,
        logger: Logger,
    ):
        self._conda_executable_path = conda_executable_path
        self._minimal_version = minimal_version
        self._conda_version_getter = conda_version_getter
        self._logger = logger

    # pylint: disable=inconsistent-return-statements
    def run(self):
        self._logger.debug(f"Using conda executable: {self._conda_executable_path}")

        conda_version = self._conda_version_getter.get()

        if StrictVersion(conda_version) < StrictVersion(self._minimal_version):
            return f"Conda version {conda_version} is too old, please update to {self._minimal_version} or higher"

        self._logger.debug(f"Conda version {conda_version} ok")
