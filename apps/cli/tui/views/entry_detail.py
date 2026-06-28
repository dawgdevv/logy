from rich.console import Group
from rich.text import Text

from ..state import State
from .entry_list import _entry_label, render_entry_list
from .ui import divider, footer_hint, shell_panel


def _detail_max_visible(h: int) -> int:
    return max(h - 12, 1)


def _detail_lines(entry, width: int) -> list[str]:
    wrap_width = max(width - 6, 20)
    lines: list[str] = []
    for paragraph in entry.content.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        words = paragraph.split(" ")
        current = ""
        for word in words:
            if not current:
                current = word
            elif len(current) + 1 + len(word) <= wrap_width:
                current = f"{current} {word}"
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines or [""]


def clamp_detail_scroll(s: State, max_visible: int, line_count: int) -> None:
    max_scroll = max(line_count - max(max_visible, 1), 0)
    s.detail_scroll = min(max(s.detail_scroll, 0), max_scroll)


def move_detail_scroll(s: State, delta: int, max_visible: int, line_count: int) -> None:
    s.detail_scroll += delta
    clamp_detail_scroll(s, max_visible, line_count)


def render_entry_detail(s: State, w: int, h: int):
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

    content_lines = _detail_lines(entry, w)
    max_display = _detail_max_visible(h)
    clamp_detail_scroll(s, max_display, len(content_lines))
    display_lines = content_lines[s.detail_scroll : s.detail_scroll + max_display]
    content_text = Text()
    for i, line in enumerate(display_lines):
        content_text.append(f"  {line}", style="white")
        if i < len(display_lines) - 1:
            content_text.append("\n")

    visible_end = min(s.detail_scroll + max_display, len(content_lines))
    status = Text()
    status.append(f"  lines {s.detail_scroll + 1}-{visible_end}/{len(content_lines)}", style="dim")
    if s.detail_scroll:
        status.append(f"  ·  ↑ {s.detail_scroll} above", style="dim italic")
    below = len(content_lines) - visible_end
    if below:
        status.append(f"  ·  ↓ {below} below", style="dim italic")

    hint = footer_hint(("↑↓", "scroll"), ("PgUp/PgDn", "page"), ("↵/Esc", "back"))

    parts = [
        header_t,
        meta_t,
        status,
        divider(w),
        content_text,
        divider(w),
        hint,
    ]
    group = Group(*parts)
    return shell_panel(
        group,
        w,
        h,
        title=Text(" entry ", style="bold cyan"),
    )
