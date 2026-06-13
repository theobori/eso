"""The esolang module."""

from abc import ABC, abstractmethod
from pathlib import Path

from eso.metadata import EsolangMetadata


class Esolang(ABC):
    """This is the interface for the implementation of esoteric languages."""

    metadata: EsolangMetadata

    @abstractmethod
    def eval(self, program: str) -> None:
        """Evaluates the given program.

        Args:
            program (str): The program.
        """

    @abstractmethod
    def compile(self, program: str, destination_filepath: Path) -> None:
        """Compiles the given program.

        Args:
            program (str): The program.
            destination_filepath (Path): The destination filepath of the compiled program.
        """
