"""The befunge interpreter module."""

import random
import sys

from typing import NoReturn
from dataclasses import dataclass
from enum import Enum
from collections import deque

from eso.exceptions import EsolangParsingError, EsolangExecutionError
from eso.esolangs.befunge.const import PROGRAM_MAX_H, PROGRAM_MAX_W


@dataclass
class ProgramCounter:
    """Represents a program counter"""

    r: int = 0
    c: int = 0


class Direction(Enum):
    """Represents four directions"""

    # (r, c)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)


DIRECTIONS = (
    Direction.LEFT,
    Direction.RIGHT,
    Direction.UP,
    Direction.DOWN,
)


class BefungeStack(deque):
    def pop(self):
        if len(self) == 0:
            return 0
        return super().pop()


class BefungeInterpreter:
    """This is a implementation of a Befunge esoteric language interpreter."""

    def __init__(
        self,
        program: str,
    ):
        self.__program = [[""] * PROGRAM_MAX_W for _ in range(PROGRAM_MAX_H)]

        lines = program.splitlines()
        self.__h = len(lines)
        if self.__h == 0 or self.__h > PROGRAM_MAX_H:
            raise EsolangParsingError(
                f"The height should be between 1 and {PROGRAM_MAX_H}"
            )

        self.__w = 0
        for r, line in enumerate(lines):
            if (w := len(line)) > self.__w:
                if w > PROGRAM_MAX_W:
                    raise EsolangParsingError(
                        f"The width should be between 1 and {PROGRAM_MAX_W}"
                    )

                self.__w = w

            for c, ch in enumerate(line):
                self.__program[r][c] = ch

        self.__pc = ProgramCounter(r=0, c=0)
        self.__direction = Direction.RIGHT
        self.__st = BefungeStack()
        self.__is_stringmode = False

    def __update_pc(self, direction: Direction) -> NoReturn:
        """Update the program counter.

        Args:
            direction (Direction): The direction to go.
        """

        self.__pc.r = (self.__pc.r + direction.value[0]) % self.__h
        self.__pc.c = (self.__pc.c + direction.value[1]) % self.__w

    def peek_command(self) -> str:
        """Peek the current command needed to be evaluated.

        Returns:
            str: Returns the command.
        """

        return self.__program[self.__pc.r][self.__pc.c]

    def __eval_command(self, command: str) -> NoReturn:
        """Evaluates the given command.

        Args:
            command (str): The command.

        Raises:
            EsolangExecutionError: Error if it tries to divide by zero.
            EsolangExecutionError: Error if there is an invalid ASCII value")
            EsolangExecutionError: Error when the user input is not an integer
        """

        match command:
            case "<":
                self.__direction = Direction.LEFT
            case ">":
                self.__direction = Direction.RIGHT
            case "^":
                self.__direction = Direction.UP
            case "v":
                self.__direction = Direction.DOWN
            case "+":
                self.__st.append(self.__st.pop() + self.__st.pop())
            case "-":
                a, b = self.__st.pop(), self.__st.pop()
                self.__st.append(b - a)
            case "*":
                self.__st.append(self.__st.pop() * self.__st.pop())
            case "/":
                a = self.__st.pop()
                if a == 0:
                    raise EsolangExecutionError("Invalid division by zero")
                b = self.__st.pop()

                self.__st.append(int(b / a))
            case "%":
                a = self.__st.pop()
                if a == 0:
                    raise EsolangExecutionError("Invalid division by zero")
                b = self.__st.pop()

                self.__st.append(int(b % a))
            case "!":
                self.__st.append(1 if self.__st.pop() == 0 else 0)
            case "`":
                a, b = self.__st.pop(), self.__st.pop()
                self.__st.append(1 if b > a else 0)
            case "?":
                self.__direction = random.choice(DIRECTIONS)
            case "_":
                self.__direction = (
                    Direction.LEFT if self.__st.pop() else Direction.RIGHT
                )
            case "|":
                self.__direction = Direction.UP if self.__st.pop() else Direction.DOWN
            case ":":
                a = self.__st.pop()
                self.__st.append(a)
                self.__st.append(a)
            case "\\":
                a, b = self.__st.pop(), self.__st.pop()
                self.__st.append(a)
                self.__st.append(b)
            case "$":
                self.__st.pop()
            case ".":
                print(self.__st.pop(), end="")
            case ",":
                v = self.__st.pop()
                if v < 0 or v > 127:
                    raise EsolangExecutionError("Invalid ASCII value")

                print(chr(v), end="")
            case "g":
                r, c = self.__st.pop(), self.__st.pop()
                if r < 0 or r >= self.__h or c < 0 or c >= self.__w:
                    self.__st.append(0)
                else:
                    self.__st.append(ord(self.__program[r][c]))
            case "p":
                r, c, v = self.__st.pop(), self.__st.pop(), self.__st.pop()
                self.__program[r][c] = chr(v % 256)
            case "&":
                user_input = input()
                if user_input.isdigit() is False:
                    raise EsolangExecutionError(
                        "Invalid user input, it should be an integer"
                    )

                self.__st.append(int(user_input))
            case "~":
                self.__st.append(ord(sys.stdin.read(1)))
            case "#":
                self.__update_pc(self.__direction)
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                self.__st.append(int(command))

    def eval(self) -> NoReturn:
        """Evaluates the program without preprocessing"""

        while True:
            command = self.peek_command()

            if command == '"':
                self.__is_stringmode = not self.__is_stringmode
            elif self.__is_stringmode:
                self.__st.append(ord(command))
            elif command == "@":
                break
            else:
                self.__eval_command(command)

            self.__update_pc(self.__direction)
