"""The brainfuck interpreter module."""

import operator

from typing import NoReturn, List, Callable, Optional
from collections import deque

from eso.esolang import EsolangMetadata
from eso.esolangs.brainfuck.configuration import BrainfuckConfiguration
from eso.exceptions import EsolangExecutionError


class BrainfuckInterpreter:
    """This is a implementation of a Brainfuck esoteric language interpreter."""

    def __init__(
        self,
        program: str,
        configuration: BrainfuckConfiguration,
        metadata: Optional[EsolangMetadata] = None,
    ):
        self.__program = program
        self.__program_len = len(program)
        self.__c = configuration
        self.__metadata = metadata

        self.__memory: List[int] = [self.__c.empty_cell_value] * self.__c.memory_size
        self.__ptr = 0
        self.__pc = 0
        self.__brackets = dict()

    def __ptr_move(self, rhs: int, op: Callable) -> int:
        """Move the memory pointer

        Args:
            rhs (int): Right-hand side operand
            op (Callable): A function taking two integer operands

        Raises:
            EsolangExecutionError: Throw an error if the wrapping is enabled
            and the pointer points on a unfree cell after wrapping.

        Returns:
            int: The new pointer value
        """

        ans = op(self.__ptr, rhs)

        if self.__c.enable_memory_wrapping:
            has_wrapping = ans < 0 or ans >= self.__c.memory_size
            ans = ans % self.__c.memory_size

            if (
                self.__c.enable_memory_wrapping_protection
                and has_wrapping
                and self.__memory[ans] != self.__c.empty_cell_value
            ):
                raise EsolangExecutionError(
                    "The pointer points to unfree cell after wrapping", self.__metadata
                )

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

    def __preprocessing(self) -> NoReturn:
        """Preprocessing the matching brackets positions"""

        st = deque()

        for i, cell in enumerate(self.__program):
            match cell:
                case "[":
                    st.append(i)
                case "]":
                    if st:
                        l = st.pop()
                        self.__brackets[l] = i
                        self.__brackets[i] = l

    def __eval(self) -> NoReturn:
        """Evaluates the program without preprocessing"""

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
                    u = input("> ")
                    self.__memory[self.__ptr] = (
                        self.__c.empty_cell_value if u == "" else ord(u[0])
                    )
                case "[":
                    if self.__memory[self.__ptr] == 0:
                        self.__pc = self.__brackets[self.__pc]
                case "]":
                    if self.__memory[self.__ptr] != 0:
                        self.__pc = self.__brackets[self.__pc]

            self.__pc += 1

    def eval(self) -> NoReturn:
        """Evaluates the program with preprocessing"""

        self.__preprocessing()
        self.__eval()
