import os
import select
import shutil
import sys
import termios
import tty

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from packages.database.repository import Repository
from packages.shared.config import settings
from packages.shared.constants import CATEGORIES, Difficulty

# Key constants
CTRL_C = "\x03"
ENTER = "\r"
BACKSPACE = "\x7f"
ESC = "\x1b"
UP = "\x1b[A"
DOWN = "\x1b[B"


_poller = None


def read_key() -> str:
    """Read a single keypress with microsecond-precision poll()."""
    global _poller
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setraw(fd)
    if _poller is None:
        _poller = select.poll()
        _poller.register(fd, select.POLLIN)
    try:
        ch = os.read(fd, 1).decode("utf-8", errors="replace")
        if ch == ESC:
            if _poller.poll(500):  # 500µs = 0.5ms
                ch += os.read(fd, 1).decode("utf-8", errors="replace")
                if _poller.poll(0):  # pure poll, no wait
                    ch += os.read(fd, 1).decode("utf-8", errors="replace")
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


console = Console()
repo = Repository(settings.db_path)

WELCOME_OPTIONS = [
    ("Daily Log", "What did you build or learn?"),
    ("Project", "Log work for a specific project"),
    ("Hard Problem", "Solved something tough?"),
    ("Recent Entries", "Browse your history"),
]


class State:
    def __init__(self) -> None:
        self.screen = "welcome"
        self.menu_idx = 0
        self.input_prompt = ""
        self.input_value = ""
        self.field_idx = 0
        self.collected: dict = {}
        self.status_msg = ""
        self.status_style = "green"
        self.project_idx = 0
        self.entries: list = []
        self.entry_idx = 0
        self.entry_scroll = 0
        self.selected_entry: dict | None = None


def term_size() -> tuple[int, int]:
    t = shutil.get_terminal_size()
    return t.columns, t.lines


def make_panel(content, width: int, height: int) -> Panel:
    return Panel(
        Align.center(content, vertical="middle"),
        box=box.ROUNDED,
        border_style="cyan",
        width=width,
        height=height,
    )


def centered(text: str, style: str = "") -> Text:
    return Text(text, style=style, no_wrap=True)


def header_block() -> Group:
    title = Text()
    title.append("logy", style="bold cyan")
    title.append("  ", style="")
    title.append("v1.0", style="dim white")

    tagline = Text("Terminal-first professional memory", style="italic dim")

    return Group(title, tagline)


def render_welcome(s: State, w: int, h: int) -> Panel:
    question = Text("What did you work on today?", style="bold")

    items: list[Text] = []
    for i, (label, desc) in enumerate(WELCOME_OPTIONS):
        if i == s.menu_idx:
            items.append(Text(f"  →  {label}  —  {desc}", style="bold cyan"))
        else:
            items.append(Text(f"     {label}  —  {desc}", style="dim"))

    hint = Text("  ↑↓ · ↵ select", style="italic dim")

    parts = [
        header_block(),
        Text(""),
        Text(""),
        question,
        Text(""),
        *items,
        Text(""),
        hint,
    ]
    return make_panel(Group(*parts), w, h)


def render_input(s: State, w: int, h: int) -> Panel:
    lines = []
    lines.append(centered(""))
    lines.append(centered(s.input_prompt, "bold"))
    lines.append(centered(""))

    display = s.input_value if s.input_value else " "
    if s.screen != "input_waiting":
        display = display + "\u2588"
    input_box = Panel(
        Text(display, no_wrap=True),
        box=box.SQUARE,
        border_style="white",
        width=min(w - 8, 60),
        height=3,
        padding=(0, 1),
    )
    lines.append(input_box)
    lines.append(Text(""))

    if s.screen != "input_waiting":
        lines.append(centered("Esc to go back", "dim"))
    else:
        lines.append(centered(""))

    content = Group(*lines)
    return make_panel(content, w, h)


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


def render_confirm(s: State, w: int, h: int, message: str) -> Panel:
    msg = Text(message, style=s.status_style)
    cont = Text("Press any key to continue", style="dim")

    content = Group(header_block(), Text(""), msg, Text(""), cont)
    return make_panel(content, w, h)


