"""The Omam CLI module."""

from typing import NoReturn

from eso import Omam
from eso.cli._helper import cli_generic


def cli_omam() -> NoReturn:
    """Function supposed to be used when creating Python executable scripts."""

    cli_generic(Omam)
