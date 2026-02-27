"""The Befunge CLI module."""

from typing import NoReturn
from argparse import ArgumentParser
from pathlib import Path

from eso import Befunge
from eso.cli._helper import cli_esolang_run


def cli_befunge() -> NoReturn:
    """Function supposed to be used when creating Python executable scripts."""

    parser = ArgumentParser(description="The Befunge CLI.")

    parser.add_argument(
        "-f",
        "--file",
        required=False,
        default=None,
        type=Path,
    )
    parser.add_argument(
        "-o",
        "--destination-binary",
        required=False,
        default=None,
        type=Path,
    )

    args = parser.parse_args()
    befunge = Befunge()

    cli_esolang_run(befunge, args.file, args.destination_binary)
