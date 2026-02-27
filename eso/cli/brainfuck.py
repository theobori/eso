"""The Brainfuck CLI module."""

from argparse import ArgumentParser
from pathlib import Path
from typing import NoReturn

from eso import Brainfuck, BrainfuckConfiguration
from eso.cli._helper import cli_esolang_run


def cli_brainfuck() -> NoReturn:
    """Function supposed to be used when creating Python executable scripts."""

    parser = ArgumentParser(description="The Brainfuck CLI.")

    parser.add_argument(
        "--enable-memory-wrapping",
        required=False,
        default=None,
        type=bool,
    )
    parser.add_argument(
        "--enable-memory-wrapping-protection",
        required=False,
        default=None,
        type=bool,
    )
    parser.add_argument(
        "--memory-size",
        required=False,
        default=None,
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

    parameters = (
        "enable_memory_wrapping",
        "enable_memory_wrapping_protection",
        "memory_size",
    )

    configuration = BrainfuckConfiguration()
    for parameter in parameters:
        if not getattr(args, parameter, None) is None:
            setattr(configuration, parameter)

    brainfuck = Brainfuck(configuration)

    cli_esolang_run(brainfuck, args.file, args.destination_binary)
