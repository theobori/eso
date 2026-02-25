"""The preprocessing module."""

from collections import deque
from typing import Dict


def preprocessing(program: str) -> Dict[int, int]:
    """Preprocessing the matching brackets positions

    Args:
        program (str): The Brainfuck program.

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

    return ans
