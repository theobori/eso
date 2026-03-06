"""The befunge esolang module."""

from pathlib import Path
from typing import NoReturn, Optional

from eso.esolang import Esolang, EsolangMetadata
from eso.esolangs.befunge.interpreter import BefungeInterpreter
from eso.esolangs.befunge.compiler import compile
from eso.esolangs.befunge.configuration import BefungeConfiguration


class Befunge(Esolang):
    """This is a controller for the Befunge esoteric language."""

    metadata = EsolangMetadata(
        name="Befunge",
        description="Befunge is a two-dimensional esoteric programming language."
        " The goal is to be as difficult to compile as possible.",
        year=1993,
        author="Chris Pressey",
    )

    def __init__(self, configuration: Optional[BefungeConfiguration] = None):
        self.__c = BefungeConfiguration() if configuration is None else configuration

    def eval(self, program: str) -> NoReturn:
        interpreter = BefungeInterpreter(program, self.__c)
        interpreter.eval()

    def compile(self, program: str, destination_filepath: Path) -> NoReturn:
        compile(program, destination_filepath, self.__c)
