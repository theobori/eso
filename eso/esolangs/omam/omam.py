"""The omam esolang module."""

from eso.esolang import EsolangMetadata
from eso.esolangs.brainfuck.brainfuck_like import BrainfuckLike


class Omam(BrainfuckLike):
    """This is a controller for the Omam esoteric language."""

    metadata = EsolangMetadata(
        name="Omam",
        description="Omam is a Brainfuck-equivalent esoteric "
        "programming language where all the commands "
        "are replaced by lyrics from songs by the indie folk "
        'band "Of Monsters And Men."',
        year=2013,
        author="Peter Berg",
    )

    substitutes = {
        "hold your horses now": ">",
        "sleep until the sun goes down": "<",
        "through the woods we ran": "+",
        "deep into the mountain sound": "-",
        "don't listen to a word i say": ".",
        "the screams all sound the same": ",",
        "though the truth may vary": "[",
        "this ship will carry": "]",
    }
