from rich.text import Text

from packages.shared.constants import CATEGORIES

from ..state import State
from .confirm import render_confirm
from .entry_detail import render_entry_detail
from .entry_list import render_entry_list, term_size
from .input import make_panel, render_input
from .picker import render_picker
from .welcome import render_welcome

__all__ = [
    "render",
    "render_welcome",
    "render_input",
    "render_picker",
    "render_confirm",
    "render_entry_list",
    "render_entry_detail",
]


def render(s: State):
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
        from packages.database.repository import Repository
        from packages.shared.config import settings

        repo = Repository(settings.db_path)
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
