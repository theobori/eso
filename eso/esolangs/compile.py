"""The esolangs compile module"""

import os

from pathlib import Path
import shutil
from uuid import uuid4
from typing import NoReturn, Optional
from os.path import dirname

from distutils.ccompiler import new_compiler

DEFAULT_ARTIFACTS_BASEDIR = "eso_build"


def helper_compile(
    c_code: str,
    destination_filepath: Path,
    artifacts_basedir: Optional[Path] = DEFAULT_ARTIFACTS_BASEDIR,
    remove_artifacts: bool = True,
) -> NoReturn:
    """Helper function to compile a C code to an executable file.
    The C code must have a (main function)/(_start symbol).

    Args:
        c_code (str): The C code to compile.
        destination_filepath (Path): The destination of the executable file.
        artifacts_basedir (Optional[Path], optional): The directory to store artifacts, C and object files. Defaults to DEFAULT_ARTIFACTS_BASEDIR.
        remove_artifacts (bool, optional): If true, it will remove artifacts produced. Defaults to True.
    """

    os.makedirs(artifacts_basedir, exist_ok=True)

    filepath = Path(artifacts_basedir, str(uuid4()) + ".c")

    with open(filepath, "w") as f:
        f.write(c_code)

    c_compiler = new_compiler()
    objs_filepaths = c_compiler.compile([filepath])

    c_compiler.link_executable(
        objs_filepaths,
        output_dir=dirname(destination_filepath),
        output_progname=destination_filepath.name,
    )

    if remove_artifacts:
        shutil.rmtree(artifacts_basedir)
