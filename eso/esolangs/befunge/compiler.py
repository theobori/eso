"""The befunge compiler module."""

from pathlib import Path
from typing import NoReturn

from eso.esolangs.befunge.configuration import BefungeConfiguration
from eso.esolangs.compile import helper_compile
from eso.exceptions import EsolangParsingError

DEFAULT_ARTIFACTS_BASEDIR = "eso_build"


C_CODE_TEMPLATE = """#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static unsigned char program[{{grid_height}}][{{grid_width}}] = {{grid}};

typedef struct {
    signed long int array[{{stack_bytes_size}}];
    int index;
} Stack;

static Stack st;

static signed long int stack_pop() {
    if (st.index == 0) {
        return 0;
    }

    return st.array[--st.index];
}

static void stack_push(signed long int val) {
    st.array[st.index++] = val;
}

static int r, c = 0;
static int is_stringmode = 0;
static int direction = 1;

static void left() {
    c -= 1;
    if (c < 0) {
        c = {{grid_width}} - 1;
    }
}

static void right() {
    c = (c + 1) % {{grid_width}};
}

static void up() {
    r -= 1;
    if (r < 0) {
        r = {{grid_height}} - 1;
    }
}

static void down() {
    r = (r + 1) % {{grid_height}};
}

typedef void (*FuncPtr)( void );

static FuncPtr directions[4] = {left, right, up, down};

int main(int argc, char **av) {
    srand( time( NULL ) );

    char command;
    signed long int a, b, rr, cc, v;

    while (1) {
        command = program[r][c];

        if (command == '\"') {
            is_stringmode = !is_stringmode;
        } else if (is_stringmode) {
            stack_push((signed long int) command);
        } else if (command == '@') {
            break;
        } else {
            switch (command)
            {
            case '<':
                direction = 0;
                break;
            case '>':
                direction = 1;
                break;
            case '^':
                direction = 2;
                break;
            case 'v':
                direction = 3;
                break;
            case '+':
                stack_push(stack_pop() + stack_pop());
                break;
            case '-':
                a = stack_pop();
                b = stack_pop();
                stack_push(b - a);
                break;
            case '*':
                stack_push(stack_pop() * stack_pop());
                break;
            case '/':
                a = stack_pop();
                b = stack_pop();
                stack_push((signed long int) (b / a));
                break;
            case '%':
                a = stack_pop();
                b = stack_pop();
                stack_push((signed long int) (b / a));
                break;
            case '!':
                stack_push(stack_pop() == 0 ? 1 : 0);
                break;
            case '`':
                a = stack_pop();
                b = stack_pop();
                stack_push(b > a ? 1 : 0);
                break;
            case '?':
                direction = rand() % 4;
                break;
            case '_':
                direction = stack_pop() != 0 ? 0 : 1;
                break;
            case '|':
                direction = stack_pop() != 0 ? 2 : 3;
                break;
            case ':':
                a = stack_pop();
                stack_push(a);
                stack_push(a);
                break;
            case '\\\\':
                a = stack_pop();
                b = stack_pop();
                stack_push(a);
                stack_push(b);
                break;
            case '$':
                stack_pop();
                break;
            case '.':
                printf(\"%ld\", stack_pop());
                break;
            case ',':
                v = stack_pop();
                if (v >= 0 && v <= 127) {
                    printf(\"%c\", (char) v);
                }
                break;
            case 'g':
                rr = stack_pop();
                cc = stack_pop();
                if (rr < 0 || rr >= {{grid_height}} || cc < 0 || cc >= {{grid_width}}) {
                    stack_push(0);
                } else {
                    stack_push((signed long int) program[rr][cc]);
                }
                break;
            case 'p':
                rr = stack_pop();
                cc = stack_pop();
                v = stack_pop();

                program[rr][cc] = (unsigned char) (v % 256);
                break;
            case '&':
                signed long int user_input;
                if (scanf(\"%ld\", &user_input) == 1) {
                    stack_push(user_input);
                }
                break;
            case '~':
                stack_push((signed long int) getchar());
                break;
            case '#':
                directions[direction]();
                break;
            case '0':
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                stack_push((signed long int) (command - '0'));
                break;
            default:
                break;
            }
        }
        directions[direction]();
    }

    return 0;
}
"""


def generate_c_code(program: str, configuration: BefungeConfiguration) -> str:
    """Generates C code from befunge program.

    Args:
        program (str): The befunge program.

    Returns:
        str: The generated C code.
    """

    grid = [[" "] * configuration.grid_width for _ in range(configuration.grid_height)]

    lines = program.splitlines()
    h = len(lines)
    if h == 0 or h > configuration.grid_height:
        raise EsolangParsingError(
            f"The height should be between 1 and {configuration.grid_height}"
        )

    for r, line in enumerate(lines):
        w = len(line)
        if w > configuration.grid_width:
            raise EsolangParsingError(
                f"The width should be between 1 and {configuration.grid_width}"
            )

        for c, ch in enumerate(line):
            grid[r][c] = "\\\\" if ch == "\\" else ch

    grid_c = ["{" + ",".join(f"'{x}'" for x in line) + "}" for line in grid]
    grid_c_str = "{" + ", \n".join(grid_c) + "}"

    c_code = (
        C_CODE_TEMPLATE.replace("{{grid}}", grid_c_str)
        .replace("{{grid}}", grid_c_str)
        .replace("{{grid_height}}", str(configuration.grid_height))
        .replace("{{grid_width}}", str(configuration.grid_width))
        # Divide by 4 because each element of the stack is a signed long int.
        # Refering to https://learn.microsoft.com/en-us/cpp/cpp/data-type-ranges?view=msvc-170,
        # a signed long int has a size of 4 bytes.
        .replace("{{stack_bytes_size}}", str(configuration.stack_bytes_size // 4))
    )

    return c_code


def compile(
    program: str,
    destination_filepath: Path,
    configuration: BefungeConfiguration,
) -> NoReturn:
    """Compile the befunge program for your platform using a C compiler.
    I recommend to install gcc and ld if you don't have them on your system.

    This is litteraly cheating, because I just embed the Befunge program next to the C Befunge interpreter.
    I don't intend to make a JIT compiler to support the p command.

    Args:
        program (str): The befunge program.
        destination_filepath (Path): The destination of the executable file.
        configuration (BefungeConfiguration): The runtime configuration.
    """

    c_code = generate_c_code(program, configuration)

    helper_compile(c_code, destination_filepath)
