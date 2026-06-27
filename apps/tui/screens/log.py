from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Select

from packages.database.repository import Repository
from packages.shared.config import settings
from packages.shared.constants import CATEGORIES, Difficulty

repo = Repository(settings.db_path)


class LogScreen(Screen):
    BINDINGS = [
        ("escape", "go_home", "Back"),
        ("ctrl+s", "submit", "Save"),
    ]

    def compose(self) -> ComposeResult:
        projects = repo.get_projects()
        project_options = [("(none)", "(none)")] + [(p.name, p.name) for p in projects]
        default_proj = projects[0].name if projects else "(none)"

        yield Header(show_clock=True)
        yield Vertical(
            Label("[bold]Daily Log[/bold] — What did you build or learn today?", classes="title"),
            Label(""),
            Input(placeholder="What did you build or learn?", id="content"),
            Label(""),
            Horizontal(
                Vertical(
                    Label("Project"),
                    Select(project_options, id="project", value=default_proj),
                ),
                Vertical(
                    Label("Category"),
                    Select(
                        [(c, c) for c in CATEGORIES],
                        id="category",
                        value="feature",
                    ),
                ),
                id="row1",
            ),
            Label(""),
            Horizontal(
                Vertical(
                    Label("Difficulty"),
                    Select(
                        [(d.value, d.value.capitalize()) for d in Difficulty],
                        id="difficulty",
                        value=Difficulty.medium.value,
                    ),
                ),
                Vertical(
                    Label("Tags (comma-separated)"),
                    Input(placeholder="e.g. rust, performance", id="tags"),
                ),
                id="row2",
            ),
            Label(""),
            Button("Save Entry", id="save", variant="primary"),
            Label("", id="status"),
        )
        yield Footer()

    CSS = """
    Vertical {
        width: 70;
        margin: 1 2;
    }
    .title {
        text-align: center;
    }
    #row1, #row2 {
        height: 5;
    }
    #row1 Vertical, #row2 Vertical {
        width: 1fr;
        margin: 0 1;
    }
    Button {
        width: 20;
        align: center middle;
    }
    #status {
        text-align: center;
    }
    """

    def action_go_home(self) -> None:
        self.app.switch_screen("home")

    def action_submit(self) -> None:
        self._save()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self._save()

    def _save(self) -> None:
        content = self.query_one("#content", Input).value
        if not content:
            status = self.query_one("#status", Label)
            status.update("[yellow]Content is required[/yellow]")
            return

        project_input = self.query_one("#project", Select)
        project_name = project_input.value if project_input.value != "(none)" else None

        category = self.query_one("#category", Select).value
        difficulty_str = self.query_one("#difficulty", Select).value
        difficulty = Difficulty(difficulty_str)

        tags_str = self.query_one("#tags", Input).value
        tags = [t.strip() for t in tags_str.split(",")] if tags_str else None

        entry = repo.create_entry(
            content=content,
            project_name=project_name,
            category=category,
            difficulty=difficulty,
            tags=tags,
        )

        status = self.query_one("#status", Label)
        status.update(f"[green]Logged entry #{entry.id}[/green]")

        self.query_one("#content", Input).value = ""
        self.query_one("#tags", Input).value = ""
