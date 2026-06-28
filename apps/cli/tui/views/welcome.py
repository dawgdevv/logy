from rich.align import Align
from rich.console import Group
from rich.text import Text

from packages.shared.config import settings

from ..state import State
from .ui import divider, footer_hint, shell_panel

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

COMPACT_LOGO_ART = "logy / memory console"


def render_welcome(s: State, w: int, h: int):
    show_block_logo = w >= 58 and h >= 22
    logo = Text(LOGO_ART if show_block_logo else COMPACT_LOGO_ART, style="bold cyan")
    logo_block = Align.center(logo)

    header_meta = Text()
    header_meta.append("v1.0", style="dim white")
    header_meta.append("   ·   ", style="dim")
    header_meta.append("Terminal-first professional memory", style="italic dim")
    if show_block_logo:
        header_meta.append("   ·   ", style="dim")
        header_meta.append("memory console", style="dim")
    header_meta_block = Align.center(header_meta)

    rule = Align.center(divider(w, inset=max(18, w // 5)))

    web_url = f"http://{settings.server_host}:{settings.server_port}"
    web_hint = Text()
    web_hint.append("  web dashboard  ", style="bold yellow")
    web_hint.append(web_url, style="underline yellow")
    web_hint.append("  → graph & search", style="dim")
    web_block = Align.center(web_hint)

    question = Align.center(Text("What do you want to capture?", style="bold white"))

    max_label = max(len(label) for label, _ in WELCOME_OPTIONS)
    menu_width = min(max(w - 16, 46), 72)
    desc_width = max(menu_width - max_label - 8, 16)
    menu_rows: list[Text] = []
    for i, (label, desc) in enumerate(WELCOME_OPTIONS):
        selected = i == s.menu_idx
        row = Text()
        row.append("  ▶ " if selected else "    ", style="bold cyan" if selected else "dim")
        row.append(f"{label:<{max_label}}", style="bold cyan" if selected else "white")
        row.append("  ")
        row.append(desc[:desc_width].ljust(desc_width), style="bold cyan" if selected else "dim")
        menu_rows.append(row)

    menu_text = Text()
    for i, row in enumerate(menu_rows):
        menu_text.append_text(row)
        if i < len(menu_rows) - 1:
            menu_text.append("\n")
    menu_block = Align.center(menu_text)

    hint = Align.center(footer_hint(("↑↓", "move"), ("↵", "select"), ("Ctrl-C", "quit")))

    parts = [
        logo_block,
        header_meta_block,
        Text(""),
        rule,
        Text(""),
        web_block,
        Text(""),
        question,
        Text(""),
        menu_block,
        Text(""),
        hint,
    ]
    title = Text.assemble((" powered by ", "bold dim"), ("cognee ", "bold cyan"))
    return shell_panel(
        Group(*parts),
        w,
        h,
        title=title,
        center=True,
    )
