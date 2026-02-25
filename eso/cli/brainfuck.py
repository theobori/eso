"""The Brainfuck CLI module."""

import os

from argparse import ArgumentParser
from pathlib import Path

from eso import Brainfuck, BrainfuckConfiguration


def cli_brainfuck():
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

    with os.fdopen(0) if args.file is None else open(args.file) as f:
        program = f.read()

    if args.destination_binary is None:
        brainfuck.eval(program)
    else:
        brainfuck.compile(program, args.destination_binary)
        print(
            f"The {brainfuck.metadata.name} program has been compiled to {args.destination_binary.absolute()}."
        )
