from pathlib import Path
from argparse import Namespace
from penvy.parameters.ParametersResolverInterface import ParametersResolverInterface


class PoetryHomeResolver(ParametersResolverInterface):
    def resolve(self, config: dict, cli_args: Namespace):
        return {
            "poetry": {"home": str(Path(config["poetry"]["home"]).expanduser())},
        }
