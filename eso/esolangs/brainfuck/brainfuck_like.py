"""The brainfuck like module."""

from pathlib import Path
from typing import Dict, NoReturn, Optional

from eso.esolangs.brainfuck.brainfuck import Brainfuck
from eso.esolangs.brainfuck.configuration import BrainfuckConfiguration
from eso.exceptions import EsolangError


class BrainfuckLike(Brainfuck):
    """This is a controller for any Brainfuck like esoteric language."""

    # Should stay a dictionnary
    substitutes: Dict[str, str]

    def __init__(self, configuration: Optional[BrainfuckConfiguration] = None):
        self._c = (
            BrainfuckConfiguration(enable_memory_wrapping=True)
            if configuration is None
            else configuration
        )

    def decode(self, program: str) -> str:
        """Convert a program to brainfuck, using the substitutes property.

        Args:
            program (str): The program.

        Returns:
            str: The Brainfuck program.
        """

        if len(self.substitutes) != 8:
            raise EsolangError("There must be 8 substituers")

        substitutes = dict(
            sorted(self.substitutes.items(), key=lambda p: len(p[0]), reverse=True)
        )

        ans = ""
        i = 0
        n = len(program)
        while i < n:
            for old in substitutes:
                n_old = len(old)
                if old == program[i : i + n_old]:
                    ans += substitutes[old]
                    i += n_old
                    break
            else:
                i += 1

        return ans

    def pre_decode(self, program: str) -> str:
        """A kind of parsing function called before decoding the program.

        Args:
            program (str): The program.

        Returns:
            str: The new program.
        """

        return program

    def eval(self, program: str) -> NoReturn:
        brainfuck_program = self.decode(self.pre_decode(program))

        super().eval(brainfuck_program)

    def compile(self, program: str, destination_filepath: Path) -> NoReturn:
        brainfuck_program = self.decode(self.pre_decode(program))

        super().compile(brainfuck_program, destination_filepath)
