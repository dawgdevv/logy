from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, Static


class MenuCard(Static):
    def __init__(self, title: str, desc: str, key: str) -> None:
        self.action_key = key
        super().__init__(
            f"[bold cyan]{key}[/]  [bold]{title}[/]  —  {desc}",
        )

    def on_click(self) -> None:
        if self.action_key:
            self.app.action_switch_screen(self.action_key)


class HomeScreen(Screen):
    BINDINGS = [
        ("l", "switch_screen('log')", "Log"),
        ("r", "switch_screen('history')", "Recent"),
        ("p", "switch_screen('projects')", "Projects"),
        ("s", "switch_screen('search')", "Search"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Vertical(
            Label("\n\n", classes="spacer"),
            Label("[bold cyan]logy[/bold cyan]  [dim]v1.0[/dim]", classes="title"),
            Label("[italic dim]Terminal-first professional memory[/italic dim]", classes="tagline"),
            Label("\n", classes="spacer"),
            Label("What did you work on today?", classes="question"),
            Label("", classes="spacer"),
            MenuCard("Daily Log", "What did you build or learn?", "log"),
            MenuCard("Project", "Log work for a specific project", "projects"),
            MenuCard("Hard Problem", "Solved something tough?", "log"),
            MenuCard("Recent Entries", "Browse your history", "history"),
            Label("", classes="spacer"),
            Label("  [dim]l o g · r e c e n t · p r o j e c t s[/dim]", classes="hint"),
        )
        yield Footer()

    CSS = """
    Screen {
        align: center middle;
    }
    Vertical {
        align: center middle;
        width: 60;
    }
    .title {
        text-style: bold;
        color: cyan;
        text-align: center;
    }
    .tagline {
        text-align: center;
    }
    .question {
        text-style: bold;
        text-align: center;
    }
    .hint {
        text-align: center;
    }
    MenuCard {
        padding: 0 2;
        margin: 0 0;
    }
    MenuCard:hover {
        color: cyan;
    }
    """
