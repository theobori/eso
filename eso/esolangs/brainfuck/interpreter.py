"""The brainfuck interpreter module."""

import operator
import sys

from typing import NoReturn, List, Callable

from eso.esolangs.brainfuck.configuration import BrainfuckConfiguration
from eso.exceptions import EsolangExecutionError
from eso.esolangs.brainfuck.preprocessing import preprocessing
from eso.getch import getche


class BrainfuckInterpreter:
    """This is a implementation of a Brainfuck esoteric language interpreter."""

    def __init__(
        self,
        program: str,
        configuration: BrainfuckConfiguration,
    ):
        self.__program = program
        self.__program_len = len(program)
        self.__c = configuration

        self.__memory: List[int] = [0] * self.__c.memory_size
        self.__ptr = 0
        self.__pc = 0
        self.__brackets = preprocessing(program)

    def __ptr_move(self, rhs: int, op: Callable) -> int:
        """Move the memory pointer

        Args:
            rhs (int): Right-hand side operand
            op (Callable): A function taking two integer operands

        Raises:
            EsolangExecutionError: Throw an error if the wrapping is enabled
            and the pointer points on a unfree cell after wrapping.

            EsolangExecutionError: Throw an error if the wrapping is disabled
            but wrapping is needed

        Returns:
            int: The new pointer value
        """

        ans = op(self.__ptr, rhs)

        has_wrapping = ans < 0 or ans >= self.__c.memory_size
        if has_wrapping:
            if self.__c.enable_memory_wrapping:
                ans = ans % self.__c.memory_size

                if (
                    self.__c.enable_memory_wrapping_protection
                    and self.__memory[ans] != 0
                ):
                    raise EsolangExecutionError(
                        "The pointer points to unfree cell after wrapping"
                    )
            # handling this because negative indexes are allowed in Python sequences
            else:
                raise EsolangExecutionError("Memory wrapping is disabled")

        return ans

    def __ptr_inc(self) -> int:
        """Increments the memory pointer by one

        Returns:
            int: The new pointer value
        """

        return self.__ptr_move(1, operator.add)

    def __ptr_dec(self) -> int:
        """Decrements the memory pointer by one

        Returns:
            int: The new pointer value
        """
        return self.__ptr_move(1, operator.sub)

    def eval(self) -> NoReturn:
        """Evaluates the program"""

        while self.__pc < self.__program_len:
            match self.__program[self.__pc]:
                case ">":
                    self.__ptr = self.__ptr_inc()
                case "<":
                    self.__ptr = self.__ptr_dec()
                case "+":
                    self.__memory[self.__ptr] = (self.__memory[self.__ptr] + 1) % 256
                case "-":
                    self.__memory[self.__ptr] = (self.__memory[self.__ptr] - 1) % 256
                case ".":
                    print(chr(self.__memory[self.__ptr]), end="")
                case ",":
                    ch = ord(getche())
                    self.__memory[self.__ptr] = 0 if ch == 10 else ch
                case "[":
                    if self.__memory[self.__ptr] == 0:
                        self.__pc = self.__brackets[self.__pc]
                case "]":
                    if self.__memory[self.__ptr] != 0:
                        self.__pc = self.__brackets[self.__pc]

            self.__pc += 1
