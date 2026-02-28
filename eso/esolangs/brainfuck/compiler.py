"""The brainfuck compiler module."""

from pathlib import Path
from typing import NoReturn

from eso.esolangs.brainfuck.configuration import BrainfuckConfiguration
from eso.esolangs.brainfuck.preprocessing import preprocessing
from eso.esolangs.compile import helper_compile

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
static int ptr = 0;"""
    ]

    if configuration.enable_memory_wrapping:
        code_lines.append(
            f"""static void fix_ptr() {{
int has_wrapping = (ptr < 0 || ptr >= {configuration.memory_size});
if (ptr < 0) {{
    ptr = {configuration.memory_size} - 1;
}} else {{
ptr = ptr % {configuration.memory_size};
}}"""
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
) -> NoReturn:
    """Compile the Brainfuck program for your platform using a C compiler.
    I recommend to install gcc and ld if you don't have them on your system.

    Args:
        program (str): The Brainfuck program.
        destination_filepath (Path): The destination of the executable file.
        configuration (BrainfuckConfiguration): The runtime configuration.
    """

    c_code = generate_c_code(program, configuration)

    helper_compile(c_code, destination_filepath)
