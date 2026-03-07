"""The eso module."""

from eso.esolangs.brainfuck import Brainfuck, BrainfuckConfiguration
from eso.esolangs.befunge import Befunge, BefungeConfiguration
from eso.esolangs.brainz import Brainz
from eso.esolangs.aaa import AAA
from eso.esolangs.pikalang import Pikalang
from eso.esolangs.lazyfuck import Lazyfuck
from eso.esolangs.detailedfuck import DetailedFuck

__all__ = [
    "Brainfuck",
    "BrainfuckConfiguration",
    "Befunge",
    "BefungeConfiguration",
    "Brainz",
    "AAA",
    "Pikalang",
    "Lazyfuck",
    "DetailedFuck",
]
