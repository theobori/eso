"""The pikalang esolang module."""

from eso.esolang import EsolangMetadata
from eso.esolangs.brainfuck.brainfuck_like import BrainfuckLike


class Pikalang(BrainfuckLike):
    """This is a controller for the Pikalang esoteric language."""

    metadata = EsolangMetadata(
        name="Pikalang",
        description="It is a joke esoteric programming language.",
        year=2014,
        author="Blake Grotewold",
    )

    substitutes = {
        "pipi": ">",
        "pichu": "<",
        "pi": "+",
        "ka": "-",
        "pikachu": ".",
        "pikapi": ",",
        "pika": "[",
        "chu": "]",
    }
