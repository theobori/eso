"""The getch module"""

# See https://github.com/joeyespo/py-getch/blob/master/getch/getch.py
try:
    from msvcrt import getch
except ImportError:
    import sys
    import tty
    import termios

    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def getche():
        fd = sys.stdin.fileno()
        old_attr = termios.tcgetattr(fd)
        try:
            new_attr = termios.tcgetattr(fd)
            new_attr[3] &= ~termios.ICANON
            termios.tcsetattr(fd, termios.TCSANOW, new_attr)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSANOW, old_attr)
        return ch
