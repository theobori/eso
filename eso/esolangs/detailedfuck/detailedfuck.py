"""The detailedfuck esolang module."""

from eso.esolang import EsolangMetadata
from eso.esolangs.brainfuck.brainfuck_like import BrainfuckLike


class DetailedFuck(BrainfuckLike):
    """This is a controller for the DetailedFuck esoteric language."""

    metadata = EsolangMetadata(
        name="DetailedFuck",
        description="DetailedFuck is a clone of Brainfuck. "
        "The goal of DetailedFuck is to allow for easier understandability of brainfuck code.",
        year=2020,
    )

    substitutes = {
        "MOVE THE MEMORY POINTER ONE CELL TO THE RIGHT": ">",
        "MOVE THE MEMORY POINTER ONE CELL TO THE LEFT": "<",
        "INCREMENT THE CELL UNDER THE MEMORY POINTER BY ONE": "+",
        "DECREMENT THE CELL UNDER THE MEMORY POINTER BY ONE": "-",
        "REPLACE THE CELL UNDER THE MEMORY POINTER'S VALUE WITH THE ASCII CHARACTER CODE OF USER INPUT": ",",
        "PRINT THE CELL UNDER THE MEMORY POINTER'S VALUE AS AN ASCII CHARACTER": ".",
        "IF THE CELL UNDER THE MEMORY POINTER'S VALUE IS ZERO INSTEAD OF READING THE NEXT COMMAND IN THE PROGRAM JUMP TO THE CORRESPONDING COMMAND EQUIVALENT TO THE ] COMMAND IN BRAINFUCK": "[",
        "IF THE CELL UNDER THE MEMORY POINTER'S VALUE IS NOT ZERO INSTEAD OF READING THE NEXT COMMAND IN THE PROGRAM JUMP TO THE CORRESPONDING COMMAND EQUIVALENT TO THE [ COMMAND IN BRAINFUCK": "]",
    }
