"""The DetailedFuck CLI module."""

from typing import NoReturn

from eso import DetailedFuck
from eso.cli._helper import cli_generic


def cli_detailedfuck() -> NoReturn:
    """Function supposed to be used when creating Python executable scripts."""

    cli_generic(DetailedFuck)
