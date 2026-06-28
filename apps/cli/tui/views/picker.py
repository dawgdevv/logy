from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from ..state import State
from .input import header_block, make_panel


def render_picker(s: State, w: int, h: int, title: str, options: list[str]) -> Panel:
    title_text = Text(title, style="bold")

    items: list[Text] = []
    for i, opt in enumerate(options):
        if i == s.menu_idx:
            items.append(Text(f"  →  {opt}", style="bold cyan"))
        else:
            items.append(Text(f"     {opt}", style="dim"))

    hint = Text("  ↑↓ · ↵ select · Esc back", style="italic dim")

    content = Group(header_block(), Text(""), title_text, Text(""), *items, Text(""), hint)
    return make_panel(content, w, h)
