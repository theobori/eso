"""The helper CLI module"""

from argparse import ArgumentParser
import os

from pathlib import Path
from typing import NoReturn, Optional

from eso.esolang import Esolang
from eso.exceptions import EsoError


def cli_create_base_parser(description: Optional[str] = None) -> ArgumentParser:
    """Returns a basic CLI argument parser, common to every Python executable script.

    Args:
        description (Optional[str], optional): A parser description. Defaults to None.

    Returns:
        ArgumentParser: The parser object.
    """

    parser = ArgumentParser()
    if description:
        parser.description = description

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

    return parser


def cli_esolang_run(
    esolang: Esolang,
    source_filepath: Optional[Path] = None,
    destination_binary: Optional[Path] = None,
    open_text_mode: str = "r",
) -> NoReturn:
    """Helper for running the evaluation or the compilation of the program with
    a given Esolang object.

    Args:
        esolang (Esolang): The esoteric language.
        source_file (Optional[Path], optional): The source filepath. Defaults to None.
        destination_binary (Optional[Path], optional): The destination filepath. Defaults to None.

    Raises:
        e: Propagates runtime error.
    """

    with (
        os.fdopen(0, mode=open_text_mode)
        if source_filepath is None
        else open(source_filepath, mode=open_text_mode)
    ) as f:
        program = f.read()

    try:
        if destination_binary is None:
            esolang.eval(program)
        else:
            esolang.compile(program, destination_binary)
            print(
                f"The {esolang.metadata.name} program has been compiled to {destination_binary.absolute()}."
            )
    except EsoError as e:
        raise e
