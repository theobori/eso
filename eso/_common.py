"""The common module"""

from collections import deque


def remove_parenthesis_content(value: str) -> str:
    """Returns a new string without parenthesis and their content.
    It will only remove valid parenthesis pairs. Time complexity is O(n) even in the worst case.

    Args:
        value (str): String object.

    Returns:
        str: The new string.
    """

    st = deque([""])
    count = 0

    for ch in value:
        if ch == "(":
            count += 1
            st.append("")
        elif ch == ")" and count > 0:
            st.pop()
            count -= 1
            continue

        st[-1] += ch

    out = "".join(st)

    # Remove whitespaces by prevention
    out = " ".join(out.split())

    return out
