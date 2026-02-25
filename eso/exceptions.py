"""The exceptions module"""

from typing import Optional

from eso.metadata import EsolangMetadata


class EsoError(Exception):
    """Eso base error."""


class EsolangError(EsoError):
    """Esolang base error."""

    def __init__(self, message: str, metadata: Optional[EsolangMetadata] = None):
        self.__message = message
        self.__metadata = metadata

    def __str__(self) -> str:
        message = "An error occured." if self.__message is None else self.__message

        if self.__metadata is None:
            return message

        message += f"The esoteric language {self.__metadata.name}"

        return message


class EsolangExecutionError(EsolangError):
    """Esolang base error."""
