import platform
from pathlib import Path
from argparse import Namespace
from penvy.parameters.ParametersResolverInterface import ParametersResolverInterface


class PoetryPathResolver(ParametersResolverInterface):
    def resolve(self, config: dict, cli_args: Namespace):
        poetry_executable = "poetry.exe" if platform.system() == "Windows" else "poetry"
        poetry_home = Path(config["poetry"]["home"]).expanduser()

        return {
            "poetry": {"executable_path": str(poetry_home.joinpath("bin").joinpath(poetry_executable))},
        }
