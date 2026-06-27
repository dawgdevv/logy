import shutil

from readchar import key as kc
from readchar import readkey
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from packages.database.repository import Repository
from packages.shared.config import settings
from packages.shared.constants import CATEGORIES, Difficulty

console = Console()
repo = Repository(settings.db_path)

WELCOME_OPTIONS = [
    ("Daily Log", "What did you build or learn?"),
    ("Project", "Log work for a specific project"),
    ("Hard Problem", "Solved something tough?"),
]

SCREEN_NAMES = ["daily_log", "project", "hard_problem"]


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
    readkey()
    s.screen = "welcome"
    s.menu_idx = 0


def run_interactive() -> None:
    s = State()

    with Live(render(s), screen=True, auto_refresh=False) as live:
        live.refresh()

        while True:
            k = readkey()

            if s.screen == "welcome":
                if k == kc.UP:
                    s.menu_idx = (s.menu_idx - 1) % len(WELCOME_OPTIONS)
                elif k == kc.DOWN:
                    s.menu_idx = (s.menu_idx + 1) % len(WELCOME_OPTIONS)
                elif k == kc.ENTER:
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

            elif s.screen in ("input", "input_waiting"):
                if k == kc.ESC:
                    s.screen = "welcome"
                    s.menu_idx = 0
                elif k == kc.ENTER:
                    s.collected[s.input_field] = s.input_value
                    _advance_input(s, live)
                elif k in (kc.BACKSPACE, "\x7f"):
                    s.input_value = s.input_value[:-1]
                elif len(k) == 1:
                    s.input_value += k

            elif s.screen == "category_picker":
                if k == kc.ESC:
                    s.screen = "welcome"
                    s.menu_idx = 0
                elif k == kc.UP:
                    s.menu_idx = (s.menu_idx - 1) % len(CATEGORIES)
                elif k == kc.DOWN:
                    s.menu_idx = (s.menu_idx + 1) % len(CATEGORIES)
                elif k == kc.ENTER:
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
                if k == kc.ESC:
                    s.screen = "welcome"
                    s.menu_idx = 0
                elif k == kc.UP:
                    s.menu_idx = (s.menu_idx - 1) % 3
                elif k == kc.DOWN:
                    s.menu_idx = (s.menu_idx + 1) % 3
                elif k == kc.ENTER:
                    s.collected["difficulty"] = diffs[s.menu_idx]
                    _finalize_entry(s, live)

            elif s.screen == "project_picker":
                projects = repo.get_projects()
                names = [p.name for p in projects] + ["+ Create new project"]
                if k == kc.ESC:
                    s.screen = "welcome"
                    s.menu_idx = 0
                elif k == kc.UP:
                    s.menu_idx = (s.menu_idx - 1) % len(names)
                elif k == kc.DOWN:
                    s.menu_idx = (s.menu_idx + 1) % len(names)
                elif k == kc.ENTER:
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