def render_entry_list(s: State, w: int, h: int) -> Panel:
    if not s.entries:
        msg = Text("No entries yet. Go log something!", style="dim")
        hint = Text("Press any key to go back", style="italic dim")
        return make_panel(Group(header_block(), Text(""), msg, Text(""), hint), w, h)

    max_visible = h - 10
    if s.entry_idx < s.entry_scroll:
        s.entry_scroll = s.entry_idx
    if s.entry_idx >= s.entry_scroll + max_visible:
        s.entry_scroll = s.entry_idx - max_visible + 1

    visible = s.entries[s.entry_scroll : s.entry_scroll + max_visible]

    title_text = Text("Recent Entries", style="bold")

    items: list[Text] = []
    for i, entry in enumerate(visible):
        actual_idx = s.entry_scroll + i
        date = entry.created_at.strftime("%b %d %H:%M")
        preview = entry.content[:50].replace("\n", " ")
        project = entry.project.name if entry.project else ""
        pname = f"  {project}" if project else ""
        line = f"  {date}  {preview:<50}{pname}"
        if actual_idx == s.entry_idx:
            items.append(Text(f"→ {line}", style="bold cyan"))
        else:
            items.append(Text(f"  {line}", style="dim"))

    hint_text = "  ↑↓ navigate · ↵ view · Esc back"
    if len(s.entries) > max_visible:
        hint_text += f"  ({s.entry_idx + 1}/{len(s.entries)})"
    hint = Text(hint_text, style="italic dim")

    content = Group(header_block(), Text(""), title_text, Text(""), *items, Text(""), hint)
    return make_panel(content, w, h)


def render_entry_detail(s: State, w: int, h: int) -> Panel:
    entry = s.selected_entry
    if not entry:
        return render_entry_list(s, w, h)

    date = entry.created_at.strftime("%Y-%m-%d %H:%M")
    project = entry.project.name if entry.project else "—"
    diff = entry.difficulty.value if hasattr(entry.difficulty, "value") else str(entry.difficulty)
    diff_style = {"easy": "green", "medium": "yellow", "hard": "red"}.get(diff, "dim")

    meta = Text()
    meta.append(f"  {date}", style="dim")
    meta.append(f"  |  {project}", style="cyan")
    meta.append("  |  ", style="dim")
    meta.append(diff, style=diff_style)
    meta.append(f"  |  {entry.category}", style="dim")

    lines = entry.content.split("\n")
    content_lines_padded = [f"  {line}" for line in lines[: h - 14]]
    content_text = Text("\n".join(content_lines_padded), style="white")
    if len(lines) > h - 14:
        content_text.append("\n  ...", style="dim")

    hint = Text("  ↵ or Esc to go back", style="italic dim")

    detail_title = Text("Entry Detail", style="bold")
    parts = [
        header_block(),
        Text(""),
        detail_title,
        Text(""),
        meta,
        Text(""),
        content_text,
        Text(""),
        hint,
    ]
    group = Group(*parts)
    return Panel(
        Align.center(group, vertical="top"),
        box=box.ROUNDED,
        border_style="cyan",
        width=w,
        height=h,
    )


def render(s: State) -> Panel:
    w, h = term_size()
    if s.screen == "welcome":
        return render_welcome(s, w, h)
    if s.screen in ("input", "input_waiting"):
        return render_input(s, w, h)
    if s.screen == "category_picker":
        return render_picker(s, w, h, "Category:", CATEGORIES)
    if s.screen == "difficulty_picker":
        return render_picker(s, w, h, "Difficulty:", ["Easy", "Medium", "Hard"])
    if s.screen == "project_picker":
        projects = repo.get_projects()
        names = [p.name for p in projects] + ["+ Create new project"]
        return render_picker(s, w, h, "Select project:", names)
    if s.screen == "confirm":
        return render_confirm(s, w, h, s.status_msg)
    if s.screen == "entry_list":
        return render_entry_list(s, w, h)
    if s.screen == "entry_detail":
        return render_entry_detail(s, w, h)
    return make_panel(Text(""), w, h)


def push_input(s: State, prompt: str, field: str) -> None:
    s.input_prompt = prompt
    s.input_value = ""
    s.input_field = field
    s.screen = "input"


def push_picker(s: State, screen: str, title: str, options: list[str], field: str) -> None:
    s.screen = screen
    s.menu_idx = 0
    s.input_field = field


DAILY_FIELDS = [
    ("content", "What did you build or learn today?"),
    ("project", "Project (or press Enter to skip)"),
]

HARD_PROBLEM_FIELDS = [
    ("content", "What was the problem?"),
    ("solution", "How did you solve it?"),
    ("lessons", "Lessons learned"),
    ("project", "Project (or press Enter to skip)"),
]


def show_confirm(s: State, live: Live, message: str, style: str = "green") -> None:
    s.screen = "confirm"
    s.status_msg = message
    s.status_style = style
    live.update(render(s))
    live.refresh()
    read_key()
    s.screen = "welcome"
    s.menu_idx = 0


