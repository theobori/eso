"""The exceptions module"""

from typing import Optional


class EsoError(Exception):
    """Eso base error."""


class EsolangError(EsoError):
    """Esolang base error."""

    def __init__(self, message: Optional[str] = None):
        self.__message = message

    def __str__(self) -> str:
        return "An error occured." if self.__message is None else self.__message


class EsolangParsingError(EsolangError):
    """Esolang parsing error."""


class EsolangExecutionError(EsolangError):
    """Esolang execution error."""


class EsolangNotImplementedError(EsoError):
    """Esolang base error."""

    def __init__(self, lang_name: str):
        self.__lang_name = lang_name

    def __str__(self) -> str:
        return f"The {self.__lang_name} implementation has no compiler."
