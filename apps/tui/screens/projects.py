from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, Label

from packages.database.repository import Repository
from packages.shared.config import settings

repo = Repository(settings.db_path)


class ProjectScreen(Screen):
    BINDINGS = [
        ("escape", "go_home", "Back"),
        ("r", "refresh", "Refresh"),
        ("n", "new_project", "New"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Horizontal(
            Vertical(
                Label("[bold]Projects[/bold]", classes="title"),
                DataTable(id="projects-table"),
                id="left",
            ),
            Vertical(
                Label("[bold]Timeline[/bold]", classes="title"),
                Vertical(id="timeline"),
                id="right",
            ),
            id="main",
        )
        yield Footer()

    CSS = """
    #main {
        margin: 1 2;
    }
    #left {
        width: 1fr;
        margin: 0 1;
    }
    #right {
        width: 2fr;
        margin: 0 1;
    }
    .title {
        text-align: center;
    }
    DataTable {
        height: 1fr;
    }
    #timeline {
        height: 1fr;
        overflow: auto;
    }
    """

    def on_mount(self) -> None:
        self._load_projects()

    def action_go_home(self) -> None:
        self.app.switch_screen("home")

    def action_refresh(self) -> None:
        self._load_projects()

    def action_new_project(self) -> None:
        def on_submit(name: str) -> None:
            if name:
                repo.create_entry(content="", project_name=name, category="other")
                self._load_projects()

        self.app.push_screen(NewProjectDialog(on_submit))

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        project_name = event.row.get("Project", "")
        if project_name:
            self._show_timeline(project_name)

    def _load_projects(self) -> None:
        table = self.query_one("#projects-table", DataTable)
        table.clear()
        table.add_columns("ID", "Project", "Entries", "Updated")

        projects = repo.get_projects()
        for project in projects:
            table.add_row(
                str(project.id),
                project.name,
                str(len(project.entries)),
                project.updated_at.strftime("%Y-%m-%d"),
            )

    def _show_timeline(self, project_name: str) -> None:
        container = self.query_one("#timeline", Vertical)
        container.remove_children()

        project = repo.get_project_by_name(project_name)
        if not project:
            return

        entries = sorted(project.entries, key=lambda e: e.created_at)
        for entry in entries:
            date = entry.created_at.strftime("%b %d, %Y")
            label = Label(f"  [dim]{date}[/dim]  {entry.content[:80]}")
            container.mount(label)


class NewProjectDialog(Screen):
    def __init__(self, callback) -> None:
        self._callback = callback
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("[bold]New Project[/bold]"),
            Input(placeholder="Project name", id="project-name"),
            Horizontal(
                Button("Create", id="create", variant="primary"),
                Button("Cancel", id="cancel"),
            ),
        )

    CSS = """
    Vertical {
        align: center middle;
        width: 40;
        height: 10;
    }
    Horizontal {
        align: center middle;
    }
    Button {
        margin: 1 1;
    }
    """

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create":
            name = self.query_one("#project-name", Input).value
            self._callback(name)
            self.app.pop_screen()
        elif event.button.id == "cancel":
            self.app.pop_screen()
