"""The brainfuck test module."""

from pathlib import Path
import unittest
import contextlib
import io
import os

from eso import Brainfuck, BrainfuckConfiguration
from eso.exceptions import EsolangExecutionError

HELLO_WORLD_PROGRAM = """[ This program prints "Hello World!" and a newline to the screen, its
  length is 106 active command characters. [It is not the shortest.]

  This loop is an "initial comment loop", a simple way of adding a comment
  to a BF program such that you don't have to worry about any command
  characters. Any ".", ",", "+", "-", "<" and ">" characters are simply
  ignored, the "[" and "]" characters just have to be balanced. This
  loop and the commands it contains are ignored because the current cell
  defaults to a value of 0; the 0 value causes this loop to be skipped.
]
++++++++               Set Cell #0 to 8
[
    >++++               Add 4 to Cell #1; this will always set Cell #1 to 4
    [                   as the cell will be cleared by the loop
        >++             Add 2 to Cell #2
        >+++            Add 3 to Cell #3
        >+++            Add 3 to Cell #4
        >+              Add 1 to Cell #5
        <<<<-           Decrement the loop counter in Cell #1
    ]                   Loop till Cell #1 is zero; number of iterations is 4
    >+                  Add 1 to Cell #2
    >+                  Add 1 to Cell #3
    >-                  Subtract 1 from Cell #4
    >>+                 Add 1 to Cell #6
    [<]                 Move back to the first zero cell you find; this will
                        be Cell #1 which was cleared by the previous loop
    <-                  Decrement the loop Counter in Cell #0
]                       Loop till Cell #0 is zero; number of iterations is 8

The result of this is:
Cell No :   0   1   2   3   4   5   6
Contents:   0   0  72 104  88  32   8
Pointer :   ^

>>.                     Cell #2 has value 72 which is 'H'
>---.                   Subtract 3 from Cell #3 to get 101 which is 'e'
+++++++..+++.           Likewise for 'llo' from Cell #3
>>.                     Cell #5 is 32 for the space
<-.                     Subtract 1 from Cell #4 for 87 to give a 'W'
<.                      Cell #3 was set to 'o' from the end of 'Hello'
+++.------.--------.    Cell #3 for 'rl' and 'd'
>>+.                    Add 1 to Cell #5 gives us an exclamation point
>++.                    And finally a newline from Cell #6"""

INFINITE_ASCII_PROGRAM = "+[<+.>]"


XMAS_TREE_PROGRAM = """[xmastree.b -- print Christmas tree
(c) 2016 Daniel B. Cristofani
http://brainfuck.org/]

>>>--------<,[<[>++++++++++<-]>>[<------>>-<+],]++>>++<--[<++[+>]>+<<+++<]<
<[>>+[[>>+<<-]<<]>>>>[[<<+>.>-]>>]<.<<<+<<-]>>[<.>--]>.>>.
"""

TIC_TAC_TOE_PROGRAM = """[tictactoe.b -- play tic-tac-toe
(c) 2020 Daniel B. Cristofani
http://brainfuck.org/
This program is licensed under a Creative Commons Attribution-ShareAlike 4.0
International License (http://creativecommons.org/licenses/by-sa/4.0/).]

--->--->>>>->->->>>>>-->>>>>>>>>>>>>>>>>>+>>++++++++++[
  <<++[
    --<+<<+<<+>>>>[
      >[<->>+++>>[-]+++<<<+[<++>>+<--]]+>+++++[>>+++++++++<<-]
      >>++++.[-]>>+[<<<<+>>+>>-]<<<<<<[>+<-]<<
    ]++++++++++.[-]>++
  ]-->>[-->[-]>]<<[
    >>--[
      -[
        -[
          -----[>+>+++++++<<+]-->>-.----->,[<->-]<[[<]+[->>]<-]<[<<,[-]]>>>>
        ]>
      ]<[
        >-[+<+++]+<+++[+[---->]+<<<<<<[>>]<[-]]
        >[<+[---->]++[<]<[>]>[[>]+>+++++++++<<-[<]]]>[>>>>]
      ]<[
        -[[>+>+<<-]>[<+>-]++>+>>]<[<<++[-->>[-]]>[[-]>[<<+>>-]>]]
      ]<[
        [[<<]-[>>]<+<-]>[-<+]<<[<<]-<[>[+>>]>[>]>[-]]
        >[[+>>]<-->>[>]+>>>]
      ]<[
        -[
          --[+<<<<--[+>[-]>[<<+>+>-]<<[>>+<<-]]++[>]]
          <<[>+>+<<-]>--[<+>-]++>>>
        ]<[<<<[-]+++>[-]>[<+>>>+<<-]+>>>]
      ]<[
        +[[<]<<[<<]-<->>+>[>>]>[>]<-]+[-<+]<++[[>+<-]++<[<<->>+]<++]<
        <<<<<<      +> > >+> > >+[
        <<<               ->+>+>+[
        <<<<<<<   +>->+> > >->->+[
        <<<<<         ->+>+> >+>+[
        <<<<            ->->+>->+[
        <<<<<<<<+>-> >+> > >->+>+[
        <<<<<         -> >+> >->+[
        <<<<            +>->+> >+]]]]]]]
        +++[[>+<-]<+++]--->>[-[<->-]<++>>]++[[<->-]>>]>[>]
      ]<
    ]
  ]<
]

[This program plays tic-tac-toe. I've given it the first move. It needs
interactive i/o, e.g. a command-line brainfuck interpreter or a brainfuck
compiler that produces command-line executables. At the '>' prompt, enter
the number of an empty space, followed by a linefeed, to play a move there.]

"""


class TestBrainfuck(unittest.TestCase):
    """Represents the Brainfuck test cases."""

    def test_eval_stdout_output(self):
        """Test the brainfuck stdout outputs"""

        brainfuck = Brainfuck()

        interpreter_stdout = io.StringIO()
        with contextlib.redirect_stdout(interpreter_stdout):
            brainfuck.eval(HELLO_WORLD_PROGRAM)

        self.assertEqual(interpreter_stdout.getvalue(), "Hello World!\n")

    def test_eval_wrapping(self):
        """Test the memory wrapping"""

        configuration = BrainfuckConfiguration(
            enable_memory_wrapping=True,
            enable_memory_wrapping_protection=True,
        )
        brainfuck = Brainfuck(configuration)

        with self.assertRaises(EsolangExecutionError):
            brainfuck.eval(INFINITE_ASCII_PROGRAM)

    def test_compile(self):
        """Test the compilation of multiple programs"""

        configuration = BrainfuckConfiguration(
            enable_memory_wrapping=True,
            enable_memory_wrapping_protection=True,
        )

        for program in (
            HELLO_WORLD_PROGRAM,
            INFINITE_ASCII_PROGRAM,
            XMAS_TREE_PROGRAM,
            TIC_TAC_TOE_PROGRAM,
        ):
            destination_filepath = Path("eso_tmp_binary")
            brainfuck = Brainfuck(configuration)
            brainfuck.compile(program, destination_filepath)

            os.remove(destination_filepath)
