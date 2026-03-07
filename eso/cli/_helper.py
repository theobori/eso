"""The helper CLI module"""

import sys
import os

from argparse import ArgumentParser
from pathlib import Path
from typing import Callable, NoReturn, Optional, Type

from eso.esolang import Esolang
from eso.exceptions import EsoError
from eso.metadata import get_metadata_sentence


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


def cli_generic(
    esolang_class: Type[Esolang],
    open_text_mode: str = "r",
) -> NoReturn:
    """The generic CLI function.

    Args:
        esolang_class (Type[Esolang]): Class types that implements the Esolang interface.
        open_text_mode (str, optional): The file open mode. Defaults to "r".
    """

    description = get_metadata_sentence(esolang_class.metadata)
    parser = cli_create_base_parser(description)
    args = parser.parse_args()

    esolang_obj = esolang_class()

    try:
        cli_esolang_run(esolang_obj, args.file, args.destination_binary, open_text_mode)
    except EsoError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def cli_create_generic_func(esolang_class: Type[Esolang]) -> Callable:
    """Returns a CLI function.

    Args:
        esolang_class (Type[Esolang]): Class types that implements the Esolang interface.

    Returns:
        Callable: The CLI function.
    """

    return lambda: cli_generic(esolang_class)


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
        open_text_mode (str, optional): The file open mode. Defaults to "r".

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
