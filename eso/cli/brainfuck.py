"""The Brainfuck CLI module."""

import sys

from argparse import ArgumentParser, BooleanOptionalAction
from pathlib import Path
from typing import NoReturn

from pydantic import ValidationError

from eso import Brainfuck, BrainfuckConfiguration
from eso.cli._helper import cli_esolang_run
from eso.exceptions import EsoError


def cli_brainfuck() -> NoReturn:
    """Function supposed to be used when creating Python executable scripts."""

    parser = ArgumentParser(description="The Brainfuck CLI.")

    parser.add_argument(
        "--enable-memory-wrapping",
        required=False,
        default=False,
        type=bool,
        action=BooleanOptionalAction,
    )
    parser.add_argument(
        "--enable-memory-wrapping-protection",
        required=False,
        default=False,
        type=bool,
        action=BooleanOptionalAction,
    )
    parser.add_argument(
        "--memory-size",
        required=False,
        default=30_000,
        type=int,
    )
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

    configuration: BrainfuckConfiguration
    try:
        configuration = BrainfuckConfiguration(
            enable_memory_wrapping=args.enable_memory_wrapping,
            enable_memory_wrapping_protection=args.enable_memory_wrapping_protection,
            memory_size=args.memory_size,
        )
    except ValidationError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    brainfuck = Brainfuck(configuration)

    try:
        cli_esolang_run(brainfuck, args.file, args.destination_binary)
    except EsoError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
