"""The aaa esolang module."""

from eso.esolang import EsolangMetadata
from eso.esolangs.brainfuck.brainfuck_like import BrainfuckLike
from eso.transform import remove_parenthesis_content


class AAA(BrainfuckLike):
    """This is a controller for the AAA esoteric language."""

    metadata = EsolangMetadata(
        name="AAA",
        description="AAA is a brainfuck-like programming language, "
        "you can only write the letter A in AAA.",
        year=2023,
    )

    substitutes = {
        "AaAa": "-",
        "AAAA": "+",
        "aAaA": ">",
        "AAaa": "<",
        "aaAA": "[",
        "aaaA": "]",
        "aaaa": ",",
        "aAaa": ".",
    }

    def pre_decode(self, program: str) -> str:
        program = remove_parenthesis_content(program)

        ans = ""
        for ch in program:
            if ch.lower() != "a":
                continue
            ans += ch

        return ans
