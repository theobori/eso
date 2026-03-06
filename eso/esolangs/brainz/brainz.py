"""The brainz esolang module."""

from pathlib import Path
from typing import NoReturn

from eso.esolang import Esolang, EsolangMetadata
from eso.esolangs.brainfuck.brainfuck import Brainfuck
from eso.esolangs.brainfuck.configuration import BrainfuckConfiguration
from eso.exceptions import EsolangParsingError


class Brainz(Esolang):
    """This is a controller for the brainz esoteric language."""

    metadata = EsolangMetadata(
        name="Brainz",
        description="It is brainfuck compressed with Huffman compression",
        year=2023,
        author="None1",
    )

    zeroes_before_one = (
        "+",
        "-",
        ">",
        "<",
        "[",
        "]",
        ".",
        ",",
    )

    zeroes_max = len(zeroes_before_one) - 1

    brainfuck_configuration = BrainfuckConfiguration(
        enable_memory_wrapping=True,
    )

    @staticmethod
    def decode(brainz_program: bytes) -> str:
        """Convert brainz binary code to brainfuck code

        Args:
            brainz_program (bytes): The BrainZ program.

        Raises:
            EsolangParsingError: Error if there are too many zeroes before a one

        Returns:
            str: The Brainfuck program
        """

        ans = ""

        zeroes = 0
        for i, byte in enumerate(brainz_program):
            for bit in range(8):
                left_bit = (byte >> (7 - bit)) & 1
                if left_bit == 1:
                    if zeroes > Brainz.zeroes_max:
                        raise EsolangParsingError(
                            f"Too many zeroes before this one at position {i * 8 + bit}"
                        )
                    ans += Brainz.zeroes_before_one[zeroes]
                    zeroes = 0
                else:
                    zeroes += 1

        return ans

    @staticmethod
    def encode(brainfuck_program: str) -> bytes:
        """Convert brainfuck code to brainz binary code

        Args:
            brainfuck_program (str): The Brainfuck program

        Returns:
            bytes: The Brainz raw bytes
        """

        ans = []

        bits_str = ""
        for command in brainfuck_program:
            zeroes: int

            try:
                zeroes = Brainz.zeroes_before_one.index(command)
            # Skipping non Brainfuck commands
            except ValueError:
                continue

            bits_str += "0" * zeroes + "1"

        n = len(bits_str)
        remaning = 8 - (n % 8)

        if remaning != 0:
            bits_str += "0" * remaning
            n += remaning

        for i in range(0, n, 8):
            byte = int(bits_str[i : i + 8], 2)
            ans.append(byte)

        return bytes(ans)

    def eval(self, program: bytes) -> NoReturn:
        brainfuck_program = self.decode(program)
        brainfuck = Brainfuck(self.brainfuck_configuration)

        brainfuck.eval(brainfuck_program)

    def compile(self, program: bytes, destination_filepath: Path) -> NoReturn:
        brainfuck_program = self.decode(program)
        brainfuck = Brainfuck(self.brainfuck_configuration)

        brainfuck.compile(brainfuck_program, destination_filepath)
