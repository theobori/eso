"""The brainz CLI module."""

from typing import NoReturn

from eso import Brainz
from eso.cli._helper import cli_generic


def cli_brainz() -> NoReturn:
    """Function supposed to be used when creating Python executable scripts."""

    cli_generic(Brainz, "rb")
