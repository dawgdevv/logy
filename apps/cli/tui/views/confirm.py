from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from ..state import State
from .input import make_panel
from .ui import footer_hint, header_block


def render_confirm(s: State, w: int, h: int, message: str) -> Panel:
    msg = Text(message, style=s.status_style)
    cont = footer_hint(("any key", "continue"))

    content = Group(header_block("Status"), Text(""), msg, Text(""), cont)
    return make_panel(content, w, h)
