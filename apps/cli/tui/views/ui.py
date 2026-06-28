from rich import box
from rich.align import Align
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text

APP_NAME = "logy"
APP_VERSION = "v1.0"
APP_TAGLINE = "Terminal-first professional memory"


def truncate(text: str, width: int) -> str:
    if width <= 0:
        return ""
    if len(text) <= width:
        return text
    if width == 1:
        return "…"
    return text[: width - 1] + "…"


def divider(width: int, inset: int = 4, style: str = "dim") -> Text:
    usable = max(width - inset, 8)
    return Text("  " + "─" * usable, style=style)


def header_block(subtitle: str | None = None) -> Group:
    title = Text()
    title.append(APP_NAME, style="bold cyan")
    title.append(" ", style="")
    title.append(APP_VERSION, style="dim white")

    tagline = Text(subtitle or APP_TAGLINE, style="italic dim")
    return Group(title, tagline)


def centered(text: str, style: str = "") -> Text:
    return Text(text, style=style, no_wrap=True)


def shell_panel(
    content: RenderableType,
    width: int,
    height: int,
    *,
    title: str | Text | None = None,
    border_style: str = "cyan",
    center: bool = False,
) -> Panel:
    body = Align.center(content, vertical="middle") if center else content
    return Panel(
        body,
        box=box.ROUNDED,
        border_style=border_style,
        width=width,
        height=height,
        title=title,
        title_align="left",
    )


def footer_hint(*parts: tuple[str, str]) -> Text:
    text = Text("  ")
    for index, (label, description) in enumerate(parts):
        if index:
            text.append("  ")
        text.append(label, style="bold cyan")
        if description:
            text.append(f" {description}", style="dim")
    return text
