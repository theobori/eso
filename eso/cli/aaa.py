"""The aaa CLI module."""

from typing import NoReturn

from eso import AAA
from eso.cli._helper import cli_generic


def cli_aaa() -> NoReturn:
    """Function supposed to be used when creating Python executable scripts."""

    cli_generic(AAA)
