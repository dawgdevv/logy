from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Label

from packages.database.repository import Repository
from packages.shared.config import settings

repo = Repository(settings.db_path)


class HistoryScreen(Screen):
    BINDINGS = [
        ("escape", "go_home", "Back"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Vertical(
            Label("[bold]Recent Entries[/bold]", classes="title"),
            DataTable(id="entries-table"),
        )
        yield Footer()

    CSS = """
    Vertical {
        margin: 1 2;
    }
    .title {
        text-align: center;
    }
    DataTable {
        height: 1fr;
    }
    """

    def on_mount(self) -> None:
        self._load_entries()

    def action_go_home(self) -> None:
        self.app.switch_screen("home")

    def action_refresh(self) -> None:
        self._load_entries()

    def _load_entries(self) -> None:
        table = self.query_one("#entries-table", DataTable)
        table.clear()
        table.add_columns("ID", "Date", "Content", "Project", "Difficulty")

        entries = repo.get_entries(limit=100)
        for entry in entries:
            date = entry.created_at.strftime("%Y-%m-%d %H:%M")
            content = entry.content[:60].replace("\n", " ")
            project = entry.project.name if entry.project else ""
            diff = entry.difficulty.value.capitalize()
            table.add_row(str(entry.id), date, content, project, diff)