def run_interactive() -> None:
    s = State()

    with Live(render(s), screen=True, auto_refresh=False) as live:
        live.refresh()

        while True:
            k = read_key()

            if k == CTRL_C:
                break

            if s.screen == "welcome":
                if k == UP:
                    s.menu_idx = (s.menu_idx - 1) % len(WELCOME_OPTIONS)
                elif k == DOWN:
                    s.menu_idx = (s.menu_idx + 1) % len(WELCOME_OPTIONS)
                elif k == ENTER:
                    choice = s.menu_idx
                    if choice == 0:
                        s.field_idx = 0
                        s.collected = {}
                        push_input(s, DAILY_FIELDS[0][1], DAILY_FIELDS[0][0])
                    elif choice == 1:
                        projects = repo.get_projects()
                        names = [p.name for p in projects] + ["+ Create new project"]
                        push_picker(s, "project_picker", "Select project:", names, "project_name")
                    elif choice == 2:
                        s.field_idx = 0
                        s.collected = {}
                        push_input(s, HARD_PROBLEM_FIELDS[0][1], HARD_PROBLEM_FIELDS[0][0])
                    elif choice == 3:
                        s.entries = repo.get_entries(limit=200)
                        s.entry_idx = 0
                        s.entry_scroll = 0
                        s.screen = "entry_list"

            elif s.screen in ("input", "input_waiting"):
                if k == ESC:
                    s.screen = "welcome"
                    s.menu_idx = 0
                elif k == ENTER:
                    s.collected[s.input_field] = s.input_value
                    _advance_input(s, live)
                elif k in (BACKSPACE, "\x7f"):
                    s.input_value = s.input_value[:-1]
                elif len(k) == 1:
                    s.input_value += k

            elif s.screen == "category_picker":
                if k == ESC:
                    s.screen = "welcome"
                    s.menu_idx = 0
                elif k == UP:
                    s.menu_idx = (s.menu_idx - 1) % len(CATEGORIES)
                elif k == DOWN:
                    s.menu_idx = (s.menu_idx + 1) % len(CATEGORIES)
                elif k == ENTER:
                    s.collected["category"] = CATEGORIES[s.menu_idx]
                    s.collected["difficulty"] = Difficulty.medium
                    push_picker(
                        s,
                        "difficulty_picker",
                        "Difficulty:",
                        ["Easy", "Medium", "Hard"],
                        "difficulty",
                    )

            elif s.screen == "difficulty_picker":
                diffs = [Difficulty.easy, Difficulty.medium, Difficulty.hard]
                if k == ESC:
                    s.screen = "welcome"
                    s.menu_idx = 0
                elif k == UP:
                    s.menu_idx = (s.menu_idx - 1) % 3
                elif k == DOWN:
                    s.menu_idx = (s.menu_idx + 1) % 3
                elif k == ENTER:
                    s.collected["difficulty"] = diffs[s.menu_idx]
                    _finalize_entry(s, live)

            elif s.screen == "entry_list":
                if k == ESC:
                    s.screen = "welcome"
                    s.menu_idx = 0
                elif not s.entries:
                    pass
                elif k == UP:
                    if s.entry_idx > 0:
                        s.entry_idx -= 1
                elif k == DOWN:
                    if s.entry_idx < len(s.entries) - 1:
                        s.entry_idx += 1
                elif k == ENTER:
                    s.selected_entry = s.entries[s.entry_idx]
                    s.screen = "entry_detail"

            elif s.screen == "entry_detail":
                if k in (ESC, ENTER):
                    s.screen = "entry_list"

            elif s.screen == "project_picker":
                projects = repo.get_projects()
                names = [p.name for p in projects] + ["+ Create new project"]
                if k == ESC:
                    s.screen = "welcome"
                    s.menu_idx = 0
                elif k == UP:
                    s.menu_idx = (s.menu_idx - 1) % len(names)
                elif k == DOWN:
                    s.menu_idx = (s.menu_idx + 1) % len(names)
                elif k == ENTER:
                    if s.menu_idx == len(names) - 1:
                        push_input(s, "New project name:", "project_name")
                    else:
                        s.collected["project_name"] = names[s.menu_idx]
                        push_input(s, "What did you build?", "content")

            live.update(render(s))
            live.refresh()


def _advance_input(s: State, live: Live) -> None:
    if s.collected.get("content") == "":
        show_confirm(s, live, "Nothing logged.", "yellow")
        return

    if s.screen == "input":
        s.screen = "input_waiting"

    fields = DAILY_FIELDS if s.collected.get("solution") is None else HARD_PROBLEM_FIELDS

    next_idx = s.field_idx + 1
    project_name = s.collected.get("project_name")

    if project_name and next_idx >= len(fields):
        push_picker(s, "category_picker", "Category:", CATEGORIES, "category")
    elif not project_name and next_idx >= len(fields):
        push_picker(s, "category_picker", "Category:", CATEGORIES, "category")
    elif next_idx < len(fields):
        s.field_idx = next_idx
        push_input(s, fields[next_idx][1], fields[next_idx][0])
    else:
        push_picker(s, "category_picker", "Category:", CATEGORIES, "category")


def _finalize_entry(s: State, live: Live) -> None:
    content = s.collected.get("content", "")
    project = s.collected.get("project_name") or None
    category = s.collected.get("category", "other")
    difficulty = s.collected.get("difficulty", Difficulty.medium)
    tags = None

    entry = repo.create_entry(
        content=content,
        project_name=project,
        category=category,
        difficulty=difficulty,
        tags=tags,
    )
    show_confirm(s, live, f"Logged entry #{entry.id}", "bold green")
