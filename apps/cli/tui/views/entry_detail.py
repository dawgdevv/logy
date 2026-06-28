from rich import box
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from ..state import State
from .entry_list import _entry_label, render_entry_list


def render_entry_detail(s: State, w: int, h: int) -> Panel:
    entry = s.selected_entry
    if not entry:
        return render_entry_list(s, w, h)

    date = entry.created_at.strftime("%b %d, %Y  %H:%M")
    label = _entry_label(entry)
    diff = entry.difficulty.value if hasattr(entry.difficulty, "value") else str(entry.difficulty)
    diff_color = {"easy": "green", "medium": "yellow", "hard": "red"}.get(diff, "dim")

    header_t = Text()
    header_t.append(f"  #{entry.id}", style="bold white")
    header_t.append(f"  ·  {date}", style="dim")

    meta_t = Text()
    meta_t.append(f"  {label}", style="bold cyan")
    meta_t.append("  ·  ", style="dim")
    meta_t.append(diff, style=f"bold {diff_color}")

    content_lines = entry.content.split("\n")
    max_display = h - 12
    display_lines = content_lines[:max_display]
    content_text = Text()
    for i, line in enumerate(display_lines):
        content_text.append(f"  {line}", style="white")
        if i < len(display_lines) - 1:
            content_text.append("\n")
    if len(content_lines) > max_display:
        remaining = len(content_lines) - max_display
        content_text.append(f"\n  ...({remaining} more lines)", style="dim italic")

    hint = Text("  ↵ or Esc to go back", style="italic dim")

    parts = [
        Text(""),
        header_t,
        meta_t,
        Text(""),
        Text("  " + "─" * min(w - 10, 50), style="dim"),
        Text(""),
        content_text,
        Text(""),
        hint,
    ]
    group = Group(*parts)
    return Panel(
        group,
        box=box.ROUNDED,
        border_style="cyan",
        width=w,
        height=h,
    )
