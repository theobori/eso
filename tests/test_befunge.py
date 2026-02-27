"""The befunge test module."""

import unittest
import contextlib
import io

from eso import Befunge


HELLO_WORLD_PROGRAMS = (
    (
        """>              v
v"Hello World!"<
>:v
^,_@""",
        "Hello World!",
    ),
    ('"!dlroW olleH",,,,,,,,,,,,@', "Hello World!"),
    ('"!dlroW olleH">:#,_@', "Hello World!"),
    (
        """89*,52*5*2*1+,92*6*,92*6*,52*1+52**1+,48*,52*8*7+,52*1+52**1+,52*1+52**4+,v
v                                                                         <
>52*52**8+,52*52**,48*1+,@""",
        "Hello World!",
    ),
    (
        """?0|0
0 0  @,,,,,,,,,,,,,_
_0_"!dlroW ,olleH"0|
0                  1
""",
        "Hello, World!",
    ),
)


class TestBefunge(unittest.TestCase):
    """Represents the befunge test cases."""

    def test_eval_stdout_output(self):
        """Test the befunge stdout outputs"""

        befunge = Befunge()

        for hello_world_program, expected_result in HELLO_WORLD_PROGRAMS:
            interpreter_stdout = io.StringIO()
            with contextlib.redirect_stdout(interpreter_stdout):
                befunge.eval(hello_world_program)

            self.assertEqual(interpreter_stdout.getvalue(), expected_result)

    def test_compile(self):
        """Test the compilation of multiple programs"""
