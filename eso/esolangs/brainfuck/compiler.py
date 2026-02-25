"""The brainfuck compiler module."""

import os

from pathlib import Path
import shutil
from uuid import uuid4
from typing import NoReturn, Optional
from os.path import dirname

from distutils.ccompiler import new_compiler

from eso.esolangs.brainfuck.configuration import BrainfuckConfiguration
from eso.esolangs.brainfuck.preprocessing import preprocessing

DEFAULT_ARTIFACTS_BASEDIR = "eso_build"


def generate_c_code(program: str, configuration: BrainfuckConfiguration) -> str:
    """Generates C code from Brainfuck program.

    Args:
        program (str): The Brainfuck program.
        configuration (BrainfuckConfiguration): The runtime configuration.

    Returns:
        str: The generated C code.
    """

    code_lines = [
        f"""#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static unsigned char memory[{configuration.memory_size}];
static unsigned int ptr = 0;"""
    ]

    if configuration.enable_memory_wrapping:
        code_lines.append(
            f"""static void fix_ptr() {{
int has_wrapping = (ptr < 0 || ptr >= {configuration.memory_size});
ptr = ptr % {configuration.memory_size};"""
        )

        if configuration.enable_memory_wrapping_protection:
            code_lines.append(
                """if (has_wrapping && memory[ptr] != 0) {
        fprintf(stderr, \"The pointer points to unfree cell after wrapping\\n\");
        exit(1);
    }
}"""
            )
        else:
            code_lines.append("}")

    code_lines.append(
        """int main(int argc, char **argv) {
memset(memory, 0, sizeof(memory));
int ch;"""
    ),

    brackets = preprocessing(program)

    for i, ch in enumerate(program):
        match ch:
            case ">":
                code_lines.append("ptr += 1;")
                if configuration.enable_memory_wrapping:
                    code_lines.append("fix_ptr();")
            case "<":
                code_lines.append("ptr -= 1;")
                if configuration.enable_memory_wrapping:
                    code_lines.append("fix_ptr();")
            case "+":
                code_lines.append("memory[ptr] = (memory[ptr] + 1) % 256;")
            case "-":
                code_lines.append("memory[ptr] = (memory[ptr] - 1) % 256;")
            case ".":
                code_lines.append('printf("%c", memory[ptr]);')
            case ",":
                code_lines.append("ch = getchar();")
                code_lines.append("memory[ptr] = (ch == 10) ? 0 : ch;")
            case "[":
                code_lines.append(f"_{i}:")
                code_lines.append(f"if (memory[ptr] == 0) {{ goto _{brackets[i]}; }}")
            case "]":
                code_lines.append(f"_{i}:")
                code_lines.append(f"if (memory[ptr] != 0) {{ goto _{brackets[i]}; }}")

    code_lines.append("return 0;")
    code_lines.append("}")

    code = "\n".join(code_lines)

    return code


def compile(
    program: str,
    destination_filepath: Path,
    configuration: BrainfuckConfiguration,
    artifacts_basedir: Optional[Path] = DEFAULT_ARTIFACTS_BASEDIR,
    remove_artifacts: bool = True,
) -> NoReturn:
    """Compile the Brainfuck program for your platform using a C compiler.
    I recommend to install gcc and ld if you don't have them on your system.

    Args:
        program (str): The Brainfuck program.
        destination_filepath (Path): The destination of the executable file.
        configuration (BrainfuckConfiguration): The runtime configuration.
        artifacts_basedir (Optional[Path], optional): The directory to store artifacts, C and object files. Defaults to DEFAULT_ARTIFACTS_BASEDIR.
        remove_artifacts (bool, optional): If true, it will remove artifacts produced. Defaults to True.
    """

    c_code = generate_c_code(program, configuration)

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
