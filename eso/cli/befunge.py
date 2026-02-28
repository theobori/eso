"""The Befunge CLI module."""

import sys

from typing import NoReturn
from argparse import ArgumentParser
from pathlib import Path

from pydantic import ValidationError

from eso import Befunge
from eso.cli._helper import cli_esolang_run
from eso.esolangs.befunge.configuration import BefungeConfiguration
from eso.esolangs.befunge.const import PROGRAM_H, PROGRAM_W
from eso.exceptions import EsoError


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
    parser.add_argument(
        "--grid-width",
        required=False,
        default=PROGRAM_W,
        type=int,
    )
    parser.add_argument(
        "--grid-height",
        required=False,
        default=PROGRAM_H,
        type=int,
    )
    parser.add_argument(
        "--stack-bytes-size",
        required=False,
        default=256,
        type=int,
    )

    args = parser.parse_args()

    parameters = (
        "grid_width",
        "grid_height",
        "stack_bytes_size",
    )

    configuration: BefungeConfiguration
    try:
        configuration = BefungeConfiguration(
            grid_width=args.grid_width,
            grid_height=args.grid_height,
            stack_bytes_size=args.stack_bytes_size,
        )
    except ValidationError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    befunge = Befunge(configuration)

    try:
        cli_esolang_run(befunge, args.file, args.destination_binary)
    except EsoError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
