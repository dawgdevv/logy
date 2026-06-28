from rich import box
from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from ..state import State

WELCOME_OPTIONS = [
    ("Daily Log", "What did you build or learn?"),
    ("Project", "Log work for a specific project"),
    ("Hard Problem", "Solved something tough?"),
    ("Recent Entries", "Browse your history"),
]

LOGO_ART = """\
██╗      ██████╗  ██████╗ ██╗   ██╗
██║     ██╔═══██╗██╔════╝ ╚██╗ ██╔╝
██║     ██║   ██║██║  ███╗ ╚████╔╝
██║     ██║   ██║██║   ██║  ╚██╔╝
███████╗╚██████╔╝╚██████╔╝   ██║
╚══════╝ ╚═════╝  ╚═════╝    ╚═╝"""


def _divider(width: int, style: str = "dim") -> Text:
    return Text("─" * min(max(width - 20, 10), 60), style=style)


def render_welcome(s: State, w: int, h: int) -> Panel:
    logo_block = Align.center(Text(LOGO_ART, style="bold cyan"))

    header_meta = Text()
    header_meta.append("v1.0", style="dim white")
    header_meta.append("   ·   ", style="dim")
    header_meta.append("Terminal-first professional memory", style="italic dim")
    header_meta_block = Align.center(header_meta)

    divider = Align.center(_divider(w))

    question = Align.center(Text("What did you work on today?", style="bold"))

    max_label = max(len(label) for label, _ in WELCOME_OPTIONS)
    menu_rows: list[tuple[str, str]] = []
    for i, (label, desc) in enumerate(WELCOME_OPTIONS):
        prefix = "→ " if i == s.menu_idx else "  "
        style = "bold cyan" if i == s.menu_idx else "dim"
        menu_rows.append((f"  {prefix}  {label:<{max_label}}    {desc}", style))

    menu_width = max(len(line) for line, _ in menu_rows)
    menu_text = Text()
    for i, (line, style) in enumerate(menu_rows):
        menu_text.append(line.ljust(menu_width), style=style)
        if i < len(menu_rows) - 1:
            menu_text.append("\n")

    hint = Align.center(Text("↑↓ navigate   ·   ↵ select", style="italic dim"))

    parts = [
        logo_block,
        Text(""),
        header_meta_block,
        Text(""),
        divider,
        Text(""),
        question,
        Text(""),
        menu_text,
        Text(""),
        hint,
    ]
    title = Text.assemble(("powered by ", "bold dim"), ("cognee", "bold cyan"))
    return Panel(
        Align.center(Group(*parts), vertical="middle"),
        box=box.ROUNDED,
        border_style="cyan",
        width=w,
        height=h,
        title=title,
        title_align="left",
    )
