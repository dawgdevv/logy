from rich.live import Live

from packages.database.repository import Repository
from packages.shared.config import settings
from packages.shared.constants import CATEGORIES, Difficulty

from .flow import (
    DAILY_FIELDS,
    HARD_PROBLEM_FIELDS,
    _advance_input,
    _finalize_entry,
    push_input,
    push_picker,
)
from .keys import BACKSPACE, CTRL_C, DOWN, ENTER, ESC, UP, read_key
from .state import State
from .views import render
from .views.entry_list import _clamp_scroll, _max_visible, term_size

repo = Repository(settings.db_path)

WELCOME_OPTIONS = [
    ("Daily Log", "What did you build or learn?"),
    ("Project", "Log work for a specific project"),
    ("Hard Problem", "Solved something tough?"),
    ("Recent Entries", "Browse your history"),
]


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
                        s.entry_type = "daily"
                        s.field_idx = 0
                        s.collected = {}
                        s.project_idx = 0
                        push_input(s, DAILY_FIELDS[0][1], DAILY_FIELDS[0][0])
                    elif choice == 1:
                        s.entry_type = "project"
                        projects = repo.get_projects()
                        names = [p.name for p in projects] + ["+ Create new project"]
                        push_picker(s, "project_picker", "Select project:", names, "project_name")
                    elif choice == 2:
                        s.entry_type = "hard_problem"
                        s.field_idx = 0
                        s.collected = {}
                        s.project_idx = 0
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
                elif k == UP and s.input_field == "project_name":
                    s.project_idx = max(0, s.project_idx - 1)
                elif k == DOWN and s.input_field == "project_name":
                    projects = repo.get_projects()
                    max_idx = len(projects)
                    s.project_idx = min(max_idx, s.project_idx + 1)
                elif k == ENTER:
                    if s.input_field == "project_name" and s.project_idx > 0:
                        projects = repo.get_projects()
                        idx = s.project_idx - 1
                        if 0 <= idx < len(projects):
                            s.collected[s.input_field] = projects[idx].name
                        else:
                            s.collected[s.input_field] = s.input_value
                    else:
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
                        _, h = term_size()
                        _clamp_scroll(s, _max_visible(h))
                elif k == DOWN:
                    if s.entry_idx < len(s.entries) - 1:
                        s.entry_idx += 1
                        _, h = term_size()
                        _clamp_scroll(s, _max_visible(h))
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
