"""The brainz test module."""

import unittest

from eso import Brainz


PROGRAMS = (
    (
        "FF 09 F0 9C F3 CC 44 45 04 CC A4 C2 20 8A 09 20 4A A0 7F 81 03 C0 92 04 50 22 07 81 55 50 2A AA A0 49 81 38 10",
        "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.",
    ),
    (
        "84 04 08 20",
        "+[,.]",
    ),
)


class Testbrainz(unittest.TestCase):
    """Represents the brainz test cases."""

    def test_codec(self):
        """Test the brainz encoder and decoder"""

        for brainz_program, brainfuck_program in PROGRAMS:
            brainz_program_bytes = bytes(
                int(byte_str, 16) for byte_str in brainz_program.strip().split()
            )

            self.assertEqual(Brainz.decode(brainz_program_bytes), brainfuck_program)
            self.assertEqual(Brainz.encode(brainfuck_program), brainz_program_bytes)
