"""The preprocessing module."""

from collections import deque
from typing import Dict

from eso.exceptions import EsolangParsingError


def preprocessing(program: str) -> Dict[int, int]:
    """Preprocessing the matching brackets positions

    Args:
        program (str): The Brainfuck program.

    Raises:
        EsolangParsingError: Error if unmatched brackets

    Returns:
        Dict[int, int]: The Python dictionnary containing jump positions.
    """

    ans = dict()
    st = deque()

    for i, cell in enumerate(program):
        match cell:
            case "[":
                st.append(i)
            case "]":
                if st:
                    l = st.pop()
                    ans[l] = i
                    ans[i] = l

    if st:
        raise EsolangParsingError("There are unmatched brackets")

    return ans
