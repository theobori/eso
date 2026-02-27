"""The befunge esolang module."""

from pathlib import Path
from typing import NoReturn

from eso.esolang import Esolang, EsolangMetadata
from eso.esolangs.befunge.interpreter import BefungeInterpreter
from eso.exceptions import EsoError


class Befunge(Esolang):
    """This is a controller for the Befunge esoteric language."""

    metadata = EsolangMetadata(
        name="Befunge",
        description="Befunge is a two-dimensional esoteric programming language"
        "The goal is to be as difficult to compile as possible",
        year=1993,
        author="Chris Pressey",
    )

    def eval(self, program: str) -> NoReturn:
        interpreter = BefungeInterpreter(program)
        interpreter.eval()

    def compile(self, program: str, destination_filepath: Path) -> NoReturn:
        raise EsoError(f"The {self.metadata.name} compilation has not been implemented")
