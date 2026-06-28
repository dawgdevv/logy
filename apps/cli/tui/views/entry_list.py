import shutil
from typing import Any

from rich.console import Group
from rich.text import Text

from ..state import State
from .ui import divider, footer_hint, header_block, shell_panel, truncate


def term_size() -> tuple[int, int]:
    t = shutil.get_terminal_size()
    return t.columns, t.lines


def _entry_label(entry: Any) -> str:
    if entry.project:
        return entry.project.name
    if entry.category == "daily":
        return "dailylog"
    if entry.category == "hard_problem":
        return "hard problem"
    return entry.category


def _clamp_scroll(s: State, max_visible: int) -> None:
    total = len(s.entries)
    if total == 0:
        s.entry_idx = 0
        s.entry_scroll = 0
        return

    max_visible = max(max_visible, 1)
    s.entry_idx = min(max(s.entry_idx, 0), total - 1)
    max_scroll = max(total - max_visible, 0)

    if s.entry_idx < s.entry_scroll:
        s.entry_scroll = s.entry_idx
    elif s.entry_idx >= s.entry_scroll + max_visible:
        s.entry_scroll = s.entry_idx - max_visible + 1
    s.entry_scroll = min(max(s.entry_scroll, 0), max_scroll)


def _max_visible(h: int) -> int:
    return max(h - 11, 1)


def move_selection(s: State, delta: int, max_visible: int) -> None:
    if not s.entries:
        return
    s.entry_idx = min(max(s.entry_idx + delta, 0), len(s.entries) - 1)
    _clamp_scroll(s, max_visible)


def jump_selection(s: State, index: int, max_visible: int) -> None:
    if not s.entries:
        return
    s.entry_idx = min(max(index, 0), len(s.entries) - 1)
    _clamp_scroll(s, max_visible)


def _scroll_meter(scroll: int, visible: int, total: int) -> str:
    if total <= visible:
        return "█"

    track = 8
    thumb_size = max(1, round(visible / total * track))
    max_start = track - thumb_size
    start = round(scroll / max(total - visible, 1) * max_start)
    return "░" * start + "█" * thumb_size + "░" * (track - start - thumb_size)


def render_entry_list(s: State, w: int, h: int):
    if not s.entries:
        msg = Text("No entries yet. Start with a daily log or project note.", style="dim")
        hint = footer_hint(("Esc", "back"))
        content = Group(header_block("Recent entries"), Text(""), msg, Text(""), hint)
        return shell_panel(
            content,
            w,
            h,
            title=Text(" history ", style="bold cyan"),
            center=True,
        )

    max_vis = _max_visible(h)
    _clamp_scroll(s, max_vis)
    visible = s.entries[s.entry_scroll : s.entry_scroll + max_vis]
    total = len(s.entries)
    below = max(0, total - (s.entry_scroll + max_vis))
    above = s.entry_scroll

    cw_num = max(2, len(str(total)))
    cw_date = 5
    cw_diff = 1
    cw_label = min(18, max(12, w // 8))
    usable = max(w - 8, 40)
    fixed = 2 + cw_num + 2 + cw_date + 2 + cw_label + 2 + cw_diff
    cw_content = max(min(usable - fixed, 96), 20)

    diff_colors = {"easy": "green", "medium": "yellow", "hard": "red"}

    vis_start = s.entry_scroll + 1
    vis_end = min(s.entry_scroll + max_vis, total)
    title = Text("  ")
    title.append("Recent entries", style="bold cyan")
    title.append(f"  {s.entry_idx + 1}/{total}", style="white")
    title.append(f"  showing {vis_start}-{vis_end}", style="dim")
    if above:
        title.append(f"  ↑{above}", style="dim")
    if below:
        title.append(f"  ↓{below}", style="dim")
    title.append(f"  {_scroll_meter(s.entry_scroll, max_vis, total)}", style="cyan")

    sep = divider(w, inset=8)
    gap = "  "
    hdr = Text()
    hdr.append("  ")
    hdr.append(f"{'#':>{cw_num}}", style="dim")
    hdr.append(gap)
    hdr.append(f"{'Date':<{cw_date}}", style="dim")
    hdr.append(gap)
    hdr.append(f"{'Content':<{cw_content}}", style="dim")
    hdr.append(gap)
    hdr.append(f"{'Label':<{cw_label}}", style="dim")
    hdr.append(gap)
    hdr.append(f"{'':<{cw_diff}}", style="dim")

    rows: list[Text] = []
    for i, entry in enumerate(visible):
        actual_idx = s.entry_scroll + i
        date = entry.created_at.strftime("%m/%d")

        first_line = entry.content.split("\n")[0]
        preview = truncate(first_line, cw_content)
        label = truncate(_entry_label(entry), cw_label)
        diff = (
            entry.difficulty.value if hasattr(entry.difficulty, "value") else str(entry.difficulty)
        )
        dc = diff_colors.get(diff, "dim")
        sel = actual_idx == s.entry_idx
        base_style = "bold white" if sel else "white"
        muted_style = "bold cyan" if sel else "dim"

        row = Text()
        row.append("▶ " if sel else "  ", style="bold cyan" if sel else "dim")

        row.append(f"{actual_idx + 1:>{cw_num}}", style=muted_style)
        row.append(gap)
        row.append(f"{date:<{cw_date}}", style=muted_style)
        row.append(gap)
        row.append(f"{preview:<{cw_content}}", style=base_style)
        row.append(gap)

        label_style = (
            "bold magenta"
            if "hard" in label
            else "bold cyan"
            if label == "dailylog"
            else "bold blue"
        )
        row.append(f"{label:<{cw_label}}", style=label_style if sel else "dim")
        row.append(gap)
        row.append("●", style=f"bold {dc}" if sel else dc)

        rows.append(row)

    footer = footer_hint(
        ("↑↓", "move"),
        ("PgUp/PgDn", "page"),
        ("Home/End", "jump"),
        ("↵", "view"),
        ("Esc", "back"),
    )

    content = Group(title, sep, hdr, *rows, sep, footer)

    return shell_panel(
        content,
        w,
        h,
        title=Text(" history ", style="bold cyan"),
    )
