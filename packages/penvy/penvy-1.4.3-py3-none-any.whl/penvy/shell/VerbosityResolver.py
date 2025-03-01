from argparse import Namespace
from penvy.parameters.ParametersResolverInterface import ParametersResolverInterface


class VerbosityResolver(ParametersResolverInterface):
    def resolve(self, config: dict, cli_args: Namespace):
        return {
            "shell": {
                "verbose_output_enabled": cli_args.verbose,
            }
        }
