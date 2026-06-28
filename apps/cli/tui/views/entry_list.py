import shutil

from rich import box
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from ..state import State


def term_size() -> tuple[int, int]:
    t = shutil.get_terminal_size()
    return t.columns, t.lines


def _entry_label(entry) -> str:
    if entry.project:
        return entry.project.name
    if entry.category == "daily":
        return "dailylog"
    if entry.category == "hard_problem":
        return "hard problem"
    return entry.category


def _clamp_scroll(s: State, max_visible: int) -> None:
    if s.entry_idx < s.entry_scroll:
        s.entry_scroll = s.entry_idx
    elif s.entry_idx >= s.entry_scroll + max_visible:
        s.entry_scroll = s.entry_idx - max_visible + 1


def _max_visible(h: int) -> int:
    return max(h - 8, 3)


def render_entry_list(s: State, w: int, h: int) -> Panel:
    if not s.entries:
        msg = Text("No entries yet. Go log something!", style="dim")
        hint = Text("Press any key to go back", style="italic dim")
        from ..views.input import header_block

        content = Group(header_block(), Text(""), msg, Text(""), hint)
        return Panel(
            content,
            box=box.ROUNDED,
            border_style="cyan",
            width=w,
            height=h,
        )

    max_vis = _max_visible(h)
    visible = s.entries[s.entry_scroll : s.entry_scroll + max_vis]
    total = len(s.entries)
    below = max(0, total - (s.entry_scroll + max_vis))

    # ── Column widths (fixed, tight) ─────────────────────────────────────────
    cw_num = 4
    cw_date = 6
    cw_diff = 1
    cw_label = 14
    gap = 1
    gap_lg = 2
    usable = w - 4
    fixed = cw_num + gap + cw_date + gap + cw_label + gap_lg + cw_diff + 4
    cw_content = min(max(usable - fixed, 15), 50)

    diff_colors = {"easy": "green", "medium": "yellow", "hard": "red"}

    # ── Title ────────────────────────────────────────────────────────────────
    vis_start = s.entry_scroll + 1
    vis_end = min(s.entry_scroll + max_vis, total)
    title = Text()
    title.append("  Recent Entries", style="bold cyan")
    title.append(f"  ({s.entry_idx + 1}/{total})", style="dim")
    title.append(f"  ·  {vis_start}–{vis_end}", style="dim")

    # ── Separator ────────────────────────────────────────────────────────────
    sep = Text("  " + "─" * usable, style="dim")

    # ── Column header ────────────────────────────────────────────────────────
    g = " " * gap
    g_lg = " " * gap_lg
    hdr = Text()
    hdr.append(f"  {'#':>{cw_num}}{g}", style="dim")
    hdr.append(f"{'Date':<{cw_date}}{g}", style="dim")
    hdr.append(f"{'Content':<{cw_content}}{g_lg}", style="dim")
    hdr.append(f"{'Label':<{cw_label}}{g}", style="dim")
    hdr.append(f"{'':<{cw_diff}}", style="dim")

    # ── Entry rows ────────────────────────────────────────────────────────────
    rows: list[Text] = []
    for i, entry in enumerate(visible):
        actual_idx = s.entry_scroll + i
        date = entry.created_at.strftime("%m/%d")

        first_line = entry.content.split("\n")[0]
        preview = first_line[:cw_content]
        if len(first_line) > cw_content:
            preview = preview[:-1] + "…"

        label = _entry_label(entry)[:cw_label]
        diff = (
            entry.difficulty.value if hasattr(entry.difficulty, "value") else str(entry.difficulty)
        )
        dc = diff_colors.get(diff, "dim")
        dot = "●"
        sel = actual_idx == s.entry_idx

        row = Text()
        if sel:
            row.append("→ ", style="bold cyan")
        else:
            row.append("  ", style="")

        row.append(f"{actual_idx + 1:>{cw_num}}", style="bold white" if sel else "dim")
        row.append(g)
        row.append(f"{date:<{cw_date}}", style="bold" if sel else "dim")
        row.append(g)
        row.append(f"{preview:<{cw_content}}", style="bold white" if sel else "white")
        row.append(g_lg)

        label_style = (
            "bold magenta"
            if "hard" in label
            else "bold cyan"
            if label == "dailylog"
            else "bold blue"
        )
        row.append(f"[{label:<{cw_label - 2}}]", style=label_style if sel else "dim")
        row.append(g)

        row.append(dot, style=f"bold {dc}" if sel else dc)

        rows.append(row)

    # ── Overflow hint ─────────────────────────────────────────────────────────
    overflow_parts: list = []
    if below > 0:
        overflow_parts.append(Text(f"  ↓ {below} more below", style="dim italic"))

    # ── Footer ────────────────────────────────────────────────────────────────
    footer = Text()
    footer.append("  ↑↓", style="bold cyan")
    footer.append(" navigate  ", style="dim")
    footer.append("↵", style="bold cyan")
    footer.append(" view  ", style="dim")
    footer.append("Esc", style="bold cyan")
    footer.append(" back", style="dim")

    content = Group(title, sep, hdr, sep, *rows, *overflow_parts, sep, footer)

    return Panel(
        content,
        box=box.ROUNDED,
        border_style="cyan",
        width=w,
        height=h,
    )
