from typing import NoReturn, Optional

from eso.esolang import Esolang, EsolangMetadata
from eso.esolangs.brainfuck.configuration import BrainfuckConfiguration
from eso.esolangs.brainfuck.interpreter import BrainfuckInterpreter


class Brainfuck(Esolang):
    """This is a controller for the Brainfuck esoteric language."""

    metadata = EsolangMetadata(
        name="Brainfuck",
        description="Designed to be extremely minimalistic, "
        "the language consists of only eight simple commands, "
        "a data pointer, and an instruction pointer",
        year=1993,
        author="Urban Müller",
    )

    def __init__(self, configuration: Optional[BrainfuckConfiguration] = None):
        self.__c = BrainfuckConfiguration() if configuration is None else configuration

    def eval(self, program: str) -> NoReturn:
        interpreter = BrainfuckInterpreter(program, self.__c, self.metadata)
        interpreter.eval()

    def compile(self, program: str) -> NoReturn:
        pass
