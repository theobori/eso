"""The lazyfuck esolang module."""

from eso.esolang import EsolangMetadata
from eso.esolangs.brainfuck.brainfuck_like import BrainfuckLike


class Lazyfuck(BrainfuckLike):
    """This is a controller for the Lazyfuck esoteric language."""

    metadata = EsolangMetadata(
        name="Lazyfuck",
        description="Lazyfuck is a trivial brainfuck substitution that "
        "requires the least possible effort to type on an ergonomic keyboard.",
        year=2023,
        author="D",
    )

    substitutes = {
        "e": ">",
        "t": "<",
        "a": "+",
        "o": "[",
        "i": "]",
        "n": "-",
        "s": ".",
        "r": ",",
    }
