from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from ..state import State
from .input import header_block, make_panel


def render_confirm(s: State, w: int, h: int, message: str) -> Panel:
    msg = Text(message, style=s.status_style)
    cont = Text("Press any key to continue", style="dim")

    content = Group(header_block(), Text(""), msg, Text(""), cont)
    return make_panel(content, w, h)
