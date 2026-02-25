"""The esolang module."""

from typing import NoReturn
from abc import ABC, abstractmethod

from eso.metadata import EsolangMetadata


class Esolang(ABC):
    """This is the interface for the implementation of esoteric languages."""

    metadata: EsolangMetadata

    @abstractmethod
    def eval(self, program: str) -> NoReturn:
        """Evaluates the given program.

        Args:
            program (str): The program.
        """

    @abstractmethod
    def compile(self, program: str) -> NoReturn:
        """Compiles the given program.

        Args:
            program (str): The program.
        """
