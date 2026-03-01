"""The brainz CLI module."""

import sys

from argparse import ArgumentParser
from pathlib import Path
from typing import NoReturn

from eso import Brainz
from eso.cli._helper import cli_esolang_run
from eso.exceptions import EsoError


def cli_brainz() -> NoReturn:
    """Function supposed to be used when creating Python executable scripts."""

    parser = ArgumentParser(description="The Brainz CLI.")

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

    brainz = Brainz()

    try:
        cli_esolang_run(brainz, args.file, args.destination_binary, "rb")
    except EsoError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
