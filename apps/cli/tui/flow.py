from rich.live import Live

from packages.database.repository import Repository
from packages.shared.config import settings
from packages.shared.constants import CATEGORIES, Difficulty

from .keys import read_key
from .state import State

repo = Repository(settings.db_path)

DAILY_FIELDS = [
    ("content", "What did you build or learn today?"),
]

HARD_PROBLEM_FIELDS = [
    ("content", "What was the problem?"),
    ("solution", "How did you solve it?"),
    ("lessons", "Lessons learned"),
]


def push_input(s: State, prompt: str, field: str) -> None:
    s.input_prompt = prompt
    s.input_value = ""
    s.input_field = field
    s.screen = "input"


def push_picker(s: State, screen: str, title: str, options: list[str], field: str) -> None:
    s.screen = screen
    s.menu_idx = 0
    s.input_field = field


def show_confirm(s: State, live: Live, message: str, style: str = "green") -> None:
    s.screen = "confirm"
    s.status_msg = message
    s.status_style = style
    from .views import render

    live.update(render(s))
    live.refresh()
    read_key()
    s.screen = "welcome"
    s.menu_idx = 0


def _advance_input(s: State, live: Live) -> None:
    if s.collected.get("content") == "":
        show_confirm(s, live, "Nothing logged.", "yellow")
        return

    if s.screen == "input":
        s.screen = "input_waiting"

    if s.entry_type == "hard_problem":
        fields = HARD_PROBLEM_FIELDS
    else:
        fields = DAILY_FIELDS

    next_idx = s.field_idx + 1
    if next_idx < len(fields):
        s.field_idx = next_idx
        push_input(s, fields[next_idx][1], fields[next_idx][0])
        return

    if s.entry_type == "project":
        push_picker(s, "category_picker", "Category:", CATEGORIES, "category")
        return

    _finalize_entry(s, live)


def _finalize_entry(s: State, live: Live) -> None:
    content = s.collected.get("content", "")
    project = s.collected.get("project_name") or None

    if s.entry_type == "daily":
        category = "daily"
        difficulty = Difficulty.medium
    elif s.entry_type == "hard_problem":
        category = "hard_problem"
        difficulty = Difficulty.hard
        parts = [
            f"Problem: {content}",
        ]
        if solution := s.collected.get("solution"):
            parts.append(f"Solution: {solution}")
        if lessons := s.collected.get("lessons"):
            parts.append(f"Lessons: {lessons}")
        content = "\n\n".join(parts)
    else:
        category = s.collected.get("category", "other")
        difficulty = s.collected.get("difficulty", Difficulty.medium)

    entry = repo.create_entry(
        content=content,
        project_name=project,
        category=category,
        difficulty=difficulty,
        tags=None,
    )
    show_confirm(s, live, f"Logged entry #{entry.id}", "bold green")
