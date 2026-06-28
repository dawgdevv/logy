import os
import select
import sys
import termios
import tty

# Key constants
CTRL_C = "\x03"
ENTER = "\r"
BACKSPACE = "\x7f"
ESC = "\x1b"
UP = "\x1b[A"
DOWN = "\x1b[B"
HOME = "\x1b[H"
END = "\x1b[F"
PAGE_UP = "\x1b[5~"
PAGE_DOWN = "\x1b[6~"

_poller = None


def read_key() -> str:
    """Read a single keypress with microsecond-precision poll()."""
    global _poller
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setraw(fd)
    if _poller is None:
        _poller = select.poll()
        _poller.register(fd, select.POLLIN)
    try:
        ch = os.read(fd, 1).decode("utf-8", errors="replace")
        if ch == ESC:
            while _poller.poll(500 if len(ch) == 1 else 0) and len(ch) < 8:
                ch += os.read(fd, 1).decode("utf-8", errors="replace")
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
