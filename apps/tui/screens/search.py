from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Input, Label

from packages.database.repository import Repository
from packages.shared.config import settings

repo = Repository(settings.db_path)


class SearchScreen(Screen):
    BINDINGS = [
        ("escape", "go_home", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Vertical(
            Label("[bold]Search Entries[/bold]", classes="title"),
            Input(placeholder="Search query...", id="query"),
            DataTable(id="results-table"),
        )
        yield Footer()

    CSS = """
    Vertical {
        margin: 1 2;
    }
    .title {
        text-align: center;
    }
    Input {
        width: 100%;
        margin: 0 0 1 0;
    }
    DataTable {
        height: 1fr;
    }
    """

    def on_mount(self) -> None:
        self.query_one("#query", Input).focus()

    def action_go_home(self) -> None:
        self.app.switch_screen("home")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "query":
            self._search(event.value)

    def _search(self, query: str) -> None:
        table = self.query_one("#results-table", DataTable)
        table.clear()
        table.add_columns("ID", "Date", "Content", "Project")

        if not query:
            return

        entries = repo.search_entries(query)
        for entry in entries:
            date = entry.created_at.strftime("%Y-%m-%d %H:%M")
            content = entry.content[:80].replace("\n", " ")
            project = entry.project.name if entry.project else ""
            table.add_row(str(entry.id), date, content, project)
