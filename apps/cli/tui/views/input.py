from rich import box
from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from packages.database.repository import Repository
from packages.shared.config import settings

from ..state import State
from .ui import centered, footer_hint, header_block, shell_panel

repo = Repository(settings.db_path)


def _wrap_text(text: str, width: int) -> list[str]:
    if width <= 0:
        return [text] if text else [""]
    if not text:
        return [""]

    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        words = paragraph.split(" ")
        current = ""
        for word in words:
            if not current:
                current = word
            elif len(current) + 1 + len(word) <= width:
                current = f"{current} {word}"
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def make_panel(content, width: int, height: int) -> Panel:
    return shell_panel(content, width, height, center=True)


def render_input(s: State, w: int, h: int) -> Panel:
    wrap_width = max(min(w - 12, 56), 20)
    wrapped = _wrap_text(s.input_value, wrap_width)

    cursor = "█" if s.screen != "input_waiting" else ""
    display_lines: list[str] = []
    for i, line in enumerate(wrapped):
        if i == len(wrapped) - 1 and cursor:
            display_lines.append(line + cursor)
        else:
            display_lines.append(line)

    actual_width = max((len(line) for line in display_lines), default=0)
    box_inner = max(actual_width, wrap_width, 24)
    box_width = box_inner + 4

    line_renderables = [Text(line, style="white") for line in display_lines]
    input_content = Group(*line_renderables) if line_renderables else Text("")

    input_box = Panel(
        input_content,
        box=box.SQUARE,
        border_style="white",
        width=box_width,
        padding=(0, 1),
    )

    lines_out = []
    lines_out.append(header_block("Capture"))
    lines_out.append(Text(""))
    lines_out.append(centered(s.input_prompt, "bold"))
    lines_out.append(centered(""))
    lines_out.append(input_box)
    lines_out.append(Text(""))

    if s.input_field == "project_name":
        lines_out.append(centered("Pick existing or create new", "italic dim"))
        projects = repo.get_projects()
        names = [p.name for p in projects]
        if not names:
            lines_out.append(centered("(no projects yet — type to create)", "dim"))
        else:
            options = [f'+ Create "{s.input_value}"' if s.input_value else "+ Create new"]
            options.extend(names)
            if s.project_idx >= len(options):
                s.project_idx = 0
            for i, opt in enumerate(options):
                if i == s.project_idx:
                    lines_out.append(centered(f"  ▶  {opt}", "bold cyan"))
                else:
                    lines_out.append(centered(f"     {opt}", "dim"))

    lines_out.append(Text(""))

    if s.screen != "input_waiting":
        if s.input_field == "project_name":
            lines_out.append(
                Align.center(footer_hint(("Esc", "back"), ("↑↓", "move"), ("↵", "select")))
            )
        else:
            lines_out.append(Align.center(footer_hint(("Esc", "back"), ("↵", "continue"))))
    else:
        lines_out.append(centered(""))

    content = Group(*lines_out)
    return make_panel(content, w, h)
