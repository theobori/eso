"""The Roadrunner CLI module."""

from typing import NoReturn

from eso import Roadrunner
from eso.cli._helper import cli_generic


def cli_roadrunner() -> NoReturn:
    """Function supposed to be used when creating Python executable scripts."""

    cli_generic(Roadrunner)
