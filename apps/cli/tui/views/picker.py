from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from ..state import State
from .input import make_panel
from .ui import divider, footer_hint, header_block


def render_picker(s: State, w: int, h: int, title: str, options: list[str]) -> Panel:
    title_text = Text(f"  {title}", style="bold")

    items: list[Text] = []
    for i, opt in enumerate(options):
        if i == s.menu_idx:
            items.append(Text(f"  ▶  {opt}", style="bold cyan"))
        else:
            items.append(Text(f"     {opt}", style="dim"))

    hint = footer_hint(("↑↓", "move"), ("↵", "select"), ("Esc", "back"))

    content = Group(
        header_block("Choose"), Text(""), title_text, divider(w), *items, divider(w), hint
    )
    return make_panel(content, w, h)
