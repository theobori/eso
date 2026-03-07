"""The Lazyfuck CLI module."""

from typing import NoReturn

from eso import Lazyfuck
from eso.cli._helper import cli_generic


def cli_lazyfuck() -> NoReturn:
    """Function supposed to be used when creating Python executable scripts."""

    cli_generic(Lazyfuck)
