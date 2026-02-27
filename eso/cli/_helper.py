"""The helper CLI module"""

import os
import sys

from pathlib import Path
from typing import NoReturn, Optional

from eso.esolang import Esolang
from eso.exceptions import EsoError


def cli_esolang_run(
    esolang: Esolang,
    source_filepath: Optional[Path] = None,
    destination_binary: Optional[Path] = None,
) -> NoReturn:
    """Helper for running the evaluation or the compilation of the program with
    a given Esolang object.

    Args:
        esolang (Esolang): The esoteric language.
        source_file (Optional[Path], optional): The source filepath. Defaults to None.
        destination_binary (Optional[Path], optional): The destination filepath. Defaults to None.
    """

    with os.fdopen(0) if source_filepath is None else open(source_filepath) as f:
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
        print(e, file=sys.stderr)
        sys.exit(1)
