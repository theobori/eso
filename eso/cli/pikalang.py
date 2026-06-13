"""The Pikalang CLI module."""

from typing import NoReturn

from eso import Pikalang
from eso.cli._helper import cli_generic


def cli_pikalang() -> NoReturn | None:
    """Function supposed to be used when creating Python executable scripts."""

    cli_generic(Pikalang)
