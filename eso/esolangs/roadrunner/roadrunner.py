"""The roadrunner esolang module."""

from eso.esolang import EsolangMetadata
from eso.esolangs.brainfuck.brainfuck_like import BrainfuckLike


class Roadrunner(BrainfuckLike):
    """This is a controller for the Roadrunner esoteric language."""

    metadata = EsolangMetadata(
        name="Roadrunner",
        description="Roadrunner is a Brainfuck clone language. "
        "It is based off of the popular Looney Tunes character Roadrunner, "
        "who, as is fairly well known, pretty much only ever says 'Meep meep!'.",
        year=2015,
        author="Katrina Scialdone",
    )

    substitutes = {
        "meeP": ">",
        "Meep": "<",
        "mEEp": "+",
        "MeeP": "-",
        "MEEP": ".",
        "meep": ",",
        "mEEP": "[",
        "MEEp": "]",
    }
